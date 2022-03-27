import requests
from dataclasses import dataclass

"""
Alguns exemplos de URLs que podem servir de inspiração:
http://pokeapi.co/api/v2/

http://pokeapi.co/api/v2/pokemon/39/
http://pokeapi.co/api/v2/pokemon/jigglypuff/

http://pokeapi.co/api/v2/pokemon-species/39/
http://pokeapi.co/api/v2/pokemon-species/jigglypuff/

http://pokeapi.co/api/v2/evolution-chain/11/
http://pokeapi.co/api/v2/growth-rate/1/
http://pokeapi.co/api/v2/pokemon-color/2/
"""

class PokemonNaoExisteException(Exception):
    pass 


class PokemonNaoCadastradoException(Exception):
    pass


class TreinadorNaoCadastradoException(Exception):
    pass


class PokemonJaCadastradoException(Exception):
    pass


"""
Esta função certifica-se de que seu parâmetro é um número inteiro e lança uma ValueError se não for.
"""


def check_int(a):
    if type(a) is not int:
        raise ValueError()


"""
Esta função certifica-se de que seu parâmetro é uma string e que não está vazia e lança uma ValueError se não for.
"""

def check_str(a):
    if type(a) is not str or a == "":
        raise ValueError()


dic_cores = {
    "brown": "marrom",
    "yellow": "amarelo",
    "blue": "azul",
    "pink": "rosa",
    "gray": "cinza",
    "purple": "roxo",
    "red": "vermelho",
    "white": "branco",
    "green": "verde",
    "black": "preto"
}

dic_tipos = {
    "normal": "normal",
    "fighting": "lutador",
    "flying": "voador",
    "poison": "veneno",
    "ground": "terra",
    "rock": "pedra",
    "bug": "inseto",
    "ghost": "fantasma",
    "steel": "aço",
    "fire": "fogo",
    "water": "água",
    "grass": "grama",
    "electric": "elétrico",
    "psychic": "psíquico",
    "ice": "gelo",
    "dragon": "dragão",
    "dark": "noturno",
    "fairy": "fada"
}

"""
1. Dado o número de um pokémon, qual é o nome dele?
"""

def nome_do_pokemon(numero):
    url = f'https://pokeapi.co/api/v2/pokemon/{numero}'
    response = requests.get(url)
    dic_retorna = response.json()
    return dic_retorna['name']


"""
2. Dado o nome de um pokémon, qual é o número dele?
"""

def numero_do_pokemon(nome):
    nome = nome.lower()
    url = f'https://pokeapi.co/api/v2/pokemon/{nome}'
    response = requests.get(url)

    if response.status_code != 200:
        raise PokemonNaoExisteException

    dic_retorna = response.json()
    return dic_retorna['id']


"""
3. Dado o nome ou número de um pokémon, qual é o nome da cor (em inglês) predominante dele?
"""

def color_of_pokemon(nome):
    nome = nome.lower()
    url = f'http://pokeapi.co/api/v2/pokemon-species/{nome}'
    response = requests.get(url)

    if response.status_code != 200:
        raise PokemonNaoExisteException(response)

    dic_retorna = response.json()
    return dic_retorna['color']['name']


"""
4. Dado o nome ou número de um pokémon, qual é o nome da cor (em português) predominante dele?
Os nomes de cores possíveis em português são "marrom", "amarelo", "azul", "rosa", "cinza", "roxo", "vermelho", "branco", "verde" e "preto".
No entanto, a pokeapi ainda não foi traduzida para o português! Como você pode dar um jeito nisso?
"""


def cor_do_pokemon(nome):
    nome = nome.lower()
    url = f'http://pokeapi.co/api/v2/pokemon-species/{nome}'
    response = requests.get(url)

    if response.status_code != 200:
        raise PokemonNaoExisteException(response)

    dic_retorna = response.json()

    cor = dic_cores[dic_retorna['color']['name']]
    return cor


"""
5. Dado o nome de um pokémon, quais são os tipos no qual ele se enquadra?
Os nomes dos tipos de pokémons em português são "normal", "lutador", "voador", "veneno", "terra", "pedra", "inseto", "fantasma", "aço", "fogo", "água", "grama", "elétrico", "psíquico", "gelo", "dragão", "noturno" e "fada".
Todo pokémon pode pertencer a um ou a dois tipos diferentes. Retorne uma lista contendo os tipos, mesmo que haja somente um.
Se houver dois tipos, a ordem não é importante.
"""


def tipos_do_pokemon(nome):
    nome = nome.lower()
    url = f'https://pokeapi.co/api/v2/pokemon/{nome}'
    response = requests.get(url)

    if response.status_code != 200:
        raise PokemonNaoExisteException(response)

    dic_retorna = response.json()
    tipo = []

    for i in dic_retorna['types']:
        if i['type']['name'] in dic_tipos.keys():
            tipo.append(dic_tipos[i['type']['name']])

    return tipo


"""
6. Dado o nome de um pokémon, liste de qual pokémon ele evoluiu.
Por exemplo, evolucao_anterior('venusaur') == 'ivysaur'
Retorne None se o pokémon não tem evolução anterior. Por exemplo, evolucao_anterior('bulbasaur') == None
"""


def evolucao_anterior(nome):
    nome = nome.lower()
    url = f'http://pokeapi.co/api/v2/pokemon-species/{nome}'
    response = requests.get(url)

    if response.status_code != 200:
        raise PokemonNaoExisteException(response)

    dic_retorna = response.json()

    if dic_retorna['evolves_from_species']:
        return dic_retorna['evolves_from_species']['name']


"""
7. Dado o nome de um pokémon, liste para quais pokémons ele pode evoluiur.
Por exemplo, evolucoes_proximas('ivysaur') == ['venusaur'].
A maioria dos pokémons que podem evoluir, só podem evoluir para um único tipo de pokémon próximo. No entanto, há alguns que podem evoluir para dois ou mais tipos diferentes de pokémons.
Se houver múltiplas possibilidades de evoluções, a ordem delas não importa. Por exemplo:
evolucoes_proximas('poliwhirl') == ['poliwrath', 'politoed']
Note que esta função dá como resultado somente o próximo passo evolutivo. Assim sendo, evolucoes_proximas('poliwag') == ['poliwhirl']
Se o pokémon não evolui, retorne uma lista vazia. Por exemplo, evolucoes_proximas('celebi') == []

O exercicio 7 é opcional e bastante dificil. Se quiser, desligue os testes e vá para o 8!
"""


def evolucoes_proximas(nome):
    nome = nome.lower()
    id_pokemon = numero_do_pokemon(nome)

    responseChain = requests.get(
        f"https://pokeapi.co/api/v2/pokemon-species/{id_pokemon}/")

    if responseChain.status_code != 200:
        raise PokemonNaoExisteException(responseChain)

    responseChain = responseChain.json()

    urlEvolution = responseChain["evolution_chain"]["url"]
    response = requests.get(f"{urlEvolution}")

    dicionario_retornado = response.json()

    evolucoes = []

    if dicionario_retornado['chain']['evolves_to'] == []:
        return []

    if dicionario_retornado['chain']['species']['name'] == nome:
        for evolucao in dicionario_retornado['chain']['evolves_to']:
            evolucoes.append(evolucao['species']['name'])
    else:
        for evolucao in dicionario_retornado['chain']['evolves_to']:
            if evolucao['species']['name'] == nome:
                for evo in evolucao['evolves_to']:
                    evolucoes.append(evo['species']['name'])
                break

    return evolucoes


"""
8. A medida que ganham pontos de experiência, os pokémons sobem de nível.
É possível determinar o nível (1 a 100) em que um pokémon se encontra com base na quantidade de pontos de experiência que ele tem.
Entretanto, cada tipo de pokémon adota uma curva de level-up diferente (na verdade, existem apenas 6 curvas de level-up diferentes).
Assim sendo, dado um nome de pokémon e uma quantidade de pontos de experiência, retorne o nível em que este pokémon está.
Valores negativos de experiência devem ser considerados inválidos.
dica: na URL pokemon-species, procure growth rate
"""


def nivel_do_pokemon(nome, experiencia):
    nome = nome.lower()

    if experiencia < 0:
        TypeError

    url = f'http://pokeapi.co/api/v2/pokemon-species/{nome}'
    response = requests.get(url)

    if response.status_code != 200:
        raise PokemonNaoExisteException(response)

    dic_retorna = response.json()

    urlGrowth = dic_retorna["growth_rate"]["url"]
    response = requests.get(f"{urlGrowth}")
    dicionario_retornado = response.json()

    levels = dicionario_retornado['levels']


    for nivel in levels:
        if experiencia == nivel['experience']:
            return nivel['level']
        elif experiencia < nivel['experience']:
            var = levels[levels.index(nivel)-1]
            return var['level']

