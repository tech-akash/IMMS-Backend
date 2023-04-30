# Generated by Django 4.1.3 on 2023-04-29 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0007_registeredstudent'),
    ]

    operations = [
        migrations.CreateModel(
            name='TakenMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('breakfast', models.IntegerField()),
                ('lunch', models.IntegerField()),
                ('dinner', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='goldtoken',
            name='TokenExpiry',
            field=models.DateField(blank=True, null=True),
        ),
    ]