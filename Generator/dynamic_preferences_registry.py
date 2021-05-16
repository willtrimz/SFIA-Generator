from dynamic_preferences.types import BooleanPreference
from dynamic_preferences.registries import global_preferences_registry
import docx
from django.forms import ValidationError
from django.conf import settings
from .models import en_Skill, cy_Skill

@global_preferences_registry.register
class EnableWelshSFIA(BooleanPreference):
    name = 'Enable_Welsh_SFIA_Skills'
    default = False
    def validate(self, value):
        if value == True:
            try:
                for skill in en_Skill.objects.all():
                    cy_Skill.objects.get(code=skill.code)
            except:
                raise ValidationError('There are skills in the database that exist in English but not Welsh - skill sets must be identical, therefore this preference cannot be enabled.')
            try:
                for skill in cy_Skill.objects.all():
                    en_Skill.objects.get(code=skill.code)
            except:
                raise ValidationError('There are skills in the database that exist in Welsh but not English - skill sets must be identical, therefore this preference cannot be enabled.')


@global_preferences_registry.register
class EnableDocxTemplatesCompetencies(BooleanPreference):
    name = 'Enable_Welsh_Docx_Templates'
    default = False
    def validate(self, value):
        if value == True:
            try:
                docx.Document(settings.BASE_DIR + '/Generator/DocxTemplates/student_template_cy.docx')
                docx.Document(settings.BASE_DIR + '/Generator/DocxTemplates/employer_template_cy.docx')
            except:
                raise ValidationError("The files 'student_template_cy.docx' and 'employer_template_cy.docx' cannot be found, therefore this preference cannot be enabled. Please ensure the Docx files have been uploaded correctly.")
            

@global_preferences_registry.register
class EnableWelshCoreCompetencies(BooleanPreference):
    name = 'Enable_Welsh_Core_Competencies'
    default = False
    def validate(self, value):
        if value == True:
            try:
                with open(settings.BASE_DIR + "/Generator/CoreCompetenciesJSONs/core_competencies_cy.json", "r"):
                    pass
            except:
                raise ValidationError("The file 'core_competencies_cy.json' cannot be found, therefore this preference cannot be enabled. Please ensure the JSON file has been uploaded correctly.")
