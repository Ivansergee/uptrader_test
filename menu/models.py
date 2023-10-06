from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='submenus', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
