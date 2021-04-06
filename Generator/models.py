from django.db import models

# Create your models here.

#Models for the English SFIA data
class en_Skill(models.Model):
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank = True, null = True)
    def __str__(self):
        return self.name.__str__()
    class Meta:
        verbose_name = 'Individual SFIA Skill (English)'
        verbose_name_plural = 'Individual SFIA Skills (English)'

class en_Level(models.Model):
    skill = models.ForeignKey(en_Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    description = models.TextField(blank = True, null = True)

class en_SkillJSON(models.Model):
    file = models.FileField(upload_to='uploads/')
    def __str__(self):
        return self.file.name.__str__()
    class Meta:
        verbose_name = 'SFIA JSON file (English)'
        verbose_name_plural = 'SFIA JSON files (English)'

# Models for the Welsh SFIA data
class cy_Skill(models.Model):
    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank = True, null = True)
    def __str__(self):
        return self.name.__str__()
    class Meta:
        verbose_name = 'Individual SFIA Skill (Cymraeg)'
        verbose_name_plural = 'Individual SFIA Skills (Cymraeg)'

class cy_Level(models.Model):
    skill = models.ForeignKey(cy_Skill, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    description = models.TextField(blank = True, null = True)

class cy_SkillJSON(models.Model):
    file = models.FileField(upload_to='uploads/')
    def __str__(self):
        return self.file.name.__str__()
    class Meta:
        verbose_name = 'SFIA JSON file (Cymraeg)'
        verbose_name_plural = 'SFIA JSON files (Cymraeg)'