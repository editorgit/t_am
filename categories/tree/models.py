from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    parent = models.ForeignKey(verbose_name='Parent category', to='self', related_name='children',
                               blank=True, null=True, on_delete=models.SET_NULL)
