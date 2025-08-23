from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import CourseForm
from models import Course
from app import db

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/')
def list():
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return render_template('courses/list.html', courses=courses)

@courses_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            session=form.session.data,
            total_fee=form.total_fee.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('courses.list'))
    return render_template('courses/form.html', form=form, title='Add Course')

@courses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.name = form.name.data
        course.session = form.session.data
        course.total_fee = form.total_fee.data
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('courses.list'))
    return render_template('courses/form.html', form=form, title='Edit Course', course=course)

@courses_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    course = Course.query.get_or_404(id)
    if course.students:
        flash('Cannot delete course with enrolled students. Please archive or transfer students first.', 'error')
    else:
        db.session.delete(course)
        db.session.commit()
        flash('Course deleted successfully!', 'success')
    return redirect(url_for('courses.list'))
