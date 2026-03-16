import scrap_alquileres_gallito_luis as gallito
import scrap_alquileres_infocasas as infocasas
import scrap_alquileres_mercadolibre as mercadolibre
import json

def parse_precio(precio_str):
    if not precio_str:
        return float('inf')  # Put ones without price at the end
    
    # Remove dots and commas
    clean_str = precio_str.replace(".", "").replace(",", "").strip()
    try:
        return float(clean_str)
    except ValueError:
        return float('inf')

def main():
    print("Iniciando Gestor de Scrapers...\n")
    
    # 1. Scraping Gallito Luis
    print("--- 1. Scraping Gallito Luis ---")
    url_gallito = "https://www.gallito.com.uy/inmuebles/casas/alquiler/montevideo/otros/pre-0-21000-pesos"
    html_gallito = gallito.fetch_html(url_gallito)
    datos_gallito = []
    if html_gallito:
        datos_gallito = gallito.parse_html_alquileres(html_gallito)
        for d in datos_gallito:
            d["es_dueno"] = False
        print(f"Extraídos {len(datos_gallito)} inmuebles de Gallito Luis.")
    else:
        print("Fallo al obtener HTML de Gallito Luis.")
        
    # Casasweb removed as requested
    print("\n--- 3. Scraping Infocasas ---")
    urls_infocasas = [
        "https://www.infocasas.com.uy/alquiler/inmuebles/canelones/neptunia/hasta-21000/pesos",
        "https://www.infocasas.com.uy/alquiler/hasta-21000/pesos?&searchstring=villa-aeroparque",
        "https://www.infocasas.com.uy/alquiler/inmuebles/canelones/colonia-nicolich/hasta-21000/pesos",
        "https://www.infocasas.com.uy/alquiler/casas/canelones/barros-blancos/hasta-21000/pesos"
    ]
    datos_infocasas = []
    
    for url in urls_infocasas:
        html_infocasas = infocasas.fetch_html(url)
        if html_infocasas:
            datos_nuevos = infocasas.parse_html_alquileres_infocasas(html_infocasas)
            for d in datos_nuevos:
                d["es_dueno"] = False
            datos_infocasas.extend(datos_nuevos)
            print(f"Extraídos {len(datos_nuevos)} inmuebles de: {url}")
        else:
            print(f"Fallo al obtener HTML de: {url}")
            
    print(f"Total extraídos de Infocasas: {len(datos_infocasas)}")

    print("\n--- 4. Scraping Mercadolibre ---")
    urls_mercadolibre = [
        {"url": "https://listado.mercadolibre.com.uy/inmuebles/casas/alquiler/canelones/dueno/casas-alquiler-barros-blancos%2C-neptunia_PriceRange_0UYU-21000UYU_NoIndex_True_PARKING*LOTS_1-1?sb=category#applied_filter_id%3Dseller_type%26applied_filter_name%3DPublica%26applied_filter_order%3D4%26applied_value_id%3Dprivate_seller%26applied_value_name%3DVendido+por+su+due%C3%B1o%26applied_value_order%3D2%26applied_value_results%3D1%26is_custom%3Dfalse", "es_dueno": True},
        {"url": "https://listado.mercadolibre.com.uy/inmuebles/casas/alquiler/canelones/casas-alquiler-barros-blancos%2C-neptunia_PriceRange_0UYU-21000UYU_NoIndex_True_PARKING*LOTS_1-1?sb=category#applied_filter_id%3DPARKING_LOTS%26applied_filter_name%3DCocheras%26applied_filter_order%3D10%26applied_value_id%3D[1-1]%26applied_value_name%3D1+cochera%26applied_value_order%3D2%26applied_value_results%3D5%26is_custom%3Dfalse", "es_dueno": False}
    ]
    datos_mercadolibre = []
    
    for item in urls_mercadolibre:
        html_mercadolibre = mercadolibre.fetch_html(item["url"])
        if html_mercadolibre:
            nuevos = mercadolibre.parse_html_mercadolibre(html_mercadolibre)
            for n in nuevos:
                n["es_dueno"] = item["es_dueno"]
            datos_mercadolibre.extend(nuevos)
            tipo_meli = "Dueño" if item["es_dueno"] else "General"
            print(f"Extraídos {len(nuevos)} inmuebles de Mercadolibre ({tipo_meli}).")
        else:
            print("Fallo al obtener HTML de Mercadolibre.")

    # 5. Consolidar datos
    datos_sin_filtrar = datos_gallito + datos_infocasas + datos_mercadolibre
    
    # 4.1. Filtrar precios fuera del rango 10.000 - 20.000 pesos
    todos_los_datos = []
    for dato in datos_sin_filtrar:
        precio_val = parse_precio(dato.get('precio', ''))
        moneda = str(dato.get('moneda', '')).upper()
        
        # NO Conservar si está en dólares (asumiendo que los montos en USD son siempre válidos)
        if "U$S" in moneda or "USD" in moneda:
            pass
        # O si está en pesos y está en el rango [10000, 20000]
        elif (precio_val >= 10000 and precio_val <= 21000) or precio_val == float('inf'): # Conservar si no tiene precio claro
            todos_los_datos.append(dato)
            
    # Ignorar los extraídos que fueron eliminados
    eliminados = len(datos_sin_filtrar) - len(todos_los_datos)
    if eliminados > 0:
        print(f"\nSe eliminaron {eliminados} publicaciones molestas (fuera del rango $10.000 - $21.000).")

    if not todos_los_datos:
        print("\nNo se encontraron datos en ninguno de los scrappers después de filtrar. Saliendo.")
        return
        
    print(f"\n--- 5. Procesando {len(todos_los_datos)} inmuebles en total ---")
    
    # 6. Ordenar datos
    print("Ordenando listado (Dueño ML primero, luego InfoCasas, Gallito Luis y general)...")
    
    def sort_key(x):
        # 0 para Dueño directo ML
        # 1 para Infocasas
        # 2 para Gallito
        # 3 para ML General (u otros)
        url_val = x.get('url', '').lower()
        if x.get('es_dueno', False):
            fuente_prioridad = 0
        elif "infocasas" in url_val:
            fuente_prioridad = 1
        elif "gallito" in url_val:
            fuente_prioridad = 2
        else:
            fuente_prioridad = 3
            
        # Precio negativo para que sea descendente (parse_precio devuelve inf para nulos, lo cual es correcto)
        precio = parse_precio(x.get('precio', ''))
        return (fuente_prioridad, -precio)

    todos_los_datos.sort(key=sort_key)
    
    # 7. Guardar en Excel y JSON
    print("Generando Excel y JSON final unificado y ordenado...")
    archivo_salida_xlsx = "alquileres.xlsx"
    archivo_salida_json = "alquileres.json"
    
    import datetime
    ahora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    json_output = {
        "last_updated": ahora,
        "data": todos_los_datos
    }
    
    # Guardar en JSON (Asegurando codificación UTF-8 para caracteres especiales)
    with open(archivo_salida_json, "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=4)
        
    import os
    # Crear carpeta public del frontend si no existe y copiar ahí el json también
    os.makedirs(os.path.join("frontend", "public"), exist_ok=True)
    with open(os.path.join("frontend", "public", "alquileres.json"), "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=4)
        
    # Utilizamos la función de gallito que crea un archivo nuevo desde cero con las imágenes
    gallito.save_to_excel(todos_los_datos, archivo_salida_xlsx)
    
    print(f"\n¡Proceso finalizado con éxito! Los archivos generados son: {archivo_salida_xlsx} y {archivo_salida_json}")

if __name__ == "__main__":
    main()
