# Generated by Django 5.1 on 2024-08-10 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0009_alter_option_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='surveyquestion',
            options={'ordering': ['order']},
        ),
    ]
