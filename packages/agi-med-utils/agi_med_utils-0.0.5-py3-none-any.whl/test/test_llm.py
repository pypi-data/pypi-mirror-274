import os, sys
from agi_med_utils.config.config import ConfigSingleton
from agi_med_utils.llm.yandex_access import YandexGPTEntryPoint
from agi_med_utils.llm.giga_access import GigaChatEntryPoint

config = ConfigSingleton('/config', '/config').get()

def test_config():
    assert isinstance(config, dict)

def test_giga():
    giga = GigaChatEntryPoint(
        client_id=config['gigachat_creds']['client_id'],
        client_secret=config['gigachat_creds']['client_secret']
        )    
    out = giga.get_response('Привет!')
    assert isinstance(out, str)
    assert len(out)
    
def test_ya_gpt():
    ya_gpt = YandexGPTEntryPoint(
    token=config['yandex_creds']['token'], 
    folder_id=config['yandex_creds']['folder_id']
    )
    out = ya_gpt.get_response('Привет!')
    assert isinstance(out, str)
    assert len(out)