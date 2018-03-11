from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
import json
from doc_plan.forms import PlanForm, ChapterForm


# Create your models here.
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

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

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

    class Meta:
        verbose_name = _("проект")
        verbose_name_plural = _("проекты")
        ordering = ["-created_at"]


class Chapter(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("название"))
    questions = models.TextField(blank=True, verbose_name=_("вопросы"))

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



class PlanManager(models.Manager):

    @require_http_methods(["POST"])
    def save_data(self, request, *args, **kwargs):
        """Метод для сохранения данных заполненного плана"""

        errors = {}
        # Проверяем данные плана
        plan = request.POST.get('plan', None)
        if plan == None:
            return False

        plan = json.loads(plan)
        # Проверяем данные при помощи формы
        plan_form = PlanForm(plan)
        if not plan_form.is_valid():
            errors['plan'] = []
            errors['plan'].append(plan_form.errors)

        # Проверяем данные разделов
        chapters = request.POST.get('chapters', None)
        if chapters != None:
            chapters = json.loads(chapters)
            chapters_cleaned_data = []
            for chapter in chapters:
                # Проверяем данные каждой главы при помощи формы
                chapter_form = ChapterForm(chapter)
                if not chapter_form.is_valid():
                    errors['chapters'] = errors.get('chapters', [])
                    errors['chapters'].append({
                        'id': chapter['id'],
                        'errors': chapter_form.errors
                    })
                else:
                    chapter_data = chapter_form.cleaned_data
                    chapter_data['id'] = chapter['id']
                    chapters_cleaned_data.append(chapter_data)

        # Если проверка плана и глав пройдена успешно - сохраняем
        if not errors:
            saved_chapters = self.save_chapters(chapters_cleaned_data)
            plan_data = plan_form.cleaned_data
            plan_data['created_by'] = request.user
            plan_data['id'] = kwargs['plan_id']
            new_plan_id = self.save_plan(plan_data, saved_chapters)
            if new_plan_id:
                return True

        return False
