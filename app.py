from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json
import os
from typing import Dict, List, Any

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Data storage (in production, use a proper database)
ORDERS_FILE = 'data/orders.json'
LOGS_FILE = 'data/action_logs.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

class OrderManager:
    def __init__(self):
        self.orders = self.load_orders()
        self.logs = self.load_logs()
    
    def load_orders(self) -> Dict[str, Any]:
        """Load orders from JSON file"""
        try:
            if os.path.exists(ORDERS_FILE):
                with open(ORDERS_FILE, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading orders: {e}")
            return {}
    
    def save_orders(self):
        """Save orders to JSON file"""
        try:
            with open(ORDERS_FILE, 'w') as f:
                json.dump(self.orders, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving orders: {e}")
    
    def load_logs(self) -> List[Dict[str, Any]]:
        """Load action logs from JSON file"""
        try:
            if os.path.exists(LOGS_FILE):
                with open(LOGS_FILE, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading logs: {e}")
            return []
    
    def save_logs(self):
        """Save action logs to JSON file"""
        try:
            with open(LOGS_FILE, 'w') as f:
                json.dump(self.logs, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving logs: {e}")
    
    def log_action(self, action_type: str, performed_by: str, order_id: str = None, details: str = ""):
        """Log an action with timestamp"""
        log_entry = {
            'action_type': action_type,
            'performed_by': performed_by,
            'timestamp': datetime.now().isoformat(),
            'order_id': order_id,
            'details': details
        }
        self.logs.append(log_entry)
        self.save_logs()
        print(f"📝 LOG: {action_type} - {order_id or 'N/A'} by {performed_by}")
    
    def generate_order_id(self) -> str:
        """Generate unique order ID"""
        if not self.orders:
            return "ORD001"
        
        # Get the highest order number and increment
        order_numbers = []
        for order_id in self.orders.keys():
            if order_id.startswith("ORD"):
                try:
                    num = int(order_id[3:])
                    order_numbers.append(num)
                except ValueError:
                    continue
        
        if order_numbers:
            next_num = max(order_numbers) + 1
        else:
            next_num = 1
        
        return f"ORD{next_num:03d}"
    
    def add_order(self, order_data: Dict[str, Any], performed_by: str = "System") -> str:
        """Add a new order"""
        order_id = self.generate_order_id()
        order_data['order_id'] = order_id
        order_data['status'] = 'Ongoing'
        order_data['created_at'] = datetime.now().isoformat()
        
        self.orders[order_id] = order_data
        self.save_orders()
        
        self.log_action('Created', performed_by, order_id, f"New order created with {order_data['num_items']} items")
        print(f"✅ ORDER CREATED: {order_id} - {order_data['num_items']} items for {order_data['recipient_name']}")
        return order_id
    
    def update_order(self, order_id: str, order_data: Dict[str, Any], performed_by: str = "System"):
        """Update an existing order"""
        if order_id in self.orders:
            old_data = self.orders[order_id].copy()
            self.orders[order_id].update(order_data)
            self.orders[order_id]['updated_at'] = datetime.now().isoformat()
            self.save_orders()
            
            self.log_action('Edited', performed_by, order_id, "Order details updated")
            print(f"📝 ORDER UPDATED: {order_id}")
            return True
        return False
    
    def mark_delivered(self, order_id: str, performed_by: str = "System"):
        """Mark an order as delivered"""
        if order_id in self.orders:
            self.orders[order_id]['status'] = 'Delivered'
            self.orders[order_id]['delivered_at'] = datetime.now().isoformat()
            self.save_orders()
            
            self.log_action('Marked Delivered', performed_by, order_id, "Order marked as delivered")
            print(f"🚚 ORDER DELIVERED: {order_id}")
            return True
        return False
    
    def delete_order(self, order_id: str, performed_by: str = "System"):
        """Delete an order"""
        if order_id in self.orders:
            order_data = self.orders[order_id]
            del self.orders[order_id]
            self.save_orders()
            
            self.log_action('Deleted', performed_by, order_id, f"Order deleted - was for {order_data['recipient_name']}")
            print(f"🗑️ ORDER DELETED: {order_id}")
            return True
        return False
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get a specific order"""
        return self.orders.get(order_id)
    
    def get_all_orders(self) -> Dict[str, Any]:
        """Get all orders"""
        return self.orders
    
    def get_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent action logs"""
        return sorted(self.logs, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        total_orders = len(self.orders)
        ongoing_orders = len([o for o in self.orders.values() if o['status'] == 'Ongoing'])
        delivered_orders = len([o for o in self.orders.values() if o['status'] == 'Delivered'])
        total_items = sum([o['num_items'] for o in self.orders.values()])
        
        return {
            'total_orders': total_orders,
            'ongoing_orders': ongoing_orders,
            'delivered_orders': delivered_orders,
            'total_items': total_items,
            'total_actions': len(self.logs)
        }

# Initialize order manager
order_manager = OrderManager()

@app.route('/')
def index():
    """Display all orders"""
    orders = order_manager.get_all_orders()
    stats = order_manager.get_stats()
    print(f"📊 DASHBOARD ACCESS: {len(orders)} orders displayed")
    return render_template('index.html', orders=orders, stats=stats)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    """Add a new order"""
    if request.method == 'POST':
        try:
            order_data = {
                'num_items': int(request.form['num_items']),
                'delivery_date': request.form['delivery_date'],
                'sender_name': request.form['sender_name'],
                'recipient_name': request.form['recipient_name'],
                'recipient_address': request.form['recipient_address']
            }
            
            performed_by = request.form.get('performed_by', 'Anonymous')
            order_id = order_manager.add_order(order_data, performed_by)
            
            flash(f'Order {order_id} created successfully! 🎉', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash(f'Error creating order: {str(e)} ❌', 'error')
            print(f"❌ ERROR CREATING ORDER: {str(e)}")
    
    return render_template('add_order.html')

@app.route('/edit_order/<order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    """Edit an existing order"""
    order = order_manager.get_order(order_id)
    if not order:
        flash('Order not found! ❌', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            order_data = {
                'num_items': int(request.form['num_items']),
                'delivery_date': request.form['delivery_date'],
                'sender_name': request.form['sender_name'],
                'recipient_name': request.form['recipient_name'],
                'recipient_address': request.form['recipient_address']
            }
            
            performed_by = request.form.get('performed_by', 'Anonymous')
            order_manager.update_order(order_id, order_data, performed_by)
            
            flash(f'Order {order_id} updated successfully! ✅', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash(f'Error updating order: {str(e)} ❌', 'error')
            print(f"❌ ERROR UPDATING ORDER {order_id}: {str(e)}")
    
    return render_template('edit_order.html', order=order, order_id=order_id)

@app.route('/mark_delivered/<order_id>')
def mark_delivered(order_id):
    """Mark an order as delivered"""
    performed_by = request.args.get('performed_by', 'Anonymous')
    
    if order_manager.mark_delivered(order_id, performed_by):
        flash(f'Order {order_id} marked as delivered! 🚚', 'success')
    else:
        flash('Order not found! ❌', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_order/<order_id>')
def delete_order(order_id):
    """Delete an order"""
    performed_by = request.args.get('performed_by', 'Anonymous')
    
    if order_manager.delete_order(order_id, performed_by):
        flash(f'Order {order_id} deleted successfully! 🗑️', 'success')
    else:
        flash('Order not found! ❌', 'error')
    
    return redirect(url_for('index'))

@app.route('/logs')
def view_logs():
    """View action logs"""
    logs = order_manager.get_logs()
    stats = order_manager.get_stats()
    print(f"📋 LOGS ACCESS: {len(logs)} logs displayed")
    return render_template('logs.html', logs=logs, stats=stats)

@app.route('/api/orders')
def api_orders():
    """API endpoint to get all orders as JSON"""
    orders = order_manager.get_all_orders()
    return jsonify(orders)

@app.route('/api/logs')
def api_logs():
    """API endpoint to get action logs as JSON"""
    logs = order_manager.get_logs()
    return jsonify(logs)

@app.route('/api/stats')
def api_stats():
    """API endpoint to get system statistics"""
    stats = order_manager.get_stats()
    return jsonify(stats)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'orders_count': len(order_manager.get_all_orders()),
        'logs_count': len(order_manager.get_logs())
    })

if __name__ == '__main__':
    print("🚀 Starting Flask Order Management System...")
    print("📦 System initialized successfully!")
    print("🌐 Access the application at: http://localhost:5000")
    print("📊 API endpoints available at: /api/orders, /api/logs, /api/stats")
    print("❤️ Health check available at: /health")
    app.run(debug=True, host='0.0.0.0', port=5000)
