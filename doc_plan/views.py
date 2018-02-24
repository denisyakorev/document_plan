from django.views.generic.list import ListView
from django.views.generic import TemplateView
from doc_plan.utils import add_plan_data
from wkhtmltopdf.views import PDFTemplateView
from doc_plan.models import Project
from doc_plan.forms import PlanForm, ChapterForm
from django.http import Http404
from django.shortcuts import render_to_response

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
        if plan_id == 'new':
            plan_form = PlanForm()
            chapter_forms = []
            chapter_forms.append(ChapterForm({'name':'Hello'}))
        else:
            try:
                project = Project.objects.get(created_by=request.user, id=plan_id)
                chapters = project.chapters.all()
                #plan_form = PlanForm(instance=project)
                plan_form = project
                chapter_forms = []
                for each in chapters:
                    #chapter_forms.append(ChapterForm(instance=each))
                    chapter_forms.append(each)

            except Project.DoesNotExist:
                raise Http404("Plan does not exist")

        context = {
                    'edit': True,
                    'plan': plan_form,
                    'chapters': chapter_forms
                   }
        print (context)
        return render_to_response('plan/plan_edit.html', context)

