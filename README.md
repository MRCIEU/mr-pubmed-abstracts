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
> - anthropometric
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

For an example abstract:


> Background: The association between air pollution, lung function, gastroesophageal reflux disease, and Non-alcoholic fatty liver disease (NAFLD) remains inconclusive. Previous studies were not convincing due to confounding factors and reverse causality. We aim to investigate the causal relationship between air pollution, lung function, gastroesophageal reflux disease, and NAFLD using Mendelian randomization analysis.
> 
> Methods: In this study, univariate Mendelian randomization analysis was conducted first. Subsequently, Steiger testing was performed to exclude the possibility of reverse association. Finally, significant risk factors identified from the univariate Mendelian analysis, as well as important factors affecting NAFLD from previous observational studies (type 2 diabetes and body mass index), were included in the multivariable Mendelian randomization analysis.
>
> Results: The results of the univariable Mendelian randomization analysis showed a positive correlation between particulate matter 2.5, gastroesophageal reflux disease, and NAFLD. There was a negative correlation between forced expiratory volume in 1 s, forced vital capacity, and NAFLD. The multivariable Mendelian randomization analysis indicated a direct causal relationship between gastroesophageal reflux disease (OR = 1.537, p = 0.011), type 2 diabetes (OR = 1.261, p < 0.001), and NAFLD.
>
> Conclusion: This Mendelian randomization study confirmed the causal relationships between air pollution, lung function, gastroesophageal reflux, and NAFLD. Furthermore, gastroesophageal reflux and type 2 diabetes were identified as independent risk factors for NAFLD, having a direct causal connection with the occurrence of NAFLD.


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



## Update

New prompt to attempt to parse methods used:

> What are the exposures and outcomes in this abstract? If there are multiple exposures or outcomes, provide them all. If there are no exposures or outcomes, provide an empty list. Also categorize the exposures and outcomes into the following groups using the exact category names provided: 
> - molecular
> - socioeconomic
> - environmental
> - behavioural
> - anthropometric
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
> If an exposure or outcome does not fit into any of these groups, specify "Other". 
> List the analytical methods used in the abstract. Match the methods to the following list of exact method names. If a method is used that is not in the list, specify "Other" and also provide the name of the method. The list of methods is as follows:
> - two-sample mendelian randomization
> - multivariable mendelian randomization
> - colocalization
> - network mendelian randomization
> - triangulation
> - reverse mendelian randomization
> - one-sample mendelian randomization
> - negative controls
> - sensitivity analysis
> - non-linear mendelian randomization
> - within-family mendelian randomization
> Summarise how many null vs non-null results were found in the abstract.
> Provide your answer in strict json format using exactly the format as the example output and without markdown code blocks.


Note that it needs improvement, doesn't work particularly well at sticking to listed methods.