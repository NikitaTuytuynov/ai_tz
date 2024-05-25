from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
import os

# for avoid csrf token
@csrf_exempt
def upload_image(request):
  if request.method == 'POST':
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
      # save the form
      form.save()
    
      category = form.cleaned_data['category']
      image = form.cleaned_data['image']

    return HttpResponse('done')
