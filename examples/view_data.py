import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.user_operations import get_all_users, get_user_by_email, get_user_profile
import logging
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

def display_users_table(users):
    """Display users in a formatted table."""
    table = Table(title="Users in Database")
    
    table.add_column("ID", style="cyan")
    table.add_column("Email", style="magenta")
    table.add_column("First Name", style="green")
    table.add_column("Last Name", style="green")
    table.add_column("Created At", style="yellow")
    
    for user in users:
        table.add_row(
            str(user['id']),
            user['email'],
            user.get('first_name', 'N/A'),
            user.get('last_name', 'N/A'),
            str(user['created_at'])
        )
    
    console.print(table)

def display_profile_table(profile):
    """Display user profile in a formatted table."""
    if not profile:
        console.print("[red]No profile found[/red]")
        return
        
    table = Table(title="User Profile")
    
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Phone", profile.get('phone', 'N/A'))
    table.add_row("Address", profile.get('address', 'N/A'))
    table.add_row("City", profile.get('city', 'N/A'))
    table.add_row("Country", profile.get('country', 'N/A'))
    table.add_row("Created At", str(profile['created_at']))
    
    console.print(table)

def main_menu():
    """Display main menu and handle user input."""
    while True:
        console.print("\n[bold cyan]Database Viewer[/bold cyan]")
        console.print("1. View all users")
        console.print("2. Search user by email")
        console.print("3. View user profile")
        console.print("4. Exit")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"])
        
        if choice == "1":
            users = get_all_users()
            display_users_table(users)
            
        elif choice == "2":
            email = Prompt.ask("Enter email to search")
            user = get_user_by_email(email)
            if user:
                display_users_table([user])
            else:
                console.print(f"[red]No user found with email: {email}[/red]")
                
        elif choice == "3":
            email = Prompt.ask("Enter email to view profile")
            user = get_user_by_email(email)
            if user:
                profile = get_user_profile(user['id'])
                display_profile_table(profile)
            else:
                console.print(f"[red]No user found with email: {email}[/red]")
                
        elif choice == "4":
            console.print("[green]Goodbye![/green]")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]") 