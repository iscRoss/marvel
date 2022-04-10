from django.db import models

# Create your models here.
class usuarios_atlas (models.Model):
    id = models.AutoField(primary_key = True)
    name =models.CharField(max_length = 100,blank = False, null = False,)
    edad =models.IntegerField(blank = False, null = False,)
    token =models.CharField(max_length = 100,blank = True, null = True,)
    password =models.CharField(max_length = 100,blank = False, null = False,)

    def __str__(self):
        return self.name
