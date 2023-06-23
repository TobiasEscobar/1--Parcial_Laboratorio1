import re
import datetime
import random
import json
import os
from os import system
system("cls")

def mostrar_menu():
    for opcion in menu:
        print(opcion)

menu = [" ",
        "1.Traer datos desde archivo:", "2.Listar cantidad por raza: ",
        "3.Listar personajes por raza:: ", "4.Listar personajes por habilidad: ", "5.Jugar batalla: ", 
        "6.Guardar Json.", "7.Mostrar Json.", "8.Salir del programa.",
        " ", 
        "REQUERIMIENTO EXTRA:",
        "9.Agregar mas poder a los Saiyan:",
        " ",
        "RECUPERATORIO:",
        "10.Ordenar personajes por atributo:", "11.Generar codigo manual:", "12.Generar codigo automatico:",
        " "]

#1. Traer datos desde archivo: guardará el contenido del archivo DBZ.csv en una colección. Tener en
#cuenta que tanto razas y habilidades deben estar guardadas en algún tipo de colección debido a que
#un personaje puede tener más de una raza y más de una habilidad.

def parser_guardar_archivo(path:str)->list:
    '''
    Brief: 
    - A partir de un archivo csv que se le pase, crea un diccionario para cada linea modificando las mismas y lo guarda en una lista.
    Parame:
    - path: Es el archivo csv donde va a iterar esta funcion.
    Return: 
    - Devuelve una lista modificada.
    '''
    lista = []
    with open(path,"r", encoding="utf-8") as archivo:
        for linea in archivo:
            lectura = re.split(",|\n",linea)
            heroe = {}
            heroe["ID"] = int(lectura[0])
            heroe["Nombre"] = lectura[1].lower()

            validar = re.search("-H", lectura[2])
            if validar != None:
                razas = re.split("-", lectura[2].lower()) 
                heroe["Raza"] = razas
            else:
                raza_unica = []
                raza_unica.append(lectura[2].lower())
                heroe["Raza"] = raza_unica

            heroe["Poder_de_pelea"] = int(lectura[3])
            heroe["Poder_de_ataque"] = int(lectura[4])

            validar = re.search("|$%", lectura[5])
            if validar != None:
                habilidades = re.split("[|$%]+", lectura[5].lower())
                heroe["Habilidades"] = habilidades
            else:
                habilidad_unica = [] 
                habilidad_unica.append(lectura[5].lower()) 
                heroe['Habilidades'] = habilidad_unica 
            lista.append(heroe) 
    return lista

#2.Listar cantidad por raza: mostrará todas las razas indicando la cantidad de personajes que
#corresponden a esa raza.
def listar_cantidad_por_raza(lista:list)->list:
    '''
    Brief:
    - Itera sobre la lista que reciba y hace un conteo del atributo que se le pase, en este caso, es con Raza
    Param:
    - lista: la lista donde itera esta funcion.
    Return: 
    - Devuelve el conteo realizado en un diccionario
    '''
    conteos = {}
    for personaje in lista:
        key = personaje["Raza"]
        for clave in key:
            if clave in conteos:
                conteos[clave] += 1
            else:
                conteos[clave] = 1
    return conteos

#3. Listar personajes por raza: mostrará cada raza indicando el nombre y poder de ataque de cada
#personaje que corresponde a esa raza. Dado que hay personajes que son cruza, los mismos podrán
#repetirse en los distintos listados.

def listar_personajes_por_raza(lista: list) -> str:
    '''
    brief:
    - Muestra por cada raza, el nombre de los personajes que esten dentro de ella y su poder de ataque.
    param:
    - lista: Lista donde debe iterar la funcion que es llamada.
    return:
    - devuelve un mensaje avisando que termino tanto de mostrar como de iterar.
    '''
    personajes_por_raza = listar_cantidad_por_raza(lista)
    
    for raza in personajes_por_raza:
        print(f"\nRaza: {raza}")
        for personaje in lista:
            razas = personaje["Raza"]
            nombre = personaje["Nombre"]
            poder_ataque = personaje["Poder_de_ataque"]
            if type(razas) == list:
                if raza in razas:
                    print(f"- Nombre: {nombre}, Poder de ataque: {poder_ataque}")
            else:
                if raza == razas:
                    print(f"- Nombre: {nombre}, Poder de ataque: {poder_ataque}")

    mensaje_de_fin = print("\nTermino la lista")
    return mensaje_de_fin


#4. Listar personajes por habilidad: el usuario ingresa la descripción de una habilidad y el programa
#deberá mostrar nombre, raza y promedio de poder entre ataque y pelea.

def listar_personajes_por_habilidad(lista:list, habilidad:str)->list:
    '''
    brief:
    - Se le muestra al usuario el nombre, raza y el promedio entre ataque y pelea del personaje que posea la habilidad ingresada.
    param:
    - lista: lista donde debe iterar para encontrar las habilidades.
    - habilidad: el valor que debe ser encontrado dentro de las habilidades.
    return:
    - Devuelve una lista con los valores nombre, raza y promedio de ataque y pelea o un mensaje de error sino se encontro la habilidad. 
    '''
    personajes_encontrados = []
    habilidad_encontrada = False
    for personaje in lista:
        habilidades = personaje["Habilidades"]
        promedio_poder = (personaje["Poder_de_ataque"] + personaje["Poder_de_pelea"]) / 2
        if habilidad in habilidades:
            personajes_encontrados.append({
                "Nombre": personaje["Nombre"],
                "Raza": personaje["Raza"],
                "Promedio de poder": promedio_poder
            })
            habilidad_encontrada = True
    if habilidad_encontrada == True:
        mensaje = print(personajes_encontrados)
        return mensaje
    else:
        mensaje_error = print("Error. No existe esa habilidad. Pruebe poniendo su inicial en mayúscula o el nombre completo.")
        return mensaje_error

#5. Jugar batalla: El usuario seleccionará un personaje. La máquina selecciona otro al azar. Gana la
#batalla el personaje que más poder de ataque tenga. El personaje que gana la batalla se deberá
#guardar en un archivo de texto, incluyendo la fecha de la batalla, el nombre del personaje que ganó y
#el nombre del perdedor. Este archivo anexará cada dato.

def jugar_batalla(lista:list)->str:
    '''
    brief:
    - llama a las funciones de seleccion personaje y luego crea un archivo txt donde guarda al ganador de la comparacion de sus niveles de poder
    param:
    - lista: Lista que se pide para poder pasarsela a las funciones que deban iterar con ella.
    return:
    - Devuelve un mensaje avisando que el resultado se guardo exitosamente.
    '''
    personaje_usuario = seleccionar_personaje(lista)
    personaje_maquina = seleccionar_personaje_azar(lista, personaje_usuario)
    
    if personaje_usuario['Poder_de_ataque'] > personaje_maquina['Poder_de_ataque']:
        ganador = personaje_usuario
        perdedor = personaje_maquina
    else:
        ganador = personaje_maquina
        perdedor = personaje_usuario

    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("resultados_batallas.txt", "a") as archivo:
        archivo.write(f"Fecha: {fecha_actual}\n")
        archivo.write(f"Ganador: {ganador['Nombre']}\n")
        archivo.write(f"Perdedor: {perdedor['Nombre']}\n")
        archivo.write("------------\n")
    
    mensaje = print("Resultado guardado exitosamente.")
    
    return mensaje

def seleccionar_personaje(lista:list)->dict:
    '''
    brief:
    - Le pide al usuario que eliga un personaje en forma de numero dentro de la lista y valida que su eleccion sea valida.
    param:
    - lista: Lista con la que debe iterar para poder mostrar los personajes dsiponibles.
    return:
    - Devuelve un diccionario que representa al personaje que eligio el usuario.
    '''
    print("Selecciona tu personaje:")
    for i in range(len(lista)):
        print(f"{i+1}. {lista[i]['Nombre']}")
    
    while True:
        opcion = input("Ingresa el número del personaje (entre 1 y 35): ")
        if opcion.isdigit():
            opcion = int(opcion)
            if opcion >= 1 and opcion <= len(lista):
                return lista[opcion-1]
        print("Opción inválida. Ingresa un número válido (entre 1 y 35).")

def seleccionar_personaje_azar(lista:list, personaje_usuario:dict)->dict:
    '''
    brief:
    - Se elige aleatoriamente un personaje de la lista pero se verifica que no se seleccione el mismo que ya haya elegido el usuario.
    param:
    -Lista: Lista donded debe iterar y elegir un personaje aleatoriamente.
    -personaje_usuario: diccionario con el que tiene que comparar que no sea el mismo.
    return:
    - Devuelve un diccionario que representa al personaje que eligio la maquina.
    '''
    personaje_maquina = random.choice(lista)
    while personaje_maquina == personaje_usuario:
        personaje_maquina = random.choice(lista)
    return personaje_maquina

#6. Guardar Json: El usuario ingresa una raza y una habilidad. Generar un listado de los personajes que
#cumplan con los dos criterios ingresados, los mismos se guardarán en un archivo Json. Deberíamos
#guardar el nombre del personaje, el poder de ataque, y las habilidades que no fueron parte de la
#búsqueda. El nombre del archivo estará nomenclado con la descripción de la habilidad y de la raza.
#Por ejemplo: si el usuario ingresa Raza: Saiyan y Habilidad: Genki Dama
#   -Nombre del archivo:
#       Saiyan_Genki_Dama.Json
#   -Datos :
#       Goten - 3000 - Kamehameha + Tambor del trueno
#       Goku - 5000000 - Kamehameha + Super Saiyan 2

def guardar_personajes_en_json(lista:list, raza:str, habilidad:str)->None:
    '''
    brief:
    - Crea un json de los personajes que cumplan con los criterios ingresados por el usuario.
    param:
    - lista: Lista donde debe iterar y conseguir la informacion.
    - raza: Primer criterio ingresado por el usuario.
    - habilidad:Segundo criterio ingresado por el usuario.
    return:
    - Devuelve un mensaje en caso de no encontrar un personaje con los criterios ingresados.
    '''
    guardar_lista = []
    criterios_encontrados = False
    for personaje in lista:
        nombre = personaje['Nombre']
        razas = personaje['Raza']
        poder_de_ataque = personaje['Poder_de_ataque']
        habilidades = personaje['Habilidades']

        if raza in razas and habilidad in habilidades:
            habilidades_actualizadas = []
            criterios_encontrados = True
            for hab in habilidades:
                if hab != habilidad:
                    habilidades_actualizadas.append(hab)
            guardar_lista.append({
                'Nombre': nombre,
                'Poder_de_ataque': poder_de_ataque,
                'Habilidades': habilidades_actualizadas
            })
    if criterios_encontrados == True:
        nombre_archivo = f"{raza.replace(' ', '_')}_{habilidad.replace(' ', '_')}.json"
        with open(nombre_archivo, 'w') as archivo_json:
            json.dump(guardar_lista, archivo_json, indent=4)
    else:
        mensaje_error = print("No se encontraron personajes con tales criterios.")
        return mensaje_error


#7. Leer Json: permitirá mostrar un listado con los personajes guardados en el archivo Json de la opción 6.

def leer_personajes_desde_json(nombre_archivo:json):
    '''
    brief:
    - Muestra en consola los Json que se creen anteriormente.
    param:
    - nombre_archivo: El archivo json donde va a hacer la lectura.
    return: Devuelve la informacion que extrae del archivo Json.
    -
    '''
    with open(nombre_archivo, 'r') as archivo_json:
        personajes = json.load(archivo_json)
    return personajes

def mostrar_personajes(personajes:dict):
    '''
    brief:
    - Muestra la informacion guardada de los Json.
    param:
    - personajes: Diccionario del cual se va a mostrar su informacion.
    return: devuelve un mensaje de error en el caso de que el Json venga vacio.
    -
    '''
    if len(personajes) == 0:
        mensaje_error = print("\nNo se encontraron personajes en el archivo.")
        return mensaje_error
    else:
        print("Listado de personajes:")
        for personaje in personajes:
            print("Nombre:", personaje['Nombre'])
            print("Poder de Ataque:", personaje['Poder_de_ataque'])
            print("Habilidades:", personaje['Habilidades'])
            print()

def mostrar_personajes_guardados(lista_archivos):
    '''
    brief:
    - Verifica que existan archivos Json guardados y si tienen datos adentro, luego utiliza dos funciones 
    para leer su informacion y luego mostrarla en la consola.
    param: 
    - lista_archivos: archivos Json en donde debe buscar su nombre y mostrar su informacion.
    return:
    - Devuelve printeado a los personajes dentro del archivo Json.
    '''
    if len(lista_archivos) == 0:
        print("\nNo se encontraron archivos JSON guardados.")
    else:
        for nombre_archivo in lista_archivos:
            print(f"\nArchivo: {nombre_archivo}\n")
            if os.path.isfile(nombre_archivo):
                personajes = leer_personajes_desde_json(nombre_archivo)
                mostrar_personajes(personajes)
            else:
                print(f"El archivo {nombre_archivo} no existe.")

#Requerimiento extra

#Agregar una opción que permita otorgarle un 50% más de poder de pelea y un 70% más de poder de ataque a los Saiyan, 
# y agregaran a sus habilidades la “transformación nivel dios”.
#Guardar en un archivo CSV los personajes que hayan recibido esta actualización.


def mas_poder(lista:list, actualizar_personaje:str):
    '''
    brief:
    - Actualiza a la raza saiyan para que tengan mas poder de pelea y ataque y los guarda en un archivo csv.
    param:
    - lista: Lista en la que debe iterar para sacar la informacion.
    - actualizar_personaje: raza a la que se la quiere actualizar
    return:
    - 
    '''
    personajes_actualizados = []
    actualizados = False
    for personaje in lista:
        razas = personaje['Raza']
        if actualizar_personaje in razas:
            actualizados = True
            razas = "saiyan"
            poder_de_pelea = personaje['Poder_de_pelea']
            poder_de_ataque = personaje['Poder_de_ataque']
            habilidades = personaje['Habilidades']
            
            poder_de_pelea *= 1.5
            poder_de_ataque *= 1.7
            habilidades.append("Transformación nivel dios")
            
            personajes_actualizados.append({
                'Nombre': personaje['Nombre'],
                'Raza': razas,
                'Poder_de_pelea': poder_de_pelea,
                'Poder_de_ataque': poder_de_ataque,
                'Habilidades': habilidades
            })
    if actualizados == True:
        with open('Personajes_actualizados.csv', 'w', encoding="utf-8") as archivo_csv:
            for personaje in personajes_actualizados:
                linea = f"{personaje['Nombre']},{personaje['Raza']},{personaje['Poder_de_pelea']},{personaje['Poder_de_ataque']},{','.join(personaje['Habilidades'])}\n"
                archivo_csv.write(linea)
    else:
        mensaje_error = print("No se pudo actualizar. Reintentelo")
        return mensaje_error

#A..
#Crear la función ordenar_personajes_por_atributo que recibirá como parámetros:
#lista_personajes: La lista de personajes.
#atributo: El atributo por el cual se desea ordenar los personajes 
#orden: true para ordenar de forma ascendente y false descendente 
#El retorno deberá ser la lista ordenada.

def ordenar_personajes_por_atributo(lista:list, atributo:str, orden:bool)->list:
    '''
    brief: 
    - Ordena a los personajes de forma ascendente o descendente segun el atributo que se especifique. 
    param:
    - lista: la lista que debe ordenar.
    - atributo: 
    - orden: depende del booleano el orden en el que se va a ordenar. True si quiere de forma ascendente o False si quiere de forma descendente. 
    return:
    - Devuelve la lista ordenada como lo haya pedido el usuario
    '''
    lista_ordenada = sorted(lista, key=lambda x:x[atributo], reverse=orden)
    return lista_ordenada


#B.   1. Crear la función ‘generar_codigo_personaje’ la cual recibirá como parámetro:
#● Personaje: Un diccionario que representa un personaje.
#
#La función deberá generar un string con el siguiente formato:
#(Inicial Nombre)-([Ganador (A = Ataque | D = Defensa | AD = Empate])-(Valor más alto entre ataque y defensa)-(ID con los ceros restantes) 
#
#EJ: 
#
#12 Androide 18 Androide-Humano 3500 3800 
#A-D-3800-000000012
#22 Kid Buu Majin 9000 9000
#K-AD-9000-00000022
#
#24 Majin Buu Majin 5000 4800
#
#M-A-5000-000000024
#
#Teniendo en cuenta el primer ejemplo de Androide 18 vemos que este tiene más poder de defensa que de ataque, por lo tanto, en este tendrá un D. En cambio  Majin Buu que gana
#por ataque, solo tiene A, por último se encuentra Kid Buu que al tener el mismo poder de ataque que de defensa tiene un AD

def generar_codigo_personaje(personaje:dict)->str:
    '''
    brief:
    - Debe tomar los valores de nombre, poder de pelea, ataque y ID del personaje que eligio el usuario y mostrar su inicial,
    su promedio de poder y su ID en un minimo y maximo de 18 caracteres
    param:
    - personaje: un diccionario que representa el personaje elegido por el usuario.
    return:
    - Devuelve el codigo del personaje en exactamente 18 caracteres.
    '''
    nombre = personaje["Nombre"]
    poder_de_pelea = personaje["Poder_de_pelea"]
    poder_de_ataque = personaje["Poder_de_ataque"]
    id_personaje = personaje["ID"]

    inicial_nombre = nombre[0].upper()
    ganador = ""
    valor_mas_alto = max(poder_de_ataque, poder_de_pelea)

    if poder_de_ataque > poder_de_pelea:
        ganador = "A"
    elif poder_de_ataque < poder_de_pelea:
        ganador = "D"
    else:
        ganador = "AD"

    ceros_restantes = str(id_personaje).zfill(17 - len(f"{inicial_nombre}-{ganador}-{valor_mas_alto}"))

    codigo_personaje = print(f"{inicial_nombre}-{ganador}-{valor_mas_alto}-{ceros_restantes}")
    return codigo_personaje

#1.1. Crear la función agregar_codigos_personajes’ la cual recibirá como parámetro:
#
#● Lista_personajes: la lista de personajes
#La función deberá iterar la lista y agregarle el código a cada
#uno de los elementos..

def agregar_codigos_personajes(lista:list)->list:
    '''
    brief:
    - Utiliza la funcion map() para asignarle la funcion generar_codigo_personaje en cada uno de los personajes de la lista.
    param:
    - lista: Lista donde se debe aplicar la generacion de los codigos de los personajes.
    return:
    - Devuelve la lista de los codigos generados en consola.
    '''
    codigos_personajes = list(map(generar_codigo_personaje, lista))
    
    return codigos_personajes