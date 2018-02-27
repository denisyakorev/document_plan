from django.views.generic.list import ListView
from django.views.generic import TemplateView
from doc_plan.utils import add_plan_data
from wkhtmltopdf.views import PDFTemplateView
from doc_plan.models import Project
from django.shortcuts import render_to_response
from django_ajax.decorators import ajax
from django.utils.translation import ugettext_lazy as _


# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'plans'
    template_name = 'plan/plans.html'
    paginate_by = 10


    def get_queryset(self):
        queryset = Project.objects.filter(created_by=self.request.user)
        return queryset



class PlanView(TemplateView):
	
	template_name = 'plan/plan_view.html'

	def get_context_data(self, **kwargs):
		context = super(PlanView, self).get_context_data(**kwargs)
		context = add_plan_data(self.request, context= context, plan_id= context['plan_id'])

		return context


class PlanPDF(PDFTemplateView):
    filename = 'plan_pdf.pdf'
    template_name = 'plan/plan_pdf/plan_pdf.html'

    def get_context_data(self, **kwargs):
        context = super(PlanPDF, self).get_context_data(**kwargs)
        context = add_plan_data(self.request, context=context, plan_id=context['plan_id'])

        return context


class PlanPdfView(TemplateView):
    template_name = 'plan/plan_pdf/plan_pdf.html'

    def get_context_data(self, **kwargs):
        context = super(PlanPdfView, self).get_context_data(**kwargs)
        context = add_plan_data(self.request, context=context, plan_id=context['plan_id'])

        return context


def plan_edit(request, plan_id):
    if request.method == 'GET':
        context = {'edit': True}
        if plan_id == 'new':
            plan= {'name': _('Название нового плана')}
            context['plan']= plan
        else:
            context = add_plan_data(request, context, plan_id)

        return render_to_response('plan/plan_edit.html', context)


@ajax
def get_chapters_data(request, plan_id):
    if plan_id == 'new':
        chapters = []
    else:
        context = add_plan_data(request, context={}, plan_id= plan_id)
        chapters = context['chapters']

    return {'chapters': chapters}

@ajax
def save_data(request, plan_id):
    pass