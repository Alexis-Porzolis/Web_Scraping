from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

# Ruta del driver de Edge
driver_path = 'C:/edgedriver/edgedriver_win64/msedgedriver.exe'

# Configurar opciones para evitar el conflicto con el directorio de usuario
edge_options = Options()
# Evita conflictos con sesiones activas
edge_options.add_argument("--remote-debugging-port=9222")
# Creamos un perfil temporal
edge_options.add_argument("--user-data-dir=C:/temp_edge_profile")

# Iniciar el servicio y el driver
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=edge_options)

# Abrir la URL
driver.get('https://tvguide.9now.com.au/guide/')

# Obtener la lista de nombres de canales
channel_divs = driver.find_elements(By.CLASS_NAME, "channel-icon")
channel_names = [div.get_attribute("data-channel-name")
                 for div in channel_divs if div.get_attribute("data-channel-name")]

# Diccionario para almacenar la información
tv_guide = {}

# Iterar sobre cada canal y obtener sus programas
for channel in channel_names:
    tv_guide[channel] = []  # Inicializar lista de programas para el canal

    # Buscar el 'guide__row' correspondiente al canal, verificando que la clase contenga 'guide__row'
    guide_rows = driver.find_elements(
        By.XPATH, f"//div[contains(@class, 'guide__row') and @data-channel-name='{channel}']")

    for row in guide_rows:
        # Intentar obtener los bloques de programas directamente
        program_blocks = row.find_elements(By.CLASS_NAME, "guide__row__block")

        # Si no se encontraron, buscar dentro de un nivel más profundo
        if not program_blocks:
            sub_divs = row.find_elements(
                By.XPATH, "./div")  # Obtener hijos directos
            for sub_div in sub_divs:
                program_blocks.extend(sub_div.find_elements(
                    By.CLASS_NAME, "guide__row__block"))

        for block in program_blocks:
            try:
                h4_element = block.find_element(By.TAG_NAME, "h4")
                program_name = h4_element.text.strip()

                # Intentar obtener el atributo <p> relacionado con el programa
                p_element = block.find_element(By.TAG_NAME, "p")
                program_info = p_element.text.strip() if p_element else "Sin información adicional"

                # Intentar obtener el enlace <a> con el atributo href
                a_element = block.find_element(By.TAG_NAME, "a")
                program_link = a_element.get_attribute(
                    "href") if a_element else "Sin enlace"

                # Relacionar nombre del programa, horario y enlace
                if program_name:  # Asegurar que no agregamos vacíos
                    tv_guide[channel].append(
                        (program_name, program_info, program_link))
            except:
                continue  # Si no encuentra el h4, p, o a, simplemente sigue con el siguiente

# Cerrar el navegador
driver.quit()

# Mostrar los resultados
for channel, programs in tv_guide.items():
    print(f"\nCanal: {channel}")
    for program in programs:
        print(f"  - Programa: {program[0]}")
        print(f"    - Horario: {program[1]}")
        print(f"    - Enlace: {program[2]}")
