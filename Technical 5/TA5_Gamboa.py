"""TA5: Sentiment Analysis with TextBlob and a word-list challenge.
Andreu Liam C. Gamboa | AN43 | November 26, 2026
Setup: python -m pip install textblob nltk
       python -m nltk.downloader opinion_lexicon
Run activity:  python TA5_Gamboa.py
Run challenge: python TA5_Gamboa.py --challenge
"""
import re
import sys

from textblob import TextBlob


# VI. LABORATORY ACTIVITY: analyze 10 sentences, then summarize.
def classify(p):
    # Negative p<0, Neutral p=0, Positive p>0
    if p < 0:
        return "Negative"
    elif p == 0:
        return "Neutral"
    else:
        return "Positive"


def activity():
    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for i in range(1, 11):
        sentence = input(f"Enter sentence {i}/10: ")
        s = TextBlob(sentence)
        p = s.sentiment.polarity
        sentiment = classify(p)
        counts[sentiment] += 1
        print(f"{sentiment} (polarity: {p:.3f})")

    print("\nSummary of 10 sentences:")
    for sentiment, total in counts.items():
        print(f"{sentiment}: {total}")


# VII. CHALLENGE: count happy and sad words from public datasets.
# Dataset: Hu and Liu Opinion Lexicon (2004), distributed by NLTK.
# The positive list is the happy dataset; the negative list is the sad one.
def load_words():
    from nltk.corpus import opinion_lexicon
    return set(opinion_lexicon.positive()), set(opinion_lexicon.negative())


HAPPY_WORDS, SAD_WORDS = set(), set()


def words(sentence):
    return re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*", sentence.lower())


def number_happy(sentence):
    return sum(word in HAPPY_WORDS for word in words(sentence))


def number_sad(sentence):
    return sum(word in SAD_WORDS for word in words(sentence))


def challenge():
    global HAPPY_WORDS, SAD_WORDS
    HAPPY_WORDS, SAD_WORDS = load_words()
    sentence = input("Enter a sentence: ")
    happy = number_happy(sentence)
    sad = number_sad(sentence)

    if happy > sad:
        analysis = "Positive (happy tone)"
    elif sad > happy:
        analysis = "Negative (sad tone)"
    else:
        analysis = "Neutral"

    print(f"Happy words: {happy}")
    print(f"Sad words: {sad}")
    print(f"Analysis: {analysis}")


if __name__ == "__main__":
    if "--challenge" in sys.argv:
        challenge()
    else:
        activity()
