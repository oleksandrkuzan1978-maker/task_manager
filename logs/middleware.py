import logging
logger = logging.getLogger('http')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
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