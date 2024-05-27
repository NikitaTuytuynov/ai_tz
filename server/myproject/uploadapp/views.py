from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import ImageUploadForm
from pymongo import MongoClient
from gridfs import GridFS
import logging

import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as tf_image
import numpy as np
from PIL import Image as PILImage

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

      # Image classification using MobileNetV2
      model = MobileNetV2(weights='imagenet')

      # Prepare the image for classification
      img = PILImage.open(image_file)
      # Ensure image is in RGB format
      img = img.convert('RGB') 
      img = img.resize((224, 224))
      img_array = tf_image.img_to_array(img)
      img_array = np.expand_dims(img_array, axis=0)
      img_array = preprocess_input(img_array)

      # Perform prediction
      predictions = model.predict(img_array)
      decoded_predictions = decode_predictions(predictions, top=3)[0]

      # Debug: Log predictions
      logging.debug(f"Predictions: {decoded_predictions}")

      # Prepare the prediction results
      prediction_text = ', '.join([f"{pred[1]} ({pred[2]*100:.2f}%)" for pred in decoded_predictions])

      return HttpResponse(f'Predictions: {prediction_text}')

  # return render(request, 'uploadapp/index.html')

def index_template(request):
  return render(request, 'uploadapp/index.html')
