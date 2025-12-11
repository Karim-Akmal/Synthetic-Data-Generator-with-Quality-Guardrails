# Synthetic vs Real Review Analysis for Jira Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

This project generates **synthetic Jira reviews** using Large Language Models (LLMs), compares them with real reviews, and evaluates **linguistic similarity**, **semantic alignment**, and **persona-based rating bias**.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Models & Providers](#models--providers)  
- [Personas Used](#personas-used)  
- [Real Review Collection](#real-review-collection)  
- [Analysis Methods](#analysis-methods)  
- [Technical Implementation](#technical-implementation)  
- [API Rate Limit Handling](#api-rate-limit-handling)  
- [Quality Report](#quality-report)  
- [CLI Usage](#cli-usage)  
- [Future Work](#future-work)  
- [License](#license)  

---

## Project Overview

- Generated **500 persona-based synthetic Jira reviews**.  
- Collected **50 real Jira reviews** for benchmarking.  
- Computed:  
  - **Vocabulary Overlap (%)**  
  - **Cosine Similarity (Embedding-Based)**  
- Used two LLM providers:  
  - HuggingFace — LLaMA-3.2 1B  
  - OpenAI — ChatGPT-4 Mini  
- Performed **bias detection** across personas.  
- Implemented batch processing, merging, and robust **rate-limit handling**.
- Added my API Keys internally so you need to use your own API KEYS
---

## Models & Providers

### Hugging Face
- **Model:** LLaMA-3.2 1B  
- Generated persona-based synthetic reviews.

### OpenAI
- **Model:** ChatGPT-4 Mini  
- Generated additional synthetic review batches.

---

## Personas Used

- Project Manager  
- Senior Developer  
- QA Tester  
- Scrum Master  
- UI/UX Developer  
- Software Engineer  

Each persona affects tone, sentiment, vocabulary, and feature focus.

---

## Real Review Collection

- **50 real Jira reviews** were manually gathered and cleaned.  
- Served as the **baseline** for similarity and bias evaluation.

---

## Analysis Methods

### Vocabulary Overlap (%)
- Measures how much of the real-review vocabulary appears in synthetic reviews.

### Cosine Similarity (Embedding-Based)
- Reviews converted to embeddings.  
- Semantic similarity measured via cosine distance.

### Persona-Based Bias Detection
- Checked for differences in:  
  - Average rating per persona  
  - Rating distribution  

---

## Technical Implementation

- Python-based pipeline  
- Persona-driven prompt templates  
- HuggingFace & OpenAI API integration  
- Batch generation with:  
  - Retry logic  
  - Delays  
  - Merging partial batches  
- Scripts for similarity & bias detection  

---

## API Rate Limit Handling

- Generate in small batches  
- Automatic retries  
- Time delays between requests  
- Merge all batches into unified datasets  

---

## Quality Report

### Vocabulary Overlap
**70.18%** similarity between synthetic and real review vocabulary.

### Rating Distribution (%)

| Rating | Real Reviews | Synthetic Reviews |
|--------|-------------|-----------------|
| 5.0    | 54.69       | 21.61           |
| 4.5    | 28.12       | -               |
| 4.0    | 9.38        | 20.33           |
| 3.0    | 3.12        | 21.43           |
| 2.5    | 1.56        | -               |
| 2.0    | 3.12        | 17.77           |
| 1.0    | -           | 18.86           |

### Role Distribution (%)

**Real Reviews**
{'Software Developer': 10.94, 'Data Warehouse Engineer': 1.56, 'IT Project Manager': 1.56,
'Senior Software Engineer': 1.56, 'Product Manager': 1.56, 'QA Manager': 7.81,
'Senior QA Engineer': 1.56, 'Project Manager': 12.5, 'Public Relations Specialist': 1.56,
'Software Engineer': 14.06, 'QA Tester': 10.94, 'Senior Project Manager': 1.56,
'Sr. Engineer': 1.56, 'Senior Software Developer': 1.56, 'Developer Associate': 1.56,
'Scrum Master': 10.94, 'UI/UX Developer': 10.94, 'Developer': 6.25}


**Synthetic Reviews**
{'Scrum Master': 18.13, 'Senior Developer': 17.22, 'Software Engineer': 15.75,
'UI/UX Developer': 15.57, 'Project Manager': 15.2, 'QA Tester': 18.13}


---

## CLI Usage

### Generate Synthetic Reviews
```bash
python reviews_generator.py --config yaml_file.yaml --output reviews15.json
```

### Convert JSONs to CSV
```bash
python from_json_to_csv.py
```

### Run Quality Evaluation
```bash
python quality_guardrail.py
```

---

## Future Work

- Add more personas  
- Compare sentiment distributions  
- Use larger LLMs (LLaMA-3 8B, GPT-4o)  
- Build dashboards for visualization  
- Extract topics or clusters from reviews  

---

## License  
### MIT License

---

This is a **fully GitHub-flavored README** with:  

- ✅ Badges  
- ✅ Proper heading levels  
- ✅ Tables and code blocks  
- ✅ Sections for CLI commands, results, and repo structure  

