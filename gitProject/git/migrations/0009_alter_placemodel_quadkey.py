# Generated by Django 5.0.1 on 2024-02-11 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0008_placemodel_quadkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placemodel',
            name='quadkey',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
