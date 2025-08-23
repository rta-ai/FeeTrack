from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import StudentForm, PaymentForm, RefundForm
from models import Student, Payment, Refund
from app import db

students_bp = Blueprint('students', __name__)

@students_bp.route('/')
def list():
    show_archived = request.args.get('archived', 'false') == 'true'
    if show_archived:
        students = Student.query.filter_by(is_archived=True).order_by(Student.archived_at.desc()).all()
    else:
        students = Student.query.filter_by(is_archived=False).order_by(Student.created_at.desc()).all()
    return render_template('students/list.html', students=students, show_archived=show_archived)

@students_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            father_name=form.father_name.data,
            contact=form.contact.data,
            course_id=form.course_id.data,
            scholarship=form.scholarship.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students.list'))
    return render_template('students/form.html', form=form, title='Add Student')

@students_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.father_name = form.father_name.data
        student.contact = form.contact.data
        student.course_id = form.course_id.data
        student.scholarship = form.scholarship.data
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students.detail', id=student.id))
    return render_template('students/form.html', form=form, title='Edit Student', student=student)

@students_bp.route('/detail/<int:id>')
def detail(id):
    student = Student.query.get_or_404(id)
    payments = Payment.query.filter_by(student_id=id).order_by(Payment.payment_date.desc()).all()
    refunds = Refund.query.filter_by(student_id=id).order_by(Refund.refund_date.desc()).all()
    return render_template('students/detail.html', student=student, payments=payments, refunds=refunds)

@students_bp.route('/payment/<int:id>', methods=['GET', 'POST'])
def add_payment(id):
    student = Student.query.get_or_404(id)
    form = PaymentForm()
    if form.validate_on_submit():
        # Validate payment amount doesn't exceed pending amount
        if form.amount.data > student.fee_pending:
            flash(f'Payment amount cannot exceed pending fee of ₹{student.fee_pending:.2f}', 'error')
        else:
            payment = Payment(
                student_id=id,
                amount=form.amount.data,
                payment_date=form.payment_date.data,
                received_by=form.received_by.data,
                notes=form.notes.data
            )
            db.session.add(payment)
            db.session.commit()
            flash('Payment recorded successfully!', 'success')
            return redirect(url_for('students.detail', id=id))
    return render_template('students/payment_form.html', form=form, student=student, title='Record Payment')

@students_bp.route('/refund/<int:id>', methods=['GET', 'POST'])
def add_refund(id):
    student = Student.query.get_or_404(id)
    form = RefundForm()
    if form.validate_on_submit():
        # Validate refund amount doesn't exceed paid amount
        if form.amount.data > student.fee_paid:
            flash(f'Refund amount cannot exceed paid fee of ₹{student.fee_paid:.2f}', 'error')
        else:
            refund = Refund(
                student_id=id,
                amount=form.amount.data,
                refund_date=form.refund_date.data,
                reason=form.reason.data,
                processed_by=form.processed_by.data
            )
            db.session.add(refund)
            db.session.commit()
            flash('Refund processed successfully!', 'success')
            return redirect(url_for('students.detail', id=id))
    return render_template('students/payment_form.html', form=form, student=student, title='Process Refund')

@students_bp.route('/archive/<int:id>', methods=['POST'])
def archive(id):
    student = Student.query.get_or_404(id)
    student.archive()
    db.session.commit()
    flash('Student archived successfully!', 'success')
    return redirect(url_for('students.list'))

@students_bp.route('/restore/<int:id>', methods=['POST'])
def restore(id):
    student = Student.query.get_or_404(id)
    student.is_archived = False
    student.archived_at = None
    db.session.commit()
    flash('Student restored successfully!', 'success')
    return redirect(url_for('students.list'))
