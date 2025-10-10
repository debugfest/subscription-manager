#!/usr/bin/env python3
"""
Subscription Manager CLI Application.

This is the main entry point for the subscription manager application.
It provides a command-line interface for managing subscriptions.
"""

import sys
import os
from typing import Optional, List
from datetime import datetime

from subscription import Subscription, SubscriptionManager
from report import ReportGenerator
from utils import (
    validate_date, validate_subscription_name, validate_category,
    validate_payment_method, parse_cost, format_currency, format_date,
    get_common_categories, get_common_payment_methods, get_current_date_string
)


class SubscriptionManagerCLI:
    """Command-line interface for the subscription manager."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.subscription_manager = SubscriptionManager()
        self.report_generator = ReportGenerator(self.subscription_manager)
        self.running = True
    
    def display_welcome(self) -> None:
        """Display welcome message and main menu."""
        print("\n" + "=" * 60)
        print("           SUBSCRIPTION MANAGER")
        print("=" * 60)
        print("Manage your subscriptions efficiently!")
        print("=" * 60)
    
    def display_main_menu(self) -> None:
        """Display the main menu options."""
        print("\nMAIN MENU:")
        print("1. Add new subscription")
        print("2. List all subscriptions")
        print("3. Edit subscription")
        print("4. Delete subscription")
        print("5. View total costs")
        print("6. View upcoming renewals")
        print("7. Search subscriptions")
        print("8. Generate reports")
        print("9. Exit")
        print("-" * 30)
    
    def get_user_choice(self) -> str:
        """Get user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-9): ").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 9.")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)
    
    def add_subscription(self) -> None:
        """Add a new subscription."""
        print("\n" + "=" * 40)
        print("ADD NEW SUBSCRIPTION")
        print("=" * 40)
        
        try:
            # Get subscription name
            while True:
                name = input("Subscription name: ").strip()
                if validate_subscription_name(name):
                    break
                print("Invalid name. Please enter a valid subscription name (2-100 characters).")
            
            # Get category
            print(f"\nCommon categories: {', '.join(get_common_categories())}")
            while True:
                category = input("Category: ").strip()
                if validate_category(category):
                    break
                print("Invalid category. Please enter a valid category (2-50 characters).")
            
            # Get cost
            while True:
                try:
                    cost_input = input("Monthly cost: ").strip()
                    cost = parse_cost(cost_input)
                    break
                except ValueError as e:
                    print(f"Invalid cost: {e}")
            
            # Get renewal date
            while True:
                renewal_date = input("Renewal date (YYYY-MM-DD): ").strip()
                if validate_date(renewal_date):
                    break
                print("Invalid date format. Please use YYYY-MM-DD format.")
            
            # Get payment method
            print(f"\nCommon payment methods: {', '.join(get_common_payment_methods())}")
            while True:
                payment_method = input("Payment method: ").strip()
                if validate_payment_method(payment_method):
                    break
                print("Invalid payment method. Please enter a valid payment method (2-50 characters).")
            
            # Create subscription
            subscription = Subscription(
                name=name,
                category=category,
                cost=cost,
                renewal_date=renewal_date,
                payment_method=payment_method
            )
            
            # Add to database
            subscription_id = self.subscription_manager.add_subscription(subscription)
            print(f"\n✅ Subscription '{name}' added successfully with ID: {subscription_id}")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"\n❌ Error adding subscription: {e}")
    
    def list_subscriptions(self) -> None:
        """List all subscriptions."""
        print("\n" + "=" * 40)
        print("ALL SUBSCRIPTIONS")
        print("=" * 40)
        
        subscriptions = self.subscription_manager.get_all_subscriptions()
        
        if not subscriptions:
            print("No subscriptions found.")
            return
        
        # Display table header
        print(f"{'ID':<4} {'Name':<25} {'Category':<15} {'Cost':<10} {'Renewal Date':<12} {'Payment Method':<15}")
        print("-" * 90)
        
        # Display subscriptions
        for sub in subscriptions:
            formatted_date = format_date(sub.renewal_date, output_format='%Y-%m-%d')
            print(f"{sub.id:<4} {sub.name[:24]:<25} {sub.category[:14]:<15} "
                  f"{format_currency(sub.cost):<10} {formatted_date:<12} {sub.payment_method[:14]:<15}")
        
        print(f"\nTotal subscriptions: {len(subscriptions)}")
    
    def edit_subscription(self) -> None:
        """Edit an existing subscription."""
        print("\n" + "=" * 40)
        print("EDIT SUBSCRIPTION")
        print("=" * 40)
        
        # First, list all subscriptions
        self.list_subscriptions()
        
        try:
            subscription_id = int(input("\nEnter subscription ID to edit: "))
            subscription = self.subscription_manager.get_subscription_by_id(subscription_id)
            
            if not subscription:
                print(f"❌ Subscription with ID {subscription_id} not found.")
                return
            
            print(f"\nEditing subscription: {subscription.name}")
            print("Press Enter to keep current value, or enter new value:")
            
            # Edit name
            new_name = input(f"Name [{subscription.name}]: ").strip()
            if new_name:
                if validate_subscription_name(new_name):
                    subscription.name = new_name
                else:
                    print("Invalid name. Keeping current value.")
            
            # Edit category
            new_category = input(f"Category [{subscription.category}]: ").strip()
            if new_category:
                if validate_category(new_category):
                    subscription.category = new_category
                else:
                    print("Invalid category. Keeping current value.")
            
            # Edit cost
            new_cost_input = input(f"Monthly cost [{format_currency(subscription.cost)}]: ").strip()
            if new_cost_input:
                try:
                    new_cost = parse_cost(new_cost_input)
                    subscription.cost = new_cost
                except ValueError as e:
                    print(f"Invalid cost: {e}. Keeping current value.")
            
            # Edit renewal date
            current_date = format_date(subscription.renewal_date, output_format='%Y-%m-%d')
            new_renewal_date = input(f"Renewal date [{current_date}]: ").strip()
            if new_renewal_date:
                if validate_date(new_renewal_date):
                    subscription.renewal_date = new_renewal_date
                else:
                    print("Invalid date format. Keeping current value.")
            
            # Edit payment method
            new_payment_method = input(f"Payment method [{subscription.payment_method}]: ").strip()
            if new_payment_method:
                if validate_payment_method(new_payment_method):
                    subscription.payment_method = new_payment_method
                else:
                    print("Invalid payment method. Keeping current value.")
            
            # Update in database
            if self.subscription_manager.update_subscription(subscription):
                print(f"\n✅ Subscription '{subscription.name}' updated successfully!")
            else:
                print(f"\n❌ Failed to update subscription.")
                
        except ValueError:
            print("❌ Invalid subscription ID.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"\n❌ Error editing subscription: {e}")
    
    def delete_subscription(self) -> None:
        """Delete a subscription."""
        print("\n" + "=" * 40)
        print("DELETE SUBSCRIPTION")
        print("=" * 40)
        
        # First, list all subscriptions
        self.list_subscriptions()
        
        try:
            subscription_id = int(input("\nEnter subscription ID to delete: "))
            subscription = self.subscription_manager.get_subscription_by_id(subscription_id)
            
            if not subscription:
                print(f"❌ Subscription with ID {subscription_id} not found.")
                return
            
            # Confirm deletion
            confirm = input(f"\nAre you sure you want to delete '{subscription.name}'? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                if self.subscription_manager.delete_subscription(subscription_id):
                    print(f"\n✅ Subscription '{subscription.name}' deleted successfully!")
                else:
                    print(f"\n❌ Failed to delete subscription.")
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("❌ Invalid subscription ID.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except Exception as e:
            print(f"\n❌ Error deleting subscription: {e}")
    
    def view_total_costs(self) -> None:
        """View total monthly and annual costs."""
        print("\n" + "=" * 40)
        print("COST SUMMARY")
        print("=" * 40)
        
        total_monthly = self.subscription_manager.get_total_monthly_cost()
        total_annual = self.subscription_manager.get_total_annual_cost()
        cost_by_category = self.subscription_manager.get_cost_by_category()
        
        print(f"Total Monthly Cost: {format_currency(total_monthly)}")
        print(f"Total Annual Cost: {format_currency(total_annual)}")
        
        if cost_by_category:
            print(f"\nCost by Category:")
            print("-" * 20)
            for category, cost in sorted(cost_by_category.items(), key=lambda x: x[1], reverse=True):
                percentage = (cost / total_monthly * 100) if total_monthly > 0 else 0
                print(f"{category}: {format_currency(cost)} ({percentage:.1f}%)")
    
    def view_upcoming_renewals(self) -> None:
        """View upcoming renewals."""
        print("\n" + "=" * 40)
        print("UPCOMING RENEWALS")
        print("=" * 40)
        
        days_input = input("Show renewals for how many days ahead? (default: 30): ").strip()
        try:
            days = int(days_input) if days_input else 30
        except ValueError:
            days = 30
        
        upcoming_renewals = self.subscription_manager.get_upcoming_renewals(days)
        
        if not upcoming_renewals:
            print(f"No renewals scheduled in the next {days} days.")
            return
        
        print(f"Renewals in the next {days} days:")
        print("-" * 30)
        
        for subscription, days_until in upcoming_renewals:
            if days_until < 0:
                status = f"OVERDUE by {abs(days_until)} days"
            elif days_until == 0:
                status = "DUE TODAY"
            else:
                status = f"Due in {days_until} days"
            
            print(f"• {subscription.name} ({subscription.category}) - {format_currency(subscription.cost)} - {status}")
    
    def search_subscriptions(self) -> None:
        """Search subscriptions by name or category."""
        print("\n" + "=" * 40)
        print("SEARCH SUBSCRIPTIONS")
        print("=" * 40)
        
        query = input("Enter search term (name or category): ").strip()
        
        if not query:
            print("Search term cannot be empty.")
            return
        
        results = self.subscription_manager.search_subscriptions(query)
        
        if not results:
            print(f"No subscriptions found matching '{query}'.")
            return
        
        print(f"\nFound {len(results)} subscription(s) matching '{query}':")
        print("-" * 50)
        
        for sub in results:
            formatted_date = format_date(sub.renewal_date, output_format='%Y-%m-%d')
            print(f"ID: {sub.id} | {sub.name} ({sub.category}) | {format_currency(sub.cost)} | {formatted_date}")
    
    def generate_reports(self) -> None:
        """Generate various reports."""
        print("\n" + "=" * 40)
        print("GENERATE REPORTS")
        print("=" * 40)
        
        print("1. Summary Report")
        print("2. Renewal Report")
        print("3. Cost Analysis Chart")
        print("4. Category Comparison Chart")
        print("5. Monthly Trend Chart")
        print("6. Comprehensive Report (All)")
        print("7. Back to Main Menu")
        
        choice = input("\nSelect report type (1-7): ").strip()
        
        try:
            if choice == '1':
                print("\nGenerating summary report...")
                self.report_generator.generate_summary_report()
            elif choice == '2':
                print("\nGenerating renewal report...")
                self.report_generator.generate_renewal_report()
            elif choice == '3':
                print("\nGenerating cost analysis chart...")
                self.report_generator.generate_cost_analysis_chart()
            elif choice == '4':
                print("\nGenerating category comparison chart...")
                self.report_generator.generate_category_comparison_chart()
            elif choice == '5':
                print("\nGenerating monthly trend chart...")
                self.report_generator.generate_monthly_trend_chart()
            elif choice == '6':
                print("\nGenerating comprehensive report...")
                self.report_generator.generate_comprehensive_report()
            elif choice == '7':
                return
            else:
                print("Invalid choice.")
                return
            
            print("\n✅ Report generated successfully!")
            
        except Exception as e:
            print(f"\n❌ Error generating report: {e}")
    
    def run(self) -> None:
        """Run the main application loop."""
        self.display_welcome()
        
        while self.running:
            try:
                self.display_main_menu()
                choice = self.get_user_choice()
                
                if choice == '1':
                    self.add_subscription()
                elif choice == '2':
                    self.list_subscriptions()
                elif choice == '3':
                    self.edit_subscription()
                elif choice == '4':
                    self.delete_subscription()
                elif choice == '5':
                    self.view_total_costs()
                elif choice == '6':
                    self.view_upcoming_renewals()
                elif choice == '7':
                    self.search_subscriptions()
                elif choice == '8':
                    self.generate_reports()
                elif choice == '9':
                    print("\nThank you for using Subscription Manager!")
                    self.running = False
                
                if self.running:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.running = False
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("Press Enter to continue...")


def main():
    """Main entry point for the application."""
    try:
        app = SubscriptionManagerCLI()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# TODO: Add email/SMS renewal reminders (integration idea)
# TODO: Add Pie Chart for category-wise spending in report.py
# TODO: Fix bug: sorting renewals by date sometimes fails if format changes
# TODO: Improve CLI with colored output using rich
# TODO: Add Export to Excel (XLSX) feature
# TODO: Add Login system for multiple users (future extension)
# TODO: Write unit tests for utils.py functions
