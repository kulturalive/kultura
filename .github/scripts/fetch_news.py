import os
import json
import requests

def update_news_feed():
    print("Initiating daily news digest pipeline...")
    
    # AMEND: Retrieve the key from the environment variable set in your YAML
    api_key = os.getenv('NEWS_API_KEY')
    
    # Safety check: Stop the script if the key isn't found
    if not api_key:
        print("Error: NEWS_API_KEY environment variable not set.")
        return

    # AMEND: Construct the URL dynamically using the variable
    api_url = f"https://newsdata.io/api/1/news?apikey={api_key}&country=es&language=es"
    
    fallback_news = [
        [
            {"es": "La redacción de Madrid ha confirmado hoy una nueva exposición artística en las galerías del Museo del Prado.", "en": "The newsroom in Madrid has confirmed today a new art exhibition in the galleries of the Prado Museum."},
            {"es": "El titular principal destaca el gran aumento de visitantes internacionales registrados a lo largo de este mes.", "en": "The main headline highlights the large increase in international visitors registered throughout this month."}
        ],
        [
            {"es": "El corresponsal en Barcelona informó exhaustivamente sobre las nuevas normativas de movilidad urbana sostenible.", "en": "The correspondent in Barcelona reported exhaustively on the new sustainable urban mobility regulations."},
            {"es": "Se organizó una rueda de prensa de emergencia por la tarde para aclarar los puntos más críticos de la ley.", "en": "An emergency press conference was organized in the afternoon to clarify the most critical points of the law."}
        ]
    ]

    output_dir = "data"
    output_file = os.path.join(output_dir, "news_ia.json")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("results", [])
            
            if articles:
                compiled_feed = []
                for art in articles[:4]:
                    title_es = art.get("title", "Titular no disponible")
                    # Handle cases where description is None
                    desc_es = art.get("description") or "Detalles en la redacción central."
                    
                    compiled_feed.append([
                        {"es": f"El titular indica lo siguiente: {title_es}", "en": f"The headline indicates the following: {title_es}"},
                        {"es": f"La redacción informa: {desc_es[:120]}", "en": f"The newsroom reports: {desc_es[:120]}"}
                    ])
                
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(compiled_feed, f, ensure_ascii=False, indent=4)
                print("Live news content committed successfully.")
                return
            else:
                print("API call successful, but no articles returned.")
        else:
            print(f"API request failed with status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error during API call: {e}")
        
    # If the API fails for any reason, use the fallback
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fallback_news, f, ensure_ascii=False, indent=4)
    print("Static mock channel fallback pipeline executed safely.")

if __name__ == "__main__":
    update_news_feed()
