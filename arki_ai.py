import streamlit as st
from google import genai
from google.genai import types

# --- TURVALLISET MÄÄRITYKSET ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API-avain puuttuu! Lisää 'GOOGLE_API_KEY' Streamlit Cloudin Secrets-asetuksiin.")
    st.stop()

# Pakota vakaa API-versio (v1) ja luo client
client = genai.Client(
    api_key=API_KEY,
    http_options={"api_version": "v1"},
)

# Valitse malli (vaihda tarvittaessa, esim. gemini-2.5-flash tms.)
MODEL_ID = "gemini-2.0-flash"

# Sovelluksen ulkoasu iPhonelle
st.set_page_config(page_title="Arki-AI", page_icon="🍲")
st.title("🍲 Arki-AI Chef (G3 Edition)")

# Pysyvät ohjeet AI:lle (system instruction)
SYSTEM_PROMPT = """
Olet suomalainen vegaani-kokki. Tehtäväsi on ehdottaa helppoja arkiruokia.
SÄÄNNÖT:
1. Käytä vain aineksia, joita saa tavallisesta suomalaisesta ruokakaupasta (S-market/K-market).
2. Reseptin tulee olla vegaaninen.
3. Pidä aineslista lyhyenä (max 7-8 ainesta).
4. Valmistusaika mieluiten alle 30 min.
5. Vastaa selkeästi: Reseptin nimi, ainekset ja lyhyet ohjeet.
""".strip()

GEN_CONFIG = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    max_output_tokens=500,
    temperature=0.7,
)

def generate_recipe(user_text: str) -> str:
    """Kutsu Geminiä turvallisesti ja palauta teksti."""
    resp = client.models.generate_content(
        model=MODEL_ID,
        contents=user_text,
        config=GEN_CONFIG,
    )
    return resp.text or ""

# --- KÄYTTÖLIITTYMÄ ---
tab1, tab2 = st.tabs(["#1 Vegeateria", "#2 Vegeateria aineksilla"])

with tab1:
    st.header("Päivän yllätys")
    if st.button("Ehdota jotain hyvää"):
        with st.spinner("Gemini laskee optimaalista reseptiä..."):
            try:
                text = generate_recipe("Ehdota yksi satunnainen, simppeli ja sesonkiin sopiva vegaaniateria.")
                st.success("Tässä ehdotus:")
                st.markdown(text)
            except Exception as e:
                st.error("Gemini-kutsu epäonnistui.")
                st.exception(e)

with tab2:
    st.header("Kokkaa kaapista")
    user_input = st.text_input(
        "Mitä aineksia käytetään?",
        placeholder="esim. tofu, kaurakerma, peruna",
    )

    if st.button("Luo resepti aineksista"):
        if user_input:
            with st.spinner("Gemini analysoi aineksiasi..."):
                try:
                    text = generate_recipe(f"Luo vegaaniresepti hyödyntäen näitä aineksia: {user_input}.")
                    st.success("Tässä resepti aineksillesi:")
                    st.markdown(text)
                except Exception as e:
                    st.error("Gemini-kutsu epäonnistui.")
                    st.exception(e)
        else:
            st.warning("Syötä ainekset ensin!")

st.divider()
st.caption("Intery Oy - Arki-AI v1.1 | Powered by Gemini")