import datetime
import pytz


from babel.dates import format_datetime


# Zona horaria de Ecuador
ecuador_tz = pytz.timezone('America/Guayaquil')


#epoch para hora
def epoch_to_time(epoch):
    # Convertir epoch a hora local de Ecuador
    local_time = datetime.datetime.fromtimestamp(epoch, ecuador_tz)
    
    # Formatear la fecha en español como "Lunes 25 de Julio a las 00:00pm"
    formatted_date = local_time.strftime('%I:%M%p')
    return formatted_date

# Función para ver qué Tareas Finalizan hoy del diccionario que está en epoch
def TareasFinalizanHoy(diccionario):
    # Hora local de Ecuador ahora
    hoy = datetime.datetime.now(ecuador_tz).date()

    #Restar un dia
    #hoy = hoy - datetime.timedelta(days=1)
    # Lo guardamos en un diccionario
    TareasHoy = {}
    MensajeFinal = "<b><i>🚨 ACTIVIDADES QUE FINALIZAN HOY 🔧</i></b>\n\n"
    bandera = False
    for Materia in diccionario:
        for Tarea in diccionario[Materia]:
            if datetime.datetime.fromtimestamp(diccionario[Materia][Tarea], ecuador_tz).date() == hoy:
                bandera = True
                MensajeFinal += f'    🔸 La actividad <code>{Tarea}</code> de <b>{Materia}</b> finaliza a las <i><b>{epoch_to_time(diccionario[Materia][Tarea])}</b></i>\n\n'
                TareasHoy[Tarea] = diccionario[Materia][Tarea]

    MensajeFinal += "⭐"

    if bandera == False:
        MensajeFinal = False

    return MensajeFinal

def epoch_to_dateCom(epoch):
    # Convertir epoch a hora local de Ecuador
    local_time = datetime.datetime.fromtimestamp(epoch, ecuador_tz)
    
    # Formatear usando Babel
    formatted_date = format_datetime(local_time, "EEEE d 'de' MMMM 'a las' hh:mma", locale='es')
    
    return formatted_date

# Función para ver las tareas en los próximos 7 días
def TareasProximaSemana(diccionario):
    # Obtener la fecha de hoy en Ecuador
    hoy = datetime.datetime.now(ecuador_tz).date()

    # Guardamos las tareas en un diccionario
    TareasProximos7Dias = {}
    MensajeFinal = "<b>📍 ACTIVIDADES QUE FINALIZAN ESTA SEMANA 🔮</b>\n\n"
    bandera = False
    
    for Materia in diccionario:
        for Tarea in diccionario[Materia]:
            # Convertir epoch a fecha en Ecuador y calcular la diferencia de días
            tarea_fecha = datetime.datetime.fromtimestamp(diccionario[Materia][Tarea], ecuador_tz).date()
            dias_para_tarea = (tarea_fecha - hoy).days
            
            # Si la tarea finaliza en los próximos 7 días, se añade al diccionario
            if dias_para_tarea <= 7 and dias_para_tarea >= 0:
                bandera = True
                TareasProximos7Dias[Tarea] = diccionario[Materia][Tarea]
                
                MensajeFinal += f"    🔹 <code>{Tarea}</code> de <b>{Materia}</b> ➡️ <i><b>{epoch_to_dateCom(diccionario[Materia][Tarea])}</b></i>\n\n"
    
    MensajeFinal += "\n Un agradecimiento a <i><b>MXCA</b></i>\n\n ⭐"

    if not bandera:
        MensajeFinal = "No hay tareas para esta semana 🤔 Investiguen, no confíen en mí.\n"
    
    return MensajeFinal

def epoch_to_date(epoch_time):
    from datetime import datetime
    return datetime.fromtimestamp(epoch_time).strftime('%d/%m/%Y %H:%M')

def encontrar_diferencias(diccionario_viejo, diccionario_nuevo):
    tareas_modificadas = "<b><i>🪛 NOTIFICADOR DE CAMBIOS ⚠️</i></b>\n\n"
    bandera = False

    # Recorremos las materias en el nuevo diccionario
    for materia, tareas_nuevas in diccionario_nuevo.items():
        tareas_viejas = diccionario_viejo.get(materia, {})

        # Recorremos las tareas en la materia
        for tarea, fecha_nueva in tareas_nuevas.items():
            # Si la tarea no está en las tareas viejas, es una nueva tarea
            if tarea not in tareas_viejas:
                bandera = True
                tareas_modificadas += f"    📝 Nueva tarea en <code>{materia}</code> ➡️ {tarea} para el <i><b>{epoch_to_date(fecha_nueva)}</b></i>\n\n"
            # Si la tarea está pero la fecha cambió, registramos la modificación
            elif tareas_viejas[tarea] != fecha_nueva:
                bandera = True
                tareas_modificadas += f"    🔄 La tarea <code>{tarea}</code> de {materia} ha cambiado de fecha de entrega de <i><b>{epoch_to_date(tareas_viejas[tarea])}</b></i> a <i><b>{epoch_to_date(fecha_nueva)}</b></i>\n\n"
                
        # Revisa las tareas viejas que ya no están en el nuevo diccionario
        for tarea in tareas_viejas:
            if tarea not in tareas_nuevas:
                bandera = True
                tareas_modificadas += f"    ❌ La tarea <code>{tarea}</code> de {materia} ha sido eliminada\n\n"

    tareas_modificadas += "⭐"
    
    if not bandera:
        return False       

    return tareas_modificadas

