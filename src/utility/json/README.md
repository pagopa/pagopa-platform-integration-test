# Utility JSON (`src/utility/json`)

Utility minime per conversione tra stringhe JSON e dizionari Python.

## API disponibili

- `json_to_dict(json_str)`
  - converte una stringa JSON in `dict`
  - solleva `JsonConversionError` se input non valido, vuoto, malformato o con root non object

- `dict_to_json(data)`
  - converte un `dict` in stringa JSON formattata
  - solleva `JsonConversionError` se input non valido o non serializzabile

- `get_attr(data, attr_path)`
  - recupera un valore da un `dict` usando un path nel formato `chiave1.chiave2...`
  - supporta anche indici lista, ad esempio `items[0].id`
  - solleva `JsonAttributeError` se il path non esiste o non e' navigabile

- `set_attr(data, attr_path, value)`
  - imposta un valore in un `dict` usando un path nel formato `chiave1.chiave2...`
  - supporta anche indici lista, ad esempio `items[0].id`
  - con `create_missing=False` (default) lancia errore se l'alberatura manca
  - con `create_missing=True` crea i nodi mancanti quando necessario
  - solleva `JsonAttributeSetError` se il path non e' scrivibile

## Esempio rapido

```python
from src.utility.json import dict_to_json, get_attr, json_to_dict, set_attr

payload = json_to_dict('{"outcome":"OK","amount":100}')
json_text = dict_to_json(payload)
outcome = get_attr({"response": payload}, "response.outcome")
container = {}
set_attr(container, "object[0].id", "A1", create_missing=True)
print(payload["outcome"])
print(outcome)
print(container)
print(json_text)
```

