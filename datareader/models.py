from collections import OrderedDict
from itertools import repeat

from django.db import models

import gspread
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


COLUMN = {
    "topic":       4,
    "subtopic":    5,
    "name" :       6,
    "definition" : 7,
    "example" :    8,
    "url_image" :  9,
}

# Create your models here.
class Menu(models.Model):
    menu_id = models.CharField(max_length=50)
    menu_name = models.CharField(max_length=100)
    subject_filter = models.CharField(max_length=50)


class Subject(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)


class Topic(models.Model):
    name = models.CharField(max_length=100)








class SubTopic(models.Model):
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, null=False, on_delete=models.CASCADE)



class Concept(models.Model):
    name = models.CharField(max_length=100)
    definition = models.CharField(max_length=200)
    example = models.CharField(max_length=200)
    url_image = models.CharField(max_length=200)
    subtopic = models.ForeignKey(SubTopic, null=False, on_delete=models.CASCADE)

    def get_all():
        return Concept.objects.all()

    def filter_by_subtopic(subtopic_filter):
        return Concept.objects.filter(subtopic=subtopic_filter)




# Rellenamos nuestra base de datos con los datos de la hoja Conceptos de Drive
def populate_concept_page():
    # Topic.objects.all().delete()

    # Conectamos con la plantilla de Google Drive
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('iOrgTest-5fa50b4936cd.json', scope)
    gc = gspread.authorize(credentials)
    sh = gc.open("iOrg2.0")

    wks = sh.get_worksheet(2)

    topic_list = []
    topic_object = {
        "name" : "",
        "subtopics" : [],
        "concepts" : []
    }
    subtopic_object = {
        "name": "",
        "concepts": []
    }
    n_concepts = 76 #número de conceptos en el documento de drive

    tmp_topic = ""
    tmp_subtopic = ""
    concept_list = []
    subtopic_list = []

    topic_index = 1
    #Recorre todas las filas  de la hoja de cálculo.
    print("INICIO------------------")
    for i in range(1,n_concepts+1):
        print("Element [i] : ",i)

        # topic_list.append({
        #     "index" : i,
        #     "name": wks.cell(i,COLUMN["topic"]).value
        # })
        # No incluimos los temas repetidos en el vector de temas.
        if  wks.cell(topic_index,COLUMN["topic"]).value != wks.cell(i,COLUMN["topic"]).value:
            #Estructura de cada variable.
            topic_list.append({
                "index" : i,
                "name" : wks.cell(i,COLUMN["topic"]).value,
                "subtopics" : [],
                "concepts" : [],
            })
            topic_index = i

            #-------------  SUBTOPICS ----------
            tmp_subtopic = {}
            subtopic_index = i-1
            subtopic_list = []
            for j in range(i,n_concepts+1):
                print("----- Element [j] : ", j)
                # si cambiamos de topic salimos de subtopic.
                if wks.cell(j, COLUMN["topic"]).value != wks.cell(i, COLUMN["topic"]).value:
                     i = j
                     print("i = j ", i , j)
                     break

        #         #si la subvariable no es igual a la anterior la añadimos
                if  wks.cell(subtopic_index,COLUMN["subtopic"]).value != wks.cell(j,COLUMN["subtopic"]).value:
                    subtopic_list.append({
                        "index": j,
                        "name": wks.cell(j, COLUMN["subtopic"]).value,
                        "concepts": []
                    })
                    subtopic_index = j


            #         -------------- CONCEPTS ------------    (creamos los conceptos de las subvariables.)
                    concept_list = []
                    for k in range(j,n_concepts+1):
                        print("---------- Element [k] : ", k)
                        #si cambiamos de subtopic salimos de crear conceptos.
                        if wks.cell(k,COLUMN["subtopic"]).value != wks.cell(j,COLUMN["subtopic"]).value:
                            j = k
                            print("j = k ", j, k)
                            break

                        concept_list.append({
                           "name" : wks.cell(k, COLUMN["name"]).value,
                            "definition" : wks.cell(k, COLUMN["definition"]).value,
                            "example" : wks.cell(k, COLUMN["example"]).value,
                            "url_image" : wks.cell(k, COLUMN["url_image"]).value,
                        })
                    subtopic_list[-1]["concepts"] = concept_list
            topic_list[-1]["subtopics"] = subtopic_list

        #continua primer for topic
        # topic_list[-1]["subtopics"] = subtopic_list


    # # Creamos en la base de datos los temas.
    Concept.objects.all().delete()
    SubTopic.objects.all().delete()
    Topic.objects.all().delete()

    for i in range(0,len(topic_list)):
        topic_tmp = Topic.objects.create(name=topic_list[i]["name"])
        for j in range(0,len(topic_list[i]["subtopics"])):
            subtopic_tmp = SubTopic.objects.create(
                name = topic_list[i]["subtopics"][j]["name"],
                topic = topic_tmp
            )
            for k in range(0,len(topic_list[i]["subtopics"][j]["concepts"])):
                Concept.objects.create(
                    name = topic_list[i]["subtopics"][j]["concepts"][k]["name"],
                    definition = topic_list[i]["subtopics"][j]["concepts"][k]["definition"],
                    example = topic_list[i]["subtopics"][j]["concepts"][k]["example"],
                    url_image = topic_list[i]["subtopics"][j]["concepts"][k]["url_image"],
                    subtopic = subtopic_tmp
                )

    return topic_list