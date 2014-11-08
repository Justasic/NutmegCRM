from django.db import models


class Customer(models.Model):
    """
    This model is used as the customer contact model. It contains customer info
    such as name, fax, email, phone number(s), and all the tickets each customer
    has.
    """
    # Added date
    created = models.DateTimeField(auto_now_add=True)
    # slugfield used in urls
    #slug = models.SlugField()

    # Customer's name
    first_name = models.CharField("first name", max_length=255)
    last_name = models.CharField("last name", max_length=255)

    # Customer's Contact information
    email = models.EmailField("email address", blank=True)
    # I made the phone field required because we may need to call the customer.
    phone = models.CharField("phone", max_length=25)


    def get_full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.get_full_name()

    class Admin:
        pass

