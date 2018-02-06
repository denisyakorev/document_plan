#!-- coding:utf-8 --

from doc_plan.models import Project
from django.http import Http404


def add_plan_data(request, context):
	"""Формируем набор данных для отображения плана"""
	user = request.user
	plan_id = context['plan_id']

	try:
		plan = Project.objects.get(id = plan_id)
		"""
		context['plan_name'] = plan.name
		context['aim_action'] = plan.aim_action
		context['aim_auditory'] = plan.aim_auditory
		context['aim_content'] = plan.aim_content
		context['reaction_action'] = plan.reaction_action
		"""
		for k,v in plan:
			context[k] = v
		print(context)
	except Project.DoesNotExist:
		print ("Плана с id %s не существует" % plan_id)
		raise Http404


