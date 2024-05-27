from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import ImageUploadForm
from pymongo import MongoClient
from gridfs import GridFS
import logging

logging.basicConfig(level=logging.DEBUG)

def upload_image(request):
  if request.method == 'POST':
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
      category = form.cleaned_data['category']
      image_file = form.files['image']

      file_content = image_file.read()
      logging.debug(f"File content length: {len(file_content)}")

      # Local save
      form.save()

      # Save to MongoDB
      client = MongoClient(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT)
      db = client[settings.MONGO_DB_NAME]
      fs = GridFS(db)
      fs.put(file_content, filename=image_file.name, category=category, content_type=image_file.content_type)

  return render(request, 'uploadapp/index.html')

def index_template(request):
  return render(request, 'uploadapp/index.html')
