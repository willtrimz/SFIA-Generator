# Generated by Django 3.0.7 on 2021-04-13 14:43

import Generator.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Generator', '0002_docx_templates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docx_templates',
            name='file',
            field=models.FileField(storage=Generator.models.OverwriteStorage(), upload_to='Generator/DocxTemplates/'),
        ),
    ]
