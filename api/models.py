from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    titulo = models.CharField(max_length = 180)
    estado = models.IntegerField()
    fecha = models.DateTimeField(auto_now = True, blank = True)

    def __str__(self):
        return self.titulo