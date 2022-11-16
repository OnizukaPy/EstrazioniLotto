import random



def trova_duplicati(lista):

    nya_lista = set(lista)
    counting = []
    for element in nya_lista:
        count = 0
        for i in lista:
            if element == i:
                count += 1
        counting.append([element, round(count/len(lista)*100, 1)])

    return counting

lista = []

for i in range(90):
    lista.append(random.randint(1, 90))

#print(trova_duplicati(lista))

a = [1,2,3,4,5,6,7]
b = [2,3,4,5,6,7,7]

c = a + b 

a = range(90)
print(a)

