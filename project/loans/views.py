from flask import Blueprint, request, jsonify
from .models import  Loan
from datetime import datetime, timedelta
from project import db

loans_blueprint = Blueprint('loans', __name__)


# Loans CRUD operations
@loans_blueprint.route('/loans', methods=['GET'])
def get_all_loans():
    # Retrieve all loans from the 'loan' table
    loans = Loan.query.all()
    loan_list = []
    for loan in loans:
        # Create a dictionary for each loan's information
        loan_info = {
            'id': loan.id,
            'book_id': loan.book_id,
            'loaner_id': loan.loaner_id,
            'loaned_date': str(loan.loaned_date),
            'returned_date': str(loan.returned_date) if loan.returned_date else None
        }
        loan_list.append(loan_info)

    return jsonify({'loans': loan_list})

@loans_blueprint.route('/loans/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    # Retrieve a specific loan by ID from the 'loan' table
    loan = Loan.query.get(loan_id)
    if loan:
        # Create a dictionary for the loan's information
        loan_info = {
            'id': loan.id,
            'book_id': loan.book_id,
            'loaner_id': loan.loaner_id,
            'loaned_date': str(loan.loaned_date),
            'returned_date': str(loan.returned_date) if loan.returned_date else None
        }
        return jsonify(loan_info)
    else:
        return jsonify({'message': 'Loan not found'}), 404

@loans_blueprint.route('/loans', methods=['POST'])
def create_loan():
    try:
        data = request.get_json()
        book_id = data['book_id']
        loaner_id = data['loaner_id']
        loaned_date = datetime.strptime(data['loaned_date'], '%Y-%m-%d')
        due_date = loaned_date + timedelta(days=7)

        existing_loan = Loan.query.filter_by(book_id=book_id, returned_date=None).first()
        if existing_loan:
            return jsonify({'error': 'Book is already loaned'}), 400

        new_loan = Loan(
            book_id=book_id,
            loaner_id=loaner_id,
            loaned_date=loaned_date,
            due_date=due_date
        )
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({'message': 'Loan created successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Invalid data or server error: ' + str(e)}), 400


@loans_blueprint.route('/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    # Update an existing loan's information based on JSON data received in the request
    loan = Loan.query.get(loan_id)
    if loan:
        data = request.get_json()
        loan.loaned_date = data['loaned_date']
        loan.returned_date = data['returned_date'] if 'returned_date' in data else None
        db.session.commit()
        return jsonify({'message': 'Loan updated successfully'})
    else:
        return jsonify({'message': 'Loan not found'}), 404

@loans_blueprint.route('/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    # Delete an existing loan from the 'loan' table
    loan = Loan.query.get(loan_id)
    if loan:
        db.session.delete(loan)
        db.session.commit()
        return jsonify({'message': 'Loan deleted successfully'})
    else:
        return jsonify({'message': 'Loan not found'}), 404

@loans_blueprint.route('/loans/<int:loan_id>/return', methods=['PUT'])
def return_book(loan_id):
    loan = Loan.query.get(loan_id)
    if loan:
        # Check if the book has already been returned
        if loan.returned_date:
            return jsonify({'message': 'Book has already been returned'}), 400

        # Update the returned_date to the current date
        loan.returned_date = datetime.now().date()
        db.session.commit()

        # Check if the return is late
        if loan.returned_date > loan.due_date:
            return jsonify({'message': 'Book returned late'}), 400

        return jsonify({'message': 'Book returned successfully'})
    else:
        return jsonify({'message': 'Loan not found'}), 404
    
@loans_blueprint.route('/late-loans', methods=['GET'])
def get_late_loans():
    # Calculate the due date for loans (7 days from the loaned date)
    due_date = datetime.now().date() - timedelta(days=7)

    # Query for loans where the current date is greater than the due date
    late_loans = Loan.query.filter(Loan.returned_date.is_(None), Loan.loaned_date <= due_date).all()

    # Create a list of late loan information
    late_loan_list = []
    for loan in late_loans:
        late_loan_info = {
            'id': loan.id,
            'book_id': loan.book_id,
            'loaner_id': loan.loaner_id,
            'loaned_date': str(loan.loaned_date),
            'due_date': str(loan.loaned_date + timedelta(days=7)),  # Calculate the due date
        }
        late_loan_list.append(late_loan_info)

    return jsonify({'late_loans': late_loan_list})

@loans_blueprint.route('/loans/check-loan-availability', methods=['GET'])
def check_loan_availability():
    try:
        book_id = request.args.get('book_id')
        existing_loan = Loan.query.filter_by(book_id=book_id, returned_date=None).first()

        if existing_loan:
            return jsonify({'available': False})
        else:
            return jsonify({'available': True})
    except Exception as e:
        return jsonify({'error': 'Server error: ' + str(e)}), 500
