from transformers import pipeline

# Load once
zsc = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Labels to detect risky intent
sensitive_labels = [
    "credentials", "confidential", "access keys",
    "internal tools", "secrets", "passwords", "vault access",
    "private tokens", "auth information", "environment variables"
]

def detect_contextual_leak(text, threshold=0.75):
    result = zsc(text, candidate_labels=sensitive_labels, multi_label=True)
    matches = []
    for label, score in zip(result["labels"], result["scores"]):
        if score >= threshold:
            matches.append((label, round(score, 2)))
    return matches
