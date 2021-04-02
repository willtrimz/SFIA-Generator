import json
from django.contrib import admin
from django.utils.text import slugify
from django.db import models
from ckeditor.widgets import CKEditorWidget
from .models import Skill, Level, SkillJSON, cy_Skill, cy_Level, cy_SkillJSON

# Register your models here.

def processJSON(modeladmin, request, queryset):
    for file in queryset:
        #file.file.open()
        data = json.load(file.file)
        if data['language'] == 'en':
            skill_model = Skill
            level_model = Level
        elif data['language'] == 'cy':
            skill_model = cy_Skill
            level_model = cy_Level
        for skill in data['skills']:
            page_attrs = {
                'name': skill['name'],
                'description': skill['description'],
            }
            page, page_created = skill_model.objects.get_or_create(code=slugify(skill['code']), defaults=page_attrs)
            if not page_created:
                continue
            else:
                #Delete current levels if updating
                for level in level_model.objects.filter(skill=page):
                    level.delete()
            for level in skill['levels']:
                level_model.objects.create(skill=page, level=level['level'], description=level['description'])
processJSON.short_description = 'Upload to Models'

# English Data
class en_LevelInline(admin.TabularInline):
    model = Level
    formfield_overrides = {
        models.TextField : {'widget': CKEditorWidget(config_name='advanced_setting')},
    }
    ordering = ('level',)
    extra = 0

class en_SkillAdmin(admin.ModelAdmin):
    model = Skill
    list_display = ['name','code',]
    search_fields = ['name','code']
    inlines = [en_LevelInline]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='advanced_setting')},
    }

class en_SkillJSONAdmin(admin.ModelAdmin):
    model = SkillJSON
    actions = [processJSON]

# Welsh Data
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

class cy_SkillJSONAdmin(admin.ModelAdmin):
    model = cy_SkillJSON
    actions = [processJSON]

admin.site.register(Skill, en_SkillAdmin)
admin.site.register(SkillJSON, en_SkillJSONAdmin)

admin.site.register(cy_Skill, cy_SkillAdmin)
admin.site.register(cy_SkillJSON, cy_SkillJSONAdmin)