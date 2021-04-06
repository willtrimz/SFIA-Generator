from dynamic_preferences.types import BooleanPreference, StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from django.forms import ValidationError
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
class EnableWelshCoreCompetencies(BooleanPreference):
    name = 'Enable_Welsh_Core_Competencies'
    default = False