from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_comma_separated_integer_list
from users.models import User


class CalculateManager(models.Manager):
    def create(self, user, array, calculations):
        calc = Calculate(user=user, array=array, calculations=calculations)
        calc.save(using=self._db)
        return calc


class Calculate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    array = models.CharField(validators=[validate_comma_separated_integer_list], max_length=100)
    calculations = models.TextField(validators=[RegexValidator(regex='^[0-9,]+$')])

    objects = CalculateManager()