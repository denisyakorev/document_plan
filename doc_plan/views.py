from django.shortcuts import render
from django.template import loader, RequestContext
from django.views.generic.list import ListView
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
        '''
        print(len(qs))
        paginator = Paginator(qs, 2)
        page = self.request.GET.get('page')
        try:
            qs = paginator.get_page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            qs = paginator.get_page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            qs = paginator.get_page(paginator.num_pages)
        '''
        return queryset


