"""
Report generation module for subscription manager.

This module handles generating various reports including summaries,
renewal reports, and visualizations using matplotlib.
"""

import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Wedge
import numpy as np

from subscription import Subscription, SubscriptionManager
from utils import format_currency, format_date, calculate_days_until_renewal


class ReportGenerator:
    """Generates various reports and visualizations for subscriptions."""
    
    def __init__(self, subscription_manager: SubscriptionManager):
        """
        Initialize the report generator.
        
        Args:
            subscription_manager: SubscriptionManager instance
        """
        self.subscription_manager = subscription_manager
        self._ensure_reports_directory()
    
    def _ensure_reports_directory(self) -> None:
        """Ensure the reports directory exists."""
        os.makedirs("reports", exist_ok=True)
    
    def generate_summary_report(self, save_to_file: bool = True) -> str:
        """
        Generate a comprehensive summary report.
        
        Args:
            save_to_file: Whether to save the report to a file
            
        Returns:
            str: Generated report content
        """
        subscriptions = self.subscription_manager.get_all_subscriptions()
        total_monthly = self.subscription_manager.get_total_monthly_cost()
        total_annual = self.subscription_manager.get_total_annual_cost()
        cost_by_category = self.subscription_manager.get_cost_by_category()
        upcoming_renewals = self.subscription_manager.get_upcoming_renewals(30)
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("SUBSCRIPTION MANAGER - SUMMARY REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        report_lines.append("")
        
        # Overview section
        report_lines.append("OVERVIEW")
        report_lines.append("-" * 20)
        report_lines.append(f"Total Subscriptions: {len(subscriptions)}")
        report_lines.append(f"Total Monthly Cost: {format_currency(total_monthly)}")
        report_lines.append(f"Total Annual Cost: {format_currency(total_annual)}")
        report_lines.append("")
        
        # Cost by category
        if cost_by_category:
            report_lines.append("COST BY CATEGORY")
            report_lines.append("-" * 20)
            for category, cost in sorted(cost_by_category.items(), key=lambda x: x[1], reverse=True):
                percentage = (cost / total_monthly * 100) if total_monthly > 0 else 0
                report_lines.append(f"{category}: {format_currency(cost)} ({percentage:.1f}%)")
            report_lines.append("")
        
        # Upcoming renewals
        if upcoming_renewals:
            report_lines.append("UPCOMING RENEWALS (Next 30 Days)")
            report_lines.append("-" * 35)
            for subscription, days_until in upcoming_renewals:
                status = "OVERDUE" if days_until < 0 else f"{days_until} days"
                report_lines.append(f"{subscription.name} - {status} - {format_currency(subscription.cost)}")
            report_lines.append("")
        
        # All subscriptions
        if subscriptions:
            report_lines.append("ALL SUBSCRIPTIONS")
            report_lines.append("-" * 20)
            for sub in sorted(subscriptions, key=lambda x: x.name):
                days_until = calculate_days_until_renewal(sub.renewal_date)
                status = "OVERDUE" if days_until < 0 else f"{days_until} days"
                report_lines.append(f"{sub.name} ({sub.category}) - {format_currency(sub.cost)}/month - Renews in {status}")
        
        report_content = "\n".join(report_lines)
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/summary_report_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write(report_content)
            print(f"Summary report saved to: {filename}")
        
        return report_content
    
    def generate_renewal_report(self, days_ahead: int = 30, save_to_file: bool = True) -> str:
        """
        Generate a detailed renewal report.
        
        Args:
            days_ahead: Number of days to look ahead for renewals
            save_to_file: Whether to save the report to a file
            
        Returns:
            str: Generated report content
        """
        upcoming_renewals = self.subscription_manager.get_upcoming_renewals(days_ahead)
        all_subscriptions = self.subscription_manager.get_all_subscriptions()
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append(f"RENEWAL REPORT - NEXT {days_ahead} DAYS")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        report_lines.append("")
        
        if not upcoming_renewals:
            report_lines.append(f"No renewals scheduled in the next {days_ahead} days.")
        else:
            # Group by days until renewal
            grouped_renewals = {}
            for subscription, days_until in upcoming_renewals:
                if days_until not in grouped_renewals:
                    grouped_renewals[days_until] = []
                grouped_renewals[days_until].append(subscription)
            
            # Sort by days (overdue first, then ascending)
            for days_until in sorted(grouped_renewals.keys()):
                subscriptions = grouped_renewals[days_until]
                total_cost = sum(sub.cost for sub in subscriptions)
                
                if days_until < 0:
                    report_lines.append(f"OVERDUE BY {abs(days_until)} DAYS")
                elif days_until == 0:
                    report_lines.append("DUE TODAY")
                else:
                    report_lines.append(f"DUE IN {days_until} DAYS")
                
                report_lines.append("-" * 20)
                for sub in subscriptions:
                    report_lines.append(f"  • {sub.name} ({sub.category}) - {format_currency(sub.cost)}")
                report_lines.append(f"  Total: {format_currency(total_cost)}")
                report_lines.append("")
        
        # Summary statistics
        total_upcoming_cost = sum(sub.cost for sub, _ in upcoming_renewals)
        report_lines.append("SUMMARY")
        report_lines.append("-" * 10)
        report_lines.append(f"Total subscriptions due: {len(upcoming_renewals)}")
        report_lines.append(f"Total cost due: {format_currency(total_upcoming_cost)}")
        
        report_content = "\n".join(report_lines)
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/renewal_report_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write(report_content)
            print(f"Renewal report saved to: {filename}")
        
        return report_content
    
    def generate_cost_analysis_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a pie chart showing cost distribution by category.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        cost_by_category = self.subscription_manager.get_cost_by_category()
        
        if not cost_by_category:
            print("No subscription data available for chart generation.")
            return None
        
        # Prepare data
        categories = list(cost_by_category.keys())
        costs = list(cost_by_category.values())
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        
        wedges, texts, autotexts = plt.pie(
            costs,
            labels=categories,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Customize the chart
        plt.title('Subscription Costs by Category', fontsize=16, fontweight='bold')
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/cost_analysis_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Cost analysis chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_monthly_trend_chart(self, months: int = 12, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a line chart showing monthly cost trends.
        
        Args:
            months: Number of months to show in the trend
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        # This is a simplified version - in a real app, you'd track historical data
        current_cost = self.subscription_manager.get_total_monthly_cost()
        
        # Generate mock trend data (in a real app, this would come from historical data)
        dates = []
        costs = []
        
        for i in range(months):
            month_date = date.today().replace(day=1) - timedelta(days=30 * i)
            dates.append(month_date)
            # Simulate some variation in costs
            variation = current_cost * (0.9 + 0.2 * np.random.random())
            costs.append(variation)
        
        dates.reverse()
        costs.reverse()
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, costs, marker='o', linewidth=2, markersize=6)
        plt.title('Monthly Subscription Cost Trend', fontsize=16, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Monthly Cost ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/monthly_trend_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Monthly trend chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_category_comparison_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a bar chart comparing costs across categories.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        cost_by_category = self.subscription_manager.get_cost_by_category()
        
        if not cost_by_category:
            print("No subscription data available for chart generation.")
            return None
        
        # Sort categories by cost
        sorted_categories = sorted(cost_by_category.items(), key=lambda x: x[1], reverse=True)
        categories = [item[0] for item in sorted_categories]
        costs = [item[1] for item in sorted_categories]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(categories, costs, color=plt.cm.viridis(np.linspace(0, 1, len(categories))))
        
        # Add value labels on bars
        for bar, cost in zip(bars, costs):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'${cost:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Subscription Costs by Category', fontsize=16, fontweight='bold')
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Monthly Cost ($)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/category_comparison_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Category comparison chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_comprehensive_report(self, save_to_file: bool = True) -> str:
        """
        Generate a comprehensive report with all available data and charts.
        
        Args:
            save_to_file: Whether to save the report and charts to files
            
        Returns:
            str: Generated report content
        """
        print("Generating comprehensive report...")
        
        # Generate text reports
        summary_report = self.generate_summary_report(save_to_file)
        renewal_report = self.generate_renewal_report(save_to_file=save_to_file)
        
        # Generate charts
        if save_to_file:
            print("Generating charts...")
            self.generate_cost_analysis_chart(save_to_file=True)
            self.generate_category_comparison_chart(save_to_file=True)
            self.generate_monthly_trend_chart(save_to_file=True)
        
        # Combine reports
        comprehensive_content = []
        comprehensive_content.append("COMPREHENSIVE SUBSCRIPTION REPORT")
        comprehensive_content.append("=" * 50)
        comprehensive_content.append("")
        comprehensive_content.append(summary_report)
        comprehensive_content.append("")
        comprehensive_content.append("=" * 50)
        comprehensive_content.append("")
        comprehensive_content.append(renewal_report)
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/comprehensive_report_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write("\n".join(comprehensive_content))
            print(f"Comprehensive report saved to: {filename}")
        
        return "\n".join(comprehensive_content)


# TODO: Add email/SMS renewal reminders (integration idea)
# TODO: Add Pie Chart for category-wise spending in report.py
# TODO: Fix bug: sorting renewals by date sometimes fails if format changes
# TODO: Improve CLI with colored output using rich
# TODO: Add Export to Excel (XLSX) feature
# TODO: Add Login system for multiple users (future extension)
# TODO: Write unit tests for utils.py functions
