"""document_plan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from doc_plan import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', TemplateView.as_view(template_name= 'landing/content.html')),
    path('<str:plan_id>/view/', views.PlanView.as_view()),
    path('<str:plan_id>/edit/', login_required(views.PlanEditView.as_view())),
    path('<str:plan_id>/download/', views.PlanPDF.as_view()),
    path('<str:plan_id>/ajax/chapters/', login_required(views.PlanEditView().get_chapters_data)),
    path('<str:plan_id>/save/', login_required(views.PlanEditView().save_data)),
    path('<str:plan_id>/delete/', login_required(views.PlanEditView().delete_plan)),
    #path('<int:plan_id>/view_pdf/', views.PlanPdfView.as_view()),
]

