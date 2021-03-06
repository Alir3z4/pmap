# Generated by Django 2.0.5 on 2018-05-23 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
            ],
            options={
                'verbose_name': 'Animal',
                'verbose_name_plural': 'Animals',
            },
        ),
        migrations.CreateModel(
            name='AnimalWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(verbose_name='weight')),
                ('weight_date', models.DateTimeField(verbose_name='weight date')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weights', to='livestock.Animal', verbose_name='animal')),
            ],
            options={
                'verbose_name': 'Animal Weight',
                'verbose_name_plural': 'Animal Weights',
            },
        ),
    ]
