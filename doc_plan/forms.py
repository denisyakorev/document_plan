from django import forms
from django.forms import ModelForm
from doc_plan.models import Project, Chapter
from ckeditor.widgets import CKEditorWidget

'''
class PlanForm(forms.Form):
    name = forms.CharField(max_length=200)
    aim_action = forms.CharField(required=False)
    aim_auditory = forms.CharField(required=False, widget=CKEditorWidget())
    aim_content = forms.CharField(required=False, widget=CKEditorWidget())
    reaction_action = forms.CharField(required=False, widget=CKEditorWidget())
    reaction_standart = forms.CharField(required=False, widget=CKEditorWidget())
    auditory_duty = forms.CharField(required=False, widget=CKEditorWidget())
    auditory_knowledge = forms.CharField(required=False, widget=CKEditorWidget())
    auditory_demography = forms.CharField(required=False, widget=CKEditorWidget())
    auditory_relations = forms.CharField(required=False, widget=CKEditorWidget())
    auditory_environment = forms.CharField(required=False, widget=CKEditorWidget())
    auditory_resume = forms.CharField(required=False, widget=CKEditorWidget())
    question_actions = forms.CharField(required=False, widget=CKEditorWidget())
    question_knowledges = forms.CharField(required=False, widget=CKEditorWidget())

class ChapterForm(forms.Form):
    name = forms.CharField(max_length=200)
    questions = forms.CharField(required=False, widget=CKEditorWidget())
'''

class PlanForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'aim_action', 'aim_auditory', 'aim_content',
                  'reaction_action', 'reaction_standart', 'auditory_duty',
                  'auditory_knowledge', 'auditory_demography', 'auditory_relations',
                  'auditory_environment', 'auditory_resume', 'question_actions',
                  'question_knowledges']
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 80%'}),
            'aim_action': CKEditorWidget(config_name='short'),
            'aim_auditory': CKEditorWidget(config_name='short'),
            'aim_content': CKEditorWidget(config_name='short'),
            'reaction_action': CKEditorWidget(config_name='default'),
            'reaction_standart': CKEditorWidget(config_name='default'),
            'auditory_duty': CKEditorWidget(config_name='wide'),
            'auditory_knowledge': CKEditorWidget(config_name='wide'),
            'auditory_demography': CKEditorWidget(config_name='wide'),
            'auditory_relations': CKEditorWidget(config_name='wide'),
            'auditory_environment': CKEditorWidget(config_name='wide'),
            'auditory_resume': CKEditorWidget(config_name='wide'),
            'question_actions': CKEditorWidget(config_name='default'),
            'question_knowledges': CKEditorWidget(config_name='default'),

        }


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ['name', 'questions']
