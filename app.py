import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Carrega API Key
load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")
if not API_KEY:
    st.error("API Key não carregada! Verifica o .env")

# ---------------------------
# Funções auxiliares
# ---------------------------

def get_puuid(name, tag, region):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    resp = requests.get(url, headers={"X-Riot-Token": API_KEY})
    if resp.status_code == 200:
        return resp.json().get("puuid")
    return None

def get_matches(puuid, region, count=5):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    resp = requests.get(url, headers={"X-Riot-Token": API_KEY})
    if resp.status_code == 200:
        return resp.json()
    return []

def get_match_info(match_id, region):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    resp = requests.get(url, headers={"X-Riot-Token": API_KEY})
    if resp.status_code == 200:
        return resp.json()
    return None

# ---------------------------
# Inicialização do session_state
# ---------------------------

if "matches" not in st.session_state:
    st.session_state.matches = []
if "puuid" not in st.session_state:
    st.session_state.puuid = None

# ---------------------------
# Interface Streamlit
# ---------------------------

st.title("LoL Match Explorer")

summoner_name = st.text_input("Summoner Name")
summoner_tag = st.text_input("Tag")
region = st.selectbox("Region", ["europe", "americas", "asia"])
num_matches = st.slider("Número de últimos jogos", 1, 20, 5)

# ---------------------------
# Buscar Jogos
# ---------------------------

if st.button("Buscar Jogos"):
    puuid = get_puuid(summoner_name, summoner_tag, region)
    if not puuid:
        st.error("Não foi possível encontrar o jogador!")
        st.session_state.matches = []
        st.session_state.puuid = None
    else:
        st.session_state.puuid = puuid
        st.session_state.matches = get_matches(puuid, region, num_matches)

# ---------------------------
# Mostrar lista de jogos e detalhes
# ---------------------------

if st.session_state.matches:
    match_choice = st.selectbox("Escolhe um jogo", st.session_state.matches)
    match_info = get_match_info(match_choice, region)
    if match_info:
        participant = next((p for p in match_info["info"]["participants"] 
                            if p["puuid"] == st.session_state.puuid), None)
        if participant:
            st.subheader(f"Resumo do jogo {match_choice}")
            st.write(f"Campeão: {participant['championName']}")
            st.write(f"K/D/A: {participant['kills']}/{participant['deaths']}/{participant['assists']}")
            st.write(f"Venceu? {'Sim' if participant['win'] else 'Não'}")
            st.write(f"Duração do jogo: {match_info['info']['gameDuration']} segundos")
        else:
            st.error("Não foi possível encontrar informações do jogador neste jogo.")