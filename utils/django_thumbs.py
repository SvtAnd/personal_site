# coding: utf-8

from io import BytesIO

from django.db.models.fields.files import ImageField, ImageFieldFile
from django.core.files.base import ContentFile

from PIL import Image, ImageOps


class ImageWithThumbsFieldFile(ImageFieldFile):

    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)

        if self.field.sizes:
            for size in self.field.sizes:
                setattr(self, 'url_%sx%s' % (size[0], size[1]),
                        self._make_thumb_name(self.url, size))

    @staticmethod
    def _make_thumb_name(name, size):
        base, extension = name.rsplit('.', 1)
        return '%s.%sx%s.%s' % (base, size[0], size[1], extension)

    @staticmethod
    def generate_thumb(original, size):
        """
        Generates a thumbnail image and returns a ContentFile object with the thumbnail
        :params original: The image being resized as `File`.
        :params size: desired thumbnail size as `tuple`. Example: (70, 100)
        """
        original.seek(0)
        image = Image.open(original)
        if image.mode not in ('L', 'RGB', 'RGBA'):
            image = image.convert('RGB')
        thumbnail = ImageOps.fit(image, size, Image.ANTIALIAS)
        _, ext = original.name.rsplit('.', 1)
        if ext.upper() == 'JPG':
            ext = 'JPEG'
        io = BytesIO()
        thumbnail.save(io, ext)
        return ContentFile(io.getvalue())

    def save(self, name, content, save=True):
        super(ImageWithThumbsFieldFile, self).save(name, content, save)

        if self.field.sizes:
            for size in self.field.sizes:
                thumb_content = self.generate_thumb(content, size)
                thumb_name = self._make_thumb_name(self.name, size)
                self.storage.save(thumb_name, thumb_content)

    def delete(self, save=True):
        if self.name and self.field.sizes:
            for size in self.field.sizes:
                thumb_name = self._make_thumb_name(self.name, size)
                try:
                    self.storage.delete(thumb_name)
                except:
                    pass
        super(ImageWithThumbsFieldFile, self).delete(save)


class ImageWithThumbsField(ImageField):
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)

    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200

    Note: The 'sizes' attribute is not required. If you don't provide it,
    ImageWithThumbsField will act as a normal ImageField

    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a
    thumbnail with that size and stores it following this format:

    available_filename.[width]x[height].extension

    Where 'available_filename' is the available filename returned by the storage
    backend for saving the original file.

    Following the usage example above: For storing a file called "photo.jpg" it saves:
    photo.jpg          (original file)
    photo.125x125.jpg  (first thumbnail)
    photo.300x200.jpg  (second thumbnail)
    """
    attr_class = ImageWithThumbsFieldFile
    #descriptor_class = ImageWithThumbsFileDescriptor

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes=None, **kwargs):
        self.verbose_name = verbose_name
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        self.sizes = sizes
        super(ImageField, self).__init__(**kwargs)
