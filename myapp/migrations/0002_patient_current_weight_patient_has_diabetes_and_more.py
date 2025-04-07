# Generated by Django 4.2 on 2025-04-02 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='current_weight',
            field=models.FloatField(blank=True, help_text='Current weight in kg', null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='has_diabetes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='has_hypertension',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.FloatField(blank=True, help_text='Height in cm', null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='is_first_pregnancy',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='pre_pregnancy_weight',
            field=models.FloatField(blank=True, help_text='Weight in kg before pregnancy', null=True),
        ),
        migrations.CreateModel(
            name='NutritionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('calories', models.IntegerField()),
                ('protein', models.FloatField(help_text='Protein in grams')),
                ('carbs', models.FloatField(help_text='Carbohydrates in grams')),
                ('fats', models.FloatField(help_text='Fats in grams')),
                ('iron', models.FloatField(help_text='Iron in mg')),
                ('calcium', models.FloatField(help_text='Calcium in mg')),
                ('folate', models.FloatField(help_text='Folate in mcg')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutrition_logs', to='myapp.patient')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
