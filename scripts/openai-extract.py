from openai import OpenAI
import json
import os
import dotenv

dotenv.load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

abstract1 = {"role": "user", "content": "Associations between modifiable exposures and disease seen in observational epidemiology are sometimes confounded and thus misleading, despite our best efforts to improve the design and analysis of studies. Mendelian randomization-the random assortment of genes from parents to offspring that occurs during gamete formation and conception-provides one method for assessing the causal nature of some environmental exposures. The association between a disease and a polymorphism that mimics the biological link between a proposed exposure and disease is not generally susceptible to the reverse causation or confounding that may distort interpretations of conventional observational studies. Several examples where the phenotypic effects of polymorphisms are well documented provide encouraging evidence of the explanatory power of Mendelian randomization and are described. The limitations of the approach include confounding by polymorphisms in linkage disequilibrium with the polymorphism under study, that polymorphisms may have several phenotypic effects associated with disease, the lack of suitable polymorphisms for studying modifiable exposures of interest, and canalization-the buffering of the effects of genetic variation during development. Nevertheless, Mendelian randomization provides new opportunities to test causality and demonstrates how investment in the human genome project may contribute to understanding and preventing the adverse effects on human health of modifiable exposures."}

abstract2 = {"role": "user", "content": """Background: Dysregulation of circulating metabolites may affect brain function and cognition, associated with alterations in the cerebral cortex architecture. However, the exact cause remains unclear. This study aimed to determine the causal effect of circulating metabolites on the cerebral cortex architecture.

Methods: This study utilized retrieved data from genome-wide association studies to investigate the relationship between blood metabolites and cortical architecture. A total of 1,091 metabolites and 309 metabolite ratios were used for exposure. The brain cortex surface area and cortex thickness were selected as the primary outcomes in this study. In this study, the inverse variance weighting method was used as the main analytical method, complemented by sensitivity analyses that were more robust to pleiotropy. Furthermore, metabolic pathway analysis was performed via MetaboAnalyst 6.0. Finally, reverse Mendelian randomization (MR) analysis was conducted to assess the potential for reverse causation.

Results: After correcting for the false discovery rate (FDR), we identified 37 metabolites and 9 metabolite ratios that showed significant causal associations with cortical structures. Among these, Oxalate was found to be most strongly associated with cortical surface area (β: 2387.532, 95% CI 756.570-4018.495, p = 0.037), while Tyrosine was most correlated with cortical thickness (β: -0.015, 95% CI -0.005 to -0.025, p = 0.025). Furthermore, pathway analysis based on metabolites identified six significant metabolic pathways associated with cortical structures and 13 significant metabolic pathways based on metabolite ratios.

Conclusion: The identified metabolites and relevant metabolic pathways reveal potential therapeutic pathways for reducing the risk of neurodegenerative diseases. These findings will help guide health policies and clinical practice in treating neurodegenerative diseases.

Keywords: Mendelian randomization; brain cortex surficial area; brain cortex thickness; genome-wide association studies; metabolites."""}

abstract3 = {"role": "user", "content": """Background: The association between air pollution, lung function, gastroesophageal reflux disease, and Non-alcoholic fatty liver disease (NAFLD) remains inconclusive. Previous studies were not convincing due to confounding factors and reverse causality. We aim to investigate the causal relationship between air pollution, lung function, gastroesophageal reflux disease, and NAFLD using Mendelian randomization analysis.

Methods: In this study, univariate Mendelian randomization analysis was conducted first. Subsequently, Steiger testing was performed to exclude the possibility of reverse association. Finally, significant risk factors identified from the univariate Mendelian analysis, as well as important factors affecting NAFLD from previous observational studies (type 2 diabetes and body mass index), were included in the multivariable Mendelian randomization analysis.

Results: The results of the univariable Mendelian randomization analysis showed a positive correlation between particulate matter 2.5, gastroesophageal reflux disease, and NAFLD. There was a negative correlation between forced expiratory volume in 1 s, forced vital capacity, and NAFLD. The multivariable Mendelian randomization analysis indicated a direct causal relationship between gastroesophageal reflux disease (OR = 1.537, p = 0.011), type 2 diabetes (OR = 1.261, p < 0.001), and NAFLD.

Conclusion: This Mendelian randomization study confirmed the causal relationships between air pollution, lung function, gastroesophageal reflux, and NAFLD. Furthermore, gastroesophageal reflux and type 2 diabetes were identified as independent risk factors for NAFLD, having a direct causal connection with the occurrence of NAFLD."""}

prompt = {"role": "user", "content": """What are the exposures and outcomes in this abstract? If there are multiple exposures or outcomes, provide them all. If there are no exposures or outcomes, provide an empty list. Also categorize the exposures and outcomes into the following groups: 
- molecular
- socioeconomic
- environmental
- behavioural
- anthropmetric
- clinical measures
- infectious disease
- neoplasm
- disease of the blood and blood-forming organs
- metabolic disease
- mental disorder
- disease of the nervous system
- disease of the eye and adnexa
- disease of the ear and mastoid process
- disease of the circulatory system
- disease of the digestive system
- disease of the skin and subcutaneous tissue
- disease of the musculoskeletal system and connective tissue
- disease of the genitourinary system
If an exposure or outcome does not fit into any of these groups, provide a new group name. Provide your answer in strict json format without markdown code blocks."""}


example_output = {"role": "assistant", "content": """
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
"""}

abstract4 = {"role": "user", "content": """Background: Epidemiological evidence links a close correlation between long-term exposure to air pollutants and autoimmune diseases, while the causality remained unknown.

Methods: Two-sample Mendelian randomization (TSMR) was used to investigate the role of PM10, PM2.5, NO2, and NOX (N = 423,796-456,380) in 15 autoimmune diseases (N = 14,890-314,995) using data from large European GWASs including UKB, FINNGEN, IMSGC, and IPSCSG. Multivariable Mendelian randomization (MVMR) was conducted to investigate the direct effect of each air pollutant and the mediating role of common factors, including body mass index (BMI), alcohol consumption, smoking status, and household income. Transcriptome-wide association studies (TWAS), two-step MR, and colocalization analyses were performed to explore underlying mechanisms between air pollution and autoimmune diseases.

Results: In TSMR, after correction of multiple testing, hypothyroidism was causally associated with higher exposure to NO2 [odds ratio (OR): 1.37, p = 9.08 × 10-4] and NOX [OR: 1.34, p = 2.86 × 10-3], ulcerative colitis (UC) was causally associated with higher exposure to NOX [OR: 2.24, p = 1.23 × 10-2] and PM2.5 [OR: 2.60, p = 5.96 × 10-3], rheumatoid arthritis was causally associated with higher exposure to NOX [OR: 1.72, p = 1.50 × 10-2], systemic lupus erythematosus was causally associated with higher exposure to NOX [OR: 4.92, p = 6.89 × 10-3], celiac disease was causally associated with lower exposure to NOX [OR: 0.14, p = 6.74 × 10-4] and PM2.5 [OR: 0.17, p = 3.18 × 10-3]. The risky effects of PM2.5 on UC remained significant in MVMR analyses after adjusting for other air pollutants. MVMR revealed several common mediators between air pollutants and autoimmune diseases. Transcriptional analysis identified specific gene transcripts and pathways interconnecting air pollutants and autoimmune diseases. Two-step MR revealed that POR, HSPA1B, and BRD2 might mediate from air pollutants to autoimmune diseases. POR pQTL (rs59882870, PPH4=1.00) strongly colocalized with autoimmune diseases.

Conclusion: This research underscores the necessity of rigorous air pollutant surveillance within public health studies to curb the prevalence of autoimmune diseases."""}


with open("data/pubmed.json") as f:
    a = json.load(f)

result = []
for i in range(len(a)):
    print(i)
    if 'ab' not in a[i].keys():
        continue
    try:        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                        abstract3,
                        prompt,
                        example_output,
                        {"role": "user", "content": bytes(a[i]['ab'], 'utf-8').decode('utf-8', 'ignore')},
                        prompt],
        )
        o = json.loads(response.choices[0].message.content)
        o['pmid'] = a[i]['pmid']
        result.append(o)
    except:
        continue
    if i % 100 == 0:
        with open("data/pubmed_abstracts.json", "w") as f:
            json.dump(result, f)

with open("data/pubmed_abstracts.json", "w") as f:
    json.dump(result, f)

with open("data/missing_pmids.txt") as f:
    m = [line.rstrip() for line in f]

a = [x for x in a if x['pmid'] in m]
len(a)

result = []
for i in range(len(a)):
    print(i)
    if 'ab' not in a[i].keys():
        continue
    try:        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                        abstract3,
                        prompt,
                        example_output,
                        {"role": "user", "content": bytes(a[i]['ab'], 'utf-8').decode('utf-8', 'ignore')},
                        prompt],
        )
        o = json.loads(response.choices[0].message.content)
        o['pmid'] = a[i]['pmid']
        result.append(o)
    except:
        continue
    if i % 100 == 0:
        with open("data/pubmed_abstracts2.json", "w") as f:
            json.dump(result, f)

with open("data/pubmed_abstracts2.json", "w") as f:
    json.dump(result, f)

with open("data/pubmed_abstracts.json") as f:
    r = json.load(f)

res = r + result
len(res)

with open("data/pubmed_abstracts.json", "w") as f:
    json.dump(res, f)

