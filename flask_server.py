from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Основная HTML-страница с картой
@app.route('/')
def serve_map():
    return send_from_directory(os.path.dirname(__file__), 'baltic_sea_map_with_colorbar.html')

# Сервис статичных файлов для карты стандартного отклонения
@app.route('/processed_graphs/<path:filename>')
def serve_static_files(filename):
    directory = os.path.join(os.path.dirname(__file__), 'processed_graphs')
    return send_from_directory(directory, filename)

# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8883)
