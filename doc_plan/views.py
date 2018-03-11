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
from django.views.decorators.http import require_http_methods


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
        }

        if kwargs['plan_id'] == 'new':
            #Если формируем новый план, то шаблон может быть предзаполнен какими-то данными, либо пустым
            try:
                plan = Project.objects.get(id=self.default_plan_id)
            except Project.DoesNotExist:
                plan = {'name': _('Название нового плана')}

            context['plan'] = plan
        else:
            context = add_plan_data(self.request, context, kwargs['plan_id'])

        return context

    @require_http_methods(["POST"])
    def save_data(self, request, *args, **kwargs):
        """Метод для сохранения данных заполненного плана"""

        errors = {}
        #Проверяем данные плана
        plan = request.POST.get('plan', None)
        if plan == None:
            return self.bad_request(message="plan does not exists")

        plan = json.loads(plan)
        #Проверяем данные при помощи формы
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
                #Проверяем данные каждой главы при помощи формы
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

        #Если проверка плана и глав пройдена успешно - сохраняем
        if not errors:
            saved_chapters = self.save_chapters(chapters_cleaned_data)
            plan_data = plan_form.cleaned_data
            plan_data['created_by'] = request.user
            plan_data['id'] = kwargs['plan_id']
            new_plan_id = self.save_plan(plan_data, saved_chapters)
            if new_plan_id:
                response = HttpResponse(json.dumps({'plan_id': new_plan_id}),
                             content_type='application/json')
                response.status_code = 200
                return response

        return self.bad_request(message="Incorrect data", errors=errors)


    def save_chapters(self, chapters_data):
        """Метод сохранения разделов"""
        chapters = []
        for chapter in chapters_data:
            #Если создаётся новый раздел - в его id присутствует "new"
            if "new" in chapter['id']:
                old_chapter = False
            else:
                old_chapter = Chapter.objects.get(id=chapter['id'])

            if not old_chapter:
                #Если создаём новый раздел - удалим сначала переданный с клиента id, чтобы создался новый
                del chapter['id']
                new_chapter = Chapter.objects.create(**chapter)
                chapters.append(new_chapter)
            else:
                old_chapter.update_chapter(chapter)
                chapters.append(old_chapter)

        return chapters


    def save_plan(self, plan_data, chapters):
        """Метод сохранения плана"""

        # Если создаётся новый план - в его id присутствует "new"
        if plan_data['id'] == 'new':
            # Перед сохранением удалим id, чтобы БД создала правильный
            del plan_data['id']
            plan = Project.objects.create(**plan_data)
        else:
            plan = Project.objects.get(created_by=plan_data['created_by'],
                                                                  id=plan_data['id'])
            if not plan:
                return False

            Project.update_plan(plan_data, chapters)

        return plan.id


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
            chapters = context['chapters']
            #Преобразовываем данных из bbcode (данные из клиента поступают в формате bbcode)
            parcer = get_parser()
            for chapter in chapters:
                chapter['name'] = parcer.render(chapter['name'])
                chapter['questions'] = parcer.render(chapter['questions'])

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


