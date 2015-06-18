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
    animation = models.CharField(max_length="10", choices=PLUGIN_ANIMATION, default='fade')
    title = models.CharField(max_length="100", blank=True, default='')
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
    

    album = FilerFolderField(verbose_name=_('album'))

    @property
    def images(self):
        if not hasattr(self, '__images'):
            files = self.album.files
            self.__images = [f for f in files if f.file_type == 'Image']
            self.__images.sort()
        return self.__images

    @property
    def size(self):
        if self.width and self.height:
            return "%dx%d" % (self.width, self.height)
