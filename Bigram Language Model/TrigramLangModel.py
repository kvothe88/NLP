######################################################### IMPORTS #########################################################
import nltk, re, codecs, math
from nltk.tokenize import TweetTokenizer
from collections import Counter



######################################################### FUNCTIONS #########################################################

def split_sequence(sequence, words):
    words = sequence.split()
    return words


def calculateUnigramProbLS(unigram, tokenized_corpus, V):
    return ((tokenized_corpus.count(unigram) + 1) / (len(tokenized_corpus) + V))


def calculateBigramProbLS(bigram, final_corpus, final_corpus_bigrams, V):
    return ((final_corpus_bigrams.count(bigram) + 1) / (final_corpus.count(bigram[0]) + V))

def calculateTrigramProbLS(trigram, final_corpus_trigrams, final_corpus_bigrams, V):
    return ((final_corpus_trigrams.count(trigram) + 1) / (final_corpus_bigrams.count((trigram[0], trigram[1])) + V))

def estimateNextWordProbability(sentence, unigrams, bigrams, bigrams_probs, unigrams_probs):
    results = {}
    Probability = 1
    if len(sentence) == 1:
        the_unigram = sentence[0]
        if the_unigram != "qwerty":
            i = 0;
            for unigram in unigrams:
                if unigram == the_unigram:
                    Probability = Probability * unigrams_probs[i]
                i = i + 1
        i = 0
        for bigram in bigrams:
            if not re.search("qwerty", str(bigram)):
                if bigram[0] == the_unigram:
                    # Probability = Probability_unigram * bigrams_probs[i]
                    print("P(", bigram, ") = ", Probability * bigrams_probs[i])
                    results[bigram[1]] = Probability * bigrams_probs[i]
            i = i + 1
        if len(results) > 0:
            print("Most possible next word: ", max(results, key=results.get))
            print("Possible next words and their probabilities to appear: ", results)
        else:
            print("Could not predict the next word for your given sentece...Does your word exists?")
    elif len(sentence) >= 2:
        last_bigram = bigramed_sentence[len(bigramed_sentence) - 1]
        print(last_bigram)
        last_unigram = last_bigram[1]
        i = 0
        for bigram in bigrams:
            if not re.search("qwerty", str(bigram)):
                if bigram[0] == last_unigram:
                    results[bigram[1]] = Probability * bigrams_probs[i]
            i = i + 1
        if len(results) > 0:
            print("Most possible next word: ", max(results, key=results.get))
            print("Possible next words and their probabilities to appear: ", results)
        else:
            print("Could not predict the next word for your given sentece...Does your word exists?")


# Markov Assumption
def estimateSentenceProbabilityLS(sentence, bigramed_sentence, unigrams, bigrams, bigrams_probs, unigrams_probs):
    Probability = 1
    first_bigram = bigramed_sentence[0]
    first_unigram = first_bigram[0]
    if first_unigram != "qwerty":
        i = 0;
        for unigram in unigrams:
            if unigram == first_unigram:
                Probability = Probability * unigrams_probs[i]
            i = i + 1
    for bigram in bigramed_sentence:
        if not re.search("qwerty", str(bigram)):
            i = 0
            for bb in bigrams:
                if bigram == bb:
                    Probability = Probability * bigrams_probs[i]
                i = i + 1
    print("P(", sentence, ") = ", Probability)

def countRareBigrams(bigrams):
    count = 0
    for bigram in bigrams:
        if re.search("qwerty", str(bigram)):
            count = count + 1
    return count


######################################################### MAIN SCRIPT #########################################################


# Load Corpus and compute total bigrams
print("Loading Corpus")
corpus = codecs.open(r'C:\Corpus\europarl-v7.fr-en.en', 'r', encoding='utf-8', errors='ignore').read()
print("Corpus loaded with success!!! Length: ", len(corpus))

# Initialize tokenization method
tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
print("Processing corpus..please wait!")
corpus = corpus.lower()
tokenized_corpus = tknzr.tokenize(corpus[0:100000])

# Replace words that appear less than 10 times in corpus
temp_counter = Counter(tokenized_corpus)
x = [word if temp_counter[word] >= 10 else 'qwerty' for word in tokenized_corpus]
x = ' '.join(x)

print("Training Trigram language Model...please wait...")
tokenized_corpus = tknzr.tokenize(x)
corpus_bigrams = list(nltk.ngrams(tokenized_corpus, 2))
# print (corpus_bigrams)

# Create Vocabulary
V = sorted(set(tokenized_corpus))

# Compute the probabilities for every Unigram!
unigrams_probs = [0.0] * len(V)

i = 0
for unigram in V:
    if unigram != "qwerty":
        unigrams_probs[i] = calculateUnigramProbLS(unigram, tokenized_corpus, len(V) - 1)
    i = i + 1

# f = open(r'output_files\UnigramsProbabilities.txt', 'w')
# i = 0;
# for unigram in V:
#     # print ("P(",V[i],") = ", unigrams_probs[i])
#     f.write("P(" + (V[i]) + ") = " + str(unigrams_probs[i]) + "\n")
#     i = i + 1
# f.close()

# Compute the probabilities for every Bigram!
final_corpus_bigrams = list(nltk.ngrams(tokenized_corpus, 2))
bigrams = sorted(set(final_corpus_bigrams))
bigrams_probs = [0.0] * len(bigrams)

i = 0
for bigram in bigrams:
    if not re.search("qwerty", str(bigram)):
        bigrams_probs[i] = calculateBigramProbLS(bigram, tokenized_corpus, final_corpus_bigrams, len(V) - 1)
    i = i + 1

# f = open(r'output_files\BigramsProbabilities.txt', 'w')
# i = 0
# for bigram in bigrams:
#     # print("P(", bigram, ") = ", bigrams_probs[i])
#     f.write("P(" + str(bigram) + ") = " + str(bigrams_probs[i]) + "\n")
#     i = i + 1

# Compute the probabilities for every Trigram!
final_corpus_trigrams = list(nltk.ngrams(tokenized_corpus, 3))
trigrams = sorted(set(final_corpus_trigrams))
trigrams_probs = [0.0] * len(trigrams)

#Compute a new V for Trigram model


i = 0
for trigram in trigrams:
    if not re.search("qwerty", str(trigram)):
        trigrams_probs[i] = calculateTrigramProbLS(trigram, final_corpus_trigrams, final_corpus_bigrams, len(bigrams) - countRareBigrams(bigrams))
    i = i + 1

f = open(r'output_files\TrigramsProbabilities.txt', 'w')
i = 0
for trigram in trigrams:
    f.write("P(" + str(trigram) + ") = " + str(trigrams_probs[i]) + "\n")
    i = i + 1



#Get user Input
sentence = input("Please insert a sentence to test the Trigram Model: \n")
sentence = sentence.lower()
print("Estimating Probability of given sentence and possible next words...")

word_sequence = []
seq1_words = split_sequence(sentence, word_sequence)



if len(seq1_words) == 1:
    estimateNextWordProbability(seq1_words, V, bigrams, bigrams_probs, unigrams_probs)
elif len(seq1_words) >= 2:
    bigramed_sentence = list(nltk.ngrams(seq1_words, 2))
    estimateSentenceProbabilityLS(sentence, bigramed_sentence, V, bigrams, bigrams_probs, unigrams_probs)
    estimateNextWordProbability(seq1_words, V, bigrams, bigrams_probs, unigrams_probs)
