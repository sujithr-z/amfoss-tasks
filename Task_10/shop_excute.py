import os
import importlib.util
from rich.table import Table
from rich import box
from rich.console import Console
from rich.panel import Panel

# Import product_database to access inventory
try:
    spec = importlib.util.spec_from_file_location("shop_database", "shop database.py")
    shop_db_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shop_db_module)
    product_database = shop_db_module.product_database
except Exception:
    # Fallback: define products directly if import fails
    class product_database:
        products = {}


def clear_terminal():
    """Clear the terminal screen using os module."""
    os.system('cls' if os.name == 'nt' else 'clear')


class price_calulating:
    def __init__(self, products=None):
        self.console = Console()
        self.data_entries = []
        self.total_sum = 0.0
        self.products = products if products is not None else product_database.products
        clear_terminal()
        self.show_welcome()
        self.run()

    def show_welcome(self):
        """Display welcome message and menu."""
        welcome_text = """
╔═══════════════════════════════════════╗
║    💵 PRICING CALCULATOR 💵           ║
╠═══════════════════════════════════════╣
║  Commands:                            ║
║                                       ║
║  add      - Add product entry         ║
║  inventory- Browse shop inventory      ║
║  view     - View pricing table        ║
║  finish   - Calculate and show total  ║
║  delete   - Delete an entry           ║
║  clear    - Clear all entries         ║
║  help     - Show this menu            ║
║  quit     - Exit calculator           ║
╚═══════════════════════════════════════╝
        """
        self.console.print(welcome_text, style="bold cyan")

    def show_inventory(self):
        """Display the shop inventory for selection."""
        inventory_list = list(self.products.items())
        
        if not inventory_list:
            print("✗ No products in inventory!")
            input("Press Enter to continue...")
            clear_terminal()
            return []
        
        table = Table(
            title='Shop Inventory',
            box=box.HEAVY_EDGE,
            header_style="bold yellow",
            show_header=True
        )
        
        table.add_column('ID', style="cyan", width=5, justify="center")
        table.add_column('Product Name', style="green", width=35)
        table.add_column('Price', style="magenta", width=15, justify="right")
        
        for id_num, (prod_name, price) in enumerate(inventory_list, start=1):
            table.add_row(str(id_num), prod_name, f"${price:.2f}")
        
        inventory_panel = Panel(
            table,
            title="[bold white on blue] 🛒 SHOP INVENTORY 🛒 [/bold white on blue]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        
        self.console.print(inventory_panel)
        return inventory_list

    def add_entry(self):
        """Add a new product entry to the pricing table."""
        try:
            print("\nSelect entry method:")
            print("1. Select from shop inventory")
            print("2. Manual entry")
            choice = input("Choice (1/2): ").strip()
            
            if choice == '1':
                # Select from inventory
                clear_terminal()
                inventory_list = self.show_inventory()
                
                if not inventory_list:
                    return
                
                try:
                    inv_id = int(input("\nEnter product ID from inventory: "))
                    if inv_id < 1 or inv_id > len(inventory_list):
                        print(f"✗ Invalid ID! Please enter a number between 1 and {len(inventory_list)}")
                        input("Press Enter to continue...")
                        clear_terminal()
                        return
                    
                    product_name, price = inventory_list[inv_id - 1]
                    print(f"\nSelected: {product_name} - ${price:.2f}")
                    
                except ValueError:
                    print("✗ Invalid ID! Please enter a valid number.")
                    input("Press Enter to continue...")
                    clear_terminal()
                    return
                
            elif choice == '2':
                # Manual entry
                product_id = int(input("Enter product ID: "))
                product_name = input("Enter product name: ").strip()
                
                if not product_name:
                    print("✗ Product name cannot be empty!")
                    input("Press Enter to continue...")
                    clear_terminal()
                    return
                
                price = float(input("Enter product price: $"))
                product_id = product_id  # Keep the manual ID
                
            else:
                print("✗ Invalid choice!")
                input("Press Enter to continue...")
                clear_terminal()
                return
            
            # Get quantity (common for both methods)
            quantity = int(input("Enter quantity: "))
            
            if quantity <= 0:
                print("✗ Quantity must be greater than 0!")
                input("Press Enter to continue...")
                clear_terminal()
                return
            
            # For inventory selection, use inventory ID; for manual, use provided ID
            if choice == '1':
                entry_id = len(self.data_entries) + 1  # Auto-increment ID
            else:
                entry_id = product_id
            
            total = price * quantity
            
            entry = {
                'id': entry_id,
                'name': product_name,
                'price': price,
                'quantity': quantity,
                'total': total
            }
            
            self.data_entries.append(entry)
            print(f"✓ Added: {product_name} (Qty: {quantity}) = ${total:.2f}")
            input("Press Enter to continue...")
            clear_terminal()
            
        except ValueError:
            print("✗ Invalid input! Please enter valid numbers.")
            input("Press Enter to continue...")
            clear_terminal()
        except KeyboardInterrupt:
            print("\n✗ Entry cancelled.")
            input("Press Enter to continue...")
            clear_terminal()

    def delete_entry(self):
        """Delete an entry from the pricing table."""
        if not self.data_entries:
            print("✗ No entries to delete!")
            input("Press Enter to continue...")
            clear_terminal()
            return
        
        self.pricing_table()
        
        try:
            entry_id = int(input("\nEnter product ID to delete: "))
            
            # Find and remove entry
            found = False
            for i, entry in enumerate(self.data_entries):
                if entry['id'] == entry_id:
                    removed = self.data_entries.pop(i)
                    print(f"✓ Deleted: {removed['name']}")
                    found = True
                    break
            
            if not found:
                print(f"✗ Product ID {entry_id} not found!")
            
            input("Press Enter to continue...")
            clear_terminal()
            
        except ValueError:
            print("✗ Invalid ID! Please enter a valid number.")
            input("Press Enter to continue...")
            clear_terminal()

    def clear_all_entries(self):
        """Clear all entries from the pricing table."""
        if not self.data_entries:
            print("✗ No entries to clear!")
            input("Press Enter to continue...")
            clear_terminal()
            return
        
        confirm = input("Are you sure you want to clear all entries? (yes/no): ").strip().lower()
        if confirm == 'yes':
            self.data_entries.clear()
            self.total_sum = 0.0
            print("✓ All entries cleared!")
        else:
            print("Clear cancelled.")
        
        input("Press Enter to continue...")
        clear_terminal()

    def calculate_total(self):
        """Calculate and display the total bill."""
        if not self.data_entries:
            print("✗ No entries to calculate! Add some products first.")
            input("Press Enter to continue...")
            clear_terminal()
            return
        
        self.total_sum = sum(entry['total'] for entry in self.data_entries)
        clear_terminal()
        
        self.pricing_table()
        
        # Display total with formatting
        total_line = "=" * 50
        self.console.print(f"\n{total_line}", style="bold yellow")
        self.console.print(f"{'TOTAL AMOUNT:':<40} ${self.total_sum:.2f}", style="bold green")
        self.console.print(total_line, style="bold yellow")
        
        print("\nPress Enter to return to menu...")
        input()
        clear_terminal()

    def pricing_table(self):
        """Display the pricing table with all entries."""
        if not self.data_entries:
            print("✗ No entries yet! Use 'add' to add products.")
            input("Press Enter to continue...")
            clear_terminal()
            return
        
        table = Table(
            title='Pricing Table',
            box=box.HEAVY_EDGE,
            header_style="bold yellow",
            show_header=True
        )

        table.add_column('ID', style="cyan", width=10, justify="center")
        table.add_column('Product Name', style="green", width=30)
        table.add_column('Price', style="magenta", width=15, justify="right")
        table.add_column('Quantity', style="cyan", width=15, justify="center")
        table.add_column('Total', style="yellow", width=15, justify="right")

        for entry in self.data_entries:
            table.add_row(
                str(entry['id']),
                entry['name'],
                f"${entry['price']:.2f}",
                str(entry['quantity']),
                f"${entry['total']:.2f}"
            )

        final_panel = Panel(
            table,
            title="[bold black on yellow] 💵 TOTAL BILL 💵 [/bold black on yellow]",
            border_style="bright_green",
            padding=(1, 2)
        )

        self.console.print(final_panel)

    def handle_view(self):
        """Handle view command."""
        self.pricing_table()
        input("\nPress Enter to continue...")
        clear_terminal()

    def handle_inventory(self):
        """Handle inventory command."""
        self.show_inventory()
        input("\nPress Enter to continue...")
        clear_terminal()

    def run(self):
        """Main loop for handling user commands."""
        # Command mapping dictionary
        commands = {
            'add': self.add_entry,
            'inventory': self.handle_inventory,
            'inv': self.handle_inventory,  # Alias
            'view': self.handle_view,
            'finish': self.calculate_total,
            'delete': self.delete_entry,
            'del': self.delete_entry,  # Alias
            'clear': self.clear_all_entries,
            'help': self.show_welcome,
        }

        while True:
            command = input("$ ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                if self.data_entries:
                    confirm = input("You have unsaved entries. Are you sure? (yes/no): ").strip().lower()
                    if confirm != 'yes':
                        continue
                self.console.print("\n[bold green]Thank you for using Pricing Calculator! 👋[/bold green]\n")
                break
            
            elif command in commands:
                commands[command]()
            
            elif not command:
                continue  # Empty input, just continue
            
            else:
                print(f"✗ Unknown command: '{command}'. Type 'help' to see available commands.")
                print()


if __name__ == "__main__":
    bill_cal = price_calulating()
