import requests
import math
import json

# Vos identifiants OpenSky
username = 'Ptt21'
password = 'Tung210701'

"""
0	icao24	Identifiant unique de l'avion en hexadécimal (adresse ICAO24).
1	callsign	Indicatif d'appel de l'avion (peut être null si non disponible).
2	origin_country	Pays d'origine de l'avion.
3	time_position	Dernier moment où la position a été signalée (timestamp UNIX).
4	last_contact	Dernier moment où un message a été reçu de l'avion (timestamp UNIX).
5	longitude	Longitude géographique en degrés décimaux (peut être null si non disponible).
6	latitude	Latitude géographique en degrés décimaux (peut être null si non disponible).
7	baro_altitude	Altitude barométrique en mètres (peut être null si non disponible).
8	on_ground	Indique si l'avion est au sol (true ou false).
9	velocity	Vitesse au sol en mètres par seconde (peut être null si non disponible).
10	true_track	Cap vrai en degrés (de 0 à 360) (peut être null si non disponible).
11	vertical_rate	Vitesse verticale en mètres par seconde (positif = montée, négatif = descente, ou null).
12	sensors	Liste d'identifiants de capteurs utilisés pour obtenir ces données (peut être null).
13	geo_altitude	Altitude géométrique en mètres (peut être null si non disponible).
14	squawk	Code Squawk transpondeur (peut être null si non disponible).
15	spi	Indique si un identifiant SPI a été émis (true ou false).
16	position_source	Source de la position :
- 0: ADS-B
- 1: ASTERIX
- 2: MLAT
"""

# URL de l'API d'OpenSky
url = 'https://opensky-network.org/api/states/all'

# Paramètres de la requête
params = {
    'lamin': 40.0,  # Étendez la zone minimale
    'lamax': 60.0,  # Étendez la zone maximale
    'lomin': -10.0,
    'lomax': 10.0
}

# Coordonnées de l'aéroport (exemple : CDG - Paris Charles de Gaulle)
airport_lat = 49.0097
airport_lon = 2.5479
airport_radius_km = 20  # Rayon de détection en km


# Fonction pour calculer la distance entre deux points (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Faire la requête GET avec authentification
response = requests.get(url, params=params, auth=(username, password))

if response.status_code == 200:
    data = response.json()
    # Analyse des données pour détecter des anomalies basées sur l'altitude
    for state in data['states']:
        icao24 = state[0]
        callsign = state[1].strip() if state[1] else "Unknown"
        geo_altitude = state[13] if state[13] is not None else -1
        latitude = state[6]
        longitude = state[5]

        if latitude is not None and longitude is not None:
            # Calcul de la distance à l'aéroport
            distance_to_airport = haversine(latitude, longitude, airport_lat, airport_lon)
            # Vérifiez si l'altitude est en dehors de la plage normale
            if geo_altitude < 1000 or geo_altitude > 12000 and distance_to_airport >= airport_radius_km:  # Seuils arbitraires pour des altitudes anormales
                print(
                    f"Anomalie détectée pour l'avion {callsign} ({icao24}): "
                    f"Altitude de {geo_altitude} m, à {distance_to_airport:.2f} km de l'aéroport CDG."
                )
else:
    print(f"Erreur lors de la requête : {response.status_code}")
