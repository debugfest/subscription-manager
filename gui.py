"""
Simple Tkinter GUI for Subscription Manager.

This module provides a basic graphical user interface for the subscription manager.
It's an optional feature that can be used instead of the CLI.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional
import os

from subscription import Subscription, SubscriptionManager
from report import ReportGenerator
from utils import validate_date, parse_cost, format_currency, get_common_categories, get_common_payment_methods


class SubscriptionManagerGUI:
    """Simple Tkinter GUI for the subscription manager."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Subscription Manager")
        self.root.geometry("800x600")
        
        self.subscription_manager = SubscriptionManager()
        self.report_generator = ReportGenerator(self.subscription_manager)
        
        self.setup_ui()
        self.refresh_subscription_list()
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Subscription Manager", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Action buttons
        ttk.Button(buttons_frame, text="Add Subscription", command=self.add_subscription_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Edit Selected", command=self.edit_selected_subscription).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Delete Selected", command=self.delete_selected_subscription).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_subscription_list).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Generate Report", command=self.generate_report_dialog).pack(side=tk.LEFT, padx=(0, 5))
        
        # Subscription list
        list_frame = ttk.LabelFrame(main_frame, text="Subscriptions", padding="5")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for subscription list
        columns = ("ID", "Name", "Category", "Cost", "Renewal Date", "Payment Method")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Cost", text="Monthly Cost")
        self.tree.heading("Renewal Date", text="Renewal Date")
        self.tree.heading("Payment Method", text="Payment Method")
        
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Category", width=100)
        self.tree.column("Cost", width=100)
        self.tree.column("Renewal Date", width=100)
        self.tree.column("Payment Method", width=120)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="Summary", padding="5")
        summary_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.summary_label = ttk.Label(summary_frame, text="")
        self.summary_label.pack()
        
        self.update_summary()
    
    def refresh_subscription_list(self) -> None:
        """Refresh the subscription list display."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add subscriptions
        subscriptions = self.subscription_manager.get_all_subscriptions()
        for sub in subscriptions:
            self.tree.insert("", tk.END, values=(
                sub.id,
                sub.name,
                sub.category,
                format_currency(sub.cost),
                sub.renewal_date,
                sub.payment_method
            ))
        
        self.update_summary()
    
    def update_summary(self) -> None:
        """Update the summary information."""
        total_monthly = self.subscription_manager.get_total_monthly_cost()
        total_annual = self.subscription_manager.get_total_annual_cost()
        count = len(self.subscription_manager.get_all_subscriptions())
        
        summary_text = f"Total Subscriptions: {count} | Monthly Cost: {format_currency(total_monthly)} | Annual Cost: {format_currency(total_annual)}"
        self.summary_label.config(text=summary_text)
    
    def add_subscription_dialog(self) -> None:
        """Open dialog to add a new subscription."""
        dialog = SubscriptionDialog(self.root, "Add Subscription")
        if dialog.result:
            try:
                subscription = dialog.result
                self.subscription_manager.add_subscription(subscription)
                self.refresh_subscription_list()
                messagebox.showinfo("Success", f"Subscription '{subscription.name}' added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add subscription: {e}")
    
    def edit_selected_subscription(self) -> None:
        """Edit the selected subscription."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a subscription to edit.")
            return
        
        item = self.tree.item(selection[0])
        subscription_id = item['values'][0]
        
        subscription = self.subscription_manager.get_subscription_by_id(subscription_id)
        if not subscription:
            messagebox.showerror("Error", "Subscription not found.")
            return
        
        dialog = SubscriptionDialog(self.root, "Edit Subscription", subscription)
        if dialog.result:
            try:
                updated_subscription = dialog.result
                updated_subscription.id = subscription_id
                self.subscription_manager.update_subscription(updated_subscription)
                self.refresh_subscription_list()
                messagebox.showinfo("Success", f"Subscription '{updated_subscription.name}' updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update subscription: {e}")
    
    def delete_selected_subscription(self) -> None:
        """Delete the selected subscription."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a subscription to delete.")
            return
        
        item = self.tree.item(selection[0])
        subscription_id = item['values'][0]
        subscription_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{subscription_name}'?"):
            try:
                if self.subscription_manager.delete_subscription(subscription_id):
                    self.refresh_subscription_list()
                    messagebox.showinfo("Success", f"Subscription '{subscription_name}' deleted successfully!")
                else:
                    messagebox.showerror("Error", "Failed to delete subscription.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete subscription: {e}")
    
    def generate_report_dialog(self) -> None:
        """Open dialog to generate reports."""
        dialog = ReportDialog(self.root, self.report_generator)
        dialog.show()
    
    def run(self) -> None:
        """Run the GUI application."""
        self.root.mainloop()


class SubscriptionDialog:
    """Dialog for adding/editing subscriptions."""
    
    def __init__(self, parent, title: str, subscription: Optional[Subscription] = None):
        """Initialize the dialog."""
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center on parent
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 150
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        self.setup_ui(subscription)
    
    def setup_ui(self, subscription: Optional[Subscription]) -> None:
        """Set up the dialog UI."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=subscription.name if subscription else "")
        name_entry = ttk.Entry(main_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Category
        ttk.Label(main_frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.category_var = tk.StringVar(value=subscription.category if subscription else "")
        category_combo = ttk.Combobox(main_frame, textvariable=self.category_var, width=27)
        category_combo['values'] = get_common_categories()
        category_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Cost
        ttk.Label(main_frame, text="Monthly Cost:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cost_var = tk.StringVar(value=str(subscription.cost) if subscription else "")
        cost_entry = ttk.Entry(main_frame, textvariable=self.cost_var, width=30)
        cost_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Renewal Date
        ttk.Label(main_frame, text="Renewal Date:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.renewal_var = tk.StringVar(value=subscription.renewal_date if subscription else "")
        renewal_entry = ttk.Entry(main_frame, textvariable=self.renewal_var, width=30)
        renewal_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(main_frame, text="(YYYY-MM-DD)", font=("Arial", 8)).grid(row=4, column=1, sticky=tk.W)
        
        # Payment Method
        ttk.Label(main_frame, text="Payment Method:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.payment_var = tk.StringVar(value=subscription.payment_method if subscription else "")
        payment_combo = ttk.Combobox(main_frame, textvariable=self.payment_var, width=27)
        payment_combo['values'] = get_common_payment_methods()
        payment_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def ok_clicked(self) -> None:
        """Handle OK button click."""
        try:
            name = self.name_var.get().strip()
            category = self.category_var.get().strip()
            cost_str = self.cost_var.get().strip()
            renewal_date = self.renewal_var.get().strip()
            payment_method = self.payment_var.get().strip()
            
            # Validate inputs
            if not name:
                messagebox.showerror("Error", "Name is required.")
                return
            
            if not category:
                messagebox.showerror("Error", "Category is required.")
                return
            
            if not cost_str:
                messagebox.showerror("Error", "Cost is required.")
                return
            
            if not renewal_date:
                messagebox.showerror("Error", "Renewal date is required.")
                return
            
            if not payment_method:
                messagebox.showerror("Error", "Payment method is required.")
                return
            
            # Parse cost
            try:
                cost = parse_cost(cost_str)
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid cost: {e}")
                return
            
            # Validate date
            if not validate_date(renewal_date):
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return
            
            # Create subscription
            self.result = Subscription(
                name=name,
                category=category,
                cost=cost,
                renewal_date=renewal_date,
                payment_method=payment_method
            )
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating subscription: {e}")
    
    def cancel_clicked(self) -> None:
        """Handle Cancel button click."""
        self.dialog.destroy()


class ReportDialog:
    """Dialog for generating reports."""
    
    def __init__(self, parent, report_generator: ReportGenerator):
        """Initialize the report dialog."""
        self.report_generator = report_generator
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Generate Reports")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center on parent
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 150
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 100
        self.dialog.geometry(f"300x200+{x}+{y}")
        
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Set up the dialog UI."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Select Report Type:", font=("Arial", 10, "bold")).pack(pady=(0, 10))
        
        # Report buttons
        ttk.Button(main_frame, text="Summary Report", command=self.generate_summary).pack(fill=tk.X, pady=2)
        ttk.Button(main_frame, text="Renewal Report", command=self.generate_renewal).pack(fill=tk.X, pady=2)
        ttk.Button(main_frame, text="Cost Analysis Chart", command=self.generate_cost_chart).pack(fill=tk.X, pady=2)
        ttk.Button(main_frame, text="Category Comparison", command=self.generate_category_chart).pack(fill=tk.X, pady=2)
        ttk.Button(main_frame, text="Comprehensive Report", command=self.generate_comprehensive).pack(fill=tk.X, pady=2)
        
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack(fill=tk.X, pady=(10, 0))
    
    def generate_summary(self) -> None:
        """Generate summary report."""
        try:
            self.report_generator.generate_summary_report()
            messagebox.showinfo("Success", "Summary report generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_renewal(self) -> None:
        """Generate renewal report."""
        try:
            self.report_generator.generate_renewal_report()
            messagebox.showinfo("Success", "Renewal report generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_cost_chart(self) -> None:
        """Generate cost analysis chart."""
        try:
            self.report_generator.generate_cost_analysis_chart()
            messagebox.showinfo("Success", "Cost analysis chart generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart: {e}")
    
    def generate_category_chart(self) -> None:
        """Generate category comparison chart."""
        try:
            self.report_generator.generate_category_comparison_chart()
            messagebox.showinfo("Success", "Category comparison chart generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart: {e}")
    
    def generate_comprehensive(self) -> None:
        """Generate comprehensive report."""
        try:
            self.report_generator.generate_comprehensive_report()
            messagebox.showinfo("Success", "Comprehensive report generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def show(self) -> None:
        """Show the dialog."""
        self.dialog.wait_window()


def main():
    """Main entry point for the GUI application."""
    app = SubscriptionManagerGUI()
    app.run()


if __name__ == "__main__":
    main()
