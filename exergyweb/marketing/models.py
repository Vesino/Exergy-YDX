from django.db import models

class Stay_Tuned(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
