# real-time-chat-app

This project is a real-time chat application built using Django Channels, WebSockets, and Django REST Framework. It allows users to communicate in real-time within various chat rooms, with support for user authentication, chat room management.

## Features

- Real-Time Communication: Users can send and receive messages in real-time using WebSockets.
- User Authentication: Secure user authentication using JWT tokens.
- Chat Room Management: Create, delete, and manage chat rooms. Users can be added or removed from chat rooms. Allow users to view the chat history.

## Setup
### Installation
1. Clone the repository.
```
git clone https://github.com/pmyatthwe/real-time-chat-app.git
cd realtime-chat-app
```
2. Create a virtual environment and activate it.
```
python3 -m venv venv
source venv/bin/activate
```
3. Install the dependencie.
```
pip install -r requirements.txt
```
4. Run the migrations.
```
python3 manage.py migrate
```
5. Create a superuser for admin access.
```
python3 manage.py createsuperuser
```
6. Start the development server.
```
python3 manage.py runserver
```

## Usage
- Register and authenticate a user.
- Create chat rooms and join them.
- Start sending messages in real-time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
