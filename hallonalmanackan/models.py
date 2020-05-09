from django.db import models


class Holiday(models.Model):
    year = models.IntegerField(db_index=True)
    month = models.SmallIntegerField()
    day = models.SmallIntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('year', 'month', 'day')
