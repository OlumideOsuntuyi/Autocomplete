from transformers import pipeline

ner_model = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def extract_entities(text):
    return {e['entity_group']: e['word'] for e in ner_model(text)}
