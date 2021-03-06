from django.contrib import admin
from doc_plan.models import Project, Chapter, ChapterOrder
from django.utils.translation import ugettext_lazy as _


# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, 				 	{'fields': ['name']}),
		(_('Задачи проекта'), 	{'fields': ['aim_action', 'aim_auditory', 'aim_content', 'reaction_action', 'reaction_standart']}),
		(_('Аудитория'), 		{'fields': ['auditory_duty', 'auditory_knowledge', 'auditory_demography', 'auditory_relations', 'auditory_environment', 'auditory_resume']}),
		(_('Вопросы'), 			{'fields': ['question_actions', 'question_knowledges']}),
		(_('Служебная информация'), {'fields': ['created_by']}),
	]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Chapter)
admin.site.register(ChapterOrder)
