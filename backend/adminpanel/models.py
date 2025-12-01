from django.db import models

# Create your models here.


class AppSettings(models.Model):
    """Global application settings"""
    
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    
    class Meta:
        db_table = 'app_settings'
        verbose_name = 'App Setting'
        verbose_name_plural = 'App Settings'
    
    def __str__(self):
        return self.setting_key
