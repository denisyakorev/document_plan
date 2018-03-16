from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class PlanManager(models.Manager):

    def save_plan(self, plan_data, chapters):
        """Метод сохранения плана"""

        # Если создаётся новый план - в его id присутствует "new"
        if plan_data['id'] == 'new':
            # Перед сохранением удалим id, чтобы БД создала правильный
            del plan_data['id']
            plan = super().create(**plan_data)

        else:
            plan = super().get(created_by=plan_data['created_by'],
                                                                  id=plan_data['id'])
        if not plan:
            return False

        plan.update_plan(plan_data, chapters)

        return plan.id



class ChapterManager(models.Manager):

    def save_chapters(self, chapters_data):
        """Метод сохранения разделов"""
        chapters = []
        for chapter in chapters_data:
            #Если создаётся новый раздел - в его id присутствует "new"
            if "new" in chapter['id']:
                old_chapter = False
            else:
                old_chapter = super().get(id=chapter['id'])

            if not old_chapter:
                #Если создаём новый раздел - удалим сначала переданный с клиента id, чтобы создался новый
                del chapter['id']
                new_chapter = super().create(**chapter)
                chapters.append(new_chapter)
            else:
                old_chapter.update_chapter(chapter)
                chapters.append(old_chapter)

        return chapters


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("название проекта"))
    aim_action = models.TextField(blank=True, verbose_name=_("действие"))
    aim_auditory = models.TextField(blank=True, verbose_name=_("аудитория"))
    aim_content = models.TextField(blank=True, verbose_name=_("содержание"))
    reaction_action = models.TextField(blank=True, verbose_name=_("реакция"))
    reaction_standart = models.TextField(blank=True, verbose_name=_("стандарт"))
    auditory_duty = models.TextField(blank=True, verbose_name=_("обязанности"))
    auditory_knowledge = models.TextField(blank=True, verbose_name=_("знания"))
    auditory_demography = models.TextField(blank=True, verbose_name=_("демография"))
    auditory_relations = models.TextField(blank=True, verbose_name=_("отношения"))
    auditory_environment = models.TextField(blank=True, verbose_name=_("окружение"))
    auditory_resume = models.TextField(blank=True, verbose_name=_("выводы"))
    question_actions = models.TextField(blank=True, verbose_name=_("процедуры"))
    question_knowledges = models.TextField(blank=True, verbose_name=_("знания"))
    chapters = models.ManyToManyField("Chapter", blank=True, verbose_name=_("разделы"))
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = PlanManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('view_plan', args=[self.id])

    def get_edit_url(self):
        return reverse('edit_plan', args=[self.id])

    def get_delete_url(self):
        return reverse('delete_plan', args=[self.id])

    def get_download_url(self):
        return reverse('download_plan', args=[self.id])

    def update_plan(self, plan_data, chapters):
        self.name = plan_data['name']
        self.aim_action = plan_data['aim_action']
        self.aim_auditory = plan_data['aim_auditory']
        self.aim_content = plan_data['aim_content']
        self.reaction_action = plan_data['reaction_action']
        self.reaction_standart = plan_data['reaction_standart']
        self.auditory_duty = plan_data['auditory_duty']
        self.auditory_knowledge = plan_data['auditory_knowledge']
        self.auditory_demography = plan_data['auditory_demography']
        self.auditory_relations = plan_data['auditory_relations']
        self.auditory_environment = plan_data['auditory_environment']
        self.auditory_resume = plan_data['auditory_resume']
        self.question_actions = plan_data['question_actions']
        self.question_knowledges = plan_data['question_knowledges']
        self.chapters.clear()
        for chapter in chapters:
            self.chapters.add(chapter)

        self.save()
        return True

    class Meta:
        verbose_name = _("проект")
        verbose_name_plural = _("проекты")
        ordering = ["-created_at"]


class Chapter(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("название"))
    questions = models.TextField(blank=True, verbose_name=_("вопросы"))
    objects = ChapterManager()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def update_chapter(self, chapter):
        self.name = chapter['name']
        self.questions = chapter['questions']
        self.save()

    class Meta:
        verbose_name = _("раздел")
        verbose_name_plural = _("разделы")



