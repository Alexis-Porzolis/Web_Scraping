from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
import csv

# Medir el tiempo de ejecución
start_time = time.time()

# Ruta del driver de Edge
driver_path = 'C:/edgedriver/edgedriver_win64/msedgedriver.exe'

# Configuración de opciones de Edge
edge_options = Options()
edge_options.add_argument("--remote-debugging-port=9222")
edge_options.add_argument("--user-data-dir=C:/temp_edge_profile")

# Iniciar el servicio y configurar el driver
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# Abrir la URL de la guía de TV
driver.get('https://tvguide.9now.com.au/guide/')
time.sleep(5)  # Esperar a que la página cargue

# Diccionario para almacenar información de regiones y ciudades
regions_info = {}

# Obtener el contenedor de las regiones
region_container = driver.find_element(By.CSS_SELECTOR, ".user-prefs.user-prefs--regions")
region_items = region_container.find_elements(By.CLASS_NAME, "pick-list__item")

# Extraer información de regiones y ciudades
for item in region_items:
    try:
        a_element = item.find_element(By.TAG_NAME, "a")
        city_name = a_element.get_attribute("data-region-name")  # Ciudad
        region_name = a_element.get_attribute("data-region-state")  # Región
        city_url = a_element.get_attribute("href")  # Enlace

        if region_name not in regions_info:
            regions_info[region_name] = {}

        regions_info[region_name][city_name] = city_url
    except Exception as e:
        print(f"Error al procesar la región: {e}")
        continue

# Diccionario para almacenar los canales por ciudad y región
city_tv_guide = {}

for region, cities in regions_info.items():
    for city, city_url in cities.items():
        driver.get(city_url)
        city_tv_guide[(city, region)] = {}  # Guardar como tupla (Ciudad, Región)

        channel_divs = driver.find_elements(By.CLASS_NAME, "channel-icon")
        channel_names = [div.get_attribute("data-channel-name") for div in channel_divs if div.get_attribute("data-channel-name")]

        for channel in channel_names:
            city_tv_guide[(city, region)][channel] = []

            guide_rows = driver.find_elements(By.XPATH, f"//div[contains(@class, 'guide__row') and @data-channel-name='{channel}']")

            for row in guide_rows:
                program_blocks = row.find_elements(By.CLASS_NAME, "guide__row__block")

                for block in program_blocks:
                    try:
                        h4_element = block.find_element(By.TAG_NAME, "h4")
                        program_name = h4_element.text.strip()

                        p_element = block.find_element(By.TAG_NAME, "p")
                        program_info = p_element.text.strip() if p_element else "Sin información adicional"

                        a_element = block.find_element(By.TAG_NAME, "a")
                        program_link = a_element.get_attribute("href") if a_element else "Sin enlace"

                        program_time = program_info if program_info else "Transmitiendo ahora"

                        if program_name:
                            city_tv_guide[(city, region)][channel].append((program_name, program_time, program_link))
                    except:
                        continue

# Cerrar el navegador
driver.quit()

# Guardar los datos en CSV
csv_filename = 'tv_guide_by_city.csv'

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Ciudad", "Región", "Canal", "Programa", "Horario", "Enlace"])

    for (city, region), channels in city_tv_guide.items():
        for channel, programs in channels.items():
            for program in programs:
                writer.writerow([city, region, channel, program[0], program[1], program[2]])

print(f"Los datos se han guardado en {csv_filename}")

# Guardar tiempo de ejecución
execution_time = (time.time() - start_time) / 60
execution_time_filename = 'execution_time.txt'

with open(execution_time_filename, mode='w', encoding='utf-8') as file:
    file.write(f"Tiempo de ejecución: {execution_time:.2f} minutos")

print(f"El tiempo de ejecución se ha guardado en {execution_time_filename}")
