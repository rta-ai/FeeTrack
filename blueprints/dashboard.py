from flask import Blueprint, render_template
from sqlalchemy import func
from models import Course, Student, Payment, Refund, Expense
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    # Calculate dashboard statistics
    courses = Course.query.all()
    
    # Total fee collected per course
    course_collections = {}
    for course in courses:
        total_payments = db.session.query(func.sum(Payment.amount)).join(Student).filter(
            Student.course_id == course.id
        ).scalar() or 0.0
        
        total_refunds = db.session.query(func.sum(Refund.amount)).join(Student).filter(
            Student.course_id == course.id
        ).scalar() or 0.0
        
        course_collections[course.name] = total_payments - total_refunds
    
    # Total fee collected across all courses
    total_collected = sum(course_collections.values())
    
    # Total pending fees
    active_students = Student.query.filter_by(is_archived=False).all()
    total_pending = sum(student.fee_pending for student in active_students)
    
    # Total expenses
    total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0.0
    
    # Net available balance
    net_balance = total_collected - total_expenses
    
    # Students with pending fees
    students_with_pending = [student for student in active_students if student.fee_pending > 0]
    
    return render_template('dashboard.html',
                         course_collections=course_collections,
                         total_collected=total_collected,
                         total_pending=total_pending,
                         total_expenses=total_expenses,
                         net_balance=net_balance,
                         active_students=active_students,
                         students_with_pending=students_with_pending)
