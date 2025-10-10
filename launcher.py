#!/usr/bin/env python3
"""
Launcher script for Subscription Manager.

This script allows users to choose between CLI and GUI interfaces.
"""

import sys
import os


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import matplotlib
        import numpy
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False


def show_menu():
    """Show the launcher menu."""
    print("\n" + "="*50)
    print("    SUBSCRIPTION MANAGER LAUNCHER")
    print("="*50)
    print("Choose your preferred interface:")
    print()
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    print("3. Run Demo (with sample data)")
    print("4. Exit")
    print("-" * 30)


def main():
    """Main launcher function."""
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                print("\nStarting CLI interface...")
                try:
                    from main import main as cli_main
                    cli_main()
                except ImportError as e:
                    print(f"❌ Error importing CLI: {e}")
                break
                
            elif choice == '2':
                print("\nStarting GUI interface...")
                try:
                    from gui import main as gui_main
                    gui_main()
                except ImportError as e:
                    print(f"❌ Error importing GUI: {e}")
                except Exception as e:
                    print(f"❌ GUI Error: {e}")
                    print("Make sure you have tkinter installed.")
                break
                
            elif choice == '3':
                print("\nRunning demo...")
                try:
                    from demo import main as demo_main
                    demo_main()
                except ImportError as e:
                    print(f"❌ Error importing demo: {e}")
                break
                
            elif choice == '4':
                print("Goodbye!")
                sys.exit(0)
                
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
