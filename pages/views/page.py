"""Implements page details view for content management system"""

from datetime import datetime
from hashlib import md5

from django.http import HttpResponseForbidden, Http404
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control
from django.views.decorators.http import condition
from django.shortcuts import render
from django.utils.translation import get_language
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from guardian.shortcuts import get_perms
from appcore.views.mixins import DecoratorChainingMixin

from pages.conf import settings
from pages.cache import cache
from pages.models import Page
from pages.models import PageContentType
from pages.models import PageSlugContent
from pages.models import PageRedirectContent


def get_timestamp(slug, language):
    # try get page modification timestamp for http caching
    page_cache_version_key = settings.PAGES_PAGE_VERSION_KEY + language + ':' + slug
    timestamp_cache_key = settings.PAGES_PAGE_CACHE_KEY + language + ':' + slug + '_timestamp'
    cache_version = cache.get(page_cache_version_key)
    cache_version = 0 if cache_version is None else cache_version
    timestamp = cache.get(timestamp_cache_key, version=cache_version)
    if timestamp is None:
        timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        cache.set(timestamp_cache_key, timestamp, settings.PAGES_PAGE_CACHE_TIMEOUT, version=cache_version)
    return timestamp


def get_etag(request, **kwargs):
    is_authenticated = str(request.user.is_authenticated())
    slug = kwargs.get('slug', None)
    language = get_language()
    modified = get_timestamp(slug, language)
    etag_bytes = (modified + language + is_authenticated).encode('utf-8')
    return md5(etag_bytes).hexdigest()


def get_last_modified(request, **kwargs):
    slug = kwargs.get('slug', None)
    language = get_language()
    modified = get_timestamp(slug, language)
    return datetime.strptime(modified, '%Y-%m-%d %H:%M:%S')


class PageDetailsView(DecoratorChainingMixin, TemplateView):

    decorators = [cache_control(must_revalidate=True, proxy_revalidate=True, max_age=settings.PAGES_PAGE_HTTP_MAX_AGE),
                  condition(etag_func=get_etag, last_modified_func=get_last_modified)]

    def get(self, request, **kwargs):
        is_authenticated = str(request.user.is_authenticated())
        slug = kwargs.get(settings.PAGES_PAGE_SLUG_NAME, None)
        if slug is None:
            raise Http404
        language = get_language()

        page_cache_key = settings.PAGES_PAGE_CACHE_KEY + language + ':' + slug + ':' + is_authenticated
        page_cache_version_key = settings.PAGES_PAGE_VERSION_KEY + language + ':' + slug

        # try get cached pages
        cache_version = cache.get(page_cache_version_key)
        cache_version = 0 if cache_version is None else cache_version
        page = cache.get(page_cache_key, version=cache_version)

        if page:
            # check if login required
            if page.is_login_required and not request.user.is_authenticated():
                return HttpResponseRedirect(settings.LOGIN_URL)

            # check user view permission
            if page.is_permission_required:
                if 'view_page' not in get_perms(request.user, page):
                    if settings.PAGES_RAISE_403:
                        raise PermissionDenied
                    if settings.PAGES_RENDER_403:
                        return render(request, settings.PAGES_TEMPLATE_403, {})
                    else:
                        return HttpResponseForbidden()

            # try get pages content from cache
            page_redirect = cache.get(page_cache_key + 'redirect', version=cache_version)
            if page_redirect:
                if page_redirect['permanent']:
                    return HttpResponsePermanentRedirect(page_redirect['url'])
                else:
                    return HttpResponseRedirect(page_redirect['url'])

            page_content = cache.get(page_cache_key + 'content', version=cache_version)
            page_ext_content = cache.get(page_cache_key + 'ext_content', version=cache_version)

        else:
            # try request pages from db and store pages content in cache
            slugs = PageSlugContent.objects.filter(slug=slug, language=language)
            if not slugs:
                raise Http404
            slug = slugs[0]
            try:
                page = Page.objects.published().filter(pk=slug.page_id)[0]

                # cache pages content
                cache.set(page_cache_version_key, cache_version)
                cache.set(page_cache_key, page, version=cache_version)

                # check if login required
                if page.is_login_required and not request.user.is_authenticated():
                    return HttpResponseRedirect(settings.LOGIN_URL)

                # check user view permission
                if page.is_permission_required:
                    if 'view_page' not in get_perms(request.user, page):
                        if settings.PAGES_RAISE_403:
                            raise PermissionDenied
                        if settings.PAGES_RENDER_403:
                            return render(request, settings.PAGES_TEMPLATE_403, {})
                        else:
                            return HttpResponseForbidden()

                page_content = {}
                page_ext_content = {}
                page_redirect = {}

                # check if this pages has redirect
                try:
                    redirect = PageRedirectContent.objects.get(page=page, language=language)
                    page_redirect.update({
                        'url': redirect.get_redirect_url(request),
                        'permanent': redirect.is_permanent
                    })
                    cache.set(page_cache_key + 'redirect', page_redirect, version=cache_version)
                    if page_redirect['permanent']:
                        return HttpResponsePermanentRedirect(page_redirect['url'])
                    else:
                        return HttpResponseRedirect(page_redirect['url'])

                except PageRedirectContent.DoesNotExist:
                    content_types = PageContentType.objects.filter(is_extended=False)
                    for content_type in content_types:
                        content_class = Page.get_content_class(content_type.type)
                        content = content_class.objects.filter(page=page, language=language)
                        if content:
                            page_content.update({content_type.type: content})

                    if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
                        ext_content_types = PageContentType.objects.extended()
                        for content_type in ext_content_types:
                            content_class = Page.get_content_class(content_type.type)
                            ext_content = content_class.objects.filter(page=page, language=language)
                            if ext_content:
                                page_ext_content.update({content_type.type: ext_content})

                if page_content:
                    cache.set(page_cache_key + 'content', page_content, version=cache_version)
                if page_ext_content:
                    cache.set(page_cache_key + 'ext_content', page_ext_content, version=cache_version)

            except IndexError:
                raise Http404

        context = {
            'page': {
                'page': page,
                'slug': slug,
                'content': page_content,
                'ext_content': page_ext_content,
                'cache_key': page_cache_key,
                'cache_version': cache_version,
                'timeout': settings.PAGES_PAGE_CACHE_TIMEOUT,
            }

        }

        return render(request, page.get_template(), context)
