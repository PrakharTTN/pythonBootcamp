# Generated by Django 5.1.6 on 2025-02-25 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('item_image', models.ImageField(upload_to='image')),
                ('item_desc', models.TextField()),
                ('item_price', models.PositiveBigIntegerField()),
                ('item_rating', models.FloatField(max_length=100)),
            ],
        ),
    ]
