# Generated by Django 2.0.8 on 2018-12-13 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readersclub', '0006_auto_20181213_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='pseudonym',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
