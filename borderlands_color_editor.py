import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, messagebox
import os
import re
import binascii

class BorderlandsColorEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Borderlands Color Changer | Made by: Jasper_Zebra")
        self.root.geometry("800x650")
        self.root.resizable(False, False)
        
        # Set application icon
        try:
            icon_path = os.path.join("assets", "color_editor_icon.png")
            icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon_image)
            print(f"Successfully loaded icon from {icon_path}")
        except Exception as e:
            print(f"Failed to load icon: {e}")
        
        # Apply Borderlands-inspired theme
        self.setup_borderlands_theme(root)
        
        # Initialize variables
        self.file_path = None
        self.save_data = None
        self.modified = False
        self.color_values = {
            "color1": tk.StringVar(value="#CCCCCC"),
            "color2": tk.StringVar(value="#CCCCCC"),
            "color3": tk.StringVar(value="#CCCCCC")
        }
        
        # Create the UI
        self.create_ui()
    
    def setup_borderlands_theme(self, root):
        """Configure Borderlands-inspired styling for the application"""
        # Create a style object to manage themed widget appearances
        style = ttk.Style()
        
        # Use clam theme as base - this helps with styling control
        style.theme_use('clam')
        
        # Define a color palette for Borderlands-inspired theming
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
            'button_pressed': '#CC5500',     # Darker orange when pressed
            'error': '#FF3333',              # Red for errors
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

        # LABEL FRAME STYLING
        style.configure('TLabelframe',
            background=colors['background'],
            bordercolor=colors['yellow'],        # Yellow borders for frames
            borderwidth=3                       # Thicker borders
        )
        style.configure('TLabelframe.Label',
            background=colors['background'],
            foreground=colors['yellow'],        # Yellow for section titles
            font=('Impact', 16)                 # Larger Impact font for section headers
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

        # ENTRY FIELD STYLING
        style.configure('TEntry',
            fieldbackground=colors['input_bg'],
            foreground=colors['foreground'],
            bordercolor=colors['yellow'],        # Yellow borders for input fields
            borderwidth=2,
            padding=8,
            font=('Impact', 14)
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
        
        # Value label style - for hex color display
        style.configure('Value.TLabel', 
            background=colors['background'],
            foreground=colors['orange'],         # Orange for values
            font=('Impact', 16)
        )

        # ROOT WINDOW BACKGROUND
        root.configure(bg=colors['background'])

        return style
    
    def create_ui(self):
        """Create the user interface with Borderlands styling"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title section with app name and Borderlands-style border
        title_frame = tk.Frame(main_frame, bg=self.colors['background'], 
                             bd=3, relief='ridge', highlightbackground=self.colors['yellow'],
                             highlightthickness=3)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with Borderlands-style text
        title_label = tk.Label(title_frame, text="BORDERLANDS COLOR EDITOR                   v1.2", 
                           font=('Impact', 28), bg=self.colors['background'], 
                           fg=self.colors['yellow'])
        title_label.pack(pady=10)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="SAVE FILE", padding=15)
        file_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly", width=40)
        file_entry.pack(side=tk.LEFT, padx=(0, 15), fill=tk.X, expand=True)
        
        # Borderlands-style orange button
        browse_button = ttk.Button(file_frame, text="LOAD SAVE", command=self.browse_file, width=15)
        browse_button.pack(side=tk.LEFT)
        
        # Color editing section
        color_frame = ttk.LabelFrame(main_frame, text="CHARACTER COLORS", padding=15)
        color_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create color displays and controls
        self.color_displays = {}
        self.hex_displays = {}
        
        # Labels for color categories - more Borderlands-like descriptions
        color_descriptions = [
            ("color1", "COLOR 1"),
            ("color2", "COLOR 2"),
            ("color3", "COLOR 3")
        ]
        
        # Grid layout with cell-shaded borders
        for idx, (color_name, label_text) in enumerate(color_descriptions):
            row = idx
            
            # Label with Borderlands font
            ttk.Label(color_frame, text=label_text).grid(row=row, column=0, sticky=tk.W, padx=10, pady=12)
            
            # Color box with thick black border for cell-shaded look
            color_hex = self.color_values[color_name].get()
            color_label = tk.Label(color_frame, bg=color_hex, width=8, height=2, 
                               borderwidth=3, relief="solid", highlightbackground="black")
            color_label.grid(row=row, column=1, padx=15, pady=12, sticky=tk.W)
            self.color_displays[color_name] = color_label
            
            # Hex display with orange text
            hex_var = tk.StringVar(value=color_hex)
            self.hex_displays[color_name] = hex_var
            ttk.Label(color_frame, textvariable=hex_var, width=8, style='Value.TLabel').grid(row=row, column=2, padx=15, pady=12)
            
            # Change button - with Borderlands-style uppercase text
            change_button = ttk.Button(color_frame, text="CHANGE COLOR", 
                                     command=lambda c=color_name: self.choose_color(c), width=15)
            change_button.grid(row=row, column=3, padx=10, pady=12)
        
        # Action buttons with Borderlands styling
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 10))
        
        save_button = ttk.Button(button_frame, text="SAVE CHANGES", command=self.save_changes, width=20)
        save_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        reload_button = ttk.Button(button_frame, text="RELOAD", command=self.reload_file, width=15)
        reload_button.pack(side=tk.RIGHT, padx=5)
        
        # Status bar with Borderlands-style border
        status_frame = tk.Frame(self.root, bg=self.colors['background'], bd=2, 
                             relief='sunken', highlightbackground=self.colors['yellow'])
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="READY TO CUSTOMIZE")
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                             font=('Impact', 12), bg=self.colors['background'], 
                             fg=self.colors['orange'], anchor=tk.W, padx=5, pady=3)
        status_label.pack(fill=tk.X)
    
    def browse_file(self):
        """Open a file dialog to select a Borderlands save file"""
        file_path = filedialog.askopenfilename(
            title="Select Borderlands Save File",
            filetypes=[("Save Files", "*.sav"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            self.file_path_var.set(file_path)
            self.load_save_file()
    
    def load_save_file(self):
        """Load the selected save file and extract color information"""
        try:
            with open(self.file_path, 'rb') as f:
                self.save_data = bytearray(f.read())
            
            # Player name pattern and color extraction
            player_name_pattern = re.compile(b'[\\x20-\\x7F]+\\x00\\xFF')
            player_match = player_name_pattern.search(self.save_data)
            
            if not player_match:
                messagebox.showerror("ERROR", "Could not find player data in save file")
                return
                
            # Get position right after the 00 FF that follows the player name
            color_start_pos = player_match.end()
            
            # Debug info
            print(f"Found potential color data at position: {color_start_pos:X}")
            print(f"Bytes at position: {self.save_data[color_start_pos:color_start_pos+15].hex(' ').upper()}")
            
            try:
                # Extract color1 (first 3 bytes after player name)
                color1_pos = color_start_pos
                color1_bytes = self.save_data[color1_pos:color1_pos+3]
                
                # Find position of first FF separator
                ff1_pos = color_start_pos + 3
                if self.save_data[ff1_pos] != 0xFF:
                    raise ValueError(f"Expected FF separator at {ff1_pos:X}, found {self.save_data[ff1_pos]:02X}")
                
                # Extract color2 (3 bytes after first FF)
                color2_pos = ff1_pos + 1
                color2_bytes = self.save_data[color2_pos:color2_pos+3]
                
                # Find position of second FF separator
                ff2_pos = color2_pos + 3
                if self.save_data[ff2_pos] != 0xFF:
                    raise ValueError(f"Expected FF separator at {ff2_pos:X}, found {self.save_data[ff2_pos]:02X}")
                
                # Extract color3 (3 bytes after second FF)
                color3_pos = ff2_pos + 1
                color3_bytes = self.save_data[color3_pos:color3_pos+3]
                
                # Update color values in the UI
                colors = {
                    "color1": color1_bytes,
                    "color2": color2_bytes,
                    "color3": color3_bytes
                }
                
                # Debug color values
                print(f"Color1: #{color1_bytes.hex().upper()}")
                print(f"Color2: #{color2_bytes.hex().upper()}")
                print(f"Color3: #{color3_bytes.hex().upper()}")
                
                for color_name, color_bytes in colors.items():
                    hex_color = f"#{color_bytes.hex().upper()}"
                    # Update variables
                    self.color_values[color_name].set(hex_color)
                    self.hex_displays[color_name].set(hex_color)
                    # Update UI
                    self.color_displays[color_name].config(bg=hex_color)
                
                # Show success message - Borderlands style
                messagebox.showinfo("SUCCESS", "Character colors loaded successfully!")
                self.status_var.set("COLORS LOADED")
                self.modified = False
                
            except Exception as e:
                messagebox.showerror("ERROR", f"Failed to extract color data: {str(e)}")
                print(f"Exception details: {e}")
                self.status_var.set("ERROR LOADING COLORS")
            
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to load save file: {str(e)}")
            self.status_var.set("ERROR LOADING FILE")
    
    def choose_color(self, color_name):
        """Open color picker for the specified color with bright color options"""
        current_color = self.color_values[color_name].get()
        
        # Define a set of bright, vibrant colors that match Borderlands aesthetic
        bright_colors = [
            # Pure primary colors
            "#FF0000", # Pure red
            "#00FF00", # Pure green
            "#0000FF", # Pure blue
            "#FFFF00", # Pure yellow
            "#FF00FF", # Pure magenta
            "#00FFFF", # Pure cyan
            
            # Bright white and black
            "#FFFFFF", "#000000"
        ]
        
        # Create a custom color dialog with Borderlands styling
        root = tk.Toplevel(self.root)
        root.title(f"CUSTOMIZE {color_name.upper()}")
        root.transient(self.root)
        root.grab_set()
        root.resizable(False, False)
        
        # Apply Borderlands theme
        root.configure(bg=self.colors['background'])
        root.option_add("*Font", "Impact 14")
        
        # Add Borderlands-style yellow border to the dialog
        root.configure(highlightbackground=self.colors['yellow'], highlightthickness=3)
        
        # Title section with Borderlands styling
        title_label = tk.Label(root, text=f"SELECT {color_name.upper()} COLOR", 
                            bg=self.colors['background'], fg=self.colors['yellow'],
                            font=('Impact', 20), pady=10)
        title_label.pack(fill=tk.X)
        
        # Create frame for current color
        current_frame = tk.Frame(root, bg=self.colors['background'], pady=10, padx=15)
        current_frame.pack(fill=tk.X)
        
        tk.Label(current_frame, text="CURRENT:", bg=self.colors['background'], 
               fg=self.colors['foreground'], font=('Impact', 14)).pack(side=tk.LEFT, padx=(0, 15))
        
        # Current color with cell-shaded border
        current_display = tk.Label(current_frame, bg=current_color, width=10, height=2, 
                                borderwidth=3, relief="solid")
        current_display.pack(side=tk.LEFT)
        
        # Create frame for bright color options
        colors_frame = tk.Frame(root, bg=self.colors['background'], pady=10, padx=15)
        colors_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add label for bright colors section - Borderlands style
        tk.Label(colors_frame, text="CHOOSE COLOR:", bg=self.colors['background'], 
               fg=self.colors['yellow'], font=('Impact', 16)).pack(anchor=tk.W, pady=(0, 10))
        
        # Create grid for bright colors
        color_grid = tk.Frame(colors_frame, bg=self.colors['background'])
        color_grid.pack(fill=tk.BOTH, expand=True)
        
        def select_color(hex_color):
            self.color_values[color_name].set(hex_color)
            self.hex_displays[color_name].set(hex_color)
            self.color_displays[color_name].config(bg=hex_color)
            self.modified = True
            self.status_var.set("CHANGES PENDING - SAVE TO APPLY")
            root.destroy()
        
        # Create color swatches with cell-shaded borders
        # Modified to use 5 columns and 9 rows
        max_cols = 10  # Set to 5 columns
        for i, hex_color in enumerate(bright_colors):
            row = i // max_cols  # Calculate row based on index and max columns
            col = i % max_cols   # Calculate column based on index and max columns
            
            # Create a frame for each color with black border for cell-shaded effect
            color_frame = tk.Frame(color_grid, bd=3, relief="raised", bg="black")
            color_frame.grid(row=row, column=col, padx=5, pady=5)
            
            # The actual color button
            color_btn = tk.Button(color_frame, bg=hex_color, width=6, height=2, 
                                relief="flat", command=lambda c=hex_color: select_color(c))
            color_btn.pack()
        
        # Add custom color button with Borderlands styling
        button_frame = tk.Frame(root, bg=self.colors['background'], pady=15, padx=15)
        button_frame.pack(fill=tk.X)

        # Custom color button with orange background
        custom_btn = tk.Button(button_frame, text="CUSTOM COLOR", command=lambda: custom_color_dialog(),
                             bg=self.colors['button_bg'], fg=self.colors['button_fg'], 
                             font=('Impact', 14), bd=3, width=15)
        custom_btn.pack(side=tk.LEFT)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="CANCEL", command=root.destroy,
                             bg=self.colors['button_bg'], fg=self.colors['button_fg'], 
                             font=('Impact', 14), bd=3, width=15)
        cancel_btn.pack(side=tk.RIGHT)

        def custom_color_dialog():
            color_result = colorchooser.askcolor(
                current_color, 
                title=f"CUSTOM {color_name.upper()} COLOR"
            )
            
            if color_result[1]:
                hex_color = color_result[1].upper()
                select_color(hex_color)
        
        # Center the dialog on the parent window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - width) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - height) // 2
        root.geometry(f"+{x}+{y}")
        
        # Wait for the dialog to be closed
        root.wait_window()
        
    def save_changes(self):
        """Save color changes back to the file"""
        if not self.save_data or not self.file_path:
            messagebox.showinfo("INFO", "No save file loaded")
            return
            
        if not self.modified:
            messagebox.showinfo("INFO", "No changes to save")
            return
        
        try:
            # Find player name to locate color data position
            player_name_pattern = re.compile(b'[\\x20-\\x7F]+\\x00\\xFF')
            player_match = player_name_pattern.search(self.save_data)
            
            if not player_match:
                messagebox.showerror("ERROR", "Could not find player data in save file")
                return
                
            # Get position right after the 00 FF that follows the player name
            color_start_pos = player_match.end()
            
            # Find positions for each color and FF separator
            color1_pos = color_start_pos
            ff1_pos = color1_pos + 3
            color2_pos = ff1_pos + 1
            ff2_pos = color2_pos + 3
            color3_pos = ff2_pos + 1
            
            # Verify the FF separators are where we expect them
            if self.save_data[ff1_pos] != 0xFF or self.save_data[ff2_pos] != 0xFF:
                messagebox.showerror("ERROR", "Color data format in save file doesn't match expected pattern")
                return
            
            # Create backup if it doesn't exist
            backup_path = f"{self.file_path}.bak"
            if not os.path.exists(backup_path):
                with open(backup_path, 'wb') as f_backup:
                    with open(self.file_path, 'rb') as f_orig:
                        f_backup.write(f_orig.read())
            
            # Update colors in the save data
            # Color 1
            color1_hex = self.color_values["color1"].get().lstrip('#')
            self.save_data[color1_pos:color1_pos+3] = binascii.unhexlify(color1_hex)
            
            # Color 2
            color2_hex = self.color_values["color2"].get().lstrip('#')
            self.save_data[color2_pos:color2_pos+3] = binascii.unhexlify(color2_hex)
            
            # Color 3
            color3_hex = self.color_values["color3"].get().lstrip('#')
            self.save_data[color3_pos:color3_pos+3] = binascii.unhexlify(color3_hex)
            
            # Write back to file
            with open(self.file_path, 'wb') as f:
                f.write(self.save_data)
            
            # Debug confirmation
            print(f"Saved colors to file:")
            print(f"Color1 at {color1_pos:X}: #{color1_hex}")
            print(f"Color2 at {color2_pos:X}: #{color2_hex}")
            print(f"Color3 at {color3_pos:X}: #{color3_hex}")
            
            # Update status - Borderlands style
            self.modified = False
            self.status_var.set("CHANGES SAVED SUCCESSFULLY")
            messagebox.showinfo("SUCCESS", "Character customization complete!")
            
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to save changes: {str(e)}")
            print(f"Exception details: {e}")
            self.status_var.set("ERROR SAVING CHANGES")
    
    def reload_file(self):
        """Reload the current save file"""
        if not self.file_path:
            return
            
        if self.modified:
            if not messagebox.askyesno("CONFIRM", "Discard unsaved changes and reload?"):
                return
                
        self.load_save_file()


if __name__ == "__main__":
    root = tk.Tk()
    app = BorderlandsColorEditor(root)
    root.mainloop()