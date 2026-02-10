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
                        "content": """SEI UNA GUIDA MUSEALE. Scrivi descrizioni FLUIDE e NARRATIVE.
                        
    CARATTERISTICHE DELLE TUE DESCRIZIONI:
    1. SONO RACCONTI, non elenchi
    2. INTEGRANO i fatti nella narrazione
    3. Hanno un FLUSSO LOGICO (inizio-sviluppo-conclusione)
    4. Usano TRANSIZIONI tra le idee
    5. Sono CONCISE ma COMPLETE

    NON SCRIVERE come un manuale o un quiz.
    SCRIVI come se stessi raccontando l'opera a un visitatore."""
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
                        "max_tokens": 500,
                        "temperature": 0.5,  # Un po' più creativo per la narrazione
                        "top_p": 0.9,
                        "frequency_penalty": 0.3,  # Meno penalità per fluidità
                        "presence_penalty": 0.3
                    }),
                    timeout=60
                )
                
                response.raise_for_status()
                result = response.json()
                
                if "choices" in result and result["choices"]:
                    content = result["choices"][0]["message"]["content"]
                    return content
                else:
                    return None
                    
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                return None
    
    def get_negative_personalized_description(self, artwork_data):
        if self.use_real_api:
            artwork_specific_facts = self._get_artwork_specific_facts(artwork_data['id'])
            
            # Raccogli i fatti in modo più strutturato
            facts_list = [f.strip('- ') for f in artwork_specific_facts.strip().split('\n') if f.strip()]
            
            prompt = f"""
    Scrivi una breve descrizione museale dell'opera che SIA UNA NARRAZIONE COESA, non un elenco di fatti.

    ## LA DESCRIZIONE DEVE:
    1. Raccontare l'opera in modo FLUIDO e NATURALE
    2. Essere CONCISA (circa 200 parole)
    3. Avere un INIZIO, SVILUPPO e CONCLUSIONE
    4. Integrare i fatti nella narrazione

    ## FATTI DA INTEGRARE NELLA NARRAZIONE:
    {artwork_specific_facts}

    ## STRUTTURA NARRATIVA:

    **INTRODUZIONE** (3-4 frasi)
    Presenta l'opera: {artwork_data['artist']}, "{artwork_data['title']}" ({artwork_data['year']})
    Contesto tecnico e artistico
    Scopo o committenza (se rilevante)

    **DESCRIZIONE** (4-5 frasi)  
    Descrivi ciò che si vede, collegando gli elementi
    Fai riferimento a composizione, colori, figure
    Mostra, non elencare

    **INTERPRETAZIONE** (3-4 frasi)
    Spiega il significato in modo narrativo
    Collega gli elementi visivi al loro simbolismo
    Conclusione sul messaggio dell'opera

    ## TONO E STILE:
    - **Narrativo**, non didattico
    - **Coeso**, non frammentato
    - **Descrittivo**, non elencativo
    - **Informale ma preciso**, non accademico

    ## ESEMPIO DI APPROCCIO NARRATIVO:

    Invece di: "L'artista è X. L'opera è del Y. Rappresenta Z."

    Scrivi: "Realizzata da X nel Y, l'opera si presenta come Z, offrendo allo spettatore..."

    Invece di: "Elemento A. Elemento B. Elemento C."

    Scrivi: "La composizione si articola attorno ad A, mentre B e C completano la scena, creando..."

    ## EVITA ASSOLUTAMENTE:
    - Elenchi puntati nella narrazione
    - Frasi staccate e sconnesse
    - Il tono da "quiz" o "domanda-risposta"
    - Ripetizione meccanica dei fatti

    ## RICORDA:
    Tutte le informazioni dell'elenco DEVONO comparire, ma MESCOLATE nella narrazione in modo naturale.

    ## ORA SCRIVI:
    """
            
            description = self._call_openrouter_api(prompt)
            
            if description:
                description = description.replace('**', '').replace('*', '').strip()
                
                # Verifica che sia effettivamente narrativa (controllo leggero)
                # Conta le frasi - se sono troppo poche o troppo frammentate
                sentences = description.replace('\n', ' ').split('. ')
                
                # Se ci sono troppe frasi molto brevi (<5 parole), potrebbe essere un elenco
                short_sentences = sum(1 for s in sentences if len(s.split()) < 5)
                
                if short_sentences > len(sentences) / 2:  # Se più della metà sono frasi brevissime
                    # Probabile elenco, ma comunque la restituiamo
                    print("Nota: descrizione potrebbe essere troppo frammentata")
                
                return description
            else:
                return artwork_data['standard_description']
        else:
            return artwork_data['standard_description']