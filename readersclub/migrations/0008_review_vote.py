# Generated by Django 2.0.8 on 2018-12-13 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readersclub', '0007_auto_20181213_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='vote',
            field=models.IntegerField(default=0),
        ),
    ]