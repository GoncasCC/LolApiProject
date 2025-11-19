import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")

def get_puuid(name, tag, region):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json().get("puuid") if r.status_code == 200 else None

def get_matches(puuid, region, count=5):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json() if r.status_code == 200 else []

def get_match_info(match_id, region):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json() if r.status_code == 200 else None

def champ_icon(champ):
    return f"https://ddragon.leagueoflegends.com/cdn/14.24.1/img/champion/{champ}.png"

# Estado global
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

st.title("LoL Match Explorer")

summoner_name = st.text_input("Summoner Name")
summoner_tag = st.text_input("Tag")
region = st.selectbox("Region", ["europe", "americas", "asia"])
count = st.slider("Games", 1, 20, 5)

if st.button("Search"):
    puuid = get_puuid(summoner_name, summoner_tag, region)

    if not puuid:
        st.error("Player not found")
    else:
        matches = get_matches(puuid, region, count)
        st.session_state.matches = matches
        st.session_state.puuid = puuid

# Mostrar lista
if "matches" in st.session_state:
    for m in st.session_state.matches:
        match = get_match_info(m, region)
        if not match:
            continue

        p = next(x for x in match["info"]["participants"]
                 if x["puuid"] == st.session_state.puuid)

        col1, col2 = st.columns([1, 4])

        with col1:
            st.image(champ_icon(p["championName"]), width=64)

        with col2:
            st.write(f"**{p['championName']}** — {p['kills']}/{p['deaths']}/{p['assists']}")
            if st.button(f"Ver detalhes ({m})"):
                st.session_state.selected_match = m
                st.switch_page("pages/jogo_detalhes.py")