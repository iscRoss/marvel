from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create your models here.
class comics (models.Model):
    id = models.AutoField(primary_key = True)
    id_comics =models.IntegerField(blank = True, null = True,)
    title =models.CharField(max_length = 100,blank = False, null = False,)
    image = models.URLField(max_length=200, blank =True, null=True)
    onsaleDate =models.DateTimeField(max_length = 100,blank = True, null = True,)
    user_crea = models.ForeignKey(User, related_name='usuario_bloqueo', on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return self.name