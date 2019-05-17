"""
Provides classes which form parts of (blocks of) a page
"""
from django.db import models
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey

from taggit.managers import TaggableManager
from home.model.abstract import (
    InlineImage,
    InfoTable,
    SkillsTable
)


class ColumnBlock(blocks.StructBlock):
    """
    Used for columur layouts
    """
    image = ImageChooserBlock()
    body = blocks.RichTextBlock(classname='full')
    url = blocks.URLBlock()


class SectionBlock(blocks.StructBlock):
    """
    A section wrapper block
    """
    title = blocks.CharBlock(max_length=64, default='please populate')
    body = blocks.RichTextBlock(blank=True)
    image = ImageChooserBlock(required=False)


class EducationTable(models.Model):
    """
    A class which is used to store a detail about a persons education
    """
    course = models.CharField(max_length=32)
    qualification = models.CharField(max_length=32)
    date_from = models.DateField("Date From")
    date_to = models.DateField("Date To")
    description = RichTextField(blank=True)


class ExperienceTable(models.Model):
    """
    A class which is used to store a detail about a persons work experience
    """
    company = models.CharField(max_length=32)
    role = models.CharField(max_length=32)
    date_from = models.DateField("Date From")
    date_to = models.DateField("Date To")
    description = RichTextField(blank=True)


class AboutPageDetailsTable(Orderable, InfoTable):
    """
    Link the InfoTable class to the AboutPage class
    """
    page = ParentalKey(
        'home.AboutPage',
        on_delete=models.CASCADE,
        related_name='details'
    )


class AboutPageSkillsTable(Orderable, SkillsTable):
    """
    Link the SkillsTable class to the AboutPage class
    """
    page = ParentalKey(
        'home.AboutPage',
        on_delete=models.CASCADE,
        related_name='skills'
    )


class ResumeEducationTable(Orderable, EducationTable):
    """
    Link the EducationTable to the Resume class
    """
    page = ParentalKey(
        'home.ResumePage',
        on_delete=models.CASCADE,
        related_name='education'
    )


class ResumeExperienceTable(Orderable, ExperienceTable):
    """
    Link the ExperienceTable to the Resume class
    """
    page = ParentalKey(
        'home.ResumePage',
        on_delete=models.CASCADE,
        related_name='experience'
    )


class GalleryTable(InlineImage):
    """
    A gallery item
    """
    title = models.CharField(max_length=32)
    description = RichTextField(blank=True)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('description', classname='full'),
    ]
    tags = TaggableManager()


class PortfolioGalleryTable(Orderable, GalleryTable):
    """
    Link the GalleryTable to the Portfolio class
    """
    page = ParentalKey(
        'home.PortfolioPage',
        on_delete=models.CASCADE,
        related_name='gallery'
    )


class FriendsGalleryTable(Orderable, GalleryTable):
    """
    Link the Gallery to the Friends class
    """
    page = ParentalKey(
        'home.FriendsPage',
        on_delete=models.CASCADE,
        related_name='gallery'
    )
