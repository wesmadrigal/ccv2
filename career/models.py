from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    
    def __repr__(self):
        print '\n'.join([ self.title, self.company, self.location ])
