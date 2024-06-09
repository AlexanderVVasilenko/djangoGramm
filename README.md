# DjangoGramm

DjangoGramm is a Django-based web application that mimics some functionalities of Instagram. Users can register, create profiles, post images, and interact with other users' posts.

## Features

- User registration and authentication
- Profile creation and editing
- Image uploading and posting (IN DEVELOPMENT)
- Interaction with posts (like(IN DEVELOPMENT), comment)
- Password reset functionality

## Installation
1. Clone the repository:
```bash
git clone https://github.com/AlexanderVVasilenko/djangoGramm.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Apply database migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Access the application at [http://localhost:8000](http://localhost:8000) in your web browser.

## Usage

- Sign up for a new account or log in with existing credentials.
- Edit your profile with a bio, and profile picture.
- Explore posts from other users and interact by liking (IN DEVELOPMENT) or commenting.
- Upload your images and share them with the community (IN DEVELOPMENT).

## Testing

To run the automated tests, use the following command:

```bash
pytest
```


## Technologies Used

- Django
- Python
- HTML/CSS
- JavaScript (IN FUTURE)

## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was inspired by the functionalities of Instagram.
- Thanks to the Django community for the excellent documentation and resources.
