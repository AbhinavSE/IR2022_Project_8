from functools import lru_cache
import re
import pandas as pd

# import nltk
# from nltk import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords, wordnet
import numpy as np
# STOPWORDS = set(stopwords.words('english'))
# lemmatizer = WordNetLemmatizer()


# def nltk_tag_to_wordnet_tag(nltk_tag):
#     if nltk_tag.startswith('J'):
#         return wordnet.ADJ
#     elif nltk_tag.startswith('V'):
#         return wordnet.VERB
#     elif nltk_tag.startswith('N'):
#         return wordnet.NOUN
#     elif nltk_tag.startswith('R'):
#         return wordnet.ADV
#     else:
#         return None


# def lemmatize(text):
#     nltk_tagged = nltk.pos_tag(nltk.word_tokenize(text))
#     wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
#     lemmatized_sentence = []
#     for word, tag in wordnet_tagged:
#         if tag is None:
#             # if there is no available tag, append the token as is
#             lemmatized_sentence.append(word)
#         else:
#             # else use the tag to lemmatize the token
#             lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
#     return " ".join(lemmatized_sentence)


def keep_text_only(text):
    if type(text) == str:
        return re.sub('[^a-zA-Z]+', ' ', text)
    return text


def remove_hashtags(text):
    if type(text) == str:
        return re.sub('#[\w]+', '', text)
    return text


def remove_links(text):
    if type(text) == str:
        return re.sub('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', text)
    return text


def remove_md_chars(text):
    if type(text) == str:
        return re.sub('[_*]+|(# )', '', text)
    return text


def remove_tags(text):
    if type(text) == str:
        text = re.sub('<[^>]+>', '', text)
    return text


def remove_mentions(text):
    if type(text) == str:
        return re.sub("@[A-Za-z0-9_]+", "", text)
    return text


# def remove_stopwords(text):
#     if type(text) == str:
#         return ' '.join([word for word in word_tokenize(text) if word not in STOPWORDS])
#     return text


def remove_nline(text):
    if type(text) == str:
        return re.sub('\s{2,}', ' ', text.replace('\n', ' '))
    return text


def remove_short_words(text):
    return re.sub(r'\b\w{1,2}\b', '', text)


def extract_domain(url):
    try:
        if type(url) == str:
            domain = url.split('//')[1].split('/')
            if len(domain) > 0:
                return domain[0]
        return url
    except:
        return url


@lru_cache(maxsize=None)
def get_compiled_regex(regex):
    return re.compile(regex, re.IGNORECASE)


@lru_cache(maxsize=None)
def compile_expression(expr: str):
    # get the variables
    vars = re.findall("'(.*?)'", expr)
    vars = [get_compiled_regex(v) for v in vars]

    # replace anything between quotes with brackets
    expr = re.sub("'(.*?)'", '{}', expr)
    return vars, expr


def checkRegexp(expr: str, text: str) -> bool:
    '''regex example: "('abc') && ('def') || ('ghi' && ('jkl' || 'mno'))"
    '''
    vars, expr = compile_expression(expr)
    # search individual expressions
    res = [v.search(text) is not None for v in vars]
    # eval for text
    return bool(eval(expr.format(*res)))


# def regex_search(regexp, text):
#     if regexp == '':
#         return ['']

#     def proc_reg(reg):
#         or_ = []
#         reg = re.findall(r'\((.*?)\)', reg) if '(' in reg else [reg]
#         for r1 in reg:
#             and_ = []
#             for r2 in r1.split('&'):
#                 case = r2.upper() == r2
#                 # replace space between 2 letters with '[ -]{0,1}'
#                 r2 = re.sub(r'([a-zA-Z]) ([a-zA-Z])', r'\1[ \-#]{0,1}\2', r2)
#                 # If only space before a word, replace r'\1[ -#]{0,1}\2' should start with nothing or space or - or #
#                 r2 = re.sub(r'^\s*([a-zA-Z])', r'(\\b|[ \.\-#]{1})\1', r2)
#                 r2 = re.sub(r'([a-zA-Z])\s*$', r'\1([ \.\-#]{1}|\\b)', r2)
#                 and_.append([r2, case])
#             or_.append(and_)
#         return or_

#     regexp = proc_reg(regexp)
#     found = []
#     for and_grp in regexp:
#         found = []
#         for reg, case in and_grp:
#             if case:
#                 f = re.findall(reg, text)
#                 if len(f) == 0:
#                     found = []
#                     break
#                 found.extend(f)
#             else:
#                 f = re.findall(reg, text, re.IGNORECASE)
#                 if len(f) == 0:
#                     found = []
#                     break
#                 found.extend(f)
#         if found:
#             break
#     return list(np.unique(found))
