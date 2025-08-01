# Generated by Django 5.2.4 on 2025-07-22 19:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("flow", "0001_initial"),
        ("job_posting", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="candidateflow",
            name="hr_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="candidate_flows",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="candidateflow",
            name="job_posting",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="candidate_flows",
                to="job_posting.jobposting",
            ),
        ),
        migrations.AddField(
            model_name="candidateactivitylog",
            name="candidate_flow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="candidate_activities_log",
                to="flow.candidateflow",
            ),
        ),
        migrations.AddField(
            model_name="candidateflow",
            name="status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="candidate_flows",
                to="flow.status",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="candidateflow",
            unique_together={("job_posting", "candidate")},
        ),
    ]
