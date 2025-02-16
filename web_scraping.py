import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import time

# Iniciar el temporizador
start_time = time.time()

# URL del sitio web
url = 'https://www.9now.com.au/'

# Realizar la solicitud HTTP
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Buscar el enlace específico
tv_guide_link = soup.find('a', title='Go to the TV Guide page')['href']

# Imprimir el enlace
print(tv_guide_link)
