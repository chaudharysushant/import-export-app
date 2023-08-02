from flask import Flask, render_template, request, redirect, url_for, send_file, session
import csv
import bcrypt

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

sample_user = {
    'username': 'USERNAME',
    'password': bcrypt.hashpw(b'PASSWORD', bcrypt.gensalt())
}

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        
        if username == sample_user['username']:
            return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']

    if username == sample_user['username'] and bcrypt.checkpw(password.encode('utf-8'), sample_user['password']):
        session['authenticated'] = True
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        return redirect(url_for('registration_success'))

    return render_template('register.html')

# Data Import/Export
data = [{'column1': 'Value1', 'column2': 'Value2'},
        {'column1': 'Value3', 'column2': 'Value4'}]

@app.route('/data')
def index():
    if session.get('authenticated'):
        return render_template('data_import_export.html', data=data)
    else:
        return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            
            pass
    return render_template('data_import_export.html', data=data)

@app.route('/export', methods=['POST'])
def export():
    if session.get('authenticated'):
        
        output_filename = 'exported_data.csv'

        with open(output_filename, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            for row in data:
                csv_writer.writerow([row['column1'], row['column2']])

        return send_file(output_filename, as_attachment=True)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
