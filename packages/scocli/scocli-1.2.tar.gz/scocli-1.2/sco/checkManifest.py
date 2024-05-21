#!/usr/bin/env python3
import os
from xml.etree import ElementTree as ET

def recopilar_archivos(ruta, recursos):
    archivos = []
    archivos_no_utilizados = []
    # Files to ignore
    ignore_files = ["package-lock.json", "package.json", "imsmanifest.xml", "node_modules/.package-lock.json", "node_modules/scoapi/scoAPI.js", "node_modules/scoapi/package.json"]
    # Extensions to ignore
    ignore_extensions = [".zip", ".babelrc"]

    for root, dirs, files in os.walk(ruta):
        for file in files:
            archivo = os.path.relpath(os.path.join(root, file), ruta)
            archivos.append(archivo)
            # Check if the file is in the ignore list
            if archivo in ignore_files or file.endswith(tuple(ignore_extensions)):
                continue
            # Comprobar si el archivo no está en los recursos definidos
            if archivo not in recursos:
                archivos_no_utilizados.append(archivo)
    return archivos, archivos_no_utilizados


def validar_archivos_necesarios(raiz_proyecto):
    # Lista de archivos necesarios en un proyecto SCORM
    archivos_necesarios = [
        "imsmanifest.xml",
    ]

    for elemento in archivos_necesarios:
        ruta_elemento = os.path.join(raiz_proyecto, elemento)
        if not os.path.exists(ruta_elemento):
            print(f"Error: No se encontró el elemento necesario '{elemento}'")
            return False

    print("La validación de los archivos necesarios se ha completado correctamente.")
    return True

def validar_imsmanifest(ruta_imsmanifest):
    try:
        tree = ET.parse(ruta_imsmanifest)
        root = tree.getroot()

        # Definir el espacio de nombres
        ns = {
            'ims': 'http://www.imsglobal.org/xsd/imscp_v1p1',
            'ns2': 'http://www.adlnet.org/xsd/adlcp_v1p3'
        }

        # Obtener todos los archivos asociados a los recursos definidos en imsmanifest.xml
        recursos = set()
        files = set()
        for resource in root.findall(".//{http://www.imsglobal.org/xsd/imscp_v1p1}resource", namespaces=ns):
            identifier = resource.attrib['identifier']
            for file_elem in resource.findall(".//{http://www.imsglobal.org/xsd/imscp_v1p1}file", namespaces=ns):
                href = file_elem.attrib['href']
                recursos.add(href)
                files.add((identifier, href))

        # Obtener los identifierref de los items dentro de organization
        organization_items = root.findall(".//ims:organizations/ims:organization/ims:item", namespaces=ns)
        for item in organization_items:
            identifierref = item.attrib['identifierref']
            for identifier, href in files:
                if identifierref == identifier:
                    recursos.add(href)

        #print("recursos:", recursos)
        #print("organization_items:", organization_items)
        print("La validación de imsmanifest.xml se ha completado correctamente.")
        return recursos

    except Exception as e:
        print(f"Error al analizar el archivo imsmanifest.xml: {e}")
        return set()

if __name__ == "__main__":
    # Buscar imsmanifest.xml en el directorio actual
    ruta_actual = os.getcwd()
    ruta_imsmanifest = os.path.join(ruta_actual, "imsmanifest.xml")

    if not os.path.exists(ruta_imsmanifest):
        print("Error: No se encontró el archivo imsmanifest.xml en el directorio actual.")
    else:
        # Validar archivos necesarios
        if not validar_archivos_necesarios(ruta_actual):
            print("El proyecto SCORM no está completo o tiene errores.")
        else:
            # Validar imsmanifest.xml
            recursos = validar_imsmanifest(ruta_imsmanifest)
            if not recursos:
                print("El proyecto SCORM no está completo o tiene errores.")
            else:
                # Recopilar todos los archivos en el proyecto
                archivos, archivos_no_utilizados = recopilar_archivos(ruta_actual, recursos)
                
                print("Archivos encontrados en el proyecto:")
                #for archivo in archivos:
                    #print(archivo)

                if archivos_no_utilizados:
                    print("\nWarnings:")
                    for archivo_no_utilizado in archivos_no_utilizados:
                        print(f"Warning: El archivo '{archivo_no_utilizado}' no está siendo declarado en el paquete SCORM.")
                        
                print("\nEl proyecto SCORM está listo para ser subido al LMS.")
