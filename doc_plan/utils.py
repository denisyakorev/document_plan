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
		plan_dict = model_to_dict(plan)
		context['plan'] = {}
		for key in plan_dict:
			context['plan'][key] = plan_dict[key]

		#add chapters data
		context['chapters'] = []
		for chapter in plan.chapters.all():
			cur_chapter_dict = {}
			cur_chapter = model_to_dict(chapter)
			for key in cur_chapter:
				cur_chapter_dict[key] = cur_chapter[key]

			context['chapters'].append(cur_chapter_dict)



	except Project.DoesNotExist:
		print ("Плана с id %s не существует" % plan_id)
		raise Http404

	return context




