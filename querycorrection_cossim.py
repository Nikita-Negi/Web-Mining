#importing essential libraries
import re
from collections import Counter

#reading bag of words
def words(text): return re.findall(r'\w+', text.lower())
WORDS = Counter(words(open('bagofwords.txt').read()))

#Probability of `word`
def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

#Most probable spelling correction for word.
def correction(word):
    return max(candidates(word), key=P)

#Generate possible spelling corrections for word.
def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

#The subset of `words` that appear in the dictionary of WORDS.
def known(words):
    return set(w for w in words if w in WORDS)

#All edits that are one edit away from `word`.
def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

#All edits that are two edits away from `word`
def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

#----------------------------------------------------------------------------------------------------------------------

#adding all the required packages and libraries to get most relevant query
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import nltk

#function to remove all the stop words from the text file and stemming it
def process (file):
    raw=open(file).read()
    tokens=word_tokenize(raw)
    words=[w.lower() for w in tokens]
    porter=nltk.PorterStemmer()
    stemmed_tokens=[porter.stem(t) for t in words]
    #removing stop words
    stop_words=set(stopwords.words('english'))
    filtered_tokens=[w for w in stemmed_tokens if not w in stop_words]
    #count words
    count= nltk.defaultdict(int)
    for word in filtered_tokens:
        count[word]+=1
    return count;

def cos_sim(a,b):
    #this function is responsible for finding cosine similarity of vector a and b using predefined functions in numpy
    dot_product=np.dot(a,b)
    norm_a=np.linalg.norm(a)
    norm_b=np.linalg.norm(b)
    return dot_product/(norm_a*norm_b)

def getSimilarity(dict1,dict2):
    all_words_list=[]
    for key in dict1:
        all_words_list.append(key)
    for key in dict2:
        all_words_list.append(key)
    #this function vectorizes both the file and the query for futher operations using numpy
    all_words_list_size=len(all_words_list)
    v1=np.zeros(all_words_list_size,dtype=np.int)
    v2 = np.zeros(all_words_list_size, dtype=np.int)
    i=0
    for (key) in all_words_list:
        v1[i]=dict1.get(key,0)
        v2[i]=dict2.get(key,0)
        i=i+1
    #it passes the 2 vectors as v1,v2 and receives cosine similarity which it returns
    return cos_sim(v1,v2);

#main function
if __name__=='__main__':
    #sim_file dictionary stores the similarity index and file number pair
    sim_file={}
    loc=0
    #dict0 stores the incorrect query form to be searched
    dict0 = process("C:/Users/DELL/PycharmProjects/calculator/venv/textfiles1/query.txt")
    qwords=dict0.keys()
    freq=dict0.values()
    print("Given query----------------------------------------------------------\n",qwords,"\n")
    correctedqwords=[]
    dict1={}
    #creating new dict1 storing corrected query
    for w in qwords:
        neww=correction(w)
        dict1[neww]= dict0[w]
        correctedqwords.append(neww)
    print("Corrected query------------------------------------------------------\n",correctedqwords,"\n")
    while loc<35:
        loc=loc+1
        path="C:/Users/DELL/PycharmProjects/calculator/venv/textfiles1/file"+str(loc)+".txt"
        #dict2 storing nth file to be compared for similarity
        dict2=process(path)
        #finding similarity with getSimilarity function and if any similarity is found, similarity:fileno. air is stored in sim_file
        if getSimilarity(dict1,dict2)>0:
            sim_file[getSimilarity(dict1,dict2)]=loc
    #sim_file is sorted in decreasing order of similarity
    keylist=sorted(sim_file,reverse=True)
    print("\nThe top results are as follows:\n")
    print("File Number\t:\tSimilarity")
    num=0
    for key in keylist:
        num=num + 1
        if num==11:
            exit()
        print ("\t%d\t\t:\t%f" % (sim_file[key],key))



