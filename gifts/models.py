# coding: utf-8

import os.path
import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from utils import ImageWithThumbsField


def get_file_path(instance, filename):
    _, ext = filename.rsplit('.', 1)
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('article', filename)


class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    img = ImageWithThumbsField(upload_to=get_file_path, sizes=((1200, 750), (360, 225)))

    def __unicode__(self):
        return self.title


@receiver(post_delete, sender=Article)
def photo_post_delete_handler(sender, instance, **kwargs):
    instance.img.delete(False)
