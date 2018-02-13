from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("project_name"))
    aim_action = models.TextField(blank=True, verbose_name=_("aim_action"))
    aim_auditory = models.TextField(blank=True, verbose_name=_("aim_auditory"))
    aim_content = models.TextField(blank=True, verbose_name=_("aim_content"))
    reaction_action = models.TextField(blank=True, verbose_name=_("reaction_action"))
    reaction_standart = models.TextField(blank=True, verbose_name=_("reaction_standart"))
    auditory_profile = models.ForeignKey("AuditoryProfile", on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("auditory_profiles"))
    question_actions = models.TextField(blank=True, verbose_name=_("question_actions"))
    question_knowledges = models.TextField(blank=True, verbose_name=_("question_knowledges"))
    chapters = models.ManyToManyField("Chapter", blank=True, verbose_name=_("chapters"))
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ["-created_at"]


class AuditoryProfile(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("auditory_name"))
    duty = models.TextField(blank=True, verbose_name=_("auditory_duty"))
    knowledge = models.TextField(blank=True, verbose_name=_("auditory_knowledge"))
    demography = models.TextField(blank=True, verbose_name=_("auditory_demography"))
    relations = models.TextField(blank=True, verbose_name=_("auditory_relations"))
    environment = models.TextField(blank=True, verbose_name=_("auditory_environment"))
    resume = models.TextField(blank=True, verbose_name=_("auditory_resume"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("auditory")
        verbose_name_plural = _("auditories")


class Chapter(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("chapter_name"))
    questions = models.TextField(blank=True, verbose_name=_("questions"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("chapter")
        verbose_name_plural = _("chapters")



