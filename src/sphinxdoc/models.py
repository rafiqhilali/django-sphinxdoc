"""
Models for django-sphinxdoc.

"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from sphinxdoc.validators import validate_isdir


class Project(models.Model):
    """Represents a Sphinx project. Each ``Project`` has a name, a slug and
    a path to the root directory of a Sphinx project (where Sphinx'
    ``conf.py``) is located).

    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,
                            help_text=_('Used in the URL for the project. '
                                        'Must be unique.'))
    path = models.CharField(max_length=255, validators=[validate_isdir],
                            help_text=_('Directory that contains Sphinx\' '
                                        '<tt>conf.py</tt>.'))

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __unicode__(self):
        return self.name

    def is_allowed(self, user):
        protected = getattr(settings, 'SPHINXDOC_PROTECTED_PROJECTS', {})
        if self.slug not in protected:
            # Project not protected, publicly visible
            return True
        is_denied = (not user.is_authenticated or
                     not user.has_perms(protected[self.slug]))
        if is_denied:
            return False
        return True

    def get_absolute_url(self):
        return reverse('doc-index', kwargs={'slug': self.slug})


class Document(models.Model):
    """Represents a JSON encoded Sphinx document. The attributes ``title`` and
    ``body`` dubicate the corresponding keys in ``content`` and are used for
    the Haystack search.

    """
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    path = models.CharField(max_length=255)
    content = models.TextField()
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __unicode__(self):
        return self.path

    def get_absolute_url(self):
        return reverse(
            'doc-detail', kwargs={'slug': self.project.slug, 'path': self.path})
