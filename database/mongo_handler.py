import streamlit as st
from pymongo import MongoClient
import datetime
import random
import string
import urllib.parse

@st.cache_resource(show_spinner=False)
def get_mongo_connection():
    try:
        connection_string = st.secrets["mongodb"]["connection_string"]
        
        # Log di debug (senza password)
        st.write(f"🔍 Connessione a MongoDB...")
        
        client = MongoClient(connection_string, 
                           serverSelectionTimeoutMS=10000,
                           connectTimeoutMS=10000,
                           socketTimeoutMS=10000)
        
        # Test connessione
        client.admin.command('ping')
        st.success("✅ Connessione MongoDB stabilita con successo!")
        
        return client
        
    except Exception as e:
        st.error(f"❌ Errore connessione MongoDB: {str(e)}")
        st.info("ℹ️ Verifica:")
        st.info("1. Le secrets in .streamlit/secrets.toml")
        st.info("2. La stringa di connessione di MongoDB Atlas")
        st.info("3. L'accesso alla rete (IP whitelist)")
        return None

def generate_participant_id():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"P_{timestamp}_{random_part}"

def save_user_data(user_data):
    try:
        client = get_mongo_connection()
        if not client:
            st.error("⚠️ Impossibile connettersi al database")
            return False, None
            
        db = client[st.secrets["mongodb"]["database_name"]]
        collection = db["participants"]
        
        user_data["created_at"] = datetime.datetime.now()
        
        if "participant_id" not in user_data:
            user_data["participant_id"] = generate_participant_id()
        
        # Log dei dati da salvare (senza informazioni sensibili)
        st.write(f"💾 Salvando dati per partecipante: {user_data['participant_id']}")
        
        result = collection.insert_one(user_data)
        
        st.success(f"✅ Dati salvati con ID: {result.inserted_id}")
        return True, user_data["participant_id"]
        
    except Exception as e:
        st.error(f"❌ Errore salvataggio MongoDB: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return False, None