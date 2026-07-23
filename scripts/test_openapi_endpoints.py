import json
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import ValidationError
from jsonschema.validators import validator_for
from referencing import Registry
import referencing.jsonschema as referencing_jsonschema
from src.conf.configuration import secrets


from src.utility.rest.rest_auth_factory import build_api_key_auth
from src.utility.rest.rest_client_factory import build_rest_client

SERVERS = 'servers'
URL = 'url'
PATHS = 'paths'
PARAMS = 'parameters'
resolved_schemas = dict()
auth = None
API_KEY_NAME = 'Ocp-Apim-Subscription-Key'

HTTP_METHODS = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options'}
results = list({})

_TYPE_FORMAT_DEFAULTS = {
    ('string', 'date-time'): lambda: datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.0000000+00:00'),
    ('string', 'date'):      lambda: datetime.now(timezone.utc).strftime('%Y-%m-%d'),
    ('string', None):        lambda: 'string',
    ('integer', 'int32'):    lambda: 1,
    ('integer', 'int64'):    lambda: 1,
    ('integer', None):       lambda: 1,
    ('number', 'double'):    lambda: 0.01,
    ('number', 'float'):     lambda: 0.01,
    ('number', None):        lambda: 0.01,
    ('boolean', None):       lambda: True,
    ('array', None):         lambda: [],
    ('object', None):        lambda: {},
}

def create_auth(file):
    """Create an authentication object based on environment variables."""
    global auth
    
    auth = build_api_key_auth(API_KEY_NAME, secrets[file])
    return auth

def get_host(data,file):
    """Extract the first server URL from the OpenAPI document."""
    host = data.get(SERVERS, [{}])[0].get(URL, None)
    if not host:
        print(f"No host found in {file}")
        raise ValueError(f"No host found in {file}")
    return host

def get_apis(data,file):
    """Extract path operations from the OpenAPI document."""
    apis = data.get(PATHS, [])
    if not apis:
        print(f"No APIs found in {file}")
        raise ValueError(f"No APIs found in {file}")
    return apis

def generate_value_from_schema(schema: dict) -> object:
    """Generate a valid runtime value from an OpenAPI schema using type/format/enum."""
    enum_values = schema.get('enum')
    if enum_values:
        return enum_values[0]

    schema_type = schema.get('type')
    schema_format = schema.get('format')

    # Array with inline items: generate a one-element list using the items schema.
    if schema_type == 'array':
        items_schema = schema.get('items', {})
        ref = items_schema.get('$ref')
        if ref:
            item_value = resolved_schemas.get(ref.split('/')[-1])
        else:
            item_value = generate_value_from_schema(items_schema)
        return [item_value] if item_value is not None else []

    factory = _TYPE_FORMAT_DEFAULTS.get((schema_type, schema_format)) \
        or _TYPE_FORMAT_DEFAULTS.get((schema_type, None))
    if factory:
        return factory()
    return None


def get_refs(param):
    """Resolve a $ref or array items $ref to a compiled schema value."""
    if param.get('type') == 'array':
        items = param.get('items', {})
        ref = items.get('$ref')
        if ref:
            # Array of known schema objects: wrap in a one-element list.
            item = resolved_schemas.get(ref.split('/')[-1])
            return [item] if item is not None else None
        # Array with inline items type: delegate to generator.
        return generate_value_from_schema(param)
    ref = param.get('$ref')
    if ref:
        schema_name = ref.split('/')[-1]
        resolved_schema = resolved_schemas.get(schema_name)
        if resolved_schema is not None:
            return resolved_schema

def get_schemas(data,file,file_name):
    """Build example payloads from component schemas for request bodies."""
    schemas = data.get('components', {}).get('schemas', {})
    if not schemas:
        print(f"No schemas found in {file}")
        raise ValueError(f"No schemas found in {file}")
    # Pass 1: resolve all primitive schemas (no properties) first so that $ref
    # lookups in pass 2 always find types like Instant, LocalDate, and enums.
    for schema_name, schema in schemas.items():
        if not schema.get('properties'):
            resolved_schemas[schema_name] = generate_value_from_schema(schema)
    # Pass 2: resolve complex schemas iteratively until stable.
    # Multiple iterations are needed when a complex schema (e.g. CreateFlowRequest)
    # references another complex schema (e.g. Sender) that appears later in the spec.
    unresolved_count = None
    for _ in range(len(schemas)):
        current_unresolved = 0
        for schema_name, schema in schemas.items():
            if not schema.get('properties') or str(schema_name).endswith('Response'):
                continue
            request_obj = {}
            for param_name, param in schema.get('properties', {}).items():
                param_example = param.get('example', None)
                if param_example is None:
                    param_example = get_refs(param)
                    # get_refs returns None when the referenced complex schema is not yet resolved.
                    if param_example is None:
                        current_unresolved += 1
                        param_example = generate_value_from_schema(param)
                else:
                    param_example = list(param_example)[0]
                request_obj[param_name] = param_example
            resolved_schemas[schema_name] = request_obj
        # Stop as soon as all $refs resolved or no further progress can be made.
        if current_unresolved == 0 or current_unresolved == unresolved_count:
            break
        unresolved_count = current_unresolved

    with open(f"resolved_schemas_{file_name}.json", 'w') as result_file:
        json.dump(resolved_schemas, result_file, indent=4)
    return resolved_schemas

def build_body(method_obj):
    """Build a request body using pre-resolved component examples."""
    request_body = method_obj.get('requestBody', {})
    content = request_body.get('content', {}).get('application/json', {})
    schema_ref = content.get('schema', {}).get('$ref')
    if schema_ref:
        schema_name = schema_ref.split('/')[-1]
        return resolved_schemas.get(schema_name)
    
def build_api_path(method_obj, api_path):
    """Build an API path by injecting path and query examples."""
    first_query_param = True
    for param in method_obj.get(PARAMS, []):
        param_name = param.get('name')
        if param.get('in') == 'path':
            api_path = api_path.replace(f"{{{param_name}}}", str(param.get('example', '')))
        elif param.get('in') == 'query':
            api_path += ('?' + (f"{param_name}={param.get('example', '')}") if first_query_param else f"&{param_name}={param.get('example', '')}")
            first_query_param = False
    return api_path

def validate_schema(response, method_obj, data):
    """Validate response JSON against the OpenAPI response schema with root-level $ref resolution."""
    schema_ref = method_obj.get('responses', {}).get(str(response.status_code), {}).get('content', {}).get('application/json', {}).get('schema', {}).get('$ref', '')
    if not schema_ref:
        return False

    schema = {'$ref': f"urn:openapi-root{str(schema_ref)}"}
    try:
        root_resource = referencing_jsonschema.DRAFT202012.create_resource(data)
        registry = Registry().with_resource("urn:openapi-root", root_resource)
        validator_cls = validator_for(schema)
        validator = validator_cls(schema=schema, registry=registry)
        validator.validate(response.json())
        print(f"Schema validation OK for {schema_ref}")
        return True
    except ValidationError as exc:
        print(f"Schema validation KO for {schema_ref}: {exc.message}")
        return False
    except Exception as exc: 
        print(f"Schema validation skipped for {schema_ref}: {exc}")
        return False
    
def test_apis(apis, rest_client, data):
    """Test all API operations by building URL, optional body, and executing HTTP calls."""
    for api_path, api_obj in apis.items():
        for method, method_obj in api_obj.items():
            if method.lower() not in HTTP_METHODS:
                continue
            request_path = build_api_path(method_obj, api_path)
            # Build request body from resolved_schemas if the operation declares a requestBody.
            body = build_body(method_obj)
            response = rest_client.request(method.upper(), request_path, json_body=json.dumps(body) if body else None)
            if response.text is not None and response.text != "":
                results.append({"Status code": response.status_code, "Response" : json.loads(response.text), "API Path" : request_path, "Sent body": body, "Valid Schema" : validate_schema(response, method_obj, data)})


def main():
    for file in Path('tmp_fetched').glob('*.json'):
        with open(file, 'r') as f:
            try:
                data = json.load(f)
                # get host from the JSON data
                host = get_host(data, file)
                # get apis from file
                apis = get_apis(data, file)
                file_name = f.name.split('.')[0].split('\\')[-1]
                get_schemas(data, file, file_name)
                create_auth(file_name)
                rest_client = build_rest_client({"url": host, "verify_ssl": True}, auth)
                test_apis(apis, rest_client,data)
                with open(f"results_{file_name}.json", 'w') as result_file:
                    json.dump(results, result_file, indent=4)
                results.clear()
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {file}: {e}")


if __name__ == "__main__":
    main()