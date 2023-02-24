from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', related_name='submenus', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
