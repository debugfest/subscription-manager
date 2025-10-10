# 🤝 Contributing to Subscription Manager

Thank you for your interest in contributing to the Subscription Manager! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Contribution Guidelines](#contribution-guidelines)
- [Priority TODOs](#priority-todos)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project follows a code of conduct that ensures a welcoming environment for all contributors. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Basic knowledge of Python, SQLite, and GUI/CLI applications

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/subscription-manager.git
   cd subscription-manager
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/originalowner/subscription-manager.git
   ```

## 🛠️ Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 3. Verify Installation

```bash
# Run the launcher
python launcher.py

# Run CLI directly
python main.py

# Run GUI directly
python gui.py

# Run the demo
python demo.py

# Run tests (if using pytest)
pytest
```

## 📁 Project Structure

```
subscription_manager/
├── main.py              # CLI entry point and user interface
├── gui.py               # Tkinter GUI interface
├── launcher.py          # Interface launcher script
├── subscription.py      # Subscription data model and database operations
├── report.py            # Report generation and visualizations
├── utils.py             # Utility functions and validation
├── demo.py              # Demo script with sample data
├── PROJECT_SUMMARY.md   # Project completion summary
├── data/                # Database storage
│   └── subscriptions.db # SQLite database
├── reports/             # Generated reports
├── tests/               # Test files (to be created)
├── requirements.txt     # Dependencies
├── README.md           # Project documentation
└── CONTRIBUTING.md     # This file
```

### Module Responsibilities

- **`main.py`**: CLI interface, user interaction, menu handling
- **`gui.py`**: Tkinter GUI interface, graphical user interaction
- **`launcher.py`**: Interface selection launcher
- **`subscription.py`**: Subscription data model, database operations, CRUD operations
- **`report.py`**: Chart generation, report creation, matplotlib visualizations
- **`utils.py`**: Validation, formatting, date handling, common utilities
- **`demo.py`**: Demo script demonstrating core functionality

## 📝 Contribution Guidelines

### Types of Contributions

We welcome various types of contributions:

1. **🐛 Bug Fixes**: Fix existing issues and bugs
2. **✨ New Features**: Add new functionality
3. **📚 Documentation**: Improve documentation and examples
4. **🧪 Tests**: Add or improve test coverage
5. **🎨 UI/UX**: Enhance user interface and experience
6. **⚡ Performance**: Optimize code performance
7. **🔧 Refactoring**: Improve code structure and maintainability

### Before You Start

1. **Check existing issues** to see if your idea is already being worked on
2. **Create an issue** for significant changes to discuss the approach
3. **Read the Priority TODOs** section below for high-priority items
4. **Follow the coding standards** outlined in this document

## 🎯 Priority TODOs

These are high-priority items that contributors can work on:

### 🔥 Critical Issues

1. **Write unit tests for utils.py functions**
   - **Files**: Create `tests/test_utils.py`
   - **Description**: Add comprehensive test coverage for utility functions
   - **Priority**: High
   - **Estimated Effort**: 4-6 hours

2. **Add comprehensive test coverage for subscription.py**
   - **Files**: Create `tests/test_subscription.py`
   - **Description**: Add tests for database operations and subscription management
   - **Priority**: High
   - **Estimated Effort**: 6-8 hours

3. **Add test coverage for report.py**
   - **Files**: Create `tests/test_report.py`
   - **Description**: Add tests for report generation and chart creation
   - **Priority**: High
   - **Estimated Effort**: 4-6 hours

4. **Add test coverage for GUI functionality**
   - **Files**: Create `tests/test_gui.py`
   - **Description**: Add tests for GUI components and interactions
   - **Priority**: High
   - **Estimated Effort**: 8-10 hours

### 🚀 New Features

5. **Improve CLI with colored output using rich**
   - **Description**: Enhance CLI with colored output and better formatting
   - **Files**: Update `main.py`, add `rich` dependency
   - **Priority**: High
   - **Estimated Effort**: 4-6 hours
   - **Dependencies**: `rich`

6. **Add Export to Excel (XLSX) feature**
   - **Description**: Export reports and subscription data to Excel format
   - **Files**: New module `export.py`, update `report.py`
   - **Priority**: High
   - **Estimated Effort**: 6-8 hours
   - **Dependencies**: `openpyxl`, `pandas`

7. **Add email/SMS renewal reminders**
   - **Description**: Send renewal reminders via email or SMS
   - **Files**: New module `notifications.py`, update `main.py` and `gui.py`
   - **Priority**: Medium
   - **Estimated Effort**: 10-12 hours
   - **Dependencies**: `smtplib`, `twilio`, `email-validator`

8. **Add web interface using Flask**
   - **Description**: Create a web-based interface using Flask
   - **Files**: New module `web_app.py`, update requirements
   - **Priority**: Medium
   - **Estimated Effort**: 15-20 hours
   - **Dependencies**: `flask`, `flask-sqlalchemy`

9. **Add data backup and restore functionality**
   - **Description**: Backup and restore subscription data
   - **Files**: New module `backup.py`, update `main.py` and `gui.py`
   - **Priority**: Medium
   - **Estimated Effort**: 6-8 hours

10. **Add budget tracking and alerts**
    - **Description**: Set subscription budgets and get alerts when exceeded
    - **Files**: New module `budget.py`, update database schema
    - **Priority**: Medium
    - **Estimated Effort**: 8-10 hours

11. **Add multi-currency support**
    - **Description**: Support different currencies for international users
    - **Files**: Update `subscription.py`, `utils.py`, `report.py`
    - **Priority**: Low
    - **Estimated Effort**: 10-12 hours

12. **Add receipt storage functionality**
    - **Description**: Store subscription receipts and invoices
    - **Files**: New module `receipts.py`, update database schema
    - **Priority**: Low
    - **Estimated Effort**: 12-15 hours

13. **Add cloud sync functionality**
    - **Description**: Sync data across devices
    - **Files**: New module `cloud_sync.py`
    - **Priority**: Low
    - **Estimated Effort**: 15-20 hours
    - **Dependencies**: `requests`, `cryptography`

14. **Add mobile app support**
    - **Description**: Create mobile app using Kivy or similar
    - **Files**: New module `mobile_app.py`
    - **Priority**: Low
    - **Estimated Effort**: 20-25 hours
    - **Dependencies**: `kivy`

## 📏 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all functions, classes, and modules
- Use **descriptive variable names** (avoid abbreviations)
- Keep **line length** under 88 characters (Black formatter standard)

### Code Formatting

We use **Black** for code formatting:

```bash
# Format code
black subscription_manager/

# Check formatting
black --check subscription_manager/
```

### Linting

We use **flake8** for linting:

```bash
# Run linter
flake8 subscription_manager/

# Run with specific rules
flake8 --max-line-length=88 --extend-ignore=E203,W503 subscription_manager/
```

### Type Checking

We use **mypy** for type checking:

```bash
# Run type checker
mypy subscription_manager/
```

### Example Code Style

```python
def add_subscription(self, subscription: Subscription) -> int:
    """
    Add a new subscription to the database.
    
    Args:
        subscription: Subscription object to add
        
    Returns:
        int: ID of the created subscription
        
    Raises:
        ValueError: If subscription data is invalid
    """
    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO subscriptions (name, category, cost, renewal_date, payment_method)
                VALUES (?, ?, ?, ?, ?)
            """, (
                subscription.name,
                subscription.category,
                subscription.cost,
                subscription.renewal_date,
                subscription.payment_method
            ))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise ValueError(f"Database error: {e}")
```

## 🧪 Testing Guidelines

### Test Structure

Create tests in the `tests/` directory:

```
tests/
├── test_subscription.py  # Tests for subscription.py
├── test_report.py        # Tests for report.py
├── test_utils.py         # Tests for utils.py
├── test_gui.py           # Tests for gui.py
├── test_main.py          # Tests for main.py
└── conftest.py           # Pytest configuration
```

### Test Naming Convention

- Test functions should start with `test_`
- Use descriptive names: `test_add_subscription_success`, `test_invalid_cost_raises_error`
- Group related tests in classes: `class TestSubscriptionManager:`

### Example Test

```python
import pytest
from subscription import SubscriptionManager, Subscription

class TestSubscriptionManager:
    """Test cases for SubscriptionManager class."""
    
    def test_add_subscription_success(self):
        """Test successful subscription addition."""
        manager = SubscriptionManager(":memory:")  # Use in-memory database for testing
        subscription = Subscription(
            name="Netflix",
            category="Streaming",
            cost=15.99,
            renewal_date="2024-02-15",
            payment_method="Credit Card"
        )
        
        subscription_id = manager.add_subscription(subscription)
        assert subscription_id is not None
        assert subscription_id > 0
    
    def test_add_subscription_invalid_cost(self):
        """Test subscription addition with invalid cost."""
        manager = SubscriptionManager(":memory:")
        subscription = Subscription(
            name="Netflix",
            category="Streaming",
            cost=-15.99,  # Invalid negative cost
            renewal_date="2024-02-15",
            payment_method="Credit Card"
        )
        
        with pytest.raises(ValueError, match="Cost cannot be negative"):
            manager.add_subscription(subscription)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=subscription_manager --cov-report=html

# Run specific test file
pytest tests/test_subscription.py

# Run with verbose output
pytest -v
```

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Add tests** for new functionality

4. **Update documentation** if needed

5. **Run tests and linting**:
   ```bash
   pytest
   flake8 subscription_manager/
   black --check subscription_manager/
   mypy subscription_manager/
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Template

When creating a PR, include:

- **Description**: What changes were made and why
- **Type**: Bug fix, new feature, documentation, etc.
- **Testing**: How the changes were tested
- **Screenshots**: If applicable (for UI changes)
- **Checklist**: Ensure all items are completed

### PR Checklist

- [ ] Code follows the project's coding standards
- [ ] Self-review of code has been performed
- [ ] Code has been commented, particularly in hard-to-understand areas
- [ ] Tests have been added/updated for new functionality
- [ ] Documentation has been updated if necessary
- [ ] All tests pass
- [ ] No linting errors
- [ ] Type checking passes

## 🐛 Issue Guidelines

### Bug Reports

When reporting bugs, include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the bug
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots** if applicable
6. **Error messages** and stack traces

### Feature Requests

When requesting features, include:

1. **Clear title** describing the feature
2. **Use case** and motivation
3. **Proposed solution** or approach
4. **Alternatives considered**
5. **Additional context** if relevant

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority: high`: High priority issue
- `priority: medium`: Medium priority issue
- `priority: low`: Low priority issue

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version number is updated
- [ ] CHANGELOG.md is updated
- [ ] Release notes are prepared
- [ ] Tag is created
- [ ] Release is published

## 📚 Additional Resources

### Documentation

- [Python Documentation](https://docs.python.org/3/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Rich Documentation](https://rich.readthedocs.io/)

### Development Tools

- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Pytest Testing Framework](https://docs.pytest.org/)

## 💬 Getting Help

If you need help or have questions:

1. **Check existing issues** for similar problems
2. **Read the documentation** and code comments
3. **Create a new issue** with detailed information
4. **Join discussions** in GitHub Discussions
5. **Ask questions** in the community forum

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Project documentation**

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for contributing to the Subscription Manager!** 💳📊

*Together, we can make subscription management more powerful and accessible for everyone!*
