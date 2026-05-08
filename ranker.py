import nltk

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
import pdfplumber
import re
import numpy as np
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


# Extract text from PDF
def extract_text_from_pdf(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text


# Preprocess text
def preprocess_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z\s]', '', text)

    tokens = word_tokenize(text)

    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    return tokens


# Convert tokens into vectors
def get_document_vector(tokens, model):

    vectors = []

    for word in tokens:

        if word in model.wv:

            vectors.append(model.wv[word])

    return np.mean(vectors, axis=0)


# MAIN RANKING FUNCTION
def rank_resume(resume_text, job_description):

    processed_resume = preprocess_text(
        resume_text
    )

    processed_jd = preprocess_text(
        job_description
    )

    training_data = [
        processed_resume,
        processed_jd
    ]

    model = Word2Vec(
        training_data,
        vector_size=100,
        window=5,
        min_count=1,
        workers=4
    )

    resume_vector = get_document_vector(
        processed_resume,
        model
    )

    jd_vector = get_document_vector(
        processed_jd,
        model
    )

    similarity = cosine_similarity(
        [resume_vector],
        [jd_vector]
    )

    score = similarity[0][0] * 100

    return round(score, 2)