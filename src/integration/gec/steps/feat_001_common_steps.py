"""Common Behave steps for GEC integration tests."""

import json
import logging

from behave import given, then, when

from src.integration.gec.helper import (
    _config_value,
    _ensure_scenario_data_loaded,
    _ensure_vars_container,
    _get_bundled_response,
    _get_request_payload,
    _load_config_file,
    _normalize_boolean_cell,
    _send_request,
    _setup_poste_bundles,
    _sort_bundles_v1_onUs_first,
    _upload_payment_methods,
)


LOGGER = logging.getLogger("gec")


def _response_json(context) -> dict:
    """Return response JSON or fail with explicit assertion."""
    if not hasattr(context, "response") or context.response is None:
        raise AssertionError("Missing HTTP response in context")
    try:
        return context.response.json()
    except Exception as error:
        raise AssertionError(f"Response is not valid JSON: {error}") from error


def _bundle_rows(context) -> list:
    """Return bundleOptions list from current response."""
    return _get_bundled_response(_response_json(context))


def _clean_cell(value: str) -> str:
    """Normalize expected table cell without altering lexical content."""
    cell = (value or "").strip()
    if len(cell) >= 2 and cell[0] == '"' and cell[-1] == '"':
        return cell[1:-1]
    return cell


def _string_values(value) -> list:
    """Convert response scalar/list into comparable strings, rendering booleans as JSON-style lowercase."""
    if value is None:
        return []
    items = value if isinstance(value, list) else [value]
    return [("true" if item else "false") if isinstance(item, bool) else str(item) for item in items]


def _payment_method_name(method: dict) -> str:
    """Return method.name with JavaScript String(...) parity used by AFM order assertion."""
    name = method.get("name")
    if name is None:
        return ""
    if isinstance(name, dict):
        return "[object Object]"
    if isinstance(name, bool):
        return "true" if name else "false"
    return str(name)


def _poste_rule(context):
    """Return Poste matching rule derived from runtime configuration."""
    global_conf = getattr(context.config, "global_configuration", {})
    enabled_raw = _config_value(global_conf, "all_ccp_new_filter_enabled")
    is_enabled = enabled_raw is True or str(enabled_raw).lower() == "true"
    id_psp_poste = str(_config_value(global_conf, "id_psp_poste") or "BPPIITRRZZZ")
    poste_channel_ids = _config_value(global_conf, "poste_channel_ids") or []
    if isinstance(poste_channel_ids, str):
        poste_channel_ids = [item.strip() for item in poste_channel_ids.split(",") if item.strip()]
    return is_enabled, id_psp_poste, poste_channel_ids


def _payload_name_for_operation(context, operation: str) -> str:
    """Resolve payload name using operation-specific precedence."""
    operation_lower = operation.lower()
    vars_dict = getattr(context, "vars", {})
    if "ricerca metodi di pagamento" in operation_lower:
        return vars_dict.get("payment_methods_request") or vars_dict.get("current_request_payload", "default_payload")
    return vars_dict.get("current_request_payload", "default_payload")


@given("che i sistemi sono operativi")
def step_systems_up(context):
    """Prepare scenario state and load AFM baseline data configuration once."""
    _ensure_vars_container(context)
    context.response = None
    _ensure_scenario_data_loaded(context)


@given("il bundle poste è configurato")
def step_bundle_poste_configured(context):
    """Upload Poste bundles with AFM parity rules."""
    _ensure_vars_container(context)
    _setup_poste_bundles(context)


@given("la configurazione dei dati di test è caricata")
def step_test_data_configured(context):
    """Ensure AFM-compatible data.json setup has been uploaded once per scenario."""
    _ensure_vars_container(context)
    _ensure_scenario_data_loaded(context)


@given('una richiesta di recupero commissioni "{payload_name}"')
def step_named_commission_request(context, payload_name: str):
    """Store payload name for subsequent commission request."""
    _ensure_vars_container(context)
    context.vars["current_request_payload"] = payload_name


@given('la configurazione dei metodi di pagamento "{config_name}"')
def step_payment_methods_configuration(context, config_name: str):
    """Upload payment methods config to marketplace endpoint."""
    _ensure_vars_container(context)
    config_data = _load_config_file(context, config_name, file_type="json")
    _upload_payment_methods(context, config_data)
    context.vars["payment_methods_config"] = config_name


@given('una richiesta di ricerca dei metodi di pagamento "{request_name}"')
def step_payment_methods_request(context, request_name: str):
    """Store payment-method search payload identifier."""
    _ensure_vars_container(context)
    context.vars["payment_methods_request"] = request_name


@given('il parametro di richiesta "{param_name}" è "{param_value}"')
def step_request_parameter(context, param_name: str, param_value: str):
    """Store request query parameters with boolean normalization where required."""
    _ensure_vars_container(context)
    params = context.vars.setdefault("request_params", {})
    if param_name in ("onUsFirst", "allCcp"):
        params[param_name] = _normalize_boolean_cell(param_value)
    else:
        params[param_name] = param_value


@given("l'impostazione allCcp è disabilitata")
def step_allccp_disabled(context):
    """Set allCcp=false for the next request."""
    _ensure_vars_container(context)
    context.vars["allCcp"] = False


@given("l'impostazione allCcp è abilitata")
def step_allccp_enabled(context):
    """Set allCcp=true for the next request."""
    _ensure_vars_container(context)
    context.vars["allCcp"] = True


@when('il client invia la richiesta di "{operation}" per il PSP "{psp_id}" con il payload "{payload_name}"')
def step_send_request_with_psp_payload(context, operation: str, psp_id: str, payload_name: str):
    """Send a request specifying both PSP and payload name."""
    _ensure_vars_container(context)
    context.vars["psp_id"] = psp_id
    _send_request(context, operation, payload_name)


@when('il client invia la richiesta di "{operation}" con il payload "{payload_name}"')
def step_send_request_with_payload(context, operation: str, payload_name: str):
    """Send a request with explicit payload name."""
    _send_request(context, operation, payload_name)


@when('il client invia la richiesta di "{operation}" per il PSP "{psp_id}"')
def step_send_request_with_psp(context, operation: str, psp_id: str):
    """Send a request with PSP and previously selected payload."""
    _ensure_vars_container(context)
    context.vars["psp_id"] = psp_id
    payload_name = _payload_name_for_operation(context, operation)
    _send_request(context, operation, payload_name)


@when('il client invia la richiesta di "{operation}"')
def step_send_request_basic(context, operation: str):
    """Send a request using current scenario payload selection."""
    payload_name = _payload_name_for_operation(context, operation)
    _send_request(context, operation, payload_name)


@then("il sistema risponde con codice di stato {status_code:d}")
def step_assert_status_code(context, status_code: int):
    """Assert response status code."""
    if not hasattr(context, "response") or context.response is None:
        raise AssertionError("Missing HTTP response in context")
    actual = context.response.status_code
    assert actual == status_code, f"Expected status {status_code}, got {actual}"


@then('il corpo della risposta corrisponde al payload "{payload_name}"')
def step_assert_response_matches_payload(context, payload_name: str):
    """Assert response body equals expected payload template."""
    expected_payload = _get_request_payload(context, f"{payload_name}_response", payload_name)
    actual_body = _response_json(context)
    assert json.dumps(actual_body, sort_keys=True) == json.dumps(expected_payload, sort_keys=True), (
        f"Response body mismatch for payload '{payload_name}'"
    )


@then('i valori del campo `{field_name}` delle opzioni bundle, dopo l\'ordinamento previsto per l\'API "{api_version}", corrispondono ai seguenti')
def step_assert_ordered_bundle_field_backtick(context, field_name: str, api_version: str):
    """Assert ordered bundle field values with V1 onUs sorting parity."""
    if context.table is None:
        raise AssertionError("Expected values table is required")
    bundles = _bundle_rows(context)
    expected_rows = context.table.rows
    ordered_bundles = bundles
    if api_version.upper() == "V1" and field_name.lower() == "onus":
        ordered_bundles = _sort_bundles_v1_onUs_first(bundles)
    assert len(ordered_bundles) == len(expected_rows), (
        f"Expected {len(expected_rows)} bundle options, got {len(ordered_bundles)}"
    )

    actual_values = []
    for bundle in ordered_bundles:
        value = bundle.get(field_name)
        if isinstance(value, bool):
            actual_values.append(_normalize_boolean_cell(str(value)))
        else:
            actual_values.append(str(value))

    expected_values = [_normalize_boolean_cell(_clean_cell(row.cells[0])) for row in expected_rows]
    assert actual_values == expected_values, f"Expected {expected_values}, got {actual_values}"


@then('i valori del campo "{field_name}" delle opzioni bundle, nell\'ordine restituito, corrispondono a')
def step_assert_ordered_field_values(context, field_name: str):
    """Assert row-wise mapping for bundle field values supporting multi-column tables."""
    if context.table is None:
        raise AssertionError("Expected values table is required")
    bundles = _bundle_rows(context)
    expected_rows = context.table.rows
    if len(bundles) < len(expected_rows):
        raise AssertionError(f"Expected at least {len(expected_rows)} bundle rows, got {len(bundles)}")
    for index, row in enumerate(expected_rows):
        expected_values = [_clean_cell(cell) for cell in row.cells]
        actual_values = _string_values(bundles[index].get(field_name))
        assert actual_values == expected_values, (
            f"Mismatch for field '{field_name}' at row {index + 1}: expected {expected_values}, got {actual_values}"
        )


@then('i valori del campo "{field_name}" delle prime opzioni bundle, nell\'ordine restituito, corrispondono a')
def step_assert_ordered_first_bundle_field(context, field_name: str):
    """Assert first-N bundle field values and store N for follow-up validations."""
    if context.table is None:
        raise AssertionError("Expected values table is required")
    bundles = _bundle_rows(context)
    expected_rows = context.table.rows
    if len(bundles) < len(expected_rows):
        raise AssertionError(f"Expected at least {len(expected_rows)} bundle rows, got {len(bundles)}")
    _ensure_vars_container(context)
    context.vars["num_first_options"] = len(expected_rows)
    for index, row in enumerate(expected_rows):
        expected_values = [_clean_cell(cell) for cell in row.cells]
        actual_values = _string_values(bundles[index].get(field_name))
        assert actual_values == expected_values, (
            f"Mismatch for field '{field_name}' at row {index + 1}: expected {expected_values}, got {actual_values}"
        )


@then("il sistema risponde con un solo bundle per ciascun PSP")
def step_assert_one_bundle_per_psp(context):
    """Assert each PSP appears at most once in bundle options."""
    psp_seen = set()
    for bundle in _bundle_rows(context):
        psp_id = bundle.get("idPsp")
        if psp_id in psp_seen:
            raise AssertionError(f"Duplicate bundle detected for PSP '{psp_id}'")
        psp_seen.add(psp_id)


@then("le opzioni bundle non riportano valori per il campo \"{field_name}\"")
def step_assert_field_empty(context, field_name: str):
    """Assert a bundle field is absent or empty for every option."""
    for bundle in _bundle_rows(context):
        value = bundle.get(field_name)
        if value not in (None, [], {}):
            raise AssertionError(f"Field '{field_name}' expected empty, got {value}")


@then("le commissioni delle opzioni bundle non riportano codici EC")
def step_assert_no_ec_codes(context):
    """Assert all bundle fees collections are absent/empty."""
    for bundle in _bundle_rows(context):
        fees = bundle.get("fees", [])
        if fees not in (None, []):
            raise AssertionError(f"Expected empty fees, got {fees}")


@then("la risposta non contiene opzioni bundle")
def step_assert_no_bundle_options(context):
    """Assert response contains an empty bundleOptions list."""
    response = _response_json(context)
    assert "bundleOptions" in response, "Missing 'bundleOptions' key in response"
    bundle_options = response["bundleOptions"]
    assert isinstance(bundle_options, list), (
        f"Expected 'bundleOptions' to be a list, got {type(bundle_options).__name__}"
    )
    assert len(bundle_options) == 0, f"Expected empty bundleOptions, got {len(bundle_options)} items"


@then("la risposta contiene i metodi di pagamento di test configurati")
def step_assert_payment_methods_present(context):
    """Assert both configured test payment methods are present."""
    methods = _response_json(context).get("paymentMethods", [])
    ids = {str(method.get("paymentMethodId") or "") for method in methods}
    global_conf = getattr(context.config, "global_configuration", {})
    expected = {
        _config_value(global_conf, "payment_method_paypal") or "PAYPAL-test",
        _config_value(global_conf, "payment_method_cards") or "CARDS-test",
    }
    if not expected.issubset(ids):
        raise AssertionError(f"Missing expected payment methods: {sorted(expected - ids)}")


@then("la risposta non contiene i metodi di pagamento di test configurati")
def step_assert_payment_methods_absent(context):
    """Assert configured test payment methods are not present."""
    methods = _response_json(context).get("paymentMethods", [])
    ids = {str(method.get("paymentMethodId") or "") for method in methods}
    global_conf = getattr(context.config, "global_configuration", {})
    forbidden = {
        _config_value(global_conf, "payment_method_paypal") or "PAYPAL-test",
        _config_value(global_conf, "payment_method_cards") or "CARDS-test",
    }
    if ids.intersection(forbidden):
        raise AssertionError(f"Forbidden payment methods found: {sorted(ids.intersection(forbidden))}")


@then('il metodo "{method_name}" è il primo della risposta')
def step_assert_first_payment_method(context, method_name: str):
    """Assert first payment method group is CP as in AFM oracle."""
    methods = _response_json(context).get("paymentMethods", [])
    if not methods:
        raise AssertionError("No payment methods found in response")
    first_group = methods[0].get("group")
    assert first_group == "CP", f"Expected first payment method group 'CP', got '{first_group}'"
    LOGGER.debug("Expected first method label placeholder: %s", method_name)


@then('i metodi diversi da "{method_name}" sono in ordine alfabetico')
def step_assert_alphabetic_order(context, method_name: str):
    """Assert payment methods after the first follow AFM JS localeCompare ordering semantics."""
    methods = _response_json(context).get("paymentMethods", [])
    if len(methods) <= 1:
        return
    names = [_payment_method_name(item) for item in methods[1:]]
    expected_order = sorted(names)
    assert names == expected_order, f"Expected {expected_order}, got {names}"
    LOGGER.debug("Reference first method placeholder: %s", method_name)


@then("per ogni opzione la commissione massima meno quella effettiva del cittadino è la somma di quelle effettive degli EC")
def step_assert_commission_sum(context):
    """Assert taxPayerFee - actualPayerFee equals sum(actualCiIncurredFee) for selected options."""
    bundles = _bundle_rows(context)
    _ensure_vars_container(context)
    limit = context.vars.get("num_first_options")
    max_rows = int(limit) if limit is not None else len(bundles)
    for index, bundle in enumerate(bundles[:max_rows]):
        fees = sorted(bundle.get("fees", []), key=lambda fee: fee.get("creditorInstitution", ""))
        fee_sum = sum(float(fee.get("actualCiIncurredFee", 0)) for fee in fees)
        tax_payer_fee = float(bundle.get("taxPayerFee", 0))
        actual_payer_fee = float(bundle.get("actualPayerFee", 0))
        left = tax_payer_fee - actual_payer_fee
        if abs(left - fee_sum) > 0.000001:
            raise AssertionError(
                f"Bundle row {index + 1}: expected {left} == {fee_sum} "
                "(taxPayerFee - actualPayerFee == sum(actualCiIncurredFee))"
            )


@then('i codici EC delle commissioni di ciascuna opzione bundle, in ordine alfabetico, corrispondono a')
def step_assert_ec_codes_ordered(context):
    """Assert EC codes by row/column from full bundle set."""
    if context.table is None:
        raise AssertionError("Expected EC codes table is required")
    bundles = _bundle_rows(context)
    expected_rows = context.table.rows
    if len(bundles) < len(expected_rows):
        raise AssertionError(f"Expected at least {len(expected_rows)} bundle rows, got {len(bundles)}")
    for index, row in enumerate(expected_rows):
        fees = sorted(bundles[index].get("fees", []), key=lambda fee: fee.get("creditorInstitution", ""))
        actual_codes = [str(fee.get("creditorInstitution", "")) for fee in fees]
        expected_codes = [_clean_cell(cell) for cell in row.cells]
        assert actual_codes == expected_codes, f"Row {index + 1}: expected {expected_codes}, got {actual_codes}"


@then('i codici EC delle commissioni delle prime opzioni bundle, in ordine alfabetico, corrispondono a')
def step_assert_ec_codes_first_bundles(context):
    """Assert EC codes by row/column for first-N bundle set and store N for sum step."""
    if context.table is None:
        raise AssertionError("Expected EC codes table is required")
    bundles = _bundle_rows(context)
    expected_rows = context.table.rows
    if len(bundles) < len(expected_rows):
        raise AssertionError(f"Expected at least {len(expected_rows)} bundle rows, got {len(bundles)}")
    _ensure_vars_container(context)
    context.vars["num_first_options"] = len(expected_rows)
    for index, row in enumerate(expected_rows):
        fees = sorted(bundles[index].get("fees", []), key=lambda fee: fee.get("creditorInstitution", ""))
        actual_codes = [str(fee.get("creditorInstitution", "")) for fee in fees]
        expected_codes = [_clean_cell(cell) for cell in row.cells]
        assert actual_codes == expected_codes, f"Row {index + 1}: expected {expected_codes}, got {actual_codes}"


@then('i metodi di pagamento di test hanno i seguenti stati')
def step_assert_payment_method_states(context):
    """Assert payment methods state table using columns metodo|stato|motivo."""
    if context.table is None:
        raise AssertionError("Expected payment method state table is required")
    methods = _response_json(context).get("paymentMethods", [])
    methods_by_id = {
        str(
            method.get("paymentMethodId")
            or method.get("payment_method_id")
            or method.get("id")
            or ""
        ): method
        for method in methods
    }
    headings = [heading.strip().lower() for heading in context.table.headings]
    try:
        metodo_index = headings.index("metodo")
        stato_index = headings.index("stato")
        motivo_index = headings.index("motivo")
    except ValueError as error:
        raise AssertionError("Expected table headings: metodo | stato | motivo") from error

    for row in context.table.rows:
        method_id = _clean_cell(row.cells[metodo_index])
        expected_status = _clean_cell(row.cells[stato_index])
        expected_reason = _clean_cell(row.cells[motivo_index])
        if method_id not in methods_by_id:
            raise AssertionError(f"Payment method '{method_id}' not found in response")
        method = methods_by_id[method_id]
        actual_status = str(method.get("status") or "")
        actual_reason = method.get("disabledReason")
        assert actual_status == expected_status, (
            f"Method '{method_id}': expected status '{expected_status}', got '{actual_status}'"
        )
        if expected_reason == "":
            if actual_reason not in (None, ""):
                raise AssertionError(
                    f"Method '{method_id}': expected disabledReason null/empty, got '{actual_reason}'"
                )
        elif str(actual_reason) != expected_reason:
            raise AssertionError(
                f"Method '{method_id}': expected disabledReason '{expected_reason}', got '{actual_reason}'"
            )


@then("nella risposta non è riportato il bundle delle Poste Italiane")
def step_assert_poste_bundle_absent(context):
    """Assert no bundle matches Poste rule for current allCcp mode."""
    bundles = _bundle_rows(context)
    is_enabled, id_psp_poste, poste_channel_ids = _poste_rule(context)
    for bundle in bundles:
        if is_enabled:
            if bundle.get("idChannel") in poste_channel_ids:
                raise AssertionError("Unexpected Poste bundle found in response")
        elif bundle.get("idPsp") == id_psp_poste:
            raise AssertionError("Unexpected Poste bundle found in response")


@then("nella risposta è riportato il bundle delle Poste Italiane")
def step_assert_poste_bundle_present(context):
    """Assert at least one bundle matches Poste rule for current allCcp mode."""
    bundles = _bundle_rows(context)
    is_enabled, id_psp_poste, poste_channel_ids = _poste_rule(context)
    if is_enabled:
        found = any(bundle.get("idChannel") in poste_channel_ids for bundle in bundles)
    else:
        found = any(bundle.get("idPsp") == id_psp_poste for bundle in bundles)
    assert found, "Expected Poste bundle not found in response"
