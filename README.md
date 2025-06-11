# Flask Order Handling System

A comprehensive order management system built with Flask that handles basic order operations including creation, editing, delivery tracking, and action logging.

## Features

### Core Functionality
- **Add New Orders**: Create orders with unique IDs, item counts, delivery dates, sender/recipient information
- **Order Management**: Edit existing orders, mark as delivered, and delete orders
- **Action Logging**: Complete audit trail of all operations with timestamps and user tracking
- **Order Display**: Clean HTML interface showing all orders with their current status

### Technical Features
- RESTful API endpoints for programmatic access
- JSON-based data persistence
- Responsive web interface
- Input validation and error handling
- Flash messaging for user feedback




### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
\`\`\`bash
1. clone the repo
cd to project path
\`\`\`

### Step 2: Create Virtual Environment (Recommended)
\`\`\`bash
python -m venv venv

# On Windows
venv\\Scripts\\activate

# On macOS/Linux
source venv/bin/activate
\`\`\`

### Step 3: Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 4: Run the Application
\`\`\`bash
python app.py
\`\`\`

The application will start on \`http://localhost:5000\`

## Usage Guide

### Web Interface

1. **View All Orders**: Navigate to \`http://localhost:5000\` to see all orders
2. **Add New Order**: Click "Add New Order" and fill in the required information
3. **Edit Order**: Click "Edit" next to any order to modify its details
4. **Mark as Delivered**: Click "Mark Delivered" to update order status
5. **Delete Order**: Click "Delete" to remove an order (with confirmation)
6. **View Logs**: Click "Action Logs" to see all system activities

### API Endpoints

- \`GET /api/orders\` - Retrieve all orders as JSON
- \`GET /api/logs\` - Retrieve action logs as JSON


### Common Issues

1. **Port Already in Use**: Change port in app.py or kill existing process
2. **Permission Errors**: Ensure write permissions for data directory
3. **Module Not Found**: Activate virtual environment and install requirements
4. **JSON Decode Error**: Delete corrupted JSON files (they'll be recreated)

**DashBoard**

![image](https://github.com/user-attachments/assets/7f7a97fb-c968-483e-bd18-262076e32cb6)


