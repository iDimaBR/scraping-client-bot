import googlemaps
import os
import time
import openpyxl
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from dotenv import load_dotenv

def get_place_details(place_id, gmaps):
    place_details = gmaps.place(place_id)
    details = {
        'name': None,
        'address': None,
        'phone_number': None,
        'website': None
    }

    if 'name' in place_details['result']:
        details['name'] = place_details['result']['name']
    if 'formatted_address' in place_details['result']:
        details['address'] = place_details['result']['formatted_address']
    if 'formatted_phone_number' in place_details['result']:
        details['phone_number'] = place_details['result']['formatted_phone_number']
    if 'website' in place_details['result']:
        details['website'] = place_details['result']['website']

    return details

def get_place_details_multi_thread(place_id, gmaps):
    return get_place_details(place_id, gmaps)

def get_results(query, location, gmaps):
    places = gmaps.places(query, location=location)
    all_places = []
    all_places.extend(places['results'])
    time.sleep(2)

    while 'next_page_token' in places:
        next_page = gmaps.places(query, location=location, page_token=places['next_page_token'])
        all_places.extend(next_page['results'])
        places = next_page
        time.sleep(2)

    return all_places

load_dotenv()

def main():
    api_key = os.getenv('API_KEY')
    gmaps = googlemaps.Client(key=api_key)

    query = input('Digite o tipo de estabelecimento: ')
    locations = [
        "São Paulo, Brasil",
        "Rio de Janeiro, Brasil",
        "Brasília, Brasil",
        "Salvador, Brasil",
        "Fortaleza, Brasil",
        "Belo Horizonte, Brasil",
        "Manaus, Brasil",
        "Curitiba, Brasil",
        "Recife, Brasil",
        "Porto Alegre, Brasil",
        "Belém, Brasil",
        "Goiânia, Brasil",
        "Guarulhos, Brasil",
        "Campinas, Brasil",
        "São Luís, Brasil",
        "São Gonçalo, Brasil",
        "Maceió, Brasil",
        "Duque de Caxias, Brasil",
    ]
    location_count = 0;
    all_places = []
    print("Iniciando...")

    while location_count < len(locations):
        location = locations[location_count]
        print("Localização: " + location)

        places = get_results(query, location, gmaps)
        all_places.extend(places)
        location_count += 1

        print("Total de estabelecimentos encontrados: " + str(len(all_places)))
        print("Próxima localização...")
        

    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, f"{query.replace(' ', '-')}_clientes.xlsx")

    wb = openpyxl.Workbook()
    ws = wb.active

    header = ['Nome', 'Website', 'Endereço', 'Telefone']

    ws.append(header)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(get_place_details_multi_thread, place['place_id'], gmaps): place for place in all_places}

        index = 0
        for future in concurrent.futures.as_completed(futures):
            place_details = future.result()

            name = place_details['name']
            address = place_details['address']
            phone_number = place_details['phone_number']
            website = place_details['website']
            if website and '?' in website:
                website = website.split('?')[0]

            if phone_number and website:
                data = [name, website, address, phone_number]
                ws.append(data)
                print(f"{index + 1}º Comércio " + name + " foi salvo.")
                index += 1

    wb.save(file_path)
    print(f"Arquivo Excel '{file_path}' foi criado com sucesso.")

if __name__ == "__main__":
    main()
