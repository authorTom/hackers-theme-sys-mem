#!/usr/bin/env python3
import os
import time
import psutil
import curses
from curses import wrapper

# Hackers-inspired ASCII art background
HACKERS_ASCII_ART = [
    "    ╔══════════════════════════════════════════════════════════╗",
    "    ║  ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ ███████╗ ║",
    "    ║  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔════╝ ║",
    "    ║  ███████║███████║██║     █████╔╝ █████╗  ██████╔╝███████╗ ║",
    "    ║  ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗╚════██║ ║",
    "    ║  ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║███████║ ║",
    "    ║  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ║",
    "    ╚══════════════════════════════════════════════════════════╝",
    "      ╔═══════════════════════════════════════════════════════╗",
    "      ║        CRASH AND BURN - SYSTEM RAM MONITOR            ║",
    "      ╚═══════════════════════════════════════════════════════╝",
    "                                                               ",
    "       ╔═══════╗  ╔═══════╗  ╔═══════╗  ╔═══════╗  ╔═══════╗   ",
    "       ║ ▓▓▓▓▓ ║  ║ ▓▓▓▓▓ ║  ║ ▓▓▓▓▓ ║  ║ ▓▓▓▓▓ ║  ║ ▓▓▓▓▓ ║   ",
    "       ╚═══════╝  ╚═══════╝  ╚═══════╝  ╚═══════╝  ╚═══════╝   ",
    "                                                               ",
    "       ╔═════════════════════════════════════════════════╗     ",
    "       ║           MESS WITH THE BEST                     ║     ",
    "       ║                DIE LIKE THE REST                 ║     ",
    "       ╚═════════════════════════════════════════════════╝     ",
]

def get_ram_info():
    """Get RAM usage information as a percentage"""
    memory = psutil.virtual_memory()
    return memory.percent

def get_color_pair(percent):
    """Return the appropriate color pair based on RAM usage percentage"""
    if percent < 10:
        return 1  # Green
    elif percent < 20:
        return 2  # Light green
    elif percent < 30:
        return 3  # Yellow-green
    elif percent < 40:
        return 4  # Yellow
    elif percent < 50:
        return 5  # Light yellow
    elif percent < 60:
        return 6  # Yellow-orange
    elif percent < 70:
        return 7  # Orange
    elif percent < 80:
        return 8  # Light red
    elif percent < 90:
        return 9  # Red-orange
    else:
        return 10  # Red

def main(stdscr):
    # Set up curses
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.use_default_colors()
    
    # Initialize color pairs (green to red gradient)
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, 10, -1)  # Custom yellow-green
    curses.init_pair(4, curses.COLOR_YELLOW, -1)
    curses.init_pair(5, 11, -1)  # Custom light yellow
    curses.init_pair(6, 208, -1)  # Custom yellow-orange
    curses.init_pair(7, 202, -1)  # Custom orange
    curses.init_pair(8, 9, -1)    # Custom light red
    curses.init_pair(9, 196, -1)  # Custom red-orange
    curses.init_pair(10, curses.COLOR_RED, -1)
    
    # ASCII art color
    curses.init_pair(20, curses.COLOR_CYAN, -1)
    
    # Get terminal size
    height, width = stdscr.getmaxyx()
    
    while True:
        try:
            stdscr.clear()
            
            # Get RAM usage
            ram_percent = get_ram_info()
            color_pair = get_color_pair(ram_percent)
            
            # Display ASCII art background
            for i, line in enumerate(HACKERS_ASCII_ART):
                if i < height - 10:  # Leave space for the RAM bar
                    stdscr.addstr(i, 0, line, curses.color_pair(20))
            
            # Display RAM usage bar
            bar_width = 50
            filled_width = int(bar_percent := ram_percent / 100 * bar_width)
            
            # Bar title
            stdscr.addstr(len(HACKERS_ASCII_ART) + 1, 10, f"RAM USAGE: {ram_percent:.1f}%")
            
            # Draw the bar frame
            stdscr.addstr(len(HACKERS_ASCII_ART) + 3, 10, "╔" + "═" * (bar_width + 2) + "╗")
            stdscr.addstr(len(HACKERS_ASCII_ART) + 4, 10, "║ " + " " * bar_width + " ║")
            stdscr.addstr(len(HACKERS_ASCII_ART) + 5, 10, "╚" + "═" * (bar_width + 2) + "╝")
            
            # Fill the bar with appropriate color
            for i in range(filled_width):
                percent_position = (i / bar_width) * 100
                bar_color = get_color_pair(percent_position)
                stdscr.addstr(len(HACKERS_ASCII_ART) + 4, 12 + i, "█", curses.color_pair(bar_color))
            
            # Add markers
            for i in range(1, 10):
                marker_pos = int(i * bar_width / 10)
                stdscr.addstr(len(HACKERS_ASCII_ART) + 6, 12 + marker_pos, f"{i*10}")
            
            # Display additional system info
            mem = psutil.virtual_memory()
            stdscr.addstr(len(HACKERS_ASCII_ART) + 8, 10, f"Total: {mem.total / (1024**3):.1f} GB")
            stdscr.addstr(len(HACKERS_ASCII_ART) + 9, 10, f"Used: {mem.used / (1024**3):.1f} GB")
            stdscr.addstr(len(HACKERS_ASCII_ART) + 10, 10, f"Available: {mem.available / (1024**3):.1f} GB")
            
            # Instructions
            stdscr.addstr(len(HACKERS_ASCII_ART) + 12, 10, "Press 'q' to quit")
            
            stdscr.refresh()
            
            # Check for 'q' key to exit
            stdscr.timeout(500)  # Update every 500ms
            key = stdscr.getch()
            if key == ord('q'):
                break
                
        except KeyboardInterrupt:
            break
        except curses.error:
            # Terminal too small, just wait for resize
            time.sleep(1)

if __name__ == "__main__":
    # Check if psutil is installed
    try:
        import psutil
    except ImportError:
        print("This tool requires the 'psutil' package.")
        print("Please install it with: pip install psutil")
        exit(1)
        
    # Run the program
    wrapper(main)