from django.db import models
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class HexagonQuestion(models.Model):
    name = models.CharField(max_length=300)
    answer = models.CharField(max_length=300)
    options = models.CharField(max_length=300)
    reason = models.CharField(max_length=300)
    topic = models.ForeignKey(Topic, null=False, on_delete=models.CASCADE)
    type_choices = (("vf", "verdadero falso"), ("opm", "opcion multiple"))
    type = models.CharField(
        max_length=2,
        choices=type_choices,
        default="vf"
    )


class HexagonOption(models.Model):
    codes = models.CharField(max_length=20)
    name =  models.CharField(max_length=300)
    question = models.ForeignKey(HexagonQuestion, null=False, on_delete=models.CASCADE)


def populate_hexagon_questions():
    # Conectamos con la plantilla de Google Drive
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('iOrgTest-5fa50b4936cd.json', scope)
    gc = gspread.authorize(credentials)
    sh = gc.open("iOrg2.0")

    wks = sh.get_worksheet(6)

    #Recorrer las filas para crear las opciones de cada pregunta del formulario para hexagono