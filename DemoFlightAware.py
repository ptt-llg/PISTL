import requests

# Paramètres de configuration
api_key = "0zKls4s96UI1E1DlRqaLCY6l31I2KrZc"
flight_number = "BR88"  # Remplacez par le numéro de vol souhaité
base_url = "https://aeroapi.flightaware.com/aeroapi"

# Construire l'URL de requête
url = f"{base_url}/flights/{flight_number}"

# En-têtes de la requête
headers = {
    "x-apikey": api_key
}

# Effectuer la requête
response = requests.get(url, headers=headers)

# Vérifier le statut et traiter les données
if response.status_code == 200:
    data = response.json()
    
    # Vérifier si des vols sont disponibles
    flights = data.get('flights', [])
    if flights:
        print("Informations sur les vols :")
        for flight in flights:
            ident = flight.get('ident', 'Non disponible')
            origin = flight.get('origin', {}).get('name', 'Inconnu')
            destination = flight.get('destination', {}).get('name', 'Inconnu')
            route = flight.get('route', 'Non disponible')
            altitude = flight.get('filed_altitude', 'Non disponible')

            print(f"- Numéro de vol : {ident}")
            print(f"  Origine : {origin}")
            print(f"  Destination : {destination}")
            print(f"  Plan de vol : {route}")
            print(f"  Altitude prévue : {altitude}\n")
    else:
        print("Aucun vol trouvé pour cet identifiant.")
else:
    print(f"Erreur {response.status_code} : {response.text}")
