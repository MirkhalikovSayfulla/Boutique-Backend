# Generated by Django 3.1.4 on 2020-12-29 11:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stars',
            field=models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]
