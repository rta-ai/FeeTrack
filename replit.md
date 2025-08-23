# Student Fee Management System

## Overview

This is a comprehensive Student Fee Management System built with Flask, designed to help educational institutions manage courses, students, fee collections, payments, and expenses. The system provides a complete dashboard view of financial status, supports installment payments, scholarship management, and includes student archiving functionality. The application follows a modular architecture with separate blueprints for different functional areas and uses SQLAlchemy for database operations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework and Structure
- **Web Framework**: Flask with Blueprint-based modular architecture
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy integration
- **Form Handling**: Flask-WTF with WTForms for secure form processing and validation
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive UI
- **Application Structure**: Organized into separate blueprints (dashboard, courses, students, expenses) for maintainability

### Database Design
- **Database**: SQLite for development with configurable DATABASE_URL for production
- **Connection Management**: Connection pooling with pool_recycle and pool_pre_ping for reliability
- **Models**: Four main entities - Course, Student, Payment, Refund, and Expense
- **Relationships**: Foreign key relationships between students and courses, with cascade deletes for related records
- **Data Integrity**: Soft delete pattern for students (archived flag) to maintain historical records

### Business Logic Architecture
- **Fee Calculation**: Automatic calculation of net payable fees (total fee minus scholarship)
- **Payment Tracking**: Real-time calculation of paid amounts and pending balances through database aggregations
- **Financial Management**: Comprehensive expense tracking with dashboard summaries
- **Student Lifecycle**: Support for student archiving/restoration instead of hard deletion

### Security and Configuration
- **Session Management**: Configurable secret key with environment variable fallback
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies
- **Environment Configuration**: Environment-based database URL and secret key configuration
- **Form Security**: CSRF protection through Flask-WTF

### User Interface Design
- **Responsive Design**: Bootstrap 5 framework with custom CSS for enhanced styling
- **Icon Integration**: Font Awesome icons throughout the interface
- **Navigation**: Consistent navigation bar with role-based menu items
- **Dashboard**: Comprehensive financial overview with key performance indicators
- **Form Validation**: Client and server-side validation with user-friendly error messages

## External Dependencies

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design and components
- **Font Awesome**: Icon library for enhanced user interface elements
- **Custom CSS**: Additional styling for application-specific design requirements

### Python Packages
- **Flask**: Core web framework for application structure
- **Flask-SQLAlchemy**: Database ORM integration with Flask
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation and rendering
- **Werkzeug**: WSGI utilities including ProxyFix middleware

### Database
- **SQLite**: Default database for development and small deployments
- **Configurable Database**: Support for PostgreSQL or other databases via DATABASE_URL environment variable

### Development and Deployment
- **Environment Variables**: DATABASE_URL and SESSION_SECRET for configuration
- **WSGI Support**: Compatible with production WSGI servers
- **Static File Serving**: Flask's static file handling for CSS, JavaScript, and images