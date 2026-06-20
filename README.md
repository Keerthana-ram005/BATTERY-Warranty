# Battery Warranty Management System

## Overview

The Battery Warranty Management System is a web-based application developed to help battery retailers efficiently manage customer warranty records. The application digitizes warranty tracking, reduces manual paperwork, and enables quick retrieval of customer and battery information whenever warranty claims arise.

This project was developed as a real-world client solution for a local battery shop using Streamlit and SQLite.

---

## Features

### User Authentication

* Secure login system for authorized users
* Session-based access control

### Customer Management

* Add new customer records
* Store customer contact details
* Search customer information

### Battery Warranty Tracking

* Register battery purchases
* Record warranty periods
* Track warranty start and expiry dates

### Warranty Search

* Search records by customer name
* Search by phone number
* Search by battery details

### Warranty Status Monitoring

* Identify active warranties
* Track expired warranties
* View warranty validity information

### Data Management

* Store records in SQLite database
* Update existing warranty records
* Manage customer and battery information

### Mobile-Friendly Interface

* Accessible through mobile devices
* Simple and easy-to-use interface for shop staff

---

## Technology Stack

* Python
* Streamlit
* SQLite
* Pandas

---

## Project Structure

```text
Battery-Warranty-System/
│
├── app.py
├── database.db
├── requirements.txt
├── README.md
├── uploads/
```

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd Battery-Warranty-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

## Use Case

This application is designed for battery retailers who need a simple and efficient way to manage warranty records digitally instead of maintaining physical warranty registers.

---

## Future Enhancements

* Warranty expiry notifications
* Excel export functionality
* Cloud deployment
* PostgreSQL database integration
* Role-based access management
* Automated backup system

---

## Author

Keerthana Ramanathan

First real-world client project developed using Streamlit and SQLite.
