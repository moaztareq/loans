Project Title: Bank Loan Management System
Overview
This is a Django-based backend project for managing bank loans. It includes:
	1) Loan Provider management.
	2) Customer loan requests and payments.
	2) Bank personnel tools for managing loan settings and monitoring loans.
	4) Validations to ensure loan amounts do not exceed available funds.
 
Features:
	1) Loan management endpoints.
	2) Payments system with amortization calculations.
	3) User roles: Bank Staff, Loan Providers, Loan Customers.
	4) Automated test cases for core functionalities.
	5) RESTful API documentation: https://documenter.getpostman.com/view/26091365/2sAYBPmEH1

Installation Instructions:
	1) Clone the Repository
 		git clone https://github.com/moaztareq/loans.git
		cd your-repo-name
	2) Create a Virtual Environment
 		python -m venv venv
		source venv/bin/activate  # For Linux/Mac
		venv\Scripts\activate     # For Windows
	3) Install Dependencies
 		pip install -r requirements.txt
	4) Set Up Environment Variables
 	6) Run Migrations
  		python manage.py makemigrations
		python manage.py migrate
  	7) Run Tests
		python manage.py test
	8) Start the Development Server
 		python manage.py runserver
   
Project Structure:
	├── core/               # User management (authentication, registration, etc.)
	├── loan/               # Loan models, views, serializers, and logic
	├── global/             # Bank settings management
	├── tests/              # Unit tests for core functionalities
	├── manage.py           # Django project management script
	├── requirements.txt    # Python dependencies
	├── README.md           # Project instructions
	├── .gitignore          # Ignored files for version control

