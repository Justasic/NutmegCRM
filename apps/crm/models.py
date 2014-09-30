from django.db import models


class Customer(models.Model):
    """
    This model is used as the customer contact model. It contains customer info
    such as name, fax, email, phone number(s), and all the tickets each customer
    has.
    """
    # Customer's name
    first_name = models.CharField("first name", max_length=255, blank=True)
    last_name = models.CharField("last name", max_length=255, blank=True)

    # Customer's Contact information
    email = models.EmailField("email address")

    def get_full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    class Admin:
        pass