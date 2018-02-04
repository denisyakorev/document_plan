from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic.list import View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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



class PlanView(View):

    def get(self, request):
        pass


