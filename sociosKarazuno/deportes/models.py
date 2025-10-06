from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class DeportePage(Page):
    resumen = models.CharField(max_length=255, blank=True)
    descripcion = RichTextField(blank=True)
    entrenador = models.CharField(max_length=150, blank=True)
    horario = models.CharField(max_length=255, blank=True)
    ubicacion = models.CharField(max_length=255, blank=True)
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel('resumen'),
        FieldPanel('descripcion'),
        MultiFieldPanel([
            FieldPanel('entrenador'),
            FieldPanel('horario'),
            FieldPanel('ubicacion'),
        ], heading="Detalles"),
        FieldPanel('imagen'),
    ]


class DeporteIndexPage(Page):
    # Página para listar todos los deportes (hija de Home)
    subpage_types = ['DeportePage']
    def get_context(self, request):
        context = super().get_context(request)
        context['deportes'] = DeportePage.objects.live().public()
        return context