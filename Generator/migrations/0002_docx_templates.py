# Generated by Django 3.0.7 on 2021-04-07 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Generator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='docx_templates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='Generator/DocxTemplates/')),
            ],
            options={
                'verbose_name': 'Docx Form Template',
                'verbose_name_plural': 'Docx Form Templates',
            },
        ),
    ]
