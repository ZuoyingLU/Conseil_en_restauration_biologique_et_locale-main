#!/usr/bin/env python3
import requests #import installed requests module
from requests.exceptions import HTTPError #import requests exceptions
from requests.compat import urljoin #could be usefull to create url…

class Client:
    def __init__(self, baseUrl, defaultProtocol="http"):
        self.set_baseurl(baseUrl) #nom de domaine / Domain name
        self.__defaultProtocol__ = defaultProtocol #Request protocol if not specified
        self.__r__ = None #Server response
        self.__error__ = None #errors

    #Changes the base url
    def set_baseurl(self, baseUrl):
        self.__baseUrl__ = baseUrl

    #Creates a url out of a Client object, a route and a protocol
    def make_url(self, route=None, protocol=None):
        if protocol == None:
            protocol = self.__defaultProtocol__
        res = urljoin(f"{protocol}://{self.__baseUrl__}", route)
        return res

    #issues an http get request
    def get(self, route, protocol=None):
        res = True
        try :
            # Stores in __r__ the response to the query
            self.__r__ = requests.get(self.make_url(route, protocol))
            # Deletes the last error (if an error is raised this is not executed)
            self.__error__ = None
        #possible errors
        except HTTPError as http_err:
            self.__error__ = f'HTTP error occurred: {http_err}'
            self.__r__ = None
            res = False
        except Exception as err:
            self.__error__ = f'Other error occurred: {err}'
            self.__r__ = None
            res = False
        return res

    #returns the last response to a succesful query
    def lr(self):
        return self.__r__

    #returns the last error raised by a query
    def lr_error(self):
        return self.__error__

    def lr_url(self):
        res = None
        if self.__r__ != None:
            res = self.__r__
        return res

    def lr_status_code(self):
        res = self.__r__.status_code
        return res

    def lr_headers(self):
        res = self.__r__.headers
        return res

    def lr_response(self):
        res = self.__r__.text
        return res

    def lr_redirections(self):
        # redirections = []
        # for response in self.__r__.history:
        #     redirection_details = {
        #         'url': response.url,
        #         'status_code': response.status_code
        #     }
        # redirections.append(redirection_details)
        # return redirections
        return self.__r__.history
    # issues an http get request
    def post (self , route , data =None , protocol = None ):
        res = True
        try :
        # Stores in __r__ the response to the query
            if data == None :
                self . __r__ = r. post ( self . make_url (route , protocol ))
            else :
                self . __r__ = r. post ( self . make_url (route , protocol ) , json = json .dumps ( data ))
    # Deletes the last error (if an error is raised this is not executed )
            self . __error__ = None
    # possible errors
        except HTTPError as http_err :
            self . __error__ = f'HTTP error occurred : { http_err }'
            self . __r__ = None
            res = False
        except Exception as err:
            self . __error__ = f'Other error occurred : { err }'
            self . __r__ = None
            res = False
            return res
    # issues an http get request
    def delete (self , route , protocol = None ) :
        res = True
        try :
    # Stores in __r__ the response to the query
            self . __r__ = r. delete ( self . make_url (route , protocol ))
            # Deletes the last error (if an error is raised this is not executed )
            self . __error__ = None
    # possible errors
        except HTTPError as http_err :
            elf . __error__ = f'HTTP error occurred : { http_err }'
            self . __r__ = None
            res = False
        except Exception as err:
            self . __error__ = f'Other error occurred : { err }'
            self . __r__ = None
            res = False
        return res

if __name__ == "__main__":
    # base_url, route, protocol = ("sid.lezinter.net","", "https") #test1
    # base_url, route, protocol = ("sid.lezinterrr.net","", "http") #test2
    base_url, route, protocol = ("sid.lezinter.net","", "http") #test3
    # base_url, route, protocol = ("luciole.lezinter.net", "index.html", "https") #test4
    c = Client(base_url)
    url = c.make_url(route, protocol)
    print("### test de make_url")
    c.set_baseurl(f"{base_url}/")
    print(url, "ok" if route == "" or url==c.make_url(f"/{route}", protocol) else "votre fonction peut planter, suivre l'énoncé")
    # print(c.get(route, protocol))
    # print(c.lr_status_code())
    if c.get(route, protocol) and c.lr_status_code() == 200:
        print(c.lr())
        print(f"###    url de la requête : {c.lr_url()}")
        print(f"### statut de la requête : {c.lr_status_code()}")
        print(f"### en-têtes complets :\n{c.lr_headers()}")
        print(f"### type contenu de la page : {c.lr_headers()['Content-Type']}")
        print(f"### contenu de la page :\n{c.lr_response()}")
        for redir in c.lr_redirections():
            print(f"{redir}")
    ## Agence Bio
    #TODO 12

