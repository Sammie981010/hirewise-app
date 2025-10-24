from flask import Flask, render_template_string, request, jsonify, session
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'hirewise_secret_key_2024'

# Data files
DATA_FILES = {
    'users': 'hirewise_users.json',
    'jobs': 'hirewise_jobs.json', 
    'professionals': 'hirewise_professionals.json',
    'quotes': 'hirewise_quotes.json',
    'messages': 'hirewise_messages.json'
}

def load_data(file_key):
    try:
        with open(DATA_FILES[file_key], 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(file_key, data):
    with open(DATA_FILES[file_key], 'w') as f:
        json.dump(data, f)

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>HireWise - Professional Service Platform</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f8f9fa; }
        .navbar { background: #2c3e50; color: white; padding: 1rem 0; }
        .nav-container { max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }
        .logo { font-size: 1.5rem; font-weight: bold; }
        .nav-links { display: flex; gap: 20px; }
        .nav-links a { color: white; text-decoration: none; padding: 8px 16px; border-radius: 4px; }
        .nav-links a:hover { background: #34495e; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .hero { background: linear-gradient(135deg, #3498db, #2c3e50); color: white; padding: 60px 20px; text-align: center; border-radius: 10px; margin-bottom: 40px; }
        .hero h1 { font-size: 3rem; margin-bottom: 20px; }
        .btn { display: inline-block; padding: 12px 24px; background: #27ae60; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; border: none; cursor: pointer; margin: 5px; }
        .btn:hover { background: #219a52; }
        .btn-secondary { background: #e74c3c; }
        .btn-secondary:hover { background: #c0392b; }
        .section { background: white; margin: 20px 0; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .card { background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db; }
        .stats { display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap; gap: 20px; }
        .stat { background: #3498db; color: white; padding: 20px; border-radius: 8px; min-width: 120px; }
        .form-group { margin: 15px 0; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
        .form-group input, .form-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .hidden { display: none; }
        .active { display: block; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">🔧 HireWise</div>
            <div class="nav-links">
                <a href="#" onclick="showSection('home')">Home</a>
                <a href="#" onclick="showSection('professionals')">Find Professionals</a>
                <a href="#" onclick="showSection('post-job')">Post Job</a>
                <a href="#" onclick="showSection('login')">Login</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div id="home" class="section active">
            <div class="hero">
                <h1>🔧 HireWise Platform</h1>
                <p>Professional Service Marketplace - Connect, Hire, Get Work Done</p>
                <button class="btn" onclick="showSection('professionals')">Find Professionals</button>
                <button class="btn btn-secondary" onclick="showSection('post-job')">Post a Job</button>
            </div>
            
            <div class="stats">
                <div class="stat"><h3>500+</h3><p>Professionals</p></div>
                <div class="stat"><h3>1,200+</h3><p>Jobs Completed</p></div>
                <div class="stat"><h3>4.8⭐</h3><p>Average Rating</p></div>
                <div class="stat"><h3>24/7</h3><p>Support</p></div>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h3>🔍 Smart Matching</h3>
                    <p>AI-powered system connects you with the best professionals.</p>
                </div>
                <div class="card">
                    <h3>📍 GPS Location</h3>
                    <p>Real-time location tracking with building-level precision.</p>
                </div>
                <div class="card">
                    <h3>💳 Secure Payments</h3>
                    <p>Integrated M-Pesa payments with wallet functionality.</p>
                </div>
                <div class="card">
                    <h3>⭐ Mutual Ratings</h3>
                    <p>AI-assisted feedback system for quality assurance.</p>
                </div>
            </div>
        </div>

        <div id="professionals" class="section hidden">
            <h2>Find Professionals</h2>
            <div id="professionals-list"></div>
        </div>

        <div id="post-job" class="section hidden">
            <h2>Post a Job</h2>
            <form onsubmit="postJob(event)">
                <div class="form-group">
                    <label>Service Type:</label>
                    <select name="service" required>
                        <option value="">Select Service</option>
                        <option value="plumber">Plumber</option>
                        <option value="cleaner">Cleaner</option>
                        <option value="electrician">Electrician</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Description:</label>
                    <input type="text" name="description" required>
                </div>
                <div class="form-group">
                    <label>Budget (KSH):</label>
                    <select name="budget" required>
                        <option value="50-100">50-100</option>
                        <option value="100-300">100-300</option>
                        <option value="300+">300+</option>
                    </select>
                </div>
                <button type="submit" class="btn">Post Job</button>
            </form>
        </div>

        <div id="login" class="section hidden">
            <h2>Login / Sign Up</h2>
            <form onsubmit="loginUser(event)">
                <div class="form-group">
                    <label>Name:</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" name="email" required>
                </div>
                <div class="form-group">
                    <label>Contact:</label>
                    <input type="tel" name="contact" required>
                </div>
                <div class="form-group">
                    <label>Account Type:</label>
                    <select name="type" required>
                        <option value="client">Client</option>
                        <option value="professional">Professional</option>
                    </select>
                </div>
                <button type="submit" class="btn">Login / Sign Up</button>
            </form>
        </div>
    </div>

    <script>
        function showSection(sectionId) {
            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
            document.getElementById(sectionId).classList.remove('hidden');
            
            if (sectionId === 'professionals') {
                loadProfessionals();
            }
        }

        function loadProfessionals() {
            fetch('/api/professionals')
                .then(response => response.json())
                .then(data => {
                    const html = data.map(pro => `
                        <div class="card">
                            <h3>${pro.name} ${pro.certified ? '✓' : ''}</h3>
                            <p><strong>Service:</strong> ${pro.service}</p>
                            <p><strong>Rating:</strong> ${pro.rating}⭐</p>
                            <p><strong>Price:</strong> KSH ${pro.price}</p>
                            <button class="btn" onclick="hireProfessional('${pro.name}')">Hire Now</button>
                        </div>
                    `).join('');
                    document.getElementById('professionals-list').innerHTML = html;
                });
        }

        function postJob(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const jobData = Object.fromEntries(formData);
            
            fetch('/api/jobs', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(jobData)
            })
            .then(response => response.json())
            .then(data => {
                alert('Job posted successfully!');
                event.target.reset();
            });
        }

        function loginUser(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const userData = Object.fromEntries(formData);
            
            fetch('/api/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(userData)
            })
            .then(response => response.json())
            .then(data => {
                alert('Login successful!');
                showSection('home');
            });
        }

        function hireProfessional(name) {
            alert(`Hire request sent to ${name}!`);
        }
    </script>
</body>
</html>
    ''')

@app.route('/api/professionals')
def get_professionals():
    professionals = load_data('professionals')
    return jsonify([
        {
            'name': pro['name'],
            'service': pro['service'],
            'rating': pro['rating'],
            'price': pro['price'],
            'certified': pro.get('certified', False)
        }
        for pro in professionals.values()
    ])

@app.route('/api/jobs', methods=['POST'])
def create_job():
    job_data = request.json
    jobs = load_data('jobs')
    
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {
        'id': job_id,
        'service': job_data['service'],
        'description': job_data['description'],
        'budget': job_data['budget'],
        'status': 'Open',
        'created': datetime.now().isoformat()
    }
    
    save_data('jobs', jobs)
    return jsonify({'success': True, 'job_id': job_id})

@app.route('/api/login', methods=['POST'])
def login():
    user_data = request.json
    users = load_data('users')
    
    user_id = user_data['email']
    users[user_id] = {
        'name': user_data['name'],
        'email': user_data['email'],
        'contact': user_data['contact'],
        'type': user_data['type'],
        'created': datetime.now().isoformat()
    }
    
    save_data('users', users)
    session['user'] = user_data
    return jsonify({'success': True})

if __name__ == '__main__':
    # Initialize data files
    for file_path in DATA_FILES.values():
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f)
    
    # Add sample data
    if os.path.getsize(DATA_FILES['professionals']) == 0:
        sample_pros = {
            "pro1": {"name": "John Plumber", "service": "Plumber", "rating": 4.8, "price": "50-100", "certified": True},
            "pro2": {"name": "Mary Cleaner", "service": "Cleaner", "rating": 4.9, "price": "30-60", "certified": True},
            "pro3": {"name": "Mike Electrician", "service": "Electrician", "rating": 4.7, "price": "100-300", "certified": False}
        }
        save_data('professionals', sample_pros)
    
    app.run(host='0.0.0.0', port=5000, debug=True)