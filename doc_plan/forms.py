from django import forms

class PlanForm(forms.Form):
    name = forms.CharField()
    aim_action = forms.TextField()
    aim_auditory = forms.TextField()
    aim_content = forms.TextField()
    reaction_action = forms.TextField()
    reaction_standart = forms.TextField()

class AuditoryForm(forms.Form):
    name = forms.CharField()
    duty = forms.TextField()
    knowledge = forms.TextField()
    demography = forms.TextField()
    relations = forms.TextField()
    environment = forms.TextField()
    resume = forms.TextField()

