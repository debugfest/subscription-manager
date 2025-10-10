"""
Subscription data model and database operations.

This module handles all subscription-related data operations including
CRUD operations, database management, and data validation.
"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from utils import validate_date, format_date, calculate_days_until_renewal


@dataclass
class Subscription:
    """Data class representing a subscription."""
    id: Optional[int] = None
    name: str = ""
    category: str = ""
    cost: float = 0.0
    renewal_date: str = ""
    payment_method: str = ""

    def __post_init__(self):
        """Validate data after initialization."""
        if self.cost < 0:
            raise ValueError("Cost cannot be negative")
        if not validate_date(self.renewal_date):
            raise ValueError("Invalid renewal date format")


class SubscriptionManager:
    """Manages subscription data and database operations."""
    
    def __init__(self, db_path: str = "data/subscriptions.db"):
        """Initialize the subscription manager with database path."""
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with subscriptions table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subscriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    cost REAL NOT NULL,
                    renewal_date TEXT NOT NULL,
                    payment_method TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
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
    
    def get_all_subscriptions(self) -> List[Subscription]:
        """
        Retrieve all subscriptions from the database.
        
        Returns:
            List[Subscription]: List of all subscriptions
        """
        subscriptions = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM subscriptions ORDER BY name")
                rows = cursor.fetchall()
                
                for row in rows:
                    subscription = Subscription(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        cost=row[3],
                        renewal_date=row[4],
                        payment_method=row[5]
                    )
                    subscriptions.append(subscription)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return subscriptions
    
    def get_subscription_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """
        Retrieve a subscription by its ID.
        
        Args:
            subscription_id: ID of the subscription to retrieve
            
        Returns:
            Optional[Subscription]: Subscription object or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM subscriptions WHERE id = ?", (subscription_id,))
                row = cursor.fetchone()
                
                if row:
                    return Subscription(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        cost=row[3],
                        renewal_date=row[4],
                        payment_method=row[5]
                    )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return None
    
    def update_subscription(self, subscription: Subscription) -> bool:
        """
        Update an existing subscription.
        
        Args:
            subscription: Subscription object with updated data
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        if not subscription.id:
            raise ValueError("Subscription ID is required for update")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE subscriptions 
                    SET name = ?, category = ?, cost = ?, renewal_date = ?, payment_method = ?
                    WHERE id = ?
                """, (
                    subscription.name,
                    subscription.category,
                    subscription.cost,
                    subscription.renewal_date,
                    subscription.payment_method,
                    subscription.id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def delete_subscription(self, subscription_id: int) -> bool:
        """
        Delete a subscription by ID.
        
        Args:
            subscription_id: ID of the subscription to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM subscriptions WHERE id = ?", (subscription_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_subscriptions_by_category(self, category: str) -> List[Subscription]:
        """
        Get all subscriptions in a specific category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List[Subscription]: List of subscriptions in the category
        """
        subscriptions = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM subscriptions WHERE category = ? ORDER BY name", (category,))
                rows = cursor.fetchall()
                
                for row in rows:
                    subscription = Subscription(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        cost=row[3],
                        renewal_date=row[4],
                        payment_method=row[5]
                    )
                    subscriptions.append(subscription)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return subscriptions
    
    def get_upcoming_renewals(self, days: int = 30) -> List[Tuple[Subscription, int]]:
        """
        Get subscriptions with renewals coming up within specified days.
        
        Args:
            days: Number of days to look ahead (default: 30)
            
        Returns:
            List[Tuple[Subscription, int]]: List of tuples containing subscription and days until renewal
        """
        upcoming = []
        subscriptions = self.get_all_subscriptions()
        
        for subscription in subscriptions:
            days_until = calculate_days_until_renewal(subscription.renewal_date)
            if 0 <= days_until <= days:
                upcoming.append((subscription, days_until))
        
        # Sort by days until renewal (ascending)
        upcoming.sort(key=lambda x: x[1])
        return upcoming
    
    def get_total_monthly_cost(self) -> float:
        """
        Calculate total monthly cost of all subscriptions.
        
        Returns:
            float: Total monthly cost
        """
        subscriptions = self.get_all_subscriptions()
        return sum(subscription.cost for subscription in subscriptions)
    
    def get_total_annual_cost(self) -> float:
        """
        Calculate total annual cost of all subscriptions.
        
        Returns:
            float: Total annual cost
        """
        return self.get_total_monthly_cost() * 12
    
    def get_cost_by_category(self) -> Dict[str, float]:
        """
        Calculate total cost grouped by category.
        
        Returns:
            Dict[str, float]: Dictionary with category as key and total cost as value
        """
        cost_by_category = {}
        subscriptions = self.get_all_subscriptions()
        
        for subscription in subscriptions:
            if subscription.category in cost_by_category:
                cost_by_category[subscription.category] += subscription.cost
            else:
                cost_by_category[subscription.category] = subscription.cost
        
        return cost_by_category
    
    def search_subscriptions(self, query: str) -> List[Subscription]:
        """
        Search subscriptions by name or category.
        
        Args:
            query: Search query string
            
        Returns:
            List[Subscription]: List of matching subscriptions
        """
        results = []
        query_lower = query.lower()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM subscriptions 
                    WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ?
                    ORDER BY name
                """, (f"%{query_lower}%", f"%{query_lower}%"))
                rows = cursor.fetchall()
                
                for row in rows:
                    subscription = Subscription(
                        id=row[0],
                        name=row[1],
                        category=row[2],
                        cost=row[3],
                        renewal_date=row[4],
                        payment_method=row[5]
                    )
                    results.append(subscription)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return results


# TODO: Add email/SMS renewal reminders (integration idea)
# TODO: Add Login system for multiple users (future extension)
# TODO: Write unit tests for utils.py functions
