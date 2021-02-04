from django.db import models

# Create your models here.



# Create your models here.
class Shop_data(models.Model):
    shop_id = models.AutoField(primary_key=True)
    shop = models.CharField(max_length=500,editable=True)
    api_key = models.CharField(max_length=100,editable=True)
    token = models.CharField(max_length=100,editable=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=True,)
    updated_at = models.DateTimeField(auto_now=True,editable=True,)

    def __str__(self):
        return self.shop +'  id = '+ str(self.shop_id)