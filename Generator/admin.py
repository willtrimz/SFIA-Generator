import json
from django.contrib import admin, messages
from django.utils.text import slugify
from django.db import models
from ckeditor.widgets import CKEditorWidget
from dynamic_preferences.registries import global_preferences_registry
from .models import en_Skill, en_Level, en_SkillJSON, cy_Skill, cy_Level, cy_SkillJSON, docx_templates, core_competencies_json
from django.contrib.auth.models import Group
# Remove the 'Group' model from the admin dashboard as it is not needed
admin.site.unregister(Group)

global_preferences = global_preferences_registry.manager()

def processJSON(modeladmin, request, queryset):
    for file in queryset:
        try:
            # Boolean flag which can be set if a skill is added which does not already exist in the converse (opposite) language's database table
            unmatched_skill_found = False
            #file.file.open()
            data = json.load(file.file)
            # Checking the language code at the top of the JSON file
            if data['language'] == 'en':
                # Selecting the English database models to be uploaded to
                skill_model = en_Skill
                level_model = en_Level
                # Selecting Welsh skill model to be checked against for non-matching skills
                converse_skill_model = cy_Skill
            elif data['language'] == 'cy':
                # Selecting the Welsh models to be uploaded to
                skill_model = cy_Skill
                level_model = cy_Level
                # Selecting English skill model to be checked against for non-matching skills
                converse_skill_model = en_Skill
            for skill in data['skills']:
                page_attrs = {
                    'name': skill['name'],
                    'description': skill['description'],
                }
                page, page_created = skill_model.objects.get_or_create(code=slugify(skill['code']), defaults=page_attrs)
                if not page_created:
                    continue
                else:
                    # Delete current levels if updating
                    for level in level_model.objects.filter(skill=page):
                        level.delete()
                for level in skill['levels']:
                    level_model.objects.create(skill=page, level=level['level'], description=level['description'])
                # For each skill added, check if it exists in the converse language's DB table
                if not converse_skill_model.objects.filter(code=slugify(skill['code'])).exists():
                    unmatched_skill_found = True
            # If this flag is set to true AND the Enable_Welsh_SFIA_Skills is enables, disable the preference and inform user.
            if unmatched_skill_found:
                if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
                    global_preferences['Enable_Welsh_SFIA_Skills'] = False
                    messages.add_message(request, messages.WARNING, "One or more of the skills uploaded does not appear in the {converse_language} skills database table. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.".format(converse_language="Welsh" if data["language"]=="en" else "English"))
        except:
            messages.add_message(request, messages.WARNING, "The selected file could not be uploaded to the database models. Please ensure you have selected the correct file and it has been formatted/structured correctly.")
processJSON.short_description = 'Upload to Models'

# English model admins:
class en_LevelInline(admin.TabularInline):
    model = en_Level
    formfield_overrides = {
        models.TextField : {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    ordering = ('level',)
    extra = 0

class en_SkillAdmin(admin.ModelAdmin):
    model = en_Skill
    list_display = ['name','code',]
    search_fields = ['name','code']
    # Link the skill levels to the skill form so they can be entered at the same time 
    inlines = [en_LevelInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    def save_model(self, request, obj, form, change):
        # Convert the skill code to a lowercase slug
        obj.code = slugify(obj.code)
        # If the same skill cannot be located in the Welsh skill database, disable the Enable_Welsh_SFIA_Skills preference
        try:
            cy_Skill.objects.get(code=obj.code)
        except:
            if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
                global_preferences['Enable_Welsh_SFIA_Skills'] = False
                messages.add_message(request, messages.WARNING, "A skill with this code does not exist in the Welsh database table. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().save_model(request, obj, form, change)
    # If skills are deleted (both indivually or part of a queryset) we know the English and Welsh skill sets will not match, so we disable the enable Enable_Welsh_SFIA_Skills preference
    def delete_model(self, request, obj):
        if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
            global_preferences['Enable_Welsh_SFIA_Skills'] = False
            messages.add_message(request, messages.WARNING, "The English and Welsh skill sets in the database must be identical. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().delete_model(request, obj)
    def delete_queryset(self, request, queryset):
        if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
            global_preferences['Enable_Welsh_SFIA_Skills'] = False
            messages.add_message(request, messages.WARNING, "The English and Welsh skill sets in the database must be identical. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().delete_queryset(request, queryset)

class en_SkillJSONAdmin(admin.ModelAdmin):
    model = en_SkillJSON
    actions = [processJSON]
    def save_model(self, request, obj, form, change):
        # Check that file follows valid format and structure
        if not ValidateSFIASkillsJson(request):
            messages.add_message(request, messages.WARNING, "The selected file could not be uploaded. Please ensure you have selected the correct file and it has been formatted/structured correctly.")
            messages.set_level(request, messages.ERROR)
        # If so, save model
        else:
            super().save_model(request, obj, form, change)

# Welsh model admins
class cy_LevelInline(admin.TabularInline):
    model = cy_Level
    formfield_overrides = {
        models.TextField : {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    ordering = ('level',)
    extra = 0

class cy_SkillAdmin(admin.ModelAdmin):
    model = cy_Skill
    list_display = ['name','code',]
    search_fields = ['name','code']
    # Link the skill levels to the skill form so they can be entered at the same time 
    inlines = [cy_LevelInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    def save_model(self, request, obj, form, change):
        # Convert the skill code to a lowercase slug
        obj.code = slugify(obj.code)
        # If the same skill cannot be located in the English skill database, disable the Enable_Welsh_SFIA_Skills preference
        try:
            en_Skill.objects.get(code=obj.code)
        except:
            if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
                global_preferences['Enable_Welsh_SFIA_Skills'] = False
                messages.add_message(request, messages.WARNING, "A skill with this code does not exist in the English database table. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().save_model(request, obj, form, change)
    # If skills are deleted (both indivually or part of a queryset) we know the English and Welsh skill sets will not match, so we disable the enable Enable_Welsh_SFIA_Skills preference
    def delete_model(self, request, obj):
        if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
            global_preferences['Enable_Welsh_SFIA_Skills'] = False
            messages.add_message(request, messages.WARNING, "The English and Welsh skill sets in the database must be identical. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().delete_model(request, obj)
    def delete_queryset(self, request, queryset):
        if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
            global_preferences['Enable_Welsh_SFIA_Skills'] = False
            messages.add_message(request, messages.WARNING, "The English and Welsh skill sets in the database must be identical. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().delete_queryset(request, queryset)

class cy_SkillJSONAdmin(admin.ModelAdmin):
    model = cy_SkillJSON
    actions = [processJSON]
    def save_model(self, request, obj, form, change):
        # Check that file follows valid format and structure
        if not ValidateSFIASkillsJson(request):
            messages.add_message(request, messages.WARNING, "The selected file could not be uploaded. Please ensure you have selected the correct file and it has been formatted/structured correctly.")
            messages.set_level(request, messages.ERROR)
        # If so, save model
        else:
            super().save_model(request, obj, form, change)


class docx_templatesAdmin(admin.ModelAdmin):
    model = docx_templates
    def save_model(self, request, obj, form, change):
        OK_file_names = ['employer_template_en.docx', 'student_template_en.docx', 'employer_template_cy.docx', 'student_template_cy.docx']
        filename = obj.__str__()
        # Check that file is named appropriately
        if filename not in OK_file_names:
            messages.add_message(request, messages.WARNING, "{fileName} is not one of the supported form types. Please attached a file which conforms to one of the following names: ".format(fileName=filename) + str(OK_file_names))
            messages.set_level(request, messages.ERROR)
        # If condition is met, save and overwrite existing file if exists
        else:
            if docx_templates.objects.filter(file__endswith=filename).exists():
                docx_templates.objects.filter(file__endswith=filename).delete()
            super().save_model(request, obj, form, change)
    def delete_model(self, request, obj):
        # If form templates are deleted, disable the Enable_Welsh_Docx_Templates language preference
        if global_preferences['Enable_Welsh_Docx_Templates'] == True:
            global_preferences['Enable_Welsh_Docx_Templates'] = False
            messages.add_message(request, messages.WARNING, "The Enable_Welsh_Docx_Templates language preference has been disabled.")
        # If an English form template is deleted, warn the user that the application requires the English templates
        if "template_en" in obj.__str__():
            messages.add_message(request, messages.WARNING, "WARNING: The form generator needs at least the English form templates to function.")
        super().delete_model(request, obj)
    def delete_queryset(self, request, queryset):
        # Same if multiple items are deleted
        if global_preferences['Enable_Welsh_Docx_Templates'] == True:
            global_preferences['Enable_Welsh_Docx_Templates'] = False
            messages.add_message(request, messages.WARNING, "The Enable_Welsh_Docx_Templates language preference has been disabled.")
        if any("template_en" in filename for filename in map(str, queryset)):
            messages.add_message(request, messages.WARNING, "WARNING: The form generator needs at least the English form templates to function.")
        super().delete_queryset(request, queryset)


class core_competencies_jsonAdmin(admin.ModelAdmin):
    model = core_competencies_json
    def save_model(self, request, obj, form, change):
        OK_file_names = ['core_competencies_en.json', 'core_competencies_cy.json']
        filename = obj.__str__()
        # Check that file is named appropriately
        if filename not in OK_file_names:
            messages.add_message(request, messages.WARNING, "{fileName} is not one of the supported files. Please attached a file which conforms to one of the following names: ".format(fileName=filename) + str(OK_file_names))
            messages.set_level(request, messages.ERROR)
        # Check that file follows valid format and structure
        elif not ValidateCoreCompetenciesJson(request):
            messages.add_message(request, messages.WARNING, "The selected file could not be uploaded. Please ensure you have selected the correct file and it has been formatted/structured correctly.")
            messages.set_level(request, messages.ERROR)
        # If conditions are met, save and overwrite existing file if exists
        else:
            if core_competencies_json.objects.filter(file__endswith=filename).exists():
                core_competencies_json.objects.filter(file__endswith=filename).delete()
            super().save_model(request, obj, form, change)
    def delete_model(self, request, obj):
        # If core competencies are deleted, disable the Enable_Welsh_Core_Competencies language preference
        if global_preferences['Enable_Welsh_Core_Competencies'] == True:
            global_preferences['Enable_Welsh_Core_Competencies'] = False
            messages.add_message(request, messages.WARNING, "The Enable_Welsh_Core_Competencies language preference has been disabled.")
        # If an English core competencies file is deleted, warn the user that the application requires the English core competencies
        if "core_competencies_en" in obj.__str__():
            messages.add_message(request, messages.WARNING, "WARNING: The form generator needs at least the English core competencies to function.")
        super().delete_model(request, obj)
    def delete_queryset(self, request, queryset):
        # Same if multiple items are deleted
        if global_preferences['Enable_Welsh_Core_Competencies'] == True:
            global_preferences['Enable_Welsh_Core_Competencies'] = False
            messages.add_message(request, messages.WARNING, "The Enable_Welsh_Core_Competencies language preference has been disabled.")
        if any("core_competencies_en" in filename for filename in map(str, queryset)):
            messages.add_message(request, messages.WARNING, "WARNING: The form generator needs at least the English core competencies to function.")
        super().delete_queryset(request, queryset)
        
# File Validation:
 
def ValidateSFIASkillsJson(request):
    # Validation to check that JSON is structured correctly and uses the correct data types
    fileIsValid = True
    try:
        file = request.FILES['file']
        data = json.load(file.file)
        if not isinstance(data['language'], str): fileIsValid = False
        skills = data['skills']
        for skill in skills:
            if not isinstance(skill['name'], str): fileIsValid = False
            if not isinstance(skill['code'], str): fileIsValid = False
            if not isinstance(skill['description'], str): fileIsValid = False
            levels = skill['levels']
            for level in levels:
                if not isinstance(level['level'], int): fileIsValid = False
                if not isinstance(level['description'], str): fileIsValid = False
    except:
        fileIsValid = False
    return fileIsValid

def ValidateCoreCompetenciesJson(request):
    # Validation to check that JSON is structured correctly and uses the correct data types
    fileIsValid = True
    try:
        file = request.FILES['file']
        data = json.load(file.file)
        if not isinstance(data['heading'], str): fileIsValid = False
        if not isinstance(data['student_message'], str): fileIsValid = False
        if not isinstance(data['employer_message'], str): fileIsValid = False
        for competency in data['competencies']:
            if not isinstance(competency['competency'], str): fileIsValid = False
            for level in competency['levels']:
                if not isinstance(level['level'], int): fileIsValid = False
                if not isinstance(level['description'], str): fileIsValid = False
        business_skills = data['business_skills']
        if not isinstance(business_skills['competency_name'], str): fileIsValid = False
        if not isinstance(business_skills['message'], str): fileIsValid = False
        if not isinstance(business_skills['skills_included'], list): fileIsValid = False
        for level in business_skills['levels']:
            if not isinstance(level['level'], int): fileIsValid = False
            if not isinstance(level['description'], str): fileIsValid = False
    except:
        fileIsValid = False
    return fileIsValid

# Register your models here.
admin.site.register(en_Skill, en_SkillAdmin)
admin.site.register(en_SkillJSON, en_SkillJSONAdmin)

admin.site.register(cy_Skill, cy_SkillAdmin)
admin.site.register(cy_SkillJSON, cy_SkillJSONAdmin)

admin.site.register(docx_templates, docx_templatesAdmin)
admin.site.register(core_competencies_json, core_competencies_jsonAdmin)