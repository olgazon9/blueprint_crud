# Book Library Application

Welcome to the Book Library Application. This application allows users to manage books, loaners, and loans. Users can add, edit, and delete books, manage loaner information, and record and manage book loans.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- Manage Books:
  - Add, edit, and delete books.
  - Search for books by title.
- Manage Loaners:
  - Add, edit, and delete loaners.
  - Search for loaners by name.
- Manage Loans:
  - Apply for a loan.
  - Return a book.
  - View late loans.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js
- NPM
- Python
- Flask
- SQLite (or another database of your choice)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/olgazon9/blueprint_crud.git

2. Install the necessary dependencies:
cd blueprint_crud
npm install
pip install -r requirements.txt

3.Set up your database by running the database migration:
flask db init
flask db migrate
flask db upgrade

4.Start the development server:
npm start
py app.py

### Usage
Visit http://localhost:yourport in your web browser to access the Book Library Application.

You can manage books, loaners, and loans through the provided web interface.

### API Endpoints
/books: Endpoints for managing books.
/loaners: Endpoints for managing loaners.
/loans: Endpoints for managing loans.
For detailed API documentation and available endpoints, please refer to the API documentation.


### Contributing
We welcome contributions from the community. If you would like to contribute, please follow these steps:

Fork the repository on GitHub.
Create a new branch for your feature or bug fix.
Make your changes and commit them.
Push your changes to your fork.
Submit a pull request to the main branch of the original repository.
Please read CONTRIBUTING.md for details on the code of conduct, and the process for submitting pull requests.



