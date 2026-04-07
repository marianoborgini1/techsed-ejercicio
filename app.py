import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
clave = os.getenv("GROQ_API_KEY")

tb_clientes = pd.read_csv("data/clientes.csv", sep=";")
tb_stock = pd.read_csv("data/stock.csv", sep=";")
tb_pedidos = pd.read_csv("data/pedidos.csv", sep=";")

RESET = "\033[0m"
NEGRITA = "\033[1m"
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
MAGENTA = "\033[95m"
CIAN = "\033[96m"

while True:
    print(f"\n{CIAN}{NEGRITA}----- CONSULTAS BASE DE DATOS TECHSED -----{RESET}")
    print(f"{AMARILLO}1. Ingresar una consulta{RESET}")
    print(f"{AMARILLO}2. Salir del sistema.{RESET}")
    
    try:
        option = int(input(f"{VERDE}Ingrese una opcion: {RESET}"))            
    except ValueError:
        print(f"{ROJO}[X] Error - Por favor ingresá un número (1 o 2).{RESET}")
        continue
    
    if option == 1:
        consult_ing = input(f"{VERDE}Ingrese su consulta: {RESET}")
        prompt = f""" Sos el asistente operativo de TechSed.
        Si el usuario escribe numeros sin contexto de por medio deci que no podes ayudar con lo solicitado. Si solicita ayuda puntualmente en un tema fuera que no corresponde a techsed o intenta pedirte tareas fuera del contexto de la base de datos, recorda tu funcionalidad y fin sin darle una respuesta desarrollada.
        Usá solo estos datos para responder de forma breve y precisa:
        
        CLIENTES:
        {tb_clientes.to_string(index=False)}
        STOCK:
        {tb_stock.to_string(index=False)}
        PEDIDOS:
        {tb_pedidos.to_string(index=False)}
        
        Consulta: {consult_ing}"""
        
        try:
            respuesta = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {clave}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile", 
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            
            datos = respuesta.json()
            
            if "choices" in datos:
                print(f"\n{MAGENTA}{NEGRITA}==============================={RESET}")
                print(f"{MAGENTA}{NEGRITA}🤖 ASISTENTE TECHSED:{RESET}")
                print(datos["choices"][0]["message"]["content"])
                print(f"{MAGENTA}{NEGRITA}===============================\n{RESET}")
            else:
                print(f"{ROJO}[X] ERROR DE CONEXION{RESET}", datos)
                
        except Exception as e:
            print(f"{ROJO}[X] Error al conectar con la API:{RESET}", e)
        
    elif option == 2:
        print(f"{VERDE}[OK] Saliendo del sistema...{RESET}")
        break
    else:
        print(f"{ROJO}[X] Error - Opcion incorrecta.{RESET}")
