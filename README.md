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

## Project Structure

\`\`\`
flask-order-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── data/                 # Data storage directory
│   ├── orders.json       # Orders database (created automatically)
│   └── action_logs.json  # Action logs (created automatically)
└── templates/            # HTML templates
    ├── base.html         # Base template with common layout
    ├── index.html        # Main orders listing page
    ├── add_order.html    # Add new order form
    ├── edit_order.html   # Edit existing order form
    └── logs.html         # Action logs display
\`\`\`

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
\`\`\`bash
git clone <your-repository-url>
cd flask-order-system
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

### Order Data Structure

Each order contains:
- **Order ID**: Unique identifier (auto-generated)
- **Number of Items**: Integer count of items
- **Delivery Date**: Target delivery date
- **Sender Name**: Name of the person sending
- **Recipient Name**: Name of the person receiving
- **Recipient Address**: Full delivery address
- **Status**: Current status (Ongoing/Delivered)
- **Timestamps**: Creation and update times

### Action Logging

Every operation is logged with:
- **Action Type**: Created, Edited, Marked Delivered, Deleted
- **Performed By**: User identifier
- **Timestamp**: When the action occurred
- **Order ID**: Which order was affected
- **Details**: Additional information about the action

## Development Approach

### Architecture Decisions

1. **File-based Storage**: Used JSON files for simplicity and portability
2. **Class-based Design**: OrderManager class encapsulates all business logic
3. **Template Inheritance**: Base template for consistent UI across pages
4. **Error Handling**: Comprehensive try-catch blocks with user-friendly messages
5. **Logging System**: Complete audit trail for compliance and debugging

### Code Organization

- **app.py**: Main application with routes and Flask configuration
- **OrderManager Class**: Handles all order operations and data persistence
- **Templates**: Separate HTML files for each page with shared base template
- **Static Styling**: Embedded CSS for simplicity (no external dependencies)

### Security Considerations

- Input validation on all forms
- Confirmation dialogs for destructive operations
- Secret key for session management
- XSS protection through template escaping

## Deployment Options

### Local Development
- Run directly with \`python app.py\`
- Access at \`http://localhost:5000\`

### Production Deployment
- Use a WSGI server like Gunicorn
- Set up proper database (PostgreSQL, MySQL)
- Configure environment variables
- Use reverse proxy (Nginx)

### Environment Variables
- \`FLASK_ENV\`: Set to 'production' for production deployment
- \`SECRET_KEY\`: Use a secure random key in production

## Testing

### Manual Testing Checklist
- [ ] Create new order with all fields
- [ ] Edit existing order
- [ ] Mark order as delivered
- [ ] Delete order
- [ ] View action logs
- [ ] Test form validation
- [ ] Test error handling

### API Testing
\`\`\`bash
# Get all orders
curl http://localhost:5000/api/orders

# Get action logs
curl http://localhost:5000/api/logs
\`\`\`

## Future Enhancements

- Database integration (SQLite, PostgreSQL)
- User authentication and authorization
- Order search and filtering
- Email notifications
- PDF report generation
- REST API with full CRUD operations
- Mobile-responsive design improvements

## Troubleshooting

### Common Issues

1. **Port Already in Use**: Change port in app.py or kill existing process
2. **Permission Errors**: Ensure write permissions for data directory
3. **Module Not Found**: Activate virtual environment and install requirements
4. **JSON Decode Error**: Delete corrupted JSON files (they'll be recreated)

### Debug Mode
The application runs in debug mode by default for development. Disable for production by setting \`debug=False\` in app.py.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes as part of the Galvan AI assessment.

---

**Author**: [Your Name]  
**Created**: June 2025  
**Framework**: Flask 2.3.3  
**Python Version**: 3.7+
\`\`\`
