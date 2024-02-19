from flask import Flask, request, render_template
import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    url_result = ''
    text_result = ''
    result = ''
    if request.method == 'POST':
        url_result = request.form.get('enterlocation1')
        text_result = request.form.get('enterlocation2')
        if url_result !='' :
            result = main.set(url_result,1)
            text_result = ''
        elif text_result != '' :
            result = main.set(text_result,0)
            url_result = ''
    return render_template('index1.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
