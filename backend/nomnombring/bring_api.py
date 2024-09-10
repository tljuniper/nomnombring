import requests
import json


class Bring:
    """
    Simple implementation of a few common interfaces of the Bring! API
    Also check out the node-bring-api for more info:
    https://github.com/foxriver76/node-bring-api
    """

    def __init__(self, email, password, key):
        self.mail = email
        self.password = password
        self.url = "https://api.getbring.com/rest/v2/"
        self.uuid = ""
        # These are the values used by the webapp for accessing the Bring! api
        self.headers = {
            "X-BRING-API-KEY": key,
            "X-BRING-CLIENT": "webApp",
            "X-BRING-CLIENT-SOURCE": "webApp",
            "X-BRING-COUNTRY": "DE",
        }
        self.session = None

    def login(self):
        """
        Login to the Bring! service using the credentials given in the constructor
        """
        payload = {"email": self.mail, "password": self.password}

        self.session = requests.Session()
        p = self.session.post(self.url + "bringauth", data=payload)
        if p.status_code != 200:
            raise Exception("Unable to login: " + str(p.content))

        data = json.loads(p.content.decode("utf-8"))

        self.name = data["name"]
        self.uuid = data["uuid"]
        self.bearerToken = data["access_token"]
        self.refreshToken = data["refresh_token"]

        self.headers["X-BRING-USER-UUID"] = self.uuid
        self.headers["Authorization"] = "Bearer " + self.bearerToken
        self.putHeaders = dict(self.headers)
        self.putHeaders[
            "Content-Type"
        ] = "application/x-www-form-urlencoded; charset=UTF-8"

    def close_session(self):
        """
        Close the user session
        """
        self.session.close()

    def get_lists(self):
        """
        Retrieve all lists of the logged in user
        @return: json string containing the lists

        Example of return:
        {
            "lists": [
                {
                    "listUuid": "00000000-0000-0000-0000-000000000000",
                    "name": "Home",
                    "theme": "ch.publisheria.bring.theme.home"
                }
            ]
        }
        """
        p = self.session.get(
            f"{self.url}bringusers/{self.uuid}/lists", headers=self.headers
        )
        if p.status_code != 200:
            raise Exception("Request failed: " + str(p.content))
        return json.loads(p.content.decode("utf-8"))

    # cSpell: disable
    def get_items(self, listUuid):
        """
            Retrieve all items in the given list
            @param listUuid: UUID of the list

            Example:
            {
            "purchase": [
                {
                    "name": "Abfalls\u00e4cke",
                    "specification": "Gelbe"
                },
                {
                    "name": "Salz",
                    "specification": ""
                }
            ],
            "recently": [
                {
                    "name": "Peperoni",
                    "specification": "3"
                }
            ],
            "status": "SHARED",
            "uuid": "00000000-0000-0000-0000-000000000000"
        }
        """
        # cSpell: enable
        p = self.session.get(f"{self.url}bringlists/{listUuid}", headers=self.headers)
        if p.status_code != 200:
            raise Exception("Request failed: " + str(p.content))
        return json.loads(p.content.decode("utf-8"))

    def add_item(self, item, specification, listUuid):
        """
        Add item with specification to given list
        @param item: Item to add to list
        @param specification: Description text for the item
        @param listUuid: UUID of the list to add this item to
        @return: None
        @raises Exception: If the response is not HTTP 200 or HTTP 204
        """
        print(f"Adding item '{item}' with specification '{specification}'.")
        body = f"&purchase={item}&recently=&specification={specification}&remove=&sender=null"
        body = bytearray(body, "utf-8")
        p = self.session.put(
            f"{self.url}bringlists/{listUuid}", headers=self.putHeaders, data=body
        )
        if p.status_code != 200 and p.status_code != 204:
            raise Exception("Request failed: " + str(p.content))

    def remove_item(self, item, specification, listUuid):
        """
        Remove item with specification from given list
        @param item: Item to remove from list
        @param specification: Description text for the item
        @param listUuid: UUID of the list
        @return: None
        @raises Exception: If the response is not HTTP 200 or HTTP 204
        """
        print(f"Removing item '{item}' with specification '{specification}'.")
        body = f"&purchase=&recently=&specification={specification}&remove={item}&sender=null"
        body = bytearray(body, "utf-8")
        p = self.session.put(
            f"{self.url}bringlists/{listUuid}", headers=self.putHeaders, data=body
        )
        if p.status_code != 200 and p.status_code != 204:
            raise Exception("Request failed: " + str(p.content))
