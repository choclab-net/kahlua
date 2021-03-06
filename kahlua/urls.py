"""
Define URL patterns and match to handlers
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from blog import views as blog_views
from search import views as search_views

# pylint: disable=invalid-name
urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^blog/', include('blog.urls', namespace="blog")),

    url(r'^blog/tag/(?P<tag>[-\w]+)/', blog_views.tag_view, name="tag"),
    url(
        r'^blog/category/(?P<category>[-\w]+)/feed/$',
        blog_views.LatestCategoryFeed(),
        name="category_feed"
    ),
    url(
        r'^blog/category/(?P<category>[-\w]+)/',
        blog_views.category_view,
        name="category"
    ),
    url(
        r'^blog/author/(?P<author>[-\w]+)/',
        blog_views.author_view,
        name="author"
    ),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    # pylint: disable=ungrouped-imports
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
