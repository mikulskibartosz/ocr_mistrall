from mistralai import Mistral
from ocr.config import load_config

config = load_config()

data = """# UMOWA ZLECENIE

zawarta w dniu 2025-04-20 w Warszawie, pomiędzy:

Komar SP. Z O.O. z siedzibą w Zgierzu., adres: Dworcowa 4, posiadającą NIP: 78500112233, REGON: 987654321, reprezentowaną przez: Mieczysława Okonia. - Prezesa Zarządu, zwaną dalej „Zleceniodawcą",
a
Panem Tomaszem Karpiem zamieszkałym przy ul. Leśnej 3, 01-234 Robakowo, posiadającym nr PESEL: 98123100123., zwaną dalej „Zleceniobiorcą"

1. Zleceniodawca zleca, a Zleceniobiorca zobowiązuje się wykonać w sposób samodzielny następujące czynności: malowanie szopy na narzędzia.
2. Umowa zawarta jest od dnia do dnia: 2025-04-20-2025-04-22
3. Zleceniobiorcy za wykonanie czynności określonych w pkt 1 przysługuje wynagrodzenie brutto w wysokości 700 zł, płatne przelewem na rachunek bankowy wskazany przez Zleceniobiorcę.
4. Zleceniobiorca nie może bez pisemnej zgody Zleceniodawcy powierzyć wykonania niniejszej umowy w części lub w całości innej osobie ani też przelewać na nią swoich praw wynikających z umowy.
5. W przypadku, gdy należne wynagrodzenie z tytułu niniejszej umowy wymienione w pkt 3 podlega opodatkowaniu podatkiem dochodowym od osób fizycznych, podatek ten obciąża Zleceniobiorcę
i zaliczka na podatek jest przekazywana za pośrednictwem Spółki do właściwego urzędu skarbowego z wyłączeniem przypadków określonych w art. 44 ustawy o podatku dochodowym od osób fizycznych (najem, dzierżawa, działalność gospodarcza), w którym Zleceniobiorca zobowiązany jest samodzielnie dokonać wpłaty zaliczek na podatek dochodowy na rzecz właściwego urzędu skarbowego.
6. Zleceniobiorca zobowiązuje się, z zastrzeżeniem ust.7, do traktowania jako poufnych wszelkich informacji, które zostaną mu udostępnione lub przekazane przez Zleceniodawcę w związku z wykonaniem niniejszej umowy, nie udostępniania ich w jakikolwiek sposób osobom trzecim bez pisemnej zgody Zleceniodawcy i wykorzystania ich tylko do celów określonych w umowie.
7. Obowiązek zachowania poufności, o którym mowa w powyższym punkcie nie dotyczy informacji które:
1) w czasie ich ujawnienia były publicznie znane,
2) których obowiązek ujawnienia wynika z orzeczenia sądu lub decyzji innego uprawnionego organu władz, z zastrzeżeniem niezwłocznego powiadomienia Zleceniodawcy o takim obowiązku.
8. Wszelkie zmiany niniejszej umowy wymagają formy pisemnej."""

prompt_template = """You are an expert extraction algorithm designed to output ONLY raw JSON.

Your task is to extract relevant information from the contract text provided below and create a structured JSON object following this schema:

```
{
  "type": "object",
  "properties": {
    "subject": { "type": "string" },
    "date": { "type": ["string", "null"] },
    "parties": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "role": { "type": "string" },
          "contact": {
            "type": ["object", "null"],
            "properties": {
              "name": { "type": "string" },
              "title": { "type": ["string", "null"] },
              "email": { "type": ["string", "null"] }
            },
            "required": ["name"]
          }
        },
        "required": ["name", "role"]
      }
    },
    "related_agreements": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": ["string", "null"] },
          "date": { "type": ["string", "null"] }
        },
        "required": ["type"]
      }
    },
    "scope_of_work": {
      "type": "object",
      "properties": {
        "services": {
          "type": "object",
          "properties": {
            "testing_services": {
              "type": "object",
              "properties": {
                "work_stream": {
                  "type": "object",
                  "properties": {
                    "major_tasks": { "type": "array", "items": { "type": "string" } },
                    "deliverables": { "type": "array", "items": { "type": "string" } }
                  }
                },
                "roles": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "role": { "type": "string" },
                      "responsibilities": { "type": "array", "items": { "type": "string" } }
                    },
                    "required": ["role", "responsibilities"]
                  }
                },
                "total_resources": { "type": ["string", "null"] }
              }
            }
          }
        },
        "project_plan_and_milestones": {
          "type": "object",
          "properties": {
            "start_date": { "type": ["string", "null"] },
            "end_date": { "type": ["string", "null"] }
          }
        },
        "place_of_performance": { "type": ["string", "null"] },
        "pricing_model": {
          "type": "object",
          "properties": {
            "cost_structure": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "work_stream": { "type": ["string", "null"] },
                  "duration": { "type": ["string", "null"] },
                  "resources": { "type": ["string", "null"] },
                  "rate": { "type": ["string", "null"] }
                }
              }
            },
            "payment_terms": {
              "type": "object",
              "properties": {
                "due_date": { "type": ["string", "null"] }
              }
            }
          }
        },
        "acceptance_criteria": {
          "type": "object",
          "properties": {
            "deliverables": { "type": "array", "items": { "type": "string" } }
          }
        },
        "duration_and_termination": {
          "type": "object",
          "properties": {
            "start_date": { "type": ["string", "null"] },
            "end_condition": { "type": ["string", "null"] }
          }
        },
        "miscellaneous_provisions": { "type": ["string", "null"] }
      }
    },
    "net_value": { "type": ["number", "string"] },
    "currency": { "type": ["string", "null"] },
    "contract_name": { "type": ["string", "null"] }
  },
  "required": ["subject", "parties", "related_agreements", "scope_of_work"]
}
```

Field Extraction Guidelines:

1. For all fields, if you cannot find the information in the text, use "missing" as the value.
2. For date fields, use YYYY-MM-DD format.
3. For the "net_value" field:
   - Extract the total net value of the agreement/order as a raw number
   - Use a period (.) as the decimal separator (e.g., 10000.50 or 97800)
   - If no explicit total value is found, return "missing"
   - Example of a correct output: 12345.67 or "missing"
4. For the "currency" field, extract the currency associated with monetary values.
5. For "contract_name", extract the title or name of the contract document.
6. For all array fields, provide empty arrays [] if no items are found.
7. For all object fields with no data, provide empty objects {}.

Contract Text to Analyze:
{{input_text}}

Output Instructions:
1. Your entire output MUST be ONLY the raw JSON object.
2. Do not include ```json or ``` markers around the JSON.
3. Do not include any explanations, notes, or text before or after the JSON object.
4. Start the output directly with an opening curly brace and end it directly with a closing curly brace.
5. Ensure the JSON is valid and properly formatted."""

prompt = prompt_template.replace("{{input_text}}", data)

mistral = Mistral(api_key=config.mistral_api_key)

response = mistral.chat.complete(
    model=config.mistral_model,
    messages=[{"role": "user", "content": prompt}],
)

print(response.choices[0].message.content)


# Przykładowa odpowiedź:
# ```
# {
#  "type": "object",
#   "properties": {
#     "subject": { "type": "string", "enum": ["UMOWA ZLECENIE"] },
#     "date": { "type": "string", "enum": ["2025-04-20"] },
#     "parties": [
#       {
#         "name": { "type": "string", "enum": ["Komar SP. Z O.O."] },
#         "role": { "type": "string", "enum": ["Zleceniodawca"] },
#         "contact": {
#           "name": { "type": "string", "enum": ["Mieczysława Okonia"] },
#           "title": { "type": "null" },
#           "email": { "type": "null" }
#         }
#       },
#       {
#         "name": { "type": "string", "enum": ["Pan Tomasz Karp"] },
#         "role": { "type": "string", "enum": ["Zleceniobiorca"] },
#         "contact": {
#           "name": { "type": "string", "enum": ["Tomasz Karp"] },
#           "title": { "type": "null" },
#           "email": { "type": "null" }
#         }
#       }
#     ],
#     "related_agreements": [],
#     "scope_of_work": {
#       "services": {
#         "testing_services": {
#           "work_stream": {
#             "major_tasks": ["malowanie szopy na narzędzia"]
#           },
#           "roles": [],
#           "total_resources": { "type": "null" }
#         }
#       },
#       "project_plan_and_milestones": {
#         "start_date": { "type": "string", "enum": ["2025-04-20"] },
#         "end_date": { "type": "string", "enum": ["2025-04-22"] }
#       },
#       "place_of_performance": { "type": "string", "enum": ["Warszawa"] },
#       "pricing_model": {
#         "cost_structure": [],
#         "payment_terms": {
#           "due_date": { "type": "null" }
#         }
#       },
#       "acceptance_criteria": {
#         "deliverables": ["malowanie szopy na narzędzia"]
#       },
#       "duration_and_termination": {
#         "start_date": { "type": "string", "enum": ["2025-04-20"] },
#         "end_condition": { "type": "null" }
#       },
#       "miscellaneous_provisions": { "type": "string", "enum": ["Zleceniobiorca nie może bez pisemnej zgody Zleceniodawcy powierzyć wykonania niniejszej umowy w części lub w całości innej osobie ani też przelewać na nią swoich praw wynikających z umowy..."] }
#     },
#     "net_value": { "type": "string", "enum": ["700"] },
#     "currency": { "type": "string", "enum": ["PLN"] },
#     "contract_name": { "type": "string", "enum": ["UMOWA ZLECENIE"] }
#   },
#   "required": ["subject", "parties", "scope_of_work"]
# }
# ```
