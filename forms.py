from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import date
from models import Course

class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=100)])
    session = StringField('Session', validators=[DataRequired(), Length(min=2, max=50)])
    total_fee = FloatField('Total Fee', validators=[DataRequired(), NumberRange(min=0)])

class StudentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=100)])
    father_name = StringField('Father Name', validators=[DataRequired(), Length(min=2, max=100)])
    contact = StringField('Contact', validators=[DataRequired(), Length(min=10, max=20)])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    scholarship = FloatField('Scholarship Amount', validators=[NumberRange(min=0)], default=0.0)
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.course_id.choices = [(c.id, f"{c.name} - {c.session}") for c in Course.query.all()]

class PaymentForm(FlaskForm):
    amount = FloatField('Payment Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    payment_date = DateField('Payment Date', validators=[DataRequired()], default=date.today)
    received_by = StringField('Received By', validators=[DataRequired(), Length(min=2, max=100)])
    notes = TextAreaField('Notes')

class RefundForm(FlaskForm):
    amount = FloatField('Refund Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    refund_date = DateField('Refund Date', validators=[DataRequired()], default=date.today)
    reason = TextAreaField('Reason for Refund', validators=[DataRequired()])
    processed_by = StringField('Processed By', validators=[DataRequired(), Length(min=2, max=100)])

class ExpenseForm(FlaskForm):
    title = StringField('Expense Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description')
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    expense_date = DateField('Expense Date', validators=[DataRequired()], default=date.today)
