from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import csv
import time

# Ruta del driver (en este caso, Microsoft Edge)
driver_path = "./msedgedriver.exe"
service = Service(driver_path)
driver = webdriver.Edge(service=service)

# Nota: Se puede usar Chrome o Firefox cambiando 'Edge' por 'Chrome' o 'Firefox' y usando el driver correspondiente.

# Medimos el tiempo de ejecución
start_time = time.time()

# Abrimos la web de la guía de TV
driver.get('https://tvguide.9now.com.au/guide/')
time.sleep(5)  # Esperamos que la página cargue

# Diccionario para almacenar regiones y ciudades
regions_info = {}
region_container = driver.find_element(
    By.CSS_SELECTOR, ".user-prefs.user-prefs--regions")
region_items = region_container.find_elements(By.CLASS_NAME, "pick-list__item")

# Extraemos las regiones y ciudades


def extract_regions():
    for item in region_items:
        try:
            a_element = item.find_element(By.TAG_NAME, "a")
            city_name = a_element.get_attribute("data-region-name")
            region_name = a_element.get_attribute("data-region-state")
            city_url = a_element.get_attribute("href")
            if region_name not in regions_info:
                regions_info[region_name] = {}
            regions_info[region_name][city_name] = city_url
        except Exception as e:
            print(f"Error al procesar la región: {e}")


extract_regions()

# Diccionario para almacenar programación por ciudad
city_tv_guide = {}

# Extraemos la programación de cada ciudad y canal


def extract_tv_guide():
    for region, cities in regions_info.items():
        for city, city_url in cities.items():
            driver.get(city_url)
            city_tv_guide[(city, region)] = {}
            channel_divs = driver.find_elements(By.CLASS_NAME, "channel-icon")
            channel_names = [div.get_attribute(
                "data-channel-name") for div in channel_divs if div.get_attribute("data-channel-name")]
            for channel in channel_names:
                city_tv_guide[(city, region)][channel] = []
                guide_rows = driver.find_elements(
                    By.XPATH, f"//div[contains(@class, 'guide__row') and @data-channel-name='{channel}']")
                for row in guide_rows:
                    program_blocks = row.find_elements(
                        By.CLASS_NAME, "guide__row__block")
                    for block in program_blocks:
                        try:
                            program_name = block.find_element(
                                By.TAG_NAME, "h4").text.strip()
                            program_time = block.find_element(
                                By.TAG_NAME, "p").text.strip()
                            program_link = block.find_element(
                                By.TAG_NAME, "a").get_attribute("href")
                            if program_name:
                                city_tv_guide[(city, region)][channel].append(
                                    (program_name, program_time, program_link))
                        except:
                            continue


extract_tv_guide()

# Guardamos los datos en CSV
csv_filename = 'tv_guide_by_city.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Ciudad", "Región", "Canal",
                    "Programa", "Horario", "Enlace"])
    for (city, region), channels in city_tv_guide.items():
        for channel, programs in channels.items():
            for program in programs:
                writer.writerow(
                    [city, region, channel, program[0], program[1], program[2]])

print(f"Los datos se han guardado en {csv_filename}")

# Guardamos el tiempo de ejecución
time_elapsed = (time.time() - start_time) / 60
with open("execution_time.txt", "w", encoding="utf-8") as file:
    file.write(f"Tiempo de ejecución: {time_elapsed:.2f} minutos")

print("Tiempo de ejecución guardado en execution_time.txt")

driver.quit()  # Cerramos el navegador
