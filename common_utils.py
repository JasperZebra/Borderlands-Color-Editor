import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import os
import re

class BorderlandsTheme:
    """Common Borderlands theme and styling utilities"""
    
    @staticmethod
    def setup_theme(root):
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

        return style, colors

class ColorPicker:
    """Common color picker dialog for both editor versions"""
    
    @staticmethod
    def choose_color(parent, current_color, color_name, colors):
        """Open color picker for the specified color with Borderlands styling"""
        # Define a set of bright, vibrant colors that match Borderlands aesthetic
        bright_colors = [
            # Pure primary colors
            "#FF0000", # Pure red
            "#FF7D00", # Pure orange
            "#FFFF00", # Pure yellow
            "#00FF00", # Pure green
            "#00FFFF", # Pure cyan
            "#0000FF", # Pure blue
            "#7D00FF", # Pure purple
            "#FF00FF", # Pure magenta
            
            # Bright white and black
            "#FFFFFF", "#000000"
        ]
        
        # Create a custom color dialog with Borderlands styling
        dialog = tk.Toplevel(parent)
        dialog.title(f"CUSTOMIZE {color_name.upper()}")
        dialog.transient(parent)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Apply Borderlands theme
        dialog.configure(bg=colors['background'])
        dialog.option_add("*Font", "Impact 14")
        
        # Add Borderlands-style yellow border to the dialog
        dialog.configure(highlightbackground=colors['yellow'], highlightthickness=3)
        
        # Title section with Borderlands styling
        title_label = tk.Label(dialog, text=f"SELECT {color_name.upper()} COLOR", 
                            bg=colors['background'], fg=colors['yellow'],
                            font=('Impact', 20), pady=10)
        title_label.pack(fill=tk.X)
        
        # Create frame for current color
        current_frame = tk.Frame(dialog, bg=colors['background'], pady=10, padx=15)
        current_frame.pack(fill=tk.X)
        
        tk.Label(current_frame, text="CURRENT:", bg=colors['background'], 
               fg=colors['foreground'], font=('Impact', 14)).pack(side=tk.LEFT, padx=(0, 15))
        
        # Current color with cell-shaded border
        current_display = tk.Label(current_frame, bg=current_color, width=10, height=2, 
                                borderwidth=3, relief="solid")
        current_display.pack(side=tk.LEFT)
        
        # Create frame for bright color options
        colors_frame = tk.Frame(dialog, bg=colors['background'], pady=10, padx=15)
        colors_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add label for bright colors section - Borderlands style
        tk.Label(colors_frame, text="CHOOSE COLOR:", bg=colors['background'], 
               fg=colors['yellow'], font=('Impact', 16)).pack(anchor=tk.W, pady=(0, 10))
        
        # Create grid for bright colors
        color_grid = tk.Frame(colors_frame, bg=colors['background'])
        color_grid.pack(fill=tk.BOTH, expand=True)
        
        # Return value - will be set when a color is selected
        result = [None]
        
        def select_color(hex_color):
            result[0] = hex_color
            dialog.destroy()
        
        # Create color swatches with cell-shaded borders
        max_cols = 5
        for i, hex_color in enumerate(bright_colors):
            row = i // max_cols  # Calculate row based on index and max columns
            col = i % max_cols   # Calculate column based on index and max columns
            
            # Create a frame for each color with black border for cell-shaded effect
            color_frame = tk.Frame(color_grid, bd=3, relief="raised", bg="black")
            color_frame.grid(row=row, column=col, padx=10, pady=10)
            
            # The actual color button
            color_btn = tk.Button(color_frame, bg=hex_color, width=8, height=3, 
                                relief="flat", command=lambda c=hex_color: select_color(c))
            color_btn.pack()
        
        # Add custom color button with Borderlands styling
        button_frame = tk.Frame(dialog, bg=colors['background'], pady=15, padx=15)
        button_frame.pack(fill=tk.X)

        # Custom color button with orange background
        custom_btn = tk.Button(button_frame, text="CUSTOM COLOR", command=lambda: custom_color_dialog(),
                             bg=colors['button_bg'], fg=colors['button_fg'], 
                             font=('Impact', 14), bd=3, width=15)
        custom_btn.pack(side=tk.LEFT)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="CANCEL", command=dialog.destroy,
                             bg=colors['button_bg'], fg=colors['button_fg'], 
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
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Wait for the dialog to be closed
        parent.wait_window(dialog)
        
        # Return the selected color or None if cancelled
        return result[0]
