from django.db import models
from core.models import BaseModel

class Product(BaseModel):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(default="-", max_length=100, null=False)
    prod_link = models.CharField(default="-", max_length=300, null=False)
    prod_price = models.IntegerField(default=0, null=False)
    prod_thumbnail = models.CharField(default="-", max_length=300, null=False)

    class Meta:
        managed = True
        db_table = 'products'

class Hashtag(BaseModel):
    hash_id = models.AutoField(primary_key=True)
    hash_name = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        managed = True
        db_table = 'hashtags'

class ProductHashtag(BaseModel):
    prod_hash_id = models.AutoField(primary_key=True)
    prod_id = models.ForeignKey(to=Product, db_column="prod_id", on_delete=models.PROTECT)
    hash_id = models.ForeignKey(to=Hashtag, db_column="hash_id", on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'products_hashtags'