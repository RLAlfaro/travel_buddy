from django.db import models
import re
import datetime

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['first_name']) < 2:
            errors['firstname_len'] = "El nombre debe tener al menos 2 caracteres de largo"

        if len(postData['last_name']) < 2:
            errors['lastname_len'] = "El apellido debe tener al menos 2 caracteres de largo"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['first_name']):
            errors['solo_letras'] = "El nombre contener tener solo letras"

        if not SOLO_LETRAS.match(postData['last_name']):
            errors['solo_letras'] = "El nombre contener tener solo letras"    

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres"

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales."

        
        return errors

class TripManager(models.Manager):
    def validador_basico(self, postData):
        errors = {}
        today = datetime.date.today()


        if len(postData['destination']) < 2:
            errors['destination_len'] = "El nombre del destino debe tener al menos 2 caracteres"

        if len(postData['description']) < 2:
            errors['description_len'] = "La descripcion no puede estar vacia"

        if postData['start_date'] < today.strftime("%d/%m/%Y"):
            errors['date_issue_1'] = "Vas a viajar al pasado?"

        if postData['end_date'] < postData['start_date']:
            errors['date_issue_2'] = "Con que planeas un viaje en el tiempo..."

        return errors   

    # manager = models.ForeignKey(User, related_name = "managers", on_delete= models.CASCADE)
    # destination = models.CharField(max_length=100)
    # description = models.TextField()
    # traveler = models.ManyToManyField(User, related_name="travelers")
    # start_date = models.DateField(("%d-%m-%Y"))
    # end_date = models.DateField(("%d-%m-%Y"))

class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name}"


class Trip(models.Model):
    manager = models.ForeignKey(User, related_name = "managers", on_delete= models.CASCADE)
    destination = models.CharField(max_length=100)
    description = models.TextField()
    traveler = models.ManyToManyField(User, related_name="travelers")
    start_date = models.DateField(("%d-%m-%Y"))
    end_date = models.DateField(("%d-%m-%Y"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __str__(self):
        return f"{self.id} : {self.manager} : {self.destination}"