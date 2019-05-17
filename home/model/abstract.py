"""
Abstract base classes
"""
from django.db import models
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel


class InlineImage(models.Model):
    """
    Abstract class for embedding an image inline to a page
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        """
        abstract base class
        """
        abstract = True


class StaticPage(Page):
    """
    Abstract base class for a page
    """
    background_image = InlineImage.image
    content_panels = Page.content_panels + [
        ImageChooserPanel('background_image'),
    ]

    class Meta:
        """
        Meta class for a static page
        """
        abstract = True


class InfoTable(models.Model):
    """
    Information table

    This class can be used to store key value pairs in the database providing
    information about a thing.
    """
    key = models.CharField(max_length=16)
    value = models.CharField(max_length=32)

    panels = [
        FieldPanel('key'),
        FieldPanel('value'),
    ]

    class Meta:
        """
        abstract base class
        """
        abstract = True


class SkillsTable(models.Model):
    """
    A class which indicates a percentage (out of 100) of a thing
    """
    skill = models.CharField(max_length=32)
    percentage = models.IntegerField()

    panels = [
        FieldPanel('skill'),
        FieldPanel('percentage'),
    ]

    class Meta:
        """
        Abstract base class
        """
        abstract = True
