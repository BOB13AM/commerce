from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=64, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    bid = models.DecimalField(max_digits=1000000000000, decimal_places=2)
    userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    wishlist = models.ManyToManyField(User, related_name="wishlistings", blank=True)
    closedbid = models.CharField(max_length=24, null=True, blank=True)
    currentbid = models.DecimalField(max_digits=1000000000000, decimal_places=2, null=True, blank=True)
    winninguser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="itemwin", null=True, blank=True)
    def __str__(self):
         return f"item id:{self.id} Title: {self.title}, description: {self.description},  minimum bid ({self.bid}$), Category {self.category}" 



class bids(models.Model):
    userbid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userbids")
    itembid = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="itembids")
    biding = models.DecimalField(max_digits=1000000000000, decimal_places=2)
    closed = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self):
         return f"User: {self.userbid}, Biding on : {self.itembid}, Biding amount: {self.biding}$"


class invalidbid(models.Model):
    invalid_userbid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invaliduserbids")
    invalid_itembid = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="invaliditembids")
    invalid_biding = models.DecimalField(max_digits=1000000000000, decimal_places=2)
    closed = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self):
         return f"User: {self.invalid_userbid}, Biding on : {self.invalid_itembid}, Biding amount: {self.invalid_biding}$"


class comments(models.Model):
    usercomment = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    itemcomment = models.ForeignKey(listing, on_delete=models.CASCADE, related_name="itemcomments")
    comment = models.CharField(max_length=255, null=True, blank=True)
    reply = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
         return f"{self.comment}"

class commentreply(models.Model):
    replying_user_main = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userreply")
    reply = models.CharField(max_length=255)
    maincomment = models.ForeignKey(comments, on_delete=models.CASCADE, related_name="commentmain")
    old_replying_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="rtor", null=True, blank=True)
    old_reply = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
         return f"{self.reply}"         