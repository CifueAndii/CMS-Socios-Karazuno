from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class HomePage(Page):
    carrusel = StreamField([
        ('imagen', ImageChooserBlock(required=True)),
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('carrusel'),
    ]
