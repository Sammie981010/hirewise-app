import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import uuid
import random

# Phase 2 Add-on Features for HireWise
class HireWisePhase2Features:
    
    def __init__(self):
        self.referrals_file = "hirewise_referrals.json"
        self.video_calls_file = "hirewise_video_calls.json"
        self.ai_suggestions_file = "hirewise_ai_suggestions.json"
        self.skill_badges_file = "hirewise_skill_badges.json"
        
        # Initialize data files
        for file in [self.referrals_file, self.video_calls_file, self.ai_suggestions_file, self.skill_badges_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f)
    
    def show_video_call_verification(self, professional_email):
        """In-app video call for client-pro verification"""
        video_window = tk.Toplevel()
        video_window.title("Video Call Verification")
        video_window.geometry("600x500")
        
        frame = ttk.Frame(video_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="Video Call Verification", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Video call simulation
        video_frame = tk.Frame(frame, bg='black', height=300)
        video_frame.pack(fill='x', pady=10)
        video_frame.pack_propagate(False)
        
        ttk.Label(video_frame, text="📹 Video Call Active", foreground='white', background='black', 
                 font=('Arial', 14)).pack(expand=True)
        
        # Call controls
        controls_frame = ttk.Frame(frame)
        controls_frame.pack(pady=10)
        
        def start_call():
            messagebox.showinfo("Video Call", f"Connecting to {professional_email}...")
            # Save call record
            with open(self.video_calls_file, 'r') as f:
                calls = json.load(f)
            
            call_id = str(uuid.uuid4())[:8]
            calls[call_id] = {
                "id": call_id,
                "client": "current_user_email",
                "professional": professional_email,
                "status": "Completed",
                "duration": "5:30",
                "verification_result": "Verified",
                "created": datetime.now().isoformat()
            }
            
            with open(self.video_calls_file, 'w') as f:
                json.dump(calls, f)
        
        def end_call():
            messagebox.showinfo("Call Ended", "Professional verified successfully!")
            video_window.destroy()
        
        ttk.Button(controls_frame, text="Start Call", command=start_call).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="End Call", command=end_call).pack(side='left', padx=5)
    
    def show_hirewise_wallet(self):
        """Enhanced HireWise Wallet for faster transactions"""
        wallet_window = tk.Toplevel()
        wallet_window.title("HireWise Wallet")
        wallet_window.geometry("500x600")
        
        frame = ttk.Frame(wallet_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="HireWise Wallet", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Wallet balance with quick actions
        balance_frame = ttk.LabelFrame(frame, text="Wallet Balance", padding="15")
        balance_frame.pack(fill='x', pady=10)
        
        ttk.Label(balance_frame, text="KSH 2,450.00", font=('Arial', 20, 'bold'), foreground='green').pack()
        ttk.Label(balance_frame, text="Available Balance", font=('Arial', 10)).pack()
        
        # Quick actions
        quick_frame = ttk.LabelFrame(frame, text="Quick Actions", padding="10")
        quick_frame.pack(fill='x', pady=10)
        
        actions_grid = ttk.Frame(quick_frame)
        actions_grid.pack()
        
        def quick_topup():
            amounts = ["100", "500", "1000", "2000"]
            amount = random.choice(amounts)
            messagebox.showinfo("Quick Top-up", f"KSH {amount} added to wallet via M-Pesa")
        
        def instant_pay():
            messagebox.showinfo("Instant Pay", "Payment sent instantly from wallet!")
        
        def request_money():
            messagebox.showinfo("Request Money", "Money request sent to client")
        
        ttk.Button(actions_grid, text="Quick Top-up", command=quick_topup, width=15).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(actions_grid, text="Instant Pay", command=instant_pay, width=15).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(actions_grid, text="Request Money", command=request_money, width=15).grid(row=1, column=0, padx=5, pady=5)
        
        # Transaction history
        history_frame = ttk.LabelFrame(frame, text="Recent Transactions", padding="10")
        history_frame.pack(expand=True, fill='both', pady=10)
        
        transactions = [
            {"type": "Payment", "amount": "-150", "desc": "Job #J001", "date": "2024-01-15"},
            {"type": "Top-up", "amount": "+500", "desc": "M-Pesa", "date": "2024-01-14"},
            {"type": "Received", "amount": "+300", "desc": "Job #J002", "date": "2024-01-13"}
        ]
        
        for txn in transactions:
            txn_frame = ttk.Frame(history_frame)
            txn_frame.pack(fill='x', pady=2)
            
            ttk.Label(txn_frame, text=txn['desc']).pack(side='left')
            color = 'green' if txn['amount'].startswith('+') else 'red'
            ttk.Label(txn_frame, text=f"KSH {txn['amount']}", foreground=color).pack(side='right')
    
    def show_ai_job_suggestions(self, user_profile):
        """AI-powered job suggestions based on user profile and history"""
        ai_window = tk.Toplevel()
        ai_window.title("AI Job Suggestions")
        ai_window.geometry("600x500")
        
        frame = ttk.Frame(ai_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="🤖 AI-Powered Job Suggestions", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # AI suggestions based on profile
        suggestions_frame = ttk.LabelFrame(frame, text="Recommended for You", padding="10")
        suggestions_frame.pack(expand=True, fill='both', pady=10)
        
        # Simulate AI suggestions
        ai_jobs = [
            {"title": "Plumbing Emergency - Westlands", "match": "95%", "budget": "KSH 200-400", "urgency": "Urgent"},
            {"title": "Kitchen Renovation - Karen", "match": "88%", "budget": "KSH 5000-8000", "urgency": "This Week"},
            {"title": "Bathroom Repair - Kilimani", "match": "82%", "budget": "KSH 300-600", "urgency": "Flexible"}
        ]
        
        for job in ai_jobs:
            job_frame = ttk.LabelFrame(suggestions_frame, text=f"Match: {job['match']}", padding="10")
            job_frame.pack(fill='x', pady=5)
            
            ttk.Label(job_frame, text=job['title'], font=('Arial', 12, 'bold')).pack(anchor='w')
            ttk.Label(job_frame, text=f"Budget: {job['budget']} | {job['urgency']}", font=('Arial', 10)).pack(anchor='w')
            
            def apply_to_job():
                messagebox.showinfo("AI Suggestion", "Application sent! AI matched you perfectly.")
            
            ttk.Button(job_frame, text="Quick Apply", command=apply_to_job).pack(anchor='e', pady=5)
        
        # AI insights
        insights_frame = ttk.LabelFrame(frame, text="AI Insights", padding="10")
        insights_frame.pack(fill='x', pady=10)
        
        insights = [
            "💡 You're 3x more likely to get plumbing jobs on weekends",
            "📈 Your response time is 40% faster than average",
            "⭐ Jobs in Westlands pay 25% more for your skills"
        ]
        
        for insight in insights:
            ttk.Label(insights_frame, text=insight, font=('Arial', 10)).pack(anchor='w', pady=2)
    
    def show_skill_verification_badges(self):
        """Skill verification badges linked to institutions"""
        badges_window = tk.Toplevel()
        badges_window.title("Skill Verification Badges")
        badges_window.geometry("600x500")
        
        frame = ttk.Frame(badges_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="🏆 Skill Verification Badges", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Available institutions
        institutions_frame = ttk.LabelFrame(frame, text="Verify Skills With", padding="10")
        institutions_frame.pack(fill='x', pady=10)
        
        institutions = [
            {"name": "TVET - Technical Training", "badge": "🔧", "status": "Available"},
            {"name": "Ajira Digital Program", "badge": "💻", "status": "Available"},
            {"name": "Kenya Institute of Plumbing", "badge": "🚿", "status": "Verified"},
            {"name": "Electrical Engineers Board", "badge": "⚡", "status": "Pending"}
        ]
        
        for inst in institutions:
            inst_frame = ttk.Frame(institutions_frame)
            inst_frame.pack(fill='x', pady=5)
            
            ttk.Label(inst_frame, text=f"{inst['badge']} {inst['name']}", font=('Arial', 12)).pack(side='left')
            
            status_color = {'Available': 'blue', 'Verified': 'green', 'Pending': 'orange'}
            ttk.Label(inst_frame, text=inst['status'], 
                     foreground=status_color.get(inst['status'], 'black')).pack(side='right')
        
        # Verification process
        verify_frame = ttk.LabelFrame(frame, text="Start Verification", padding="10")
        verify_frame.pack(fill='x', pady=10)
        
        ttk.Label(verify_frame, text="Select Institution:").pack(anchor='w')
        inst_combo = ttk.Combobox(verify_frame, values=["TVET", "Ajira Digital", "KIP", "EEB"])
        inst_combo.pack(fill='x', pady=5)
        
        ttk.Label(verify_frame, text="Certificate/ID Number:").pack(anchor='w')
        cert_entry = ttk.Entry(verify_frame)
        cert_entry.pack(fill='x', pady=5)
        
        def verify_skill():
            if not inst_combo.get() or not cert_entry.get():
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            messagebox.showinfo("Verification", f"Verification request sent to {inst_combo.get()}!\nYou'll receive confirmation within 24 hours.")
            
            # Save verification record
            with open(self.skill_badges_file, 'r') as f:
                badges = json.load(f)
            
            badge_id = str(uuid.uuid4())[:8]
            badges[badge_id] = {
                "id": badge_id,
                "user": "current_user_email",
                "institution": inst_combo.get(),
                "certificate_id": cert_entry.get(),
                "status": "Pending",
                "created": datetime.now().isoformat()
            }
            
            with open(self.skill_badges_file, 'w') as f:
                json.dump(badges, f)
        
        ttk.Button(verify_frame, text="Submit for Verification", command=verify_skill).pack(pady=10)
    
    def show_referral_system(self):
        """Referral system to attract more users"""
        referral_window = tk.Toplevel()
        referral_window.title("Referral Program")
        referral_window.geometry("500x600")
        
        frame = ttk.Frame(referral_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="🎁 Referral Program", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Referral stats
        stats_frame = ttk.LabelFrame(frame, text="Your Referral Stats", padding="15")
        stats_frame.pack(fill='x', pady=10)
        
        ttk.Label(stats_frame, text="Total Referrals: 5", font=('Arial', 12, 'bold')).pack(anchor='w')
        ttk.Label(stats_frame, text="Earnings: KSH 500", font=('Arial', 12, 'bold'), foreground='green').pack(anchor='w')
        ttk.Label(stats_frame, text="Next Reward at 10 referrals", font=('Arial', 10)).pack(anchor='w')
        
        # Referral code
        code_frame = ttk.LabelFrame(frame, text="Your Referral Code", padding="10")
        code_frame.pack(fill='x', pady=10)
        
        referral_code = "HIRE" + str(uuid.uuid4())[:6].upper()
        code_entry = ttk.Entry(code_frame, value=referral_code, state='readonly', font=('Arial', 14, 'bold'))
        code_entry.pack(fill='x', pady=5)
        
        def copy_code():
            referral_window.clipboard_clear()
            referral_window.clipboard_append(referral_code)
            messagebox.showinfo("Copied", "Referral code copied to clipboard!")
        
        ttk.Button(code_frame, text="Copy Code", command=copy_code).pack(pady=5)
        
        # Referral rewards
        rewards_frame = ttk.LabelFrame(frame, text="Referral Rewards", padding="10")
        rewards_frame.pack(fill='x', pady=10)
        
        rewards = [
            "👥 Refer a Client: KSH 50 bonus",
            "🔧 Refer a Professional: KSH 100 bonus", 
            "🏆 10 Referrals: Premium badge + KSH 500",
            "💎 25 Referrals: VIP status + KSH 1,500"
        ]
        
        for reward in rewards:
            ttk.Label(rewards_frame, text=reward, font=('Arial', 10)).pack(anchor='w', pady=2)
        
        # Share options
        share_frame = ttk.LabelFrame(frame, text="Share & Earn", padding="10")
        share_frame.pack(fill='x', pady=10)
        
        def share_whatsapp():
            message = f"Join HireWise with my code {referral_code} and get KSH 25 bonus!"
            messagebox.showinfo("WhatsApp", f"Share this message:\n{message}")
        
        def share_sms():
            messagebox.showinfo("SMS", f"Send '{referral_code}' to your contacts!")
        
        share_buttons = ttk.Frame(share_frame)
        share_buttons.pack()
        
        ttk.Button(share_buttons, text="Share on WhatsApp", command=share_whatsapp).pack(side='left', padx=5)
        ttk.Button(share_buttons, text="Share via SMS", command=share_sms).pack(side='left', padx=5)
        
        # Recent referrals
        recent_frame = ttk.LabelFrame(frame, text="Recent Referrals", padding="10")
        recent_frame.pack(expand=True, fill='both', pady=10)
        
        recent_referrals = [
            {"name": "John K.", "type": "Client", "bonus": "KSH 50", "date": "2024-01-15"},
            {"name": "Mary W.", "type": "Professional", "bonus": "KSH 100", "date": "2024-01-12"}
        ]
        
        for ref in recent_referrals:
            ref_frame = ttk.Frame(recent_frame)
            ref_frame.pack(fill='x', pady=2)
            
            ttk.Label(ref_frame, text=f"{ref['name']} ({ref['type']})").pack(side='left')
            ttk.Label(ref_frame, text=ref['bonus'], foreground='green').pack(side='right')

# Integration functions for main app
def add_phase2_buttons(button_frame, current_user):
    """Add Phase 2 feature buttons to main dashboard"""
    phase2 = HireWisePhase2Features()
    
    if current_user['type'] == 'Client':
        ttk.Button(button_frame, text="AI Job Match", 
                  command=lambda: phase2.show_ai_job_suggestions(current_user), width=20).pack(pady=5)
        ttk.Button(button_frame, text="HireWise Wallet", 
                  command=phase2.show_hirewise_wallet, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Referral Program", 
                  command=phase2.show_referral_system, width=20).pack(pady=5)
    
    elif current_user['type'] == 'Professional':
        ttk.Button(button_frame, text="Skill Badges", 
                  command=phase2.show_skill_verification_badges, width=20).pack(pady=5)
        ttk.Button(button_frame, text="AI Job Suggestions", 
                  command=lambda: phase2.show_ai_job_suggestions(current_user), width=20).pack(pady=5)
        ttk.Button(button_frame, text="HireWise Wallet", 
                  command=phase2.show_hirewise_wallet, width=20).pack(pady=5)
        ttk.Button(button_frame, text="Referral Program", 
                  command=phase2.show_referral_system, width=20).pack(pady=5)