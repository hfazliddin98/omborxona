from django.db import models
from users.models import AsosiyModel


class Kategoriya(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MaxsulotNomi(AsosiyModel):
    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.CASCADE, related_name='maxsulot')
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

