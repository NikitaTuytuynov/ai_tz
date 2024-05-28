from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_DB_HOST, settings.MONGO_DB_PORT)
db = client[settings.MONGO_DB_NAME]