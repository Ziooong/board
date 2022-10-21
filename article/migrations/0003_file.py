# Generated by Django 4.1 on 2022-10-21 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0002_reply"),
    ]

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("o_filename", models.CharField(max_length=1000)),
                ("s_filename", models.CharField(max_length=1000)),
                ("filesize", models.IntegerField(default=0)),
            ],
        ),
    ]
