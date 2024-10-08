# Generated by Django 5.1 on 2024-08-09 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('type', models.CharField(choices=[('MULTIPLE_CHOICE', 'Multiple Choice'), ('SELECT', 'Select'), ('TEXT', 'Text')])),
                ('required', models.BooleanField(blank=True, null=True)),
            ],
        ),
    ]
