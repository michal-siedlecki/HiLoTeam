import subprocess

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/run_script', methods=['POST'])
def run_script():
    if request.method == 'POST':
        try:
            # Uruchamianie skryptu pythona ssh_generator.py
            subprocess.run(['python', 'ssh_generator.py'], check=True)
            with open('keys/ssh_id.pub') as public_key:
                public_key = public_key.read()
            return render_template('keys_success.html', public_key=public_key)
        except subprocess.CalledProcessError as e:
            return f'Błąd podczas generowania kluczy: {e}'
    return 'Naciśnij przycisk, aby uruchomić skrypt.'


if __name__ == '__main__':
    app.run()
