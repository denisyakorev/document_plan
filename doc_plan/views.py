from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from doc_plan.utils import add_plan_data


from doc_plan.models import Project

# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects.html'
    paginate_by = 2


    def get_queryset(self):
        queryset = Project.objects.filter(created_by=self.request.user)
        return queryset



class PlanView(TemplateView):
    template_name = 'landing/content.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context = add_plan_data(request, context)
        return self.render_to_response(context)


