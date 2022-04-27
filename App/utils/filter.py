import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import Counter
import string
import warnings

warnings.filterwarnings("ignore")
nltk.download("punkt")
nltk.download("stopwords")


def remove_emoji(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U0001F1F2-\U0001F1F4"
        "\U0001F1E6-\U0001F1FF"
        "\U0001F600-\U0001F64F"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U0001F1F2"
        "\U0001F1F4"
        "\U0001F620"
        "\u200d"
        "\u2640-\u2642"
        "]+",
        flags=re.UNICODE,
    )
    text = emoji_pattern.sub(r"", text)
    return text


def stemming(text):
    x = text.split(" ")
    ps = PorterStemmer()
    return " ".join([ps.stem(i) for i in x])


def remove_links(text):
    rem_url = re.sub("http\S+", "", text)
    rem_email = re.sub(
        "\S*[a-zA-Z0-9._\-]+@[a-zA-Z0-9._\-]+.[a-zA-Z0-9_\-]+s*", "", rem_url
    )
    rem_num = re.sub("[0-9]+", "", rem_email)
    return rem_num


def remove_art_connector(text):
    article = [
        "CAN",
        "IS",
        "HIS",
        "MORE",
        "WHO",
        "ABOUT",
        "THEIR",
        "OUR",
        "HAS",
        "WHO",
        "GET",
        "THEM",
        "WHAT",
        "OUT",
        "FROM",
        "HAVE",
        "HERE",
        "WE",
        "ALL",
        "THERE",
        "TO",
        "ALSO",
        "AND",
        "AS",
        "BUT",
        "YET",
        "YOU",
        "THE",
        "WAS",
        "FOR",
        "ARE",
        "THEY",
        "THIS",
        "THAT",
        "WERE",
        "WITH",
        "YOUR",
        "JUST",
        "WILL",
        "NOT",
    ]
    ans = []
    for word in text:
        if word.strip() not in article:
            ans.append(word)
    return ans


def remove_punc(tokens):
    table = string.punctuation
    ptokens = []
    for w in tokens:
        if w not in table:
            ptokens.append(w)
    ptokens = [s for s in ptokens if s]
    ptokens = [re.sub(r"[\n\t]+", " ", s) for s in ptokens]

    return ptokens


def stopword(text):
    x = text.split(" ")
    for i in range(len(x)):
        if x[i] in stopwords.words("english"):
            x[i] = ""
    x = remove_punc(x)
    x = remove_art_connector(x)
    return " ".join(x)


# Filter the parsed text, by, converting them into lowercase, removing any tags, extra spaces.
vocab = set()


def filter(item, b):
    global vocab
    if type(item) == str:
        item = item.lower()
        item = re.sub("[#@]\w+\s*", "", item)
        item = re.sub(r"\\N", "", item)
        item = remove_emoji(item)
        item = remove_links(item)
        item = stopword(item)
        item = stemming(item)
        item = word_tokenize(item)
        item = Counter(item)
        if b:
            for x in item.keys():
                vocab.add(x)
    return item
