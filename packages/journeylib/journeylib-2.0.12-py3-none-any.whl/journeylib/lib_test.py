import pytest
import logging
import journeylib as jl

# res = jl.ins_historico('Nelson', 'PRESENTE', 1, lista_msga, 'holita', url='http://localhost:5000/insertar/chat')
# res = jl.get_historico('Nelson', 'PRESENTE', 1, url='http://localhost:5000/read/chats')

def test_get_historico_exitoso():
    res = jl.get_historico('Nelson', 'PRESENTE', 1, url='http://localhost:5000/read/chats')
    assert res[0]['role'] == 'system'
    assert res[1]['role'] == 'user'
    assert res[2]['role'] == 'assistant'
    print('\n\ntest_get_historico_exitoso, lista de mensajes devueltos:')
    for msg in res:
        print(msg)

def test_ins_historico_exitoso():
    lista_msgs = [ {'role': 'user', 'content': 'Por favor funciona'}, {'role': 'assistant', 'content': 'Ok ahora quiero funcionar'}]
    res = jl.ins_historico('Nelson', 'PRESENTE', 1, lista_msgs, 'holita', url='http://localhost:5000/insertar/chat')
    assert type(res) is int
    assert res == 1
