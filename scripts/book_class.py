import logging
from logging import warning as log
import json

from modules.book_class.book_class import BookClass
from modules.book_class.find_class import FindClass
from modules.book_class.mail_sender import send_success_mail

DB_NAME = 'storage.db'
JSON_DATA = {}

### LOGGING

logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(funcName)s():%(lineno)s: %(message)s")

### MAIN APP

log('Starting FH flash booking service')

### LOADING CONFIGURATION

with open('confs.json') as json_file:
  JSON_DATA = json.load(json_file)

### GETTING CLASSES

fc = FindClass(log, DB_NAME, JSON_DATA['classes'])
class_to_book = fc.retrieve_class()

if class_to_book is not None:
  bc = BookClass(log, DB_NAME, JSON_DATA['user'])
  ok = bc.book_class(class_to_book)
  if ok:
    send_success_mail(JSON_DATA['mail'], class_to_book)
else:
  log('No classes to book')
