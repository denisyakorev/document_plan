from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic.list import ListView


from doc_plan.models import Project

# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects.html'


    def get_queryset(self):
        qs = Project.objects.filter(created_by=self.request.user)
        return qs


