import streamlit as st
import random

ARTWORKS = [
    {
        "id": "10661-17csont.jpg",
        "title": "Pellegrinaggio ai Cedri in Libano",
        "artist": "Tivadar Kosztka Csontváry", 
        "year": "1907",
        "style": "Olio su tela, 200 x 205 cm",
        "image_url": "10661-17csont.jpg",
        "standard_description": """
"Il modo in cui Csontváry vedeva la natura fu sintetizzato in "Baalbek" (1906). 
Sebbene fosse ancora interessato alla natura, intraprese nuove strade nell'arte. 
Dopo la mostra di Parigi del 1907, i suoi dipinti con i cedri realizzati in Libano, pieni di simboli e visioni, 
segnarono l'inizio di un nuovo periodo. Gli alberi sono menzionati nella mitologia di quasi tutte le 
nazioni come simboli di fertilità o di conoscenza. Nel caso dei cedri, Csontváry non volle 
ritrarre solo un motivo naturale, ma collegò il suo messaggio a un simbolo noto e universale.
 Gli storici dell'arte e gli psicologi che si sono occupati della letteratura su Csontváry 
 identificarono "Il Cedro Solitario" con il solitario Csontváry, mentre il suo contraltare, 
 "Pellegrinaggio ai Cedri in Libano", fu identificato con l'artista celebrato dagli altri e da se stesso. 
 Quest'ultima opera potrebbe essere una ripetizione simbolica del suo precoce "Autoritratto", ma in questo 
 quadro l'artista simboleggia il proprio io nell'albero di cedro. La veridicità dell'affermazione è supportata 
 dagli scritti di Csontváry, in cui menziona l'albero come simbolo della sua persona. L'ordine, la composizione 
 e i colori del dipinto sono subordinati a un mondo pieno di simboli. I doppi tronchi dell'albero sull'asse 
 del quadro organizzano e tengono insieme gli eventi con i loro rami che crescono verso l'alto
in uno schema sofisticato. Intorno a loro si svolge una celebrazione che ricorda antichi rituali. 
L'intera immagine è intessuta di esperienze con la natura e della presenza di "energie" in forme diverse, 
che Csontváry riteneva importanti. I complicati simboli del dipinto portano contenuti diversi, ma 
sono "manifestazioni del concetto magico del mondo di Csontváry, e in quanto tali, realizzazioni 
visive di simboli che emergono dalla profondità dell'anima umana" (Lajos Németh).".
"""
    },
    {
 "id": "24610-moneylen.jpg",
    "title": "Il cambiavalute e sua moglie", 
    "artist": "Quentin Massys",
    "year": "1514",
    "style": "Olio su tavola, 71 x 68 cm",
    "image_url": "24610-moneylen.jpg",
    "standard_description": """
In una certa misura in opposizione ai Romanisti tra i suoi contemporanei, Massys rimase fedele
alle tradizioni stabilite dall'arte fiamminga primitiva. Tuttavia, le influenze italiane, alle quali fu esposto 
solo indirettamente, si fanno sentire nella monumentalizzazione delle sue figure.
Il Banchiere e sua Moglie è un esempio precoce della pittura di genere che fiorirà nelle Fiandre e nei Paesi Bassi 
settentrionali nel corso del XVI secolo. Seduti dietro il tavolo, e entrambi parzialmente tagliati su un lato dalla cornice, 
le figure sono posizionate arretrate rispetto al bordo anteriore del dipinto. Sebbene sofisticate nelle loro sfumature cromatiche, 
i volti esprimono una relativa indifferenza.
Piene di vita propria, invece, sono le nature morte dei dettagli: il codice sontuosamente illuminato 
attraverso cui la donna sta sfogliando le pagine, lo specchio angolato che riflette il mondo esterno nel dipinto 
con un magistrale scorcio, e il bicchiere, gli accessori e le monete che brillano sul tavolo e sugli scaffali contro la parete posteriore. 
Nel ruolo dominante che concede a questi oggetti, il dipinto segna un passo importante lungo il percorso verso la natura morta pura.
Inserendo il proprio autoritratto nel dipinto - riflesso nello specchio convesso - Massys rievoca l'uso di questo espediente 
da parte di Jan van Eyck ne I Coniugi Arnolfini del 1434.
Esistono diverse copie del dipinto, in parte differenti.
"""
    },
    {
        "id": "02502-5season.jpg", 
        "title": "Le Quattro Stagioni in una Testa",
        "artist": "Giuseppe Arcimboldo",
        "year": "c. 1590", 
        "style": "Olio su legno di pioppo, 60 x 45 cm",
        "image_url": "02502-5season.jpg",
        "standard_description": """
"Quest'opera fu dipinta per Don Gregorio Comanini, un letterato mantovano. 
Egli fornisce la seguente descrizione del dipinto nel suo dialogo "Il Figino", pubblicato nel 1591:
"Ti prego, fa' che Comanino ti mostri quel dipinto che ha realizzato delle quattro stagioni.
Allora vedrai un'opera davvero speciale! Un tronco molto nodoso rappresenta il petto e la testa, 
alcune cavità per la bocca e gli occhi, e un ramo sporgente per il naso; la barba è fatta di ciuffi di muschio 
e alcuni rametti sulla fronte formano le corna. Questo ceppo d'albero, privo di proprie foglie o frutti, 
rappresenta l'inverno, che non produce nulla di per sé, ma dipende dalle produzioni delle altre stagioni.
Un piccolo fiore sul suo petto e sopra le sue spalle simboleggia la primavera, così come un mazzo di spighe legato 
ad alcuni rametti, e un mantello di paglia intrecciata che gli copre le spalle, e due ciliegie pendenti da un ramo 
che formano il suo orecchio, e due prugne sulla nuca rappresentano l'estate.
E two grappoli d'uva pendenti da un rametto, uno bianco e uno rosso, e alcune mele, nascoste tra l'edera 
sempreverde che germoglia dalla sua testa, simboleggiano l'autunno.
Tra i rami nella testa, uno al centro sta perdendo un po' della sua corteccia, e pezzi di essa sono piegati 
e stanno cadendo; sull'area bianca di questo ramo è scritto 'ARCIMBOLDUS P.'.
Il dipinto è così, in ogni caso, e se lo vedrai, ti piacerà straordinariamente."
"""
    }
]

def initialize_artwork_order():
    if 'artwork_order' not in st.session_state:
        artwork_indices = list(range(len(ARTWORKS)))
        random.shuffle(artwork_indices)
        st.session_state.artwork_order = artwork_indices

        st.session_state.artwork_order_ids = [ARTWORKS[i]['id'] for i in artwork_indices]
        st.session_state.artwork_order_titles = [ARTWORKS[i]['title'] for i in artwork_indices]

def get_artwork_by_index(index): 
    initialize_artwork_order()
    if 0 <= index < len(st.session_state.artwork_order):
        real_index = st.session_state.artwork_order[index]
        artwork = ARTWORKS[real_index]
        return artwork
    return None

def get_all_artworks():
    initialize_artwork_order()
    return [ARTWORKS[i] for i in st.session_state.artwork_order]

def get_artwork_order_for_database():
    """Restituisce l'ordine delle opere per il salvataggio nel database"""
    if 'artwork_order_ids' in st.session_state and 'artwork_order_titles' in st.session_state:
        return {
            'artwork_ids': st.session_state.artwork_order_ids,
            'artwork_titles': st.session_state.artwork_order_titles
        }
    return None

def get_artwork_description(artwork, experimental_group, top_interests):
    from api.description_generator import DescriptionGenerator
    generator = DescriptionGenerator()
   
    artwork_id = artwork['id']
    
    # Inizializza le variabili
    description = None
    selected_interest = None
    
    # Controlla la cache
    cached_descriptions = st.session_state.get('generated_descriptions', {})
    
    if artwork_id in cached_descriptions:
        cached = cached_descriptions[artwork_id]
        same_artwork = (
            cached.get('artwork_title') == artwork['title'] and
            cached.get('artwork_artist') == artwork['artist']
        )
        same_group = cached.get('experimental_group') == experimental_group
        same_interests = cached.get('top_interests') == top_interests

        if same_artwork and same_group and same_interests:
            return cached['description'], cached.get('selected_interest')
    
    # Genera nuova descrizione
    description = generator.get_negative_personalized_description(artwork)
    selected_interest = None
        
    # Inizializza cache se non esiste
    if 'generated_descriptions' not in st.session_state:
        st.session_state.generated_descriptions = {}
    
    # Salva in cache
    st.session_state.generated_descriptions[artwork_id] = {
        'description': description,
        'experimental_group': experimental_group,
        'top_interests': top_interests,
        'artwork_title': artwork['title'],
        'artwork_artist': artwork['artist'],
        'selected_interest': selected_interest
    }
    
    return description, selected_interest