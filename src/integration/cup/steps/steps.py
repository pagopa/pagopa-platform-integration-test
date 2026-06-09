from behave import given, when, then, use_step_matcher

use_step_matcher("re")


@given(r"Il PSP ha ricevuto dalla Corporate un file di input valido che include i dati mandatori\s*")
def step_psp_riceve_input_valido_mandatorio(context):
    pass


@given(r"Il file di input contiene una sola chiave di identificazione Ente\s*")
def step_file_contiene_una_sola_chiave_ente(context):
    pass


@given(
    r"Il PSP ha ricevuto dalla Corporate un file di input non valido, contenente più parametri identificativi"
    r" \((?P<organizationFiscalCode>[^,]*), (?P<istatCode>[^,]*), (?P<catastalCode>[^)]*)\)"
)
def step_psp_riceve_input_multi_parametri(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@given(
    r"Il PSP ha ricevuto dalla Corporate un file di input non valido, contenente uno dei parametri identificativi"
    r" \((?P<organizationFiscalCode>[^,]*), (?P<istatCode>[^,]*), (?P<catastalCode>[^)]*)\)"
    r" che non rispetta il formato sintattico previsto"
)
def step_psp_riceve_input_parametro_formato_sintattico_errato(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@given(
    r"Il PSP ha ricevuto dalla Corporate un file di input non valido, in cui sono assenti uno o più campi mandatori"
    r" \((?P<debtorFiscalCode>[^,]*), (?P<debtorFullName>[^,]*), (?P<amount>[^)]*)\)"
)
def step_psp_riceve_input_campi_obbligatori_mancanti(context, debtorFiscalCode, debtorFullName, amount):
    pass


@given(
    r"Il PSP ha ricevuto dalla Corporate un file di input non valido, in cui uno dei campi mandatori"
    r" \((?P<amount>[^,]*), (?P<debtorFiscalCode>[^)]*)\) è valorizzato con un formato errato"
)
def step_psp_riceve_input_formato_campo_errato(context, amount, debtorFiscalCode):
    pass


@given(
    r"Il PSP ha ricevuto dalla Corporate un file di input valido, contenente uno dei parametri identificativi"
    r" \((?P<organizationFiscalCode>[^,]*), (?P<istatCode>[^,]*), (?P<catastalCode>[^)]*)\)"
    r" non presente nella cache multi-livello"
)
def step_psp_riceve_input_parametro_non_in_cache(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@when(
    r"Il PSP Invia la primitiva demandPaymentNotice includendo i dati mandatori"
    r" e valorizzando un parametro identificativo"
)
def step_psp_invia_demand_payment_notice_happy_path(context):
    pass


@when(
    r"Il PSP Invia la primitiva demandPaymentNotice valorizzando più di un parametro identificativo"
    r" \((?P<organizationFiscalCode>[^,]*), (?P<istatCode>[^,]*), (?P<catastalCode>[^)]*)\)"
)
def step_psp_invia_demand_payment_notice_multi_identificativo(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@when(
    r"Il PSP Invia la primitiva demandPaymentNotice valorizzando uno dei parametri identificativi"
    r" \((?P<organizationFiscalCode>[^,]*), (?P<istatCode>[^,]*), (?P<catastalCode>[^)]*)\)"
    r" non rispettando il formato sintattico previsto"
)
def step_psp_invia_demand_payment_notice_formato_sintattico_errato(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@when(
    r"Il PSP Invia la primitiva demandPaymentNotice priva di uno dei campi mandatori"
    r" \((?P<debtorFiscalCode>[^,]*), (?P<debtorFullName>[^,]*), (?P<amount>[^)]*)\)"
)
def step_psp_invia_demand_payment_notice_senza_campo_obbligatorio(context, debtorFiscalCode, debtorFullName, amount):
    pass


@when(
    r"Il PSP Invia una richiesta con il formato errato di uno dei campi"
    r" \((?P<amount>[^,]*), (?P<debtorFiscalCode>[^)]*)\)"
)
def step_psp_invia_richiesta_formato_campo_errato(context, amount, debtorFiscalCode):
    pass


@when(
    r"Il PSP Invia la primitiva demandPaymentNotice valorizzando uno dei parametri identificativi"
    r" \((?P<organizationFiscalCode>[^,]*), (?P<istatCode>[^,]*), (?P<catastalCode>[^)]*)\)"
    r" con un valore non presente nella cache multi-livello"
)
def step_psp_invia_demand_payment_notice_non_in_cache(context, organizationFiscalCode, istatCode, catastalCode):
    pass


@then(r"Viene creata correttamente la posizione debitoria")
def step_viene_creata_posizione_debitoria(context):
    pass


@then(
    r"La posizione debitoria contiene il campo remittanceInformation:"
    r" /RFB/(?P<IUV>[^/]+)/CNR/(?P<CF_Debitore>[^/]+)/TXT/Canone Unico Patrimoniale Saldo (?P<anno>.+)"
)
def step_posizione_debitoria_contiene_remittance_information(context, IUV, CF_Debitore, anno):
    pass


@then(
    r"La posizione debitoria contiene il campo payment\.option\.description"
    r" : Canone Unico Patrimoniale (?P<anno>.+)"
)
def step_posizione_debitoria_contiene_payment_option_description(context, anno):
    pass


@then(r"Il PSP Riceve la risposta demandPaymentNotice res con l'esito della creazione nel formato previsto per l'output")
def step_psp_riceve_risposta_demand_payment_notice_res(context):
    pass


@then(r"Il PSP riceve un 200 OK che all'interno riporta il fault code (?P<risposta>\S+)")
def step_psp_riceve_200_con_fault_code(context, risposta):
    pass
