# Generated by Django 3.2 on 2023-04-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='register',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
