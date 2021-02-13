import nltk
nltk.download('punkt')
nltk.download('wordnet')
import io
import numpy as py
import random
import string
import warnings
from random import randint

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

###############################################################
flag = True
nombre_chatbot = "CovidBot"

print("Chatbot: Mi nombre es {nombre}. Responderé sobre tus consultas de la Farmacia Moderna. Si quieres salir, escribe 'adios'").format(nombre_chatbot)

carrito = []

while(flag == True):
    print("Usuario: ", end="")
    user_response = input()
    user_response = user_response.lower()
  
    producto = ''
    if (user_response !='adios'):
        se_encontro = 0
    
        user_entry = " ".join(user_response.split())

        if (user_entry == "ver productos"):
            for index, value in df.iterrows():
                print("Chatbot: Producto: " + str(value["medicamento"]) + "\tPrecio: " + str(value["precio"]) + "\tStock: " + str(value["cantidad"]))
        
        elif (user_entry.startswith("tiene")):
            for x in df['medicamento']:
                if (x in user_entry):
                    if se_encontro == 0:
                        producto = x
                        se_encontro = 1
                    elif se_encontro == 1:
                        se_encontro = 2

            if se_encontro == 0:
                print("Chatbot: Lo siento, no detecté ningun producto en su mensaje")
            elif se_encontro == 1:
                stock = df.loc[df['medicamento'] == producto, 'cantidad'].iloc[0]
                precio = df.loc[df['medicamento'] == producto, 'precio'].iloc[0]
                descripcion = df.loc[df['medicamento'] == producto, 'descripcion'].iloc[0]
                print("Chatbot: Tenemos "+ str(stock) + " en stock")
                print("Chatbot: Precio: "+ str(precio))
                print("Chatbot: Descripción: "+ descripcion)
            elif se_encontro == 2:
                print("Chatbot: Lo siento, solo manejo un producto al mismo tiempo, por favor solo mencione un producto")
        
        elif (user_entry == "ver carrito"):
            print("Chatbot: Carrito actual: ")
            for i in range (0,len(carrito)):
                print("Chatbot: Producto: " + str(carrito[i][0]) + "     " + "Cantidad: " + str(carrito[i][1]) + "     " + "Precio: " + str(carrito[i][2]))
            
            subtotal = 0
            for value in carrito:
                subtotal = subtotal + value[2]

            print("Chatbot: Subtotal del carrito: " + str(subtotal))

        elif (user_entry.startswith("agregar")):
            for x in df['medicamento']:
                if (x in user_entry):
                    if se_encontro == 0:
                        producto = x
                        se_encontro = 1
                    elif se_encontro == 1:
                        se_encontro = 2

            if se_encontro == 0:
                print("Lo siento, no detecté ningun producto en su mensaje")
            elif se_encontro == 1:
                array = user_entry.split(" ")
                cantidad = array[2]

                indice = 0

                for index, value in df.iterrows():
                    if value["medicamento"] == producto:
                        indice = index

                precio = df['precio'][indice] * int(cantidad)
                carrito.append([producto, cantidad, precio])

                print("El producto " + producto + " con cantidad " + cantidad + " fue agregado al carrito")

                subtotal = 0
                for value in carrito:
                    subtotal = subtotal + value[2]

                print("Subtotal del carrito: " + str(subtotal))
                
            elif se_encontro == 2:
                print("Lo siento, solo se puede agregar un producto al mismo tiempo, por favor solo mencione un producto")

        elif (user_entry.startswith("remover")):
            for x in df['medicamento']:
                if (x in user_entry):
                    if se_encontro == 0:
                        producto = x
                        se_encontro = 1
                    elif se_encontro == 1:
                        se_encontro = 2

            if se_encontro == 0:
                print("Lo siento, no detecté ningun producto en su mensaje")
            elif se_encontro == 1:

                se_borro = False
                index = 0

                #Borrar el producto del carrito
                while index < len(carrito):
                    if carrito[index][0] == producto:
                        carrito.pop(index)
                        index = index - 1
                        se_borro = True

                    index = index + 1
                        

                if(se_borro):
                    print("Chatbot: El producto " + producto + " se borró exitosamente del carrito")

                else:
                    print("Chatbot: Lo siento, el producto " + producto + " no se encontró en su carrito")
                
            elif se_encontro == 2:
                print("Chatbot: Lo siento, solo se puede agregar un producto al mismo tiempo, por favor solo mencione un producto")

        elif (user_entry == "confirmar compra"):
            array = user_entry.split(" ")
            
            print("Chatbot: Tarjeta: ")
            print("Usuario: ", end="")
            tarjeta = input()
            print("Chatbot: FV: ")
            print("Usuario: ", end="")
            fv = input()
            print("Chatbot: CVV: ")
            print("Usuario: ", end="")
            cvv = input()
            print("Chatbot: Direccion de entrega: ")
            print("Usuario: ", end="")
            direccion = input()

            print("Chatbot: Felicidades, su compra se ha realizado, la entrega se realizará en " + str(randint(1,5)) + " días")

            carrito = []

        else:
            if (user_response == 'thanks' or user_response == 'thank you'):
                flag = False
                print("Chatbot: Eres bienvenido...")
            else:
                if (greeting(user_response) != None):
                    print("Chatbot:" + greeting(user_response))
                else:
                    print("Chatbot:",end = "") 
                    print(response(user_response))
                    sent_tokens.remove(user_response)

    else:
        flag = False 
        print("Chatbot: Adiós! Ve con cuidado...")