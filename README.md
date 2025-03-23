## Instalation

1. Clone the repository:
   ```bash
   git clone https://github.com/507015T/doctor-aibolit.git
   ```
2. Navigate to the project directory:
   ```bash
   cd doctor-aibolit
   ```
3. create venv, makemigrations, migrate 
   ```bash
   python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt && python3 manage.py makemigrations && python3 manage.py migrate

   ```
4. If you use docker, docker-compose
    ```bash
    docker-compose build && docker-compose up
    ```

## Configuration

Set the following environment variables:

- `SECRET_KEY`: Django secret key for production environment.
- `DEBUG`: Set to `True` in development, `False` in production.
## Testing

To run tests:

1. Make sure the virtual environment is activated.
2. Run the following command:
   ```bash
   python3 manage.py test
   ```

This will run all the unit tests for the project.
