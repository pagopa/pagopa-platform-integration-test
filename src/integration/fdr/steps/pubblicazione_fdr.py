from behave import given, when, then

@given(u'il PSP vuole recuperare un FdR con identificativo diverso da "{fdr_id}"')
def step_impl(context, fdr_id):
    context.fdrId = fdr_id

@when(u'il PSP avvia una richiesta di pubblicazione flusso attraverso l\'API "Publish an existing flow in draft status"')
def publish_fdr_step(context):
    publish_url = f"{context.fdr_url}/psps/{context.pspId}/fdrs/{context.fdrId}/publish"
    context.response = context.rest.fdr_client.post(publish_url, context.headers)#controllare gli effettivi oggetti


@then(u'il parametro is_Latest viene settato a "TRUE"')
def check_is_latest_step(context):
    is_latest = context.response.json().get("is_Latest")
    if is_latest != "TRUE":
        raise AssertionError(f"Expected is_Latest to be 'TRUE', but got {is_latest}")