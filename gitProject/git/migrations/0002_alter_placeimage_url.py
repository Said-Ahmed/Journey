# Generated by Django 5.0.1 on 2024-01-12 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeimage',
            name='url',
            field=models.FileField(blank=True, upload_to='images/place/%Y/%m/%d/'),
        ),
    ]
