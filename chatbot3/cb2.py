import nltk
nltk.download('punkt')
nltk.download('wordnet')
import io
import numpy as py
import random
import string
import warnings

warnings.filterwarnings('ignore')
f = open('text.txt','r',errors='ignore')
raw = f.read()
raw = raw.lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

sentToken = sent_tokens[:2]
wordToken = word_tokens[:2]

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)

def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello","hi","greetings","sup","what's up","hey")
GREETING_RESPONSES = ["hi","hey","nods","hi there","hello","I am glad! you are talking to me"]

def greeting(sentence):
  for word in sentence.split():
    if word.lower() in GREETING_INPUTS:
      return random.choice(GREETING_RESPONSES)

# VECTORIZER
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
  chatbot_response=''
  sent_tokens.append(user_response)
  TfidfVec = TfidfVectorizer(tokenizer=LemNormalize,stop_words='english')
  tfidf = TfidfVec.fit_transform(sent_tokens)
  vals = cosine_similarity(tfidf[-1],tfidf)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  req_tfidf = flat[-2]
  if (req_tfidf == 0):
    chatbot_response = chatbot_response + "Im sorry! I don't understand you"
    return chatbot_response
  else:
    chatbot_response = chatbot_response + sent_tokens[idx]
    return chatbot_response

###############################################################
import pandas as pd
df = pd.read_csv('farmacia.csv')

#cant = df.loc[df['medicamento'==y,'cantidad']]



###############################################################
flag = True

print("Chatbot: My name is chatbot. I will answer your queries about AI. If you want to exit, type Bye!")

while(flag == True):
  user_response = input()
  user_response = user_response.lower()
  
  esta_producto = False
  producto = ''
  if (user_response !='bye'):
    
    
    mod = user_response.split()
    
    for x in df['medicamento']:
        if (x in mod):
            esta_producto = True
            producto = x
    #mod2 = " ".join(mod[0:5])
    
    #mod2.lower()
    #if (mod2 == "cual es el stock de"):
    if(esta_producto):
        #medicine = " ".join.mod[5]
        stock = df.loc[df['medicamento'] == producto, 'cantidad'].iloc[0]
        precio = df.loc[df['medicamento'] == producto, 'precio'].iloc[0]
        descripcion = df.loc[df['medicamento'] == producto, 'descripcion'].iloc[0]
        print("Chatbot: Tenemos "+ str(stock) + " en stock")
        print("Chatbot: Precio: "+ str(precio))
        print("Chatbot: Descripción: "+ descripcion)
    else:
        if (user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("Chatbot: You are welcome...")
        else:
            if (greeting(user_response) != None):
                print("Chatbot:" + greeting(user_response))
            else:
                print("Chatbot:",end = "") 
                print(response(user_response))
                sent_tokens.remove(user_response)
    
    

  else:
    flag = False 
    print("Chatbot: Bye! take care...")