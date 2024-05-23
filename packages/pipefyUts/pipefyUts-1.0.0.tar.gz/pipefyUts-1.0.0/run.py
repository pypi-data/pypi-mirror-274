import sys
sys.path.append("./pipefyUts")

from pipefyUts import Pipefy,NewCard,CardField


ORG_ID =  "52629"
TOKEN  = "eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MDYwMjE2OTYsImp0aSI6ImFkZTE0Y2IwLTJlMjQtNDI2MC1iMzY4LTE1ZGZhYmRlNjNmNCIsInN1YiI6MzAyNjkxNDMyLCJ1c2VyIjp7ImlkIjozMDI2OTE0MzIsImVtYWlsIjoicnBhLnJpc2NvQHN5bXBsYS5jb20uYnIiLCJhcHBsaWNhdGlvbiI6MzAwMzEyNTIwLCJzY29wZXMiOltdfSwiaW50ZXJmYWNlX3V1aWQiOm51bGx9.ImvpteOXbCS9A0yv86XMH9gkOVEPQvJJCZOKFrSGSdadxy19NMke92AIU32z52rOe73Hj85cM6HczbtuB16inA"

pfy = Pipefy(ORG_ID,TOKEN)

pfy.listMembers()

pfy.listStartFormFields(pipe_id="1025104")

pfy.listCardsFromPhase(phase_id="325918208")



class MyCard(NewCard):
    #DEFAULT
    __title__                = "MyCardTitle"
    __pipeid__               = "304282374"

    #PIPEFY FIELDS
    descricao                = CardField(str)
    valor_total              = CardField(float)
    respons_vel_pela_an_lise = CardField(list)
    arquivos                 = CardField(list,is_file_path=True)

    def __init__(self,**kwargs): NewCard.__init__(self,**kwargs)


myNewCard = MyCard(
    descricao                = "AdtPro",
    valor_total              = 10000,
    respons_vel_pela_an_lise = ["301975616"],
    arquivos                 = [r"C:\Users\melque\Documents\Doc1.pdf"]
)

pfy.createCard(card=myNewCard)


pass

