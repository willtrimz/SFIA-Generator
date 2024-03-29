# Generated by Django 3.0.7 on 2021-04-06 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cy_Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Individual SFIA Skill (Cymraeg)',
                'verbose_name_plural': 'Individual SFIA Skills (Cymraeg)',
            },
        ),
        migrations.CreateModel(
            name='cy_SkillJSON',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
            options={
                'verbose_name': 'SFIA JSON file (Cymraeg)',
                'verbose_name_plural': 'SFIA JSON files (Cymraeg)',
            },
        ),
        migrations.CreateModel(
            name='en_Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Individual SFIA Skill (English)',
                'verbose_name_plural': 'Individual SFIA Skills (English)',
            },
        ),
        migrations.CreateModel(
            name='en_SkillJSON',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
            options={
                'verbose_name': 'SFIA JSON file (English)',
                'verbose_name_plural': 'SFIA JSON files (English)',
            },
        ),
        migrations.CreateModel(
            name='en_Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Generator.en_Skill')),
            ],
        ),
        migrations.CreateModel(
            name='cy_Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Generator.cy_Skill')),
            ],
        ),
    ]
