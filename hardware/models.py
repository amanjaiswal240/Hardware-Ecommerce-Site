from django.db import models

class Product(models.Model):
    category=models.CharField(max_length=50)
    sub_category=models.CharField(max_length=50)
    product_name=models.CharField(max_length=100)
    description=models.CharField(max_length=400)
    pub_date=models.DateField()
    price=models.IntegerField()
    quantity=models.IntegerField()
    image=models.ImageField(upload_to='hardware/images')

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount= models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    zip_code=models.CharField(max_length=40)

    def __str__(self):
        return self.name
    
class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
