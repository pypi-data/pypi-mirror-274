# Generated by Django 5.0.4 on 2024-05-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nets_core', '0010_permission_role_userrole_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled?'),
        ),
    ]
