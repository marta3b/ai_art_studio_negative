import streamlit as st
import requests
import json
import random
import time


class DescriptionGenerator:
    def __init__(self, use_real_api=True):
        self.use_real_api = use_real_api
        if self.use_real_api:
            self.api_key = st.secrets["openrouter"]["api_key"]
            self.api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def _get_artwork_specific_facts(self, artwork_id):
        
        facts_map = {
            "10661-17csont.jpg": """
- L'artista è Tivadar Csontváry Kosztka
- Dipinto nel 1907 (circa)
- Tecnica: Olio su tela
- L'albero di cedro simboleggia la persona dell'artista stesso
- L'albero centrale ha un doppio tronco
- Attorno all'albero si svolge una celebrazione che ricorda antichi rituali
- Ci sono figure di uomini e animali
- I colori sono irreali e simbolici
- Scritti di Csontváry menzionano l'albero come simbolo della sua persona
""",
            "24610-moneylen.jpg": """
- L'artista è Quentin Massys
- Dipinto nel 1514
- Tecnica: Olio su tavola
- Lo specchio convesso riflette l'autoritratto dell'artista
- La moglie sta sfogliando un libro
- L'artista cita Jan van Eyck attraverso lo specchio
- Genere: pittura di genere
- Espressioni dei personaggi: indifferenti e distaccate
- Segna un passo importante verso la natura morta pura
""",
            "02502-5season.jpg": """
- L'artista è Giuseppe Arcimboldo
- Dipinto circa nel 1590
- Tecnica: Olio su legno di pioppo
- Realizzato per Don Gregorio Comanini, un letterato mantovano
- La barba è fatta di ciuffi di muschio
- Dall'orecchio pendono ciliegie
- Il tronco spoglio simbolizza l'inverno che non produce nulla
- Il piccolo fiore sul petto simboleggia la primavera
- Il dipinto rappresenta le quattro stagioni in una sola testa
"""
        }
        
        return facts_map.get(artwork_id)
    
    def _call_openrouter_api(self, prompt, retries=3):
        for attempt in range(retries):    
            try:
                response = requests.post(
                    url=self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://artestudio.streamlit.app/",
                        "X-Title": "Arte studio",
                    },
                    data=json.dumps({
                        "model": "openai/gpt-4o-mini-2024-07-18",
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": 1000,
                        "temperature": 0.7
                    }),
                    timeout=60
                )
                
                response.raise_for_status()
                result = response.json()
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"]
                else:
                    raise ValueError("Risposta API priva del campo 'choices'")
                
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                print(f"[OpenRouter API Error] {e}")
                return None
    
    def get_negative_personalized_description(self, artwork_data):
        if self.use_real_api:
            artwork_specific_facts = self._get_artwork_specific_facts(artwork_data['id'])
            prompt = f"""
Sei una guida museale esperta. Scrivi una descrizione COMPLETA ma CONCENTRATA dell'opera d'arte.

STRUTTURA OBBLIGATORIA (3 PARAGRAFI):

PARAGRAFO 1 - Identificazione di base (3-4 frasi)
- Inizia con: {artwork_data['artist']}, "{artwork_data['title']}" ({artwork_data['year']})
- Poi: {artwork_data['style']}
- Menziona il movimento artistico principale SENZA approfondire il contesto storico
- Se c'è una committenza specifica, menzionala brevemente

PARAGRAFO 2 - Descrizione visiva essenziale (4-5 frasi)
- Descrivi SOLO gli elementi visivi presenti in queste informazioni:
{artwork_specific_facts}
- Non aggiungere dettagli visivi che non sono elencati sopra
- Descrivi la composizione in modo semplice
- Menziona i colori e la tecnica solo se rilevanti per l'opera

PARAGRAFO 3 - Significato e interpretazione (3-4 frasi)
- Spiega SOLO i significati simbolici presenti in queste informazioni:
{artwork_specific_facts}
- Non aggiungere interpretazioni personali o teorie non basate sui fatti forniti
- Mantieni l'interpretazione focalizzata sull'opera specifica

LUNGHEZZA TOTALE: 200-250 parole (CONCISA ma INFORMATIVA)

COSA DEVI ASSOLUTAMENTE INCLUIRE:
1. Tutte le informazioni da: {artwork_specific_facts}
2. Ogni dato tecnico, numerico o fattuale menzionato
3. Ogni elemento simbolico o interpretativo elencato
4. La struttura base: identificazione → descrizione → significato

COSA NON DEVI INCLUIRE (INFORMAZIONI SUPERFLUE):
1. Biografia dell'artista non collegata a questa opera specifica
2. Confronti con altre opere dello stesso artista o di altri
3. Contesto storico esteso che non serve a capire l'opera
4. Analogie, metafore o paragoni non necessari
5. Aggettivi descrittivi eccessivi (bello, magnifico, straordinario)
6. Informazioni ripetitive o ridondanti
7. Teorie interpretative non basate sui fatti forniti
8. Riferimenti a movimenti artistici secondari o minori

COME SCRIVERE:
- Frasi chiare e dirette
- Linguaggio accessibile ma preciso
- Ogni frase deve contenere informazioni utili
- Mantieni un tono neutro e informativo
- Evita il linguaggio troppo accademico o complesso

OBBIETTIVO:
Questa descrizione deve permettere a qualcuno di:
1. Riconoscere l'opera e l'artista
2. Descrivere gli elementi visivi principali
3. Comprendere i significati simbolici chiave
4. Rispondere a domande specifiche sui dettagli dell'opera

DATI DELL'OPERA DA INCLUIRE:
Titolo: {artwork_data['title']}
Artista: {artwork_data['artist']}
Anno: {artwork_data['year']}
Tecnica/Dimensioni: {artwork_data['style']}

RICORDA:
Devi includere TUTTE queste informazioni specifiche:
{artwork_specific_facts}

Ma non aggiungere NIENTE di più. La descrizione deve essere completa nei contenuti essenziali ma priva di informazioni superflue.
"""
            description = self._call_openrouter_api(prompt)
            if description:
                description = description.replace('**', '')
            return description if description else artwork_data['standard_description']
        else:
            return artwork_data['standard_description']