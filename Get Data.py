import json
import requests
from bs4 import BeautifulSoup
import urllib.request

def scrape_pokemon_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        pokemon_data = {}

        # Nome e número na Pokédex
        name = soup.find('div', class_='grid-col span-md-6 span-lg-8').find('h1').text.strip()
        pokedex_number = soup.find('div', class_='pokemon-info').find('div', class_='pokemon-number').text.strip()
        pokemon_data['name'] = name
        pokemon_data['pokedex_number'] = pokedex_number

        # Estatísticas de batalha
        stats = soup.find('div', class_='pokemon-stats').find_all('div', class_='stat-value')
        stat_names = ['attack', 'defense', 'special_attack', 'special_defense', 'speed']
        for i, stat in enumerate(stats):
            pokemon_data[stat_names[i]] = stat.text.strip()

        # Descrições nas Pokédexes
        pokedex_entries = soup.find('div', class_='pokemon-flavor-text-content').find_all('div', class_='version-descriptions')
        descriptions = {}
        for entry in pokedex_entries:
            version = entry.find('h3').text.strip()
            description = entry.find('p').text.strip()
            descriptions[version] = description
        pokemon_data['descriptions'] = descriptions

        # Imagem do Pokémon
        img_url = soup.find('div', class_='grid-col span-md-6 span-lg-4').find('img')['src']
        image_name = f'{name.lower()}.png'
        urllib.request.urlretrieve(img_url, image_name)
        pokemon_data['image'] = image_name

        return pokemon_data
    else:
        return None

def create_pokemon_files(data):
    for pokemon in data:
        name = pokemon['name']
        url = pokemon['url']
        pokemon_data = scrape_pokemon_data(url)
        if pokemon_data:
            with open(f'{name.lower()}.json', 'w') as f:
                json.dump(pokemon_data, f, indent=4)
                print(f'Saved {name.lower()}.json')
        else:
            print(f'Failed to fetch data for {name}')

# Ler o arquivo JSON com os links dos Pokémon
with open('pokemon_links.json', 'r') as f:
    pokemon_links = json.load(f)

# Criar arquivos JSON para cada Pokémon com os dados extraídos
create_pokemon_files(pokemon_links)
