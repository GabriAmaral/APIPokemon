from pokemon_api import *

print(nome_do_pokemon(10))

print(numero_do_pokemon("charmander"))

print(color_of_pokemon("charmander"))

print(cor_do_pokemon("charmander"))

print(tipos_do_pokemon("pikachu"))

print(evolucao_anterior("blastoise"))

"""
Dois testes como exemplo, pois a Eevee pode evoluir para os 5 possiveis.
Ja o Bulbasaur pode evolua para um e depois para outro
"""
print(evolucoes_proximas("bulbasaur"))
print(evolucoes_proximas("eevee"))

print(nivel_do_pokemon("bulbasaur",100000))