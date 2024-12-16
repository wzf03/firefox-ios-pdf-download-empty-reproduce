from flask import Flask, send_from_directory, request, make_response, render_template_string
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configuration
UPLOAD_FOLDER = 'downloads'  # Create this folder in your project directory
VALID_CREDENTIALS = {
    'admin': 'password123'  # Replace with secure credentials
}

# Create downloads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        input { width: 100%; padding: 8px; margin-top: 5px; }
        button { padding: 10px 15px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        .error { color: red; margin-bottom: 15px; }
    </style>
</head>
<body>
    <h2>Login</h2>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
    <form method="POST" action="/login">
        <div class="form-group">
            <label>Username:</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Password:</label>
            <input type="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
</body>
</html>
'''

FILES_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Available Files</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
        .file-list { margin-top: 20px; }
        .file-item { padding: 10px; border-bottom: 1px solid #eee; }
        .file-item a { text-decoration: none; color: #007bff; }
        .logout { float: right; }
    </style>
</head>
<body>
    <h2>Available Files</h2>
    <a href="/logout" class="logout">Logout</a>
    <div class="file-list">
        {% for file in files %}
        <div class="file-item">
            <a href="/download/{{ file }}">{{ file }}</a>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_cookie = request.cookies.get('auth_token')
        if not auth_cookie or auth_cookie != 'authenticated':
            return make_response(render_template_string(LOGIN_TEMPLATE))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(FILES_TEMPLATE, files=files)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            response = make_response('Redirecting...')
            response.set_cookie('auth_token', 'authenticated')
            response.headers['Location'] = '/'
            response.status_code = 302
            return response
        
        return render_template_string(LOGIN_TEMPLATE, error='Invalid credentials')
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    response = make_response('Redirecting...')
    response.delete_cookie('auth_token')
    response.headers['Location'] = '/login'
    response.status_code = 302
    return response

@app.route('/download/<filename>')
@requires_auth
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7788)
