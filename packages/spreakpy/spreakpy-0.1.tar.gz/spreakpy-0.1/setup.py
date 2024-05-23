import setuptools as s

s.setup(
          name="spreakpy",
          version="0.1",
          description="A voice and audio package",
          long_description="A python package that uses famous tts and audio packages to simplfy them and give a devloper less work to do",
          author="P.Ghaywat",
          author_email="Pratham.Ghaywat@outlook.com",
          requires=("pyttsx3", "googletrans", "PyPDF2","gTTS","os","nltk","pocketsphinx","scipy"),
          url= "https://github.com/PrathamGhaywat/spreakpy",
)