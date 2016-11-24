from __future__ import unicode_literals

from django.contrib import admin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from models import SliderPluginModel, Image


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1

class SliderPlugin(CMSPluginBase):
    model = SliderPluginModel
    name = _("Slider Plugin")
    inlines = [ImageInline, ]
    render_template = "djangocms_slider/slider.html"
    fieldsets = (
        (None, {
            'fields': ('animation', 'anim_speed', 'pause_time',)
        }),
        (_('Controls'), {
            'fields': ('arrows','paginator',)
        }),
        (_('Style'), {
            'fields': (('margin','min_slides', 'max_slides'),
            ('width', 'height'),)
        }),
    )

    def render(self, context, instance, placeholder):
        context.update({
        	'object': instance,
        	'images':instance.images.all()
        })
        return context


plugin_pool.register_plugin(SliderPlugin)
