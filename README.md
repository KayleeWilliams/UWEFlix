# UWEFlix
This is my implementation for my Distributed and Enterprise Software Development module coursework.

The dockerfile is in the UWEFlix folder.

## Installation
### Docker
1. Install Docker
2. Clone the repository
3. Build the Docker Image, `docker build -t <image_name> .`

### Virtual Environment
1. Install Python 3.9
2. Clone the repository
3. Create a virtual environment, `python3 -m venv venv`
4. Activate the virtual environment, `venv\Scripts\activate`
5. Install the requirements, `pip install -r requirements.txt`

## Running the application
### Docker
1. Run the Docker Image, `docker run -p 8000:8000 <image_name>`

### Virtual Environment
1.  Navigate to UWEFlix folder, `python3 manage.py runserver`

## In Action
### Film Page
![Film Page](/images/film_page.png)
### Film Page (Film Details + Showings)
![Film Page (Film Details + Showings)](/images/film_details.png)

### Booking Form
![Booking Form](/images/booking_form.png)

### Booking Confirmation
![Booking Confirmation](/images/booking_confirmation.png)

