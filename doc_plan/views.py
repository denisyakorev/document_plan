from django.shortcuts import render
from django.template import loader, Context, RequestContext
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from doc_plan.utils import add_plan_data
from rlextra.rml2pdf import rml2pdf
from io import StringIO
from reportlab.lib.utils import getBytesIO, asBytes


from reportlab.pdfgen import canvas
from django.http import HttpResponse

from easy_pdf.views import PDFTemplateView


from doc_plan.models import Project

# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'plans'
    template_name = 'plan/plans.html'
    paginate_by = 2


    def get_queryset(self):
        queryset = Project.objects.filter(created_by=self.request.user)
        return queryset



class PlanView(TemplateView):
	
	template_name = 'plan/plan_view.html'

	def get_context_data(self, **kwargs):
		context = super(PlanView, self).get_context_data(**kwargs)
		context = add_plan_data(self.request, context)

		return context


def make_pdf(request, plan_id=None):
    response = HttpResponse()
    response['CONTENT_TYPE'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename=plan_pdf.pdf'
    template = loader.get_template('plan_pdf/test.rml')
    context = {'plan_id': plan_id}
    context = add_plan_data(request, context)
    rml = template.render(context)
    f = open('/home/denis/projects/document-plan/bin/document_plan/pages/pdf/test_output.rml', 'w')
    f.write(rml)
    f.close()
    buf = StringIO()

    #rml2pdf.go(rml, outputFileName=buf)

    pdfData = buf.read()

    print (pdfData)
    #response.write(pdfData)

    return response



class PdfView(PDFTemplateView):
    template_name = 'plan/plan_view.html'

    def get_context_data(self, **kwargs):
        context = super(PdfView, self).get_context_data(**kwargs)
        context = add_plan_data(self.request, context)
        context['pagesize'] = "A4"

        return context