#!-- coding:utf-8 --

from doc_plan.models import Project
from django.http import Http404
from django.forms.models import model_to_dict

from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm





def add_plan_data(request, context= {}, plan_id= None):
	"""Формируем набор данных для отображения плана"""
	if not plan_id:
		return context

	user = request.user

	try:
		#add plan data
		plan = Project.objects.get(id = plan_id)
		plan_dict = model_to_dict(plan)
		for key in plan_dict:
			context[key] = plan_dict[key]

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


def make_pdf_content(context):

	temp = BytesIO()

	canvas = Canvas(temp, pagesize=A4)
	pdfmetrics.registerFont(TTFont('FreeSans', 'doc_plan/static/fonts/FreeSans.ttf'))
	test_string = '123456789o123456789o123456789o123456789o123456789o123456789o123456789o123456789o123456789o'
	canvas.setFont('FreeSans', 32)
	canvas.drawString(20*mm, 270*mm, test_string)
	canvas.showPage()
	canvas.save()

	return temp.getvalue()

def print_lines(string, font_size, canvas):
    num_in_line = {
        32: 28,
    }

