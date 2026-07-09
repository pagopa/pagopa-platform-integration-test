def delete_payments(context):
    delete_payments_url = f"{context.config.fdr_base_url}/psps/{context.pspId}/fdrs/{context.fdr}/payments/del"
    request_body = f"""
    {
      "indexList":{context.fdr.payments_to_delete}
    }
    """
    context.fdr.response = context.fdr.rest_client.post(delete_payments_url, json_body = request_body)
    context.fdr.http_status_code = context.fdr.delete_payments_response.status_code
