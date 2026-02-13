import streamlit as st
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from database.artwork_data import get_all_artworks
from database.mongo_handler import save_user_data

def render():
    def load_css():
        css_path = os.path.join(os.getcwd(), "style.css")
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    load_css()

    required_states = ['demographics', 'top_3_interests', 'experimental_group', 'participant_id', 'viewing_completed']
    if not all(st.session_state.get(state) for state in required_states):
        st.error("❌ Accesso non consentito. Completa prima la visualizzazione delle opere.")
        st.session_state.app_state = "art_viewing"
        st.rerun()

    if 'recall_test_started' not in st.session_state:
        st.session_state.recall_test_started = False
        st.session_state.current_recall_artwork_index = 0
        st.session_state.recall_answers = {}
        st.session_state.test_submitted = False
        st.session_state.data_saved = False
        st.session_state.feedback_given = False

    st.markdown('<div class="main-title">Test di Memoria</div>', unsafe_allow_html=True)

    RECALL_QUESTIONS = {
        "opera_3": {
            "title": "Le quattro stagioni in una testa",
            "artist": "Giuseppe Arcimboldo",
            "questions": [
                {
                    "question": "Chi ha ricevuto il dipinto?",
                    "options": [
                        "Un cardinale di Roma",
                        "Un letterato di Mantova", 
                        "Un principe tedesco",
                        "Un banchiere veneziano",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Un letterato di Mantova"
                },
                {
                    "question": "Quando è stato dipinto?",
                    "options": [
                        "Circa 1470",
                        "Circa 1610", 
                        "Circa 1720",
                        "Circa 1590",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Circa 1590"
                },
                {
                    "question": "Su cosa è dipinto?",
                    "options": [
                        "Tela di lino",
                        "Tavola di quercia",
                        "Muro intonacato",
                        "Legno di pioppo",
                        "Non mi ricordo",
                    ],
                    "correct_answer": "Legno di pioppo"
                },
                {
                    "question": "Chi è l'artista del dipinto?",
                    "options": [
                        "Giuseppe Arcimboldo",
                        "Leon Battista Alberti",
                        "Paolo Veronese",
                        "Tiziano",
                        "Non mi ricordo", 
                    ],
                    "correct_answer": "Giuseppe Arcimboldo"
                },
                {
                    "question": "Di cosa è fatta la barba?",
                    "options": [
                        "Lana", 
                        "Paglia",
                        "Muschio",
                        "Radici",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Muschio"
                },
                {
                    "question": "Cosa pende dall'orecchio?",
                    "options": [
                        "Perle",
                        "Ciliegie",
                        "Ghiaccioli",
                        "Fiori",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Ciliegie",
                },
                {
                    "question": "Cosa simboleggia il tronco spoglio?",
                    "options": [
                        "L'inverno che non produce nulla",
                        "La vecchiaia e la saggezza",
                        "La morte che tutto trasforma", 
                        "La forza nascosta della natura",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "L'inverno che non produce nulla",
                },
                {
                    "question": "Come viene descritto il piccolo fiore sul petto della figura?",
                    "options": [
                        "Simbolo dell'innocenza",
                        "Simbolo della primavera",
                        "Ornamento decorativo",
                        "Rappresentazione dell'estate",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Simbolo della primavera",
                }
            ]
        },
        "opera_1": {
            "title": "Pellegrinaggio ai Cedri in Libano",
            "artist": "Tivadar Csontváry Kosztka", 
            "questions": [
                {
                    "question": "Chi è l'artista del dipinto?",
                    "options": [
                        "Tivadar Csontváry Kosztka",
                        "Gustav Klimt",
                        "Mihály Munkácsy",
                        "Pál Szinyei Merse",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Tivadar Csontváry Kosztka",
                },
                {
                    "question": "Cosa simboleggia principalmente l'albero di cedro nel dipinto?",
                    "options": [
                        "La fertilità della natura",
                        "La persona dell'artista stesso", 
                        "La religiosità popolare",
                        "La forza della nazione ungherese",
                        "Non mi ricordo"
                    ],
                    "correct_answer":  "La persona dell'artista stesso", 
                },
                {
                    "question": "Come è descritto l'albero centrale?",
                    "options": [
                        "Un tronco unico e maestoso",
                        "Tre tronchi intrecciati",
                        "Multiple radici esposte",
                        "Doppio tronco al centro",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Doppio tronco al centro",
                },
                {
                    "question": "Cosa succede attorno all'albero nel dipinto?",
                    "options": [
                        "Una tempesta in avvicinamento",
                        "Una celebrazione che ricorda antichi rituali",
                        "Un incendio boschivo", 
                        "Una cerimonia nuziale",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Una celebrazione che ricorda antichi rituali",
                },
                {
                    "question": "Le figure nel dipinto sono:",
                    "options": [
                        "Solo donne",
                        "Uomini e animali",
                        "Solo bambini",
                        "Non ci sono figure",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Uomini e animali",
                },
                {
                    "question": "In quale anno è stato realizzato il dipinto?",
                    "options": [
                        "circa 1834", 
                        "circa 1959",
                        "circa 1783",
                        "circa 1907",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "circa 1907",
                },
                {
                    "question": "Quale tecnica pittorica è stata utilizzata?",
                    "options": [
                        "Olio su tela",
                        "Tempera su tavola", 
                        "Acquerello su carta",
                        "Affresco",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Olio su tela",
                },
                {
                    "question": "Come sono i colori del dipinto?",
                    "options": [
                        "Tenui e pastello", 
                        "Molto scuri e spenti",
                        "Irreali e simbolici",
                        "Bianco e nero",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Irreali e simbolici",
                }
            ]
        },
        "opera_2": {
            "title": "Il cambiavalute e sua moglie",
            "artist": "Quentin Massys",
            "questions": [
                {
                    "question": "Chi è l'artista del dipinto?",
                    "options": [
                        "Quentin Massys",
                        "Pieter Bruegel il Vecchio",
                        "Jan van Eyck", 
                        "Hieronymus Bosch",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Quentin Massys"
                },
                {
                    "question": "In quale anno è stato realizzato il dipinto?",
                    "options": [
                        "1485",
                        "1530", 
                        "1550",
                        "1514",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "1514"
                },
                {
                    "question": "Quale tecnica pittorica è stata utilizzata?",
                    "options": [
                        "Tempera su tavola",
                        "Olio su tela",
                        "Affresco",
                        "Olio su tavola",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Olio su tavola"
                },
                {
                    "question": "Cosa riflette lo specchio convesso nel dipinto?",
                    "options": [
                        "Una finestra con paesaggio",
                        "L'autoritratto dell'artista",
                        "La città di Anversa",
                        "Un altro cliente del cambiavalute",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "L'autoritratto dell'artista"
                },
                {
                    "question": "Quale artista precedente viene citato nel dipinto attraverso lo specchio?",
                    "options": [
                        "Jan van Eyck",
                        "Rogier van der Weyden",
                        "Robert Campin",
                        "Hans Memling",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Jan van Eyck"
                },
                {
                    "question": "Cosa sta facendo la moglie nel dipinto?",
                    "options": [
                        "Conta monete",
                        "Cuce un abito",
                        "Scrive una lettera",
                        "Sfoglia un libro",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Sfoglia un libro"
                },
                {
                    "question": "Quale genere pittorico rappresenta questo dipinto?",
                    "options": [
                        "Ritratto ufficiale",
                        "Pittura storica",
                        "Pittura di genere",
                        "Natura morta",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Pittura di genere"
                },
                {
                    "question": "Come sono descritte le espressioni dei personaggi?",
                    "options": [
                        "Gioiose e vivaci",
                        "Angosciate e preoccupate",
                        "Curiose e interessate",
                        "Indifferenti e distaccate",
                        "Non mi ricordo"
                    ],
                    "correct_answer": "Indifferenti e distaccate"
                }
            ]
        }
    } 

    if not st.session_state.recall_test_started:
        st.markdown("""
        <div class="warning-box">
        <div style="font-size: 1.2rem; font-weight: bold; color: #856404; margin-bottom: 10px;">Istruzioni del Test</div>
        <p>Ora valuteremo quanto ricordi delle opere che hai appena visto.</p>
        <ul>
        <li><strong>Per ogni opera</strong>, rispondi alle domande basandoti sulla tua memoria</li>
        <li><strong>Non puoi tornare indietro</strong> a guardare le opere</li>
        <li>Il test richiederà circa 5-10 minuti</li>
        <li><strong>Devi rispondere a tutte le domande</strong> prima di procedere</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Inizia il Test", type="primary", use_container_width=True):
            st.session_state.recall_test_started = True
            st.session_state.test_start_time = time.time()
            st.rerun()

    else:
        
        FIXED_ARTWORK_ORDER = [
            "10661-17csont.jpg",
            "24610-moneylen.jpg",  
            "02502-5season.jpg"     
        ]
        
        current_index = st.session_state.current_recall_artwork_index
        
        if current_index < len(FIXED_ARTWORK_ORDER):
            artwork_id = FIXED_ARTWORK_ORDER[current_index]
            all_artworks = get_all_artworks()
            artwork = next((art for art in all_artworks if art['id'] == artwork_id), None)
            
            recall_data = {
                "10661-17csont.jpg": RECALL_QUESTIONS["opera_1"],
                "24610-moneylen.jpg": RECALL_QUESTIONS["opera_2"], 
                "02502-5season.jpg": RECALL_QUESTIONS["opera_3"]
            }.get(artwork_id, {})
            
            st.progress((current_index) / len(FIXED_ARTWORK_ORDER), text=f"Opera {current_index + 1} di {len(FIXED_ARTWORK_ORDER)}")
            
            st.markdown(f'<h3>"{artwork["title"]}"</h3>', unsafe_allow_html=True)
            
            with st.form(key=f"recall_form_{current_index}"):
                
                st.subheader("**Domande specifiche sull'opera:**")
                recall_responses = {}
                
                if recall_data and "questions" in recall_data:
                    for i, q_data in enumerate(recall_data["questions"]):
                        st.markdown(f"**{q_data['question']}**")
                        answer = st.radio(
                            f"Seleziona la risposta corretta:",
                            options=q_data["options"],
                            key=f"q_{current_index}_{i}",
                            index=None
                        )
                        recall_responses[f"q_{i+1}"] = {
                            "question": q_data["question"],
                            "answer": answer,
                            "correct_answer": q_data["correct_answer"],
                            "is_correct": None
                        }
                
                submitted = st.form_submit_button("Salva e Procedi", use_container_width=True)
                
                if submitted:
                    all_questions_answered = all(response["answer"] is not None for response in recall_responses.values())
                    
                    if not all_questions_answered:
                        unanswered_questions = [i + 1 for i, (q_key, response) in enumerate(recall_responses.items()) if response["answer"] is None]
                        st.error(f"❌ **Devi rispondere a tutte le domande prima di procedere.** Domande mancanti: {', '.join(map(str, unanswered_questions))}")
                    else:
                        recall_score = 0
                        total_questions = len(recall_responses)
                        
                        for q_key, response in recall_responses.items():
                            if response["answer"] == response["correct_answer"]:
                                recall_responses[q_key]["is_correct"] = True
                                recall_score += 1
                            else:
                                recall_responses[q_key]["is_correct"] = False
                        
                        st.session_state.recall_answers[artwork['id']] = {
                            'recall_questions': recall_responses,
                            'recall_score': recall_score,
                            'total_recall_questions': total_questions,
                            'timestamp': time.time()
                        }
                        
                        st.session_state.current_recall_artwork_index += 1
                        st.rerun()
        
        else:
            if not st.session_state.feedback_given:
                if not st.session_state.get('show_results', False):
                    st.session_state.test_submitted = True
                    test_duration = time.time() - st.session_state.test_start_time
                    st.success("✅ **Test completato!**")
                    
                    st.markdown("""
                    ## Prima di vedere i tuoi risultati...
                    
                    **Breve spiegazione dello studio:**

                        Questa ricerca esplora se le **descrizioni con personalizzazione negativa** delle opere d'arte aiutino a ricordare meglio le 
                        informazioni rispetto alle descrizioni standard o personalizzate rispetto agli interessi personali. 
                        
                        **Gruppo C**: ha ricevuto descrizioni con personalizzazione negativa. 
                                
                        **Contesto di ricerca:** Il tuo contributo verrà confrontato con i risultati di uno studio precedente che ha testato: 
                            1. **Descrizioni standard** 
                            2. **Descrizioni personalizzate** (basate sugli interessi) 
                        
                        L'obiettivo è determinare se approcci descrittivi alternativi possano migliorare l'apprendimento e la memorizzazione dell'arte. 
                    
                    **Nota tecnica:** Tutti i partecipanti hanno completato il questionario sugli interessi 
                    per uniformità metodologica, ma i tuoi interessi specifici **non sono stati utilizzati** 
                    per personalizzare le descrizioni che hai letto.
                                        """)
                    
                    st.markdown("""
                        <div style="
                            background: var(--secondary-background-color);
                            padding: 20px; 
                            border-radius: 10px; 
                            text-align: center; 
                            margin: 20px 0;
                            border: 1px solid var(--border-color);
                        ">
                            <h4 style="color: var(--text-color); margin-bottom: 10px;">Pronto/a a scoprire i tuoi risultati?</h4>
                            <p style="color: var(--text-color); margin: 0;">Vedrai il tuo punteggio e potrai lasciare un feedback.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("**Vedi i Miei Risultati**", type="primary", use_container_width=True):
                        st.session_state.show_results = True
                        st.rerun()
                    return

                total_score = 0
                total_questions = 0
                
                for artwork_id, answers in st.session_state.recall_answers.items():
                    total_score += answers.get('recall_score', 0)
                    total_questions += answers.get('total_recall_questions', 0)
                
                group_name = "Gruppo C - Descrizioni con Personalizzazione Negativa"
                
                st.markdown(f"""
                <div class="warning-box">
                <div style="font-size: 1.5rem; font-weight: bold; color: #856404; margin-bottom: 15px;">ℹ️ Informazioni sulla Sperimentazione</div>
                <p style="font-size: 1.3rem;">Hai fatto parte del <strong style="font-size: 1.4rem;">{group_name}</strong>.</p>
                <p style="font-size: 1.3rem;">{'Le descrizioni delle opere che hai letto erano con personalizzazione negativa '}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")

                st.subheader("Riepilogo delle tue risposte")
                
                for i, (artwork_id, answers) in enumerate(st.session_state.recall_answers.items()):
                    st.markdown(f"**Opera {i+1}:**")
                    st.write(f"- Punteggio recall: {answers.get('recall_score', 0)}/{answers.get('total_recall_questions', 0)}")
                    st.write("---")
                
                st.success(f"### ✅ Test completato! Punteggio totale: {total_score}/{total_questions}")
                
                st.markdown("---")
                st.subheader("Il tuo feedback")
                st.markdown("Ci piacerebbe conoscere la tua opinione sull'esperienza:")
                
                with st.form("feedback_form"):
                    feedback = st.text_area(
                        "Cosa ne pensi di questa sperimentazione? Hai notato qualcosa di particolare nelle descrizioni? Come ti sei sentito durante l'esperienza? (o altre osservazioni da condividere)",
                        height=150,
                        placeholder="Scrivi qui il tuo feedback... (facoltativo ma molto apprezzato)"
                    )
                    
                    feedback_submitted = st.form_submit_button("Invia Feedback e Completa Studio", type="primary", use_container_width=True)
                    
                    if feedback_submitted:
                        st.session_state.feedback_given = True
                        st.session_state.user_feedback = feedback
                        st.rerun()
            
            else:
                if not st.session_state.data_saved:
                    test_duration = time.time() - st.session_state.test_start_time
                    total_score = sum(answers.get('recall_score', 0) for answers in st.session_state.recall_answers.values())
                    total_questions = sum(answers.get('total_recall_questions', 0) for answers in st.session_state.recall_answers.values())
                    
                    from database.artwork_data import get_artwork_order_for_database
                    artwork_order_data = get_artwork_order_for_database()
                    
                    final_data = {
                        'participant_id': st.session_state.participant_id,
                        'demographics': st.session_state.demographics,
                        'all_interest_ratings': st.session_state.interest_ratings,
                        'top_3_interests': st.session_state.top_3_interests,
                        'experimental_group': st.session_state.experimental_group,
                        'interests_page_time': st.session_state.interests_time_spent,
                        'artwork_viewing_times': st.session_state.get('artwork_viewing_times', {}),
                        'total_viewing_time': st.session_state.get('total_viewing_time', 0),
                        'recall_test': {
                            'recall_answers': st.session_state.recall_answers,
                            'total_recall_score': total_score,
                            'total_recall_questions': total_questions,
                            'test_duration': test_duration,
                            'completed_timestamp': datetime.now().isoformat()
                        },
                        'user_feedback': st.session_state.get('user_feedback', ''),
                        'study_completed': True,
                    }
                    
                    if artwork_order_data:
                        final_data['artwork_order'] = artwork_order_data
                    final_data['generated_descriptions'] = st.session_state.get('generated_descriptions', {})
                    final_data['artwork_selected_interests'] = st.session_state.get('artwork_interests', {})
                    
                    try:
                        save_user_data(final_data)
                        st.session_state.data_saved = True
                        st.success("✅ I tuoi dati sono stati salvati con successo!")
                    except Exception as e:
                        st.error(f"Errore nel salvataggio dei dati: {e}")
                else:
                    st.info("ℹ️ I dati sono già stati salvati.")
                
                st.markdown("""
                <div class="success-box">
                <div style="font-size: 1.2rem; font-weight: bold; color: #856404; margin-bottom: 10px;"><strong>Studio Completato!</strong></div>
                <p>Grazie mille per aver partecipato a questo studio. I tuoi contributi sono preziosi per la nostra ricerca sull'apprendimento personalizzato nell'arte!</p>
                <p><strong>Verrete reindirizzati alla pagina iniziale!</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Termina Studio", type="primary", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.session_state.app_state = "welcome"
                    st.rerun()