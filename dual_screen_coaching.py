"""
🎯 FRONTIER DUAL SCREEN COACHING SYSTEM
Two separate screens triggered by phone number lookup:
1. Agent Screen - Top 2-4 focus items for customer interaction
2. GigaCoach Screen - Enhanced supervisor coaching view

Features:
- Phone number lookup launches both screens
- Agent gets clean, focused view with priorities
- GigaCoach gets comprehensive coaching dashboard
- Real customer data integration
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import sqlite3
import threading
import time
import random
from datetime import datetime
import os
import csv

class DualScreenCoachingSystem:
    def __init__(self):
        # Frontier Color Scheme
        self.colors = {
            'primary': '#FF0037',      # Frontier Red
            'accent': '#96FFF5',       # Frontier Cyan
            'background': '#141928',   # Dark Navy
            'white': '#FFFFFF',
            'light_gray': '#F0F0F0',
            'dark_gray': '#333333',
            'success': '#28A745',
            'warning': '#FFC107'
        }
        
        self.agent_window = None
        self.gigacoach_window = None
        self.current_customer = None
        
        self.load_data()
        self.create_main_launcher()
        self.setup_database()

    def load_data(self):
        """Load customer and agent data from CSV files"""
        try:
            # Load customer data
            customer_file = r"C:\Users\ftrhack168\Documents\customer_data.csv"
            self.customer_data = []
            if os.path.exists(customer_file):
                with open(customer_file, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    self.customer_data = list(reader)
                print(f"SUCCESS: Loaded {len(self.customer_data)} customers")
            else:
                print(f"WARNING: Customer file not found: {customer_file}")

            # Load agent data
            agent_file = r"C:\Users\ftrhack168\Documents\agent_performance_data.csv.csv"
            self.agent_data = []
            if os.path.exists(agent_file):
                with open(agent_file, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.DictReader(f)
                    self.agent_data = list(reader)
                print(f"SUCCESS: Loaded {len(self.agent_data)} agents")
            else:
                print(f"WARNING: Agent file not found: {agent_file}")
                
        except Exception as e:
            print(f"ERROR: Error loading data: {e}")
            self.customer_data = []
            self.agent_data = []

    def create_main_launcher(self):
        """Create main launcher window for phone number input"""
        self.root = tk.Tk()
        self.root.title("🎯 Frontier Dual Screen Coaching - Phone Lookup")
        self.root.geometry("600x400")
        self.root.configure(bg=self.colors['background'])
        
        # Custom fonts
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.header_font = font.Font(family="Arial", size=14, weight="bold")
        self.body_font = font.Font(family="Arial", size=12)
        
        # Main header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎯 FRONTIER DUAL SCREEN COACHING",
            font=self.title_font,
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=30)
        
        # Phone input section
        input_frame = tk.Frame(self.root, bg=self.colors['background'])
        input_frame.pack(expand=True, pady=50)
        
        tk.Label(
            input_frame,
            text="📞 Enter Customer Phone Number:",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['white']
        ).pack(pady=20)
        
        # Phone entry with larger font
        self.phone_entry = tk.Entry(
            input_frame,
            font=('Arial', 16),
            width=20,
            bg=self.colors['white'],
            justify='center'
        )
        self.phone_entry.pack(pady=10)
        self.phone_entry.focus()
        
        # Bind Enter key
        self.phone_entry.bind('<Return>', lambda e: self.launch_dual_screens())
        
        # Launch button
        launch_btn = tk.Button(
            input_frame,
            text="🚀 Launch Agent & GigaCoach Screens",
            command=self.launch_dual_screens,
            bg=self.colors['accent'],
            fg=self.colors['dark_gray'],
            font=self.header_font,
            relief='flat',
            padx=30,
            pady=15
        )
        launch_btn.pack(pady=20)
        
        # Instructions
        instructions = """
INSTRUCTIONS:
1. Enter customer phone number above
2. Press Enter or click Launch
3. Agent Screen will open with top focus items
4. GigaCoach Screen will open with coaching dashboard

Sample numbers to test: 3256351299, 5125550123, 8908754034
        """
        
        tk.Label(
            input_frame,
            text=instructions,
            font=self.body_font,
            bg=self.colors['background'],
            fg=self.colors['light_gray'],
            justify='left'
        ).pack(pady=30)

    def launch_dual_screens(self):
        """Launch both agent and gigacoach screens"""
        phone = self.phone_entry.get().strip()
        if not phone:
            messagebox.showwarning("Input Required", "Please enter a customer phone number")
            return
        
        # Find or create customer data
        customer = self.find_customer(phone)
        if not customer:
            customer = self.create_demo_customer(phone)
        
        self.current_customer = customer
        
        # Close existing windows if open
        if self.agent_window:
            self.agent_window.destroy()
        if self.gigacoach_window:
            self.gigacoach_window.destroy()
        
        # Launch both screens
        self.create_agent_screen()
        self.create_gigacoach_screen()
        
        # Minimize main launcher
        self.root.iconify()

    def find_customer(self, phone):
        """Find customer in loaded data"""
        if not self.customer_data:
            return None
            
        # Clean phone number for comparison
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        for customer in self.customer_data:
            customer_phone = ''.join(filter(str.isdigit, str(customer.get('ANI_Phone_Number', ''))))
            if clean_phone in customer_phone or customer_phone in clean_phone:
                return customer
        
        return None

    def create_demo_customer(self, phone):
        """Create demo customer data for testing"""
        demo_profiles = [
            {
                'Customer_Type': 'Upsell Customer',
                'ANI_Phone_Number': phone,
                'Keyword_Transcript': 'Speed upgrade needed for home office',
                'Regional_Customer_Attributes': 'Tech Savvy; Young Professional',
                'Competitor_Data': 'Cox. Max speed 500 MB. Average Price $42',
                'Address': '123 Tech Street, City ST 12345'
            },
            {
                'Customer_Type': 'Loyal Customer',
                'ANI_Phone_Number': phone,
                'Keyword_Transcript': 'Want sports package with streaming',
                'Regional_Customer_Attributes': 'Sports Person; Middle Income',
                'Competitor_Data': 'Spectrum. Max speed 1 GB. Average Price $50',
                'Address': '456 Sports Ave, City ST 12345'
            },
            {
                'Customer_Type': 'At Risk Customer',
                'ANI_Phone_Number': phone,
                'Keyword_Transcript': 'Need business-grade internet solution',
                'Regional_Customer_Attributes': 'Highly Educated; Tech Savvy; Young Demographics',
                'Competitor_Data': 'Windstream. Max speed 400 MB. Average Price $40',
                'Address': '789 Business Blvd, City ST 12345'
            }
        ]
        
        return random.choice(demo_profiles)

    def create_agent_screen(self):
        """Create clean agent screen with top focus items"""
        self.agent_window = tk.Toplevel(self.root)
        self.agent_window.title("🎯 AGENT VIEW - Customer Focus Items")
        self.agent_window.geometry("800x600")
        self.agent_window.configure(bg=self.colors['background'])
        
        # Position on left side of screen
        self.agent_window.geometry("+100+100")
        
        # Header with customer info
        header_frame = tk.Frame(self.agent_window, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        customer_name = f"Customer-{self.current_customer['ANI_Phone_Number'][-4:]}"  # Use last 4 digits as name
        customer_info = f"📞 {customer_name} | {self.current_customer['ANI_Phone_Number']} | {self.current_customer['Customer_Type']}"
        
        tk.Label(
            header_frame,
            text=customer_info,
            font=self.header_font,
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack(pady=20)
        
        # Call reason
        reason_frame = tk.Frame(self.agent_window, bg=self.colors['background'])
        reason_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            reason_frame,
            text=f"🎯 Call Reason: {self.current_customer.get('Keyword_Transcript', 'General inquiry')}",
            font=self.body_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        ).pack()
        
        # Top focus items section
        focus_frame = tk.LabelFrame(
            self.agent_window,
            text="🎪 TOP FOCUS ITEMS FOR THIS CUSTOMER",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['accent'],
            relief='ridge',
            bd=2
        )
        focus_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Generate and display focus items
        focus_items = self.generate_agent_focus_items()
        
        for i, item in enumerate(focus_items, 1):
            self.create_focus_item_card(focus_frame, item, i)
        
        # Quick actions
        actions_frame = tk.Frame(self.agent_window, bg=self.colors['background'])
        actions_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            actions_frame,
            text="📞 Call Complete",
            command=self.complete_call,
            bg=self.colors['success'],
            fg=self.colors['white'],
            font=self.body_font,
            padx=20,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            actions_frame,
            text="🔄 New Customer",
            command=self.new_customer_lookup,
            bg=self.colors['warning'],
            fg=self.colors['dark_gray'],
            font=self.body_font,
            padx=20,
            pady=5
        ).pack(side='right', padx=5)

    def create_focus_item_card(self, parent, item, priority):
        """Create a focus item card for the agent"""
        # Card frame with priority-based styling
        card_colors = {
            1: {'bg': self.colors['primary'], 'fg': self.colors['white']},
            2: {'bg': self.colors['accent'], 'fg': self.colors['dark_gray']},
            3: {'bg': '#FF69B4', 'fg': self.colors['white']},
            4: {'bg': '#87CEEB', 'fg': self.colors['dark_gray']}
        }
        
        color = card_colors.get(priority, card_colors[1])
        
        card_frame = tk.Frame(parent, bg=color['bg'], relief='raised', bd=3)
        card_frame.pack(fill='x', padx=10, pady=10)
        
        # Priority indicator
        tk.Label(
            card_frame,
            text=f"#{priority} PRIORITY",
            font=('Arial', 10, 'bold'),
            bg=color['bg'],
            fg=color['fg']
        ).pack(pady=5)
        
        # Item title
        tk.Label(
            card_frame,
            text=item['title'],
            font=('Arial', 14, 'bold'),
            bg=color['bg'],
            fg=color['fg']
        ).pack(pady=5)
        
        # Success rate
        tk.Label(
            card_frame,
            text=f"Success Rate: {item['confidence']}%",
            font=self.body_font,
            bg=color['bg'],
            fg=color['fg']
        ).pack()
        
        # Key talking point
        tk.Label(
            card_frame,
            text=f"💡 Key Point: {item['talking_point']}",
            font=self.body_font,
            bg=color['bg'],
            fg=color['fg'],
            wraplength=600,
            justify='center'
        ).pack(pady=10, padx=20)

    def generate_agent_focus_items(self):
        """Generate top focus items based on customer profile"""
        customer_type = self.current_customer.get('Customer_Type', 'Standard')
        call_reason = self.current_customer.get('Keyword_Transcript', 'general').lower()
        customer_attributes = self.current_customer.get('Regional_Customer_Attributes', '').lower()
        
        # Base items that can be customized
        base_items = []
        
        # Determine focus items based on customer attributes and call reason
        if 'tech' in customer_attributes or 'upgrade' in call_reason:
            base_items = [
                {
                    'title': 'GIG SPEED UPGRADE',
                    'confidence': 92,
                    'talking_point': 'Mention dedicated bandwidth for work-from-home with guaranteed speeds even during peak hours'
                },
                {
                    'title': 'PREMIUM INTERNET PACKAGE', 
                    'confidence': 88,
                    'talking_point': 'Emphasize enterprise-grade reliability and 24/7 priority tech support'
                },
                {
                    'title': 'SMART HOME BUNDLE',
                    'confidence': 85,
                    'talking_point': 'Highlight professional installation and integration with existing devices'
                },
                {
                    'title': 'ADVANCED SECURITY',
                    'confidence': 80,
                    'talking_point': 'Focus on protecting work data and remote access security'
                }
            ]
        elif 'business' in call_reason or 'upsell' in customer_type.lower():
            base_items = [
                {
                    'title': 'BUSINESS INTERNET SOLUTION',
                    'confidence': 94,
                    'talking_point': 'Stress uptime guarantees and dedicated business support'
                },
                {
                    'title': 'DEDICATED LINE SERVICE',
                    'confidence': 89,
                    'talking_point': 'Emphasize exclusive bandwidth and priority network access'
                },
                {
                    'title': 'SECURITY & BACKUP PACKAGE',
                    'confidence': 87,
                    'talking_point': 'Highlight business continuity and data protection features'
                },
                {
                    'title': 'PRIORITY TECHNICAL SUPPORT',
                    'confidence': 85,
                    'talking_point': 'Mention direct business support line and faster resolution times'
                }
            ]
        elif 'sports' in customer_attributes or 'sports' in call_reason:
            base_items = [
                {
                    'title': 'PREMIUM SPORTS PACKAGE',
                    'confidence': 91,
                    'talking_point': 'Highlight all major sports networks and exclusive game access'
                },
                {
                    'title': 'STREAMING SPORTS BUNDLE',
                    'confidence': 87,
                    'talking_point': 'Mention mobile access and multi-device streaming capabilities'
                },
                {
                    'title': 'DVR UPGRADE',
                    'confidence': 83,
                    'talking_point': 'Emphasize recording multiple games simultaneously and extended storage'
                },
                {
                    'title': 'PREMIUM CHANNELS ADD-ON',
                    'confidence': 79,
                    'talking_point': 'Focus on exclusive sports content and behind-the-scenes access'
                }
            ]
        else:
            # Default items
            base_items = [
                {
                    'title': 'SPEED UPGRADE',
                    'confidence': 90,
                    'talking_point': 'Focus on faster speeds for better streaming and browsing experience'
                },
                {
                    'title': 'PREMIUM INTERNET',
                    'confidence': 85,
                    'talking_point': 'Emphasize reliability and consistent performance'
                },
                {
                    'title': 'ENTERTAINMENT BUNDLE',
                    'confidence': 82,
                    'talking_point': 'Highlight value and convenience of bundled services'
                },
                {
                    'title': 'STREAMING PACKAGE',
                    'confidence': 78,
                    'talking_point': 'Mention access to popular streaming services in one place'
                }
            ]
        
        # Return top 4 items
        return base_items[:4]

    def create_gigacoach_screen(self):
        """Create comprehensive GigaCoach supervisor screen"""
        self.gigacoach_window = tk.Toplevel(self.root)
        self.gigacoach_window.title("🎯 GIGACOACH - Enhanced Supervisor Dashboard")
        self.gigacoach_window.geometry("1000x700")
        self.gigacoach_window.configure(bg=self.colors['background'])
        
        # Position on right side of screen
        self.gigacoach_window.geometry("+920+100")
        
        # Header
        header_frame = tk.Frame(self.gigacoach_window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🎯 GIGACOACH - ENHANCED COACHING DASHBOARD",
            font=self.header_font,
            bg=self.colors['primary'],
            fg=self.colors['white']
        ).pack(pady=15)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.gigacoach_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tab 1: Agent Analysis
        self.create_agent_analysis_tab(notebook)
        
        # Tab 2: Customer Analysis  
        self.create_customer_analysis_tab(notebook)
        
        # Tab 3: Live Coaching
        self.create_live_coaching_tab(notebook)
        
        # Tab 4: Session Analytics
        self.create_analytics_tab(notebook)

    def create_agent_analysis_tab(self, notebook):
        """Create agent analysis tab for GigaCoach"""
        agent_frame = tk.Frame(notebook, bg=self.colors['background'])
        notebook.add(agent_frame, text="👤 Agent Analysis")
        
        # Match agent to customer
        matched_agent = self.match_agent_to_customer(self.current_customer)
        
        # Agent performance section
        perf_frame = tk.LabelFrame(
            agent_frame,
            text="🏆 MATCHED AGENT PERFORMANCE",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        )
        perf_frame.pack(fill='x', padx=20, pady=10)
        
        # Agent details
        agent_text = f"""
👤 AGENT: {matched_agent['name']}

📈 PERFORMANCE METRICS:
• Close Rate: {matched_agent['close_rate']} (Target: 50%+) ✅
• NPS Score: {matched_agent['nps']}/10.0 (Target: 9.0+) ✅
• Handle Time: {matched_agent['aht']} (Target: <7:00) ✅
• Specialty: {matched_agent['specialty']} ✅ PERFECT MATCH!

🧠 AI MATCHING REASONING:
• {matched_agent['reason1']}
• {matched_agent['reason2']}
        """
        
        tk.Label(
            perf_frame,
            text=agent_text.strip(),
            font=self.body_font,
            bg=self.colors['background'],
            fg=self.colors['white'],
            justify='left'
        ).pack(padx=20, pady=15, anchor='w')
        
        # Real-time coaching suggestions
        coaching_frame = tk.LabelFrame(
            agent_frame,
            text="💡 REAL-TIME COACHING SUGGESTIONS",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        )
        coaching_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        suggestions_text = """
🎯 COACHING OPPORTUNITIES:
• Agent is performing above targets - encourage continued excellence
• Customer type matches agent specialty - expect high success rate
• Suggest using customer's work situation to build rapport
• Recommend mentioning competitor comparison if price concerns arise

⚠️ WATCH FOR:
• Price objections - coach agent to focus on value over cost
• Technical questions - agent has strong product knowledge
• Upselling opportunities - customer profile indicates openness to upgrades

📊 PREDICTED OUTCOME:
• Success Probability: 87%
• Estimated Call Duration: 6-8 minutes
• Recommended Follow-up: Email summary of new services
        """
        
        tk.Label(
            coaching_frame,
            text=suggestions_text.strip(),
            font=self.body_font,
            bg=self.colors['background'],
            fg=self.colors['white'],
            justify='left'
        ).pack(padx=20, pady=15, anchor='w')

    def create_customer_analysis_tab(self, notebook):
        """Create customer analysis tab for GigaCoach"""
        customer_frame = tk.Frame(notebook, bg=self.colors['background'])
        notebook.add(customer_frame, text="📊 Customer Analysis")
        
        # Customer profile section
        profile_frame = tk.LabelFrame(
            customer_frame,
            text="👤 CUSTOMER PROFILE ANALYSIS",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        )
        profile_frame.pack(fill='x', padx=20, pady=10)
        
        customer_name = f"Customer-{self.current_customer['ANI_Phone_Number'][-4:]}"
        customer_text = f"""
📞 CUSTOMER DETAILS:
• Name: {customer_name}
• Type: {self.current_customer['Customer_Type']}
• Phone: {self.current_customer['ANI_Phone_Number']}
• Address: {self.current_customer.get('Address', 'N/A')}
• Call Reason: {self.current_customer.get('Keyword_Transcript', 'General inquiry')}

📈 CUSTOMER PROFILE:
• Attributes: {self.current_customer.get('Regional_Customer_Attributes', 'Standard')}
• Competitor: {self.current_customer.get('Competitor_Data', 'N/A')}
• Likelihood to Upgrade: HIGH (85%)
• Price Sensitivity: MEDIUM
• Loyalty Score: 8.2/10
        """
        
        tk.Label(
            profile_frame,
            text=customer_text.strip(),
            font=self.body_font,
            bg=self.colors['background'],
            fg=self.colors['white'],
            justify='left'
        ).pack(padx=20, pady=15, anchor='w')
        
        # Opportunity analysis
        opp_frame = tk.LabelFrame(
            customer_frame,
            text="🎯 OPPORTUNITY ANALYSIS",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        )
        opp_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        focus_items = self.generate_agent_focus_items()
        opp_text = "🎪 TOP OPPORTUNITIES:\n"
        
        for i, item in enumerate(focus_items, 1):
            opp_text += f"\n{i}. {item['title']} ({item['confidence']}% confidence)\n   💡 {item['talking_point']}\n"
        
        opp_text += f"""

💰 REVENUE POTENTIAL:
• Current Monthly: $65
• Upgrade Potential: $95-120
• Annual Value Increase: $360-660

🎯 STRATEGY RECOMMENDATION:
• Lead with speed/performance benefits
• Address work-from-home needs specifically  
• Bundle services for better value proposition
• Emphasize reliability and support quality
        """
        
        tk.Label(
            opp_frame,
            text=opp_text.strip(),
            font=self.body_font,
            bg=self.colors['background'],
            fg=self.colors['white'],
            justify='left'
        ).pack(padx=20, pady=15, anchor='nw')

    def create_live_coaching_tab(self, notebook):
        """Create live coaching tab for GigaCoach"""
        coaching_frame = tk.Frame(notebook, bg=self.colors['background'])
        notebook.add(coaching_frame, text="🎪 Live Coaching")
        
        # Live status
        status_frame = tk.Frame(coaching_frame, bg=self.colors['success'], height=40)
        status_frame.pack(fill='x', padx=10, pady=5)
        status_frame.pack_propagate(False)
        
        tk.Label(
            status_frame,
            text="🟢 LIVE CALL IN PROGRESS - Coaching Active",
            font=self.header_font,
            bg=self.colors['success'],
            fg=self.colors['white']
        ).pack(pady=8)
        
        # Script suggestions
        script_frame = tk.LabelFrame(
            coaching_frame,
            text="📝 SUGGESTED SCRIPTS & RESPONSES",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        )
        script_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create scrollable text area
        script_text = tk.Text(
            script_frame,
            font=self.body_font,
            bg=self.colors['light_gray'],
            fg=self.colors['dark_gray'],
            wrap='word',
            height=25
        )
        
        scrollbar = tk.Scrollbar(script_frame)
        scrollbar.pack(side='right', fill='y')
        
        script_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=script_text.yview)
        
        script_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Generate comprehensive coaching content
        coaching_content = self.generate_live_coaching_content()
        script_text.insert('1.0', coaching_content)
        script_text.config(state='disabled')  # Make read-only

    def generate_live_coaching_content(self):
        """Generate comprehensive live coaching content"""
        focus_items = self.generate_agent_focus_items()
        
        customer_name = f"Customer-{self.current_customer['ANI_Phone_Number'][-4:]}"
        call_reason = self.current_customer.get('Keyword_Transcript', 'your account').lower()
        
        content = f"""🎯 LIVE COACHING FOR: {customer_name}

🎪 OPENING SCRIPT:
"Thank you for calling Frontier, this is [Agent Name]. I see you're calling about {call_reason}. I'd be happy to help you with that right away. Let me pull up your account details..."

📋 DISCOVERY QUESTIONS:
1. "Can you tell me more about the specific issues you're experiencing?"
2. "How is this impacting your daily activities or work?"
3. "What would be the ideal solution from your perspective?"

🎯 PRIORITY OPPORTUNITY #1: {focus_items[0]['title']}
SUCCESS RATE: {focus_items[0]['confidence']}%

APPROACH:
"{focus_items[0]['talking_point']}"

KEY BENEFITS TO EMPHASIZE:
• Addresses their specific call reason directly
• Provides immediate value and improvement
• Competitive pricing with superior service

OBJECTION HANDLING:
Price Concern: "I understand price is important. Let me show you the value..."
Need Doubt: "Many customers are surprised how much this helps with [their issue]..."
Timing: "I can hold this pricing for you while you think about it..."

🎯 PRIORITY OPPORTUNITY #2: {focus_items[1]['title']}
SUCCESS RATE: {focus_items[1]['confidence']}%

APPROACH:
"{focus_items[1]['talking_point']}"

BUNDLE OPPORTUNITY:
"Since we're already upgrading your [service], I can add [second service] for just $X more per month - it's actually cheaper than getting them separately."

🔄 TRANSITION PHRASES:
• "Let me see what other options might benefit you..."
• "Based on what you've shared, I think you'd also appreciate..."
• "Many customers with similar needs also find value in..."

⚡ URGENCY BUILDERS:
• "This promotion ends [date]"
• "I can lock in this rate for you today"
• "Installation availability is limited this month"

✅ CLOSING TECHNIQUES:
• Assumptive: "I'll get this set up for you right now..."
• Choice: "Would you prefer installation this week or next?"
• Summary: "So you're getting [benefits] for just $X more per month..."

📞 CALL COMPLETION:
• Confirm all details and pricing
• Set clear expectations for installation/activation
• Provide confirmation number
• Thank customer and offer future support

🎯 SUCCESS INDICATORS TO LISTEN FOR:
• Customer asking about pricing/availability
• Mentioning positive past experiences
• Asking technical questions (shows interest)
• Discussing family/work needs

⚠️ RED FLAGS TO WATCH FOR:
• Multiple price objections
• Mentions of competitor research
• Reluctance to provide information
• Time pressure statements

🏆 POST-CALL COACHING:
• Review what went well
• Identify missed opportunities  
• Plan follow-up strategy
• Update customer profile with new information
        """
        
        return content

    def create_analytics_tab(self, notebook):
        """Create analytics tab for GigaCoach"""
        analytics_frame = tk.Frame(notebook, bg=self.colors['background'])
        notebook.add(analytics_frame, text="📊 Analytics")
        
        # Session stats
        stats_frame = tk.LabelFrame(
            analytics_frame,
            text="📈 SESSION STATISTICS",
            font=self.header_font,
            bg=self.colors['background'],
            fg=self.colors['accent']
        )
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        stats_text = """
📊 TODAY'S COACHING RESULTS:
• Calls Coached: 23
• Success Rate: 78% (Target: 70%)
• Average Handle Time: 7:32
• Revenue Generated: $1,847
• Customer Satisfaction: 9.1/10

🏆 AGENT PERFORMANCE:
• Calls Above Target: 4 agents
• Top Performer: Sarah Johnson (92% close rate)
• Improvement Needed: 2 agents scheduled for coaching

🎯 OPPORTUNITY ANALYSIS:
• Most Successful: Speed Upgrades (85% success)
• Highest Revenue: Business Packages ($340 avg)
• Best Customer Type Match: Tech Savvy (91% success)
        """
        
        tk.Label(
            stats_frame,
            text=stats_text.strip(),
            font=self.body_font,
            bg=self.colors['background'],
            fg=self.colors['white'],
            justify='left'
        ).pack(padx=20, pady=15, anchor='w')

    def match_agent_to_customer(self, customer):
        """AI-powered agent matching with reasoning"""
        if self.agent_data:
            customer_type = customer.get('Customer_Type', 'Tech Savvy')
            
            # Find agents matching customer type
            matching_agents = []
            for agent in self.agent_data:
                agent_specialty = agent.get('Strongest_customer_type', '').lower()
                if customer_type.lower() in agent_specialty:
                    matching_agents.append(agent)
            
            if matching_agents:
                # Get highest performing matching agent
                best_match = None
                best_rate = 0
                
                for agent in matching_agents:
                    try:
                        close_rate = float(agent.get('Close_Rate', '0%').rstrip('%'))
                        if close_rate > best_rate:
                            best_rate = close_rate
                            best_match = agent
                    except ValueError:
                        continue
                
                if best_match:
                    return {
                        'name': best_match['Name'],
                        'close_rate': best_match['Close_Rate'],
                        'nps': best_match['NPS'],
                        'aht': best_match['AHT'],
                        'specialty': best_match['Strongest_customer_type'],
                        'reason1': f"Specializes in {customer_type} customers with {best_match['Close_Rate']} success rate",
                        'reason2': f"High NPS score of {best_match['NPS']} indicates excellent customer satisfaction"
                    }
        
        # Demo agent matching
        customer_type = customer.get('Customer_Type', 'Tech Savvy')
        
        demo_agents = {
            'Tech Savvy': {
                'name': 'Sarah Johnson', 'close_rate': '52%', 'nps': '9.5', 'aht': '6:45',
                'specialty': 'Tech Savvy Customers',
                'reason1': 'Specializes in tech-savvy customers with 52% close rate (above target)',
                'reason2': 'Excellent technical knowledge and fast handling time of 6:45 minutes'
            },
            'Business Owner': {
                'name': 'Emily Rodriguez', 'close_rate': '58%', 'nps': '9.7', 'aht': '5:58',
                'specialty': 'Business Solutions',
                'reason1': 'Top performer for business customers with 58% close rate',
                'reason2': 'Outstanding NPS of 9.7 and efficient 5:58 minute handle time'
            },
            'Sports Fan': {
                'name': 'Michael Chen', 'close_rate': '38%', 'nps': '8.9', 'aht': '8:15',
                'specialty': 'Sports Entertainment',
                'reason1': 'Sports enthusiast specialist with deep product knowledge',
                'reason2': 'Strong relationship builder with sports-focused customers'
            }
        }
        
        return demo_agents.get(customer_type, demo_agents['Tech Savvy'])

    def complete_call(self):
        """Handle call completion"""
        result = messagebox.askyesno(
            "Call Complete", 
            "Mark this call as completed?\n\nThis will log the session and prepare for the next customer."
        )
        
        if result:
            # Log session
            self.log_coaching_session()
            
            # Show success message
            messagebox.showinfo("Success", "Call completed and logged successfully!")
            
            # Close agent and gigacoach windows
            if self.agent_window:
                self.agent_window.destroy()
            if self.gigacoach_window:
                self.gigacoach_window.destroy()
            
            # Restore main launcher
            self.root.deiconify()
            self.phone_entry.delete(0, tk.END)

    def new_customer_lookup(self):
        """Start new customer lookup"""
        # Close current windows
        if self.agent_window:
            self.agent_window.destroy()
        if self.gigacoach_window:
            self.gigacoach_window.destroy()
        
        # Restore main launcher
        self.root.deiconify()
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.focus()

    def setup_database(self):
        """Setup SQLite database for logging"""
        try:
            self.conn = sqlite3.connect('gigacoach_sessions.db')
            cursor = self.conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS coaching_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    phone_number TEXT,
                    customer_name TEXT,
                    customer_type TEXT,
                    agent_matched TEXT,
                    opportunities_shown TEXT,
                    call_outcome TEXT
                )
            ''')
            
            self.conn.commit()
            print("SUCCESS: GigaCoach database initialized")
            
        except Exception as e:
            print(f"WARNING: Database setup error: {e}")
            self.conn = None

    def log_coaching_session(self):
        """Log the coaching session"""
        if self.conn and self.current_customer:
            try:
                cursor = self.conn.cursor()
                matched_agent = self.match_agent_to_customer(self.current_customer)
                focus_items = self.generate_agent_focus_items()
                
                customer_name = f"Customer-{self.current_customer['ANI_Phone_Number'][-4:]}"
                cursor.execute('''
                    INSERT INTO coaching_sessions 
                    (timestamp, phone_number, customer_name, customer_type, agent_matched, opportunities_shown, call_outcome)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    datetime.now().isoformat(),
                    self.current_customer['ANI_Phone_Number'],
                    customer_name,
                    self.current_customer['Customer_Type'],
                    matched_agent['name'],
                    str([item['title'] for item in focus_items]),
                    'Completed'
                ))
                
                self.conn.commit()
                print("SUCCESS: Session logged to database")
                
            except Exception as e:
                print(f"WARNING: Logging error: {e}")

    def run(self):
        """Start the dual screen coaching system"""
        print("STARTING: Frontier Dual Screen Coaching System...")
        print("READY: Enter phone numbers to launch Agent & GigaCoach screens")
        
        # Sample phone numbers for testing
        sample_numbers = ["3256351299", "5125550123", "8908754034", "2143334455"]
        print(f"TEST: Sample numbers available: {', '.join(sample_numbers)}")
        
        self.root.mainloop()

if __name__ == "__main__":
    # Run the dual screen coaching system
    app = DualScreenCoachingSystem()
    app.run()