from django.db import models
# from Cython.Compiler.TypeSlots import descrdelfunc



class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to="article_images")
    thumb = models.ImageField(upload_to="article_thumbs")
