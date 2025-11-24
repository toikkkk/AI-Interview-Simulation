import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def run_preprocessing(text: str) -> str:
    """Basic preprocessing: casefolding, cleaning, stopwords, stemming."""
    if not text:
        return ""

    # Lowercase
    text = text.lower().strip()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove extra whitespace
    text = " ".join(text.split())

    # Stemming (Sastrawi)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    text = stemmer.stem(text)

    return text
