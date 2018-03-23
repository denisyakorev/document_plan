#!-- coding:utf-8 --

from doc_plan.models import Project, ChapterOrder
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
		for chapter_order in ChapterOrder.objects.filter(project=plan).order_by('order'):
			context['chapters'].append(chapter_order.chapter)


	except Project.DoesNotExist:
		raise Http404

	return context


