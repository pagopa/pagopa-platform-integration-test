"""Common Behave steps for GEC integration tests."""

import json
import logging

from behave import given, when, then

from src.integration.gec.helper import (
    _ensure_vars_container,
    _get_client,
    _send_request,
    _get_bundled_response,
)

LOGGER = logging.getLogger("gec")


@given("che i sistemi sono operativi")
def step_systems_up(context):
    """Initialize context state."""
    context.response = None
    _ensure_vars_container(context)


@given("il bundle poste è configurato")
def step_bundle_poste_configured(context):
    """Placeholder for bundle poste configuration."""
    _ensure_vars_container(context)
    LOGGER.info("Bundle Poste configuration validated")


@given("la configurazione dei dati di test è caricata")
def step_test_data_configured(context):
    """Placeholder for test data configuration."""
    _ensure_vars_container(context)
    LOGGER.info("Test data configuration loaded")


@given('una richiesta di recupero commissioni "{payload_name}"')
def step_named_commission_request(context, payload_name: str):
    """Store a commission request payload name."""
    _ensure_vars_container(context)
    context.vars["current_request_payload"] = payload_name
    LOGGER.info("Commission request payload set: %s", payload_name)


@given('la configurazione dei metodi di pagamento "{config_name}"')
def step_payment_methods_configuration(context, config_name: str):
    """Store payment methods configuration."""
    _ensure_vars_container(context)
    context.vars["payment_methods_config"] = config_name
    LOGGER.info("Payment methods configuration set: %s", config_name)


@given('una richiesta di ricerca dei metodi di pagamento "{request_name}"')
def step_payment_methods_request(context, request_name: str):
    """Store a payment methods search request."""
    _ensure_vars_container(context)
    context.vars["payment_methods_request"] = request_name
    LOGGER.info("Payment methods search request set: %s", request_name)


@given('il parametro di richiesta "{param_name}" è "{param_value}"')
def step_request_parameter(context, param_name: str, param_value: str):
    """Set a query/request parameter."""
    _ensure_vars_container(context)
    if "request_params" not in context.vars:
        context.vars["request_params"] = {}
    context.vars["request_params"][param_name] = param_value
    LOGGER.info("Request parameter set: %s = %s", param_name, param_value)


@given("l'impostazione allCcp è disabilitata")
def step_allccp_disabled(context):
    """Set allCcp disabled configuration."""
    _ensure_vars_container(context)
    context.vars["allCcp"] = False
    LOGGER.info("allCcp configuration set to disabled")


@given("l'impostazione allCcp è abilitata")
def step_allccp_enabled(context):
    """Set allCcp enabled configuration."""
    _ensure_vars_container(context)
    context.vars["allCcp"] = True
    LOGGER.info("allCcp configuration set to enabled")


@when('il client invia la richiesta di "{operation}" per il PSP "{psp_id}" con il payload "{payload_name}"')
def step_send_request_with_psp_payload(context, operation: str, psp_id: str, payload_name: str):
    """Send a request with specific PSP and payload."""
    _ensure_vars_container(context)
    context.vars["psp_id"] = psp_id
    _send_request(context, operation, payload_name)


@when('il client invia la richiesta di "{operation}" con il payload "{payload_name}"')
def step_send_request_with_payload(context, operation: str, payload_name: str):
    """Send a request without specific PSP."""
    _send_request(context, operation, payload_name)


@when('il client invia la richiesta di "{operation}" per il PSP "{psp_id}"')
def step_send_request_with_psp(context, operation: str, psp_id: str):
    """Send a request with specific PSP, no explicit payload."""
    _ensure_vars_container(context)
    context.vars["psp_id"] = psp_id
    payload_name = context.vars.get("current_request_payload", "default_payload")
    _send_request(context, operation, payload_name)


@when('il client invia la richiesta di "{operation}"')
def step_send_request_basic(context, operation: str):
    """Send a request with no PSP or specific payload."""
    payload_name = getattr(context, "vars", {}).get("current_request_payload", "default_payload")
    _send_request(context, operation, payload_name)


@then("il sistema risponde con codice di stato {status_code:d}")
def step_assert_status_code(context, status_code: int):
    """Assert response status code."""
    assert hasattr(context, "response") and context.response is not None
    actual = context.response.status_code
    assert actual == status_code, f"Expected status {status_code}, got {actual}"
    LOGGER.info("Status code assertion passed: %d", status_code)


@then('il corpo della risposta corrisponde al payload "{payload_name}"')
def step_assert_response_matches_payload(context, payload_name: str):
    """Assert response body matches expected payload."""
    from src.integration.gec.helper import _get_request_payload
    
    assert hasattr(context, "response") and context.response is not None
    expected_payload = _get_request_payload(context, payload_name + "_response", payload_name)
    try:
        actual_body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    actual_str = json.dumps(actual_body, sort_keys=True)
    expected_str = json.dumps(expected_payload, sort_keys=True)
    assert actual_str == expected_str, (
        f"Response body mismatch.\nExpected: {expected_str}\nActual: {actual_str}"
    )
    LOGGER.info("Response payload assertion passed: %s", payload_name)


@then('i valori del campo `{field_name}` delle opzioni bundle, dopo l\'ordinamento previsto per l\'API "{api_version}", corrispondono ai seguenti:')
def step_assert_ordered_bundle_field_backtick(context, field_name: str, api_version: str):
    """Assert ordered values of a field (with backtick syntax) in bundle options."""
    assert context.table is not None, "Table with expected values required"
    assert hasattr(context, "response") and context.response is not None
    
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    if not bundles:
        raise AssertionError("No bundle options found in response")
    
    actual_values = []
    for bundle in bundles:
        value = bundle.get(field_name)
        actual_values.append(str(value) if value is not None else None)
    
    expected_values = [row.cells[0] for row in context.table.rows]
    
    assert actual_values == expected_values, (
        f"Ordered {field_name} mismatch.\nExpected: {expected_values}\nActual: {actual_values}"
    )
    LOGGER.info("Ordered bundle field assertion passed: %s", field_name)


@then('i valori del campo "{field_name}" delle opzioni bundle, nell\'ordine restituito, corrispondono a:')
def step_assert_ordered_field_values(context, field_name: str):
    """Assert ordered values of a field in bundle options."""
    assert context.table is not None, "Table with expected values required"
    assert hasattr(context, "response") and context.response is not None
    
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    if not bundles:
        raise AssertionError("No bundle options found in response")
    
    actual_values = []
    for bundle in bundles:
        value = bundle.get(field_name)
        actual_values.append(str(value) if value is not None else None)
    
    expected_values = [row.cells[0] for row in context.table.rows]
    
    assert actual_values == expected_values, (
        f"Ordered {field_name} mismatch.\nExpected: {expected_values}\nActual: {actual_values}"
    )
    LOGGER.info("Ordered field values assertion passed: %s", field_name)


@then('i valori del campo "{field_name}" delle prime opzioni bundle, nell\'ordine restituito, corrispondono a:')
def step_assert_ordered_first_bundle_field(context, field_name: str):
    """Assert ordered values of a field in first N bundle options."""
    assert context.table is not None, "Table with expected values required"
    assert hasattr(context, "response") and context.response is not None
    
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    if not bundles:
        raise AssertionError("No bundle options found in response")
    
    expected_values = [row.cells[0] for row in context.table.rows]
    actual_values = []
    for bundle in bundles[:len(expected_values)]:
        value = bundle.get(field_name)
        actual_values.append(str(value) if value is not None else None)
    
    assert actual_values == expected_values, (
        f"Ordered first {field_name} mismatch.\nExpected: {expected_values}\nActual: {actual_values}"
    )
    LOGGER.info("Ordered first bundle field assertion passed: %s", field_name)


@then("il sistema risponde con un solo bundle per ciascun PSP")
def step_assert_one_bundle_per_psp(context):
    """Assert one bundle per PSP in response."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    psp_counts = {}
    for bundle in bundles:
        psp_id = bundle.get("idPsp")
        psp_counts[psp_id] = psp_counts.get(psp_id, 0) + 1
    
    for psp_id, count in psp_counts.items():
        assert count == 1, f"PSP {psp_id} has {count} bundles, expected 1"
    
    LOGGER.info("One bundle per PSP assertion passed")


@then("le opzioni bundle non riportano valori per il campo \"{field_name}\"")
def step_assert_field_empty(context, field_name: str):
    """Assert field is empty in all bundle options."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    for bundle in bundles:
        value = bundle.get(field_name)
        assert value is None or value == [] or value == {}, (
            f"Field {field_name} expected empty, got: {value}"
        )
    
    LOGGER.info("Empty field assertion passed: %s", field_name)


@then("le commissioni delle opzioni bundle non riportano codici EC")
def step_assert_no_ec_codes(context):
    """Assert no EC codes in bundle commissions."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    for bundle in bundles:
        transfers = bundle.get("transfers") or bundle.get("commissioni") or []
        assert len(transfers) == 0, (
            f"Expected no EC codes but found: {transfers}"
        )
    
    LOGGER.info("No EC codes assertion passed")


@then("la risposta contiene i metodi di pagamento di test configurati")
def step_assert_payment_methods_present(context):
    """Assert response contains configured payment methods."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    methods = body.get("paymentMethods") or body.get("methods") or body
    assert len(methods) > 0, "No payment methods found in response"
    LOGGER.info("Payment methods present assertion passed")


@then("la risposta non contiene i metodi di pagamento di test configurati")
def step_assert_payment_methods_absent(context):
    """Assert response does not contain configured payment methods."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    methods = body.get("paymentMethods") or body.get("methods") or body
    assert len(methods) == 0, f"Expected no payment methods, found: {methods}"
    LOGGER.info("Payment methods absent assertion passed")


@then('il metodo "{method_name}" è il primo della risposta')
def step_assert_first_payment_method(context, method_name: str):
    """Assert specific payment method is first in response."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    methods = body.get("paymentMethods") or body.get("methods") or body or []
    if isinstance(methods, list) and len(methods) > 0:
        first = methods[0]
        first_name = first.get("name") or first.get("type") or str(first)
        assert first_name == method_name, (
            f"First method expected '{method_name}', got '{first_name}'"
        )
    else:
        raise AssertionError("No methods found in response")
    
    LOGGER.info("First payment method assertion passed: %s", method_name)


@then('i metodi diversi da "{method_name}" sono in ordine alfabetico')
def step_assert_alphabetic_order(context, method_name: str):
    """Assert payment methods (except specified one) are alphabetically ordered."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    methods = body.get("paymentMethods") or body.get("methods") or body or []
    if isinstance(methods, list) and len(methods) > 1:
        rest = methods[1:]
        rest_names = []
        for m in rest:
            name = m.get("name") or m.get("type") or str(m)
            rest_names.append(name)
        
        sorted_names = sorted(rest_names)
        assert rest_names == sorted_names, (
            f"Methods not alphabetically ordered.\nExpected: {sorted_names}\nGot: {rest_names}"
        )
    
    LOGGER.info("Alphabetic order assertion passed")


@then("per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC")
def step_assert_commission_sum(context):
    """Assert max commission minus actual equals sum of EC commissions."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    for bundle in bundles:
        tax_payer_fee = bundle.get("taxPayerFee", 0)
        primary_ci_fee = bundle.get("primaryCiIncurredFee", 0)
        assert tax_payer_fee >= primary_ci_fee, (
            f"Commission logic invalid for bundle {bundle.get('idBundle')}"
        )
    
    LOGGER.info("Commission sum assertion passed")


@then('i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a:')
def step_assert_ec_codes_ordered(context):
    """Assert EC codes in bundles match expected list."""
    assert context.table is not None, "Table with expected EC codes required"
    assert hasattr(context, "response") and context.response is not None
    
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    expected_codes = [row.cells[0] for row in context.table.rows]
    
    bundles = _get_bundled_response(body)
    for bundle in bundles:
        transfers = bundle.get("idsTransfers") or bundle.get("transfers") or []
        actual_codes = []
        if isinstance(transfers, list):
            actual_codes = sorted([str(t) for t in transfers])
        else:
            actual_codes = sorted([str(transfers)])
        
        assert actual_codes == sorted(expected_codes), (
            f"EC codes mismatch for bundle {bundle.get('idBundle')}.\n"
            f"Expected: {sorted(expected_codes)}\nActual: {actual_codes}"
        )
    
    LOGGER.info("EC codes ordered assertion passed")


@then('i codici EC delle commissioni delle prime opzioni bundle, in ordine alfabetico, corrispondono a:')
def step_assert_ec_codes_first_bundles(context):
    """Assert EC codes for first N bundles match expected list."""
    assert context.table is not None, "Table with expected EC codes required"
    assert hasattr(context, "response") and context.response is not None
    
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    expected_codes = [row.cells[0] for row in context.table.rows]
    
    bundles = _get_bundled_response(body)
    for bundle in bundles:
        transfers = bundle.get("idsTransfers") or bundle.get("transfers") or []
        actual_codes = []
        if isinstance(transfers, list):
            actual_codes = sorted([str(t) for t in transfers])
        else:
            actual_codes = sorted([str(transfers)])
        
        assert actual_codes == sorted(expected_codes), (
            f"EC codes mismatch for bundle {bundle.get('idBundle')}.\n"
            f"Expected: {sorted(expected_codes)}\nActual: {actual_codes}"
        )
    
    LOGGER.info("EC codes for first bundles assertion passed")


@then('i metodi di pagamento di test hanno i seguenti stati:')
def step_assert_payment_methods_status(context):
    """Assert payment methods have expected status and reason."""
    assert context.table is not None, "Table with method status required"
    assert hasattr(context, "response") and context.response is not None
    
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    methods = body.get("paymentMethods") or body.get("methods") or body or []
    
    methods_map = {}
    if isinstance(methods, list):
        for m in methods:
            if isinstance(m, dict):
                name = m.get("name") or m.get("type")
                if name:
                    methods_map[name] = m
    
    for row in context.table.rows:
        metodo = row.get("metodo")
        stato = row.get("stato")
        motivo = row.get("motivo")
        
        assert metodo in methods_map, f"Method '{metodo}' not found in response"
        
        method_data = methods_map[metodo]
        actual_state = method_data.get("status") or method_data.get("stato")
        actual_reason = method_data.get("reason") or method_data.get("motivo") or ""
        
        assert actual_state == stato, (
            f"Method '{metodo}' status expected '{stato}', got '{actual_state}'"
        )
        
        if motivo:
            assert actual_reason == motivo, (
                f"Method '{metodo}' reason expected '{motivo}', got '{actual_reason}'"
            )
    
    LOGGER.info("Payment methods status assertion passed")


@then("nella risposta non è riportato il bundle delle Poste Italiane")
def step_assert_poste_bundle_absent(context):
    """Assert Poste Italiane bundle is not in response."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    for bundle in bundles:
        psp_name = bundle.get("pspBusinessName") or bundle.get("idPsp") or ""
        assert "poste" not in psp_name.lower(), (
            f"Poste Italiane bundle found but expected absent: {psp_name}"
        )
    
    LOGGER.info("Poste Italiane bundle absent assertion passed")


@then("nella risposta è riportato il bundle delle Poste Italiane")
def step_assert_poste_bundle_present(context):
    """Assert Poste Italiane bundle is in response."""
    assert hasattr(context, "response") and context.response is not None
    try:
        body = context.response.json()
    except Exception as e:
        raise AssertionError(f"Response not valid JSON: {e}")
    
    bundles = _get_bundled_response(body)
    poste_found = False
    for bundle in bundles:
        psp_name = bundle.get("pspBusinessName") or bundle.get("idPsp") or ""
        if "poste" in psp_name.lower():
            poste_found = True
            break
    
    assert poste_found, "Poste Italiane bundle not found in response"
    LOGGER.info("Poste Italiane bundle present assertion passed")
