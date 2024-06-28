# DocPad

[![codecov](https://codecov.io/gh/swetayadav0521/DocPad/branch/main/graph/badge.svg?token=4c9a7679-f591-4a62-8e57-6bfdb24f0735)](https://codecov.io/gh/swetayadav0521/DocPad)

APIs To Document Patient Interactions and View Patient History

---

## Technical Concept

### Architecture Overview

- **Frontend**: SwaggerUI, provided by FastAPI for API interaction.
- **Backend**: FastAPI to handle HTTP requests and responses.
- **Database**: SQLite for simplicity and demonstration purposes.
- **Containerization**: Docker to containerize the application.

### Endpoints

1. Document Patient Interaction:
  - Method: `POST`
  - URL: `/patient/{patient_id}/interaction`
  - Description: Records an interaction with a patient, documenting the outcome.
2. View Patient History:
- Method: `GET`
- URL: `/patient/{patient_id}`
- Description: Retrieves all interactions for a specific patient.
3. List All Patients:
- Method: `GET`
- URL: `/patients`
- Description: Lists all patients in the database.

## Prerequisites

- Docker
- Docker compose

## Steps to run the application

1. Clone the Repository

```
git clone https://github.com/swetayadav0521/DocPad.git
cd DocPad

```

2. Build Docker Image

```
docker-compose build

```
3. Run Docker Container

```
docker-compose up

```

4. Open `http://localhost:8000/docs` to access SwaggerUI and test the API endpoints

5. Press `CTRL+C` to quit the docker.


## Run Testcase

```
python -m pytest tests/*.py

```

## Suggestions for enhancement

1. **Dropdown List for Health Status**: Doctors can select the health status of a patient from a dropdown list with options "Yes" and "No".

#### Benefits:

- Simplifies the process of recording patient health status.
- Reduces the data entry errors.
- Standardizes the data format.

2. **Machine Learning Algorithm for Health Status**: Implement a machine learning algorithm to analyze the "notes" field and automatically determine the patient's health status based on the comments.

#### Benefits:

- Can assist doctors in making more informed decisions.
- Enhances the capability of the application with intelligent features.





