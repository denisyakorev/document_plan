from django.views.generic.list import ListView
from doc_plan.models import Project


class ProjectListView(ListView):
    model = Project
    context_object_name = 'plans'
    template_name = 'plan/plans.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.filter(created_by=self.request.user)
        return queryset