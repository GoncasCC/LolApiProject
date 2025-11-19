import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")

def get_match_info(match_id, region):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json() if r.status_code == 200 else None

def champ_icon(champ):
    return f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{champ}.png"

# Certificar que há match selecionado
if "selected_match" not in st.session_state or st.session_state.selected_match is None:
    st.error("Nenhum jogo selecionado.")
    st.stop()

match_id = st.session_state.selected_match
region = st.session_state.get("region", "europe")

match_info = get_match_info(match_id, region)
participants = match_info["info"]["participants"]

st.title(f"Detalhes do jogo {match_id}")

# Ordenar por roles
role_order = ["Top", "Jungle", "Mid", "Adc", "Support"]

def role_sort_key(p):
    try:
        return role_order.index(p["teamPosition"])
    except:
        return 99  # fallback

# Dividir equipas
blue = sorted([p for p in participants if p["teamId"] == 100], key=role_sort_key)
red  = sorted([p for p in participants if p["teamId"] == 200], key=role_sort_key)

col_blue, col_red = st.columns(2)

# ===========================
#       BLUE TEAM
# ===========================
with col_blue:
    st.header("🔵 BLUE TEAM")
    for p in blue:
        c1, c2 = st.columns([1, 4])

        with c1:
            st.image(champ_icon(p["championName"]), width=64)

        with c2:
            st.write(f"### {p['riotIdGameName']}")
            st.write(f"**{p['championName']}** — {p['kills']}/{p['deaths']}/{p['assists']}")
            st.write(f"Role: {p['teamPosition']}")
            st.write(f"{'🟢 Victory' if p['win'] else '🔴 Defeat'}")
            st.write("---")


# ===========================
#       RED TEAM
# ===========================
with col_red:
    st.header("🔴 RED TEAM")
    for p in red:
        c1, c2 = st.columns([1, 4])

        with c1:
            st.image(champ_icon(p["championName"]), width=64)

        with c2:
            st.write(f"### {p['riotIdGameName']}")
            st.write(f"**{p['championName']}** — {p['kills']}/{p['deaths']}/{p['assists']}")
            st.write(f"Role: {p['teamPosition']}")
            st.write(f"{'🟢 Victory' if p['win'] else '🔴 Defeat'}")
            st.write("---")

# Botão voltar
if st.button("⬅️ Back"):
    st.switch_page("app.py")