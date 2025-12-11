import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer, util
from collections import Counter
from datetime import datetime


#Load Data
real_reviews_path = "Jira_Reviews_50.csv"
synthetic_reviews_path = "merged_reviews.csv"

real_df = pd.read_csv(real_reviews_path)
synthetic_df = pd.read_csv(synthetic_reviews_path)

# For simplicity, assume column: "Review Text" and "Persona" exist
real_texts = real_df["Review Text"].tolist()
synthetic_texts = synthetic_df["Review Text"].tolist()


# Diversity Metrics
# Vocabulary overlap (unique words)
vectorizer = CountVectorizer().fit(real_texts + synthetic_texts)
real_vocab = set(vectorizer.transform(real_texts).nonzero()[1])
synthetic_vocab = set(vectorizer.transform(synthetic_texts).nonzero()[1])
vocab_overlap_percent = len(real_vocab & synthetic_vocab) / len(real_vocab) * 100

print(f"Vocabulary overlap: {vocab_overlap_percent:.2f}%")

# Semantic similarity using embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
real_embeddings = model.encode(real_texts, convert_to_tensor=True)
synthetic_embeddings = model.encode(synthetic_texts, convert_to_tensor=True)

similarity_matrix = util.cos_sim(synthetic_embeddings, real_embeddings)



# Bias Check
# Sentiment / rating distribution check
real_rating_counts = Counter(real_df["Rating"])
synthetic_rating_counts = Counter(synthetic_df["Rating"])

# Role coverage check
real_roles = Counter(real_df["Persona"])
synthetic_roles = Counter(synthetic_df["Persona"])

# Sentiment / rating distribution comparison
def rating_distribution(df):
    counts = Counter(df["Rating"])
    total = sum(counts.values())
    return {k: round(v/total*100,2) for k,v in counts.items()}

real_rating_dist = rating_distribution(real_df)
synthetic_rating_dist = rating_distribution(synthetic_df)

# Role coverage comparison
def role_distribution(df):
    counts = Counter(df["Persona"])
    total = sum(counts.values())
    return {k: round(v/total*100,2) for k,v in counts.items()}

real_role_dist = role_distribution(real_df)
synthetic_role_dist = role_distribution(synthetic_df)


# Generate Markdown Report

report_lines = [
    f"# Synthetic Reviews Quality Report - {datetime.today().strftime('%Y-%m-%d')}\n",
    f"**Vocabulary Overlap with Real Reviews:** {vocab_overlap_percent:.2f}%",
    "## Rating Distribution (%)",
    f"Real Reviews: {real_rating_dist}",
    f"Synthetic Reviews: {synthetic_rating_dist}\n",
    "## Role Distribution (%)",
    f"Real Reviews: {real_role_dist}",
    f"Synthetic Reviews: {synthetic_role_dist}\n",
]

report_md = "\n".join(report_lines)
with open("synthetic_reviews_quality_report.md", "w") as f:
    f.write(report_md)

print("✅ Markdown quality report generated: synthetic_reviews_quality_report.md")
