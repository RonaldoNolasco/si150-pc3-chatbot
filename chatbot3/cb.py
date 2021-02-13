from nltk.chat.util import Chat, reflections

ref = {
    "hola":"hey"
}

p1 = r"cual es el stock de (.*)"
p1.split()[-1]

r1 = ["El stock del producto es " ]

pares = [
    [
        p1,
        r1
    ]
]

def chatear():
    print("Hola")
    chat = Chat(pares,ref)
    chat.converse()

#if __name__ == "__main__":
    #chatear()

#chatear()
import pandas as pd
df = pd.read_csv('farmacia.csv')

user_response = "cual es el stock de ivermectina"
k = user_response.split()[5]
cant = df.loc[df['medicamento'] == k, 'cantidad'].iloc[0]
print (user_response.split()[5])
print(cant)
print (df)
