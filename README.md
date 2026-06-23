# Mock Payment Gateway (Meeza / dLocal Style)

## Features
- Create Payment
- Redirect to mock payment route
- Simulated success/failure
- Async webhook callback
- Payment status tracking



# Backend Payment Clone

A Flask-based payment API.


## Setup

Create and activate the environment:

```bash
conda create --name payments python=3.10
conda activate payments
pip install -r requirements.txt
```

Copy environment variables:

```bash
cp .env.example .env
```

## Run

```bash
python app.py
