import streamlit as st
import time

def welcome_page():
    def load_css():
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    load_css()

    if st.session_state.get('consent_given', False):
        show_demographics_section()
    else:
        show_consent_section()

def show_consent_section():
    st.progress(25, text="Fase 1 di 4: Consenso informato")

    st.markdown('<div class="main-title">Studio sull\'Apprendimento dell\'Arte</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Benvenuto/a nel nostro studio di ricerca!</div>', unsafe_allow_html=True)

    st.markdown("""
    Stiamo studiando **come le persone apprendono e ricordano le opere d'arte** attraverso diverse tipologie di descrizioni.

    **Tempo stimato:** 25-30 minuti
    """)

    with st.container():
        st.markdown('<div class="section-header">Maggiori informazioni sullo studio</div>', unsafe_allow_html=True)
        st.markdown("""
        **Cosa farete:**
        - Compilare un breve questionario iniziale (8-10 min)
        - Visualizzare 3 opere d'arte con descrizioni (10-15 min)
        - Rispondere a domande sulle opere viste (5-10 min)
        
        **Condizioni sperimentali:**
        I partecipanti vengono assegnati casualmente a uno di due gruppi che vedranno descrizioni leggermente diverse.
        """)

    st.markdown("---")
    st.markdown('<div class="section-header">Consenso Informato</div>', unsafe_allow_html=True)

    consenso = st.checkbox("**Dichiaro di:**", key="consenso_checkbox")
    st.markdown("""
    - Aver letto e compreso le informazioni sullo studio
    - Essere maggiorenne (18+ anni)
    - Acconsentire volontariamente a partecipare
    - Comprendere che posso ritirarmi in qualsiasi momento senza conseguenze
    - Accettare che i dati anonimi siano utilizzati per scopi di ricerca
    """)

    if consenso:
        st.success("✅ Consenso registrato con successo!")
        
        if st.button("**Procedi alle Informazioni Demografiche**", type="primary", use_container_width=True):
            st.session_state.consent_given = True
            st.rerun()
    else:
        st.warning("⚠️ Devi dare il consenso per partecipare allo studio")

def show_demographics_section():
    st.progress(50, text="Fase 2 di 4: Informazioni demografiche")

    st.markdown('<div class="main-title">Informazioni Demografiche</div>', unsafe_allow_html=True)
    st.markdown("Per favore, fornisci alcune informazioni di base:")

    with st.form("demographic_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("**Età**", min_value=18, max_value=100, value=18)
            gender = st.selectbox("**Genere**", ["", "Femmina", "Maschio", "Altro", "Preferisco non dire"])
            education = st.selectbox("**Livello di istruzione**", [
                "", "Licenza media", "Diploma", "Laurea triennale", 
                "Laurea magistrale", "Dottorato/Master"
            ])
        
        with col2:
            art_familiarity = st.selectbox(
            "**Qual è la tua esperienza con l'arte?**",
            ["", 
            "Nessuna esperienza (non visito musei e non mi interesso di arte)",
            "Appassionato autodidatta (mi informo e visito mostre per interesse personale)",
            "Praticante amatoriale (disegno/dipingo per hobby)",
            "Ho una formazione tecnica (corsi specifici di disegno/pittura/scultura)",
            "Studio o ho studiato arte a livello universitario/accademico",
            "Lavoro professionalmente nel settore artistico"]
            )
            museum_visits = st.selectbox(
                "**Con quale frequenza visiti musei?**",
                ["", "Mai", "Raramente (1-2 volte/anno)", "Qualche volta (3-6 volte/anno)", "Spesso (più di 6 volte/anno)"]
            )
        
        demographics_complete = all([age >= 18, gender, education, art_familiarity, museum_visits])
        
        if st.form_submit_button("**Procedi alla Sezione Interessi**", type="primary", use_container_width=True):
            if demographics_complete:
                st.session_state.demographics = {
                    'age': age,
                    'gender': gender,
                    'education': education,
                    'art_familiarity': art_familiarity,
                    'museum_visits': museum_visits
                }
                st.session_state.app_state = "interests"
                st.rerun()
            else:
                st.warning("⚠️ Completa tutti i campi demografici per procedere")