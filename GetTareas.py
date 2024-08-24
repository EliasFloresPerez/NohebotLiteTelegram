import apiMoodle as api
import json
from dotenv import load_dotenv
import os

# Carga las variables de entorno del archivo .env
load_dotenv()

# Obtén las variables de entorno
link = os.getenv('LINK')
token = os.getenv('TOKEN')
userId = os.getenv('USER_ID')


#Obtener materias

def Obtener_tareas():

    materias = api.getMaterias(token, userId, link)    

    output = {}

    for materia in materias:
        nombreMateria = materia['fullname'].split('-')[0]
        output[nombreMateria] = {}

        #Obtenemos las tareas de cada curso
        tareas = api.getAssignments(token, materia['id'], link)
        tareas = tareas['courses'][0]['assignments']

        for tarea in tareas:
            
            
            #Fecha
            output[nombreMateria][tarea['name']] = tarea['duedate']

        #Obtenemos los quizes de cada curso
        quizes = api.getQuizes(token, materia['id'], link)
        quizes = quizes['quizzes']

        for quiz in quizes:
            #Fecha
            output[nombreMateria][quiz['name']] = quiz['timeclose']

        
        #Obtenemos los foros de cada curso
        foros = api.getForums(token, materia['id'], link)
        

        for foro in foros:
            if foro['duedate']:
                #Fecha
                output[nombreMateria][foro['name']] = foro['cutoffdate']
    
    

   

    return output


