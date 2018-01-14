from django.shortcuts import render
from django.template import loader, RequestContext

# Create your views here.
def home(request):
    template = loader.get_template('landing/content.html')
    context = {'user':request.user,}
    return render(request, 'landing/content.html', context)