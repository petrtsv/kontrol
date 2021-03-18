import datetime
from uuid import uuid4

from django.db import models


class Session(models.Model):
    name = models.CharField(max_length=128)
    token = models.UUIDField(default=uuid4, editable=False, unique=True)
    create_date = models.DateTimeField('date created', default=datetime.datetime.now())
    update_date = models.DateTimeField('date updated', default=datetime.datetime.now())
    progress = models.FloatField(default=0.0)
    millis_left = models.BigIntegerField(default=0)

    class Status(models.IntegerChoices):
        STATUS_NOT_STARTED = 0
        STATUS_RUNNING = 1
        STATUS_DONE = 2

    status = models.IntegerField(choices=Status.choices, default=Status.STATUS_NOT_STARTED)

    @property
    def is_running(self):
        return self.status == self.Status.STATUS_RUNNING

    @property
    def progress_percent(self):
        return round(100 * self.progress, 1)

    @property
    def time_left(self):
        return str(datetime.timedelta(milliseconds=self.millis_left))

    def __str__(self):
        return 'Session "%s" created %s' % (str(self.name), str(self.create_date))


class Plot(models.Model):
    class Type(models.IntegerChoices):
        TYPE_LINE = 1
        TYPE_SCATTER = 2
        TYPE_IMAGE = 3

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    type = models.IntegerField(choices=Type.choices)
    title = models.CharField(max_length=64)

    def __str__(self):
        return 'Plot "%s" of session "%s"' % (str(self.title), str(self.session.name))


class Point(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)

    x_value = models.FloatField()
    y_value = models.FloatField()
    group = models.CharField(max_length=64)

    def __str__(self):
        return '"%s", x=%.3f y=%.3f' % (self.group, self.x_value, self.y_value)


class ImageData(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    add_date = models.DateTimeField('date added', default=datetime.datetime.now())
    value = models.ImageField(upload_to='uploaded/images')
