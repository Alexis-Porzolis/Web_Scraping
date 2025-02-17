from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import csv

# Medir el tiempo de ejecución al inicio del script
start_time = time.time()

# Ruta del driver de Edge (asegúrate de tener el driver adecuado en tu sistema)
driver_path = 'C:/edgedriver/edgedriver_win64/msedgedriver.exe'

# Configuración de opciones de Edge para evitar conflictos con sesiones activas
edge_options = Options()
# Utilizamos un puerto remoto de depuración para evitar errores
edge_options.add_argument("--remote-debugging-port=9222")
# Creamos un perfil temporal para las sesiones de usuario
edge_options.add_argument("--user-data-dir=C:/temp_edge_profile")

# Iniciar el servicio y configurar el driver
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# Abrir la URL de la guía de TV
driver.get('https://tvguide.9now.com.au/guide/')

# Esperamos a que los elementos carguen completamente
time.sleep(5)

# Diccionario para almacenar la información de las regiones y ciudades
regions_info = {}

# Encontramos el contenedor de las regiones y ciudades
region_container = driver.find_element(
    By.CSS_SELECTOR, ".user-prefs.user-prefs--regions")

# Obtenemos todos los elementos de la lista que contienen las regiones y ciudades
region_items = region_container.find_elements(By.CLASS_NAME, "pick-list__item")

# Iteramos sobre las regiones y ciudades para obtener la información relevante
for item in region_items:
    try:
        # Extraemos el enlace para cada ciudad
        a_element = item.find_element(By.TAG_NAME, "a")

        # Obtenemos los atributos necesarios: nombre de ciudad, nombre de región y el enlace
        city_name = a_element.get_attribute("data-region-name")  # Ciudad
        region_name = a_element.get_attribute("data-region-state")  # Región
        city_url = a_element.get_attribute("href")  # Enlace a la ciudad

        # Si la región no está en el diccionario, la agregamos
        if region_name not in regions_info:
            regions_info[region_name] = {}

        # Almacenamos la ciudad y su URL en la región correspondiente
        regions_info[region_name][city_name] = city_url
    except Exception as e:
        print(f"Error al procesar la región: {e}")
        continue

# Diccionario para almacenar la información de los canales por ciudad
city_tv_guide = {}

# Iteramos sobre las regiones y sus ciudades
for region, cities in regions_info.items():
    for city, city_url in cities.items():
        # Accedemos a la URL de la ciudad
        driver.get(city_url)

        # Inicializamos el diccionario para almacenar los canales y programas de esa ciudad
        city_tv_guide[city] = {}

        # Obtenemos los nombres de los canales disponibles en la ciudad
        channel_divs = driver.find_elements(By.CLASS_NAME, "channel-icon")
        channel_names = [div.get_attribute("data-channel-name")
                         for div in channel_divs if div.get_attribute("data-channel-name")]

        # Iteramos sobre los canales para obtener sus programas
        for channel in channel_names:
            # Inicializamos la lista de programas para el canal
            city_tv_guide[city][channel] = []

            # Buscamos las filas del programa para el canal específico
            guide_rows = driver.find_elements(
                By.XPATH, f"//div[contains(@class, 'guide__row') and @data-channel-name='{channel}']")

            # Iteramos sobre las filas de programación
            for row in guide_rows:
                # Intentamos obtener los bloques de programas directamente
                program_blocks = row.find_elements(
                    By.CLASS_NAME, "guide__row__block")

                # Si no encontramos los bloques, los buscamos en sub-elementos
                if not program_blocks:
                    sub_divs = row.find_elements(By.XPATH, "./div")
                    for sub_div in sub_divs:
                        program_blocks.extend(sub_div.find_elements(
                            By.CLASS_NAME, "guide__row__block"))

                # Extraemos la información de cada programa
                for block in program_blocks:
                    try:
                        # Obtenemos el nombre del programa
                        h4_element = block.find_element(By.TAG_NAME, "h4")
                        program_name = h4_element.text.strip()

                        # Obtenemos la información adicional (como el horario del programa)
                        p_element = block.find_element(By.TAG_NAME, "p")
                        program_info = p_element.text.strip() if p_element else "Sin información adicional"

                        # Obtenemos el enlace del programa
                        a_element = block.find_element(By.TAG_NAME, "a")
                        program_link = a_element.get_attribute(
                            "href") if a_element else "Sin enlace"

                        # Verificamos si no hay horario y dejamos el comentario "Transmitiendo ahora"
                        program_time = program_info if program_info else "Transmitiendo ahora"

                        # Almacenamos la información del programa si tiene nombre
                        if program_name:
                            city_tv_guide[city][channel].append(
                                (program_name, program_time, program_link))  # Guardamos la información del programa

                    except:
                        continue  # Si ocurre un error, continuamos con el siguiente bloque de programa

# Cerramos el navegador después de haber recopilado todos los datos
driver.quit()

# Exportamos los datos a un archivo CSV
csv_filename = 'tv_guide_by_city.csv'

# Abrimos el archivo CSV en modo escritura
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escribimos el encabezado del archivo CSV
    writer.writerow(["Ciudad", "Canal", "Programa", "Horario", "Enlace"])

    # Escribimos los datos de cada ciudad, canal y programa
    for city, channels in city_tv_guide.items():
        for channel, programs in channels.items():
            for program in programs:
                # Escribimos una fila por cada programa
                writer.writerow(
                    [city, channel, program[0], program[1], program[2]])

print(f"Los datos se han guardado en el archivo {csv_filename}")

# Guardamos el tiempo de ejecución en un archivo de texto, en minutos
# Convertimos el tiempo de ejecución a minutos
execution_time = (time.time() - start_time) / 60
execution_time_filename = 'execution_time.txt'

with open(execution_time_filename, mode='w', encoding='utf-8') as file:
    file.write(f"Tiempo de ejecución: {execution_time:.2f} minutos")

print(
    f"El tiempo de ejecución se ha guardado en el archivo {execution_time_filename}")
