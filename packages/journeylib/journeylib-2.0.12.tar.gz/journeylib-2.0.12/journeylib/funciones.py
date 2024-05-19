#Imports necesarios para las funciones de la libreria
import requests

#Metodo de prueba para el despliege de la libreria
def hola_journey():
    print('Holitaa, esta es una librería diseñada y publicada por JourneyGen para el proyecto GPTravel.')

"""
Endpoint para insertar:
http://ismi.fi.upm.es:8080/insertar/chat
body{

}
response{

}

Endpoint para recibir:
servidor/read/chats
body{
    username: (nombre de usuario),
    chat: (int, numero de chat),
    tipoIA: (enum, PASADO PRESENTE FUTURO COMPRA)
}
response{
    mensajes: [
        {
            fecha: (formato SQL),
            input: (content del usuario),
            output: (content de la ia)
        }
    ]
}
"""

#Implementacion de las funciones necesarias para la libreria
"""
METODO INSERTAR HISTORICO
Descripcion: Inserta un nuevo par de mensajes a la bd de CASH
"""
def ins_historico(usr, tipoIA, num_chat, lista_msg, contexto, cerrado=False, url='http://195.35.1.47:8080/insertar/chat'):
    """
    PRE:
        usr es un nombre de usuario valido
        tipoIA es un string de entre la lista ['PASADO', 'PRESENTE', 'FUTURO', 'COMPRA']
        num_chat es un int coherente con una de las siguientes descripciones:
            1. identificador de chat existente
            2. None (en este caso crearía un chat nuevo)
        lista_msg es una lista de diccionarios formato {'role':'', 'content':''}
        contexto es un string con el contexto que use la ia que esté teniendo la conversación
    POST:
        inserta un nuevo mensaje en la BD de CASH
    DEVUELVE:
        (int): valor identificativo asociado al chat sobre el que se insertan los mensajes
    """
    try:
        datos_post = { # Formato con el que se consume la api
            'usr': usr,
            'num_chat': num_chat,
            'contexto': contexto,
            'lista_msg': lista_msg,
            'tipoIA': tipoIA,
            'cerrado': cerrado
        }
        response = requests.post(url, json=datos_post)

        if response.status_code == 200:
            n_chat = response.json()['num_chat'] # Obtenemos el numero de chat devuelto al hacer la solicitud
            return n_chat
        else:
            raise ValueError(f"ins_historico, codigo de respuesta {response.status_code}, detail: {response.text}") # Codigo de respuesta distinto de 200 (no exitoso)
    except Exception as e: # Excepcion ocurrida al hacer la peticion
        raise e

def get_historico(usr, tipoIA, num_chat, url='http://195.35.1.47:8080/read/chats'):
    """
    PRE:
        usr es un nombre de usuario valido
        tipoIA es un string de entre la lista ['PASADO', 'PRESENTE', 'FUTURO', 'COMPRA']
        num_chat es un int correspondiente a un identificador de chat existente
    DEVUELVE:
        una lista de diccionarios (json) con el siguiente formato:
        {'role':'', 'content':''}
        El primer mensaje será con role='system' y content='contexto de la ia'
        El resto de los mensajes serán pares que alternarán entre mensajes del usuario y la ia
    """
    msgs = [] # Lista donde se guardaran todos los mensajes que se pasaran a la IA por el create
    
    try:
        datos_post = { # Formato con el que se consume la api
            'username': usr,
            'chat': num_chat,
            'tipoIA': tipoIA
        }
        
        response = requests.post(url, json=datos_post)

        if response.status_code == 200:
            """
             Obtenemos cuerpo, lista de dict tq: {
                'fecha': mensaje.fecha.strftime("%Y-%m-%d %H:%M"),
                'input': mensaje.input,
                'output': mensaje.output,
                'cerrado': mensaje.cerrado,
                'contexto': mensaje.contextoia
            }
            """
            data = response.json()
            
            msg_contexto = {'role': 'system', 'content': data[0]['contexto']}
            msgs.append(msg_contexto)
            for msg in data:
                msg_usuario = {'role': 'user', 'content': msg['input']}
                msg_ia = {'role': 'assistant', 'content': msg['output']}
                msgs.append(msg_usuario)
                msgs.append(msg_ia)
            
            return msgs

        else:
            raise ValueError(f"ins_historico, codigo de respuesta {response.status_code}") # Codigo de respuesta distinto de 200 (no exitoso)
    except Exception as e: # Excepcion ocurrida al hacer la peticion
        raise e

def get_historico_falso(usr, url='http://farlier.org:8080/chat/obtener'):

    datos_post = {
        'usr': usr
    }
    response = requests.post(url, json=datos_post)

    return {'respuesta': response.text, 'codigo': response.status_code}

def ins_historico_falso(usr, msgs, url='http://farlier.org:8080/chat/insertar'):

    datos_post = {
        'usr': usr,
        'msgs': msgs
    }
    response = requests.post(url, json=datos_post)

    return {'respuesta': response.text, 'codigo': response.status_code}