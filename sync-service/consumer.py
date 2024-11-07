from kafka import KafkaConsumer
import requests
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("patient_consumer.log"),
        logging.StreamHandler()
    ]
)

# Kafka Consumer configuration
consumer = KafkaConsumer(
    'hospital.hospital.patients',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='dcm4chee-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x else None
)

# DCM4CHEE PACS REST API endpoint for creating patients
dcm4chee_url = 'http://arc:8080/dcm4chee-arc/aets/DCM4CHEE/rs/patients'

# Listen for messages from Kafka
for message in consumer:
    try:
        patient_data = message.value.get('after') if message.value else None
        if not patient_data:
            logging.warning("Received an empty or invalid message, skipping...")
            continue

        # Log the raw data retrieved from Kafka
        logging.info(f"Retrieved data from Kafka: {patient_data}")

        # Format the data for DCM4CHEE request
        dcm4chee_patient_data = {
            "00100010": {  # Patient Name
                "vr": "PN",
                "Value": [{"Alphabetic": patient_data.get("PatientName").replace(" ", "^")}]  # Assuming format "Last^First"
            },
            "00100020": {  # Patient ID
                "vr": "LO",
                "Value": [patient_data.get("PatientID")]
            },
            "00100021": {  # Medical Record Number (if applicable)
                "vr": "LO",
                "Value": [patient_data.get("PatientID")]
            },
            "00100030": {  # Date of Birth
                "vr": "DA",
                "Value": [datetime.strptime(str(patient_data.get("PatientBirthDate")), "%Y%m%d").strftime("%Y%m%d")]
                if patient_data.get("birth_date") else []
            },
            "00100040": {  # Gender
                "vr": "CS",
                "Value": [patient_data.get("PatientSex")]
            }
        }

        # Log the formatted data
        logging.info(f"Formatted data for DCM4CHEE: {json.dumps(dcm4chee_patient_data, indent=2)}")

        # Send the patient data to DCM4CHEE PACS system
        response = requests.post(dcm4chee_url, json=dcm4chee_patient_data)
        response.raise_for_status()
        logging.info(f"Patient {patient_data['PatientID']} created successfully in DCM4CHEE.")

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed for message: {message.value}. Error: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create patient {patient_data.get('PatientID')} in DCM4CHEE: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
