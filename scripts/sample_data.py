"""
Sample data generator for the Flask Order Management System
Run this script to populate the system with sample orders for testing
"""

import json
import os
from datetime import datetime, timedelta
import random

# Sample data
SAMPLE_SENDERS = [
    "John Smith", "Sarah Johnson", "Mike Wilson", "Emily Davis", 
    "David Brown", "Lisa Anderson", "Tom Miller", "Anna Garcia"
]

SAMPLE_RECIPIENTS = [
    "Alice Cooper", "Bob Martinez", "Carol White", "Daniel Lee",
    "Eva Thompson", "Frank Harris", "Grace Clark", "Henry Lewis"
]

SAMPLE_ADDRESSES = [
    "123 Main St, New York, NY 10001",
    "456 Oak Ave, Los Angeles, CA 90210",
    "789 Pine Rd, Chicago, IL 60601",
    "321 Elm St, Houston, TX 77001",
    "654 Maple Dr, Phoenix, AZ 85001",
    "987 Cedar Ln, Philadelphia, PA 19101",
    "147 Birch Way, San Antonio, TX 78201",
    "258 Spruce Ct, San Diego, CA 92101"
]

def generate_sample_orders(num_orders=10):
    """Generate sample orders for testing"""
    orders = {}
    logs = []
    
    for i in range(1, num_orders + 1):
        order_id = f"ORD{i:03d}"
        
        # Random delivery date (1-30 days from now)
        delivery_date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        
        # Random status (80% ongoing, 20% delivered)
        status = "Delivered" if random.random() < 0.2 else "Ongoing"
        
        order = {
            "order_id": order_id,
            "num_items": random.randint(1, 10),
            "delivery_date": delivery_date,
            "sender_name": random.choice(SAMPLE_SENDERS),
            "recipient_name": random.choice(SAMPLE_RECIPIENTS),
            "recipient_address": random.choice(SAMPLE_ADDRESSES),
            "status": status,
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat()
        }
        
        if status == "Delivered":
            order["delivered_at"] = (datetime.now() - timedelta(days=random.randint(0, 3))).isoformat()
        
        orders[order_id] = order
        
        # Create log entry for order creation
        log_entry = {
            "action_type": "Created",
            "performed_by": "Sample Data Generator",
            "timestamp": order["created_at"],
            "order_id": order_id,
            "details": f"Sample order created with {order['num_items']} items"
        }
        logs.append(log_entry)
        
        # Add delivery log if delivered
        if status == "Delivered":
            delivery_log = {
                "action_type": "Marked Delivered",
                "performed_by": "Sample Data Generator",
                "timestamp": order["delivered_at"],
                "order_id": order_id,
                "details": "Sample order marked as delivered"
            }
            logs.append(delivery_log)
    
    return orders, logs

def save_sample_data():
    """Save sample data to JSON files"""
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate sample data
    orders, logs = generate_sample_orders(15)
    
    # Save orders
    with open('data/orders.json', 'w') as f:
        json.dump(orders, f, indent=2)
    
    # Save logs
    with open('data/action_logs.json', 'w') as f:
        json.dump(logs, f, indent=2)
    
    print(f"✅ Generated {len(orders)} sample orders")
    print(f"✅ Generated {len(logs)} action log entries")
    print("✅ Sample data saved to data/ directory")
    print("\nSample orders created:")
    for order_id, order in orders.items():
        print(f"  {order_id}: {order['num_items']} items for {order['recipient_name']} - {order['status']}")

if __name__ == "__main__":
    save_sample_data()
