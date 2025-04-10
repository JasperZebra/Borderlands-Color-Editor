import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
import binascii
from common_utils import BorderlandsTheme, ColorPicker

class PCColorEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Borderlands Color Editor (PC) | Made by: Jasper_Zebra")
        self.root.geometry("900x800")  # Increased height for scan section
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
        style, self.colors = BorderlandsTheme.setup_theme(root)
        self.style = style
        
        # Initialize variables
        self.file_path = None
        self.save_data = None
        self.modified = False
        self.color_values = {
            "color1": tk.StringVar(value="#CCCCCC"),
            "color2": tk.StringVar(value="#CCCCCC"),
            "color3": tk.StringVar(value="#CCCCCC")
        }
        self.color_positions = {
            "color1": 0,
            "color2": 0,
            "color3": 0
        }
        self.player_name_var = tk.StringVar()
        self.scan_result_pos = 0
        
        # Create the UI
        self.create_ui()
    
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
        title_label = tk.Label(title_frame, text="BORDERLANDS COLOR EDITOR - PC", 
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
        
        # Player name scanner section
        scan_frame = ttk.LabelFrame(main_frame, text="NAME SCANNER", padding=15)
        scan_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Player name entry
        ttk.Label(scan_frame, text="CHARACTER NAME:").pack(side=tk.LEFT, padx=(0, 10))
        self.player_name_var = tk.StringVar()
        player_name_entry = ttk.Entry(scan_frame, textvariable=self.player_name_var, width=30)
        player_name_entry.pack(side=tk.LEFT, padx=(0, 15), fill=tk.X, expand=True)
        
        # Scan button
        scan_button = ttk.Button(scan_frame, text="SCAN", command=self.scan_for_player_name, width=15)
        scan_button.pack(side=tk.LEFT)
        
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
        
        # Return to menu button
        menu_button = ttk.Button(button_frame, text="MAIN MENU", command=self.return_to_menu, width=15)
        menu_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar with Borderlands-style border
        status_frame = tk.Frame(self.root, bg=self.colors['background'], bd=2, 
                             relief='sunken', highlightbackground=self.colors['yellow'])
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="READY TO CUSTOMIZE")
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                             font=('Impact', 12), bg=self.colors['background'], 
                             fg=self.colors['orange'], anchor=tk.W, padx=5, pady=3)
        status_label.pack(fill=tk.X)
    
    def return_to_menu(self):
        """Return to the main platform selection menu"""
        if self.modified:
            if not messagebox.askyesno("CONFIRM", "Discard unsaved changes and return to menu?"):
                return
        
        self.root.destroy()
        
        # Import and run the launcher
        import main
        root = tk.Tk()
        app = main.BorderlandsLauncher(root)
        root.mainloop()
    
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
        """Load the selected save file without automatic color extraction"""
        try:
            with open(self.file_path, 'rb') as f:
                self.save_data = bytearray(f.read())
            
            # Clear any previous color data
            for color_name in ["color1", "color2", "color3"]:
                # Reset position data
                self.color_positions[color_name] = 0
                # Reset color display to default
                default_color = "#CCCCCC"
                self.color_values[color_name].set(default_color)
                self.hex_displays[color_name].set(default_color)
                self.color_displays[color_name].config(bg=default_color)
            
            # Update status message
            self.status_var.set("SAVE FILE LOADED - USE SCAN BUTTON OR ENTER NAME TO LOCATE COLORS")
            messagebox.showinfo("SUCCESS", "Save file loaded successfully! Use the Name Scanner to locate your character colors.")
            self.modified = False
            
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to load save file: {str(e)}")
            self.status_var.set("ERROR LOADING FILE")
    
    def choose_color(self, color_name):
        """Open color picker for the specified color"""
        current_color = self.color_values[color_name].get()
        new_color = ColorPicker.choose_color(self.root, current_color, color_name, self.colors)
        
        if new_color:
            # Update the color
            self.color_values[color_name].set(new_color)
            self.hex_displays[color_name].set(new_color)
            self.color_displays[color_name].config(bg=new_color)
            self.modified = True
            self.status_var.set("CHANGES PENDING - SAVE TO APPLY")
        
    def reload_file(self):
        """Reload the current save file"""
        if not self.file_path:
            return
            
        if self.modified:
            if not messagebox.askyesno("CONFIRM", "Discard unsaved changes and reload?"):
                return
                
        self.load_save_file()
    
    def scan_for_player_name(self):
        """Scan for the player name in the save file - PC version with BGR colors"""
        if not self.save_data:
            messagebox.showerror("ERROR", "No save file loaded")
            return
            
        player_name = self.player_name_var.get().strip()
        if not player_name:
            messagebox.showerror("ERROR", "Please enter a character name")
            return
            
        try:
            print(f"Scanning for name '{player_name}' in PC save file...")
            
            # First, search for the name in the save file (case insensitive)
            found_pos = -1
            
            # Try a direct search first (faster)
            player_name_bytes = player_name.encode('utf-8', errors='replace')
            found_pos = self.save_data.find(player_name_bytes)
            
            if found_pos == -1:
                # Try case-insensitive search
                save_str = self.save_data.decode('latin-1', errors='replace').lower()
                player_name_lower = player_name.lower()
                
                if player_name_lower in save_str:
                    found_pos = save_str.find(player_name_lower)
                    print(f"Found name '{player_name}' using case-insensitive search at position: {found_pos:X}")
            else:
                print(f"Found name '{player_name}' using direct search at position: {found_pos:X}")
            
            if found_pos == -1:
                # Try a character-by-character search as fallback
                for i in range(len(self.save_data) - len(player_name)):
                    match = True
                    for j, char in enumerate(player_name.lower()):
                        byte_val = self.save_data[i + j]
                        if byte_val != ord(char) and byte_val != ord(char.upper()):
                            match = False
                            break
                    
                    if match:
                        found_pos = i
                        print(f"Found name '{player_name}' using character-by-character search at position: {found_pos:X}")
                        break
            
            if found_pos == -1:
                messagebox.showerror("ERROR", f"Could not find character name '{player_name}' in save file")
                return
            
            # Find the null terminator after the name
            name_end_pos = found_pos + len(player_name)
            while name_end_pos < len(self.save_data) and self.save_data[name_end_pos] != 0:
                name_end_pos += 1
            
            # Skip the null terminator
            if name_end_pos < len(self.save_data) and self.save_data[name_end_pos] == 0:
                name_end_pos += 1
            
            # Debug: Print bytes after the name
            debug_length = 30
            debug_end = min(name_end_pos + debug_length, len(self.save_data))
            debug_data = self.save_data[name_end_pos:debug_end]
            print(f"Bytes after name: {debug_data.hex(' ').upper()}")
            
            # Extract colors using the pattern:
            # Color 1 (3 bytes), FF separator, Color 2 (3 bytes), FF separator, Color 3 (3 bytes)
            try:
                # Color 1 is immediately after the null terminator
                color1_pos = name_end_pos
                color1_bytes = self.save_data[color1_pos:color1_pos+3]
                self.color_positions["color1"] = color1_pos
                print(f"Color1 at {color1_pos:X}: {color1_bytes.hex(' ').upper()}")
                
                # Color 2 is after the FF separator
                color2_pos = color1_pos + 3 + 1  # color1 (3 bytes) + FF (1 byte)
                color2_bytes = self.save_data[color2_pos:color2_pos+3]
                self.color_positions["color2"] = color2_pos
                print(f"Color2 at {color2_pos:X}: {color2_bytes.hex(' ').upper()}")
                
                # Color 3 is after the second FF separator
                color3_pos = color2_pos + 3 + 1  # color2 (3 bytes) + FF (1 byte)
                color3_bytes = self.save_data[color3_pos:color3_pos+3]
                self.color_positions["color3"] = color3_pos
                print(f"Color3 at {color3_pos:X}: {color3_bytes.hex(' ').upper()}")
                
                # Update color values in the UI
                colors = {
                    "color1": color1_bytes,
                    "color2": color2_bytes,
                    "color3": color3_bytes
                }
                
                # Process colors - convert from BGR to RGB for display
                for color_name, color_bytes in colors.items():
                    # Convert BGR to RGB
                    b, g, r = color_bytes
                    hex_color = f"#{r:02X}{g:02X}{b:02X}"  # Convert BGR to RGB for display
                    
                    # Debug color values
                    print(f"{color_name}: BGR={color_bytes.hex().upper()} → RGB={hex_color}")
                    
                    # Update variables
                    self.color_values[color_name].set(hex_color)
                    self.hex_displays[color_name].set(hex_color)
                    # Update UI
                    self.color_displays[color_name].config(bg=hex_color)
                
                # Show success message
                messagebox.showinfo("SUCCESS", f"Found character colors for '{player_name}' successfully!")
                self.status_var.set(f"COLORS LOADED FOR '{player_name.upper()}'")
                self.modified = False
                
            except Exception as e:
                # If exact pattern matching fails, try a more flexible approach
                print(f"Error extracting colors with specific pattern: {e}")
                print("Attempting to use fallback method...")
                
                # Fallback method could be implemented here if needed
                messagebox.showerror("ERROR", f"Could not extract colors: {str(e)}")
                self.status_var.set("ERROR EXTRACTING COLORS")
                    
        except Exception as e:
            messagebox.showerror("ERROR", f"Error during scan: {str(e)}")
            print(f"Exception details: {e}")
            self.status_var.set("SCAN ERROR")

    def save_changes(self):
        """Save color changes back to the file"""
        if not self.save_data or not self.file_path:
            messagebox.showinfo("INFO", "No save file loaded")
            return
            
        if not self.modified:
            messagebox.showinfo("INFO", "No changes to save")
            return
        
        try:
            # Create backup if it doesn't exist
            backup_path = f"{self.file_path}.bak"
            if not os.path.exists(backup_path):
                with open(backup_path, 'wb') as f_backup:
                    with open(self.file_path, 'rb') as f_orig:
                        f_backup.write(f_orig.read())
            
            # Update colors in the save data
            for color_name in ["color1", "color2", "color3"]:
                color_pos = self.color_positions[color_name]
                color_hex = self.color_values[color_name].get().lstrip('#')
                
                if len(color_hex) == 6:  # Ensure we have a valid hex color
                    # Parse RGB values from hex
                    r = int(color_hex[0:2], 16)
                    g = int(color_hex[2:4], 16)
                    b = int(color_hex[4:6], 16)
                    
                    # Convert RGB to BGR for saving
                    bgr_bytes = bytes([b, g, r])
                    self.save_data[color_pos:color_pos+3] = bgr_bytes
                    
                    print(f"Saved {color_name} at {color_pos:X}: RGB=#{color_hex} → BGR={bgr_bytes.hex().upper()}")
            
            # Write back to file
            with open(self.file_path, 'wb') as f:
                f.write(self.save_data)
            
            # Update status
            self.modified = False
            self.status_var.set("CHANGES SAVED SUCCESSFULLY")
            messagebox.showinfo("SUCCESS", "Character customization complete!")
            
        except Exception as e:
            messagebox.showerror("ERROR", f"Failed to save changes: {str(e)}")
            print(f"Exception details: {e}")
            self.status_var.set("ERROR SAVING CHANGES")