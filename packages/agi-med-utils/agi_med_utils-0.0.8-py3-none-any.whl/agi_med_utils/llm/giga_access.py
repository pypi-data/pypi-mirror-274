from base64 import b64encode
from gigachat import GigaChat


class GigaChatEntryPoint:
    def __init__(self, client_id, client_secret):
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
        self.warmup()

    def get_response(self, total_input: str, input_is_long=False) -> str:
        this_model = self.long_model if input_is_long else self.model
        try:
            return this_model.chat(total_input).choices[0].message.content
        except:
            return self.ERROR_MESSAGE

    def get_embeddings(self, total_input: str, input_is_long=False) -> list:
        this_model = self.long_model if input_is_long else self.model
        try:
            return this_model.embeddings(total_input).data[0].embedding
        except:
            return self.ZEROS

    def warmup(self) -> None:
        assert self.get_response('Прогрев') != self.ERROR_MESSAGE, 'Нет доступа к ллм!'
        assert self.get_response('Прогрев', input_is_long=True) != self.ERROR_MESSAGE, 'Нет доступа к ллм!'
        assert self.get_embeddings('Прогрев') != self.ZEROS, 'Нет доступа к ллм!'
        assert self.get_embeddings('Прогрев', input_is_long=True) != self.ZEROS, 'Нет доступа к ллм!'
        