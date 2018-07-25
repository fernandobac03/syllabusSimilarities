#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
""" Librería de algoritmos para NLP."""
__author__ = "Esteban Sebastián Espinoza Abril, Noemi Elizabeth Sari Uguña"
__version__ = "1.0"
__status__ = "Producción"
__copyright__ = "Escuela de Sistemas - Facultad de Ingeniería - Universidad de Cuenca"

#---------------------------- Importa las librerías ----------------------------
import string
import nltk
import numpy as np
from nltk.stem import *
from nltk import word_tokenize
from stop_words import get_stop_words
from nltk.tokenize import TweetTokenizer
from nltk.stem.snowball import SpanishStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.metrics import masi_distance
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

#------- Descarga de datos adicionales para las librerías si es necesario ------
#nltk.download('stopwords')
#nltk.download('punkt')

#---------------------- Definición de Variables Globales -----------------------
TWEET_TOKENIZER = TweetTokenizer()
SNOWBALL_STEMMER = SpanishStemmer()
LANCASTER_STEMMER = LancasterStemmer()
PORTER_STEMMER = PorterStemmer()
TEXTO_SIN_PUNTUACION = dict((ord(char), None) for char in string.punctuation)

#--------------------------- Definición de Funciones ---------------------------
def normalization(text):
    return text.lower().translate(TEXTO_SIN_PUNTUACION)

def tweet_tokenization(text):
    return TWEET_TOKENIZER.tokenize(text)

def word_tokenization(text):
    return word_tokenize(text)

def stopping(tokens):
    return sorted(set([token for token in tokens if token \
                  not in get_stop_words('spanish')]))

def snowball_stemming(stopwords):
    return set([SNOWBALL_STEMMER.stem(palabra) for palabra in stopwords])

def lancaster_stemming(stopwords):
    return [LANCASTER_STEMMER.stem(palabra) for palabra in stopwords]

def porter_stemming(stopwords):
    return [PORTER_STEMMER.stem(palabra) for palabra in stopwords]

def cosine_similarity(texto1, texto2):
    vectorizer = TfidfVectorizer(tokenizer=word_tokenization)
    tf_idf = vectorizer.fit_transform([texto1, texto2])
    return ((tf_idf * tf_idf.T).A)[0, 1]

def jaccard_similarity(vector_a, vector_b):
    vector_c = vector_a.intersection(vector_b)
    return float(len(vector_c)) / (len(vector_a) + len(vector_b) - len(vector_c))

def dices_similarity(vector_a, vector_b):
    vector_c = vector_a.intersection(vector_b)
    return float(2 * len(vector_c)) / (len(vector_a) + len(vector_b))

def overlap_similarity(vector_a, vector_b):
    vector_c = vector_a.intersection(vector_b)
    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)
    min_value = np.min((vector_a.min(), vector_b.min()))
    return float(len(vector_c)) / float(len(min_value))
