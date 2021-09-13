####################################################################################
# text_features.py: Computes natural language processing (NLP) features from text
# Text is loaded via a source CSV file and name of a column to process
# Then following occurs:
#   1. Cleaning to produce:
#       - Cleaned sentence text (cleaned punctuation, lower cased, stop words intacted, not stemmed, etc.)
#       - Cleaned non-stop word text (the cleaned sentence text, but with no punctuation, no stop words, stemmed, etc)
#   2. Features computed 
#       - Entry level (e.g. each row's text used by itself)
#       - Corpus level (e.g. all row's text used as a training corpus to extract each row's features)
#   3. Output written to CSV files
#       - "_sentences.csv": Cleaned sentence text, each row corresponding to cleaned sentence text for an input row
#           Note: if you are going to manually get LIWC features from the LIWC GUI, use this file
#       - "_features.csv": Features, with each row corresponding to features computed for an input row 
#   Note: empty strings will be written for values that could not be computed based on input data
# See file bottom for usage via command line args

# Written by Gina Sprint, Gonzaga University.

# Copyright (c) 2021. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.
####################################################################################

import sys
import os 
import itertools 

import numpy as np
import pandas as pd
from textblob import TextBlob
from spellchecker import SpellChecker
from textatistic import Textatistic
import spacy
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import gensim.downloader as api
from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

import text_cleaning
    
####################################################################################
# NLP features based on original, uncleaned text
####################################################################################
def compute_named_entity_recognition_stats(text, stats_ser):
    nlp = spacy.load("en")
    doc = nlp(text)
    # from https://stackoverflow.com/questions/59068687/spacy-most-efficient-way-to-sort-entities-by-label
    entities = {key: list(set(map(lambda x: str(x), g))) for key, g in itertools.groupby(sorted(doc.ents, key=lambda x: x.label_), lambda x: x.label_)}

    stats_ser["NumUniqueDATETIMEEntities"] = (len(entities["DATE"]) if "DATE" in entities else 0) + (len(entities["TIME"]) if "TIME" in entities else 0)
    stats_ser["NumUniqueGPELOCEntities"] = (len(entities["GPE"]) if "GPE" in entities else 0) + (len(entities["LOC"]) if "LOC" in entities else 0)
    stats_ser["NumUniqueORGEntities"] = (len(entities["ORG"]) if "ORG" in entities else 0)
    stats_ser["NumUniquePERSONEntities"] = (len(entities["PERSON"]) if "PERSON" in entities else 0)

def compute_original_text_stats(sentences, stats_ser):
    text = ""
    for resp in sentences:
        resp = str(resp)
        if len(resp) > 0:
            text += resp 
            if text[-1] != ".":
                text += "."
            text += " "
    compute_named_entity_recognition_stats(text, stats_ser)

####################################################################################
# Simple NLP features based on cleaned text
####################################################################################
def compute_pos_tag_stats(blob, pos="NN"):
    # list and description of tags: https://medium.com/@gianpaul.r/tokenization-and-parts-of-speech-pos-tagging-in-pythons-nltk-library-2d30f70af13b
    count = 0 
    for _, tag in blob.tags:
        if pos in tag:
            count += 1 
    return count

def compute_polarity_stats(all_sentences):
    # sentiment analysis
    all_polarity = []
    for sentence in all_sentences:
        all_polarity.append(TextBlob(sentence).sentiment.polarity)
    return np.mean(all_polarity), np.std(all_polarity)

def compute_subjectivity_stats(all_sentences):
    # sentiment analysis
    all_subjectivity = []
    for sentence in all_sentences:
        all_subjectivity.append(TextBlob(sentence).sentiment.subjectivity)
    return np.mean(all_subjectivity), np.std(all_subjectivity)

def count_unknown_words(blob):
    # following https://towardsdatascience.com/textblob-spelling-correction-46321fc7f8b8
    spell = SpellChecker()
    misspelled = spell.unknown(blob.words) # returns set
    ignore_words = ["dmn", "tv", "renton", "dmntm", "manualdmntm", "wsu", "cd", "pm", "am", "pc"] # add here as needed by domain
    for word in ignore_words:
        if word in misspelled:
            misspelled.remove(word)
    num_misspelled = len(misspelled)
    return num_misspelled

def compute_cleaned_text_stats(all_cleaned_sentences, all_non_stop_words, stats_ser):
    """
    all_cleaned_sentences (list of str): each str is a sentence that has been ran through pre_clean_text_and_extract_sentences()
    all_non_stop_words (list of str): each str is a single non-stop word from sentences
    """
    # print("all_cleaned_sentences:", all_cleaned_sentences)
    all_words_str = " ".join(all_cleaned_sentences)
    blob = TextBlob(all_words_str)
    num_words = len(blob.words)

    # trying to avoid absolute numbers and express everything in normalized values or percentages
    # stats_ser["NumSentences"] = len(all_cleaned_sentences)
    # stats_ser["NumUniqueSentences"] = len(set(all_cleaned_sentences))
    stats_ser["PercentUniqueSentences"] = len(set(all_cleaned_sentences)) / len(all_cleaned_sentences) * 100
    # stats_ser["NumWords"] = num_words
    readability = Textatistic(all_words_str)
    # print(readability.dict())
    stats_ser["DaleChallScore"] = readability.dalechall_score
    stats_ser["SMOGScore"] = readability.smog_score
    # stats_ser["NumWordsPerSentenceAvg"] = num_words / len(all_cleaned_sentences) # in LIWC
    stats_ser["NumCharsPerWordAvg"] = readability.char_count / readability.word_count
    stats_ser["NumSyllablesPerWordAvg"] = readability.sybl_count / readability.word_count
    # stats_ser["NumNounPhrases"] = len(blob.noun_phrases) # runs really slow
    stats_ser["PercentStopWords"] = len(all_non_stop_words) / num_words * 100
    stats_ser["PercentUnknownWords"] = count_unknown_words(blob) / num_words * 100
    # stats_ser["PercentNouns"] = compute_pos_tag_stats(blob, pos="NN") / num_words * 100 # in LIWC
    # stats_ser["PercentVerbs"] = compute_pos_tag_stats(blob, pos="VB") / num_words * 100 # in LIWC
    # stats_ser["PercentDeterminants"] = compute_pos_tag_stats(blob, pos="DT") / num_words * 100 # in LIWC
    stats_ser["PolarityAvg"], stats_ser["PolarityStd"] = compute_polarity_stats(all_cleaned_sentences)
    stats_ser["SubjectivityAvg"], stats_ser["SubjectivityStd"] = compute_subjectivity_stats(all_cleaned_sentences)

####################################################################################
# Text features based on a "training" corpus
####################################################################################
def compute_tfidf_features(text_name, train_text, test_text=None):
    # TF-IDF (term frequency-inverse document frequency)
    # following Tadesse et al. 2019 Detection of Depression-related Posts in Reddit Social Media Forum
    num_most_frequent = 100
    count_vect = CountVectorizer(ngram_range=(1,2)) # unigrams and bigrams
    train_counts = count_vect.fit_transform(train_text)
    sum_words = train_counts.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in count_vect.vocabulary_.items()]
    words_freq = sorted(words_freq, key = lambda x: x[1], reverse=True)
    most_frequent_words = [word_count_tuple[0] for word_count_tuple in words_freq[:num_most_frequent]]
    tfidf_transformer = TfidfVectorizer(ngram_range=(1,2))
    train_matrix = tfidf_transformer.fit_transform(train_text)
    tfidf_train_df = pd.DataFrame(train_matrix.toarray(), index=train_text.index, columns=tfidf_transformer.get_feature_names())
    most_frequent_train_df = tfidf_train_df[most_frequent_words]
    most_frequent_train_df.columns = [text_name + "_TFIDF" + col for col in most_frequent_train_df.columns]
    
    # if there is test text data to compute TF-IDF features for, process it now
    most_frequent_test_df = test_counts = None
    if test_text is not None:
        test_counts = count_vect.transform(test_text)
        test_matrix = tfidf_transformer.transform(test_text) # no data leakage
        tfidf_test_df = pd.DataFrame(test_matrix.toarray(), index=test_text.index, columns=tfidf_transformer.get_feature_names())
        most_frequent_test_df = tfidf_test_df[most_frequent_words]
        most_frequent_test_df.columns = [text_name + "_TFIDF" + col for col in most_frequent_test_df.columns]
    return most_frequent_train_df, train_counts, most_frequent_test_df, test_counts

def compute_lda_topic_features(text_name, train_text, train_counts, test_text=None, test_counts=None, num_topics=5):
    # topic modeling with LDA (Latent Dirichlet Allocation)
    # following Tadesse et al. 2019 Detection of Depression-related Posts in Reddit Social Media Forum
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    train_topics = lda.fit_transform(train_counts)
    train_topics_df = pd.DataFrame(train_topics, index=train_text.index, columns=[text_name + "_Topic#" + str(i) + "Probability" for i in range(num_topics)])
    # if there is test text data to compute LDA features for, process it now
    test_topics_df = None
    if test_text is not None and test_counts is not None:
        test_topics = lda.transform(test_counts)
        test_topics_df = pd.DataFrame(test_topics, index=test_text.index, columns=[text_name + "_Topic#" + str(i) + "Probability" for i in range(num_topics)])
    return train_topics_df, test_topics_df
        
def compute_embedding_features(text_name, text, sentences, word_vectors, embedding_vector_size):
    # word embeddings
    # following Gonzalez-Atienza et al. 2019 "An Automatic System for Dementia Detection using Acoustic and Linguistic Features"
    # need to take average of word vectors in a document to get a "document vector" (e.g. document is all text from one instance)
    text_embeddings = {}
    for i in range(len(text)):
        ind = text.index[i]
        sentence = sentences[i]
        text_embedding = np.zeros(embedding_vector_size)
        count = 0
        for j in range(len(sentence)): # go through each word
            if sentence[j] in word_vectors.key_to_index:
                text_embedding += word_vectors[sentence[j]] # type is numpy.ndarray
                count += 1
        if count > 0: # otherwise embeddings will be all 0s
            text_embedding /= count # take average
        text_embeddings[ind] = text_embedding
    df = pd.DataFrame(text_embeddings).T
    df.columns = [text_name + "_Embedding#" + str(col) for col in df.columns] # so they have unique names across content and taskDescription
    means = df.mean(axis=1) # take average across embedding_vector_size values
    stds = df.std(axis=1) # take std across embedding_vector_size values
    df[text_name + "_EmbeddingMean"] = means
    df[text_name + "_EmbeddingStd"] = stds
    return df

def run_embedding_workflow(text_name, train_text, test_text, word_vectors, embedding_vector_size=50):
    # following https://www.kaggle.com/pierremegret/gensim-word2vec-tutorial
    # use bigrams... As Phrases() takes a list of list of words as input:
    train_sentences = [temp.split(" ") for temp in train_text]
    train_bigram  = Phraser(Phrases(train_sentences, min_count=30))
    train_sentences_bigrams = train_bigram[train_sentences]

    if word_vectors is None: # for training the model from scratch instead of using pre-trained one. need to have large corpus to do this
        w2v_model = Word2Vec(min_count=20,
                    window=2,
                    vector_size=embedding_vector_size,
                    sample=6e-5, 
                    alpha=0.03, 
                    min_alpha=0.0007, 
                    negative=20, 
                    workers=1) # to help ensure reproducibility of results: https://stackoverflow.com/questions/34831551/ensure-the-gensim-generate-the-same-word2vec-model-for-different-runs-on-the-sam
        w2v_model.build_vocab(train_sentences_bigrams)
        w2v_model.train(train_sentences_bigrams, total_examples=w2v_model.corpus_count, epochs=30)
        word_vectors = w2v_model.wv

    train_embedding_df = compute_embedding_features(text_name, train_text, train_sentences_bigrams, word_vectors, embedding_vector_size)
    # if there is test text data to compute embeddings for, process it now
    test_embedding_df = None
    if test_text is not None:
        test_sentences = [temp.split(" ") for temp in test_text]
        test_bigram = Phraser(Phrases(test_sentences, min_count=30))
        test_sentences_bigrams = test_bigram[test_sentences]
        test_embedding_df = compute_embedding_features(text_name, test_text, test_sentences_bigrams, word_vectors, embedding_vector_size)
    
    return train_embedding_df, test_embedding_df

####################################################################################
# Driver program helper functions
####################################################################################
def compute_corpus_level_features(non_stop_text_ser, features_df):
    most_frequent_train_df, train_counts, _, _ = compute_tfidf_features(text_ser.name, non_stop_text_ser)
    features_df = features_df.join(most_frequent_train_df)

    train_topics_df, _ = compute_lda_topic_features(text_ser.name, non_stop_text_ser, train_counts)
    features_df = features_df.join(train_topics_df)

    path = api.load("glove-wiki-gigaword-50", return_path=True) # can choose a different pre-trained Word2Vec model: https://github.com/RaRe-Technologies/gensim-data#models
    word_vectors = KeyedVectors.load_word2vec_format(path) # slow to load, so load once before call to run workflow() which may be called multiple times
    embedding_vector_size = 50 # because gigaword-50 corpus
    train_embedding_df, _ = run_embedding_workflow(text_ser.name, non_stop_text_ser, None, word_vectors, embedding_vector_size)
    features_df = features_df.join(train_embedding_df)

    return features_df

def extract_text_features(text_ser):
    cleaned_sentence_text_dict = {} # for LIWC features to be manually computed using LIWC GUI program
    text_stats_sers_dict = {} # for the features we extract here
    non_stop_text_dict = {} # for the corpus-level features
    for row_id in text_ser.index:
        print("Processing row ID:", row_id)
        text = text_ser[row_id]
        sentences = text_cleaning.pre_clean_text_and_extract_sentences(text)
        text_stats_ser = pd.Series(dtype=float, name=row_id)
        if len(sentences) > 0:
            compute_original_text_stats(sentences, text_stats_ser)
            all_cleaned_sentences, all_non_stop_words = text_cleaning.clean_all_sentences_words(sentences)
            if len(all_cleaned_sentences) > 0:
                compute_cleaned_text_stats(all_cleaned_sentences, all_non_stop_words, text_stats_ser)
                cleaned_sentence_text_dict[row_id] = " ".join(all_cleaned_sentences)
                non_stop_text = " ".join(all_non_stop_words)
                non_stop_text_dict[row_id] = non_stop_text # build the corpus of non-stop text
        text_stats_sers_dict[row_id] = text_stats_ser
    cleaned_sentence_text_ser = pd.Series(cleaned_sentence_text_dict)
    features_df = pd.DataFrame(text_stats_sers_dict).T # build dataframe from dict of series
    non_stop_text_ser = pd.Series(non_stop_text_dict) 

    # corpus-level features (TF-IDF, embeddings, and LDA) over non_stop_text
    features_df = compute_corpus_level_features(non_stop_text_ser, features_df)

    return cleaned_sentence_text_ser, features_df

def get_cmd_line_args():
    if len(sys.argv) != 3:
        print("USAGE: python nlp_features.py input_filename.csv text_column_name_str")
        print("EXAMPLE: python nlp_features.py test_input_file.csv text_col")
        exit()
    
    filename, text_col_name = sys.argv[1], sys.argv[2]
    if not os.path.exists(filename):
        print(filename, "path does not exist")
        exit()

    df = pd.read_csv(filename, index_col=0)
    if text_col_name not in df.columns:
        print(text_col_name, "is not a valid column name in", filename)
        exit()

    text_ser = df[text_col_name]
    if text_ser.dtype != object:
        print(text_col_name, "does not contain string text data")
        exit()
    return filename, text_ser

if __name__ == "__main__":
    # set environment variable PYTHONHASHSEED=0 to ensure reproducibility with built Word2Vec models: https://stackoverflow.com/questions/34831551/ensure-the-gensim-generate-the-same-word2vec-model-for-different-runs-on-the-sam
    # command line args:
    #   input_filename.csv (this is a CSV file with where each row is an instance/subject and each column is a datapoint of some sort)
    #       first column should be unique index/key for rows
    #   text_column_name_str (this is the name of one of the columns that contains only text data)
    filename, text_ser = get_cmd_line_args()

    cleaned_sentence_text_ser, features_df = extract_text_features(text_ser)
    # write cleaned sentences and features to file
    no_extension = os.path.splitext(filename)[0] # everything before the last dot
    cleaned_sentence_text_ser.to_csv(no_extension + "_" + text_ser.name + "_sentences.csv", header=False) # use this for input to LIWC
    features_df.to_csv(no_extension + "_" + text_ser.name + "_features.csv") # then combine LIWC features with this file to get total NLP features