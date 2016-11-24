from __future__ import unicode_literals

from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from filer.fields.folder import FilerFolderField


class SliderPluginModel(CMSPlugin):
    PLUGIN_ANIMATION = (
            ('fade', "Fade"),
            ('slide', "Slide"),
        )
    animation = models.CharField(max_length=10, choices=PLUGIN_ANIMATION, default='fade')
    title = models.CharField(max_length=100, blank=True, default='')
    anim_speed = models.PositiveIntegerField(_('anim speed'), default=500,
                                      help_text=_("Animation Speed (ms)"))
    pause_time = models.PositiveIntegerField(_('pause time'), default=3000,
                                      help_text=_("Pause time (ms)"))
    margin = models.PositiveIntegerField(_('Margin slide'), default=0,
                                      help_text=_("Margin slide (px)"))
    min_slides = models.PositiveIntegerField(_('Min slide'), default=1,
                                      help_text=_("Minimal number slide"))
    max_slides = models.PositiveIntegerField(_('Max slide'), default=4,
                                      help_text=_("Maximun number slide"))
    width = models.PositiveIntegerField(_('width'), null=False, blank=False,
                                 help_text=_("Width of the plugin (px)"))
    height = models.PositiveIntegerField(_('height'), null=False, blank=False,
                                  help_text=_("Height of the plugin (px)"))
    arrows = models.BooleanField(_('arrows'), default=True,
                          help_text=_('Arrow buttons for navigation'))
    paginator = models.BooleanField(_('paginator'), default=True,
                          help_text=_('Paginator buttons for navigation'))

    @property
    def size(self):
        if self.width and self.height:
            return "%dx%d" % (self.width, self.height)

    def copy_relations(self, oldinstance):
        for image in oldinstance.images.all():
            image.pk = None
            image.slider = self
            image.save()


class Image(models.Model):

    class Meta:
        verbose_name_plural = _('images')
        pass

    slider = models.ForeignKey(SliderPluginModel, related_name="images")
    image = FilerImageField(related_name=_('image'),)
    title = models.TextField(_('title'),null=True,blank=True,)
    caption_text = models.TextField(_('caption text'),null=True,blank=True,)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.image.label
