import royalnet.utils as ru
import royalnet.constellation.api as rca
import royalnet.constellation.api.apierrors as rcae


# Le docs autogenerate sono disponibili al percorso `/docs` a server avviato


class EchoStar(rca.ApiStar):
    # Una breve frase che spieghi cosa faccia il metodo, compare nelle docs autogenerate
    summary = "Un metodo di esempio per far vedere come si fanno pagine API con Constellation."

    # Opzionalmente, una descrizione aggiuntiva che spieghi cosa fa il metodo
    description = """Blah blah blah, blah blah blah?"""

    # I metodi HTTP che possono essere usati per eseguire il metodo
    methods = ["GET", "POST"]
    # È possibile disambiguare tra i vari metodi con `data.method`

    # Il path HTTP da usare per chiamare il metodo
    path = "/api/example/echo/v1"

    # Se il metodo richiede o no autenticazione
    # Solo a fini di documentazione, non fa realmente alcun controllo di suo
    requires_auth = True
    # Per ottenere l'utente che ha fatto la richiesta all'API, usa `await data.user()`
    # Se l'utente non è loggato, restituisce automaticamente 403 Forbidden, a meno che l'eccezione
    # `rcae.ForbiddenError` non venga catturata

    # Parametri che possono essere passati al metodo, con una breve descrizione di cosa dovrebbero essere
    parameters = {
        "echo": "La frase che deve restituire il metodo. "
                "(Opzionale: Se non viene passata, questa funzione restituirà il nome dell'utente che l'ha chiamata.)",
        "error": "Se il metodo deve restituire un errore di esempio."
    }
    # I parametri sono accessibili a `data[nomeparametro]` (ad esempio, `data["echo"]`)
    # Tutti i parametri passati saranno stringhe
    # Parametri richiesti, ma non passati causeranno un `rcae.MissingParameterError`
    # che porterà a un errore 400 Bad Request

    # Le categorie sotto le quali inserire questo metodo nella documentazione autogenerata
    tags = ["example"]

    # Quello che deve fare effettivamente il metodo
    # Deve restituire un oggetto di tipo JSON, ovvero una stringa, un intero, un float, una lista, un dict oppure None
    async def api(self, data: rca.ApiData) -> ru.JSON:

        # Se il parametro errore passato è true...
        if data["error"] == "true":
            # Restituisci un fallimento con errore di esempio
            raise Exception("Errore di esempio! E' tutto ok!")
        # Se il parametro "error" non viene passato, l'utente riceverà un 400 Bad Request

        # Assicuriamoci che l'utente sia loggato
        user = await data.user()
        # Assicuriamoci che l'utente abbia il ruolo "admin"
        if "admin" not in user.roles:
            raise Exception("Salve Smilzo! Lei non è admin!")

        # `data` è un normalissimo dict (con qualche attributo extra)
        # Posso usare il metodo `.get()` dei dict per provare a ottenere un valore e restituire None se esso non esiste
        echo = data.get("echo")

        if echo is None:
            # Prendiamo il nome utente dell'utente loggato
            # user è un normalissimo oggetto SQLAlchemy della tabella Users definita in `royalnet.backpack.tables.users`
            # che è esattamente uguale a quella che avevi progettato tu
            echo = user.username

        # Restituiamo 200 OK e la frase "riecheggiata" assieme ad esso
        return {"echo": echo, "method_used": data.method}

# Una volta scritto il codice, il metodo va importato e aggiunto alla lista
# `available_page_stars` del file `__init__.py`
