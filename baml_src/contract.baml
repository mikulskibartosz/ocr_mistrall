class Contact {
  name string
  title string?
  email string?
}

class Party {
  name string @description("Mianownik, liczba pojedyncza, bez zwrotów grzecznościowych")
  role string
  contact Contact?
}

class RelatedAgreement {
  type string
  date string?
}

class WorkStream {
  major_tasks string[]
  deliverables string[]
}

class Role {
  role string
  responsibilities string[]
}

class Services {
  work_stream WorkStream
  roles Role[]
  total_resources string?
}

class ProjectPlanAndMilestones {
  start_date string?
  end_date string?
}

class CostStructure {
  work_stream string?
  duration string?
  resources string?
  rate string?
}

class PaymentTerms {
  due_date string?
}

class PricingModel {
  cost_structure CostStructure[]
  payment_terms PaymentTerms
}

class AcceptanceCriteria {
  deliverables string[]
}

class DurationAndTermination {
  start_date string?
  end_condition string?
}

class ScopeOfWork {
  services Services
  project_plan_and_milestones ProjectPlanAndMilestones
  place_of_performance string?
  pricing_model PricingModel
  acceptance_criteria AcceptanceCriteria
  duration_and_termination DurationAndTermination
  miscellaneous_provisions string?
}

class Contract {
  subject string
  date string?
  parties Party[]
  related_agreements RelatedAgreement[]
  scope_of_work ScopeOfWork
  net_value string | float
  currency string?
  contract_name string?
}

function ExtractContract(contract: string) -> Contract {
  client Mistral
  prompt #"You are an expert extraction algorithm designed to output ONLY raw JSON.

Your task is to extract relevant information from the contract text provided below and create a structured JSON object following this schema:

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

Output Instructions:
1. Your entire output MUST be ONLY the raw JSON object.
2. Do not include ```json or ``` markers around the JSON.
3. Do not include any explanations, notes, or text before or after the JSON object.
4. Start the output directly with an opening curly brace and end it directly with a closing curly brace.
5. Ensure the JSON is valid and properly formatted.

### EXAMPLE INPUT:
UMOWA ZLECENIE

zawarta w dniu 2025-04-22 w Krakowie, pomiędzy:

Zielony Ogród Sp. z o.o. z siedzibą w Krakowie, adres: Kwiatowa 15, posiadającą NIP: 9453267891, REGON: 123456789, reprezentowaną przez: Annę Nowak - Prezes Zarządu, zwaną dalej „Zleceniodawcą",
a
Panem Tomaszem Markowskim zamieszkałym przy ul. Słonecznej 7, 32-400 Myślenice, posiadającym nr PESEL: 89071512345, zwanego dalej „Zleceniobiorcą"

1. Zleceniodawca zleca, a Zleceniobiorca zobowiązuje się wykonać w sposób samodzielny następujące czynności: projektowanie układu roślin w ogrodzie pokazowym.
2. Umowa zawarta jest od dnia do dnia: 2025-04-25-2025-05-10
3. Zleceniobiorcy za wykonanie czynności określonych w pkt 1 przysługuje wynagrodzenie brutto w wysokości 12000 zł, płatne przelewem na rachunek bankowy wskazany przez Zleceniobiorcę.
4. Zleceniobiorca nie może bez pisemnej zgody Zleceniodawcy powierzyć wykonania niniejszej umowy w części lub w całości innej osobie ani też przelewać na nią swoich praw wynikających z umowy.
5. W przypadku, gdy należne wynagrodzenie z tytułu niniejszej umowy wymienione w pkt 3 podlega opodatkowaniu podatkiem dochodowym od osób fizycznych, podatek ten obciąża Zleceniobiorcę
i zaliczka na podatek jest przekazywana za pośrednictwem Spółki do właściwego urzędu skarbowego z wyłączeniem przypadków określonych w art. 44 ustawy o podatku dochodowym od osób fizycznych (najem, dzierżawa, działalność gospodarcza), w którym Zleceniobiorca zobowiązany jest samodzielnie dokonać wpłaty zaliczek na podatek dochodowy na rzecz właściwego urzędu skarbowego.
6. Zleceniobiorca zobowiązuje się, z zastrzeżeniem ust.7, do traktowania jako poufnych wszelkich informacji, które zostaną mu udostępnione lub przekazane przez Zleceniodawcę w związku z wykonaniem niniejszej umowy, nie udostępniania ich w jakikolwiek sposób osobom trzecim bez pisemnej zgody Zleceniodawcy i wykorzystania ich tylko do celów określonych w umowie.
7. Obowiązek zachowania poufności, o którym mowa w powyższym punkcie nie dotyczy informacji które:
1) w czasie ich ujawnienia były publicznie znane,
2) których obowiązek ujawnienia wynika z orzeczenia sądu lub decyzji innego uprawnionego organu władz, z zastrzeżeniem niezwłocznego powiadomienia Zleceniodawcy o takim obowiązku.
8. Wszelkie zmiany niniejszej umowy wymagają formy pisemnej.

### EXAMPLE OUTPUT:
{
  "subject": "UMOWA ZLECENIE",
  "date": "2025-04-22",
  "parties": [
    {
      "name": "Zielony Ogród Sp. z o.o., Kwiatowa 15, Krakow, NIP: 9453267891, REGON: 123456789, Prezes Zarządu: Anna Nowak",
      "role": "Zleceniodawca"
    },
    {
      "name": "Tomasz Markowski, ul. Słoneczna 7, 32-400 Myślenice, nr PESEL: 89071512345",
      "role": "Zleceniobiorca"
    }
  ],
  "related_agreements": [],
  "scope_of_work": {
    "services": {
      "work_stream": {
        "major_tasks": ["projektowanie układu roślin w ogrodzie pokazowym"],
        "deliverables": []
      },
      "roles": []
    },
    "project_plan_and_milestones": {
      "start_date": "2025-04-25",
      "end_date": "2025-05-10"
    },
    "place_of_performance": "missing",
    "pricing_model": {
      "cost_structure": [],
      "payment_terms": {
        "due_date": "missing"
      }
    },
    "acceptance_criteria": {
      "deliverables": ["projekt układu roślin w ogrodzie pokazowym"]
    },
    "duration_and_termination": {
      "start_date": "2025-04-25",
      "end_condition": "missing"
    },
    "miscellaneous_provisions": "missing"
  },
  "net_value": "12000",
  "currency": "PLN",
  "contract_name": "UMOWA ZLECENIE"
}

In Polish, the change from "Markowskim" to "Markowski" involves understanding the case system, specifically changing from the instrumental case to the nominative case for surnames. Here are the rules:
-skim → -ski (Kowalskim → Kowalski)
-ckim → -cki (Nowiackim → Nowiacki)
-dzkim → -dzki (Zawadzkim → Zawadzki)
-ką → -ka (Nowaczką → Nowaczka)
-em → ∅ (Kowalczykiem → Kowalczyk)
-czem → -cz (Kowaczem → Kowacz)
-wiczem → -wicz (Adamkiewiczem → Adamkiewicz)
-ową → -owa (Nowakową → Nowakowa)
-ówną → -ówna (Kowalczówną → Kowalczówna)
-lem → -l (Wróbelem → Wróbel)
-piem → -p (Karpiem → Karp)

Contract Text to Analyze:
    {{ contract }}

    {{ ctx.output_format }}
  "#
}

test sample_contract {
  functions [ExtractContract]
  args {
    contract #"UMOWA ZLECENIE

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
8. Wszelkie zmiany niniejszej umowy wymagają formy pisemnej.
    "#
  }
  @@assert(contract_name, {{ this.contract_name == "UMOWA ZLECENIE" }})
  @@assert(net_value, {{ this.net_value == "700" }})
  @@assert(currency, {{ this.currency == "PLN" }})
  @@assert(date, {{ this.date == "2025-04-20" }})
  @@assert(parties, {{ this.parties | length == 2 }})
  @@assert(parties.zleceniodawca.name, {{ this.parties[0].name == "Komar SP. Z O.O., Dworcowa 4, Zgierz, NIP: 78500112233, REGON: 987654321, Prezes Zarządu: Mieczysław Okonia" }})
  @@assert(parties.zleceniodawca.role, {{ this.parties[0].role == "Zleceniodawca" }})
  @@assert(parties.zleceniobiorca.name, {{ this.parties[1].name == "Tomasz Karp, ul. Leśna 3, 01-234 Robakowo, nr PESEL: 98123100123" }})
  @@assert(parties.zleceniobiorca.role, {{ this.parties[1].role == "Zleceniobiorca" }})
  @@assert(scope_of_work.services.work_stream.major_tasks, {{ this.scope_of_work.services.work_stream.major_tasks == ["malowanie szopy na narzędzia"] }})
  @@assert(scope_of_work.services.work_stream.major_tasks, {{ this.scope_of_work.services.work_stream.roles == []}})
  @@assert(scope_of_work.project_plan_and_milestones.start_date, {{ this.scope_of_work.project_plan_and_milestones.start_date == "2025-04-20" }})
  @@assert(scope_of_work.project_plan_and_milestones.end_date, {{ this.scope_of_work.project_plan_and_milestones.end_date == "2025-04-22" }})
  @@assert(scope_of_work.acceptance_criteria.deliverables, {{ this.scope_of_work.acceptance_criteria.deliverables == ["malowanie szopy na narzędzia"] }})
  @@assert(scope_of_work.duration_and_termination.start_date, {{ this.scope_of_work.duration_and_termination.start_date == "2025-04-20" }})
  @@assert(scope_of_work.duration_and_termination.end_condition, {{ this.scope_of_work.duration_and_termination.end_condition == "missing" }})
}
