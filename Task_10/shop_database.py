# shop_database.py
import os
import sys
import subprocess

# Auto-install rich if not found
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
except ImportError:
    print("⚠️  Rich module not found. Installing automatically...")
    print("This will only happen once.\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
        print("\n✓ Installation complete! Starting InvX...\n")
        # Import again after installation
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich import box
    except Exception as e:
        print(f"❌ Failed to install Rich module: {e}")
        print("\nPlease install manually using:")
        print("  pip install rich")
        input("\nPress Enter to exit...")
        sys.exit(1)

from datetime import datetime
from rich.text import Text
import animation_shop_intro
from shop_excute import price_calulating
import time
import animation_shop_intro


def clear_terminal():
    """Clear the terminal screen using os module."""
    os.system('cls' if os.name == 'nt' else 'clear')


class product_database:
    products = {
        "Wireless Mouse": 24.99,
        "USB-C Cable (2m)": 12.50,
        "Laptop Stand": 45.00,
        "Mechanical Keyboard": 89.99,
        "Bluetooth Headphones": 67.50,
        "Phone Case": 15.99,
        "Portable Charger (10000mAh)": 32.00,
        "HDMI Cable (1.5m)": 9.99,
        "Webcam HD 1080p": 55.00,
        "Desk Lamp LED": 28.75
    }

    __intro_setting=1

    def __init__(self):
        self.console = Console()

    def add_product(self, product_name: str, price: float) -> bool:
        """Add a product to the database."""
        try:
            product_database.products[product_name] = float(price)
            return True
        except (ValueError, TypeError):
            return False
    
    def del_product(self, product_name: str) -> bool:
        """Delete a product from the database."""
        if product_name in product_database.products:
            del product_database.products[product_name]
            return True
        return False
    
    def product_database_excution(self):
        """Display the product inventory table."""
        update_time = f"shop inventory update at [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
        table = Table(
            box=box.HEAVY_EDGE,
            show_header=True,
            header_style="bold yellow",
            caption=update_time
        )

        table.add_column('ID', style="cyan", width=5)
        table.add_column('Product', style='green', width=30)
        table.add_column('Price', style='magenta', width=10)

        for id_number, (prod_name, price) in enumerate(product_database.products.items(), start=1):
            table.add_row(str(id_number), prod_name, f"${price:.2f}")
        
        final_panel = Panel(
            table,
            title="[bold white on blue] 🛒 SHOP INVENTORY 🛒 [/bold white on blue]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        
        
        self.console.print(final_panel)
    
    def cal_pricing(self):
        """Launch the pricing calculator."""
        clear_terminal()
        price_calulating(product_database.products)

    def handle_add_product(self):
        """Handle adding a product to the database."""
        while True:
            self.product_database_excution()
            command = input("$ ")
            
            if command == 'add':
                product_name = input("Enter product name: ").strip()
                if not product_name:
                    print("Product name cannot be empty!")
                    continue
                
                try:
                    price = float(input(f"Enter price for {product_name}: $"))
                    if self.add_product(product_name, price):
                        print(f"✓ Added {product_name} at ${price:.2f}")
                    else:
                        print("✗ Failed to add product")
                except ValueError:
                    print("✗ Invalid price format")
                
                input("\nPress Enter to continue...")
                clear_terminal()
            
            elif command == 'back':
                clear_terminal()
                break
            
            elif command == 'help':
                print("\nCommands:")
                print("  add  - Add a new product")
                print("  back - Return to main menu")
                print("  help - Show this help\n")
                input("Press Enter to continue...")
                clear_terminal()
            
            else:
                print(f"Unknown command: {command}. Type 'help' for commands or 'back' to return.")
                input("Press Enter to continue...")
                clear_terminal()

    def handle_delete_product(self):
        """Handle deleting a product from the database."""
        while True:
            self.product_database_excution()
            command = input("$ ")
            
            if command == 'del':
                product_name = input("Enter product name to delete: ").strip()
                if not product_name:
                    print("Product name cannot be empty!")
                    continue
                
                if product_name in product_database.products:
                    confirm = input(f"Are you sure you want to delete '{product_name}'? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        if self.del_product(product_name):
                            print(f"✓ Deleted {product_name}")
                        else:
                            print("✗ Failed to delete product")
                    else:
                        print("Deletion cancelled")
                else:
                    print(f"✗ Product '{product_name}' not found in database")
                
                input("\nPress Enter to continue...")
                clear_terminal()
            
            elif command == 'back':
                clear_terminal()
                break
            
            elif command == 'help':
                print("\nCommands:")
                print("  delete - Delete a product")
                print("  back   - Return to main menu")
                print("  help   - Show this help\n")
                input("Press Enter to continue...")
                clear_terminal()
            
            else:
                print(f"Unknown command: {command}. Type 'help' for commands or 'back' to return.")
                input("Press Enter to continue...")
                clear_terminal()

    def handle_view_table(self):
        """Display the product table."""
        self.product_database_excution()
        input("\nPress Enter to return to main menu...")
        

    def help(self):
        """Display help information with Rich styling"""
    
        # Title
        title = Text("SHOP DATABASE - COMMAND REFERENCE", style="bold white on blue", justify="center")
        self.console.print("\n")
        self.console.print(Panel(title, border_style="bright_blue", box=box.DOUBLE))
        
        # Create main help table
        table = Table(
            title="[bold cyan]Available Commands[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
            title_style="bold cyan"
        )
        
        table.add_column("Command", style="bold green", width=30)
        table.add_column("Description", style="white", width=50)
        
        # Add commands with descriptions
        commands_info = [
            ("show table --info", "Display all products in inventory table"),
            ("ALT table --add", "Add a new product to the database"),
            ("ALT table --del", "Delete a product from the database"),
            ("open price-cal --", "Open price calculation interface"),
            ("sys setting --intro_animation", "Toggle intro animation on/off"),
            ("help", "Display this help message"),
            ("quit", "Exit the shop database system"),
        ]
        
        for cmd, desc in commands_info:
            table.add_row(cmd, desc)
        
        self.console.print(table)
        
        # Usage examples panel
        self.console.print("\n")
        examples = Table(
            title="[bold yellow]Usage Examples[/bold yellow]",
            box=box.SIMPLE,
            show_header=False,
            border_style="yellow"
        )
        examples.add_column(style="cyan")
        
        examples.add_row("→ [green]show table --info[/green]     [dim]# View all products[/dim]")
        examples.add_row("→ [green]ALT table --add[/green]       [dim]# Add new item[/dim]")
        examples.add_row("→ [green]open price-cal --[/green]     [dim]# Calculate prices[/dim]")
        
        self.console.print(examples)
        
        # Tips section
        self.console.print("\n")
        tips_panel = Panel(
            "[bold cyan]💡 Tips:[/bold cyan]\n"
            "• Commands are [yellow]case-sensitive[/yellow]\n"
            "• Type [green]help[/green] anytime to see this menu\n"
            "• Press [red]Ctrl+C[/red] to interrupt any operation",
            title="[bold white]Quick Tips[/bold white]",
            border_style="blue",
            box=box.ROUNDED
        )
        self.console.print(tips_panel)
        
        self.console.print("\n[dim]Press ENTER to continue...[/dim]")
        input()

    def intro_setting_animenation(self):
        while True:
            n=input('$').strip().lower()
            if n=='change intro=1':
                product_database.__intro_setting=1
                print(f"✓ Intro animation set to mode 1")
                input("\nPress Enter to continue...")
                clear_terminal()
                break
            elif n=='change intro=2':
                product_database.__intro_setting=2
                print(f"✓ Intro animation set to mode 2")
                input("\nPress Enter to continue...")
                clear_terminal()
                break
            elif n=='change intro=3':
                product_database.__intro_setting=3
                print(f"✓ Intro animation set to mode 3")
                input("\nPress Enter to continue...")
                clear_terminal()
                break
            elif n=='back':
                clear_terminal()
                break
            elif n=='help':
                console=Console()
                help="""
                Commands:
                  change intro=1  - Set intro animation to mode 1
                  change intro=2  - Set intro animation to mode 2
                  change intro=3  - Set intro animation to mode 3
                  back            - Return to main menu
                  help            - Show this help message
                """
                console.print(f"[bold green]{help}[/bold green]")
                input("\nPress Enter to continue...")
                clear_terminal()
            else:
                console=Console()
                help="""
                help command for chnaging intro :
                  ---- " change intro=1 "
                  ---- " change intro=2 "
                  ---- " change intro=3 "
                  """
                console.print("[bold red] invalid command.... [/bold red] ")
                console.print(f"[ bold green ] {help} [/bold green]")
                input("\nPress Enter to continue...")
                clear_terminal()



    def welcome_menu(self):
        self.args=product_database.__intro_setting
        if self.args==1:
            animation_intro=animation_shop_intro.rich_animated_intro()
        elif self.args==2:
            animation_intro=animation_shop_intro.rich_fancy_intro()
        else:
            animation_intro=animation_shop_intro.rich_simple_intro()   

    def user_input(self):
        """Main user input handler with command-based structure."""
        # Command mapping dictionary for cleaner code
        commands = {
            'show table --info': self.handle_view_table,
            'alt table --add': self.handle_add_product,
            'alt table --del': self.handle_delete_product,
            'open price-cal --': self.cal_pricing,
            'sys setting --intro_animation': self.intro_setting_animenation,
            'help': self.help,
        }

        while True:  # Outer loop to allow reset without recursion
            clear_terminal()
            self.welcome_menu()
            
            while True:  # Inner loop for main menu
                command = input("$ ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    self.console.print("\n[bold green]Thank you for using Shop Database! 👋[/bold green]\n")
                    return  # Exit completely
                
                elif command == 'reset --sys':
                    clear_terminal()
                    self.console.print("[bold yellow]🔄 Resetting system...[/bold yellow]\n")
                    time.sleep(1)  # Brief pause for visual feedback
                    break  # Break inner loop, restart outer loop

                elif command == 'clear':
                    clear_terminal()
                    continue
                
                elif command in commands:
                    clear_terminal()
                    commands[command]()
                
                else:
                    print(f"✗ Unknown command: '{command}'. Type 'help' to see available commands.")
                    print()


if __name__ == "__main__":
    database_shop = product_database()
    database_shop.user_input()
