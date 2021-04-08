import json
from django.contrib import admin, messages
from django.utils.text import slugify
from django.db import models
from ckeditor.widgets import CKEditorWidget
from dynamic_preferences.registries import global_preferences_registry
from .models import en_Skill, en_Level, en_SkillJSON, cy_Skill, cy_Level, cy_SkillJSON, docx_templates

global_preferences = global_preferences_registry.manager()
# Register your models here.

def processJSON(modeladmin, request, queryset):
    for file in queryset:
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
processJSON.short_description = 'Upload to Models'

# English model admins
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
    inlines = [en_LevelInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    def save_model(self, request, obj, form, change):
        try:
            cy_Skill.objects.get(code=obj.code)
        except:
            if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
                global_preferences['Enable_Welsh_SFIA_Skills'] = False
                messages.add_message(request, messages.WARNING, "A skill with this code does not exist in the Welsh database table. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().save_model(request, obj, form, change)

class en_SkillJSONAdmin(admin.ModelAdmin):
    model = en_SkillJSON
    actions = [processJSON]

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
    inlines = [cy_LevelInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    def save_model(self, request, obj, form, change):
        try:
            en_Skill.objects.get(code=obj.code)
        except:
            if global_preferences['Enable_Welsh_SFIA_Skills'] == True:
                global_preferences['Enable_Welsh_SFIA_Skills'] = False
                messages.add_message(request, messages.WARNING, "A skill with this code does not exist in the English database table. Therefore the ""Enable_Welsh_SFIA_Skills"" preference has been disabled.")
        super().save_model(request, obj, form, change)

class cy_SkillJSONAdmin(admin.ModelAdmin):
    model = cy_SkillJSON
    actions = [processJSON]

class docx_templatesAdmin(admin.ModelAdmin):
    model = docx_templates
    def save_model(self, request, obj, form, change):
        form_types = ['employer_template_en.docx', 'student_template_en.docx', 'employer_template_cy.docx', 'student_template_cy.docx']
        filename = obj.__str__()
        if filename not in form_types:
            messages.add_message(request, messages.WARNING, "{fileName} is not one of the supported form types. Please attached a file which conforms to one of the following names: ".format(fileName=filename) + str(form_types))
            messages.set_level(request, messages.ERROR)
        else:
            if docx_templates.objects.filter(file__endswith=filename).exists():
                docx_templates.objects.filter(file__endswith=filename).delete()
            super().save_model(request, obj, form, change)


admin.site.register(en_Skill, en_SkillAdmin)
admin.site.register(en_SkillJSON, en_SkillJSONAdmin)

admin.site.register(cy_Skill, cy_SkillAdmin)
admin.site.register(cy_SkillJSON, cy_SkillJSONAdmin)

admin.site.register(docx_templates, docx_templatesAdmin)