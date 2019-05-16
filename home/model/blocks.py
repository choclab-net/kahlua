from django.db import models
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.core.models import Orderable, Page
from modelcluster.fields import ParentalKey

from taggit.managers import TaggableManager

class ColumnBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    body = blocks.RichTextBlock(classname='full')
    url = blocks.URLBlock()

class SectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=64, default='please populate')
    body = blocks.RichTextBlock(blank=True)
    image = ImageChooserBlock(required=False)

class InfoTable(models.Model):
    key = models.CharField(max_length=16)
    value = models.CharField(max_length=32)

    panels = [
        FieldPanel('key'),
        FieldPanel('value'),
    ]

    class Meta:
        abstract = True

class SkillsTable(models.Model):
    skill = models.CharField(max_length=32)
    percentage = models.IntegerField()

    panels = [
        FieldPanel('skill'),
        FieldPanel('percentage'),
    ]

    class Meta:
        abstract = True

class EducationTable(models.Model):
    course = models.CharField(max_length=32)
    qualification = models.CharField(max_length=32)
    date_from = models.DateField("Date From")
    date_to = models.DateField("Date To")
    description = RichTextField(blank=True)

class ExperienceTable(models.Model):
    company = models.CharField(max_length=32)
    role = models.CharField(max_length=32)
    date_from = models.DateField("Date From")
    date_to = models.DateField("Date To")
    description = RichTextField(blank=True)

class AboutPageDetailsTable(Orderable, InfoTable):
    page = ParentalKey('home.AboutPage', on_delete=models.CASCADE, related_name='details')

class AboutPageSkillsTable(Orderable, SkillsTable):
    page = ParentalKey('home.AboutPage', on_delete=models.CASCADE, related_name='skills')

class ResumeEducationTable(Orderable, EducationTable):
    page = ParentalKey('home.ResumePage', on_delete=models.CASCADE, related_name='education')

class ResumeExperienceTable(Orderable, ExperienceTable):
    page = ParentalKey('home.ResumePage', on_delete=models.CASCADE, related_name='experience')

class GalleryTable(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=32)
    description = RichTextField(blank=True)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('description', classname='full'),
    ]
    tags = TaggableManager()


class PortfolioGalleryTable(Orderable, GalleryTable):
    page = ParentalKey('home.PortfolioPage', on_delete=models.CASCADE, related_name='gallery')

class FriendsGalleryTable(Orderable, GalleryTable):
    page = ParentalKey('home.FriendsPage', on_delete=models.CASCADE, related_name='gallery')
