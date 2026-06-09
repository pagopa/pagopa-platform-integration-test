# language: it
@FEAT_001_CUP_Creazione_di_una_posizione_debitoria_per_CUP
Funzionalità: Creazione di una posizione debitoria per CUP

  # ===============================================================================================
  # Happy Path: flusso di creazione della posizione debitoria
  # ===============================================================================================

  @positivo @FEAT_001_CUP_scenario_01
  Scenario: Posizione debitoria per CUP creata correttamente
    Dato Il PSP ha ricevuto dalla Corporate un file di input valido che include i dati mandatori
    E Il file di input contiene una sola chiave di identificazione Ente
    Quando Il PSP Invia la primitiva demandPaymentNotice includendo i dati mandatori e valorizzando un parametro identificativo
    Allora Viene creata correttamente la posizione debitoria
    E La posizione debitoria contiene il campo remittanceInformation: /RFB/{IUV}/CNR/{CF_Debitore}/TXT/Canone Unico Patrimoniale Saldo {anno}
    E La posizione debitoria contiene il campo payment.option.description : Canone Unico Patrimoniale {anno}
    E Il PSP Riceve la risposta demandPaymentNotice res con l'esito della creazione nel formato previsto per l'output

  # ===============================================================================================
  # Casi di errore
  # ===============================================================================================

  @negativo @FEAT_001_CUP_scenario_02
  Schema dello scenario: Valorizzazione di più parametri identificativi
    Dato Il PSP ha ricevuto dalla Corporate un file di input non valido, contenente più parametri identificativi (<organizationFiscalCode>, <istatCode>, <catastalCode>)
    Quando Il PSP Invia la primitiva demandPaymentNotice valorizzando più di un parametro identificativo (<organizationFiscalCode>, <istatCode>, <catastalCode>)
    Allora Il PSP riceve un 200 OK che all'interno riporta il fault code <risposta>

    Esempi:
      | organizationFiscalCode | istatCode | catastalCode | risposta                                |
      | 02438750586            | 058091    |              | PPT_MULTI_IDENTIFICATIVO_NON_CONSENTITO |
      |                        | 058091    | H501         | PPT_MULTI_IDENTIFICATIVO_NON_CONSENTITO |
      | 02438750586            |           | H501         | PPT_MULTI_IDENTIFICATIVO_NON_CONSENTITO |

  # ===============================================================================================

  @negativo @FEAT_001_CUP_scenario_03
  Schema dello scenario: Il dato fornito (CF, ISTAT o Catastale) non rispetta il formato sintattico previsto
    Dato Il PSP ha ricevuto dalla Corporate un file di input non valido, contenente uno dei parametri identificativi (<organizationFiscalCode>, <istatCode>, <catastalCode>) che non rispetta il formato sintattico previsto
    Quando Il PSP Invia la primitiva demandPaymentNotice valorizzando uno dei parametri identificativi (<organizationFiscalCode>, <istatCode>, <catastalCode>) non rispettando il formato sintattico previsto
    Allora Il PSP riceve un 200 OK che all'interno riporta il fault code <risposta>

    Esempi:
      | organizationFiscalCode | istatCode | catastalCode | risposta                            |
      | 02438750586000         |           |              | PPT_PARAMETRO_IDENTIFICATIVO_ERRATO |
      |                        | 058091A   |              | PPT_PARAMETRO_IDENTIFICATIVO_ERRATO |
      |                        |           | H50          | PPT_PARAMETRO_IDENTIFICATIVO_ERRATO |

  # ===============================================================================================

  @negativo @FEAT_001_CUP_scenario_04
  Schema dello scenario: Mancanza di uno o più parametri obbligatori
    Dato Il PSP ha ricevuto dalla Corporate un file di input non valido, in cui sono assenti uno o più campi mandatori (<debtorFiscalCode>, <debtorFullName>, <amount>)
    Quando Il PSP Invia la primitiva demandPaymentNotice priva di uno dei campi mandatori (<debtorFiscalCode>, <debtorFullName>, <amount>)
    Allora Il PSP riceve un 200 OK che all'interno riporta il fault code <risposta>

    Esempi:
      | debtorFiscalCode | debtorFullName | amount | risposta                      |
      | 00488410010      | TIM S.p.A      |        | PPT_DATI_OBBLIGATORI_MANCANTI |
      | 00488410010      |                | 50000  | PPT_DATI_OBBLIGATORI_MANCANTI |
      |                  | TIM S.p.A      | 50000  | PPT_DATI_OBBLIGATORI_MANCANTI |

  # ===============================================================================================

  @negativo @FEAT_001_CUP_scenario_05
  Schema dello scenario: Formato dei campi amount o debtorFiscalCode non valido
    Dato Il PSP ha ricevuto dalla Corporate un file di input non valido, in cui uno dei campi mandatori (<amount>, <debtorFiscalCode>) è valorizzato con un formato errato
    Quando Il PSP Invia una richiesta con il formato errato di uno dei campi (<amount>, <debtorFiscalCode>)
    Allora Il PSP riceve un 200 OK che all'interno riporta il fault code <risposta>

    Esempi:
      | debtorFiscalCode | amount | risposta                  |
      | 00488            |        | PPT_FORMATO_DATI_INVALIDO |
      |                  | 500.00 | PPT_FORMATO_DATI_INVALIDO |

  # ===============================================================================================

  @negativo @FEAT_001_CUP_scenario_06
  Schema dello scenario: La chiave di ricerca fornita (CF, ISTAT o Catastale) non è presente in cache
    Dato Il PSP ha ricevuto dalla Corporate un file di input valido, contenente uno dei parametri identificativi (<organizationFiscalCode>, <istatCode>, <catastalCode>) non presente nella cache multi-livello
    Quando Il PSP Invia la primitiva demandPaymentNotice valorizzando uno dei parametri identificativi (<organizationFiscalCode>, <istatCode>, <catastalCode>) con un valore non presente nella cache multi-livello
    Allora Il PSP riceve un 200 OK che all'interno riporta il fault code <errore_output>

    Esempi:
      | organizationFiscalCode | istatCode | catastalCode | errore_output                  |
      | 81001550435            |           |              | PPT_CODICE_FISCALE_NON_CENSITO |
      |                        | 043001    |              | PPT_CODICE_ISTAT_NON_CENSITO   |
      |                        |           | A031         | PPT_CODICE_CATASTO_NON_CENSITO |
