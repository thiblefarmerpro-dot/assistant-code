import streamlit as st
import requests

st.set_page_config(page_title="Mon Assistant Code Qwen", page_icon="💻")

st.title("🚀 Mon Assistant Code (Qwen2.5-Coder)")
st.write("Posez vos questions de programmation ci-dessous :")

# Récupération de la clé API depuis les secrets sécurisés de Streamlit
api_key = st.secrets.get("OPENROUTER_API_KEY")

if not api_key:
    st.error("⚠️ La clé API OpenRouter n'est pas configurée dans les secrets.")
else:
    user_prompt = st.text_area("Votre question :", placeholder="Ex: Écris une fonction Python pour trier une liste...")

    if st.button("Générer le code"):
        if user_prompt:
            with st.spinner("L'IA réfléchit..."):
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "deepseek/deepseek-chat:free",

                    "messages": [
                        {"role": "user", "content": user_prompt}
                    ]
                }
                
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 200:
                    resultat = response.json()
                    reponse_ia = resultat["choices"][0]["message"]["content"]
                    
                    st.success("Réponse :")
                    st.markdown(reponse_ia)
                else:
                    st.error(f"Erreur de l'API : {response.status_code} - {response.text}")
        else:
            st.warning("Veuillez entrer une question.")
