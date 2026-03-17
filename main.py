from http.server import HTTPServer
from controller.base_handler import BaseHandler


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), BaseHandler)
    print("Сервер запущен на http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
