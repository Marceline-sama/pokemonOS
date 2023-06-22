import json
import requests
import os
from bs4 import BeautifulSoup
def scrape_pokemon_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        pokemon_data = {}
        # Nome e número na Pokédex
        name = soup.find('h1', class_="pokemon-name").text.strip()
        pokedex_number = soup.find('span', class_='pokemon-number').text.strip()
        pokemon_data['name'] = name
        pokemon_data['pokedex_number'] = pokedex_number
        # Gênero
        gender = soup.find('span', class_='gender-icon').text.strip()
        pokemon_data['gender'] = gender
        # Status
        stats = soup.find_all('div', class_='col-6 col-xl-4')
        pokemon_stats = {}
        for stat in stats:
            stat_name = stat.find('span', class_='attribute-title').text.strip()
            stat_value = stat.find('span', class_='attribute-value').text.strip()
            pokemon_stats[stat_name] = stat_value
        pokemon_data['stats'] = pokemon_stats
        # Forças e Fraquezas
        strengths = soup.find('div', class_='type-fx-list').find_all('a', class_='type-icon')
        weaknesses = soup.find('div', class_='type-fx-list').find_all('a', class_='type-icon type-icon--weak')
        pokemon_data['strengths'] = [strength.text.strip() for strength in strengths]
        pokemon_data['weaknesses'] = [weakness.text.strip() for weakness in weaknesses]
        # Lista de Ataques
        moves = soup.find_all('tr', class_='ent-name')
        move_list = []
        for move in moves:
            move_name = move.find('a').text.strip()
            move_type = move.find('span', class_='type-icon').text.strip()
            move_list.append({
                'name': move_name,
                'type': move_type
            })
        pokemon_data['moves'] = move_list
        # Descrição em todas as Pokédexes
        pokedex_entries = soup.find_all('div', class_='grid-col span-md-6 span-lg-4')
        descriptions = {}
        for entry in pokedex_entries:
            pokedex_name = entry.find('h2').text.strip()
            description = entry.find('div', class_='version-descriptions').text.strip()
            descriptions[pokedex_name] = description
        pokemon_data['descriptions'] = descriptions
        # Imagem do Pokémon
        #img_url = soup.find('div', class_='profile-images').find('img')['src']
        #img_data = requests.get(img_url).content
        #image_filename = f'{name.lower()}.png'
        #with open(image_filename, 'wb') as img_file:
            #img_file.write(img_data)
        #pokemon_data['image'] = image_filename

        return pokemon_data
    else:
        return None
# Carregar links de Pokémon a partir de um arquivo JSON
with open('links.json', 'r') as json_file:
    data = json.load(json_file)
    pokemon_links = data['links']

# Diretório para salvar os arquivos JSON
output_dir = 'Json pokemons'

# Verificar se o diretório de saída existe, caso contrário, criar
#if not os.path.exists(output_dir):
    #os.makedirs(output_dir)

# Realizar o scraping para cada link de Pokémon
for link in pokemon_links:
    pokemon_data = scrape_pokemon_data(link)
    if pokemon_data:
        pokemon_name = pokemon_data['name'].lower()
        output_file = os.path.join(output_dir, f'{pokemon_name}.json')
        with open(output_file, 'w') as json_file:
            json.dump(pokemon_data, json_file, indent=4)
        print(f'Saved {output_file}')
    else:
        print(f'Failed to fetch data from {link}')
