
<html lang="en">
<body>
    <h1>Customer Support System</h1>
    <p>A real-time customer support system with JWT authentication and Twilio WhatsApp webhook integration.</p>
    
    <h2>Project Structure</h2>
    <pre>
    support_system
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
    </pre>

    <h2>Installation</h2>
    <p>Clone the repository and install the required dependencies:</p>
    <pre><code>git clone https://github.com/nandannsr/SupportAgent_BE.git
cd support_system
pip install -r requirements.txt</code></pre>

    <h2>Setup Database and Migrations</h2>
    <pre><code>python manage.py makemigrations
python manage.py migrate</code></pre>

    <h2>Create a Superuser</h2>
    <p>Before using the application, create a superuser:</p>
    <pre><code>python manage.py createsuperuser</code></pre>
    <p>Follow the prompts to enter a username, email, and password.</p>

    <h2>Authentication</h2>
    <p>JWT is used for authentication. Obtain a token using:</p>
    <pre><code>POST /api/token/
Body: {
    "username": "your_username",
    "password": "your_password"
}</code></pre>
    <p>Use the received token to authenticate subsequent requests.</p>

    <h2>Twilio WhatsApp Webhook</h2>
    <p>When a customer sends a WhatsApp message, it triggers the webhook:</p>
    <ul>
        <li>The webhook processes the message.</li>
        <li>The message is sent to the frontend via WebSockets in real-time.</li>
    </ul>
    <p>Agents can also send messages back to customers from the frontend.</p>

    <h2>Running the Server</h2>
    <pre><code>python manage.py runserver</code></pre>
    <p>Access the application at <code>http://127.0.0.1:8000/</code></p>
</body>
</html>
