from src.utilities.helpers import generate_uuid
from src.utilities.messages import messages


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


def _update_website(*args):
    url, unique_key, subscription = args
    if not subscription.websites[f'{unique_key}']:
        raise ValueError(messages['not_found'])
    subscription.websites[f'{unique_key}'][0].url = url
    subscription.commit()
    return subscription.websites[f'{unique_key}'][0]

def _delete_website(*args):
    unique_key, subscription = args[1], args[2]
    if not subscription.websites[f'{unique_key}']:
        raise ValueError(messages['not_found'])
    del subscription.websites[f'{unique_key}']
    return None

def _list_website(*args):
    subscription = args[2]
    websites = [site for site in subscription.websites.keys()]
    return websites