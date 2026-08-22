import os
import re
import sqlite3
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
# SentenceTransformer will be loaded lazily
import numpy as np

# Lazy initialization placeholder for the embedding model
_EMBEDDING_MODEL = None  # will be loaded on first use

def _load_embedding_model():
    """Load the SentenceTransformer model lazily.
    This function initializes the global _EMBEDDING_MODEL the first time it is needed.
    Using a lightweight model to keep memory usage reasonable.
    """
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _EMBEDDING_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        except Exception as e:
            raise RuntimeError(f"Failed to load SentenceTransformer model: {e}")
 
# Global TF‑IDF vectorizer for keyword extraction – will be fitted lazily on all reference answers
_TFIDF_VECTORIZER = None

def _init_vectorizer():
    """Fit a TfidfVectorizer on the full set of reference answers.
    This is called the first time ``extract_keywords`` is used.
    """
    global _TFIDF_VECTORIZER
    if _TFIDF_VECTORIZER is not None:
        return
    # Resolve database path (same logic as other modules)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'database.db')
    if not os.path.exists(db_path):
        db_path = 'database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT answer_text FROM ReferenceAnswers")
    corpus = [row[0] for row in cur.fetchall()]
    conn.close()
    # Clean the corpus using the same routine as ``clean_text``
    cleaned_corpus = [clean_text(doc) for doc in corpus]
    vectorizer = TfidfVectorizer()
    vectorizer.fit(cleaned_corpus)
    _TFIDF_VECTORIZER = vectorizer

def get_embedding(text: str):
    """Return sentence embedding for given text using the lazily loaded model."""
    _load_embedding_model()
    if not text:
        return np.zeros(_EMBEDDING_MODEL.get_sentence_embedding_dimension())
    return _EMBEDDING_MODEL.encode([text])[0]

# Ensure NLTK stopwords are available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

STOP_WORDS = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """Normalize text: lowercase, strip punctuation, remove stopwords."""
    if not text:
        return ''
    text = text.lower()
    # Replace hyphens and dash characters with a space to keep words separate
    for dash in ['-', '‑', '–', '—']:
        text = text.replace(dash, ' ')
    # Remove punctuation (but keep spaces) after dash handling
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    cleaned_words = [w for w in words if w not in STOP_WORDS]
    return ' '.join(cleaned_words)

def extract_keywords(text: str, top_n: int = 6) -> list:
    """Return the top *top_n* TF‑IDF keywords from *text*.
    The global TF‑IDF vectorizer is lazily initialised on the full reference answer corpus.
    """
    if not text:
        return []
    _init_vectorizer()
    cleaned = clean_text(text)
    vec = _TFIDF_VECTORIZER.transform([cleaned])
    feature_names = _TFIDF_VECTORIZER.get_feature_names_out()
    scores = vec.toarray()[0]
    term_scores = [(feature_names[i], scores[i]) for i in range(len(scores)) if scores[i] > 0]
    term_scores.sort(key=lambda x: x[1], reverse=True)
    return [term for term, _ in term_scores[:top_n]]

def fit_vectorizer(corpus):
    """Fit a TfidfVectorizer on a list of reference answers (corpus)."""
    cleaned_corpus = [clean_text(doc) for doc in corpus]
    vectorizer = TfidfVectorizer()
    vectorizer.fit(cleaned_corpus)
    return vectorizer

def vectorize(text, vectorizer):
    """Transform *text* (or list of texts) into the TF‑IDF space of *vectorizer}."""
    if isinstance(text, str):
        cleaned_input = [clean_text(text)]
    else:
        cleaned_input = [clean_text(t) for t in text]
    return vectorizer.transform(cleaned_input)

if __name__ == '__main__':
    # Simple sanity check when run directly
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'database.db')
    if not os.path.exists(db_path):
        db_path = 'database.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT answer_text FROM ReferenceAnswers LIMIT 5;")
    rows = cur.fetchall()
    conn.close()
    sample_corpus = [r[0] for r in rows]
    vec = fit_vectorizer(sample_corpus)
    print('Vectorizer vocab size:', len(vec.vocabulary_))
    sample = "I handle conflict by communicating clearly and listening to all perspectives."
    print('Keywords:', extract_keywords(sample))
