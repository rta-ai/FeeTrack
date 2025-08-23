from flask import Blueprint, render_template, request, redirect, url_for, flash
from forms import ExpenseForm
from models import Expense
from app import db

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/')
def list():
    expenses = Expense.query.order_by(Expense.expense_date.desc()).all()
    return render_template('expenses/list.html', expenses=expenses)

@expenses_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            title=form.title.data,
            description=form.description.data,
            amount=form.amount.data,
            expense_date=form.expense_date.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expenses.list'))
    return render_template('expenses/form.html', form=form, title='Add Expense')

@expenses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    expense = Expense.query.get_or_404(id)
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.title = form.title.data
        expense.description = form.description.data
        expense.amount = form.amount.data
        expense.expense_date = form.expense_date.data
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expenses.list'))
    return render_template('expenses/form.html', form=form, title='Edit Expense', expense=expense)

@expenses_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses.list'))
