from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self):
        return reverse('system_tailoring')

    def __str__(self):
        return self.item_name