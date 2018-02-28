from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin
from doc_plan.utils import add_plan_data
from wkhtmltopdf.views import PDFTemplateView
from doc_plan.models import Project
from django_ajax.decorators import ajax
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
import json
from doc_plan.forms import PlanForm


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
        plan = request.POST.get('plan', None)
        #Если переданы данные о плане
        if plan == None:
            return self.bad_request("plan does not exists")
        else:
            old_plan = Project.objects.get(created_by=request.user, id=kwargs['plan_id'])
            if not old_plan:
                return self.bad_request("plan does not exists")
            else:
                # и есть существующий план с аналогичными данными
                pass





        return self.bad_request("plan does not exists")


    def get_chapters_data(self, request, *args, **kwargs):
        if kwargs['plan_id'] == 'new':
            chapters = []
        else:
            context = add_plan_data(request, context={}, plan_id=kwargs['plan_id'])
            chapters = context['chapters']

        response = HttpResponse(json.dumps({'chapters': chapters}),
                                content_type='application/json')

        return response


    def bad_request(self, message):
        response = HttpResponse(json.dumps({'message': message}),
                                content_type='application/json')
        response.status_code = 400
        return response


