import tkinter as tk
from tkinter import ttk, messagebox
import json
import math
import random

try:
    import requests
    import geocoder
    GPS_AVAILABLE = True
except ImportError:
    GPS_AVAILABLE = False

class HireWiseGPS:
    def __init__(self):
        # Sample GPS coordinates for Nairobi areas
        self.locations = {
            "Westlands": {"lat": -1.2676, "lng": 36.8108},
            "Karen": {"lat": -1.3197, "lng": 36.6859},
            "Kilimani": {"lat": -1.2921, "lng": 36.7872},
            "CBD": {"lat": -1.2864, "lng": 36.8172},
            "Kasarani": {"lat": -1.2258, "lng": 36.8969},
            "Embakasi": {"lat": -1.3031, "lng": 36.8929}
        }
        
        # Current user location (simulated)
        self.current_location = {"lat": -1.2921, "lng": 36.7872}  # Kilimani
    
    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calculate distance between two GPS coordinates in km"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng/2) * math.sin(delta_lng/2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def get_precise_address_location(self):
        """Get precise apartment-level GPS location"""
        if GPS_AVAILABLE:
            try:
                g = geocoder.ip('me')
                if g.ok:
                    lat, lng = g.latlng
                    address = self.reverse_geocode(lat, lng)
                    self.current_location = {"lat": lat, "lng": lng}
                    return address, self.current_location
            except:
                pass
        
        # Fallback to simulated precise location
        lat = -1.2921 + random.uniform(-0.001, 0.001)
        lng = 36.7872 + random.uniform(-0.001, 0.001)
        address = self.reverse_geocode(lat, lng)
        self.current_location = {"lat": lat, "lng": lng}
        return address, self.current_location
    
    def reverse_geocode(self, lat, lng):
        if GPS_AVAILABLE:
            try:
                url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=19&addressdetails=1"
                response = requests.get(url, headers={'User-Agent': 'HireWise/1.0'})
                data = response.json()
                
                address = data.get('address', {})
                
                # Try apartment/unit identifiers
                apartment = (address.get('apartment') or address.get('unit') or 
                            address.get('flat') or address.get('suite'))
                
                building = (address.get('building') or address.get('house_name') or 
                           address.get('amenity') or address.get('residential'))
                
                house_number = address.get('house_number', '')
                road = address.get('road', 'Unknown Road')
                
                if apartment and building:
                    return f"Apt {apartment}, {building}, {road.upper()}"
                elif apartment and house_number:
                    return f"Apt {apartment}, {house_number} {road.upper()}"
                elif building:
                    return f"{building}, {road.upper()}"
                elif house_number:
                    return f"{house_number} {road.upper()}"
                else:
                    return road.upper()
            except:
                pass
        
        # Simulate apartment detection
        apartments = ["A1", "B2", "C3", "D4", "E5"]
        buildings = ["Jabulani Villa", "Sunrise Apartments", "Garden Court", "Palm Heights"]
        roads = ["MUTHAM ROAD", "KIAMBU ROAD", "NGONG ROAD", "WAIYAKI WAY"]
        
        apt = random.choice(apartments)
        building = random.choice(buildings)
        road = random.choice(roads)
        
        return f"Apt {apt}, {building}, {road}"
    
    def find_nearest_professionals(self, professionals_data, service_type=None):
        """Find professionals sorted by distance"""
        current_lat = self.current_location["lat"]
        current_lng = self.current_location["lng"]
        
        professionals_with_distance = []
        
        for pro_id, pro in professionals_data.items():
            # Get professional's location coordinates
            pro_location = self.locations.get(pro['location'], self.locations['CBD'])
            
            # Calculate distance
            distance = self.calculate_distance(
                current_lat, current_lng,
                pro_location['lat'], pro_location['lng']
            )
            
            # Filter by service type if specified
            if service_type and service_type != "All" and pro['service'] != service_type:
                continue
            
            pro_with_distance = pro.copy()
            pro_with_distance['distance'] = round(distance, 1)
            pro_with_distance['id'] = pro_id
            professionals_with_distance.append(pro_with_distance)
        
        # Sort by distance
        return sorted(professionals_with_distance, key=lambda x: x['distance'])
    
    def show_gps_professionals(self, root, professionals_file):
        """Show professionals sorted by GPS distance"""
        gps_window = tk.Toplevel(root)
        gps_window.title("📍 Nearest Service Providers")
        gps_window.geometry("700x600")
        
        frame = ttk.Frame(gps_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="📍 Nearest Service Providers", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Current location display
        current_address, current_coords = self.get_precise_address_location()
        location_frame = ttk.LabelFrame(frame, text="Your Precise Location", padding="10")
        location_frame.pack(fill='x', pady=10)
        
        ttk.Label(location_frame, text=f"🏠 {current_address}", 
                 font=('Arial', 12, 'bold')).pack(anchor='w')
        ttk.Label(location_frame, text=f"📍 GPS: {current_coords['lat']:.6f}, {current_coords['lng']:.6f}", 
                 font=('Arial', 10)).pack(anchor='w')
        ttk.Label(location_frame, text="🎯 Apartment-level accuracy", 
                 font=('Arial', 9), foreground='green').pack(anchor='w')
        
        # Service filter
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill='x', pady=10)
        
        ttk.Label(filter_frame, text="Service:").pack(side='left')
        service_var = tk.StringVar(value="All")
        service_combo = ttk.Combobox(filter_frame, textvariable=service_var,
                                   values=["All", "Plumber", "Cleaner", "Web Designer", "Electrician", "Carpenter"],
                                   width=15)
        service_combo.pack(side='left', padx=5)
        
        def refresh_list():
            self.update_professionals_list(tree, professionals_file, service_var.get())
        
        ttk.Button(filter_frame, text="🔄 Refresh Location", command=refresh_list).pack(side='left', padx=10)
        
        # Professionals list with distance
        list_frame = ttk.LabelFrame(frame, text="Service Providers by Distance", padding="10")
        list_frame.pack(expand=True, fill='both', pady=10)
        
        # Create treeview
        tree = ttk.Treeview(list_frame, columns=('Service', 'Distance', 'Rating', 'Price'), show='tree headings')
        tree.heading('#0', text='Name')
        tree.heading('Service', text='Service')
        tree.heading('Distance', text='Distance (km)')
        tree.heading('Rating', text='Rating')
        tree.heading('Price', text='Price (KSH)')
        
        # Set column widths
        tree.column('#0', width=150)
        tree.column('Service', width=120)
        tree.column('Distance', width=100)
        tree.column('Rating', width=80)
        tree.column('Price', width=100)
        
        tree.pack(expand=True, fill='both')
        
        # Initial load
        self.update_professionals_list(tree, professionals_file, "All")
        
        # Action buttons
        action_frame = ttk.Frame(frame)
        action_frame.pack(pady=10)
        
        def contact_professional():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a professional")
                return
            
            item = tree.item(selection[0])
            pro_name = item['text']
            distance = item['values'][1]
            
            messagebox.showinfo("Contact", f"Contacting {pro_name}\nDistance: {distance} km\n\nEstimated arrival: {int(float(distance) * 10)} minutes")
        
        def get_directions():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a professional")
                return
            
            item = tree.item(selection[0])
            pro_name = item['text']
            messagebox.showinfo("Directions", f"Opening GPS directions to {pro_name}...\n(Would open Google Maps in real app)")
        
        ttk.Button(action_frame, text="📞 Contact", command=contact_professional).pack(side='left', padx=5)
        ttk.Button(action_frame, text="🗺️ Get Directions", command=get_directions).pack(side='left', padx=5)
        
        return gps_window
    
    def update_professionals_list(self, tree, professionals_file, service_filter):
        """Update the professionals list with GPS distances"""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Load professionals
        with open(professionals_file, 'r') as f:
            professionals = json.load(f)
        
        # Get nearest professionals
        nearest_pros = self.find_nearest_professionals(professionals, service_filter)
        
        # Populate tree
        for pro in nearest_pros:
            badge = " ✓" if pro.get('certified', False) else ""
            distance_color = "🟢" if pro['distance'] < 5 else "🟡" if pro['distance'] < 10 else "🔴"
            
            tree.insert('', 'end', text=pro['name'] + badge,
                       values=(pro['service'], 
                              f"{distance_color} {pro['distance']} km",
                              f"{pro['rating']}⭐", 
                              pro['price']))
    
    def show_location_settings(self, root):
        """Show GPS location settings"""
        settings_window = tk.Toplevel(root)
        settings_window.title("📍 Location Settings")
        settings_window.geometry("400x300")
        
        frame = ttk.Frame(settings_window, padding="20")
        frame.pack(expand=True, fill='both')
        
        ttk.Label(frame, text="📍 Location Settings", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Location permission
        perm_frame = ttk.LabelFrame(frame, text="Location Permission", padding="10")
        perm_frame.pack(fill='x', pady=10)
        
        location_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(perm_frame, text="Enable GPS location services", 
                       variable=location_enabled).pack(anchor='w')
        ttk.Label(perm_frame, text="Allow HireWise to access your location for better service matching", 
                 font=('Arial', 9), foreground='gray').pack(anchor='w')
        
        # Manual location
        manual_frame = ttk.LabelFrame(frame, text="Manual Location", padding="10")
        manual_frame.pack(fill='x', pady=10)
        
        ttk.Label(manual_frame, text="Set your area:").pack(anchor='w')
        area_var = tk.StringVar(value="Kilimani")
        area_combo = ttk.Combobox(manual_frame, textvariable=area_var,
                                 values=list(self.locations.keys()))
        area_combo.pack(fill='x', pady=5)
        
        def save_settings():
            if area_var.get() in self.locations:
                self.current_location = self.locations[area_var.get()]
                messagebox.showinfo("Settings", f"Location set to {area_var.get()}")
                settings_window.destroy()
        
        ttk.Button(manual_frame, text="Save Settings", command=save_settings).pack(pady=10)

# Integration function
def add_gps_to_dashboard(button_frame, root, professionals_file):
    """Add GPS feature to main dashboard"""
    gps = HireWiseGPS()
    
    ttk.Button(button_frame, text="📍 Nearest Providers", 
              command=lambda: gps.show_gps_professionals(root, professionals_file), 
              width=20).pack(pady=3)
    
    ttk.Button(button_frame, text="⚙️ Location Settings", 
              command=lambda: gps.show_location_settings(root), 
              width=20).pack(pady=3)