from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    category_name = models.CharField(max_length=256)
    category_image = models.ImageField(upload_to='category/images') 
    
    def get_absolute_url(self):
        return reverse('system_tailoring')

    def __str__(self):
        return self.category_name

class Item(models.Model):
    BOX_CONDITION = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )

    item_name = models.CharField(max_length=256)
    item_description = models.TextField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Should we add a default Image if not yet set?
    # models.ImageField(upload_to = '', default = 'pic_folder/None/no-img.jpg')
    item_image = models.ImageField(upload_to='inventory/images')
    item_category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    item_condition = models.PositiveSmallIntegerField(choices=BOX_CONDITION)

    # item_count not applicable for now, but this can be used in the future!
    # item_count = models.IntegerField()
    
    # item can be 'dibs' by multiple users. Users can dibs multiple items
    item_user_dibs = models.ManyToManyField(User, through='UserDibs')

    def get_absolute_url(self):
        return reverse('system_tailoring')

    def __str__(self):
        return self.item_name

class UserDibs(models.Model):
    item = models.ForeignKey(Item, related_name='item', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_dibs', on_delete=models.CASCADE)
    user_receipt = models.ImageField(upload_to='inventory/images/receipts', null=True)
    # user_instructions = models.TextField(null=True, blank=False)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('item', 'user')
