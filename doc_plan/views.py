from django.views.generic.list import ListView
from django.views.generic import TemplateView
from doc_plan.utils import add_plan_data, make_pdf_content
from django.http import HttpResponse
from django.template import loader
import trml2pdf
from io import BytesIO, StringIO
from rlextra.rml2pdf import rml2pdf
from reportlab.lib.utils import getBytesIO, isUnicode, asUnicode, asNative, asBytes, isPy3, unicodeT
from wkhtmltopdf.views import PDFTemplateView

import os
from django.conf import settings
from xhtml2pdf import pisa


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def render_pdf_view(request):
    template_path = 'plan_pdf/test_output.html'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(Context(context))

    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



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
		context = add_plan_data(self.request, context= context, plan_id= context['plan_id'])

		return context


def make_pdf(request, plan_id= None):
    context = add_plan_data(request, plan_id= plan_id)
    context['sRoot'] = os.path.join(settings.BASE_DIR, '/static/')
    response = HttpResponse(content_type='applacation/pdf')
    response['Content-Disposition'] = 'attachment; filename=plan.pdf'


    """
    #Реализация для reportlab
    content = make_pdf_content(context)
    response.write(content)
    """

    """
    #Реализация для trml2pdf
    rml = loader.render_to_string('plan_pdf/test_output.rml', context)
    print(rml)
    pdf = trml2pdf.parseString(rml)

    response.write(pdf)
    """


    """
    #Реализация для xhtml2pdf
    template_path = 'plan_pdf/test_output.html'

    # find the template and render it.
    template = loader.get_template(template_path)
    html = template.render(context)

    print(html)

    # create a pdf
    pisaStatus = pisa.CreatePDF(
        html, dest=response, encoding='utf8')
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    """

    """
    #Реализация для rml2pdf
    rml = loader.render_to_string('plan_pdf/test_output.rml', context)
    buf = StringIO()
    rml2pdf.go(rml, outputFileName=buf)
    response.write(buf.getvalue())
    """

    return response


class PlanPDF(PDFTemplateView):
    filename = 'plan_pdf.pdf'
    template_name = 'plan/plan_pdf/plan_pdf.html'


    def get_context_data(self, **kwargs):
        context = super(PlanPDF, self).get_context_data(**kwargs)
        context = add_plan_data(self.request, context=context, plan_id=context['plan_id'])

        return context


class PlanPdfView(TemplateView):
    template_name = 'plan/plan_pdf/plan_pdf.html'
    footer_template = 'plan/plan_pdf/footer.html'

    def get_context_data(self, **kwargs):
        context = super(PlanPdfView, self).get_context_data(**kwargs)
        context = add_plan_data(self.request, context=context, plan_id=context['plan_id'])

        return context