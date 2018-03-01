from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from doc_plan.utils import add_plan_data
from wkhtmltopdf.views import PDFTemplateView
from doc_plan.models import Project, Chapter
from django_ajax.decorators import ajax
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
import json
from doc_plan.forms import PlanForm, ChapterForm


# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'plans'
    template_name = 'plan/plans.html'
    paginate_by = 10


    def get_queryset(self):
        queryset = Project.objects.filter(created_by=self.request.user)
        return queryset


class PlanContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(PlanContextMixin, self).get_context_data(**kwargs)
        context = add_plan_data(self.request, context=context, plan_id=context['plan_id'])

        return context


class PlanView(TemplateView, PlanContextMixin):
	template_name = 'plan/plan_view.html'



class PlanPDF(PDFTemplateView, PlanContextMixin):
    filename = 'plan_pdf.pdf'
    template_name = 'plan/plan_pdf/plan_pdf.html'


class PlanPdfView(TemplateView, PlanContextMixin):
    template_name = 'plan/plan_pdf/plan_pdf.html'


class PlanEditView(TemplateView):
    template_name = 'plan/plan_edit.html'


    def get_context_data(self, **kwargs):
        context = {'edit': True}

        if kwargs['plan_id'] == 'new':
            plan = {'name': _('Название нового плана')}
            context['plan'] = plan
        else:
            context = add_plan_data(self.request, context, kwargs['plan_id'])

        return context



    def save_data(self, request, *args, **kwargs):

        if request.method != "POST":
            return self.bad_request(message="plan does not exists")

        errors = {}

        #Проверяем данные плана
        plan = request.POST.get('plan', None)
        if plan == None:
            return self.bad_request(message="plan does not exists")

        plan = json.loads(plan)
        plan_form = PlanForm(plan)
        if not plan_form.is_valid():
            errors['plan'] = []
            errors['plan'].append(plan_form.errors)

        #Проверяем данные разделов
        chapters = request.POST.get('chapters', None)
        if chapters != None:
            chapters = json.loads(chapters)
            chapters_cleaned_data = []
            for chapter in chapters:
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


        if not errors:
            saved_chapters = self.save_chapters(chapters_cleaned_data)
            plan_data = plan_form.cleaned_data
            plan_data['created_by'] = request.user
            plan_data['id'] = kwargs['plan_id']
            chapters = saved_chapters
            is_plan_saved = self.save_plan(plan_data, chapters)
            if is_plan_saved:
                return HttpResponse(json.dumps({'message': 'plan_saved'}),
                             content_type='application/json')



        return self.bad_request(message="Incorrect data", errors=errors)


    def save_chapters(self, chapters_data):
        chapters = []
        for chapter in chapters_data:
            print (chapter)
            if "new" in chapter['id']:
                old_chapter = False
            else:
                old_chapter = Chapter.objects.select_for_update().filter(id=chapter['id'])
            if not old_chapter:
                del chapter['id']
                new_chapter = Chapter.objects.create(**chapter)
                chapters.append(new_chapter)
            else:
                old_chapter.update(**chapter)
                old_chapter.save()
                chapters.append(old_chapter)

        return chapters



    def save_plan(self, plan_data, chapters):

        if plan_data['id'] == 'new':
            del plan_data['id']
            plan = Project.objects.create(**plan_data)

        else:
            plan = Project.objects.select_for_update().filter(created_by=plan_data['created_by'],
                                                                  id=plan_data['id'])
            if not plan:
                return False
            plan.update(**plan_data)

        plan.chapters.clear()
        for chapter in chapters:
            plan.chapters.add(chapter)

        plan.save()

        return True






    def get_chapters_data(self, request, *args, **kwargs):
        if kwargs['plan_id'] == 'new':
            chapters = []
        else:
            context = add_plan_data(request, context={}, plan_id=kwargs['plan_id'])
            chapters = context['chapters']

        response = HttpResponse(json.dumps({'chapters': chapters}),
                                content_type='application/json')

        return response


    def bad_request(self, **kwargs):
        response_data = {}
        for elem in kwargs:
            response_data[elem] = kwargs[elem]
        response = HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        response.status_code = 400
        return response


