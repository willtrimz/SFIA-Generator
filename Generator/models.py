from django.db import models

# Create your models here.

#Models for the English SFIA data
class Skill(models.Model):
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank = True, null = True)
    def __str__(self):
        return self.name.__str__()

class Level(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    description = models.TextField(blank = True, null = True)

class SkillJSON(models.Model):
    file = models.FileField(upload_to='uploads/')
    class Meta:
        verbose_name = 'Skills JSON file'
        verbose_name_plural = 'Skills JSON files'
    def __str__(self):
        return self.file.name.__str__()

# Models for the Welsh SFIA data
class cy_Skill(models.Model):
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank = True, null = True)
    def __str__(self):
        return self.name.__str__()
    class Meta:
        verbose_name = 'Welsh SFIA Skill'
        verbose_name_plural = 'Welsh SFIA Skills'

class cy_Level(models.Model):
    skill = models.ForeignKey(cy_Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    description = models.TextField(blank = True, null = True)

class cy_SkillJSON(models.Model):
    file = models.FileField(upload_to='uploads/')
    class Meta:
        verbose_name = 'Welsh Skills JSON file'
        verbose_name_plural = 'Welsh Skills JSON files'
    def __str__(self):
        return self.file.name.__str__()