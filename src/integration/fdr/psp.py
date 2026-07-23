def get_psp_info(context, psp_id):
    """
    Recupera le informazioni del PSP dal sistema e le inserisce nel contesto.

    Args:
        context: Il contesto di Behave.
        psp_id: L'ID del PSP da recuperare.
    """
    psp_info_endpoint = f"{context.config.psp_base_url}/paymentserviceproviders/{psp_id}"
    context.get_psp_response = context.psp.rest.client.get(psp_info_endpoint)

# https://api.uat.platform.pagopa.it/apiconfig/auth/api/v1/paymentserviceproviders/WOLLNLB1