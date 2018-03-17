#!-- coding:utf-8 --

from doc_plan.models import Project
from django.http import Http404
from django.forms.models import model_to_dict



def add_plan_data(request, context= {}, plan_id= None):
	"""Формируем набор данных для отображения плана"""
	if not plan_id:
		return context

	user = request.user
	try:
		#add plan data
		plan = Project.objects.get(id = plan_id)
		context['plan'] = plan

		#add chapters data
		context['chapters'] = []
		for chapter in plan.chapters.all():
			context['chapters'].append(chapter)


	except Project.DoesNotExist:
		raise Http404

	return context


