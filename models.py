from datetime import datetime
from app import db
from sqlalchemy import func

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    session = db.Column(db.String(50), nullable=False)
    total_fee = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    students = db.relationship('Student', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.name}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    scholarship = db.Column(db.Float, default=0.0)
    is_archived = db.Column(db.Boolean, default=False)
    archived_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='student', lazy=True, cascade='all, delete-orphan')
    refunds = db.relationship('Refund', backref='student', lazy=True, cascade='all, delete-orphan')
    
    @property
    def total_fee(self):
        return self.course.total_fee if self.course else 0.0
    
    @property
    def net_payable_fee(self):
        return max(0, self.total_fee - self.scholarship)
    
    @property
    def fee_paid(self):
        total_paid = db.session.query(func.sum(Payment.amount)).filter(
            Payment.student_id == self.id
        ).scalar() or 0.0
        
        total_refunded = db.session.query(func.sum(Refund.amount)).filter(
            Refund.student_id == self.id
        ).scalar() or 0.0
        
        return max(0, total_paid - total_refunded)
    
    @property
    def fee_pending(self):
        return max(0, self.net_payable_fee - self.fee_paid)
    
    def archive(self):
        self.is_archived = True
        self.archived_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Student {self.name}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    received_by = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.amount} for Student {self.student_id}>'

class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    refund_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    reason = db.Column(db.Text, nullable=False)
    processed_by = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Refund {self.amount} for Student {self.student_id}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Expense {self.title}: {self.amount}>'
