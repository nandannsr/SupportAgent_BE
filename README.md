# Customer Support System

A real-time customer support system with JWT authentication and Twilio WhatsApp webhook integration.

## Project Structure
```
Support_System
├── chat_app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── webhooks.py
│   ├── utils.py
│   ├── web_socket/
│   │   ├── consumers.py
│   │   ├── routing.py
├── db.sqlite3
├── manage.py
├── requirements.txt
├── support_system/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
├── .env.sample
```

## Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/nandannsr/SupportAgent_BE.git
cd Support_System
pip install -r requirements.txt
```

## Setup Environment Variables
Create a `.env` file in the root directory based on `.env.sample`:
```bash
cp .env.sample .env
```
Update the `.env` file with the necessary configurations.

### Twilio Integration
To integrate Twilio, you need to set up your **Account SID** and **Auth Token** in the `.env` file. 

- Sign up or log in to Twilio: [Twilio Console](https://www.twilio.com/login?g=%2Fconsole%3F&t=2b1c98334b25c1a785ef15b6556396290e3c704a9b57fc40687cbccd79c46a8c)
- Enable **WhatsApp Messaging** in Twilio.
- Copy your **Account SID** and **Auth Token** from the Twilio Console.
- Add them to your `.env` file as follows:
  ```ini
  TWILIO_ACCOUNT_SID=your_account_sid
  TWILIO_AUTH_TOKEN=your_auth_token
  ```

## Setup Database and Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Create a Superuser
Before using the application, create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to enter a username, email, and password.

## Authentication
JWT is used for authentication. Obtain a token using:
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```
Use the received token to authenticate subsequent requests.

## Twilio WhatsApp Webhook
When a customer sends a WhatsApp message, it triggers the webhook:
- The webhook processes the message.
- The message is sent to the frontend via WebSockets in real-time.
- Agents can also send messages back to customers from the frontend.

## Install Redis
Ensure Redis is installed on your system for ASGI support:
```bash
sudo apt update
sudo apt install redis-server
```
Start Redis:
```bash
sudo systemctl start redis
```
Enable Redis to start on boot:
```bash
sudo systemctl enable redis
```

## Running the Server
```bash
python manage.py runserver
```
Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

