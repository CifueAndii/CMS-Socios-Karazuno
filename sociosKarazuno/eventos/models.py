from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class CategoriaEvento(models.Model):
    nombre = models.CharField(max_length=100)

    def _str_(self):
        return self.nombre

class EventoPage(Page):
    fecha_inicio = models.DateTimeField("Fecha y hora de inicio", default=timezone.now)
    fecha_fin = models.DateTimeField("Fecha y hora de fin", null=True, blank=True)
    lugar = models.CharField(max_length=255, blank=True, null=True)
    descripcion = RichTextField(blank=True)
    aforo = models.PositiveIntegerField(null=True, blank=True)
    inscripcion_abierta = models.BooleanField(default=False)

    color = models.CharField(
        max_length=7,
        default="#007bff",  # Azul por defecto
        help_text="Selecciona un color en formato HEX (por ejemplo: #FF5733)"
    )


    content_panels = Page.content_panels + [
        FieldPanel("fecha_inicio"),
        FieldPanel("fecha_fin"),
        FieldPanel('lugar'),
        FieldPanel("color"),
        FieldPanel('descripcion'),
        MultiFieldPanel([
            FieldPanel('aforo'),
            FieldPanel('inscripcion_abierta'),
        ], heading='Opciones de evento')
    ]

    #parent_page_types = ["eventos.CalendarioPage"]
    parent_page_types = ["eventos.EventoIndexPage"]

class EventoIndexPage(Page):
    template = "eventos/evento_index_page.html"
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    # para traer los eventos hijos
    def get_context(self, request):
        context = super().get_context(request)
        eventos = EventoPage.objects.child_of(self).live().order_by("fecha_inicio")
        context["eventos"] = eventos
        return context
    
class CalendarioPage(Page):
    template = "eventos/calendario_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        from eventos.models import EventoPage

        eventos = EventoPage.objects.live().public().order_by('fecha_inicio')
        context["eventos"] = eventos
        return context
    