# Flask CRUD Operations with Multiple Databases

This project demonstrates performing CRUD (Create, Read, Update, Delete) operations using Flask with various databases including SQLite, MySQL, MongoDB, and PostgreSQL. The application utilizes raw SQL queries for database interactions instead of SQLAlchemy.

## Files Used

- `flask-sqlite.py`: Demonstrates CRUD operations with SQLite database.
- `flask-mysql.py`: Demonstrates CRUD operations with MySQL database.
- `flask-mongo.py`: Demonstrates CRUD operations with MongoDB.
- `flask-pgsql.py`: Demonstrates CRUD operations with PostgreSQL database.
- `.env`: Environment file for storing sensitive information (e.g., database credentials).
- `requirements.txt`: Contains the list of dependencies required for the project.
- `Procfile`: Specifies the commands that are executed by the app on startup.

## Setup and Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/minnukota381/Flask-CRUD-App.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Flask-CRUD-App
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up databases:

   - For SQLite: No setup required.
   - For MySQL: Create a MySQL database and configure the connection settings in `.env`.
   - For MongoDB: Make sure MongoDB is running locally or configure the connection settings in `.env`.
   - For PostgreSQL: Create a PostgreSQL database and configure the connection settings in `.env`.

## Usage

1. Run the Flask application:

    ```bash
    python flask-sqlite.py
    ```

    Replace `flask-sqlite.py` with the respective file name for other databases.

2. Access the application in your web browser at `http://localhost:5000`.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
