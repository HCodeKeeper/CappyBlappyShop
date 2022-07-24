from django.db import models


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=70)
    rating = models.SmallIntegerField(max_length=1, default=0)
    description = models.CharField(max_length=5000)
    manufacturer = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2) #ALWAYS USD
    quantity = models.IntegerField(max_length=9)


class Addon(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.SmallIntegerField(max_length=1, default=0)
    upvotes = models.IntegerField(default=0, max_length=6)
    downvotes = models.IntegerField(default=0, max_length=6)
    text = models.CharField(max_length=1000, default="")


class Order(models.Model):
    customer = models.ForeignKey(User)
    creation_date = models.DateTimeField()


#Product instance(s) ordered by a user
class Item(models.Model):
    product = models.ForeignKey(Product)
    addon = models.ForeignKey(Addon)
    quantity = models.IntegerField(max_length=5, default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
