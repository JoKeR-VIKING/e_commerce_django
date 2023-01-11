from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=150)
    brand = models.CharField(max_length=150, default="non-branded")
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=150, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
