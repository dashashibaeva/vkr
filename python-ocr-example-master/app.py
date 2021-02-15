import os

from flask import Flask, render_template, request

from ocr_core import ocr_core

UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # Проверка загрузки пользователем файла
        if 'file' not in request.files:
            return render_template('upload.html', msg='Ошибка! Вы не выбрали файл!')
        file = request.files['file']
        # Если пользователь не выбрал файл, браузер сообщит об этом
        if file.filename == '':
            return render_template('upload.html', msg='Ошибка! Вы не выбрали файл!')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            # Вызов функции распознавания символов
            extracted_text = ocr_core(file)

            # Извлечение текста (математических символов
            # и чисел) на фото  отображение
            return render_template('upload.html',
                                   msg='Распознавание выполнено успешно.',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()
