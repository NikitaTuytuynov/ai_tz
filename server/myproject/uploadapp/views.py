from pymongo import MongoClient, errors as mongo_errors
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm
from PIL import Image as PILImage
from gridfs import GridFS
from .mongodb import db
import numpy as np
import logging

# Import tensorflow
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image as tf_image
import tensorflow as tf

# Add logging
logging.basicConfig(level=logging.DEBUG)

@api_view(['POST'])
def upload_image(request):
  form = ImageUploadForm(request.POST, request.FILES)

  if form.is_valid():
    categoryByUser = form.cleaned_data['categoryByUser']
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
      fs = GridFS(db)
      fs.put(file_content, filename=image_file.name, categoryByUser=categoryByUser, categoryByAI=prediction_names, content_type=image_file.content_type)

      return HttpResponse(f'Operation Successful!<br><br>User prediction: {categoryByUser}<br>AI predictions: {prediction_text}')
      
    # Catch mongo errors
    except mongo_errors.PyMongoError as error:
      logging.error(f"MongoDB error: {error}")
      return HttpResponse('There was an error saving the file to MongoDB.')
      
    # Catch other errors 
    except Exception as error:
      logging.error(f"An error occurred: {error}")
      return HttpResponse('An unexpected error occurred.')

  else:
    logging.error('Form is invalid.')
    return HttpResponse('Form is invalid.')


@api_view(['GET'])
def image_list(request):
  try:
    # Get all files from fs.files
    fs_files = db['fs.files']
    files = fs_files.find()

    file_list = []

    for file in files:
      file_info = {
        'filename': file['filename'],
        'categoryByUser': file['categoryByUser'],
        'categoryByAI': file['categoryByAI']
      }

      file_list.append(file_info)

    return JsonResponse(file_list, safe=False)
  
  # Catch mongo errors
  except mongo_errors.PyMongoError as error:
    logging.error(f"MongoDB error: {error}")
    return HttpResponse('There was an error getting the files from MongoDB.')

  # Catch other errors 
  except Exception as error:
    logging.error(f"An error occurred: {error}")
    return HttpResponse('An unexpected error occurred.')


def get_index_template(request):
  return render(request, 'uploadapp/index.html')
