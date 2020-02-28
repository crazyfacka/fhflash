import re
import requests
import sqlite3
import re

class BookClass():
  log, db_name, user = None, None, None

  def __init__(self, log, db_name, user):
    self.log = log
    self.db_name = db_name
    self.user = user

  def login_and_book(self, class_to_book):
    self.log('Preparing to book class with ID %s' % class_to_book['id'])
    with requests.Session() as s:
      s.get('https://www.myhut.pt/')

      s.post('https://www.myhut.pt/myhut/functions/login.php', {
        'myhut-login-email': self.user['username'],
        'myhut-login-password': self.user['password']
      })

      s.get('https://www.myhut.pt/myhut/aulas/')

      resp = s.post('https://www.myhut.pt/myhut/functions/myhut.php', {
        'aula': class_to_book['id'],

        'socio': self.user['id'],
        'robot': 'asbcdefghijklmnopqrstuvwxz',
        'op': 'book-aulas'
      })

      confirmation_resp = s.get('https://www.myhut.pt/myhut/functions/get-aulas-info.php')
      result = re.search(class_to_book['class_name'], confirmation_resp.text)      
      if result.start() != -1:
        self.log('Class %s booked' % class_to_book['id'])
        with sqlite3.connect(self.db_name) as conn:
          c = conn.cursor()
          c.execute('INSERT INTO booked_classes VALUES (?)', (class_to_book['id'],))
          return True
      else:
        self.log('Error booking class %s' % class_to_book['id'])
        return False

  def book_class(self, class_to_book):
    with sqlite3.connect(self.db_name) as conn:
      c = conn.cursor()
      c.execute('SELECT COUNT(1) FROM booked_classes WHERE id=?', (class_to_book['id'],))
      row = c.fetchone()
      if row[0] == 1:
        self.log('Class %s already booked' % class_to_book['id'])
        return False

    return self.login_and_book(class_to_book)