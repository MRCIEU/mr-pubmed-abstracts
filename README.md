# Analyse abstracts of MR papers using OpenAI


Create a .env file in the root directory and add the following variables:

```bash
OPENAI_API_KEY=your_openai_api_key
```


## Background

The PubMed search term "Mendelian randomisation" [Title] OR "Mendelian randomization" [Title]" yields nearly 7000 results at the time of writing. This script will extract the following information from those results:

- Pubmed ID
- Title
- Abstract
- Publication date
- Journal name
- Journal ISSN
- First author's affiliation

It's saved in `data/pubmed.json`.

The `scripts/openai-extract.py` script will then use the OpenAI API to generate a summary of each of those abstracts. The prompt on how to analyse the abstract is as follows:

> What are the exposures and outcomes in this abstract? If there are multiple exposures or outcomes, provide them all. If there are no exposures or outcomes, provide an empty list. Also categorize the exposures and outcomes into the following groups: 
> - molecular
> - socioeconomic
> - environmental
> - behavioural
> - anthropmetric
> - clinical measures
> - infectious disease
> - neoplasm
> - disease of the blood and blood-forming organs
> - metabolic disease
> - mental disorder
> - disease of the nervous system
> - disease of the eye and adnexa
> - disease of the ear and mastoid process
> - disease of the circulatory system
> - disease of the digestive system
> - disease of the skin and subcutaneous tissue
> - disease of the musculoskeletal system and connective tissue
> - disease of the genitourinary system
> 
> If an exposure or outcome does not fit into any of these groups, provide a new group name. Provide your answer in strict json format without markdown code blocks.

An example output looks like:

```json
{
  "exposures": [
    {
        "id": "1",
        "trait": "Particulate matter 2.5",
        "category": "Environmental"
    },
    {
        "id": "2",
        "trait": "Type 2 diabetes",
        "category": "metabolic disease"
    },
    {
        "id": "3",
        "trait": "Body mass index",
        "category": "Anthropometric"
    }
  ],
  "outcomes": [
    {
        "id": "1",
        "trait": "Forced expiratory volume in 1 s",
        "category": "Clinical measure"
    },
    {
        "id": "2",
        "trait": "Forced vital capacity",
        "category": "Clinical measure"
    },
    {
        "id": "3",
        "trait": "Gastroesophageal reflux disease",
        "category": "disease of the digestive system"
    },
    {
        "id": "4",
        "trait": "Non-alcoholic fatty liver disease (NAFLD)",
        "category": "disease of the digestive system"
    }
  ]
}
```

For every abstract in `data/pubmed.json`, the script will generate a summary and save it in `data/pubmed-abstracts.json`.


