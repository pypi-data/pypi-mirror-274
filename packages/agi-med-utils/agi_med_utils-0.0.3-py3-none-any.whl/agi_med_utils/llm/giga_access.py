from base64 import b64encode
from gigachat import GigaChat


class GigaChatEntryPoint:
    def __init__(self, config):
        client_id = config['gigachat_creds']['client_id']
        client_secret = config['gigachat_creds']['client_secret']
        creds = b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
        self.model = GigaChat(
            credentials=creds,
            scope='GIGACHAT_API_CORP',
            verify_ssl_certs=False,
            model='GigaChat-Pro',
            profanity_check=False,
        )
        self.long_model = GigaChat(
            credentials=creds,
            scope='GIGACHAT_API_CORP',
            verify_ssl_certs=False,
            model='GigaChat-Plus',
            profanity_check=False,
        )
        self.DIM = 1024
        self.ZEROS = [0 for _ in range(self.DIM)]
        self.ERROR_MESSAGE = 'Простите, я Вас не понял. Повторите, пожалуйста, поподробнее и другими словами'

    def get_response(self, total_input: str) -> str:
        try:
            return self.model.chat(total_input).choices[0].message.content
        except:
            return self.ERROR_MESSAGE

    def get_embeddings(self, total_input: str, input_is_long=False) -> list:
        this_model = self.long_model if input_is_long else self.model
        try:
            return this_model.embeddings(total_input).data[0].embedding
        except:
            return self.ZEROS
