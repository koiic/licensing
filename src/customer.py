from collections import defaultdict
from datetime import datetime, timezone, timedelta

from src.utilities.messages import messages
from src.data import db
from src.utilities.helpers import check_site_limit, check_user_subscription
from src.website import Website


class Customer:
    """
        Customer class for all things relating to customer
    """
    website_count = 0
    websites = {}

    def __init__(self, name, password, email):
        """
        Constructure method for customer

        Parameters:
            name(str): The customer name
            password(str): the customer password
            email(str): the customer email address

        """
        self.name = name
        self.password = password
        self.email = email
        self.auth = False

    def __repr__(self):
        return f'<User {self.email}>'

    def commit(self):
        """
        Method to save user in datastructure
        :return: None
        """
        if self.email not in db['customers']:
            db['customers'][f'{self.email}'] = self
        else:
            raise ValueError(messages['already_exist'].format('Email'))

    def customer_authentication(self, password):
        """
        Method to authenticate customer.
        :param password: customer's password
        :return: auth
        """
        if password == self.password:
            self.auth = True
        else:
            raise ValueError(messages['invalid_credentials'])

    def subscribe(self, plan):
        """
        Method to enable customer to subscribe to a new plan
        :param plan: Plan object
        :return: A subscription object containing the Plan details
        """
        if self.auth:
            user_subscription = db['subscriptions'].get(self.email)
            if not user_subscription:
                new_subscription = CustomerSubscription(self, plan)
                new_subscription.commit()
                return new_subscription
            raise Exception(messages['sub_exist'])
        raise ValueError(messages['not_authenticated'])

    def update_plans(self, plan):
        """
           This method enable customers to update their plans.

        """

        if self.auth:
            user_subscription = db['subscriptions'].get(self.email)
            if not user_subscription:
                return self.subscribe(plan)
            user_subscription.plan = plan

    def add_new_website(self, url):
        """
        method to enable customer add new website
        :param url: website url
        :return: details of a new Website object
        """
        if self.auth:
            # import pdb; pdb.set_trace()
            user_subscription = check_user_subscription(self.email)
            website_allowed = user_subscription.plan.website_allowance
            check_site_limit(website_allowed, user_subscription.websites)
            new_website = Website(url, self)
            user_subscription.websites[f'{new_website.unique_key}'].append(new_website)
            user_subscription.commit()
            return new_website
        raise ValueError(messages['not_authenticated'])

    def manage_website(self, site_url=None, unique_key=None, action=None):
        """
        this method allow the user to manage their site
        :param site_url: website url
        :param unique_key: website unique identifier
        :param action: action to perform on site
        :return: website object
        """
        if self.auth:
            user_subscription = check_user_subscription(self.email)
            if action:
                if action == 'update':
                    if not user_subscription.websites[f'{unique_key}']:
                        raise ValueError(messages['not_found'])
                    user_subscription.websites[f'{unique_key}'][0].url = site_url
                    user_subscription.commit()
                    return user_subscription.websites[f'{unique_key}'][0]

                elif action == 'delete':
                    if not user_subscription.websites[f'{unique_key}']:
                        raise ValueError(messages['not_found'])
                    del user_subscription.websites[f'{unique_key}']
                    return None

                elif action == 'list':
                    websites = [site for site in user_subscription.websites.keys()]
                    return websites
            else:
                raise ValueError(messages('no_action'))
        else:
            raise ValueError(messages['not_authenticated'])


class CustomerSubscription:
    """
    Class for implementation of customer subscription
    """

    def __init__(self, customer, plan):
        """
        constructor mnethod for customer subscription
        :param user: customer  object
        :param plan: subscription plan
        """
        self.customer = customer
        self.plan = plan
        self.websites = defaultdict(list)
        self.created_date = datetime.now(timezone.utc)

    def __repr__(self):
        return f'<{self.plan} is your new subscription>'

    def commit(self):
        """
        Method for saving new customer subscription in the datastructure
        :return: None
        """
        db['subscriptions'][f'{self.customer.email}'] = self

    @property
    def get_sub_expiry_date(self):
        """
        Method to get subscription expired date
        :return: datetime
        """
        return self.created_date + timedelta(days=365)

    def get_sub_plan(self):
        """
        method to get subscription plan
        :return: Plan object
        """
        return self.plan
