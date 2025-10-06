from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StructBlock, URLBlock


class MultimediaBlock(StructBlock):
    tipo = blocks.ChoiceBlock(
        choices=[
            ('imagen', 'Imagen'),
            ('video', 'Video (YouTube, Vimeo, etc.)'),
        ],
        default='imagen',
        label="Tipo de medio"
    )
    imagen = ImageChooserBlock(required=False)
    video_url = URLBlock(required=False, help_text="URL del video (YouTube, Vimeo, etc.)")
    descripcion = blocks.CharBlock(required=False, help_text="Descripción breve del contenido")

    class Meta:
        icon = "media"
        label = "Elemento multimedia"


class GaleriaPage(Page):
    descripcion = RichTextField(blank=True, features=["bold", "italic", "link"])
    elementos = StreamField(
        [("multimedia", MultimediaBlock())],
        use_json_field=True,
        blank=True,
        verbose_name="Galería de medios"
    )

    content_panels = Page.content_panels + [
        FieldPanel("descripcion"),
        FieldPanel("elementos"),
    ]

    class Meta:
        verbose_name = "Galería Multimedia"
        verbose_name_plural = "Galerías Multimedia"
