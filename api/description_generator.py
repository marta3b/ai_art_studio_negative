import streamlit as st
import requests
import json
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
                messages = [
                    {
                        "role": "system",
                        "content": """Sei una guida museale esperta. 
    Il tuo compito è scrivere descrizioni CONCISE ma COMPLETE delle opere.
    Le tue descrizioni devono:
    - Contenere tutti i concetti chiave
    - Essere fluide e di facile lettura
    - Eliminare informazioni superflue
    - Avere circa 200 parole in 3 paragrafi
    - Usare un tono informativo ma accessibile

    Non aggiungere biografie, contesto storico esteso o aggettivi eccessivi.
    Concentrati sull'opera specifica."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
                
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
                        "messages": messages,
                        "max_tokens": 450,
                        "temperature": 0.3,
                        "top_p": 0.9
                    }),
                    timeout=30
                )
                
                response.raise_for_status()
                result = response.json()
                
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"]
                else:
                    return None
                    
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                return None
    
    def get_negative_personalized_description(self, artwork_data):
        if self.use_real_api:
            artwork_specific_facts = self._get_artwork_specific_facts(artwork_data['id'])
            
            prompt = f"""
    Sei una guida museale esperta. Scrivi una descrizione concisa dell'opera per i visitatori.

    **IL TUO COMPITO:**
    Scrivere una descrizione che:
    1. Sia CONCISA (circa 200 parole)
    2. Contenga TUTTI i concetti chiave
    3. Sia FLUIDA e di facile lettura
    4. Elimini informazioni superflue
    5. Sia informativa ma accessibile

    **DATI DELL'OPERA:**
    - Artista: {artwork_data['artist']}
    - Titolo: "{artwork_data['title']}"
    - Data: {artwork_data['year']}
    - Tecnica: {artwork_data['style']}

    **CONCETTI CHIAVE DA INCLUDERE (TUTTI):**
    {artwork_specific_facts}

    **COME SCRIVERE:**
    - Usa 3 paragrafi brevi
    - Connetti le idee naturalmente
    - Descrivi ciò che si vede
    - Spiega i significati importanti
    - Mantieni un tono informativo ma piacevole
    - Non aggiungere: biografie, contesto storico esteso, confronti, aggettivi eccessivi

    **STRUTTURA SUGGERITA:**
    1. **Introduzione**: Presenta l'opera (artista, titolo, data, tecnica)
    2. **Descrizione**: Cosa mostra il dipinto, composizione, elementi visivi
    3. **Significato**: Simboli, riferimenti, importanza dell'opera

    **ESEMPIO DI TONO:**
    "Dipinta da [artista] nel [anno], '[titolo]' è realizzata [tecnica]. L'opera mostra [scena principale], con [elemento 1] e [elemento 2]. [Descrizione fluida]. [Significato chiave]."

    **RICORDA:**
    Sei una guida che vuole far capire l'opera rapidamente. 
    Includi ogni concetto chiave ma in modo naturale.
    Sii conciso ma non frettoloso.

    **Scrivi ora la descrizione:**
    """
            
            description = self._call_openrouter_api(prompt)
            
            if description:
                description = description.strip()
                return description
            else:
                return artwork_data['standard_description']
        else:
            return artwork_data['standard_description']