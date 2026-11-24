# Payment Transaction Anomaly Detection

This folder contains the project landing page and the annotated Jupyter notebook.

## Contents

- `index.html` — project page linked from the main project library.
- `notebooks/payment-fraud-detection-annotated.ipynb` — annotated notebook with Markdown explanations before code cells.

## Required existing assets

The project page expects these files to remain in the main `docs/assets` folders:

- `docs/assets/style.css`
- `docs/assets/images/payment-fraud-detection-architecture.drawio.svg`
- `docs/assets/images/payment-fraud-detection-architecture.drawio`

## Dataset

The notebook uses the Kaggle ULB Credit Card Fraud Detection dataset. The dataset is not included in this package. Do not commit the raw CSV to GitHub unless you have checked repository size and dataset licensing/distribution requirements.

The original notebook uses a Kaggle input path. Update the data-loading cell for your local environment before rerunning.

## GitHub Pages

The main dashboard card should link to:

`projects/payment-anomaly-detection/index.html`

The notebook is provided as a downloadable artifact. GitHub Pages does not execute notebook code; run it in Jupyter, JupyterLab or Kaggle.
