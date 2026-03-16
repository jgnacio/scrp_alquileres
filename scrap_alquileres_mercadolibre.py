import requests
from bs4 import BeautifulSoup
import time

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Accept': '*/*'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"Status Code Meli ({url[:30]}...): {response.status_code}")
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(f"Error al obtener HTML de Mercadolibre: {e}")
        return None

def parse_html_mercadolibre(html_listado):
    datos = []
    soup = BeautifulSoup(html_listado, 'html.parser')
    
    avisos = soup.find_all('li', class_='ui-search-layout__item')
    print(f"Se encontraron {len(avisos)} avisos en el listado de MercadoLibre.")
    if len(avisos) == 0:
        print("HTML snippet:")
        print(html_listado[:1000])
    
    for aviso in avisos:
        enlace_tag = aviso.find('a', class_='poly-component__title')
        if not enlace_tag:
            continue
        url_detalle = enlace_tag.get('href')
        titulo = enlace_tag.text.strip()
        
        img_tag = aviso.find('img', class_='poly-component__picture')
        imagen_url = img_tag.get('src', '') if img_tag else ''
        if not imagen_url and img_tag:
            # Mercadolibre a veces usa data-src o similares en listados lazy load
            imagen_url = img_tag.get('data-src', '')
            
        precio_monto = ''
        precio_moneda = ''
        precio_tag = aviso.find('span', class_='andes-money-amount__fraction')
        moneda_tag = aviso.find('span', class_='andes-money-amount__currency-symbol')
        if precio_tag:
            precio_monto = precio_tag.text.strip()
        if moneda_tag:
            precio_moneda = moneda_tag.text.strip()
            if precio_moneda == '$':
                precio_moneda = 'UYU'

        # Ahora ingresamos a la pagina individual para sacar detalles como M2
        html_detalle = fetch_html(url_detalle)
        
        detalles_str = ""
        area_m2 = ""
        
        if html_detalle:
            soup_det = BeautifulSoup(html_detalle, 'html.parser')
            
            detalles_text = []
            specs = soup_det.find_all('div', class_='ui-pdp-highlighted-specs-res__icon-label')
            for spec in specs:
                lbl = spec.find("span", class_="ui-pdp-label")
                if lbl:
                    text_clean = lbl.text.strip()
                    detalles_text.append(text_clean)
                    if 'm²' in text_clean or 'm2' in text_clean:
                        area_m2 = text_clean.replace('totales', '').replace('cubiertos', '').strip()

            detalles_str = " | ".join(detalles_text)
            time.sleep(1) # delay
            
        datos.append({
            'imagen_url': imagen_url,
            'moneda': precio_moneda,
            'precio': precio_monto,
            'titulo': titulo,
            'detalles': detalles_str,
            'area_m2': area_m2,
            'id': '',
            'tiene_telefono': '', 
            'whatsapp_link': '', 
            'url': url_detalle
        })

    return datos
