# Generated by Django 5.0.1 on 2024-02-14 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0011_alter_placemodel_quadkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placemodel',
            name='quadkey',
            field=models.CharField(db_index=True, default=1, max_length=30),
            preserve_default=False,
        ),
    ]