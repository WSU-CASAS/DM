####################################################################################
# text_cleaning.py: Cleans text prior to natural language processing (NLP) feature extraction
# Different NLP algorithms need different cleaning prior to use
# Order of cleaning/pre-processing:
#   1. Pre-clean: 
#       - Remove non-ASCII characters
#       - Replace repeated whitespace punctuation characters with single character
#       - Break into sentences/phrases
#   2.a. Clean sentences:
#       - Convert to lower case
#       - Take care of oddities with punctuation
#       - Replace contractions with long form
#       - Remove tokens with no alphabetic characters
#   2.b. Clean words (doesn't affect cleaned sentences)
#       - Remove stop words
#       - Stem words

# Written by Gina Sprint, Gonzaga University.

# Copyright (c) 2021. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.
####################################################################################

import re

# uncomment if do not have stopwords dictionary downloaded on machine
# import nltk
# nltk.download("stopwords") 
from nltk.corpus import stopwords
from textblob import TextBlob

# from https://stackoverflow.com/questions/43018030/replace-apostrophe-short-words-in-python
contractions = {
    "ain't": "am not / are not",
    "aren't": "are not / am not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had / he would",
    "he'd've": "he would have",
    "he'll": "he shall / he will",
    "he'll've": "he shall have / he will have",
    "he's": "he has / he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has / how is",
    "i'd": "I had / I would",
    "i'd've": "I would have",
    "i'll": "I shall / I will",
    "i'll've": "I shall have / I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had / it would",
    "it'd've": "it would have",
    "it'll": "it shall / it will",
    "it'll've": "it shall have / it will have",
    "it's": "it has / it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had / she would",
    "she'd've": "she would have",
    "she'll": "she shall / she will",
    "she'll've": "she shall have / she will have",
    "she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as / so is",
    "that'd": "that would / that had",
    "that'd've": "that would have",
    "that's": "that has / that is",
    "there'd": "there had / there would",
    "there'd've": "there would have",
    "there's": "there has / there is",
    "they'd": "they had / they would",
    "they'd've": "they would have",
    "they'll": "they shall / they will",
    "they'll've": "they shall have / they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had / we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall / what will",
    "what'll've": "what shall have / what will have",
    "what're": "what are",
    "what's": "what has / what is",
    "what've": "what have",
    "when's": "when has / when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has / where is",
    "where've": "where have",
    "who'll": "who shall / who will",
    "who'll've": "who shall have / who will have",
    "who's": "who has / who is",
    "who've": "who have",
    "why's": "why has / why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had / you would",
    "you'd've": "you would have",
    "you'll": "you shall / you will",
    "you'll've": "you shall have / you will have",
    "you're": "you are",
    "you've": "you have"
}

####################################################################################
# Pre-cleaning
####################################################################################
def pre_clean_text_and_extract_sentences(resp):
    # break an entry into sentences. textblob is built on nltk's PunktSentenceTokenizer which does not consider \n as sentence separators
    # so we will have to do that
    sentences = []
    resp = str(resp)
    resp = resp.strip()
    if len(resp) > 0:
        resps = resp.split("\n")
        for r in resps:
            if r != "nan":
                # remove non-ascii characters (because some entries have Ø which is not a valid ASCII char so it is mapped to \x9D which when printed kills the python program, weird
                r = r.encode("ascii", errors="ignore").decode()
                # remove additional spaces and tabs from middle of string 
                r = re.sub(' +', ' ', r)
                r = re.sub('\t+', ' ', r)
                r = re.sub('\:+', ':', r)
                r = re.sub('\.+', '.', r)
                blob = TextBlob(r)
                sentences.extend([str(sentence) for sentence in blob.sentences])
    # remove any sentences that are only 1 character, that's not really a sentence!
    sentences = [sentence for sentence in sentences if len(sentence) > 1]
    # put a period at the end of a response if it doesn't have one because it was delimited by "\n"
    for i in range(len(sentences)):
        if sentences[i][-1] not in [".", "!", "?"]:
            sentences[i] += "."
    return sentences

####################################################################################
# Sentence cleaning
####################################################################################
def handle_special_punctuation(responses):
    for i in range(len(responses)):
        responses[i] = responses[i].replace("etc.", " et cetera ") # was running into issues with Textatistic later where etc. was at end of sentence but the . was part of the word etc but not a sentence delimiter, so let's just expand this abbreviation/punctuation
        responses[i] = responses[i].replace("&", " and ")
        responses[i] = responses[i].replace("@", " at ")
        responses[i] = responses[i].replace("-", " ")
        # get rid of double quotes and other punctuation
        responses[i] = responses[i].replace("\"", " ") 
        responses[i] = responses[i].replace("/", " ")
        responses[i] = responses[i].replace(":", " ")   
        responses[i] = responses[i].replace("“", "") 
        responses[i] = responses[i].replace("”", "")
        responses[i] = responses[i].replace("’", "")
        responses[i] = responses[i].replace("'", "")
        responses[i] = responses[i].replace("(", "")
        responses[i] = responses[i].replace(")", "")
        responses[i] = re.sub(' +', ' ', responses[i]) # in case we just added back in extra spaces

def clean_contractions_dict():
    # the dictionary above was found online
    # some long forms have two form separated by /
    # let's just use the first long form
    for short_form, long_form in contractions.items():
        if "/" in long_form:
            new_long_form = long_form.split("/")[0].strip()
            contractions[short_form] = new_long_form

def replace_contractions_with_long_form(responses):
    clean_contractions_dict()
    for i, response in enumerate(responses):
        new_response = []
        response = response.replace("’", "'") # handle the other kind of apostrophe
        words = response.split(" ")
        for word in words:
            word = word.strip().lower()
            if word in contractions:
                new_response.append(contractions[word].lower())
            elif len(word) > 0: # don't put in empty words that may result from double spaces
                new_response.append(word)
        responses[i] = " ".join(new_response)

def remove_tokens_with_numeric_chars(sentences):
    new_responses = []
    for i, sentence in enumerate(sentences):
        to_remove = []
        words = sentence.split(" ")
        for j, word in enumerate(words):
            # to find only alphabetical chars:"[a-zA-Z]+"
            numeric_chars = re.findall("[0-9]+", word) # findall() finds *all* the matches and returns them as a list of strings, with each string representing one match
            if len(numeric_chars) > 0: # at least one word with numeric chars
                # print(i, "word has numeric chars:", word, "\"", sentence, "\"")
                to_remove.append(word)
        keep_words = [word for word in words if word not in to_remove]
        new_response = " ".join(keep_words)
        if len(new_response) > 0:
            if new_response[-1] not in [".", "!", "?"]:
                new_response += "." # add period to end if we removed an ending punctuation
            new_responses.append(new_response)
    return new_responses

####################################################################################
# Word cleaning
####################################################################################
def remove_stop_words_and_stem(blob):
    # remove stop words
    stops = stopwords.words("english")
    no_stops = []
    for word in blob.words:
        if word not in stops:
            no_stops.append(word.stem())
    return no_stops

def clean_all_sentences_words(sentences):
    # convert to lower case
    sentences = [str(response).lower() for response in sentences]
    # replace contractions with long form
    replace_contractions_with_long_form(sentences)
    # take care of oddities with punctuation
    handle_special_punctuation(sentences)
    # remove tokens with no alphabetic characters
    print("*", sentences)
    sentences = remove_tokens_with_numeric_chars(sentences)
    # remove any sentences that are only 1 character, that's not really a sentence!
    sentences = [sentence for sentence in sentences if len(sentence) > 1]
    print("**", sentences)

    all_text_no_stop_words = []
    for sentence in sentences:
        blob = TextBlob(sentence)
        no_stop_words = remove_stop_words_and_stem(blob)
        all_text_no_stop_words.extend(no_stop_words)
    return sentences, all_text_no_stop_words