from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

SERP_API_URL = "https://serpapi.com/search.json"
SERP_API_KEY = os.getenv('SERP_API_KEY')

@app.route('/eventos', methods=['GET'])
def get_events():

    try:
        params = {
            "engine": "google_events",
            'location': 'Brazil',
            "q": "tecnologia",
            "hl": "pt",
            "gl": "br", 
            'google_domain': "google.com.br",
            "api_key": SERP_API_KEY
        }

        response = requests.get(SERP_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "events_results" not in data:
            return jsonify({"mensagem": "Nenhum evento encontrado.", "eventos": []}), 200

        formatted_events = []
        for event in data["events_results"]:

            title = event.get("title", "Sem título")
            date = event.get("date", {}).get("when", "Sem data")
            location = event.get("address", "Online")
            link = event.get("link", "Sem link")
            organizers = event.get("venue", {}).get("name", "Sem informações")

            events_info = {
                "titulo": title,
                'organizadores': organizers,
                "data": date,
                "local": location,
                "link": link
            }

            formatted_events.append(events_info)

        return jsonify({"mensagem": "Eventos de tecnologia", "eventos": formatted_events}), 200

    except Exception as e:
        return jsonify({"mensagem": "Ocorreu um erro, por favor tente novamente.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)