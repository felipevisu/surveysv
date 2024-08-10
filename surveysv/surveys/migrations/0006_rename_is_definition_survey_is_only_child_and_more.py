# Generated by Django 5.1 on 2024-08-09 00:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_alter_surveyquestion_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='is_definition',
            new_name='is_only_child',
        ),
        migrations.CreateModel(
            name='SurveyInheritance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('child_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_links', to='surveys.survey')),
                ('parent_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_links', to='surveys.survey')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('parent_survey', 'child_survey')},
            },
        ),
        migrations.AddField(
            model_name='survey',
            name='parent_surveys',
            field=models.ManyToManyField(related_name='child_surveys', through='surveys.SurveyInheritance', to='surveys.survey'),
        ),
    ]
