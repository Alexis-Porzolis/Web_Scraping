# 📺 Web Scraping de TV Guide

## 🚀 Introducción

Este script en Python realiza scraping de la guía de TV del sitio web [9Now TV Guide](https://tvguide.9now.com.au/) para extraer información relevante sobre los canales y su programación.

### 🎯 **Objetivos**

✔ Obtener la lista de regiones y sus respectivas ciudades.  
✔ Extraer la programación de cada canal con sus metadatos clave.  
✔ Guardar los datos estructurados en un archivo CSV.  
✔ Medir e imprimir el tiempo de ejecución.

---

## 📦 Tecnologías Utilizadas

- **Python** 🐍
- **Selenium** 🌐 (Para automatizar la navegación web)
- **CSV** 📄 (Para almacenamiento de datos)
- **Time** ⏳ (Para medir tiempos de ejecución)

---

## ⚙ Configuración del WebDriver

El script utiliza **Microsoft Edge WebDriver**.  
También se puede utilizar **Chrome** o **Firefox** reemplazando:

```python
driver = webdriver.Edge(service=service)  # Cambiar 'Edge' por 'Chrome' o 'Firefox'
```

Asegúrate de tener el **WebDriver correspondiente** instalado en tu sistema.

---

## 🛠 Estructura del Código

El proceso de scraping se divide en dos funciones principales:

### **1️⃣ Extracción de Regiones**

📌 `extract_regions()` obtiene todas las regiones y ciudades disponibles en la plataforma, almacenándolas en `regions_info`.

### **2️⃣ Extracción de Programación de TV**

📌 `extract_tv_guide()` navega por cada ciudad de `regions_info`, accede a la guía de TV y extrae la programación de cada canal, guardándola en `city_tv_guide`.

---

## 💾 Almacenamiento de Datos

Los datos extraídos se guardan en **CSV** con las siguientes columnas:

- 📍 **Ciudad**
- 🏛 **Región**
- 📡 **Canal**
- 🎬 **Programa**
- 🕒 **Horario**
- 🔗 **Enlace**

Además, el tiempo total de ejecución se guarda en `execution_time.txt`.

---

## 📝 Autor

📌 **Alexis Porzolis**
