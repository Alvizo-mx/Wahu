import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
import requests
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

from fake_useragent import UserAgent

import time
from datetime import datetime
import random


# Variables de tipo listas donde se guardara nuestra informacion 

Fecha = []
Id_stock = []
URL_auto = []
URL_image = []
Estatus = []
T_invenario = []
Marca = []
Modelo = []
Año = []
Km = []
Version = []
Transmision = []
Color = []
Costo_normal = []
Oferta = []
Mensualidades = []
Ubicacion = []

URL_actual = []
Tamaño_coches = []
Posicion_coche = []
Total_paginas = []



# https://www.kavak.com/mx/seminuevos/?
url = 'https://www.kavak.com/mx/seminuevos/?' 
 
# Utiliza Beautiful Soup para analizar el total de paginas en este momento
response = requests.get(url)
print(response.status_code)
soup = BeautifulSoup(response.content,"html.parser")

n_paginas = soup.find_all("a",{'class': 'results_results__pagination-item__2wkpb'})[4].get_text()

# Cambiando el agente de usuario por primera vez
options = Options()
ua = UserAgent()
user_agent = ua.random

# Define los encabezados de la solicitud
headers = {
    'User-Agent': user_agent
}


# Codigo: for i in range(int(n_paginas) - 1):

for i in range(int(n_paginas)):
  # https://www.kavak.com/mx/seminuevos/?page=0                         normal
  # https://www.kavak.com/mx/seminuevos/?order=higher_price&page=1      mayor precio
  # https://www.kavak.com/mx/seminuevos/?order=lower_mileage&page=1     menos kilometraje
  url ="https://www.kavak.com/mx/seminuevos/?order=higher_price&page="+ str(i) 
  response=requests.get(url, headers=headers) 

  if i % 20 == 0:
    # Cambiando el agente de usuario 
    options = Options()
    ua = UserAgent()
    user_agent = ua.random

  # Si el estatus de la pagina, es bueno entonces entramos de lo contrario agregamos info de el error y continuamos 
  if response.status_code == 200:
    # Configuracion de selenium
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Evita que el sitio web detecte que estás utilizando Selenium
    options.add_argument("--start-maximized")  # Inicia el navegador maximizado
    options.add_argument(f'--user-agent={user_agent}')
    driver_path = r'C:\Users\Wahu\Documents\chromedriver-win64\chromedriver.exe' 
    options.add_argument(f"webdriver.chrome.driver={driver_path}")

    driver = webdriver.Chrome(options=options) #Creamos un driver cada vez que visitamos una página
    driver.get(url)

    # Espera a que la página cargue completamente
    time.sleep(random.uniform(3, 6))

    # Hace scroll hacia abajo suavemente utilizando JavaScript
    scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

    scroll_increment = 100  # Ajusta según sea necesario
    num_scrolls = int(scroll_height / scroll_increment)

    for _ in range(num_scrolls):
      driver.execute_script("window.scrollTo(0, {});".format(scroll_increment))
      time.sleep(0.4)  # Ajusta según sea necesario para dar tiempo a cargar los elementos
      scroll_increment += 150  # Ajusta según sea necesario para el tamaño de la pagina


    # Obtiene el contenido HTML de la página después de interactuar con ella
    html = driver.page_source

    # Utiliza Beautiful Soup para analizar el contenido HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Espera un poco más después del último scroll
    time.sleep(random.uniform(3, 6))

    
    # Extrayendo la informacion
    for i in range(len(soup.find_all("a",{'class': 'card-product_cardProduct__3qZCJ'}))):
      fecha_actual = datetime.now()
      Fecha.append(fecha_actual)

      find_id = soup.find_all("a",{'class': 'card-product_cardProduct__3qZCJ'})[i].get("data-testid")
      kkk_id = find_id.split('-')[-1]
      Id_stock.append(kkk_id)
      
      URL_auto.append(soup.find_all("a",{'class': 'card-product_cardProduct__3qZCJ'})[i].get('href'))

      URL_image.append(soup.find_all("div",{'class': 'card-product_cardProduct__imageContainer__nn_0a'})[i].find("img").get('src'))

      Estatus.append(soup.find_all("div",{'class': 'card-product_cardProduct__imageContainer__nn_0a'})[i].get_text("div",{'class': 'card-product_cardProduct__badgesContainer__V35qk'}))

      T_invenario.append("Sin datos")

      auto = soup.find_all("h3",{'class': 'card-product_cardProduct__title__RR0CK'})[i].get_text()
      # Creamos un separador
      separador = auto.split(' • ')
      # Ahora 'separador' es una lista que contiene cada parte separada
      Marca.append(separador[0])
      Modelo.append(separador[1])

      Caracteristicas = soup.find_all("p",{'class': 'card-product_cardProduct__subtitle__hbN2a'})[i].get_text()
      # Creamos un separador
      elementos = Caracteristicas.split(' • ')
      # Ahora 'elementos' es una lista que contiene cada parte separada
      Año.append(elementos[0])
      Km.append(elementos[1])
      Version.append(elementos[2])
      Transmision.append(elementos[3])
                                       
      # Usando un condicional para manejar el NoneType
      costo_norm = soup.find_all('div',{'class': 'card-product_cardProduct__priceContainer__3T0tb'})[i].find('span', {'class':'card-product_cardProduct__price__Er33n'})

      if costo_norm is not None:
          Costo_normal.append(costo_norm.text)
      else:
          Costo_normal.append("Sin datos")

      oferta_text = soup.find_all('div', {'class': 'card-product_cardProduct__priceMainContainer__ex_hf'})[i].find('span', {'class': 'amount_uki-amount__large__price__2NvVx'})
      if oferta_text:
          Oferta.append(oferta_text.text)
      else:
          Oferta.append("Sin datos") 

      impar_num = 2 * i + 1  # Calcula el i-ésimo número impar
      mensualidad_text = soup.find_all('span',{'class': 'card-product_cardProduct__priceSection__2GKb8'})[impar_num]
      if mensualidad_text:
          Mensualidades.append(mensualidad_text.text)
      else:
          Mensualidades.append("Sin datos")

      Ubicacion.append(soup.find_all('div',{'class': 'card-product_cardProduct__footer__MQKa_'})[i].get_text())

      # Informacion para analizar
      URL_actual.append(driver.current_url)

      Tamaño_coches.append(len(soup.find_all("a",{'class': 'card-product_cardProduct__3qZCJ'})))

      Posicion_coche.append(i)

      Total_paginas.append(n_paginas)


    driver.close() #Cerramos el driver una vez tenemos la información
        
  else:
    fecha_actual = datetime.now()
    Fecha.append(fecha_actual)
    Id_stock.append(url)
    URL_auto.append("URL_ERROR")
    URL_image.append("URL_ERROR")
    Estatus.append("URL_ERROR")
    T_invenario.append("URL_ERROR")
    Marca.append("URL_ERROR")
    Modelo.append("URL_ERROR")
    Año.append("URL_ERROR")
    Km.append("URL_ERROR")
    Version.append("URL_ERROR")
    Transmision.append("URL_ERROR")
    Costo_normal.append("URL_ERROR")
    Oferta.append("URL_ERROR")
    Mensualidades.append("URL_ERROR")
    Ubicacion.append("URL_ERROR")
    URL_actual.append("URL_ERROR")
    Tamaño_coches.append("URL_ERROR")
    Posicion_coche.append("URL_ERROR")
    Total_paginas.append("URL_ERROR")
    continue
    
    
driver.quit() #Cerramos el driver una vez tenemos la información


# Creamos un archivo pandas con los arreglos 
THE_SKKKAPER_Jupyter_ = pd.DataFrame({'Fecha':Fecha,'Id_stock':Id_stock,'URL_actual':URL_actual,'Tamaño_coches':Tamaño_coches,'Posicion_coche':Posicion_coche,
                                        'Total_paginas':Total_paginas ,'URL_auto':URL_auto,
                                        'URL_image':URL_image,'Estatus':Estatus,'T_invenario':T_invenario,'Marca':Marca,'Modelo':Modelo,'Version':Version,
                                        'Año':Año,'Km':Km,'Transmision':Transmision,
                                        'Costo_normal':Costo_normal, 'Oferta':Oferta,'Mensualidades':Mensualidades,'Ubicacion':Ubicacion})

# Rellenando valores NaN
THE_SKKKAPER_Jupyter_.fillna("Sin datos", inplace=True)

# Rellenando la columna estatus si tiene alguna cadena vacia
THE_SKKKAPER_Jupyter_['Estatus'].replace('', 'Sin etiqueta', inplace=True)

# Obtén la fecha actual con el formato dia-mes-año
# fecha_actual = datetime.now().strftime("%d-%m-%Y")
fecha_actual = datetime.now().strftime("%d-%m-%Y-%H")

# Agrega la fecha al nombre del DataFrame
nombre_del_df = f"THE_SKKKAPER_{fecha_actual}"

# Guarda el DataFrame en un archivo de CSV con el nuevo nombre
ruta_excel = f"{nombre_del_df}.csv" # Para excel usar .xlsx como extension
# THE_SKKKAPER_.to_excel(ruta_excel, index=False)

# Guarda el DataFrame en un archivo de CSV con el nuevo nombre
THE_SKKKAPER_Jupyter_.to_csv(ruta_excel, sep ="|" ,index=False)

print('Saved file: ' + ruta_excel)