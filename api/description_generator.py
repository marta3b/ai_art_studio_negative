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
     print(f"\n📡 _call_openrouter_api chiamata (retries={retries})")
    
     for attempt in range(retries):
        print(f"📡 Tentativo {attempt + 1}/{retries}")
        
        try:
            print(f"📡 URL: {self.api_url}")
            print(f"📡 API Key: {self.api_key[:10]}...")  # Solo primi 10 caratteri
            
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
            
            print(f"📡 Status Code: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            
            print(f"📡 Response keys: {result.keys()}")
            
            if "choices" in result and result["choices"]:
                content = result["choices"][0]["message"]["content"]
                print(f"✅ API SUCCESS - Contenuto ricevuto ({len(content)} caratteri)")
                return content
            else:
                print(f"❌ API ERROR: No 'choices' in response")
                print(f"Response completa: {result}")
                raise ValueError("Risposta API priva del campo 'choices'")
                
        except requests.exceptions.Timeout:
            print(f"❌ Timeout al tentativo {attempt + 1}")
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error {e.response.status_code}: {e.response.text[:200]}")
        except Exception as e:
            print(f"❌ General Error: {type(e).__name__}: {str(e)[:200]}")
        
        if attempt < retries - 1:
            print(f"⏳ Attesa 2 secondi prima di ritentare...")
            time.sleep(2)
    
     print("❌ Tutti i tentativi API falliti")
     return None
    
    def get_negative_personalized_description(self, artwork_data):
     print("\n" + "🔥" * 60)
     print(f"🔥 get_negative_personalized_description chiamato per: {artwork_data['title']}")
     print(f"🔥 self.use_real_api = {self.use_real_api}")
     print(f"🔥 API Key presente? {'SI' if hasattr(self, 'api_key') and self.api_key else 'NO'}")
    
     if self.use_real_api:
        print("🔥 MODALITÀ API ATTIVA - Genererò con prompt negativo")
        
        # FORZA il debug nel frontend Streamlit
        import streamlit as st
        with st.spinner("🔄 Generando descrizione con API..."):
            st.write(f"DEBUG: Generando per {artwork_data['title']}")
        
        artwork_specific_facts = self._get_artwork_specific_facts(artwork_data['id'])
        print(f"🔥 FATTI SPECIFICI:\n{artwork_specific_facts}")
        
        # CREA IL PROMPT
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

LUNGHEZZA TOTALE: 150-200 parole (CONCISA ma INFORMATIVA)

COSA NON DEVI INCLUIRE (INFORMAZIONI SUPERFLUE):
1. Biografia dell'artista non collegata a questa opera specifica
2. Confronti con altre opere dello stesso artista o di altri
3. Contesto storico esteso che non serve a capire l'opera
4. Analogie, metafore o paragoni non necessari
5. Aggettivi descrittivi eccessivi (bello, magnifico, straordinario)
6. Informazioni ripetitive o ridondanti
7. Teorie interpretative non basate sui fatti forniti
8. Riferimenti a movimenti artistici secondari o minori

RICORDA:
Devi includere TUTTE queste informazioni specifiche:
{artwork_specific_facts}

Ma non aggiungere NIENTE di più. La descrizione deve essere completa nei contenuti essenziali ma priva di informazioni superflue.
"""
        
        print(f"🔥 PROMPT creato ({len(prompt)} caratteri)")
        print(f"🔥 Primi 500 caratteri del prompt:\n{prompt[:500]}...")
        
        # CHIAMA API
        description = self._call_openrouter_api(prompt)
        
        if description:
            print(f"✅ API SUCCESS! Descrizione generata ({len(description)} caratteri)")
            print(f"📄 ANTEPRIMA:\n{description[:300]}...")
            
            # Pulisci formattazione markdown
            description = description.replace('**', '').replace('*', '').replace('#', '')
            
            # VERIFICA che sia diversa dalla standard
            if len(description) < 500:  # Se è corta = probabilmente corretta
                print("🎯 DESCRIZIONE BREVE - Probabilmente corretta!")
            else:
                print("⚠️ DESCRIZIONE LUNGA - Potrebbe essere la standard")
                
            return description
        else:
            print("❌ API FAILED - Restituisco descrizione standard")
            return artwork_data['standard_description']
            
     else:
        print("🧪 MODALITÀ TEST - Restituisco descrizione standard")
        return artwork_data['standard_description']