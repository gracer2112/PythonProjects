from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/pi')
def pi():
    return redirect("http://127.0.0.1:5001")  # Ajuste a URL e porta conforme necessário

@app.route('/pt')
def pt():
    return redirect("http://127.0.0.1:5002")  # Ajuste a URL e porta conforme necessário

@app.route('/sr')
def sr():
    return redirect("http://127.0.0.1:5003")  # Ajuste a URL e porta conforme necessário

if __name__ == '__main__':
    app.run(debug=True, port=5000)