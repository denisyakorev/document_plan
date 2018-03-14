from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from doc_plan.utils import add_plan_data
from wkhtmltopdf.views import PDFTemplateView
from doc_plan.models import Project, Chapter
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from doc_plan.forms import PlanForm, ChapterForm
from precise_bbcode.bbcode import get_parser
from django.urls import reverse
from django.views.generic.list import ListView


class PlanContextMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(PlanContextMixin, self).get_context_data(**kwargs)
        try:
            context = add_plan_data(self.request, context=context, plan_id=context['plan_id'])
        except KeyError:
            context = add_plan_data(self.request, context=context)

        context['plan_creation_url'] = reverse('plan_creation')
        context['new_plan_url'] = reverse('edit_plan', args=['new'])

        return context



class ProjectListView(ListView, PlanContextMixin):
    model = Project
    context_object_name = 'plans'
    template_name = 'plan/plans.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.filter(created_by=self.request.user)
        return queryset


class LandingView(TemplateView, PlanContextMixin):
	template_name = 'landing/content.html'


class PlanView(TemplateView, PlanContextMixin):
	template_name = 'plan/plan_view.html'


class PlanPDF(PDFTemplateView, PlanContextMixin):
    template_name = 'plan/plan_pdf/plan_pdf.html'

    def get_filename(self):
        plan = Project.objects.get(id=self.kwargs['plan_id'])
        return 'plan_'+ str(plan.id) + ".pdf"


class PlanPdfView(TemplateView, PlanContextMixin):
    template_name = 'plan/plan_pdf/plan_pdf.html'


class PlanEditView(TemplateView):
    """Класс, содержащий методы, необходимые для редактирования плана"""
    template_name = 'plan/plan_edit.html'
    #Id плана, который будет использоваться для предзаполнения шаблона редактирования
    default_plan_id = None
    #Id плана, используемого в качестве примера правильного заполнения
    sample_plan_id = 1

    def get_context_data(self, **kwargs):
        """Формирование контекста для редактирования плана"""
        context = {
            'edit': True,
            'sample_plan_id': self.sample_plan_id,
            'sample_plan_url': reverse('view_plan', args=[self.sample_plan_id]),
            'about_method_url': reverse('plan_creation'),
        }

        if kwargs['plan_id'] == 'new':
            #Если формируем новый план, то шаблон может быть предзаполнен какими-то данными, либо пустым
            try:
                plan = Project.objects.get(id=self.default_plan_id)
            except Project.DoesNotExist:
                plan =  _('Название нового плана')

            context['plan'] = plan
        else:
            context = add_plan_data(self.request, context, kwargs['plan_id'])

        return context


    def save_data(self, request, *args, **kwargs):
        """Метод для сохранения данных заполненного плана"""
        if request.method != "POST":
            return self.bad_request(message="incorrect method")

        #Проверяем данные плана
        plan = request.POST.get('plan', None)
        if plan == None:
            return self.bad_request(message="plan does not exists")
        else:
            plan = json.loads(plan)

        # Проверяем данные разделов
        chapters = request.POST.get('chapters', None)
        if chapters != None:
            chapters = json.loads(chapters)

        errors = {
            'plan': [],
            'chapters': [],
        }

        cleaned_data = {
            'plan': [],
            'chapters': [],
        }

        #Проверяем данные при помощи формы
        plan_form = PlanForm(plan)
        if not plan_form.is_valid():
            errors['plan'].append(plan_form.errors)
        else:
            cleaned_data['plan'] = plan_form.get_cleaned_plan(request, kwargs)

        if chapters:
            for chapter in chapters:
                #Проверяем данные каждой главы при помощи формы
                chapter_form = ChapterForm(chapter)
                if not chapter_form.is_valid():
                    errors['chapters'].append(chapter_form.get_chapter_errors())
                else:
                    cleaned_data['chapters'].append(chapter_form.get_cleaned_chapter())

        #Если проверка плана и глав пройдена успешно - сохраняем
        if not errors['plan'] and not errors['chapters']:
            saved_chapters = Chapter.objects.save_chapters(cleaned_data['chapters'])
            new_plan_id = Project.objects.save_plan(cleaned_data['plan'], saved_chapters)

            if new_plan_id:
                response = HttpResponse(json.dumps({'plan_id': new_plan_id}),
                             content_type='application/json')
                response.status_code = 200
                return response

        return self.bad_request(message="Incorrect data", errors=errors)


    def delete_plan(self, request, *args, **kwargs):
        """Метод удаления плана"""
        try:
            plan = Project.objects.get(created_by=request.user,
                                   id=kwargs['plan_id'])
        except Project.DoesNotExist:
            raise Http404("Plan does not exist")

        plan.delete()
        return HttpResponseRedirect('/accounts/profile/')


    def get_chapters_data(self, request, *args, **kwargs):
        """Метод получения данных о разделах указанного плана"""
        context = {}

        # Если создаётся новый план - в его id присутствует "new"
        if kwargs['plan_id'] == 'new':
            chapters = []
        else:
            context = add_plan_data(request, context={}, plan_id=kwargs['plan_id'])
            chapters = []
            #Преобразовываем данных из bbcode (данные из клиента поступают в формате bbcode)
            parcer = get_parser()
            for chapter in context['chapters']:
                chapters.append({
                    'id': chapter.id,
                    'name': parcer.render(chapter.name),
                    'questions': parcer.render(chapter.questions)
                })

        response = HttpResponse(json.dumps({'chapters': chapters}),
                                content_type='application/json')
        response.status_code = 200
        return response


    def bad_request(self, **kwargs):
        """Метод формирования сообщения об ошибке для ajax запросов"""
        response_data = {}
        for elem in kwargs:
            response_data[elem] = kwargs[elem]
        response = HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        response.status_code = 400
        return response


