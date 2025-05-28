## Prerequisites

- Stup Vertex AI api in gcp, Activate Vertex API
- setup gcloud CLI for easy authentication follow this (https://cloud.google.com/sdk/docs/install) or use the authentication settigns of GCP
- Python 3.9+ environment

Setting up virtual environment (bash)
conda create --name hsnAgent python=3.10
conda activate hsnAgent
pip install -r requirements.txt

gloud after installation might not be detected in your new env check it using
gcloud --version

positive - (hsnAgent) ayan@ayan--Laptop-14-ec0xxx:~/Desktop/hsn-agent$ gcloud --version
Google Cloud SDK 523.0.1
bq 2.1.17
bundled-python3-unix 3.12.9
core 2025.05.22
gcloud-crc32c 1.0.0
gsutil 5.34

if doesnt then find out the SDK's binary path and add it to the system's PATH environment variable

gcloud init and configure the gcp project

adk web
