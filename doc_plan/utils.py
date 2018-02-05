#!-- coding:utf-8 --

from doc_plan.models import Project


def get_plan_data(request):
	"""Формируем набор данных для отображения плана"""
	user = request.user
	plan_id = request.plan_id
	plan = Project.objects.get(id = plan_id)