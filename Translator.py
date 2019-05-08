import decode_server

class translatorAI:
  def __init__(self):
    self.model = decode_server.model_decoder()

  def getMessage(self, string):
    return self.model.getMessage(string)

  def close(self):
    self.model.closeModel()


if __name__ == '__main__':
  foo = translatorAI()
  while True:
    mess = input('enter string to translate [q = quit]:')
    if (mess == 'q'):
      foo.close()
      break
    foo.getMessage(mess)