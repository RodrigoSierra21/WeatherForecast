# Group14-ML4Industry. Project Instructions

A Python tool to predict weather conditions using machine learning.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Running the Code](#running-the-code)
- [Example Usage](#example-usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Setup Instructions

1. Clone the repository: git clone https://github.com/RSM1234q/Group14-ML4Industry.git
2. Navigate to the project directory.
3. Create a virtual environment: python -m venv venv
4. Activate the virtual environment:
   - Windows: venv\Scripts\activate
   - macOS/Linux: source venv/bin/activate
5. Install the dependencies: pip install -r requirements.txt

## Running the Code

Data Fetching
To fetch data from the APIs:

    1.- Navigate to src/DataProcessing/APIs.
    2.- Run the following scripts:
        Meteorological Data: Fetches meteorological features.
            run: src/DataProcessing/APIs/getMeteorologicalBulk.py
        Target Pollutants Data: Fetches target pollutant data.
            run: src/DataProcessing/APIs/getTargetBulk.py

Database Building

    1.- Navigate to src/DataProcessing/Databases.
    2.- Enter the desired script.
        run: src/DataProcessing/Databases/<script_name>.py

Data Preprocessing

    1.- Navigate to the DataProcessing directory and run dataProcessing.py:
        run: src/DataProcessing/dataProcessing.py

    2.- Visualization
        To generate visualization graphs:
        - Open dataProcessing.py.
        - Uncomment the specified lines for graphing.
        - Re-run the script to see visualizations:

Feature Selection

    1.- Go to src/FeatureSelection and open featureImportances.py:
    2.- Uncomment the variable for the target column you want to use.
    3.- Run the script to execute feature selection:
        run:  src/FeatureSelection/featureImportances.py

Model Training

    1.- Go to src/Models.
    2.- Open modelRunner.
    3.- Uncommnet the model you want to run
    4.- UNcomment the target pollutant you want to train the mdoel for
        run: src/Models/modelRunnner.py
    5.- Optional: Go to src/Models/ModelsClasses, go to the script of the model you want train and
    uncomment the lines for generating visualizations to display graphs during training.

Data Streaming and Monitoring

    To stream the latest data, monitor data distribution shifts, model metrics, and latest predictions:
    1.- Navigate to src/Deployment/Backend.
        run: huggingFaceFunctions.py to automatically execute the entire workflow:

The hugging face repoditory can eb found in: https://huggingface.co/spaces/RaghavTiwari/AirPollution
password : admin
