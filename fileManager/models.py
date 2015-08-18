from django.db import models
class File0(models.Model):
    uid = models.CharField(max_length=100)
    File = models.FileField(upload_to = './upload/')

    def __unicode__(self):
        return self.uid

    
    
