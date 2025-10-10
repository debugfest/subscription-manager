# 💳 Subscription Manager

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-blue.svg)](https://pep8.org)

A comprehensive Python application for managing subscriptions with both CLI and GUI interfaces. Track your monthly subscriptions, monitor renewal dates, analyze costs by category, and generate detailed reports with beautiful visualizations using matplotlib. Perfect for individuals and families who want to take control of their subscription spending.

## ✨ Features

### 💳 **Subscription Management**
- **Add Subscriptions**: Record subscriptions with name, category, cost, renewal date, and payment method
- **Edit Subscriptions**: Modify existing subscription details and information
- **Delete Subscriptions**: Remove subscriptions with confirmation prompts
- **List Subscriptions**: View all subscriptions with filtering and sorting options
- **Search Subscriptions**: Find subscriptions by name or category
- **Data Validation**: Comprehensive input validation for all fields

### 💰 **Cost Tracking & Analytics**
- **Monthly Cost Calculation**: Track total monthly subscription costs
- **Annual Cost Projection**: Calculate yearly subscription spending
- **Category Breakdown**: Analyze spending by subscription categories
- **Cost Trends**: Monitor spending patterns over time
- **Renewal Monitoring**: Track upcoming renewals within configurable timeframes
- **Overdue Alerts**: Identify overdue subscriptions

### 📊 **Reports & Visualizations**
- **Summary Reports**: Comprehensive text-based subscription summaries
- **Renewal Reports**: Detailed upcoming renewal information
- **Cost Analysis Charts**: Pie charts showing category-wise spending
- **Category Comparison Charts**: Bar charts comparing subscription costs
- **Monthly Trend Charts**: Line charts showing cost trends over time
- **Comprehensive Reports**: All reports combined with visualizations
- **Export Capabilities**: Save reports and charts to files

### 🖥️ **Multiple Interfaces**
- **CLI Interface**: Full-featured command-line interface for power users
- **GUI Interface**: User-friendly Tkinter-based graphical interface
- **Launcher Script**: Easy interface selection between CLI and GUI
- **Demo Script**: Sample data and feature demonstration

### 🔍 **Search & Filter**
- **Advanced Search**: Find subscriptions by name or category
- **Category Filtering**: View subscriptions by specific categories
- **Renewal Filtering**: Filter by upcoming renewals
- **Cost Filtering**: Find high or low-cost subscriptions
- **Flexible Sorting**: Sort by name, cost, renewal date, or category

### 🏗️ **Technical Features**
- **SQLite Database**: Reliable local storage with automatic table creation
- **Modular Design**: Clean separation of concerns across modules
- **Type Hints**: Full type annotation support for better code quality
- **PEP 8 Compliance**: Follows Python style guidelines
- **Error Handling**: Graceful failure modes and user-friendly error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/subscription-manager.git
   cd subscription-manager
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   # Use the launcher to choose interface
   python launcher.py
   
   # Or run directly
   python main.py          # CLI interface
   python gui.py           # GUI interface
   ```

### Demo

Try the demo to see the application in action:

```bash
python demo.py
```

## 📖 Usage Guide

### Interface Selection

The application offers two interfaces:

1. **CLI Interface** (`main.py`): Command-line interface for power users
2. **GUI Interface** (`gui.py`): Graphical interface for easy use
3. **Launcher** (`launcher.py`): Choose your preferred interface

### CLI Interface

The CLI features an intuitive menu system:

```
1. Add new subscription      - Add a new subscription
2. List all subscriptions    - View all subscriptions
3. Edit subscription         - Modify existing subscription
4. Delete subscription       - Remove a subscription
5. View total costs          - See cost summaries
6. View upcoming renewals    - Check renewal dates
7. Search subscriptions      - Find specific subscriptions
8. Generate reports          - Create detailed reports
9. Exit                     - Close the application
```

### Adding a Subscription

1. Select "Add new subscription" from the menu
2. Enter the required information:
   - **Name**: Subscription name (e.g., "Netflix", "Spotify Premium")
   - **Category**: Subscription category (e.g., "Streaming", "Music", "Software")
   - **Monthly Cost**: Cost per month (supports various formats)
   - **Renewal Date**: Next renewal date (YYYY-MM-DD format)
   - **Payment Method**: How you pay (e.g., "Credit Card", "PayPal")

### GUI Interface

The GUI provides a user-friendly interface with:
- **Subscription List**: View all subscriptions in a table
- **Add/Edit/Delete**: Buttons for subscription management
- **Summary Panel**: Real-time cost and renewal information
- **Report Generation**: Generate reports with one click

### Generating Reports

1. Select "Generate reports" from the menu
2. Choose from various report types:
   - Summary Report
   - Renewal Report
   - Cost Analysis Chart
   - Category Comparison Chart
   - Monthly Trend Chart
   - Comprehensive Report (all reports combined)

### Searching Subscriptions

1. Select "Search subscriptions" from the menu
2. Choose search criteria:
   - Search by name
   - Search by category
   - Filter by upcoming renewals
   - Filter by cost range

## 🏗️ Project Structure

```
subscription_manager/
├── main.py              # CLI entry point and user interface
├── gui.py               # Tkinter GUI interface
├── launcher.py          # Interface launcher script
├── subscription.py      # Subscription data model and database operations
├── report.py            # Report generation and matplotlib visualizations
├── utils.py             # Utility functions, validation, and formatting
├── demo.py              # Demo script with sample data
├── PROJECT_SUMMARY.md   # Project completion summary
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── CONTRIBUTING.md     # Contribution guidelines
├── data/
│   └── subscriptions.db # SQLite database (auto-created)
└── reports/            # Generated reports and charts
```

## 🔧 API Reference

### Core Classes

#### `Subscription`
Data class representing a subscription.

```python
from subscription import Subscription

subscription = Subscription(
    name="Netflix",
    category="Streaming",
    cost=15.99,
    renewal_date="2024-02-15",
    payment_method="Credit Card"
)
```

#### `SubscriptionManager`
Manages subscription data and database operations.

```python
from subscription import SubscriptionManager

manager = SubscriptionManager()
subscription_id = manager.add_subscription(subscription)
subscriptions = manager.get_all_subscriptions()
total_cost = manager.get_total_monthly_cost()
```

#### `ReportGenerator`
Generates reports and visualizations.

```python
from report import ReportGenerator

reports = ReportGenerator(manager)
reports.generate_summary_report()
reports.generate_cost_analysis_chart()
reports.generate_comprehensive_report()
```

### Key Methods

#### Subscription Management
- `add_subscription(subscription)` - Add new subscription
- `get_all_subscriptions()` - Retrieve all subscriptions
- `get_subscription_by_id(id)` - Get subscription by ID
- `update_subscription(id, subscription)` - Update existing subscription
- `delete_subscription(id)` - Remove subscription by ID
- `search_subscriptions(query, search_type)` - Search subscriptions

#### Cost Analytics
- `get_total_monthly_cost()` - Get total monthly cost
- `get_total_annual_cost()` - Get total annual cost
- `get_cost_by_category()` - Get costs by category
- `get_upcoming_renewals(days)` - Get upcoming renewals
- `get_overdue_subscriptions()` - Get overdue subscriptions

#### Report Generation
- `generate_summary_report()` - Comprehensive summary report
- `generate_renewal_report()` - Upcoming renewals report
- `generate_cost_analysis_chart()` - Category cost pie chart
- `generate_category_comparison_chart()` - Category comparison bar chart
- `generate_monthly_trend_chart()` - Monthly cost trend line chart
- `generate_comprehensive_report()` - All reports combined

### Utility Functions

```python
from utils import validate_date, parse_cost, format_currency

# Validate date input
is_valid = validate_date("2024-02-15")  # True

# Parse cost string
cost = parse_cost("$15.99")  # 15.99

# Format currency
formatted = format_currency(15.99)  # "$15.99"
```

## 🧪 Testing

### Running Tests

```bash
# Run the demo script
python demo.py

# Install test dependencies (if using pytest)
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=subscription_manager
```

### Test Structure

The project includes a comprehensive demo script (`demo.py`) that demonstrates:
- Database initialization
- Adding sample subscriptions
- Retrieving and filtering data
- Generating reports and charts
- Error handling scenarios

## 🐛 Troubleshooting

### Common Issues

#### Database Permission Error
```bash
# Ensure write permissions in the project directory
chmod 755 data/
```

#### Matplotlib Display Issues
```bash
# Install additional dependencies
pip install matplotlib[all]

# On Linux, you might need:
sudo apt-get install python3-tk
```

#### GUI Not Displaying
```bash
# Ensure Tkinter is installed
# On Ubuntu/Debian:
sudo apt-get install python3-tk

# On macOS (usually pre-installed):
# No additional steps needed

# On Windows (usually pre-installed):
# No additional steps needed
```

#### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

### Error Messages

| Error | Solution |
|-------|----------|
| `Cost cannot be negative` | Enter a positive cost value |
| `Invalid renewal date format` | Use YYYY-MM-DD format (e.g., 2024-02-15) |
| `Invalid name` | Provide a valid subscription name (2-100 characters) |
| `Invalid category` | Provide a valid category (2-50 characters) |

## 🔮 Roadmap

### Planned Features

- [ ] **Rich CLI Interface**: Enhanced CLI with colored output using Rich library
- [ ] **Export to Excel**: Export reports to Excel (XLSX) format
- [ ] **Email/SMS Reminders**: Send renewal reminders via email or SMS
- [ ] **Web Interface**: Flask-based web application
- [ ] **Mobile App**: Cross-platform mobile support
- [ ] **Cloud Sync**: Sync data across devices
- [ ] **Budget Tracking**: Set subscription budgets and alerts
- [ ] **Receipt Storage**: Store subscription receipts and invoices
- [ ] **Multi-Currency Support**: Support for different currencies
- [ ] **Advanced Analytics**: Machine learning insights and predictions

### Known Issues

- [ ] Limited chart customization options
- [ ] No support for recurring subscriptions with different frequencies
- [ ] Basic error handling for some edge cases
- [ ] No data backup/restore functionality

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Matplotlib](https://matplotlib.org/) for data visualization
- [SQLite](https://www.sqlite.org/) for data persistence
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for GUI interface
- The Python community for excellent libraries and tools

## 📞 Support

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/yourusername/subscription-manager/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/yourusername/subscription-manager/discussions)

## 📊 Project Statistics

- **Lines of Code**: ~2,500+
- **Test Coverage**: 80%+ (target)
- **Dependencies**: 2 core, 8 optional
- **Python Version**: 3.8+
- **Database**: SQLite
- **UI Frameworks**: CLI + Tkinter GUI

## 💡 Example Usage

### Sample Data
The application comes with sample data including:
- Streaming services (Netflix, Spotify, Disney+)
- Software subscriptions (Adobe Creative Cloud, Microsoft 365)
- Cloud storage (Dropbox, Google Drive)
- News & media (The New York Times, Medium)
- Productivity tools (Slack, Zoom)

### Sample Output
```
SUBSCRIPTION MANAGER - SUMMARY REPORT
============================================================
Generated on: January 15, 2024 at 02:30 PM

OVERVIEW
--------------------
Total Subscriptions: 6
Total Monthly Cost: $112.95
Total Annual Cost: $1,355.40

COST BY CATEGORY
--------------------
Software: $52.99 (46.9%)
Streaming: $15.99 (14.2%)
News & Media: $17.00 (15.1%)
Music: $9.99 (8.8%)
Cloud Storage: $9.99 (8.8%)
Productivity: $6.99 (6.2%)

UPCOMING RENEWALS (Next 30 Days)
-----------------------------------
Spotify Premium - 5 days - $9.99
The New York Times - 21 days - $17.00
Netflix - 31 days - $15.99

ALL SUBSCRIPTIONS
--------------------
Adobe Creative Cloud (Software) - $52.99/month - Renews in 47 days
Dropbox Plus (Cloud Storage) - $9.99/month - Renews in 25 days
Microsoft 365 (Productivity) - $6.99/month - Renews in 44 days
Netflix (Streaming) - $15.99/month - Renews in 31 days
Spotify Premium (Music) - $9.99/month - Renews in 5 days
The New York Times (News & Media) - $17.00/month - Renews in 21 days
```

---

**Made with ❤️ for subscription management**

*Start managing your subscriptions and take control of your spending today!* 💳📊