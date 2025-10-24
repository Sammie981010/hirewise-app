import http.server
import socketserver
import threading
import webbrowser
import json
import os
from datetime import datetime, timedelta
import uuid

class HireWiseShareServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.share_links = {}
        
    def create_share_link(self, data_type="demo", expires_hours=24):
        """Create temporary shareable link"""
        link_id = str(uuid.uuid4())[:8]
        expires = datetime.now() + timedelta(hours=expires_hours)
        
        self.share_links[link_id] = {
            "id": link_id,
            "type": data_type,
            "created": datetime.now().isoformat(),
            "expires": expires.isoformat(),
            "active": True
        }
        
        return f"http://localhost:{self.port}/share/{link_id}"
    
    def start_server(self):
        """Start the sharing server"""
        try:
            # Try different ports if default is busy
            for port in range(self.port, self.port + 10):
                try:
                    handler = self.create_handler()
                    self.server = socketserver.TCPServer(("", port), handler)
                    self.port = port
                    
                    # Start server in background thread
                    server_thread = threading.Thread(target=self.server.serve_forever)
                    server_thread.daemon = True
                    server_thread.start()
                    
                    print(f"Sharing server started on port {port}")
                    return True
                except OSError:
                    continue
            
            print("No available ports found")
            return False
        except Exception as e:
            print(f"Error starting server: {e}")
            return False
    
    def create_handler(self):
        share_links = self.share_links
        
        class ShareHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path.startswith('/share/'):
                    link_id = self.path.split('/')[-1]
                    if link_id in share_links:
                        link_data = share_links[link_id]
                        if datetime.now() < datetime.fromisoformat(link_data['expires']):
                            self.send_demo_page(link_id)
                        else:
                            self.send_expired_page()
                    else:
                        self.send_not_found()
                else:
                    self.send_main_page()
            
            def send_demo_page(self, link_id):
                html = f'''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>HireWise - Professional Service Platform</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f8f9fa; }}
                        .navbar {{ background: #2c3e50; color: white; padding: 1rem 0; position: sticky; top: 0; z-index: 100; }}
                        .nav-container {{ max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }}
                        .logo {{ font-size: 1.5rem; font-weight: bold; }}
                        .nav-links {{ display: flex; gap: 20px; }}
                        .nav-links a {{ color: white; text-decoration: none; padding: 8px 16px; border-radius: 4px; transition: background 0.3s; }}
                        .nav-links a:hover {{ background: #34495e; }}
                        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
                        .hero {{ background: linear-gradient(135deg, #3498db, #2c3e50); color: white; padding: 60px 20px; text-align: center; margin-bottom: 40px; border-radius: 10px; }}
                        .hero h1 {{ font-size: 3rem; margin-bottom: 20px; }}
                        .hero p {{ font-size: 1.2rem; margin-bottom: 30px; }}
                        .btn {{ display: inline-block; padding: 12px 24px; background: #27ae60; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; transition: background 0.3s; border: none; cursor: pointer; }}
                        .btn:hover {{ background: #219a52; }}
                        .btn-secondary {{ background: #e74c3c; }}
                        .btn-secondary:hover {{ background: #c0392b; }}
                        .section {{ background: white; margin: 20px 0; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }}
                        .card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db; }}
                        .stats {{ display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap; gap: 20px; }}
                        .stat {{ background: #3498db; color: white; padding: 20px; border-radius: 8px; min-width: 120px; }}
                        .form-group {{ margin: 15px 0; }}
                        .form-group label {{ display: block; margin-bottom: 5px; font-weight: bold; }}
                        .form-group input, .form-group select, .form-group textarea {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }}
                        .professionals-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
                        .professional-card {{ background: white; border: 1px solid #ddd; border-radius: 8px; padding: 20px; text-align: center; transition: transform 0.3s; }}
                        .professional-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                        .rating {{ color: #f39c12; font-weight: bold; }}
                        .badge {{ background: #27ae60; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; }}
                        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }}
                        .modal-content {{ background: white; margin: 5% auto; padding: 30px; border-radius: 10px; max-width: 500px; position: relative; }}
                        .close {{ position: absolute; top: 15px; right: 20px; font-size: 24px; cursor: pointer; }}
                        .hidden {{ display: none; }}
                        .active {{ display: block; }}
                        @media (max-width: 768px) {{
                            .hero h1 {{ font-size: 2rem; }}
                            .nav-links {{ display: none; }}
                            .stats {{ flex-direction: column; align-items: center; }}
                        }}
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
                        <!-- Home Section -->
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
                                    <p>AI-powered system connects you with the best professionals based on location, skills, and ratings.</p>
                                </div>
                                <div class="card">
                                    <h3>📍 GPS Location</h3>
                                    <p>Real-time location tracking with building-level precision for accurate service delivery.</p>
                                </div>
                                <div class="card">
                                    <h3>💳 Secure Payments</h3>
                                    <p>Integrated M-Pesa payments with wallet functionality and secure transactions.</p>
                                </div>
                                <div class="card">
                                    <h3>⭐ Mutual Ratings</h3>
                                    <p>AI-assisted feedback system where both parties rate each other for quality assurance.</p>
                                </div>
                            </div>
                        </div>

                        <!-- Professionals Section -->
                        <div id="professionals" class="section hidden">
                            <h2>Find Professionals</h2>
                            <div class="form-group">
                                <label>Service Type:</label>
                                <select id="serviceFilter" onchange="filterProfessionals()">
                                    <option value="all">All Services</option>
                                    <option value="plumber">Plumber</option>
                                    <option value="cleaner">Cleaner</option>
                                    <option value="electrician">Electrician</option>
                                    <option value="carpenter">Carpenter</option>
                                </select>
                            </div>
                            
                            <div class="professionals-grid" id="professionalsGrid">
                                <div class="professional-card" data-service="plumber">
                                    <h3>John Plumber ✓</h3>
                                    <p class="rating">4.8⭐ (127 reviews)</p>
                                    <p><strong>Service:</strong> Plumbing</p>
                                    <p><strong>Price:</strong> KSH 50-100</p>
                                    <p><strong>Location:</strong> Nairobi</p>
                                    <span class="badge">Certified</span>
                                    <br><br>
                                    <button class="btn" onclick="hireProfessional('John Plumber')">Hire Now</button>
                                </div>
                                
                                <div class="professional-card" data-service="cleaner">
                                    <h3>Mary Cleaner ✓</h3>
                                    <p class="rating">4.9⭐ (89 reviews)</p>
                                    <p><strong>Service:</strong> Cleaning</p>
                                    <p><strong>Price:</strong> KSH 30-60</p>
                                    <p><strong>Location:</strong> Nairobi</p>
                                    <span class="badge">Certified</span>
                                    <br><br>
                                    <button class="btn" onclick="hireProfessional('Mary Cleaner')">Hire Now</button>
                                </div>
                                
                                <div class="professional-card" data-service="electrician">
                                    <h3>Mike Electrician</h3>
                                    <p class="rating">4.7⭐ (156 reviews)</p>
                                    <p><strong>Service:</strong> Electrical</p>
                                    <p><strong>Price:</strong> KSH 100-300</p>
                                    <p><strong>Location:</strong> Nairobi</p>
                                    <br><br>
                                    <button class="btn" onclick="hireProfessional('Mike Electrician')">Hire Now</button>
                                </div>
                            </div>
                        </div>

                        <!-- Post Job Section -->
                        <div id="post-job" class="section hidden">
                            <h2>Post a Job</h2>
                            <form onsubmit="postJob(event)">
                                <div class="form-group">
                                    <label>Service Type:</label>
                                    <select required>
                                        <option value="">Select Service</option>
                                        <option value="plumber">Plumber</option>
                                        <option value="cleaner">Cleaner</option>
                                        <option value="electrician">Electrician</option>
                                        <option value="carpenter">Carpenter</option>
                                    </select>
                                </div>
                                
                                <div class="form-group">
                                    <label>Job Description:</label>
                                    <textarea rows="4" placeholder="Describe what you need done..." required></textarea>
                                </div>
                                
                                <div class="form-group">
                                    <label>Budget Range (KSH):</label>
                                    <select required>
                                        <option value="">Select Budget</option>
                                        <option value="0-50">0-50</option>
                                        <option value="50-100">50-100</option>
                                        <option value="100-300">100-300</option>
                                        <option value="300+">300+</option>
                                    </select>
                                </div>
                                
                                <div class="form-group">
                                    <label>Timing:</label>
                                    <select required>
                                        <option value="urgent">Urgent (ASAP)</option>
                                        <option value="scheduled">Scheduled</option>
                                    </select>
                                </div>
                                
                                <button type="submit" class="btn">Post Job</button>
                            </form>
                        </div>

                        <!-- Login Section -->
                        <div id="login" class="section hidden">
                            <h2>Login / Sign Up</h2>
                            <form onsubmit="loginUser(event)">
                                <div class="form-group">
                                    <label>Name:</label>
                                    <input type="text" placeholder="Your full name" required>
                                </div>
                                
                                <div class="form-group">
                                    <label>Email:</label>
                                    <input type="email" placeholder="your@email.com" required>
                                </div>
                                
                                <div class="form-group">
                                    <label>Contact:</label>
                                    <input type="tel" placeholder="0712345678" required>
                                </div>
                                
                                <div class="form-group">
                                    <label>Account Type:</label>
                                    <select required>
                                        <option value="client">Client</option>
                                        <option value="professional">Professional</option>
                                    </select>
                                </div>
                                
                                <button type="submit" class="btn">Login / Sign Up</button>
                            </form>
                        </div>
                    </div>

                    <!-- Hire Modal -->
                    <div id="hireModal" class="modal">
                        <div class="modal-content">
                            <span class="close" onclick="closeModal()">&times;</span>
                            <h3>Hire Professional</h3>
                            <p id="hireText"></p>
                            <div class="form-group">
                                <label>Your Message:</label>
                                <textarea rows="3" placeholder="Describe your job requirements..."></textarea>
                            </div>
                            <button class="btn" onclick="sendHireRequest()">Send Hire Request</button>
                        </div>
                    </div>

                    <script>
                        function showSection(sectionId) {{
                            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
                            document.getElementById(sectionId).classList.remove('hidden');
                        }}

                        function filterProfessionals() {{
                            const filter = document.getElementById('serviceFilter').value;
                            const cards = document.querySelectorAll('.professional-card');
                            cards.forEach(card => {{
                                if (filter === 'all' || card.dataset.service === filter) {{
                                    card.style.display = 'block';
                                }} else {{
                                    card.style.display = 'none';
                                }}
                            }});
                        }}

                        function hireProfessional(name) {{
                            document.getElementById('hireText').textContent = `Send a hire request to ${{name}}?`;
                            document.getElementById('hireModal').style.display = 'block';
                        }}

                        function closeModal() {{
                            document.getElementById('hireModal').style.display = 'none';
                        }}

                        function sendHireRequest() {{
                            alert('Hire request sent successfully! The professional will contact you soon.');
                            closeModal();
                        }}

                        function postJob(event) {{
                            event.preventDefault();
                            alert('Job posted successfully! Professionals will start sending quotes soon.');
                        }}

                        let currentUser = null;

                        function loginUser(event) {{
                            event.preventDefault();
                            const form = event.target;
                            const name = form.querySelector('input[type="text"]').value;
                            const email = form.querySelector('input[type="email"]').value;
                            const userType = form.querySelector('select').value;
                            
                            currentUser = {{ name, email, type: userType }};
                            showDashboard();
                        }}

                        function showDashboard() {{
                            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
                            
                            const dashboardHtml = `
                                <div class="section active" id="dashboard">
                                    <div class="hero">
                                        <h1>Welcome, ${{currentUser.name}}!</h1>
                                        <p>${{currentUser.type}} Dashboard</p>
                                        <button class="btn btn-secondary" onclick="logout()">Logout</button>
                                    </div>
                                    
                                    <div class="grid">
                                        ${{currentUser.type === 'client' ? `
                                            <div class="card">
                                                <h3>📝 Post a Job</h3>
                                                <p>Create new job postings and find professionals.</p>
                                                <button class="btn" onclick="showSection('post-job')">Post Job</button>
                                            </div>
                                            <div class="card">
                                                <h3>👥 Find Professionals</h3>
                                                <p>Browse and hire certified professionals.</p>
                                                <button class="btn" onclick="showSection('professionals')">Find Pros</button>
                                            </div>
                                            <div class="card">
                                                <h3>💼 My Jobs</h3>
                                                <p>View your posted jobs and manage quotes.</p>
                                                <button class="btn" onclick="showMyJobs()">My Jobs</button>
                                            </div>
                                            <div class="card">
                                                <h3>💬 Messages</h3>
                                                <p>Chat with professionals and manage communications.</p>
                                                <button class="btn" onclick="showMessages()">Messages</button>
                                            </div>
                                        ` : `
                                            <div class="card">
                                                <h3>👤 My Profile</h3>
                                                <p>Manage your professional profile and services.</p>
                                                <button class="btn" onclick="showProfile()">Edit Profile</button>
                                            </div>
                                            <div class="card">
                                                <h3>🔍 Browse Jobs</h3>
                                                <p>Find available jobs and send quotes.</p>
                                                <button class="btn" onclick="showAvailableJobs()">Browse Jobs</button>
                                            </div>
                                            <div class="card">
                                                <h3>📋 My Quotes</h3>
                                                <p>Track your sent quotes and job applications.</p>
                                                <button class="btn" onclick="showMyQuotes()">My Quotes</button>
                                            </div>
                                            <div class="card">
                                                <h3>💬 Messages</h3>
                                                <p>Communicate with clients and manage chats.</p>
                                                <button class="btn" onclick="showMessages()">Messages</button>
                                            </div>
                                        `}}
                                    </div>
                                </div>
                            `;
                            
                            document.querySelector('.container').innerHTML += dashboardHtml;
                        }}

                        function logout() {{
                            currentUser = null;
                            location.reload();
                        }}

                        function showMyJobs() {{
                            const jobsHtml = `
                                <div class="section active" id="my-jobs">
                                    <h2>My Posted Jobs</h2>
                                    <div class="professionals-grid">
                                        <div class="professional-card">
                                            <h3>Plumbing Repair</h3>
                                            <p><strong>Budget:</strong> KSH 100-300</p>
                                            <p><strong>Status:</strong> Open</p>
                                            <p><strong>Quotes:</strong> 3 received</p>
                                            <button class="btn">View Quotes</button>
                                        </div>
                                        <div class="professional-card">
                                            <h3>House Cleaning</h3>
                                            <p><strong>Budget:</strong> KSH 50-100</p>
                                            <p><strong>Status:</strong> Assigned</p>
                                            <p><strong>Professional:</strong> Mary Cleaner</p>
                                            <button class="btn">Contact Pro</button>
                                        </div>
                                    </div>
                                    <button class="btn btn-secondary" onclick="showDashboard()">Back to Dashboard</button>
                                </div>
                            `;
                            document.querySelector('.container').innerHTML = jobsHtml;
                        }}

                        function showAvailableJobs() {{
                            const jobsHtml = `
                                <div class="section active" id="available-jobs">
                                    <h2>Available Jobs</h2>
                                    <div class="professionals-grid">
                                        <div class="professional-card">
                                            <h3>Electrical Wiring</h3>
                                            <p><strong>Client:</strong> John Doe</p>
                                            <p><strong>Budget:</strong> KSH 200-500</p>
                                            <p><strong>Location:</strong> Nairobi</p>
                                            <button class="btn" onclick="sendQuote('Electrical Wiring')">Send Quote</button>
                                        </div>
                                        <div class="professional-card">
                                            <h3>Carpet Cleaning</h3>
                                            <p><strong>Client:</strong> Jane Smith</p>
                                            <p><strong>Budget:</strong> KSH 50-100</p>
                                            <p><strong>Location:</strong> Mombasa</p>
                                            <button class="btn" onclick="sendQuote('Carpet Cleaning')">Send Quote</button>
                                        </div>
                                    </div>
                                    <button class="btn btn-secondary" onclick="showDashboard()">Back to Dashboard</button>
                                </div>
                            `;
                            document.querySelector('.container').innerHTML = jobsHtml;
                        }}

                        function showMyQuotes() {{
                            const quotesHtml = `
                                <div class="section active" id="my-quotes">
                                    <h2>My Quotes</h2>
                                    <div class="professionals-grid">
                                        <div class="professional-card">
                                            <h3>Kitchen Repair</h3>
                                            <p><strong>Client:</strong> Alice Johnson</p>
                                            <p><strong>Quote:</strong> KSH 250</p>
                                            <p><strong>Status:</strong> Pending</p>
                                            <p><strong>Location:</strong> Westlands, Nairobi</p>
                                            <button class="btn" onclick="openMaps('Westlands Nairobi')">📍 View Location</button>
                                        </div>
                                        <div class="professional-card">
                                            <h3>Bathroom Cleaning</h3>
                                            <p><strong>Client:</strong> Bob Wilson</p>
                                            <p><strong>Quote:</strong> KSH 80</p>
                                            <p><strong>Status:</strong> Accepted</p>
                                            <p><strong>Location:</strong> Karen, Nairobi</p>
                                            <button class="btn" onclick="openMaps('Karen Nairobi')">📍 View Location</button>
                                        </div>
                                    </div>
                                    <button class="btn btn-secondary" onclick="showDashboard()">Back to Dashboard</button>
                                </div>
                            `;
                            document.querySelector('.container').innerHTML = quotesHtml;
                        }}

                        function showMessages() {{
                            const messagesHtml = `
                                <div class="section active" id="messages">
                                    <h2>Messages</h2>
                                    <div class="card">
                                        <h3>Chat with John Plumber</h3>
                                        <p><em>"I can fix your sink tomorrow morning. What time works for you?"</em></p>
                                        <small>2 hours ago</small>
                                    </div>
                                    <div class="card">
                                        <h3>Chat with Mary Cleaner</h3>
                                        <p><em>"Job completed successfully! Please rate my service."</em></p>
                                        <small>1 day ago</small>
                                    </div>
                                    <button class="btn btn-secondary" onclick="showDashboard()">Back to Dashboard</button>
                                </div>
                            `;
                            document.querySelector('.container').innerHTML = messagesHtml;
                        }}

                        function sendQuote(jobTitle) {{
                            alert(`Quote sent for ${{jobTitle}}! Client will review and respond soon.`);
                        }}

                        function openMaps(location) {{
                            window.open(`https://www.google.com/maps/search/${{location.replace(' ', '+')}}`, '_blank');
                        }}

                        // Close modal when clicking outside
                        window.onclick = function(event) {{
                            const modal = document.getElementById('hireModal');
                            if (event.target === modal) {{
                                modal.style.display = 'none';
                            }}
                        }}
                    </script>
                </body>
                </html>
                '''
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(html.encode())
            
            def send_expired_page(self):
                html = '''
                <html><body style="font-family: Arial; text-align: center; padding: 50px;">
                <h2>⏰ Link Expired</h2>
                <p>This sharing link has expired. Please request a new one.</p>
                </body></html>
                '''
                self.send_response(410)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
            
            def send_not_found(self):
                html = '''
                <html><body style="font-family: Arial; text-align: center; padding: 50px;">
                <h2>🔍 Link Not Found</h2>
                <p>The requested sharing link does not exist.</p>
                </body></html>
                '''
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
            
            def send_main_page(self):
                html = '''
                <html><body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>🔧 HireWise Sharing Server</h1>
                <p>Server is running. Use the application to generate sharing links.</p>
                </body></html>
                '''
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
        
        return ShareHandler
    
    def stop_server(self):
        if self.server:
            self.server.shutdown()

# Global share server instance
share_server = HireWiseShareServer()