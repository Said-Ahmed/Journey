# Generated by Django 5.0.1 on 2024-02-11 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0009_alter_placemodel_quadkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placemodel',
            name='quadkey',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
    ]