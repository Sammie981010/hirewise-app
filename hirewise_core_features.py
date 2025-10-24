import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import uuid

# Core system features extension for HireWise
class HireWiseCoreFeatures:
    
    def refresh_professionals_list(self, tree, service_filter, location_filter, rating_filter, price_filter):
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Load professionals
        with open(self.professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Apply filters
        for pro_id, pro in professionals.items():
            # Service filter
            if service_filter != "All" and pro['service'] != service_filter:
                continue
            
            # Location filter
            if location_filter != "All" and pro['location'] != location_filter:
                continue
            
            # Rating filter
            if rating_filter != "All":
                min_rating = float(rating_filter.replace("+", ""))
                if pro['rating'] < min_rating:
                    continue
            
            # Price filter
            if price_filter != "All":
                if price_filter == "300+" and not pro['price'].startswith("300") and not pro['price'].startswith("500"):
                    continue
                elif price_filter != "300+" and pro['price'] != price_filter:
                    continue
            
            badge = " ✓" if pro.get('certified', False) else ""
            tree.insert('', 'end', text=pro['name'] + badge,
                       values=(pro['service'], f"{pro['rating']}⭐", pro['price'], pro['location']))
    
    def show_messages(self):
        msg_window = tk.Toplevel(self.root)
        msg_window.title("Messages")
        msg_window.geometry("700x500")
        
        frame = ttk.Frame(msg_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Messages", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load messages
        with open(self.messages_file, 'r') as f:
            messages = json.load(f)
        
        # Filter user's messages
        user_messages = {k: v for k, v in messages.items() 
                        if v.get('sender') == self.current_user['email'] or v.get('receiver') == self.current_user['email']}
        
        if not user_messages:
            ttk.Label(frame, text="No messages yet").pack(pady=20)
            return
        
        # Messages list
        msg_frame = ttk.Frame(frame)
        msg_frame.pack(expand=True, fill='both')
        
        for msg_id, msg in user_messages.items():
            msg_item = ttk.LabelFrame(msg_frame, text=f"From: {msg['sender']}", padding="10")
            msg_item.pack(fill='x', pady=5)
            
            ttk.Label(msg_item, text=msg['content']).pack(anchor='w')
            ttk.Label(msg_item, text=f"Date: {msg['created'][:10]}", font=('Arial', 8)).pack(anchor='e')
        
        # Send new message
        send_frame = ttk.LabelFrame(frame, text="Send Message", padding="10")
        send_frame.pack(fill='x', pady=10)
        
        ttk.Label(send_frame, text="To:").pack(anchor='w')
        to_entry = ttk.Entry(send_frame)
        to_entry.pack(fill='x', pady=2)
        
        ttk.Label(send_frame, text="Message:").pack(anchor='w')
        msg_text = tk.Text(send_frame, height=3)
        msg_text.pack(fill='x', pady=2)
        
        def send_message():
            if not to_entry.get().strip() or not msg_text.get("1.0", tk.END).strip():
                messagebox.showerror("Error", "Please fill in recipient and message")
                return
            
            msg_id = str(uuid.uuid4())[:8]
            messages[msg_id] = {
                "id": msg_id,
                "sender": self.current_user['email'],
                "receiver": to_entry.get().strip(),
                "content": msg_text.get("1.0", tk.END).strip(),
                "created": datetime.now().isoformat()
            }
            
            with open(self.messages_file, 'w') as f:
                json.dump(messages, f)
            
            messagebox.showinfo("Success", "Message sent!")
            msg_window.destroy()
        
        ttk.Button(send_frame, text="Send", command=send_message).pack(pady=5)
    
    def show_payments(self):
        pay_window = tk.Toplevel(self.root)
        pay_window.title("Payments & Wallet")
        pay_window.geometry("600x500")
        
        frame = ttk.Frame(pay_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Payment System", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Wallet balance
        balance_frame = ttk.LabelFrame(frame, text="Wallet Balance", padding="10")
        balance_frame.pack(fill='x', pady=10)
        
        ttk.Label(balance_frame, text="Current Balance: KSH 1,250", font=('Arial', 12, 'bold')).pack()
        
        # M-Pesa integration
        mpesa_frame = ttk.LabelFrame(frame, text="M-Pesa Top Up", padding="10")
        mpesa_frame.pack(fill='x', pady=10)
        
        ttk.Label(mpesa_frame, text="Phone Number:").pack(anchor='w')
        phone_entry = ttk.Entry(mpesa_frame)
        phone_entry.pack(fill='x', pady=2)
        
        ttk.Label(mpesa_frame, text="Amount (KSH):").pack(anchor='w')
        amount_entry = ttk.Entry(mpesa_frame)
        amount_entry.pack(fill='x', pady=2)
        
        def initiate_mpesa():
            if not phone_entry.get().strip() or not amount_entry.get().strip():
                messagebox.showerror("Error", "Please fill in phone and amount")
                return
            
            # Simulate M-Pesa STK push
            messagebox.showinfo("M-Pesa", f"STK push sent to {phone_entry.get()}\\nEnter PIN to complete payment")
            
            # Save payment record
            with open(self.payments_file, 'r') as f:
                payments = json.load(f)
            
            pay_id = str(uuid.uuid4())[:8]
            payments[pay_id] = {
                "id": pay_id,
                "user": self.current_user['email'],
                "type": "Top Up",
                "amount": amount_entry.get().strip(),
                "method": "M-Pesa",
                "status": "Completed",
                "created": datetime.now().isoformat()
            }
            
            with open(self.payments_file, 'w') as f:
                json.dump(payments, f)
        
        ttk.Button(mpesa_frame, text="Pay via M-Pesa", command=initiate_mpesa).pack(pady=5)
        
        # Payment history
        history_frame = ttk.LabelFrame(frame, text="Payment History", padding="10")
        history_frame.pack(expand=True, fill='both', pady=10)
        
        # Load payment history
        with open(self.payments_file, 'r') as f:
            payments = json.load(f)
        
        user_payments = {k: v for k, v in payments.items() if v.get('user') == self.current_user['email']}
        
        if user_payments:
            tree = ttk.Treeview(history_frame, columns=('Type', 'Amount', 'Method', 'Status'), show='tree headings')
            tree.heading('#0', text='Date')
            tree.heading('Type', text='Type')
            tree.heading('Amount', text='Amount')
            tree.heading('Method', text='Method')
            tree.heading('Status', text='Status')
            
            for pay_id, payment in user_payments.items():
                date = datetime.fromisoformat(payment['created']).strftime('%Y-%m-%d')
                tree.insert('', 'end', text=date,
                           values=(payment['type'], f"KSH {payment['amount']}", payment['method'], payment['status']))
            
            tree.pack(expand=True, fill='both')
    
    def show_admin_pros(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("Manage Professionals")
        admin_window.geometry("800x600")
        
        frame = ttk.Frame(admin_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Professional Management", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load professionals
        with open(self.professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=('Service', 'Rating', 'Certified', 'Status'), show='tree headings')
        tree.heading('#0', text='Name')
        tree.heading('Service', text='Service')
        tree.heading('Rating', text='Rating')
        tree.heading('Certified', text='Certified')
        tree.heading('Status', text='Status')
        
        for pro_id, pro in professionals.items():
            certified = "Yes" if pro.get('certified', False) else "No"
            status = pro.get('status', 'Active')
            tree.insert('', 'end', text=pro['name'],
                       values=(pro['service'], f"{pro['rating']}⭐", certified, status))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def approve_professional():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a professional")
                return
            
            messagebox.showinfo("Success", "Professional approved and certified!")
        
        def suspend_professional():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a professional")
                return
            
            messagebox.showinfo("Success", "Professional suspended!")
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Approve & Certify", command=approve_professional).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Suspend", command=suspend_professional).pack(side='left', padx=5)
    
    def show_analytics(self):
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("System Analytics")
        analytics_window.geometry("600x500")
        
        frame = ttk.Frame(analytics_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="System Analytics", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Load data for analytics
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        with open(self.jobs_file, 'r') as f:
            jobs = json.load(f)
        with open(self.professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Statistics
        stats_frame = ttk.LabelFrame(frame, text="Platform Statistics", padding="20")
        stats_frame.pack(fill='x', pady=10)
        
        total_users = len(users)
        total_jobs = len(jobs)
        total_pros = len(professionals)
        active_jobs = len([j for j in jobs.values() if j['status'] == 'Open'])
        
        ttk.Label(stats_frame, text=f"Total Users: {total_users}", font=('Arial', 12)).pack(anchor='w')
        ttk.Label(stats_frame, text=f"Total Jobs Posted: {total_jobs}", font=('Arial', 12)).pack(anchor='w')
        ttk.Label(stats_frame, text=f"Active Professionals: {total_pros}", font=('Arial', 12)).pack(anchor='w')
        ttk.Label(stats_frame, text=f"Open Jobs: {active_jobs}", font=('Arial', 12)).pack(anchor='w')
        
        # Service distribution
        service_frame = ttk.LabelFrame(frame, text="Popular Services", padding="20")
        service_frame.pack(fill='x', pady=10)
        
        services = {}
        for job in jobs.values():
            service = job['service']
            services[service] = services.get(service, 0) + 1
        
        for service, count in sorted(services.items(), key=lambda x: x[1], reverse=True):
            ttk.Label(service_frame, text=f"{service}: {count} jobs", font=('Arial', 10)).pack(anchor='w')
    
    def show_disputes(self):
        disputes_window = tk.Toplevel(self.root)
        disputes_window.title("Manage Disputes")
        disputes_window.geometry("700x400")
        
        frame = ttk.Frame(disputes_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Dispute Management", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Sample disputes
        disputes = [
            {"id": "D001", "client": "john@email.com", "professional": "mary@email.com", "issue": "Work not completed", "status": "Open"},
            {"id": "D002", "client": "jane@email.com", "professional": "mike@email.com", "issue": "Payment dispute", "status": "Resolved"}
        ]
        
        tree = ttk.Treeview(frame, columns=('Client', 'Professional', 'Issue', 'Status'), show='tree headings')
        tree.heading('#0', text='Dispute ID')
        tree.heading('Client', text='Client')
        tree.heading('Professional', text='Professional')
        tree.heading('Issue', text='Issue')
        tree.heading('Status', text='Status')
        
        for dispute in disputes:
            tree.insert('', 'end', text=dispute['id'],
                       values=(dispute['client'], dispute['professional'], dispute['issue'], dispute['status']))
        
        tree.pack(expand=True, fill='both', pady=10)
        
        def resolve_dispute():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a dispute")
                return
            
            messagebox.showinfo("Success", "Dispute resolved and parties notified!")
        
        ttk.Button(frame, text="Resolve Dispute", command=resolve_dispute).pack(pady=10)

# Add these methods to the main HireWiseApp class
def extend_hirewise_app():
    # This would be integrated into the main app class
    pass