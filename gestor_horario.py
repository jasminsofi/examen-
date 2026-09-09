#Registrar materias y actividades en un horario semanal 
import json
#para ver si existe el archivo 
import os
#preparando las fechas 
from datetime import datetime 

#DEFINIMOS CONSTANTES
#Aqui estamos guardando el nombre de nuestro archivos
#Donde se guarda el archivo 
ARCHIVO_DATOS="horario.json" 
#Donde se guarda el reporte 
ARCHIVO_REPORTE="reporte_horario.json" 
#Dias disponibles
DIAS_SEMANAL=[
    "Lunes",
    "Martes",
    "Miercoles",
    "Jueves",
    "Viernes"]

#CLASE GESTORHORARIO
#la clase es un molde 
#class sirve para crear un objeto y que tenga varias caracteristicas 
#_init_ es que autimaticamente de guarda las cosas 
class GestorHorario:
    def __init__(self):
        self.eventos=[] #lista donde se guarda las actividades 
        self.cargar_datos()#donde me guarda todos los datos 

    #CARGAR ARCHIVO JSON 
    #os.path.exists() sirve para ver si existe el archivo 
    def cargar_datos(self):
        self.eventos = []
        if os.path.exists(ARCHIVO_DATOS):
            #try intenta leer el archivo 
            try:
                # Se agrega encoding="utf-8" para leer tildes y la ñ correctamente
                # la r es leer 
                with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                    self.eventos = json.load(archivo)
            except json.JSONDecodeError:
                print("Error al cargar los datos. El archivo puede estar corrupto.")
        else:
            self.eventos = []

    

    #GUARDAR ARCHIVO JSON

    #creacion de la funcion dentro de la clase
    #json.drump es para guardar los datos en el archivo json 
    #self.eventos es la lista que se guarda en el archivo json 
    #indent=4 es para que se vea bonito el archivo json 
    #ensure_ascii=False → permite que aparezcan normalmente las tildes y la ñ
    #la W es escribir
    def guardar_datos(self):
        with open(ARCHIVO_DATOS,"w",encoding="utf-8") as archivo:
            json.dump(
                self.eventos,
                archivo,
                indent=4,
                ensure_ascii=False
                ) 
    
        #VALIDAR HORA 

        # #try y except es para que si el usuario pone una hora mal no se caiga el programa 
        # #"%H:%M" es el formato de hora que se espera hora:minutos
        # #valuerror es ver si el usuario pone mal la hora 
    def validar_hora(self,hora):
        try:
            datetime.strptime(hora,"%H:%M")
            return True
        except ValueError:
            return False
        
#VALIDAR CHOQUES

#self permite que todas las funciones trabajen con los mismos datos 
#hay_conflicto es para ver si hay un choque materias o actividades en el horario
#if evento["dia"]==dia: es para ver si el dia de la actividad que se quiere registrar es igual al dia de la actividad que ya esta registrada 
# inicio_evento=evento["hora_inicio"] y fin_evento=evento["hora_fin"] es para guardar la hora de inicio y final de la actividad que ya esta registrada 
#if inicio<fin_evento and fin>inicio_evento , return True , return False todo esto es para ver si hay un choque de horarios entre la actividad que se quiere registrar y la actividad que ya esta registrada
    def hay_conflicto(self,dia,inicio,fin,evento_excluir=None):

        for evento in self.eventos:
            if evento is evento_excluir:
                continue
            if evento['dia']==dia:
                inicio_evento=evento['hora_inicio']
                fin_evento=evento['hora_fin']
                if inicio<fin_evento and fin>inicio_evento:
                    return True
        return False

#REGISTRAR EVENTO

#aqui le permite agregar una nueva materia o actividad a un horario o agenda al usuario
#el strip() es para quitar los espacios en blanco al inicio y al final de la cadena de texto 
#el join()es para unir los elementos de una lista en una cadena separando el texto con comas
#.strip()es para quitar los espacios innesesarios
#.capitalize()convierte la primera letra en mayuscula 
    def registrar_evento(self):
        materia=input("ingrese el nombre de la materia o actividad:  ").strip()
        dia=input("ingrese el dia de la semana (lunes,martes,miercoles,jueves,viernes): ").strip().capitalize()
        hora_inicio=input("ingrese la hora de inicio (formato 24 horas, ej:14:30)").strip()
        hora_fin=input("ingrese la hora de finalizacion (formato 24 horas, ej:16:30)").strip()
        ubicacion=input("ingrese la ubicacion (ENTER para omitir): ").strip()
#validar nombre 
        if not materia:
            print("El nombre de la materia o actividad no puede estar vacio.")
            return
#validar dia
        if dia not in DIAS_SEMANAL:
            print("Dia invalido. Debe ser uno de los siguientes: ",",".join(DIAS_SEMANAL))
            return
#validar hora inicio y final 
        if not self.validar_hora(hora_inicio):
            print("hora de inicio invalida")
            return
        if not self.validar_hora(hora_fin):
            print("hora de finalizacion invalida")
            return
        if hora_inicio>=hora_fin:
            print("la hora de inicio debe ser menor que la hora de fin")
            return
        if self.hay_conflicto(dia,hora_inicio,hora_fin):
            print("existe un choque de horario")
            return
#crear nuevo elemento
        nuevo_evento={"materia":materia,"dia":dia,"hora_inicio":hora_inicio,"hora_fin":hora_fin,"ubicacion":ubicacion}
        self.eventos.append(nuevo_evento)
        self.guardar_datos()
        print("\nevento registrado exitosamente.")

    #VER HORARIO
    def ver_horario(self):
        if not self.eventos:
            print("\n No hay eventos registrados.")
            return
        #obtenemos las horas de inicio y fien unicas y las ordenamos 
        franjas=sorted(list(set((evento['hora_inicio'],evento['hora_fin']) for evento in self.eventos)))

        print("\n"+"="*90)
        print(f"| {'Hora':<13} | {'Lunes':<12} | {'Martes':<12} | {'Miercoles':<12} | {'Jueves':<12} | {'Viernes':<12} |")
        print("="*90)

        for inicio,fin in franjas:
            hora_list=f"{inicio}-{fin}"
            fila = [f"| {hora_list:<13}"]
            for dia in DIAS_SEMANAL:
                actividad="libre"
                for evento in self.eventos:
                    if evento['dia'].lower()==dia.lower() and evento['hora_inicio']==inicio:
                        actividad=evento['materia'][:12]#corta si supera los 12 caracteres  
                        break
                fila.append(f"|{actividad:<12}")

            fila.append("|")
            print(" ".join(fila))
        print("="*90)
        input("\n Presione ENTER para continuar...")


#ELEMINAR EVENTO
    def eliminar_evento(self):
        materia = input("ingrese el nombre de la materia o actividad a eliminar: ").strip().lower()
        dia = input("ingrese el dia de la semana (lunes,martes,miercoles,jueves,viernes): ").strip().lower()

        for evento in self.eventos:
            if (evento['materia'].strip().lower() == materia and 
                evento['dia'].strip().lower() == dia):
                
                self.eventos.remove(evento)
                self.guardar_datos()
                print("evento eliminado exitosamente")
                return

        print("evento no encontrado")

#GENERAR REPORTE
    def generar_reporte(self): 
        reporte = []
        print("\n" + "=" * 42)
        print("REPORTE DEL HORARIO SEMANAL")
        print("=" * 42)

        for dia in DIAS_SEMANAL:
            # Filtramos recorriendo la lista con 'evento'
            eventos_dia = [evento for evento in self.eventos if evento['dia'].lower() == dia.lower()]
            eventos_dia.sort(key=lambda evento: evento['hora_inicio'])

            eventos_json = []
            print(f"\n{dia}:")
            if eventos_dia:
                for evento in eventos_dia:
                    print(f"- {evento['materia']} ({evento['hora_inicio']} - {evento['hora_fin']}) en {evento['ubicacion']}")
                    eventos_json.append({
                        "materia": evento['materia'],
                        "hora_inicio": evento['hora_inicio'],
                        "hora_fin": evento['hora_fin'],
                        "ubicacion": evento['ubicacion']
                    })
            else:
                print("- Sin actividades")

            print("-" * 42)
            reporte.append({"dia": dia, "eventos": eventos_json})
            
            # Paginación solicitada
            input("Presione ENTER para continuar...")

        with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as archivo:
            json.dump(reporte, archivo, indent=4, ensure_ascii=False)
                   

                        
#MODIFICAR EVENTO
    def modificar_evento(self):
        materia = input("Ingrese el nombre de la materia o actividad que desea modificar: ").strip().lower()
        dia = input("Ingrese el dia de la semana: ").strip().lower().capitalize()
        for evento in self.eventos:
            if (evento["materia"].lower() == materia.lower() and
            evento["dia"].lower() == dia.lower()):
                print("\nEvento encontrado.")
                nueva_materia = input(f"Nuevo nombre (ENTER para mantener '{evento['materia']}'): ").strip()
                nuevo_dia = input(f"Nuevo dia (ENTER para mantener '{evento['dia']}'): ").strip()
                nueva_hora_inicio = input(f"Nueva hora de inicio (ENTER para mantener '{evento['hora_inicio']}'): ").strip()
                nueva_hora_fin = input(f"Nueva hora de finalizacion (ENTER para mantener '{evento['hora_fin']}'): ").strip()
                nueva_ubicacion = input(f"Nueva ubicacion (ENTER para mantener '{evento['ubicacion']}'): ").strip()
            # Mantener los datos anteriores si se presiona ENTER
                dia_final = nuevo_dia if nuevo_dia else evento["dia"]
                hora_inicio_final = (
                    nueva_hora_inicio
                    if nueva_hora_inicio
                    else evento["hora_inicio"]
                )
                hora_fin_final = (
                    nueva_hora_fin
                    if nueva_hora_fin
                    else evento["hora_fin"]
                      )

            # Validar dia
                dia_final = dia_final.capitalize()
                if dia_final not in DIAS_SEMANAL:
                    print("Dia invalido.")
                    return

            # Validar hora de inicio
                if not self.validar_hora(hora_inicio_final):
                    print("Hora de inicio invalida.")
                    return

            # Validar hora de finalizacion
                if not self.validar_hora(hora_fin_final):
                    print("Hora de finalizacion invalida.")
                    return

            # Comprobar que la hora de inicio sea menor
            # que la hora de finalizacion
                if hora_inicio_final >= hora_fin_final:
                    print("La hora de inicio debe ser menor ""que la hora de finalizacion." )
                    return

            # Comprobar si existe un choque de horario
                if self.hay_conflicto(dia_final,hora_inicio_final,hora_fin_final,evento):
                    print("Existe un choque de horario.")
                    return

            # Guardar los cambios
                if nueva_materia:
                    evento["materia"] = nueva_materia
                evento["dia"] = dia_final
                evento["hora_inicio"] = hora_inicio_final
                evento["hora_fin"] = hora_fin_final

                if nueva_ubicacion:
                    evento["ubicacion"] = nueva_ubicacion

            # Guardar en el archivo JSON
            self.guardar_datos()

            print("\nEvento modificado exitosamente.")
            return

    print("\nEvento no encontrado.")
   

           

    
   




            



   
      

    

