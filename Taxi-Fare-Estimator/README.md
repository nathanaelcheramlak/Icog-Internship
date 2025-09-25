# Taxi Fare Estimator

This project is a taxi fare estimator that uses a machine learning model to predict the fare of a taxi ride based on the distance, time of day, day of the week, and number of passengers. This project uses Celery and Celery Beat to automate the model retraining process.

## Features

- **Fare Prediction:** Predicts taxi fares based on ride details.
- **Automatic Retraining:** Celery Beat scheduler automatically retrains the model with new data.
- **Model Training:** Train the machine learning model on historical ride data.
- **REST API:** Provides endpoints for prediction and model training.
- **Data Generation:** Includes a utility to populate the database with random ride data.
- **Simple UI:** A simple user interface to interact with the API.

## Technologies Used

- **Backend:** Django, Django REST Framework
- **Machine Learning:** Scikit-learn, XGBoost, Pandas, Numpy
- **Asynchronous Tasks:** Celery, Redis
- **Database:** SQLite (default)

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/nathanaelcheramlak/Icog-Internship.git
    cd Icog-Internship/Taxi-Fare-Estimator
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    pip install -r tfe_backend/requirements.txt
    ```

4.  **Navigate to the backend directory:**

    ```bash
    cd tfe_backend
    ```

5.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

## User Interface

Access the web interface at: `http://127.0.0.1:8000/prediction/`

The UI provides a simple form to input ride details and get fare predictions instantly.

## API Endpoints

The following API endpoints are available:

- `POST /prediction/predict/`: Predicts the fare for a single ride.
- `POST /prediction/populate/`: Populates the database with random ride data.
- `GET/POST /prediction/train/`: Trains the machine learning model on the available data.
- `GET /`: A simple UI to interact with the API.

## Usage

### Predict a Fare

To predict a fare, send a `POST` request to the `/prediction/predict/` endpoint with the following JSON payload:

```json
{
	"distance": 5.0,
	"time": 15,
	"day_of_week": 3,
	"passengers": 2
}
```

### Populate the Database

To populate the database with random ride data, send a `POST` request to the `/prediction/populate/` endpoint with the following JSON payload:

```json
{
	"count": 100
}
```

This will add 100 new ride records to the database.

## Model Training

To train the model, send a `GET` or `POST` request to the `/prediction/train/` endpoint. This will train the model on all the data in the database and save the trained model and scaler to disk. The endpoint will return the evaluation metrics (MAE and RMSE) on the training data.

## Automation and Scheduling

This project uses Celery and Celery Beat to automate the model retraining process. The model is automatically retrained every two minutes with new data from the last 24 hours.

### Prerequisites

- **Redis:** Make sure you have Redis installed and running. You can install it using a package manager like `apt` or `brew`:

  ```bash
  # On Debian/Ubuntu
  sudo apt-get install redis-server

  # On macOS
  brew install redis
  ```

  Then, start the Redis server:

  ```bash
  redis-server
  ```

### Running the Celery Worker and Beat

1.  **Start the Celery worker:**
    Open a new terminal, navigate to the `tfe_backend` directory, and run the following command:

    ```bash
    celery -A tfe_backend worker -l info
    ```

2.  **Start the Celery Beat scheduler:**
    Open another terminal, navigate to the `tfe_backend` directory, and run the following command:
    ```bash
    celery -A tfe_backend beat -l info
    ```

Now, the model will be automatically retrained every two minutes.
