# Generated by Django 3.1.5 on 2021-01-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=1, max_digits=4)),
                ('unit', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/static/images/')),
            ],
        ),
    ]
