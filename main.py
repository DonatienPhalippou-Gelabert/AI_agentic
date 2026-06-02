import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from tools import convertir_devise, sauvegarder_texte  # Import de ton outil depuis tools.py

# 1. Charger les variables du fichier .env local
load_dotenv()

# Vérification de sécurité avant de lancer le script
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Erreur : La clé OPENAI_API_KEY est manquante dans le fichier .env")

# 2. Initialisation du modèle
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Liaison de l'outil au LLM
llm_with_tools = llm.bind_tools([convertir_devise, sauvegarder_texte])

# La requête demande explicitement deux actions successives
query = "Convertis 150 euros en yens et sauvegarde le résultat dans un fichier nommé rapport.txt"

# Liste pour conserver l'historique de la conversation 
messages = [("user", query)]

# Dictionnaire des fonctions pour l'exécution dynamique
fonctions_disponibles = {
    "convertir_devise": convertir_devise,
    "sauvegarder_texte": sauvegarder_texte
}

# Limite de sécurité pour éviter une boucle infinie si l'IA s'emballe
max_iterations = 5
iteration = 0

print("Lancement de l'agent...")

while iteration < max_iterations:
    iteration += 1
    
    # On envoie tout l'historique au LLM
    ai_msg = llm_with_tools.invoke(messages)
    # On ajoute la réflexion actuelle du LLM à l'historique
    messages.append(ai_msg)
    
    # Si le LLM demande l'exécution d'un ou plusieurs outils
    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            nom_fonction = tool_call["name"]
            arguments = tool_call["args"]
            
            print(f"\n[Étape {iteration}] L'IA fait appel à l'outil : {nom_fonction}")
            print(f"Arguments reçus : {arguments}")
            
            if nom_fonction in fonctions_disponibles:
                # Exécution de la fonction Python
                resultat_outil = fonctions_disponibles[nom_fonction](**arguments)
                print(f"Résultat de l'outil : {resultat_outil}")
                
                # On formalise le résultat sous forme de ToolMessage
                tool_message = ToolMessage(
                    content=str(resultat_outil),
                    tool_call_id=tool_call["id"]
                )
                # On ajoute ce résultat à l'historique pour que le LLM le lise au prochain tour
                messages.append(tool_message)
    else:
        # Si le LLM n'appelle plus d'outils, c'est qu'il a fini son travail
        print("\nRéponse finale de l'agent :")
        print(ai_msg.content)
        break