from src.data import db
from src.customer import Customer
from src.plan import SinglePlan, PlusPlan, InfinitePlan
from src.utilities.messages import messages


def customer_registration(name, password, email):
    check_user_exist(email)
    new_customer = Customer(name, password, email)
    new_customer.commit()
    return new_customer


def check_user_exist(email):
    if email in db['customers']:
        raise ValueError(messages['already_exist'].format('Email'))


def sign_in_customer(email, password):
    if email not in db['customers']:
        raise ValueError(messages['invalid_credentials'])
    customer = db['customers'].get(str(email))
    customer.customer_authentication(password)
    return customer
