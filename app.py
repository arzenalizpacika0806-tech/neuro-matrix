import streamlit as st
import json
import os
import plotly.graph_objects as go
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

# --- 3. NEURO-TÉRKÉP ALGORITMUS ---
def calculate_brain_stats(data):
    # Agyterületek pontszámainak kiszámítása
    pfc = 0       # Prefrontális kortex (Logika, Sakk, Python, PhD)
    temporal = 0  # Temporális lebeny (Zene, Akusztika)
    cerebellum = 0# Kisagy & Motoros (Finommotorika, Design, Gitár/Hegedű)
    parietal = 0  # Parietális (Térbeli, Asztrofizika, Kémia)

    for kat, skill_lista in data.items():
        for s in skill_lista:
            val = (s["lvl"] * 20) + s["xp"]
            name = s["nev"].lower()
            
            if "sakk" in name or "python" in name or "phd" in name or "hipotézis" in name:
                pfc += val
            if "hegedű" in name or "akusztika" in name or "hang" in name:
                temporal += val
            if "design" in name or "ruha" in name or "motor" in name:
                cerebellum += val
            if "astro" in name or "galaxis" in name or "kvantum" in name or "kémia" in name:
                parietal += val

    return {
        "Prefrontális Kortex (Logika/Stratégia)": min(pfc, 100),
        "Temporális Lebeny (Auditív/Akusztika)": min(temporal, 100),
        "Kisagy & Motoros Kortex (Koordináció)": min(cerebellum, 100),
        "Parietális Lebeny (Térbeli/Fizika)": min(parietal, 100)
    }

# --- 4. FEJLÉC & SIDEBAR ---
st.title("⚡ NEURO-MATRIX // KOGNITÍV CORE")
st.caption("v0.4 // Advanced Cortical Mapping System")
st.divider()

with st.sidebar:
    st.header("🔑 AI MAG BEÁLLÍTÁS")
    api_key = st.text_input("Gemini API Kulcs:", type="password")
    
    st.divider()
    st.header("🔮 TUDATI STATISZTIKÁK")
    for kategoria, skill_lista in skills_data.items():
        st.caption(f"--- {kategoria} ---")
        for skill in skill_lista:
            progress_val = min(skill["xp"] / 100.0, 1.0)
            st.progress(progress_val, text=f"{skill['nev']} (Lvl {skill['lvl']})")

# --- 5. FŐ LAPSZERKEZET ---
tab_chat, tab_brain = st.tabs(["💬 AI MENTOR", "🧠 NEURO-TOPOGRÁFIA"])

with tab_chat:
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
        uj_skill_nev = st.text_input("Új skill neve:", placeholder="Pl. Kvantum-Mérés")
        
        if st.button("Csomópont Injektálása"):
            if uj_skill_nev:
                uj_id = "node_" + str(len(skills_data[uj_kat]) + 1)
                skills_data[uj_kat].append({"id": uj_id, "nev": uj_skill_nev, "lvl": 1, "xp": 0})
                save_skills(skills_data)
                st.success("Csomópont mentve!")
                st.rerun()

    with col_right:
        st.subheader(f"💬 Mentor // {kivalasztott_skill}")
        user_input = st.text_input("Üzenet a Mentornak:", key="input")
        
        if st.button("Üzenet Küldése"):
            if not api_key:
                st.error("Add meg a Gemini API kulcsodat az oldalsávban!")
            elif user_input:
                client = genai.Client(api_key=api_key)
                prompt = f"Matrix AI Mentor vagy. Aktív csomópont: {kivalasztott_skill}. Kérdés: {user_input}"
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                st.markdown(f"**AI Professzor:**\n{response.text}")

with tab_brain:
    st.subheader("📊 Agyterületi Fejlettségi Profil (Cortical Radar)")
    
    brain_stats = calculate_brain_stats(skills_data)
    
    # Plotly Pókháló Diagram (Radar Chart)
    categories = list(brain_stats.keys())
    values = list(brain_stats.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(123, 44, 191, 0.4)',
        line=dict(color='#c77dff', width=2),
        name='Kognitív Profil'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#e0aaff"),
            angularaxis=dict(color="#e0aaff")
        ),
        paper_bgcolor="#0a0512",
        plot_bgcolor="#0a0512",
        font=dict(color="#e0aaff", family="Courier New"),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    > **Neuro-Metrika Megjegyzés:** Amikor új skilleket nyitsz meg vagy XP-t szerzel a Mátrixban, az agyterületi hálózat automatikusan újraszámolja a szinaptikus kapacitásodat.
    """)
