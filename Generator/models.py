from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your database models here.

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

# Allows files to be overritten when a file of the same name is uploaded
# Used for docx templates and core competencies
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return super().get_available_name(name, max_length)

class docx_templates(models.Model):
    file = models.FileField(upload_to='Generator/DocxTemplates/', storage=OverwriteStorage())
    def __str__(self):
        return self.file.name.__str__()
    class Meta:
        verbose_name = 'Docx Form Template'
        verbose_name_plural = 'Docx Form Templates'

class core_competencies_json(models.Model):
    file = models.FileField(upload_to='Generator/CoreCompetenciesJSONs/', storage=OverwriteStorage())
    def __str__(self):
        return self.file.name.__str__()
    class Meta:
        verbose_name = 'Core Competencies JSON file'
        verbose_name_plural = 'Core Competencies JSON files'
