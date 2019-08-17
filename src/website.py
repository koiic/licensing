from src.utilities.helpers import generate_uuid


class Website:
    def __init__(self, url, customer):
        """

        :rtype: object
        """
        self.url = url
        self.customer = customer
        self.unique_key = generate_uuid()

    def __repr__(self):
        return f'<this is {self.customer} website and the url is {self.url}>'

    def get_website(self, url):
        if self.url == url:
            return self
