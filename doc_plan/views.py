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
		print(context)
		return context


