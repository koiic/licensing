class Plan:
    def __init__(self, name, website_allowance, price):
        self.name = name
        self.website_allowance = website_allowance
        self.price = price

    def printPlan(self):
        print(f'{self.plan_name}, {self.price}, {self.website_allowance}')

    def __repr__(self):
        return f'< {self.name} plan, {self.website_allowance} website>'


class SinglePlan(Plan):

    def __init__(self, name='Single', website_allowance=1, price=49):
        # call super() function
        super().__init__(name, website_allowance, price)


class PlusPlan(Plan):

    def __init__(self, name='Plus', website_allowance=3, price=99):
        # call super() function
        super().__init__(name, website_allowance, price)


class InfinitePlan(Plan):

    def __init__(self, name='Infinite', website_allowance='unlimited', price=249):
        # call super() function
        super().__init__(name, website_allowance, price)
