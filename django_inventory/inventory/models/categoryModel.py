from django.db import models

class Categories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name=models.CharField(max_length = 50, unique=True)
    description=models.TextField(blank=True)
    added_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'


class Subcategories(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    description=models.TextField(blank=True)
    added_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Sub Categories'
