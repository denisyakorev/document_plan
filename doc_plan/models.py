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
    auditory_duty = models.TextField(blank=True, verbose_name=_("auditory_duty"))
    auditory_knowledge = models.TextField(blank=True, verbose_name=_("auditory_knowledge"))
    auditory_demography = models.TextField(blank=True, verbose_name=_("auditory_demography"))
    auditory_relations = models.TextField(blank=True, verbose_name=_("auditory_relations"))
    auditory_environment = models.TextField(blank=True, verbose_name=_("auditory_environment"))
    auditory_resume = models.TextField(blank=True, verbose_name=_("auditory_resume"))
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


class Chapter(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("chapter_name"))
    questions = models.TextField(blank=True, verbose_name=_("questions"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("chapter")
        verbose_name_plural = _("chapters")



