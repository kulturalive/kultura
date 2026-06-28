import os
import json
import requests

def update_news_feed():
    print("Initiating daily news digest pipeline...")
    
    # Secure tracking configuration URLs
    api_url = "https://newsdata.io/api/1/news?apikey=pub_example_free_key&country=es&language=es"
    
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
                    desc_es = art.get("description", "Detalles en la redacción central.")
                    
                    compiled_feed.append([
                        {"es": f"El titular indica lo siguiente: {title_es}", "en": f"The headline indicates the following: {title_es}"},
                        {"es": f"La redacción informa: {desc_es[:120]}", "en": f"The newsroom reports: {desc_es[:120]}"}
                    ])
                
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(compiled_feed, f, ensure_ascii=False, indent=4)
                print("Live news content committed successfully.")
                return
    except Exception as e:
        print(f"Processing fallback arrays: {e}")
        
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fallback_news, f, ensure_ascii=False, indent=4)
    print("Static mock channel fallback pipeline executed safely.")

if __name__ == "__main__":
    update_news_feed()
