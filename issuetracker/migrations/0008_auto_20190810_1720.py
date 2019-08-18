# Generated by Django 2.0.2 on 2019-08-10 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0007_auto_20190803_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status_colour',
            field=models.CharField(choices=[('dark', 'To do'), ('warning', 'In Progress'), ('success', 'Complete')], default='dark', max_length=20),
        ),
    ]