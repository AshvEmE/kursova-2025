from django.db import models

class Task(models.Model):
    title = models.CharField('Name',max_length=100)
    description = models.TextField('Description')


    def __str__(self):
        return self.title