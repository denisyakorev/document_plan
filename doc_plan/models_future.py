from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("project_name"))
    aim_action = models.TextField(blank=True, verbose_name=_("aim_action"))
    aim_auditory = models.TextField(blank=True, verbose_name=_("aim_auditory"))
    aim_content = models.TextField(blank=True, verbose_name=_("aim_content"))
    reaction_action = models.TextField(blank=True, verbose_name=_("reaction_action"))
    reaction_standart = models.TextField(blank=True, verbose_name=_("reaction_standart"))
    auditory_profiles = models.ManyToManyField("AuditoryProfile", null=True, blank=True, verbose_name=_("auditory_profiles"))
    questions = models.ManyToManyField("Question", null=True, blank=True, verbose_name=_("questions"))
    chapters = models.ManyToManyField("Chapter", null=True, blank=True, verbose_name=_("chapters"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")


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


class Question(models.Model):
    ACTION = "a"
    KNOWLEDGE = "k"
    TYPES_CHOISES = (
        (ACTION, "action"),
        (KNOWLEDGE, "knowledge"),
    )

    text = models.CharField(max_length=1000, verbose_name=_("question_text"))
    question_type = models.CharField(max_length=2, choises=TYPES_CHOISES, default=ACTION)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")


class Chapter(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("chapter_name"))
    questions = models.ManyToManyField(Question, blank=True, null=True, verbose_name=_("questions"))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("chapter")
        verbose_name_plural = _("chapters")



