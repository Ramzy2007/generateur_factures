# Generated by Django 5.1 on 2024-08-12 00:22

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('produit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailFacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField(default=1)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produit.produit')),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('produits', models.ManyToManyField(through='produit.DetailFacture', to='produit.produit')),
            ],
        ),
        migrations.AddField(
            model_name='detailfacture',
            name='facture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produit.facture'),
        ),
    ]
