from http.server import HTTPServer
from controller.base_handler import BaseHandler
from config import Config
from container import Container
from router import Router
import sys
import controller.base_handler as base_handler_module

if __name__ == "__main__":
    Config.setup_logging()
    logger = Config.get_logger(__name__)

    container = Container()
    router = Router(container)
    base_handler_module.router = router

    container.service.load_unfinished_matches()
    server = HTTPServer((Config.HOST, Config.PORT), BaseHandler)
    logger.info(f"Сервер запущен на http://{Config.HOST}:{Config.PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        container.service.save_active_matches()
        logger.info("Сервер остановлен пользователем.")
        server.shutdown()
    except Exception as e:
        logger.exception(f"Ошибка сервера: {e}")
        sys.exit(1)
