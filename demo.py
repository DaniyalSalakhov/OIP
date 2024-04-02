from flask import Flask, render_template, request
from task5 import Search_system
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_value = request.form['input_value']
        search = Search_system()
        links = search.search(input_value)[:10]
        return render_template('output.html', input_value=input_value, result=links)
    else:
        return '''<html>
                    <head>
                        <title>Пример страницы ввода</title>
                    </head>
                    <body>
                        <h1>Введите ваш запрос:</h1>
                        <form action="/" method="POST">
                            <input type="text" name="input_value">
                            <br><br>
                            <input type="submit" value="Отправить">
                        </form>
                    </body>
                </html>'''


if __name__ == '__main__':
    app.run()
