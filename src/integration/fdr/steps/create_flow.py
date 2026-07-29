from behave import given, when, then
from src.integration.fdr import common
from src.integration.fdr import psp

@given(u'i sistemi sono operativi')
def check_health(context):
    common.check_health(context)

@given(u'un nuovo id flusso di rendicontazione pari a "{fdr_id}"')
def get_fdr_id(context, fdr_id):
    context.fdr_id = fdr_id

@given(u'il PSP "{psp_id}" non è in stato "{psp_status}"')
def check_psp_disabled(context, psp_id, psp_status):
    psp.get_psp_info(context, psp_id)
    assert context.get_psp_response.status_code == 200, f"Failed to retrieve PSP info for pspId {psp_id}. Status code: {context.get_psp_response.status_code}, Response: {context.get_psp_response.text}"   
    assert context.get_psp_response.json().get("status") != psp_status, f"Expected PSP with pspId {psp_id} to not be in status {psp_status}, but it is. Response: {context.get_psp_response.text}"

@given(u'il PSP "{psp_name}" con pspId "{psp_id}" non è censito a sistema')
def check_psp_not_registered(context, psp_name, psp_id):
    psp.get_psp_info(context, psp_id)
    assert context.get_psp_response.httpStatusCode == 404, f"Expected PSP with pspId {psp_id} to not be registered, but it is. Status code: {context.get_psp_response.httpStatusCode}, Response: {context.get_psp_response.text}"

@given(u'il PSP "{psp_name}" con pspId "{psp_id}" correttamente censito a sistema')
def check_psp_registered(context, psp_name, psp_id):
    psp.get_psp_info(context, psp_id)
    assert context.get_psp_response.httpStatusCode == 200, f"Expected PSP with pspId {psp_id} to be registered, but it is not. Status code: {context.get_psp_response.httpStatusCode}, Response: {context.get_psp_response.text}"


@when(u'il PSP invia una richiesta di creazione flusso tramite l\'api "Create a new flow structure"')
def create_fdr(context):
    fdr_create_flow_endpoint = f"{context.secrets.fdr_base_url}/psps/{context.psp_id}/fdrs/{context.fdr_id}"
    fdr_create_request_payload = common.build_create_fdr_request_payload(context)
    context.response = context.fdr.rest.client.post(fdr_create_flow_endpoint, json=fdr_create_request_payload)

@then(u'il sistema risponde con il codice di stato HTTP "{http_status_code:d}"')
def check_response_status(context, http_status_code):
    assert context.response.httpStatusCode == http_status_code, f"Expected HTTP status code {http_status_code}, but got {context.response.httpStatusCode}. Response: {context.response.text}"

@then(u'il nuovo flusso viene creato con id "{fdr_id}"')
def check_fdr_id(context, fdr_id):
    context.get_fdr_response = context.fdr.rest.client.get(f"/psps/{context.psp_id}/CREATED/fdrs/{fdr_id}/organizations/{context.receiver.organization_id}")
    assert context.get_fdr_response.json().get("fdrId") == fdr_id, f"Expected fdrId {fdr_id}, but got {context.get_fdr_response.json().get('fdrId')}. Response: {context.get_fdr_response.text}"

@then(u'il flusso è in stato "{fdr_status}"')
def check_fdr_status(context, fdr_status):
    assert context.get_fdr_response.json().get("fdrStatus") == fdr_status, f"Expected fdrStatus {fdr_status}, but got {context.get_fdr_response.json().get('fdrStatus')}. Response: {context.get_fdr_response.text}"

@then(u'il campo "revision" è pari a 1')
def check_revision(context):
    assert context.get_fdr_response.json().get("revision") == 1, f"Expected revision 1, but got {context.get_fdr_response.json().get('revision')}. Response: {context.get_fdr_response.text}"

@then(u'il campo "last_update_date" è aggiornato all\'ora corrente')
def check_last_update_date(context):
    assert context.get_fdr_response.json().get("lastUpdateDate") == context.request_date, f"Expected lastUpdateDate to match request_date, but got {context.get_fdr_response.json().get('lastUpdateDate')} and {context.request.json().get('creationDate')}. Response: {context.get_fdr_response.text}"

@then(u'il campo "creation_date" è aggiornato all\'ora corrente')
def check_creation_date(context):
    assert context.get_fdr_response.json().get("creationDate") == context.request_date, f"Expected creationDate to match request_date, but got {context.get_fdr_response.json().get('creationDate')} and {context.request.json().get('lastUpdateDate')}. Response: {context.get_fdr_response.text}"

@then(u'il flusso di rendicontazione non viene creato a sistema')
def check_fdr_not_created(context):
    fdr_response = context.fdr.rest.client.get(f"/psps/{context.create_fdr.sender.psp_id}/created/fdrs/{context.fdr_id}/organizations/{context.receiver.organization_id}")
    assert fdr_response.status_code == 404, f"Expected HTTP status code 404 for non-existing FDR, but got {fdr_response.status_code}. Response: {fdr_response.text}"

@given(u'che il flusso di rendicontazione "{fdr_id}" esiste già in stato "{fdr_status}"')
def check_fdr_exists(context, fdr_id, fdr_status):
    context.get_fdr_response = context.fdr.rest.client.get(f"/psps/{context.create_fdr.sender.psp_id}/{fdr_status}/fdrs/{fdr_id}/organizations/{context.receiver.organization_id}")
    assert context.get_fdr_response.status_code == 200, f"Expected HTTP status code 200 for existing FDR, but got {context.get_fdr_response.status_code}. Response: {context.get_fdr_response.text}"
    assert context.get_fdr_response.json().get("fdrStatus") == fdr_status, f"Expected existing FDR status {fdr_status}, but got {context.get_fdr_response.json().get('fdrStatus')}. Response: {context.get_fdr_response.text}"
    

@then(u'il campo "revision" è incrementato di 1 rispetto alla revisione esistente')
def check_revision_incremented(context):
    assert context.get_fdr_response.json().get("revision") == context.get_fdr_response.json().get("revision") + 1, f"Expected revision to be incremented by 1, but got {context.response.json().get('revision')} and {context.get_fdr_response.json().get('revision')}. Response: {context.response.text}"


@then(u'il flusso di rendicontazione esistente non viene modificato a sistema')
def check_fdr_not_modified(context):
    fdr_response = context.fdr.rest.client.get(f"/psps/{context.create_fdr.sender.psp_id}/{context.get_fdr_response.json().get('fdrStatus')}/fdrs/{context.get_fdr_response.json().get('fdrId')}/organizations/{context.receiver.organization_id}")
    assert fdr_response.json().get("fdrStatus") == context.get_fdr_response.json().get("fdrStatus"), f"Expected existing FDR status to remain unchanged, but got {fdr_response.json().get('fdrStatus')} and {context.get_fdr_response.json().get('fdrStatus')}. Response: {fdr_response.text}"
    assert fdr_response.json().get("revision") == context.get_fdr_response.json().get("revision"), f"Expected existing FDR revision to remain unchanged, but got {fdr_response.json().get('revision')} and {context.get_fdr_response.json().get('revision')}. Response: {fdr_response.text}"
    assert fdr_response.json().get("lastUpdateDate") == context.get_fdr_response.json().get("lastUpdateDate"), f"Expected existing FDR lastUpdateDate to remain unchanged, but got {fdr_response.json().get('lastUpdateDate')} and {context.get_fdr_response.json().get('lastUpdateDate')}. Response: {fdr_response.text}"
    assert fdr_response.json().get("creationDate") == context.get_fdr_response.json().get("creationDate"), f"Expected existing FDR creationDate to remain unchanged, but got {fdr_response.json().get('creationDate')} and {context.get_fdr_response.json().get('creationDate')}. Response: {fdr_response.text}"


@then(u'il blob object corrispondente viene salvato correttamente a sistema')
def check_blob_saved(context):
    blob_name = "%s_%s_%s.json.zip" % (
        context.fdr_response.json().get("sender").get("pspid"),
        context.fdr_response.json().get("revision"),
        context.fdr_response.json().get("fdr")
    )

    blob = context.blob.service_client.find_blob(context.config.blob.container_name, blob_name)
    assert blob is not None, "Expected blob object to be saved in the system, but it was not found."
