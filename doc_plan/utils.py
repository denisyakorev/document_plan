#!-- coding:utf-8 --

from doc_plan.models import Project
from django.http import Http404
from django.forms.models import model_to_dict


def add_plan_data(request, context):
	"""Формируем набор данных для отображения плана"""
	user = request.user
	plan_id = context['plan_id']

	try:
		plan = Project.objects.get(id = plan_id)
		plan_dict = model_to_dict(plan)
		for key in plan_dict:
			context[key] = plan_dict[key]

	except Project.DoesNotExist:
		print ("Плана с id %s не существует" % plan_id)
		raise Http404

	return context


