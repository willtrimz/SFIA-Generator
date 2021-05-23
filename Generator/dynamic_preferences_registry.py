from dynamic_preferences.types import BooleanPreference
from dynamic_preferences.registries import global_preferences_registry
import docx
from django.forms import ValidationError
from django.conf import settings
from .models import en_Skill, cy_Skill, docx_templates, core_competencies_json

@global_preferences_registry.register
class EnableWelshSFIA(BooleanPreference):
    name = 'Enable_Welsh_SFIA_Skills'
    default = False
    def validate(self, value):
        # Preference will not be allowed to be enabled if it does not pass validation
        if value == True:
            try:
            # Check that for all English skills, the same skill exists in Welsh
                for skill in en_Skill.objects.all():
                    cy_Skill.objects.get(code=skill.code)
            except:
                # If any skill not found in the converse db model, an error is raised and preference is not enabled
                raise ValidationError('There are skills in the database that exist in English but not Welsh - skill sets must be identical, therefore this preference cannot be enabled.')
            try:
            # Check that for all Welsh skills, the same skill exists in English
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
                # Check that db contains the Welsh docx templates
                docx_templates.objects.get(file__contains="student_template_cy")
                docx_templates.objects.get(file__contains="employer_template_cy")
            except:
                raise ValidationError("The files 'student_template_cy.docx' or 'employer_template_cy.docx' (or both) cannot be found, therefore this preference cannot be enabled. Please ensure the Docx files have been uploaded correctly.")
            

@global_preferences_registry.register
class EnableWelshCoreCompetencies(BooleanPreference):
    name = 'Enable_Welsh_Core_Competencies'
    default = False
    def validate(self, value):
        if value == True:
            try:
            # Check that db contains the Welsh core competencies file
                core_competencies_json.objects.get(file__contains="core_competencies_cy")
            except:
                raise ValidationError("The file 'core_competencies_cy.json' cannot be found, therefore this preference cannot be enabled. Please ensure the JSON file has been uploaded correctly.")
