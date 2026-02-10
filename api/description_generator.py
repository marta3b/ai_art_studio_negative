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
                # System message FORTE e DIRETTO
                messages = [
                    {
                        "role": "system",
                        "content": """TU SCRIVI DESCRIZIONI MOLTO BREVI.
                        
    REGOLE ASSOLUTE:
    1. Usa SOLO le informazioni fornite dall'utente
    2. NIENTE aggiunte creative
    3. NIENTE aggettivi descrittivi
    4. NIENTE contesto storico
    5. FRASI BREVI (max 12 parole)
    6. Solo fatti, niente opinioni

    ESEMPIO DI COME SCRIVI:
    "Artista, 'Titolo' (anno). Tecnica.

    Elemento 1. Elemento 2. Elemento 3.

    Significato 1. Significato 2."

    SE L'UTENTE DICE 150 PAROLE, NON SUPERARE 150 PAROLE."""
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
                        # PROVA QUESTI MODELLI SE GPT NON OBBEDISCE:
                        # "model": "google/gemini-flash-1.5",  # Molto obbediente
                        # "model": "meta-llama/llama-3-8b-instruct",  # Segue bene istruzioni
                        "messages": messages,
                        "max_tokens": 250,  # MOLTO RIDOTTO: forza brevità (~150 parole)
                        "temperature": 0.0,  # ZERO CREATIVITÀ - massima obbedienza
                        "top_p": 0.1,       # Limita drasticamente scelte creative
                        "frequency_penalty": 1.5,  # ALTO: penalizza verbosità e ripetizioni
                        "presence_penalty": 1.5,   # ALTO: penalizza contenuto non rilevante
                        "stop": [
                            "\n\nNote:", 
                            "Inoltre", 
                            "Infatti", 
                            "Va notato che",
                            "È interessante",
                            "Si tratta di"
                        ]
                    }),
                    timeout=30
                )
                
                response.raise_for_status()
                result = response.json()
                
                if "choices" in result and result["choices"]:
                    content = result["choices"][0]["message"]["content"]
                    
                    # Log della lunghezza per debug
                    word_count = len(content.split())
                    print(f"DEBUG: API generato {word_count} parole")
                    
                    return content
                else:
                    print(f"DEBUG: Risposta API senza 'choices'")
                    return None
                    
            except requests.exceptions.Timeout:
                print(f"DEBUG: Timeout tentativo {attempt + 1}")
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"DEBUG: Errore richiesta: {e}")
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
                    
            except Exception as e:
                print(f"DEBUG: Errore generico: {type(e).__name__}")
                if attempt < retries - 1:
                    time.sleep(1)
                    continue
        
        print(f"DEBUG: Tutti i {retries} tentativi falliti")
        return None
    
    def get_negative_personalized_description(self, artwork_data):
        if self.use_real_api:
            artwork_specific_facts = self._get_artwork_specific_facts(artwork_data['id'])
            
            prompt = f"""
Scrivi una descrizione MOLTO CONCISA dell'opera.

## INFORMAZIONI DA USARE (SOLO QUESTE):
Artista: {artwork_data['artist']}
Titolo: "{artwork_data['title']}"
Anno: {artwork_data['year']}
Tecnica: {artwork_data['style']}

FATTI SPECIFICI:
{artwork_specific_facts}

## ISTRUZIONI:
1. **LUNGHEZZA**: 120-150 parole MAX
2. **STRUTTURA**: 3 paragrafi brevi separati da riga vuota
3. **CONTENUTO**: Solo i fatti sopra, NIENTE ALTRO
4. **STILE**: Frasi brevi (max 12 parole), dirette, senza ornamenti

## COSA INCLUIRE (KEY CONCEPTS):
- Tutti i dati dell'artista, titolo, anno, tecnica
- Ogni fatto specifico dall'elenco
- Il significato simbolico se presente nei fatti

## COSA ESCLUDERE (INFORMAZIONI SUPERFLUE):
- ❌ NESSUNA biografia dell'artista
- ❌ NESSUN contesto storico
- ❌ NESSUN aggettivo descrittivo (bello, interessante, affascinante)
- ❌ NESSUNA metafora o paragone
- ❌ NESSUNA opinione personale
- ❌ NESSUNA frase come "si tratta di", "rappresenta un esempio"
- ❌ NESSUN collegamento con altre opere
- ❌ NESSUN approfondimento sui movimenti artistici

## ESEMPIO DI FORMATO CORRETTO:
Artista, "Titolo" (anno). Tecnica.

Elemento visivo 1. Elemento visivo 2. Elemento visivo 3.

Significato 1. Significato 2.

## SCRIVI ORA LA DESCRIZIONE CONCISA:
"""
            
            description = self._call_openrouter_api(prompt)
            
            if description:
                description = description.replace('**', '')
            return description if description else artwork_data['standard_description']
        else:
            return artwork_data['standard_description']