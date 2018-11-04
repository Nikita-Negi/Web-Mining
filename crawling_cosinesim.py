#adding all the required packages and libraries
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
    # importing necessary libraries and packages needed to get urls
    from bs4 import BeautifulSoup
    import requests
    #defining root node
    url = "http://www.boredpanda.com"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    url_list = []
    #finding all the anchor elements (urls) in the root node
    for link in soup.find_all('a'):
        try:
            #if url is of the valid type then adding it to the url_list
            if (link.get('href')[0] == '/'):
                url_list.append(url + link.get('href'))
        except TypeError:
            print("\n")

    #x stores file number
    x = 0
    #file_url is a dictionary used to store file number and url pair
    file_url={}
    #visiting every page in the url_list and storing content as text file
    for page_link in url_list:
        try:
            x = x + 1
            page_response = requests.get(page_link, timeout=5)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            textContent = []
            content = ''
            #this loop stores various text lines as list elements in textContent
            for i in range(0, 20):
                paragraphs = page_content.find_all("p")[i].text
                textContent.append(paragraphs)
            #text in a document is stored as a string in content
            for w in textContent:
                content = content + w
            #a file is opened in a specific position and written to with the content of one page
            filename = "C:/Users/DELL/PycharmProjects/calculator/venv/textfiles/file" + str(x) + ".txt"
            saveFile = open(filename, "w")
            saveFile.write(content)
            saveFile.close()
            print(x, ". Visiting: ", page_link)
            print("File ", x, " saved as text successfully.\n")
            file_url[x]=page_link
        #defining some standard errors
        except IndexError:
            x = x - 1
        except UnicodeEncodeError:
            x = x - 1
        except UnicodeDecodeError:
            x = x - 1
        except RuntimeError:
            x = x - 1
    #sim_file dictionary stores the similarity index and file number pair
    sim_file={}
    loc=0
    #dict1 stores the query to be searched
    dict1 = process("C:/Users/DELL/PycharmProjects/calculator/venv/textfiles/query.txt")
    while loc<73:
        loc=loc+1
        path="C:/Users/DELL/PycharmProjects/calculator/venv/textfiles/file"+str(loc)+".txt"
        #dict2 storing nth file to be compared for similarity
        dict2=process(path)
        #finding similarity with getSimilarity function and if any similarity is found, similarity:fileno. air is stored in sim_file
        if getSimilarity(dict1,dict2)>0:
            sim_file[getSimilarity(dict1,dict2)]=loc
    #sim_file is sorted in decreasing order of similarity
    keylist=sorted(sim_file,reverse=True)
    print("The query from the user: times eyes regret 25 hilarious jobs")
    print("The top 10 results are as follows:")
    print("File Number\t:\tSimilarity\t:\tURL\n")
    num=0
    for key in keylist:
        num=num + 1
        if num==11:
            exit()
        print ("%d\t:\t%f\t:\t%s" % (sim_file[key],key,file_url[sim_file[key]]))



