
This is a social media platform built using Django, where users can create profiles, share posts, follow other users, like/dislike posts, and comment on them.
In fact this is my first django project.

## Database Structure
This Django application utilizes a database to store and manage various entities and their relationships. The following ERD provides a visual representation of the database structure:

![1.png](..%2F1.png)

The ERD illustrates the entities, relationships, and attributes within the database. It serves as a reference for understanding how the data is organized and connected in the application.

## Features

- User registration and authentication
- User profiles with usernames, profile pictures, and bios
- Viewing user profiles of other people
- Sending friend requests or follows to other users
- Publishing posts with long texts and multiple photos, including a title and category tags
- Liking and disliking posts
- Commenting on posts
- Following specific categories
- Archive posts or accounts for removal from public access

## Technologies Used

- Django
- Python
- HTML/CSS


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MahdiehSoleimani/django_socialmedia.git
   ```

2. Create a virtual environment:

   ```bash
   virtualenv venv
   ```

3. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run database migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://localhost:8000` in your browser.

## Usage

- Register a new user account or log in with an existing one.
- Create your profile, including a username, profile picture, and bio.
- Explore the platform by viewing user profiles, sending friend requests or follows, and checking out posts from followed users and categories.
- Create new posts, add titles, content, and category tags.
- Like or dislike posts to express your opinion.
- Comment on posts to engage in conversations.
- Archive your own posts or account to remove them from public access.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to create an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- This project was inspired by the functionalities of popular social media platforms like Twitter.
- The project utilizes the Django web framework for efficient development.

## Contact

If you have any questions or inquiries, please feel free to contact by mahdieh.soleimani2000@gmail.com.

