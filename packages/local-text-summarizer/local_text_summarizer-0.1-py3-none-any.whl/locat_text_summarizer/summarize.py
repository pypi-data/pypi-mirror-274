import re
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Check if 'punkt' package is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    print('punkt package is downloaded')
except LookupError:
    # Download 'punkt' package
    nltk.download('punkt')
    print('punkt package is downloaded')

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\W', ' ', text)  # Remove all non-word characters
    return text

def get_word_frequencies(text):
    words = word_tokenize(text.lower())
    return Counter(words)

def score_sentences(sentences, word_freq):
    sentence_scores = {}
    for sentence in sentences:
        sentence_length = len(word_tokenize(sentence))
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]
    return sentence_scores

def condense_story(text, ratio=0.5):
    sentences = sent_tokenize(text)
    if len(sentences) <= 1:
        return text
    cleaned_text = clean_text(text)
    word_freq = get_word_frequencies(cleaned_text)
    sentence_scores = score_sentences(sentences, word_freq)
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary_length = max(1, int(len(sentences) * ratio))
    summary_sentences = sorted_sentences[:summary_length]
    condensed_summary = ' '.join(summary_sentences)
    print(condensed_summary)
    return condensed_summary

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Summarize text.')
    parser.add_argument('text', type=str, help='Text to summarize')
    parser.add_argument('--ratio', type=float, default=0.5, help='Summary ratio')
    args = parser.parse_args()
    print(condense_story(args.text, args.ratio))

if __name__ == '__main__':
    main()
