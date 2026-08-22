import sys, os
sys.path.insert(0, os.getcwd())
from ai.nlp_processor import clean_text, _init_vectorizer
import ai.nlp_processor as npmod

ref_text = "Denormalization duplicates data to avoid joins, improving read performance but risking consistency issues. It's a trade-off between speed and storage."

cleaned = clean_text(ref_text)
print('CLEANED TEXT:', repr(cleaned))

_init_vectorizer()
vec = npmod._TFIDF_VECTORIZER.transform([cleaned])
feature_names = npmod._TFIDF_VECTORIZER.get_feature_names_out()
scores = vec.toarray()[0]
nonzero = [(feature_names[i], scores[i]) for i in range(len(scores)) if scores[i] > 0]
nonzero.sort(key=lambda x: x[1], reverse=True)
print('ALL NONZERO TERMS FOR THIS DOCUMENT:', nonzero)
