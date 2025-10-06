from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey

DEPORTES = [
    ("futbol", "Fútbol"),
    ("basquet", "Basquet"),
    ("voley", "Voley"),
    ("handball", "Handball"),
]

class TablaDePosicionesPage(Page):
    descripcion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("descripcion"),
        InlinePanel("equipos", label="Equipos por deporte"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        equipos_por_deporte = {}
        for key, nombre in DEPORTES:
            equipos_por_deporte[nombre] = self.equipos.filter(deporte=key).order_by("-puntos")
        context["equipos_por_deporte"] = equipos_por_deporte
        return context

class Equipo(models.Model):
    page = ParentalKey("resultados.TablaDePosicionesPage", on_delete=models.CASCADE, related_name="equipos")
    nombre = models.CharField(max_length=100)
    deporte = models.CharField(max_length=20, choices=DEPORTES, default="futbol")
    partidos_jugados = models.PositiveIntegerField(default=0)
    ganados = models.PositiveIntegerField(default=0)
    empatados = models.PositiveIntegerField(default=0)
    perdidos = models.PositiveIntegerField(default=0)
    puntos = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel("nombre"),
        FieldPanel("deporte"),
        FieldPanel("partidos_jugados"),
        FieldPanel("ganados"),
        FieldPanel("empatados"),
        FieldPanel("perdidos"),
        FieldPanel("puntos"),
    ]

    class Meta:
        ordering = ["-puntos", "-ganados"]

    def __str__(self):
        return f"{self.nombre} ({self.get_deporte_display()})"
