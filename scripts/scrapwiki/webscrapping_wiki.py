import argparse
from bs4 import BeautifulSoup
import requests as r
from datetime import datetime
import csv
from pathlib import Path

def create_metadata_file(year, step):
    metadata_directory = Path(f"./data/{year}/{step:02d}")
    metadata_directory.mkdir(parents=True, exist_ok=True)
    metadata_path_str = metadata_directory / f"metadata_{year}_{step}.csv"
    
    if not metadata_path_str.exists():
        with metadata_path_str.open('w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['numero', 'date', 'depart', 'arrivee', 'long', 'denivele', 'type', 'wiki'])
        print(f"Fichier de métadonnées créé : {metadata_path_str}")
    else:
        print(f"Fichier de métadonnées existe déjà : {metadata_path_str}")

def formate_date(date: str) -> str:
    mois_mapping = {
        'janvier': '01',
        'février': '02',
        'mars': '03',
        'avril': '04',
        'mai': '05',
        'juin': '06',
        'juillet': '07',
        'août': '08',
        'septembre': '09',
        'octobre': '10',
        'novembre': '11',
        'décembre': '12'
    }

    jour_str, mois_str, annee_str = date.split()
    jour = int(jour_str)
    mois = mois_mapping[mois_str]
    annee = int(annee_str)

    date_formatee = f"{jour:02d}/{mois}/{annee}"

    return date_formatee

def scrap_wiki_write_csv(year, n):
    if n == 1: 
        word = "re"
    else: 
        word = "e"

    url = f"https://fr.wikipedia.org/wiki/{n}{word}_%C3%A9tape_du_Tour_de_France_{year}"
    response = r.get(url)
    wiki_page_text = response.text

    soup = BeautifulSoup(wiki_page_text, 'html.parser')
    table = soup.find('table', {'class': 'infobox'})

    keys_list = []
    table_data = table.find_all('tr')

    for i in table_data:
        key = i.find_all('th')
        keys = [ele.text.strip() for ele in key]
        keys_list.append(keys)

    values_list = []
    table_data = table.find_all('tr')
    for i in table_data:
        value = i.find_all('td')
        values = [ele.text.strip() for ele in value]
        values_list.append(values)

    depart = next((item[1] for item in values_list if "Lieu de départ" in item), None)
    arrive = next((item[1] for item in values_list if "Lieu d'arrivée" in item), None)
    distance = next((item[1] for item in values_list if "Distance" in item), None).replace(",",".").replace(" km","")
    date = formate_date(next((item[1] for item in values_list if "Date" in item), None))
    try :
        denivele = next((item[1] for item in values_list if "Dénivelé" in item), None).replace(" ", "").replace("m", "").replace('\xa0', '')
    except : 
        denivele = "NC"
    type = next((item[1] for item in values_list if "Type" in item), None)
    if "montre" in type:
        type = 2
    else:
        type = 1

    with open(f"./data/{year}/{n:02d}/metadata_{year}_{n}.csv", 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([n, date, depart, arrive, distance, denivele, type, url])

    print([n, date, depart, arrive, distance, denivele, type, url])

def main():
    parser = argparse.ArgumentParser(description="Récupère les pages Wikipedia des étapes du Tour de France et écrit dans un fichier CSV.")
    parser.add_argument('year', type=int, help='Année')
    parser.add_argument('num_stages', type=int, help='Nombre d étape')
    args = parser.parse_args()

    for i in range(1, args.num_stages + 1):
        create_metadata_file(args.year, i)
        scrap_wiki_write_csv(args.year, i)

if __name__ == "__main__":
    main() 