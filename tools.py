def convertir_devise(montant: float, devise_cible: str) -> str:
    """
    Convertit un montant de l'Euro (EUR) vers une autre devise (USD, GBP, JPY).
    """
    taux = {
        "USD": 1.08,
        "GBP": 0.85,
        "JPY": 162.50
    }
    
    devise_cible = devise_cible.upper()
    if devise_cible not in taux:
        return f"Désolé, la devise {devise_cible} n'est pas supportée."
        
    resultat = montant * taux[devise_cible]
    return f"{montant} EUR valent {resultat:.2f} {devise_cible}"

def sauvegarder_texte(contenu: str, nom_fichier: str) -> str:
    """
    Sauvegarde un texte ou un résultat important dans un fichier .txt local.
    Le nom du fichier doit se terminer par '.txt'."""
    # Sécurité pour s'assurer que l'extension est correcte
    if not nom_fichier.endswith('.txt'):
        nom_fichier += '.txt'
        
    try:
        with open(nom_fichier, "w", encoding="utf-8") as f:
            f.write(contenu)
        return f"Succès : Le contenu a bien été sauvegardé dans le fichier '{nom_fichier}'."
    except Exception as e:
        return f"Erreur lors de l'écriture du fichier : {str(e)}"