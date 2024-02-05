## Getting Started

1. **Change into the project directory:**
    ```bash
    cd Rabah
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

4. **Create a superuser (for Django Admin access):**
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

6. **Access the Django Admin:**
    - Open your browser and go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    - Log in with the superuser credentials created in step 4.

7. **Run Celery for background tasks:**
    ```bash
    celery -A Rabah worker --loglevel=info
    ```

## GitHub Repository
You can find the project on GitHub: [Rabah GitHub Repository](git@github.com:Impact-Technology-Consulting/Rabah.git)

## Additional Notes
[Include any additional notes or instructions here.]

## License
[Specify the project's license information here.]
