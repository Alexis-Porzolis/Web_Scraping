# 📺 Web Scraping de TV Guide

## 🚀 Introducción

Este proyecto consta de dos scripts principales en Python que permiten obtener, procesar y visualizar la guía de programación de TV del sitio web [9Now TV Guide](https://tvguide.9now.com.au/).

1. **`script_web_scraping.py`**: Se encarga de realizar web scraping para extraer la programación de TV y guardarla en un archivo CSV.
2. **`script_data_processing.ipynb`**: Realiza la carga, limpieza, almacenamiento en SQLite y visualización de los datos extraídos.

---

## 🎯 **Objetivos**

### `script_web_scraping.py`

✔ Obtener la lista de regiones y sus respectivas ciudades.  
✔ Extraer la programación de cada canal con sus metadatos clave.  
✔ Guardar los datos estructurados en un archivo CSV.  
✔ Medir e imprimir el tiempo de ejecución.

### `script_data_processing.ipynb`

✔ Leer el archivo CSV generado por el script de scraping.  
✔ Realizar limpieza de datos, eliminando valores nulos.  
✔ Visualizar los 10 programas más transmitidos mediante un gráfico de barras.  
✔ Crear una base de datos en SQLite con un modelo dimensional.  
✔ Poblar las tablas dimensionales y de hechos con la información extraída.

---

## 📦 **Tecnologías Utilizadas**

- **Python** 🐍
- **Selenium** 🌐 (Para automatizar la navegación web)
- **CSV** 📄 (Para almacenamiento de datos)
- **SQLite** 📂 (Para almacenar y procesar los datos estructurados)
- **Matplotlib & Seaborn** 🎨 (Para visualización de datos)

---

## ⚙ **Configuración del WebDriver**

El script de scraping utiliza **Microsoft Edge WebDriver**.  
Se puede cambiar por **Chrome** o **Firefox** reemplazando:

```python
driver = webdriver.Edge(service=service)  # Cambiar 'Edge' por 'Chrome' o 'Firefox'
```

Asegúrate de tener el **WebDriver correspondiente** instalado en tu sistema.

---

## 🛠 **Estructura del Código**

### **1️⃣ Extracción de Datos (`script_web_scraping.py`)**

📌 `extract_regions()` obtiene todas las regiones y ciudades disponibles en la plataforma.  
📌 `extract_tv_guide()` extrae la programación de TV de cada ciudad y la almacena en un archivo CSV.

### **2️⃣ Procesamiento y Visualización (`script_data_processing.ipynb`)**

📌 Carga el archivo CSV en un DataFrame de Pandas.  
📌 Realiza una limpieza eliminando valores nulos.  
📌 Visualiza los 10 programas más transmitidos mediante Seaborn y Matplotlib.  
📌 Crea una base de datos SQLite con un modelo dimensional.  
📌 Inserta los datos procesados en las tablas dimensionales y de hechos.

---

## 💾 **Almacenamiento de Datos**

Los datos extraídos se guardan en **CSV** con las siguientes columnas:

- 📍 **Ciudad**
- 🏢 **Región**
- 📰 **Canal**
- 🎬 **Programa**
- 🕒 **Horario**
- 🔗 **Enlace**

Luego, el procesamiento almacena estos datos en **SQLite** siguiendo un modelo de base de datos dimensional.

---

## 📝 Autor

📌 **Alexis Porzolis**
