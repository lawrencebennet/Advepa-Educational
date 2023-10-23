from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Stand(models.Model):
    name = models.CharField(_("name"), max_length=150)
    info = models.TextField(_('info'), max_length=500, blank=True)

    class Meta:
        verbose_name = _("Stand")
        verbose_name_plural = _("Stands")

    def __str__(self):
        return self.name


class Pavilion(models.Model):
    name = models.CharField(_("name"), max_length=150)
    stands = models.ManyToManyField(Stand, blank=True)
    info = models.TextField(_('info'), max_length=500, blank=True)

    class Meta:
        verbose_name = _("Pavilion")
        verbose_name_plural = _("Pavilions")

    def __str__(self):
        return self.name


class Exhibition(models.Model):
    name = models.CharField(_("name"), max_length=150, unique=True)
    pavilions = models.ManyToManyField(Pavilion, blank=True)
    info = models.TextField(_('info'), max_length=500, blank=True)

    class Meta:
        verbose_name = _("Exhibition")
        verbose_name_plural = _("Exhibitions")

    def __str__(self):
        return self.name


class Action(models.Model):
    date = models.DateTimeField(blank=False)
    date_string = models.CharField(max_length=150, default='')
    user = models.CharField(max_length=150, blank=False)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    pavilion = models.ForeignKey(Pavilion, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    main_action = models.CharField(max_length=150, blank=False)
    action_detail = models.CharField(max_length=150)
    platform = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    region = models.CharField(max_length=150)
    province = models.CharField(max_length=150)
    municipality = models.CharField(max_length=150)
    geo_string = models.CharField(max_length=150, default='')

    class Meta:
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")

    def __str__(self):
        return f'{self.main_action}, {self.action_detail}'


class Import(models.Model):
    STATUS_CHOICES = (
        ('failed', 'Fallito'),
        ('success', 'Successo'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='failed', blank=False)
    imported_actions = models.IntegerField(default=0)
    exhibitions_updated = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()

    class Meta:
        verbose_name = _("Import")
        verbose_name_plural = _("Imports")


class GraphInteraction(models.Model):
    GRAPH_CHOICES = (
        ('access', 'Accessi'),
        ('actions', 'Azioni'),
    )
    graph = models.CharField(max_length=100, choices=GRAPH_CHOICES, default='actions', blank=False)
    time = models.DateTimeField()

    class Meta:
        verbose_name = _("Interaction")
        verbose_name_plural = _("Interactions")

