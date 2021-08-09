# Generated by Django 3.0 on 2020-06-12 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('withdraw_date', models.DateField()),
                ('status', models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('F', 'Failed')], default='P', max_length=1)),
                ('request_amount', models.IntegerField(default=1)),
            ],
            options={
                'ordering': ['-withdraw_date'],
            },
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('blood_volume', models.IntegerField(default=0)),
                ('receive_date', models.DateField(auto_now_add=True)),
                ('expire_date', models.DateField()),
                ('expire_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('withdraw_date', models.DateField()),
                ('blood_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraws', to='core.BloodRequest')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraws', to='core.Hospital')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraws', to='core.Stock')),
            ],
            options={
                'ordering': ['-withdraw_date'],
            },
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloodrequests', to='core.Hospital'),
        ),
        migrations.AddField(
            model_name='bloodrequest',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bloodreuqests', to='core.Stock'),
        ),
        migrations.CreateModel(
            name='BloodDonation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_volume', models.IntegerField(default=0)),
                ('donate_date', models.DateField(auto_now_add=True)),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blooddonations', to='core.Stock')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blooddonations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-donate_date'],
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donate_date', models.DateField(help_text='YYYY-MM-DD', verbose_name='Appointment Date')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('C', 'Completed'), ('F', 'Failed')], default='P', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]