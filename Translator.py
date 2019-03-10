import sh

# Load decoder scipt of translation and execute
def translatorAI(String):
  # Open and write text need to translate
  file = open("colab/en.txt","w")
  file.write(String)
  file.close()

  # Run decode
  sh.sh("translate-script.sh")

  # Read text after decode
  file = open("colab/translation.txt","r")
  output = file.read()
  file.close()

  # Return back to bot
  return output


if __name__ == '__main__':
  translatorAI("Hello world")