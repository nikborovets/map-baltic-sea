from flask import Flask, send_from_directory, request, make_response
import os
import time
from datetime import timedelta

app = Flask(__name__)

# Конфигурация для production
app.config['PREFERRED_URL_SCHEME'] = 'https'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 год в секундах

# Словарь для кэширования HTML-страницы
html_cache = {'content': None, 'timestamp': 0}

# Основная HTML-страница с картой
@app.route('/')
def serve_map():
    # Простое кэширование HTML страницы на сервере (обновляется каждые 12 часов)
    now = time.time()
    if html_cache['content'] is None or now - html_cache['timestamp'] > 43200:
        file_path = os.path.join(os.path.dirname(__file__), 'baltic_sea_map_with_colorbar.html')
        with open(file_path, 'rb') as f:
            html_cache['content'] = f.read()
            html_cache['timestamp'] = now
            
    response = make_response(html_cache['content'])
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    
    # Добавляем заголовки кэширования для браузера
    response.headers['Cache-Control'] = 'public, max-age=3600'  # 1 час
    return response

# Сервис статичных файлов для карты стандартного отклонения
@app.route('/processed_graphs/<path:filename>')
def serve_static_files(filename):
    directory = os.path.join(os.path.dirname(__file__), 'processed_graphs')
    response = send_from_directory(directory, filename)
    
    # Добавляем кэширование для картинок на 7 дней
    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        response.headers['Cache-Control'] = 'public, max-age=604800'
        
    return response

# Добавляем обработку ошибок
@app.errorhandler(404)
def not_found(error):
    return "Файл не найден", 404

@app.errorhandler(500)
def server_error(error):
    return "Внутренняя ошибка сервера", 500

# Информация о здоровье сервиса
@app.route('/health')
def health():
    return "OK", 200

# Запуск сервера только при прямом запуске файла
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8883)
