import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
clave = os.getenv("GROQ_API_KEY")

tb_clientes = pd.read_csv("data/clientes.csv", sep=";")
tb_stock = pd.read_csv("data/stock.csv", sep=";")
tb_pedidos = pd.read_csv("data/pedidos.csv", sep=";")

while True:
    print("----- CONSULTAS AUTOMATICAS -----")
    print("1. Ingresar una consulta")
    print("2. Salir del sistema.")
    
    try:
        option = int(input("Ingrese una opcion: "))            
    except ValueError:
        print("[X] Error - Por favor ingresá un número (1 o 2).")
        continue
    
    if option == 1:
        consult_ing = input("Ingrese su consulta: ")
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
                print("\n===============================")
                print("ASISTENTE TECH-SED:")
                print(datos["choices"][0]["message"]["content"])
                print("===============================\n")
            else:
                print("[X] ERROR DE CONEXION", datos)
                
        except Exception as e:
            print("[X] Error al conectar con la API:", e)
        
    elif option == 2:
        print("[OK] Saliendo del sistema...")
        break
    else:
        print("[X] Error - Opcion incorrecta.")
