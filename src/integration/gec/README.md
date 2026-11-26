# GEC integration suite

Suite Behave per parità AFM/GEC.

## Configurazione chiavi principali

Nei file [dev.yaml](./dev.yaml) e [uat.yaml](./uat.yaml):

- `gec.url`: host V1 (`/fees`, `/psps/{idPsp}/fees`, `/payment-methods/search`)
- `gec.url_v2`: host V2 (`/fees/multi`)
- `gec.extension`: query di default V2 (es. `?maxOccurrences=10`)
- `gec.marketplace_host`: host marketplace (`/payment-methods`)
- `gec.marketplace_key`: subscription key marketplace
- `gec.auth.*`: subscription key calcolatore/configurazione
- `gec.azure_connection_string`: connection string Azure Table (issuer range)
- `gec.timeout`: timeout delle richieste in secondi (5 in DEV/UAT)

In `config/.secrets.yaml`, sia `dev` sia `uat` richiedono i segreti reali:
`tas-gec-calculator-subscription-key`, `tas-gec-marketplace-subscription-key` e
`azure-storage-connection-string`.

In `global_configuration`:

- `id_psp_poste`
- `poste_channel_ids`
- `poste_pay_channel_ids`
- `all_ccp_new_filter_enabled`
- `amex_abi`
- `psp_blacklist`
- `issuer_range_table`
- `payment_method_paypal`
- `payment_method_cards`

## Setup/teardown

- Caricamento `data.json`: un POST `/configuration/bundles/add` con `ciBundleList` annidata, poi `/configuration/touchpoint/add` e `/configuration/paymenttypes/add`.
- Caricamento metodi test: POST marketplace `/payment-methods`; vengono tracciati gli ID restituiti dal payload caricato.
- Setup issuer: snapshot delle righe esistenti nelle sole partizioni `300000`, `309500` e `340000`, prima della cancellazione e del setup dei range.
- Teardown: POST `/configuration/bundles/delete` con bundle tracciati, DELETE marketplace solo per gli ID dei metodi caricati con successo e ripristino best-effort dello snapshot issuer dopo la rimozione delle sole righe fixture `ISSUER_ENTITIES`.
