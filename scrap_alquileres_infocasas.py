import cloudscraper
from bs4 import BeautifulSoup
import json
import logging

logging.basicConfig(level=logging.INFO)

def fetch_html(url):
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        response = scraper.get(url, timeout=15)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to get 200 OK. Content preview:")
            print(response.text[:500])
            return None
    except Exception as e:
        print(f"Exception fetching url for Infocasas: {e}")
        return None

def parse_html_alquileres_infocasas(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    articles = soup.select(".listingCard")
    print(f"Se encontraron {len(articles)} avisos en el HTML de infocasas.")

    inmuebles = []

    for article in articles:
        try:
            inmueble = {}
            
            a_tag = article.select_one("a.lc-data")
            if a_tag:
                href = a_tag.get("href", "")
                if href and not href.startswith("http"):
                    inmueble['url'] = "https://www.infocasas.com.uy" + href
                else:
                    inmueble['url'] = href
            else:
                inmueble['url'] = ""

            inmueble['id'] = ""
            if inmueble['url']:
                # Example: https://www.infocasas.com.uy/alquiler/.../193415003
                inmueble['id'] = inmueble['url'].split('/')[-1]

            # Title
            title_tag = article.select_one(".lc-title")
            inmueble['titulo'] = title_tag.text.strip().replace("\n", " ") if title_tag else ""

            # Price
            price_tag = article.select_one(".main-price")
            if price_tag:
                price_text = price_tag.text.strip()
                # Usually "$ 17.500" or "U$S 500"
                parts = price_text.split(" ", 1)
                if len(parts) == 2:
                    inmueble['moneda'] = parts[0].strip()
                    inmueble['precio'] = parts[1].strip()
                else:
                    inmueble['moneda'] = ""
                    inmueble['precio'] = price_text
            else:
                inmueble['moneda'] = ""
                inmueble['precio'] = ""

            # Area
            tags = article.select(".lc-typologyTag__item strong")
            area_str = ""
            for tag in tags:
                if "m²" in tag.text:
                    area_str = tag.text.replace("m²", "").strip()
            inmueble['area_m2'] = area_str

            # Details
            desc_tag = article.select_one(".lc-description")
            inmueble['detalles'] = desc_tag.text.strip().replace("\n", " ") if desc_tag else ""

            # Phone / WhatsApp
            phone_btn = article.select_one(".phone-button")
            inmueble['tiene_telefono'] = bool(phone_btn)
            
            wpp_btn = article.select_one(".wpp-button")
            inmueble['whatsapp_link'] = "Sí" if wpp_btn else ""

            # Image
            img_tag = article.select_one(".gallery-image img")
            inmueble['imagen_url'] = img_tag.get("src", "") if img_tag else ""

            # Align keys
            inmueble_norm = {
                'url': inmueble.get('url', ''),
                'titulo': inmueble.get('titulo', ''),
                'id': inmueble.get('id', ''),
                'detalles': inmueble.get('detalles', ''),
                'moneda': inmueble.get('moneda', ''),
                'precio': inmueble.get('precio', ''),
                'area_m2': inmueble.get('area_m2', ''),
                'tiene_telefono': inmueble.get('tiene_telefono', False),
                'whatsapp_link': inmueble.get('whatsapp_link', ''),
                'imagen_url': inmueble.get('imagen_url', '')
            }

            inmuebles.append(inmueble_norm)
        except Exception as e:
            print(f"Error al procesar un aviso de infocasas: {e}")
            continue

    return inmuebles
