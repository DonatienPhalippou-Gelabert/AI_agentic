import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from tools import convertir_devise  # Import de ton outil depuis tools.py

# 1. Charger les variables du fichier .env local
load_dotenv()

# Vérification de sécurité avant de lancer le script
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Erreur : La clé OPENAI_API_KEY est manquante dans le fichier .env")

# 2. Initialisation du modèle
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Liaison de l'outil au LLM
llm_with_tools = llm.bind_tools([convertir_devise])

# 4. Exécution de la première étape (La question)
query = "J'ai 50 euros, ça fait combien en dollars ?"
ai_msg = llm_with_tools.invoke(query)

# 5. La boucle de décision (Action)
if ai_msg.tool_calls:
    tool_call = ai_msg.tool_calls[0]
    nom_fonction = tool_call["name"]
    arguments = tool_call["args"]
    
    # Exécution locale de la fonction Python
    if nom_fonction == "convertir_devise":
        resultat_outil = convertir_devise(**arguments)
        
        # Création du message de retour pour l'IA
        tool_message = ToolMessage(
            content=str(resultat_outil),
            tool_call_id=tool_call["id"]
        )
        
        # 6. Réponse finale de l'IA avec toutes les informations
        reponse_finale = llm_with_tools.invoke([
            ("user", query), 
            ai_msg, 
            tool_message
        ])
        
        print("\nRéponse de l'agent :")
        print(reponse_finale.content)
else:
    # Si le LLM décide qu'il n'a pas besoin d'outil pour répondre
    print("\nRéponse directe :")
    print(ai_msg.content)