from funciones_parcial01 import * 
from os import system
system("cls")

lista = parser_guardar_archivo("DBZ.csv")

#Utilizada para el case 6-7
archivos_guardados = []

seguir = True
while seguir == True:

    mostrar_menu()

    respuesta = int(input("Ingresa una opcion del menu: "))

    match respuesta:
        case 1:
            print(lista)
        case 2:
            mostrar = listar_cantidad_por_raza(lista)
            print(mostrar)
        case 3:
            listar_personajes_por_raza(lista)
        case 4:
            habilidad_deseada = input("Ingrese la habilidad deseada: ")
            listar_personajes_por_habilidad(lista, habilidad_deseada)
        case 5:
            jugar_batalla(lista)
        case 6:
            ingresar_raza = input("Ingrese la raza del personaje: ")
            ingresar_habilidad = input("Ingrese la habilidad del personaje: ")
            guardar_personajes_en_json("DBZ.csv", ingresar_raza, ingresar_habilidad)
            nombre_archivo = f"{ingresar_raza.replace(' ', '_')}_{ingresar_habilidad.replace(' ', '_')}.json"
            archivos_guardados.append(nombre_archivo)
        case 7:
            mostrar_personajes_guardados(archivos_guardados)
        case 8:
            #Sale del programa
            seguir = False
    # Configuracion extra:
        case 9:
            personaje_a_actualizar = "saiyan"
            mas_poder(lista, personaje_a_actualizar)
    # Recuperatorio:
        case 10:
            atributo = input("Ingrese un atributo (ID - Nombre - Raza - Poder_de_ataque - Poder_de_pelea - Habilidades):")
            while (atributo != "ID" and atributo != "Nombre" and atributo != "Raza" and atributo != "Poder_de_ataque" and atributo != "Poder_de_pelea" and atributo != "Habilidades"):
                atributo = input("Error. Reingrese un atributo (ID - Nombre - Raza - Poder_de_ataque - Poder_de_pelea - Habilidades):")
            
            orden = input("Ingrese si quiere ordenar de forma asc o des: (True o False): ")
            while(orden != "True" and orden != "False"):
                orden = input("Error. Reingrese si quiere ordenar de forma asc o des: (True o False): ")
            
            if orden == "True":
                lista_ordenada_asc = ordenar_personajes_por_atributo(lista, atributo, True)
                print(lista_ordenada_asc)
            elif orden == "False":
                lista_ordenada_des = ordenar_personajes_por_atributo(lista, atributo, False)
                print(lista_ordenada_des)
        case 11:
            pedir_personaje = seleccionar_personaje(lista)
            generar_codigo_personaje(pedir_personaje)
        case 12:
            agregar_codigos_personajes(lista)
