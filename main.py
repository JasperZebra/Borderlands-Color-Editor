import tkinter as tk
from tkinter import ttk
import os
import importlib
import sys

class BorderlandsLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Borderlands Color Editor | Made by: Jasper_Zebra | Version 1.5")
        self.root.geometry("600x350")
        self.root.resizable(False, False)
        
        # Set application icon
        try:
            icon_path = os.path.join("assets", "color_editor_icon.png")
            icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Failed to load icon: {e}")
        
        # Setup theme
        self.setup_theme(root)
        
        # Create UI
        self.create_ui()
    
    def setup_theme(self, root):
        """Setup Borderlands-inspired theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define color palette
        colors = {
            'background': '#2D2D2D',         # Dark gray background
            'foreground': '#FFFFFF',         # White text
            'yellow': '#FFC800',             # Borderlands yellow
            'dark_yellow': '#CC9900',        # Darker yellow for hover states
            'orange': '#FF7800',             # Borderlands orange
            'dark_orange': '#CC5500',        # Darker orange
            'border': '#000000',             # Black borders for cell-shaded look
            'input_bg': '#3A3A3A',           # Slightly lighter gray for inputs
            'button_bg': '#FF7800',          # Orange buttons
            'button_fg': '#000000',          # Black text on buttons
            'button_pressed': '#CC5500',     # Darker orange when pressed - ADDED THIS LINE
        }
        
        # Store colors for later use
        self.colors = colors

        # GLOBAL STYLE CONFIGURATION
        style.configure('.',
            background=colors['background'],
            foreground=colors['foreground'],
            fieldbackground=colors['input_bg'],
            troughcolor=colors['background'],
            borderwidth=2,                       # Thicker borders for cell-shaded look
            bordercolor=colors['border'],
            font=('Impact', 14)                  # Borderlands uses Impact-like fonts
        )

        # FRAME STYLING
        style.configure('TFrame',
            background=colors['background']
        )

        # LABEL STYLING
        style.configure('TLabel',
            background=colors['background'],
            foreground=colors['foreground'],
            font=('Impact', 14)
        )
        
        # Title style - for main headers
        style.configure('Title.TLabel', 
            background=colors['background'],
            foreground=colors['yellow'],         # Yellow titles
            font=('Impact', 24)                  # Very large Impact font
        )
        
        # BUTTON STYLING - Orange with black text like Borderlands UI
        style.configure('TButton',
            background=colors['button_bg'],
            foreground=colors['button_fg'],
            bordercolor=colors['border'],
            borderwidth=2,                      # Thicker border for cell-shaded look
            lightcolor=colors['orange'],
            darkcolor=colors['orange'],
            focuscolor=colors['dark_orange'],
            relief='raised',                    # Raised appearance
            padding=8,
            font=('Impact', 14)
        )
        style.map('TButton',
            background=[('pressed', colors['button_pressed']), ('active', colors['dark_orange'])],
            foreground=[('pressed', colors['button_fg']), ('active', colors['button_fg'])]
        )

        # Configure platform button style
        style.configure('Platform.TButton', 
            padding=20,
            font=('Impact', 18)
        )

        # ROOT WINDOW BACKGROUND
        root.configure(bg=colors['background'])
    
    def create_ui(self):
        """Create selection screen UI"""
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title section with app name and Borderlands-style border
        title_frame = tk.Frame(main_frame, bg=self.colors['background'], 
                            bd=3, relief='ridge', highlightbackground=self.colors['yellow'],
                            highlightthickness=3)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Title with Borderlands-style text
        title_label = tk.Label(title_frame, text="BORDERLANDS COLOR EDITOR", 
                           font=('Impact', 28), bg=self.colors['background'], 
                           fg=self.colors['yellow'])
        title_label.pack(pady=10)
        
        # Selection text
        selection_label = ttk.Label(main_frame, 
                                text="SELECT YOUR PLATFORM:", 
                                font=('Impact', 18),
                                foreground=self.colors['orange'])
        selection_label.pack(pady=(0, 30))
        
        # Platform buttons container
        platforms_frame = ttk.Frame(main_frame)
        platforms_frame.pack(fill=tk.X, padx=40)
        
        # Xbox 360 Button
        xbox_button = ttk.Button(platforms_frame, 
                             text="XBOX 360", 
                             style='Platform.TButton',
                             command=self.launch_xbox_editor)
        xbox_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=10)
        
        # PC Button
        pc_button = ttk.Button(platforms_frame, 
                           text="PC", 
                           style='Platform.TButton',
                           command=self.launch_pc_editor)
        pc_button.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10, pady=10)
    
    def launch_xbox_editor(self):
        """Launch the Xbox 360 version of the color editor"""
        self.root.destroy()  # Close launcher
        
        # Import and run the Xbox editor
        try:
            import xbox_editor
            root = tk.Tk()
            app = xbox_editor.XboxColorEditor(root)
            root.mainloop()
        except ImportError:
            print("Error: Could not import xbox_editor.py")
            sys.exit(1)
    
    def launch_pc_editor(self):
        """Launch the PC version of the color editor"""
        self.root.destroy()  # Close launcher
        
        # Import and run the PC editor
        try:
            import pc_editor
            root = tk.Tk()
            app = pc_editor.PCColorEditor(root)
            root.mainloop()
        except ImportError:
            print("Error: Could not import pc_editor.py")
            sys.exit(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = BorderlandsLauncher(root)
    root.mainloop()