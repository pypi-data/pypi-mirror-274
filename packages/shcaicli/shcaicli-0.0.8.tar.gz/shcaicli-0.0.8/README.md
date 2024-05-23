# SHCAi Client 
![build](https://github.com/ihealth-group/shcai-cli/actions/workflows/ci-cd.yml/badge.svg) 
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

### Instalação

Para instalar o SHCAi client: `pip install -U shcaicli`

### Uso

```python
from shcaicli.api import SHCAi
import os

api_key = os.getenv('API_KEY')
shc = SHCAi(api_key=api_key, tokens_mode=True)

cn = 'Paciente diagnosticado com has, nega dm. Em 20/09 iniciou QT para tratamento CA de mama'
cn_inferred = shc.infer(cn=cn)
```

### Estrutura de retorno

O exemplo acima retorna a seguinte estrutura:

<details>
    <summary>Clique para ver</summary>

```json
[
    {
        "text_tokens": [
            "Paciente",
            "diagnosticado",
            "com",
            "has",
            ",",
            "nega",
            "dm",
            ".",
            "Em",
            "20/09",
            "iniciou",
            "QT",
            "para",
            "tratamento",
            "CA",
            "de",
            "mama"
        ],
        "clinical_entities": [
            {
                "entity": "has",
                "entity_tokens": [
                    "has"
                ],
                "label": "DISEASE",
                "start": 3,
                "end": 4,
                "assertion": "PRESENTE",
                "adverse_event": "",
                "el": {
                    "term_text": "I10 - hipertensão essencial (primária)",
                    "terminology": "ICD10",
                    "term_code": "I10",
                    "term_desc": "hipertensão essencial (primária)"
                },
                "relations": []
            },
            {
                "entity": "dm",
                "entity_tokens": [
                    "dm"
                ],
                "label": "DISEASE",
                "start": 6,
                "end": 7,
                "assertion": "AUSENTE",
                "adverse_event": "",
                "el": {
                    "term_text": "E14 - diabetes mellitus não especificado",
                    "terminology": "ICD10",
                    "term_code": "E14",
                    "term_desc": "diabetes mellitus não especificado"
                },
                "relations": []
            },
            {
                "entity": "20/09",
                "entity_tokens": [
                    "20/09"
                ],
                "label": "TEMPORAL_CONCEPT",
                "start": 9,
                "end": 10,
                "assertion": "",
                "adverse_event": "",
                "el": {
                    "term_text": "",
                    "terminology": "",
                    "term_code": "",
                    "term_desc": ""
                },
                "relations": [
                    {
                        "entity": "QT",
                        "entity_tokens": [
                            "QT"
                        ],
                        "position": "tail",
                        "start": 11,
                        "end": 12,
                        "type": "is_date_of"
                    }
                ]
            },
            {
                "entity": "QT",
                "entity_tokens": [
                    "QT"
                ],
                "label": "PROCEDURE",
                "start": 11,
                "end": 12,
                "assertion": "PRESENTE",
                "adverse_event": "",
                "el": {
                    "term_text": "",
                    "terminology": "",
                    "term_code": "",
                    "term_desc": ""
                },
                "relations": [
                    {
                        "entity": "20/09",
                        "entity_tokens": [
                            "20/09"
                        ],
                        "position": "head",
                        "start": 9,
                        "end": 10,
                        "type": "is_date_of"
                    }
                ]
            },
            {
                "entity": "CA",
                "entity_tokens": [
                    "CA"
                ],
                "label": "DISEASE",
                "start": 14,
                "end": 15,
                "assertion": "PRESENTE",
                "adverse_event": "",
                "el": {
                    "term_text": "",
                    "terminology": "",
                    "term_code": "",
                    "term_desc": ""
                },
                "relations": [
                    {
                        "entity": "mama",
                        "entity_tokens": [
                            "mama"
                        ],
                        "position": "tail",
                        "start": 16,
                        "end": 17,
                        "type": "disease_has_primary_anatomic_site"
                    }
                ]
            },
            {
                "entity": "mama",
                "entity_tokens": [
                    "mama"
                ],
                "label": "BODY_PART",
                "start": 16,
                "end": 17,
                "assertion": "",
                "adverse_event": "",
                "el": {
                    "term_text": "",
                    "terminology": "",
                    "term_code": "",
                    "term_desc": ""
                },
                "relations": [
                    {
                        "entity": "CA",
                        "entity_tokens": [
                            "CA"
                        ],
                        "position": "head",
                        "start": 14,
                        "end": 15,
                        "type": "disease_has_primary_anatomic_site"
                    }
                ]
            }
        ],
        "biomarkers": [],
        "lab_tests": [],
        "vital_signs": [],
        "entities_relations": [
            {
                "relation_type": "is_date_of",
                "head_entity": "20/09",
                "tail_entity": "QT",
                "head_entity_tokens": [
                    "20/09"
                ],
                "tail_entity_tokens": [
                    "QT"
                ],
                "head_start": 9,
                "head_end": 10,
                "tail_start": 11,
                "tail_end": 12
            },
            {
                "relation_type": "disease_has_primary_anatomic_site",
                "head_entity": "CA",
                "tail_entity": "mama",
                "head_entity_tokens": [
                    "CA"
                ],
                "tail_entity_tokens": [
                    "mama"
                ],
                "head_start": 14,
                "head_end": 15,
                "tail_start": 16,
                "tail_end": 17
            }
        ]
    }
]
```
</details>

Atenção especial para a estrutura de cada `clinical_entities`:

```json
{
    "entity": "20/09",
    "entity_tokens": [
        "20/09"
    ],
    "label": "TEMPORAL_CONCEPT",
    "start": 9,
    "end": 10,
    "assertion": "",
    "adverse_event": "",
    "el": {
        "term_text": "",
        "terminology": "",
        "term_code": "",
        "term_desc": ""
    },
    "relations": [
        {
            "entity": "QT",
            "entity_tokens": [
                "QT"
            ],
            "position": "tail",
            "start": 11,
            "end": 12,
            "type": "is_date_of"
        }
    ]
}
```

O campo `relations` está presente e mostra a quais outras entidades ela está relacionada. No exemplo acima, a entidade
categorizada como `TEMPORAL_CONCEPT` `20/09` possui uma relação com a entidade `QT`. Ao analisar a relação vemos o campo
especial `position` ele mostra que `QT` está no `tail` da relação que deve ser lida assim:

`20/09 is_date_of QT`

### Tokens do texto da nota

O texto clínico foi quebrado em tokens para facilitar a identificação de cada item entre as relações. Os campos `start` e
`end` fazem referência a posição do token na lista de tokens.