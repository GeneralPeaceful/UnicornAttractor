# Generated by Django 2.0.2 on 2019-08-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuetracker', '0002_auto_20190803_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('To do', 'To do 2'), ('In Progress', 'In Progress'), ('Complete', 'Complete')], default='To do', max_length=20),
        ),
    ]
