import re
from langdetect import detect, DetectorFactory
import nltk
from nltk.tokenize import sent_tokenize

DetectorFactory.seed = 0
nltk.download('punkt', quiet=True)

def clean_text(text: str) -> str:
    text = re.sub(r'\[.*?\]|\(.*?\)|Advertisement|Subscribe.*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_language(text: str) -> str:
    try:
        code = detect(text[:300])
        mapping = {
            'en':'en', 'gu':'gu', 'hi':'hi', 'ta':'ta', 'te':'te',
            'kn':'kn', 'ml':'ml', 'bn':'bn', 'mr':'mr', 'pa':'pa',
            'or':'or', 'as':'as', 'ur':'ur', 'ne':'ne'
        }
        return mapping.get(code, 'en')
    except:
        return 'en'

def chunk_text(text: str, max_chars: int = 1000) -> list:
    sentences = sent_tokenize(text)
    chunks = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) + 1 < max_chars:
            current += (" " + sent if current else sent)
        else:
            if current:
                chunks.append(current.strip())
            current = sent
    if current:
        chunks.append(current.strip())
    return chunks