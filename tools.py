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