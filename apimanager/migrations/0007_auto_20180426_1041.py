# Generated by Django 2.0.4 on 2018-04-26 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apimanager', '0006_auto_20180420_0632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restapitestcase',
            name='successed',
        ),
        migrations.AlterField(
            model_name='validate',
            name='comparator',
            field=models.CharField(choices=[('equals', '=='), ('less_than', '<'), ('less_than_or_equals', '<='), ('greater_than', '>'), ('greater_than_or_equals', '>='), ('not_equals', '!='), ('string_equals', 'string_equals'), ('length_equals', 'length_equals'), ('length_greater_than', 'length_greater_than'), ('length_greater_than_or_equals', 'length_greater_than_or_equals'), ('length_less_than', 'length_less_than'), ('length_less_than_or_equals', 'length_less_than_or_equals'), ('contains', 'contains'), ('contained_by', 'contained_by'), ('type_match', 'type_match'), ('regex_match', 'regex_match'), ('startswith', 'startswith'), ('endswith', 'endswith')], max_length=50),
        ),
    ]
