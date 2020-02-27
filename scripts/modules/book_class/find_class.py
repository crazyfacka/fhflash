import datetime
from datetime import datetime as date
import json
import random
import requests
import sqlite3

from .class_parser import ClassParser

class FindClass():
  log, db_name, classes = None, None, None

  def __init__(self, log, db_name, classes):
    self.log = log
    self.db_name = db_name
    self.classes = classes

  def find_class(self, today, confs, classes):
    weekday = str(today.weekday() + 2)
    if weekday in confs:
      class_name = confs[weekday]['c']
      class_time_interval = confs[weekday]['t']
      
      if class_name in classes:
        now = date.now()
        testing_now = date.strptime(now.strftime('%H:%M'), '%H:%M')
        start_time = date.strptime(class_time_interval[0], '%H:%M')
        end_time = date.strptime(class_time_interval[1], '%H:%M')
        for c in classes[class_name]:
          testing_time = date.strptime(c['t'], '%H:%M')
          if (testing_time - testing_now).total_seconds() < 9 * 3600 and testing_now < testing_time and start_time < testing_time and end_time > testing_time:
            c['id'] = c['id'].replace('aula', '', 1)
            c['class_name'] = class_name
            return c

  def retrieve_class(self):
    today = date.now().date()
    rnd = random.randint(100000000000, 199999999999)

    with sqlite3.connect(self.db_name) as conn:
      c = conn.cursor()
      c.execute('SELECT contents FROM cached_classes_data WHERE date=?', (today,))
      row = c.fetchone()
      
      data = {}
      if row is None:
        final_url = 'https://www.myhut.pt/myhut/functions/get-aulas.php?id=3&date=' + str(today) + '&rnd=' + str(rnd)
        r = requests.get(final_url)
        self.log('Loading classes from %s' % final_url)

        parser = ClassParser()
        parser.feed(r.text)
        data = parser.get_data()
        c.execute('INSERT INTO cached_classes_data VALUES (?, ?)', (str(today), json.dumps(data)))
      else:
        self.log('Loaded cached data for %s' % today)
        data = json.loads(row[0])
        
    class_to_book = self.find_class(today, self.classes, data)
    return class_to_book
