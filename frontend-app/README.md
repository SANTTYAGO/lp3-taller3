# lp3-taller3
Diseño de Front-end para consumir el API del proyecto lp3-taller2

## Pasos

1. Realice un `fork` de este proyecto, y luego `clone` su proyecto en su equipo local para trabajar.
2. Desarrolle un Front-end que consuma los servicios del API creado en [https://github.com/UR-CC/lp3-taller2](https://github.com/UR-CC/lp3-taller2)
3. Para el desarrollo del Front-end puede utilizar cualquier framework/lenguaje de su preferencia.


# Front-end Application for Music API

This project is a front-end application that consumes the services of a music API. It is designed to provide a user-friendly interface for managing users, songs, and favorites.

## Project Structure

```
frontend-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── components             # Contains components for user, song, and favorite functionalities
│   │   ├── user_component.py   # User-related functionalities
│   │   ├── song_component.py    # Song-related functionalities
│   │   └── favorite_component.py # Favorite songs functionalities
│   ├── utils                  # Utility functions for API calls
│   │   └── api_client.py      # Functions for making API requests
│   └── templates              # HTML templates for rendering views
│       ├── base.html          # Base template for the application
│       ├── users.html         # Template for displaying user information
│       ├── songs.html         # Template for displaying song information
│       └── favorites.html      # Template for displaying favorite songs
├── requirements.txt           # Lists project dependencies
├── .env                       # Environment variables for configuration
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the root directory and configure the necessary environment variables, such as API URLs.

## Usage

To run the application, execute the following command:

```
python src/main.py
```

Visit `http://localhost:5000` in your web browser to access the application.

## Features

- User management: View and manage user information.
- Song management: Display song details and perform actions on songs.
- Favorites: Mark songs as favorites and view the list of favorite songs.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.