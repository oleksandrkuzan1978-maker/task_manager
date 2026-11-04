import logging
logger = logging.getLogger('http')

class RequestLoggingMiddleware:
    """ Middleware для логирования HTTP-запросов и статусов ответов.

       Перехватывает входящие HTTP-запросы, передаёт их на дальнейшую
       обработку и записывает в лог HTTP-метод, путь запроса
       и статус полученного ответа.

       Логи записываются с уровнем INFO через логгер 'http'.
       """
    def __init__(self, get_response):
        """ Инициализирует middleware.
                Args:
                    get_response: Следующий middleware или обработчик Django,
                        которому передаётся HTTP-запрос.
                """
        self.get_response = get_response

    def __call__(self, request):
        """Обрабатывает HTTP-запрос и логирует полученный ответ.
               Args:
                   request: Объект HTTP-запроса Django.
               Returns:
                   HttpResponse: Ответ, сформированный Django после обработки
                       запроса."""
        response = self.get_response(request)

        logger.info('%s %s %s',
                    request.method,
                    request.path,
                    response.status_code)
        return response

# Что здесь происходит?
# 1. Django передаёт HTTP-запрос в middleware.
# 2. self.get_response(request) передаёт запрос дальше, на обработку.
# 3. Когда Django получает ответ, мы извлекаем его статус.
# 4. logger.info() записывает HTTP-метод, путь и статус ответа.
# 5. return response возвращает ответ пользователю.