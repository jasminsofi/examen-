#mostrar el menu y devuelve la opcion para elegir 
from gestor_horario import GestorHorario
def menu_horario():
    print("\n"+"="*34)
    print("GENERADOR DE HORARIO DE ESTUDIANTE")
    print("\n"+"="*34)
    print("1.Registrar una materia o actividad")
    print("2.ver horario semanal")
    print("3.Modificar una materia o actividad")
    print("4.Eliminar una materia o actividad")
    print("5.Generar reporte del horario")
    print("6.Salir")
    print("\n"+"="*42)

    return input ("seleccione una opcion:  ").strip()
#crear el objetivo del gestor 
gestor=GestorHorario()

#creamos ciclo para que el menu se repite hasta que el usuario quiera salir 
#el gestor maneja todas funciones del horario
while True:
    opcion=menu_horario()
    if opcion=="1":
        gestor.registrar_evento()
    elif opcion=="2":
        gestor.ver_horario()
    elif opcion=="3":
        gestor.modificar_evento()
    elif opcion=="4":
        gestor.eliminar_evento()
    elif opcion=="5":
        gestor.generar_reporte()
    elif opcion=="7":
        gestor.exportar_calendario() 
    elif opcion=="6":
        print("saliendo del programa...¡GRACIAS NOS VEMOS PRONTO CHAITO!")
        break
    else:
        print("opcion invalida, por favor seleccione una opcion valida")
#git add .
#git commit -m "Cambios en el proyecto"
#git push
#def ver_por_dia(self):
   # dia = input("Ingrese el día: ").strip().capitalize()

   # for evento in self.eventos:
        #if evento["dia"] == dia:
            #print(evento["materia"])

