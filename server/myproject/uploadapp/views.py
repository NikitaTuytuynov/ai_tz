from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import ImageUploadForm
from PIL import Image as PILImage
from pymongo import MongoClient, errors as mongo_errors
from gridfs import GridFS
import numpy as np
import logging

# Import tensorflow
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as tf_image

# Add logging
logging.basicConfig(level=logging.DEBUG)

def upload_image(request):
  if request.method == 'POST':
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
      category = form.cleaned_data['category']
      image_file = form.files['image']

      try:
        file_content = image_file.read()
        logging.debug(f"File content length: {len(file_content)}")

        # Local save
        form.save()

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

        # Prepare the prediction results
        prediction_names = [pred[1] for pred in decoded_predictions]
        prediction_text = ', '.join([f"{pred[1]} ({pred[2]*100:.2f}%)" for pred in decoded_predictions])

        # Save to MongoDB
        client = MongoClient(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT)
        db = client[settings.MONGO_DB_NAME]
        fs = GridFS(db)
        fs.put(file_content, filename=image_file.name, categoryByUser=category, categoryByAI=prediction_names, content_type=image_file.content_type)

        return HttpResponse(f'Operation Successful!<br><br>User prediction: {category}<br>AI predictions: {prediction_text}')
      
      # Catch mongo errors
      except mongo_errors.PyMongoError as error:
        logging.error(f"MongoDB error: {error}")
        return HttpResponse('There was an error saving the file to MongoDB.')
      
      # Catch other errors 
      except Exception as error:
        logging.error(f"An error occurred: {error}")
        return HttpResponse('An unexpected error occurred.')

    else:
      return HttpResponse('Incorrect request method')

  return render(request, 'uploadapp/index.html')

def index_template(request):
  return render(request, 'uploadapp/index.html')
