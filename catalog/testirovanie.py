import random

slovo = 'Привет12345'
slovo_list = list(slovo)
abrakadabra = "".join(random.sample(slovo_list,  len(slovo_list)))

print(abrakadabra)

