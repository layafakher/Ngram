import random
import pandas as pd
import re

#this method tokenize a text and return a list of words
def tokenize(text):
    words  = []
    for word in text.split():
        words.append(word.strip())
    return words

#this method calculate ngarms of a text and return a dictionary of words
def calculateNgarm(text, n):
    ngram_dictionary = {}
    words = tokenize(text)
    for i in range(len(words) - n + 1):
        ngram = " ".join(words[i:i + n])
        ngram_dictionary[ngram] = ngram_dictionary.get(ngram, 0) + 1
    return ngram_dictionary


# read corpus
with open('corpus.txt', 'r') as f:
    text = f.read()


# text preprocessing
def text_preprocess(text):
    text = str(text).lower()  # convert to lower case
    text = text.replace('{html}', "")  # remove html tag
    rem_url = re.sub(r'http\S+', '', text)  # remove links
    rem_num = re.sub('[0-9]+', '', rem_url)  # remove numbers
    punctuation = '''!()-[]{};:'",.?@#$%^&*_~'''  #remove punctuations
    out=  ""
    for ch in rem_num:
        if ch not in punctuation:
            out = out + ch
    return out

text = text_preprocess(text)


# calculate ngrams and bigrams
unigram_freq = calculateNgarm(text, 1)
bigram_freq = calculateNgarm(text, 2)

# calculate number of bigrams and unigrams
print("{:15s} {:15s} {:15s}".format("Unigram", "Count", "Frequency"))
for u, c in unigram_freq.items():
    print("{:15s} {:<15d} {:<15.5f}".format(u, c, c / len(text.split())))

print("\n{:15s} {:15s}".format("Bigram", "Count"))
for b, c in bigram_freq.items():
    print("{:15s} {:<15d} ".format(b, c))


# print bigram Table
# **************************************
bigram_tuples_list = []
for key in bigram_freq:
    bigram_tuples_list.append(tuple(key.split()))

words = sorted(list(set([item for t in bigram_tuples_list for item in t])))
df = pd.DataFrame(0, columns=words, index=words)
for i in bigram_tuples_list:
    df.at[i[0], i[1]] += 1
print(df.loc['a':'responsibility','<s>':'improve'])
# **************************************

# Generate a random string less than 5 words long
#removing <s>,</s> from wordslist to prevent seeing <s>,</s> in the middle of random text
#they should be only at at the beginning and at the end 
rand_length = random.randint(2, 5)
words = set(tokenize(text)).difference(["<s>","</s>"])



rand_string_list = ["<s>"] + random.choices(list(words),k=rand_length) + ["</s>"]

rand_string = " ".join(rand_string_list)
print("\nRandom string: {}".format(rand_string))


# calculet bigram of random text
random_text_bigram = calculateNgarm(rand_string,2)
random_text_bigram_tuples = []
for key in random_text_bigram:
    random_text_bigram_tuples.append(tuple(key.split()))

# calculate probability of generated random text using bigram 
#We should use add-one smoothing to prevent the probability to become 0

prob = 1
for pair in random_text_bigram_tuples:
    prev_count = unigram_freq.get(pair[0], 0)  #c(wn-1)
    bigram_count = bigram_freq.get(" ".join(pair), 0) #c(wn-1wn)
    if prev_count > 0:
        p = (bigram_count) / (prev_count)
        print("p(",pair[1],"|",pair[0],") = ",(bigram_count) / (prev_count))
        prob *= p
        

print("Probability of occurrence: {:.10f}".format(prob))


