import pytest
from journeylib.funciones import ins_historico
from fastapi.responses import JSONResponse
import json
    
def test_ins_historico_usr_vacio():
    usr = ''
    num_chat = 1
    contexto = 'contexto'
    lista_msg = [{"role": "user", "content": "Hola, ¿cómo estás?"},
                 {"role": "assistant", "content": "Hola, soy ia."}]
    tipoIA = 'PASADO'
    cerrado = True
    url='http://ismi.fi.upm.es:8080/insertar/chat'

    status_code = ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado, url)
    assert status_code != 200

def test_ins_historico_lista_msg_vacia():
    usr = 'usuario'
    num_chat = 1
    contexto = 'contexto'
    lista_msg = []
    tipoIA = 'PASADO'
    cerrado = True
    url='http://ismi.fi.upm.es:8080/insertar/chat'

    status_code = ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado, url)
    assert status_code != 200

def test_ins_historico_tipoIA_invalido():
    usr = 'usuario'
    num_chat = 1
    contexto = 'contexto'
    lista_msg = []
    tipoIA = 'PASADO'
    cerrado = True
    url='http://ismi.fi.upm.es:8080/insertar/chat'

    tipos_validos = ['PASADO', 'PRESENTE', 'FUTURO', 'COMPRA']
    if tipoIA not in tipos_validos:
        raise ValueError("El valor de tipoIA debe ser uno de {tipos_validos}")
    
    with pytest.raises(ValueError):
        ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado, url)

def test_ins_historico_url_invalido():
    usr = 'usuario'
    num_chat = 1
    contexto = 'contexto'
    lista_msg = []
    tipoIA = 'PASADO'
    cerrado = True
    url='aaa'

    url_valida = ['http://ismi.fi.upm.es:8080/insertar/chat']
    if url not in url_valida:
        raise ValueError("Url invalida")
    
    with pytest.raises(ValueError):
        ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado, url)
 
"""
def test_ins_historico():
    usr = 'usuario'
    num_chat = 1
    contexto = 'contexto'
    lista_msg = [{"role": "user", "content": "Hola, ¿cómo estás?"},
                 {"role": "assistant", "content": "Hola, soy ia."}]
    tipoIA = 'PASADO'
    cerrado = True
    datos=[usr, num_chat, contexto, lista_msg, tipoIA, cerrado]

    response = ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado)
    assert response.status_code == 200

    expected_data = {
        'id_usuario': usr,
        'num_chat': num_chat,
        'contexto': contexto,
        'lista_msg': lista_msg,
        'tipoIA': tipoIA,
        'cerrado': cerrado
    }
    # Convierte la respuesta JSON a un diccionario para comparar fácilmente
    response_data = json.loads(response.content)
    assert response_data == expected_data
"""