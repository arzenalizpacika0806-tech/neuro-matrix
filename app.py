import streamlit as st
import json
import os
from google import genai

# --- 1. OLDAL BEÁLLÍTÁSA ÉS FEKETE-LILA MÁTRIX STÍLUS ---
st.set_page_config(page_title="NEURO-MATRIX", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0a0512;
        color: #e0aaff;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        color: #c77dff;
        background-color: #190a28;
        border: 1px solid #7b2cbf;
        font-family: 'Courier New', Courier, monospace;
        border-radius: 6px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #7b2cbf;
        color: #ffffff;
        border-color: #c77dff;
    }
    h1, h2, h3 {
        color: #c77dff !important;
        font-family: 'Courier New', Courier, monospace;
    }
    [data-testid="stSidebar"] {
        background-color: #10061e;
        border-right: 1px solid #3c096c;
    }
    .stTextInput>div>div>input {
        background-color: #190a28;
        color: #e0aaff;
        border: 1px solid #5a189a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADATBÁZIS KEZELŐ ---
DATA_FILE = "skills.json"

def load_skills():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "Stratégia & Logika": [{"id": "sakk_01", "nev": "♟️ Sakk Megnyitások & Játékelmélet", "lvl": 2, "xp": 35}],
            "Akusztika & Művészet": [{"id": "hegedu_01", "nev": "🎻 Hegedű & Akusztika", "lvl": 4, "xp": 60}],
            "Tudomány & Archívum": [{"id": "gateway_01", "nev": "⚛️ Gateway Process & Kogníció", "lvl": 1, "xp": 20}]
        }

def save_skills(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

skills_data = load_skills()

# --- 3. FEJLÉC & OLDALSÁV ---
st.title("⚡ NEURO-MATRIX // KOGNITÍV CORE")
st.caption("Alaprendszer Architektúra v0.3 // Active AI Core")

st.divider()

with st.sidebar:
    st.header("🔑 AI MAG BEÁLLÍTÁS")
    api_key = st.text_input("Gemini API Kulcs:", type="password", placeholder="Itt add meg az API kulcsot...")
    
    st.divider()
    st.header("🔮 TUDATI STATISZTIKÁK")
    st.write("**Felhasználó:** ARCHITECT")
    st.divider()
    
    st.subheader("Aktív Készségfák")
    for kategoria, skill_lista in skills_data.items():
        st.caption(f"--- {kategoria} ---")
        for skill in skill_lista:
            progress_val = min(skill["xp"] / 100.0, 1.0)
            st.progress(progress_val, text=f"{skill['nev']} (Lvl {skill['lvl']})")

# --- 4. FŐ INTERFÉSZ ---
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("🎯 Csomópont Választó")
    
    kategoria_lista = list(skills_data.keys())
    kivalasztott_kat = st.selectbox("Válassz Kategóriát:", kategoria_lista)
    
    elrheto_skillek = [s["nev"] for s in skills_data[kivalasztott_kat]]
    kivalasztott_skill = st.selectbox("Válassz Aktív Csomópontot:", elrheto_skillek)
    
    st.divider()
    
    st.subheader("➕ Új Csomópont Nyitása")
    uj_kat = st.selectbox("Melyik kategóriába kerüljön?", kategoria_lista, key="new_kat")
    uj_skill_nev = st.text_input("Új skill / csomópont neve:", placeholder="Pl. ⚡ Kvantum-Elektrodinamika")
    
    if st.button("Csomópont Injektálása a Mátrixba"):
        if uj_skill_nev:
            uj_id = "node_" + str(len(skills_data[uj_kat]) + 1)
            uj_elem = {"id": uj_id, "nev": uj_skill_nev, "lvl": 1, "xp": 0}
            
            skills_data[uj_kat].append(uj_elem)
            save_skills(skills_data)
            st.success(f"Csomópont hozzáadva: {uj_skill_nev}")
            st.rerun()
        else:
            st.warning("Adj meg egy nevet az új skillnek!")

with col_right:
    st.subheader(f"💬 AI Mentor // {kivalasztott_skill}")
    
    user_input = st.text_input("Üzenet a Mentornak:", key="input", placeholder="Pl. Magyarázd el a fizikai hátteret...")
    
    if st.button("Üzenet Küldése"):
        if not api_key:
            st.error("Kérlek, add meg a Gemini API kulcsodat a bal oldalsávban!")
        elif not user_input:
            st.warning("Írj be egy kérdést!")
        else:
            st.markdown(f"**Te:** {user_input}")
            
            try:
                # Gemini API hívása
                client = genai.Client(api_key=api_key)
                
                system_instruction = f"""
                Egy Mátrix-stílusú, szigorú és magasan kvalifikált tudományos AI Mentor vagy.
                A jelenlegi aktív csomópont, amiben a felhasználóval dolgoztok: {kivalasztott_skill}.
                Válaszolj mély tudományos alapossággal, precíz fizikai/matematikai/logikai háttérrel, cyber/mátrix hangvételben.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"{system_instruction}\n\nFelhasználó kérdése: {user_input}"
                )
                
                st.markdown(f"**AI Professzor:**\n{response.text}")
                
            except Exception as e:
                st.error(f"Hiba történt az API hívás során: {e}")
