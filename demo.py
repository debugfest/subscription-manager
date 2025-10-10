#!/usr/bin/env python3
"""
Demo script for Subscription Manager.

This script demonstrates the functionality of the subscription manager
by adding some sample data and generating reports.
"""

from subscription import Subscription, SubscriptionManager
from report import ReportGenerator
from utils import get_current_date_string


def create_sample_data():
    """Create sample subscription data for demonstration."""
    manager = SubscriptionManager()
    
    # Sample subscriptions
    sample_subscriptions = [
        Subscription(
            name="Netflix",
            category="Streaming",
            cost=15.99,
            renewal_date="2024-02-15",
            payment_method="Credit Card"
        ),
        Subscription(
            name="Spotify Premium",
            category="Music",
            cost=9.99,
            renewal_date="2024-01-20",
            payment_method="PayPal"
        ),
        Subscription(
            name="Adobe Creative Cloud",
            category="Software",
            cost=52.99,
            renewal_date="2024-03-01",
            payment_method="Credit Card"
        ),
        Subscription(
            name="Microsoft 365",
            category="Productivity",
            cost=6.99,
            renewal_date="2024-02-28",
            payment_method="Bank Transfer"
        ),
        Subscription(
            name="Dropbox Plus",
            category="Cloud Storage",
            cost=9.99,
            renewal_date="2024-01-10",
            payment_method="Credit Card"
        ),
        Subscription(
            name="The New York Times",
            category="News & Media",
            cost=17.00,
            renewal_date="2024-02-05",
            payment_method="Credit Card"
        )
    ]
    
    print("Adding sample subscriptions...")
    for subscription in sample_subscriptions:
        try:
            subscription_id = manager.add_subscription(subscription)
            print(f"✅ Added {subscription.name} (ID: {subscription_id})")
        except Exception as e:
            print(f"❌ Failed to add {subscription.name}: {e}")
    
    return manager


def demonstrate_features(manager):
    """Demonstrate various features of the subscription manager."""
    print("\n" + "="*60)
    print("SUBSCRIPTION MANAGER DEMONSTRATION")
    print("="*60)
    
    # List all subscriptions
    print("\n1. ALL SUBSCRIPTIONS:")
    print("-" * 30)
    subscriptions = manager.get_all_subscriptions()
    for sub in subscriptions:
        print(f"• {sub.name} ({sub.category}) - ${sub.cost:.2f}/month")
    
    # Total costs
    print(f"\n2. COST SUMMARY:")
    print("-" * 20)
    total_monthly = manager.get_total_monthly_cost()
    total_annual = manager.get_total_annual_cost()
    print(f"Total Monthly Cost: ${total_monthly:.2f}")
    print(f"Total Annual Cost: ${total_annual:.2f}")
    
    # Cost by category
    print(f"\n3. COST BY CATEGORY:")
    print("-" * 25)
    cost_by_category = manager.get_cost_by_category()
    for category, cost in sorted(cost_by_category.items(), key=lambda x: x[1], reverse=True):
        percentage = (cost / total_monthly * 100) if total_monthly > 0 else 0
        print(f"{category}: ${cost:.2f} ({percentage:.1f}%)")
    
    # Upcoming renewals
    print(f"\n4. UPCOMING RENEWALS (Next 30 days):")
    print("-" * 40)
    upcoming = manager.get_upcoming_renewals(30)
    if upcoming:
        for subscription, days_until in upcoming:
            status = "OVERDUE" if days_until < 0 else f"{days_until} days"
            print(f"• {subscription.name} - {status} - ${subscription.cost:.2f}")
    else:
        print("No renewals in the next 30 days.")
    
    # Search functionality
    print(f"\n5. SEARCH EXAMPLE (searching for 'cloud'):")
    print("-" * 45)
    search_results = manager.search_subscriptions("cloud")
    for sub in search_results:
        print(f"• {sub.name} ({sub.category}) - ${sub.cost:.2f}")


def generate_sample_reports(manager):
    """Generate sample reports."""
    print(f"\n6. GENERATING REPORTS:")
    print("-" * 25)
    
    report_generator = ReportGenerator(manager)
    
    try:
        print("Generating summary report...")
        report_generator.generate_summary_report()
        print("✅ Summary report generated")
        
        print("Generating renewal report...")
        report_generator.generate_renewal_report()
        print("✅ Renewal report generated")
        
        print("Generating cost analysis chart...")
        report_generator.generate_cost_analysis_chart()
        print("✅ Cost analysis chart generated")
        
        print("Generating category comparison chart...")
        report_generator.generate_category_comparison_chart()
        print("✅ Category comparison chart generated")
        
        print("\nAll reports saved to the 'reports/' directory!")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")


def main():
    """Main demonstration function."""
    print("Subscription Manager Demo")
    print("This demo will create sample data and demonstrate features.")
    
    try:
        # Create sample data
        manager = create_sample_data()
        
        # Demonstrate features
        demonstrate_features(manager)
        
        # Generate reports
        generate_sample_reports(manager)
        
        print(f"\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("You can now:")
        print("• Run 'python main.py' for the CLI interface")
        print("• Run 'python gui.py' for the GUI interface")
        print("• Check the 'reports/' directory for generated files")
        print("• Check the 'data/' directory for the database")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    main()
