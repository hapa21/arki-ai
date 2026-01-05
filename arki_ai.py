import streamlit as st
import google.generativeai as genai

# --- TURVALLISET MÄÄRITYKSET ---
# Haetaan API-avain Streamlitin omista asetuksista (Secrets), 
# jotta se ei päädy GitHubiin muiden nähtäväksi.
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API-avain puuttuu! Lisää 'GOOGLE_API_KEY' Streamlit Cloudin Secrets-asetuksiin.")
    st.stop()

genai.configure(api_key=API_KEY)

# Käytetään uutta julkaistua mallia
model = genai.GenerativeModel('gemini-1.5-flash')

# Sovelluksen ulkoasu iPhonelle
st.set_page_config(page_title="Arki-AI", page_icon="🍲")
st.title("🍲 Arki-AI Chef (G3 Edition)")

# Pysyvät ohjeet AI:lle
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

with tab1:
    st.header("Päivän yllätys")
    if st.button("Ehdota jotain hyvää"):
        with st.spinner('Gemini 3 laskee optimaalista reseptiä...'):
            prompt = SYSTEM_PROMPT + "\nEhdota yksi satunnainen, simppeli ja sesonkiin sopiva vegaaniateria."
            response = model.generate_content(prompt)
            st.success("Tässä ehdotus:")
            st.markdown(response.text)

with tab2:
    st.header("Kokkaa kaapista")
    user_input = st.text_input("Mitä aineksia käytetään?", placeholder="esim. tofu, kaurakerma, peruna")
    
    if st.button("Luo resepti aineksista"):
        if user_input:
            with st.spinner('Gemini 3 analysoi aineksiasi...'):
                prompt = SYSTEM_PROMPT + f"\nLuo vegaaniresepti hyödyntäen näitä aineksia: {user_input}."
                response = model.generate_content(prompt)
                st.success("Tässä resepti aineksillesi:")
                st.markdown(response.text)
        else:
            st.warning("Syötä ainekset ensin!")

st.divider()
st.caption("Intery Oy - Arki-AI v1.1 | Powered by Gemini 3")