# cython: language_level=3


def format_url(url):
    # Déterminer si un protocole est déjà spécifié dans l'URL
    if url.startswith("http://"):
        original_protocol = "http"
        url = url[len("http://") :]
    elif url.startswith("https://"):
        original_protocol = "https"
        url = url[len("https://") :]
    else:
        # Utiliser "http" par défaut si aucun protocole n'est spécifié
        original_protocol = "http"

    # Diviser l'URL pour vérifier le numéro de port
    url_parts = url.split(":")
    if len(url_parts) == 2:
        port = url_parts[1]
        if port == "80":
            return f"http://{url_parts[0]}"
        elif port == "443":
            return f"https://{url_parts[0]}"
        else:
            # Conserver le port spécifié dans l'URL
            return f"{original_protocol}://{url}"
    else:
        # Utiliser le protocole original si aucun port n'est spécifié
        return f"{original_protocol}://{url}"
