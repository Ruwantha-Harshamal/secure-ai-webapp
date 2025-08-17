import re
import spacy
from transformers import pipeline
from presidio_analyzer import AnalyzerEngine

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load zero-shot classification model
zsc = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Initialize Presidio Analyzer
analyzer = AnalyzerEngine()

# Load sensitive labels for ZSC
sensitive_labels = [
    "personal information", "private data", "financial information", 
    "medical information", "confidential data", "passwords", "internal data"
]

# Load keywords
def load_keywords(file_path="keywords.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return []
    
custom_keywords = load_keywords()

# Enhanced Regex patterns
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
api_key_pattern = re.compile(r'sk-[a-zA-Z0-9]{10,}')
# Additional patterns for better detection
phone_pattern = re.compile(r'\b(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b')
ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
credit_card_pattern = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')
github_token_pattern = re.compile(r'ghp_[a-zA-Z0-9]{36}')
aws_key_pattern = re.compile(r'AKIA[0-9A-Z]{16}')

def detect_regex(text):
    matches = []
    matches += [(m.group(), "EMAIL") for m in email_pattern.finditer(text)]
    matches += [(m.group(), "IP_ADDRESS") for m in ip_pattern.finditer(text)]
    matches += [(m.group(), "API_KEY") for m in api_key_pattern.finditer(text)]
    return matches

def detect_spacy_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def detect_presidio_pii(text):
    results = analyzer.analyze(text=text, entities=[], language='en')
    return [(text[result.start:result.end], result.entity_type) for result in results]

def detect_contextual_leak(text):
    output = zsc(text, candidate_labels=sensitive_labels, multi_label=True)
    detected = []
    for label, score in zip(output["labels"], output["scores"]):
        if score >= 0.7:  # Threshold
            detected.append(label)
    return detected

def mask_entity(entity_type):
    entity_masking = {
        "PERSON": "[PERSON]",
        "GPE": "[LOCATION]",
        "LOC": "[LOCATION]",
        "ORG": "[ORGANIZATION]",
        "MONEY": "[MONEY]",
        "EMAIL": "[EMAIL]",
        "IP_ADDRESS": "[IP_ADDRESS]",
        "API_KEY": "[API_KEY]",
        "PHONE_NUMBER": "[PHONE_NUMBER]",
        "ADDRESS": "[ADDRESS]",
        "CREDIT_CARD": "[CREDIT_CARD]",
        "IBAN_CODE": "[BANK_ACCOUNT]",
        "US_SSN": "[SSN]"
    }
    return entity_masking.get(entity_type, "[MASKED]")

def run_secure_prompt_filter(text):
    masked_text = text

    # Step 1: Regex detection
    for match, label in detect_regex(text):
        masked_text = masked_text.replace(match, mask_entity(label))

    # Step 2: spaCy NER
    for ent_text, ent_label in detect_spacy_entities(text):
        masked_text = masked_text.replace(ent_text, mask_entity(ent_label))

    # Step 3: Presidio PII detection
    for pii_text, pii_type in detect_presidio_pii(text):
        masked_text = masked_text.replace(pii_text, mask_entity(pii_type))

    # Step 4: Contextual classification
    context_labels = detect_contextual_leak(text)
    for label in context_labels:
        masked_text = masked_text.replace(label, "[MASKED_CONTEXT]")

    # Step 5: Keyword matching
    for keyword in custom_keywords:
        if keyword.lower() in masked_text.lower():
            masked_text = masked_text.replace(keyword, "[KEYWORD]")

    return masked_text
