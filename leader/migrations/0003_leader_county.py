# Generated by Django 2.0 on 2017-12-14 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leader', '0002_reviewing'),
    ]

    operations = [
        migrations.AddField(
            model_name='leader',
            name='county',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
