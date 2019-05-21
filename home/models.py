"""
Base models for Kahlua template
"""
from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel
)

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin

# pylint: disable=unused-import
from .model.blocks import (  # noqa: F401
    AboutPageDetailsTable,
    AboutPageSkillsTable,
    ResumeEducationTable,
    ResumeExperienceTable,
    PortfolioGalleryTable,
    FriendsGalleryTable
)

from .model.abstract import InlineImage, StaticPage


class ResumePage(StaticPage):
    """
    Model for a resume
    """
    onepage_template = 'home/sections/resume.html'
    content_panels = StaticPage.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('education', label='Education')
            ],
            heading="Education",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                InlinePanel('experience', label='Experience'),
            ],
            heading="Exerience",
            classname="collapsible collapsed"
        ),
    ]


class PortfolioPage(StaticPage):
    """
    Model for a portfolio - used as a gallery
    """
    onepage_template = 'home/sections/portfolio.html'
    content_panels = StaticPage.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('gallery', label='Photo')
            ],
            heading="Gallery",
            classname="collapsible"
        ),
    ]

    def get_child_tags(self):
        """
        Gets the child tags for the current item, particularly, image tags
        """
        tags = []
        for item in self.gallery.all():
            tags += item.image.tags.all()
        tags = sorted(set(tags))
        return tags


class FriendsPage(StaticPage):
    """
    Used to provide information about a "friend"
    """
    onepage_template = 'home/sections/portfolio.html'
    description = RichTextField(blank=True)

    content_panels = StaticPage.content_panels + [
        FieldPanel('description', classname='full'),
        MultiFieldPanel(
            [
                InlinePanel('gallery', label='Photo')
            ],
            heading="Gallery",
            classname="collapsible"
        ),
    ]

    def get_child_tags(self):
        """
        Gets the child tags for the current item, particularly, image tags
        """
        tags = []
        for item in self.gallery.all():
            tags += item.image.tags.all()
        tags = sorted(set(tags))
        return tags


class AboutPage(StaticPage, InlineImage):
    """
    A full about me section
    """
    onepage_template = 'home/sections/about.html'
    friends = FriendsPage.objects.live()
    body = RichTextField(blank=True)

    content_panels = StaticPage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('body', classname='full'),
                ImageChooserPanel('image'),
                MultiFieldPanel(
                    [
                        InlinePanel(
                            'details',
                            label='Details',
                            heading='Information'
                        ),
                    ],
                    heading="Information",
                    classname="collapsible collapsed"
                ),
            ],
            heading="About sections",
            classname="collapsible"
        ),
        MultiFieldPanel(
            [
                InlinePanel('skills', label='Skills'),
            ],
            heading="Skills",
            classname="collapsible collapsed"
        ),
    ]


class HomePage(RoutablePageMixin, StaticPage):
    """
    The home page of the application
    """
    onepage_template = 'home/sections/intro.html'
    parent_page_types = [
        'wagtailcore.Page',
    ]
    strapline = models.CharField(max_length=128, blank=True)

    content_panels = StaticPage.content_panels + [
        FieldPanel('strapline'),
    ]
    subpage_types = [AboutPage, PortfolioPage, ResumePage, FriendsPage]

    def get_subsections(self):
        """
        Return page queryset with sections to render on the HomePage.
        """
        return (
            self
            .get_children()
            .specific()
            .live()
            .public()
        )

    def get_context(self, request, *args, **kwargs):
        """
        Gets the current context
        """
        context = super().get_context(request, args, kwargs)
        context['subsections'] = self.get_subsections()
        context['nav_sections'] = self.get_subsections().in_menu()
        return context
