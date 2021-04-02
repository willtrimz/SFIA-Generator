from dynamic_preferences.types import BooleanPreference, StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from django.forms import ValidationError
from .models import Skill, cy_Skill

@global_preferences_registry.register
class EnableWelshSFIA(BooleanPreference):
    name = 'Enable_Welsh_SFIA_Skills'
    default = False

    def validate(self, value):
        if value == True:
            try:
                for skill in Skill.objects.all():
                    cy_Skill.objects.get(code=skill.code)
            except:
                raise ValidationError('There are skills in the database that exist in English but not Welsh.')
            try:
                for skill in cy_Skill.objects.all():
                    Skill.objects.get(code=skill.code)
            except:
                raise ValidationError('There are skills in the database that exist in Welsh but not English.')



@global_preferences_registry.register
class EnableWelshCoreCompetencies(BooleanPreference):
    name = 'Enable_Welsh_Core_Competencies'
    default = False