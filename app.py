import streamlit as st
import requests

st.set_page_config(page_title="Mon Assistant Code", page_icon="💻")

st.title("🚀 Mon Assistant Code (avec Historique)")
st.write("Posez vos questions de programmation ci-dessous :")

api_key = st.secrets.get("OPENROUTER_API_KEY")

if not api_key:
    st.error("⚠️ La clé API OpenRouter n'est pas configurée dans les secrets.")
else:
    # 1. Initialiser l'historique des messages s'il n'existe pas
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. Afficher l'historique des messages précédents
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Zone de saisie du chat (remplace text_area par chat_input pour un effet type ChatGPT)
    if user_prompt := st.chat_input("Écris ta question ici (ex: script Roblox, Python...) :"):
        
        # Ajouter le message de l'utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Générer la réponse de l'IA
        with st.chat_message("assistant"):
            with st.spinner("L'IA réfléchit..."):
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                # On envoie tout l'historique pour que l'IA ait du contexte
                data = {
                    "model": "openrouter/free",
                    "messages": st.session_state.messages
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    resultat = response.json()
                    reponse_ia = resultat["choices"][0]["message"]["content"]
                    
                    st.markdown(reponse_ia)
                    # Ajouter la réponse de l'assistant à l'historique
                    st.session_state.messages.append({"role": "assistant", "content": reponse_ia})
                else:
                    st.error(f"Erreur de l'API : {response.status_code} - {response.text}")
