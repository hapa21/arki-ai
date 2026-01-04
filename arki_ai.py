import streamlit as st
import google.generativeai as genai

# --- MÄÄRITYKSET ---
# Syötä aiemmasta projektistasi tuttu API-avain tähän
API_KEY = "AIzaSyAxwY7S_3YedMvbtGRGSXu4mGte8NhWteI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash')

# Sovelluksen ulkoasu iPhonelle
st.set_page_config(page_title="Arki-AI", page_icon="🍲")
st.title("🍲 Arki-AI Chef")

# Pysyvät ohjeet AI:lle (System Instructions)
SYSTEM_PROMPT = """
Olet suomalainen vegaani-kokki. Tehtäväsi on ehdottaa helppoja arkiruokia.
SÄÄNNÖT:
1. Käytä vain aineksia, joita saa tavallisesta suomalaisesta ruokakaupasta (S-market/K-market).
2. Reseptin tulee olla vegaaninen.
3. Pidä aineslista lyhyenä (max 7-8 ainesta).
4. Valmistusaika mieluiten alle 30 min.
5. Vastaa selkeästi: Reseptin nimi, ainekset ja lyhyet ohjeet.
"""

# --- KÄYTTÖLIITTYMÄ ---
tab1, tab2 = st.tabs(["#1 Vegeateria", "#2 Vegeateria aineksilla"])

# VAIHTOEHTO #1: Täysi yllätys
with tab1:
    st.header("Päivän yllätys")
    if st.button("Ehdota jotain hyvää"):
        with st.spinner('AI-kokki miettii...'):
            prompt = SYSTEM_PROMPT + "\nEhdota yksi satunnainen, simppeli ja sesonkiin sopiva vegaaniateria."
            response = model.generate_content(prompt)
            st.success("Tässä ehdotus:")
            st.markdown(response.text)

# VAIHTOEHTO #2: Aineksilla rajoitettu
with tab2:
    st.header("Kokkaa kaapista")
    user_input = st.text_input("Mitä aineksia käytetään?", placeholder="esim. tofu, kaurakerma, peruna")
    
    if st.button("Luo resepti aineksista"):
        if user_input:
            with st.spinner('Suunnitellaan...'):
                prompt = SYSTEM_PROMPT + f"\nLuo vegaaniresepti hyödyntäen näitä aineksia: {user_input}."
                response = model.generate_content(prompt)
                st.success("Tässä resepti aineksillesi:")
                st.markdown(response.text)
        else:
            st.warning("Syötä ainekset ensin!")

st.divider()
st.caption("Intery Oy - Arki-AI v1.0")
