import GetTareas as gt
import FuncionesAlertas as fa
import json
import datetime
import pytz
import time
import threading
import asyncio
import TelegramBot as Tl
from fastapi import FastAPI,HTTPException
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware

import bd as bd

app = FastAPI() 
bot_thread  = ""
BotObject = None



# Configuración para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permite solicitudes desde cualquier dominio
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


async def Obtener_Tareas_Cambios():
    global BotObject
    #Obtenemos las tareas
    diccionario = gt.Obtener_tareas()

    try:
        #abrimos la base de datos y sacamos el json
        bd_obj = bd.BaseDeDatosJson()
        bd_obj.abrir_conexion()
        tareas = bd_obj.obtener_tareas(1)
        bd_obj.cerrar_conexion()

        tareas = json.loads(tareas) #Convertimos el string a diccionario
    except Exception as e:
        tareas = {}
        print(e)

    
    #Comparamos las tareas
    cambios = fa.encontrar_diferencias(tareas, diccionario)

    #Activamos el notificador de cambios
    if cambios != False:
        await BotObject.send_message(BotObject.grupo_chat_id, cambios)

    #Guardamos las tareas en el archivo tareas.json
    try:
        tareas = json.dumps(diccionario)
        bd_obj = bd.BaseDeDatosJson()
        bd_obj.abrir_conexion()

        bd_obj.modificar_tareas(1, tareas)
        bd_obj.cerrar_conexion()
    except Exception as e:
        print("Error al guardar las tareas en la base de datos: " + str(e))

    return diccionario,cambios

@app.get("/TareasHoy")
async def Tareas_hoy():
    try:
        #Obtenemos las tareas
        diccionario, cambios = await Obtener_Tareas_Cambios()


        #Obtenemos las tareas que finalizan hoy
        mensaje = fa.TareasFinalizanHoy(diccionario)

        if mensaje == False:
            return {"message": "No hay tareas que finalicen hoy"}
        else:
            await BotObject.send_message(BotObject.grupo_chat_id, mensaje)
            return {"message": "Tareas notificadas al grupo de Telegram"}
        

    except Exception as e:
        #return {"message": "Error: " + str(e)}
        raise HTTPException(status_code=404, detail= "Error: " + str(e))
    


@app.get("/TareasSemana")
async def Tareas_Semana():
    try:
        #Obtenemos las tareas  

        diccionario,cambios = await Obtener_Tareas_Cambios()

        #Obtenemos las tareas que finalizan en la semana
        mensaje = fa.TareasProximaSemana(diccionario)
        if mensaje == False:
            return {"message": "No hay tareas que finalicen en la semana"}
        else:
            await BotObject.send_message(BotObject.grupo_chat_id, mensaje)
            return {"message": "Tareas Semanales notificadas al grupo de Telegram"}
    except Exception as e:
        #return {"message": "Error: " + str(e)}
        raise HTTPException(status_code=404, detail= "Error: " + str(e))


@app.get("/NotificarCambios")
async def Notificar_Cambios():
    try:
        #Notificamos los cambios en las tareas
        diccionario,cambios = await Obtener_Tareas_Cambios()

        if cambios == False:
            return {"message": "No hay cambios en las tareas"}
        else:
            return {"message": "Cambios notificados al grupo de Telegram"}
        
    except Exception as e:
        #return {"message": "Error: " + str(e)}
        raise HTTPException(status_code=404, detail= "Error: " + str(e))


def run_bot():
    global BotObject 
    print("Bot de Telegram iniciado")
    asyncio.set_event_loop(asyncio.new_event_loop())  # Crea un nuevo bucle de eventos
    BotObject = Tl.BotTelegram()
    BotObject.iniciar()






bot_thread = threading.Thread(target=run_bot)
bot_thread.start()  # Inicia el bot en un hilo aparte

    


        


