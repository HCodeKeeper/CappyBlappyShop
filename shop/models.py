from django.db import models


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    tel = models.CharField(max_length=11)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    image_src = models.CharField(max_length=256)
    rating = models.SmallIntegerField(default=0)
    description = models.CharField(max_length=5000)
    manufacturer = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    # ALWAYS USD
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()


class Deal(models.Model):
    title = models.CharField(max_length=50)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    percents = models.FloatField(max_length=3)


class Addon(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.SmallIntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    text = models.CharField(max_length=1000, default="")


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    creation_date = models.DateTimeField()


# Product instance(s) ordered by a user
class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    addon = models.ForeignKey(Addon, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField( default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
