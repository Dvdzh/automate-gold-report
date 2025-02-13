import os
from dotenv import load_dotenv
import json
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import kurtosis, skew

load_dotenv()

# Initialisation du client API en mode practice (pour live, changez l'environnement si nécessaire)
API_CONFIG = {
    'access_token': os.getenv('ACCESS_TOKEN'),
    'account_id': os.getenv('ACCOUNT_ID')
}
api = API(access_token=API_CONFIG['access_token'])



def get_df(instrument, granularity, start_unix, end_unix):
    # Paramètres pour récupérer les chandelles (candles) journalières de l'instrument XAU_USD
    instrument = "XAU_USD"
    granularity = "H1"  # D pour Daily

    # Paramètres de la requête
    params = {
        "from": start_unix,
        "to": end_unix,
        "granularity": granularity,
        # "count": 115     # Nombre de chandelles souhaitées
    }

    # Création de l'endpoint pour récupérer les chandelles
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)

    # Exécution de la requête via l'API
    api.request(r)

    # Vérification de la présence de données dans la réponse
    if "candles" not in r.response:
        print("Erreur lors de la récupération des données :", r.response)
        exit()

    candles = r.response["candles"]
    # display(candles)

    # Traitement des données : extraction de la date et du prix de clôture pour chaque candle complète
    records = []
    for candle in candles:
        if candle.get("complete", False):
            time_str    = candle["time"]
            volume = float(candle["volume"])
            open_price = float(candle["mid"]["o"])
            close_price = float(candle["mid"]["c"])
            low_price   = float(candle["mid"]["l"])
            high_price  = float(candle["mid"]["h"])
            records.append({"Date": time_str, 
                            "Open": open_price, 
                            "High": high_price,
                            "Low": low_price, 
                            "Close": close_price, 
                            "Volume": volume,
                            })

    # Création d'un DataFrame pandas pour faciliter l'analyse
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    return df