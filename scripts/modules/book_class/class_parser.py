from html.parser import HTMLParser

class ClassParser(HTMLParser):
  depth = 0
  hit = 0
  classes = {}
  
  cur_class = ''
  cur_time = ''

  def get_class(self, attrs):
    for attr in attrs:
      if attr[0] == 'href':
        return attr[1][1:]

  def get_data(self):
    return self.classes

  def handle_starttag(self, tag, attrs):
    self.depth += 1
    if self.depth == 4:
      self.cur_class = self.get_class(attrs)

  def handle_endtag(self, tag):
    self.depth -= 1

  def handle_data(self, data):
    if self.depth == 6:
      if self.hit == 0:
        self.cur_time = data
      elif self.hit == 1:
        if data not in self.classes:
          self.classes[data] = []
        self.classes[data].append({'t': self.cur_time, 'id': self.cur_class})

      self.hit += 1
      self.hit %= 2