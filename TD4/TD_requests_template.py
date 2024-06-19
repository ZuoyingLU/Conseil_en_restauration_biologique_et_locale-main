#!/usr/bin/env python3
import requests #import installed requests module
from requests.exceptions import HTTPError #import requests exceptions
from requests.exceptions import JSONDecodeError #import requests exceptions
from requests.compat import urljoin #could be usefull to create url…

#Creates a url out of a Client object, a route and a protocol
def make_url(base_url, route = None, protocol="http"):
    res = urljoin(f"{protocol}://{base_url}", route)
    return res

if __name__ == "__main__":
    base_url, route, protocol = ("sid.lezinter.net","", "https") #test1
    # base_url, route, protocol = ("sid.lezinterrr.net","", "http") #test2
    # base_url, route, protocol = ("sid.lezinter.net","", "http") #test3
    # base_url, route, protocol = ("luciole.lezinter.net", "index.html", "https") #test4
    url = make_url(base_url, route, protocol)
    print("### test de make_url")
    print(url, "ok" if route == "" or url==make_url(f"{base_url}/", f"/{route}", protocol) else "votre fonction peut planter, suivre l'énoncé")
    try :
        resp = requests.get(url)
        if True:#TODO Q5 == 200:
            print(f"###    url de la requête : {'TODO Q4'}")
            print(f"### statut de la requête : {'TODO Q5'}")
            #mettre les en-têtes dans h
            h = "TODO Q6"
            print(f"### en-têtes complets :\n{h}")
            print("### type de contenu de la page :")
            print("TODO Q7")
            print("### contenu de la page :")
            print("TODO Q8")
            print("### historique des redirections")
            for redir in 'TODO Q9':
                "TODO Q9"
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    ## Agence Bio
    #TODO 12
