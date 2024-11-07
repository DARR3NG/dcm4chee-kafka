## Step 1

1. Clone the repository:
   ```bash
   git clone https://github.com/DARR3NG/dcm4chee-kafka.git

   cd dcm4chee-kafka
   
   docker-compose up -d
## Step 2
1. Access the MySQL container:
   ```bash
   docker exec -it container_mysql mysql -h localhost -u root -p hospital
  
Note: The root password is password.


2. Run the following SQL commands to set up the database:
      ```bash

   CREATE TABLE patients (    PatientID VARCHAR(50) PRIMARY KEY, PatientName VARCHAR(100), DateOfBirth DATE, Gender CHAR(1), Address VARCHAR(200), PhoneNumber VARCHAR(50), MedicalRecordNumber VARCHAR(50), SSN VARCHAR(20) );

   INSERT INTO patients (PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber, MedicalRecordNumber, SSN)
   VALUES
   ('M4125', 'Otmane^Elkastali', '1945-08-04', 'M', '820 JORIE BLVD^^CHICAGO^IL^60523', '(314)555-1212', '20-98-4000', NULL);

   GRANT ALL PRIVILEGES ON *.* TO 'debezium'@'%';
   FLUSH PRIVILEGES;
   exit

## Step 3
1. Send a curl request to the Kafka Connect server to start a connector with the configuration file debezium-config.json:
   ```bash
   curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors --data @debezium-config.json

3. Connect to the broker container. First, get the IP address of the service:
   ```bash
   docker inspect container_broker
5. Start a session in the broker container:
   ```bash
   docker exec -it container_broker bash
7. List Kafka topics:
   ```bash
   bin/kafka-topics.sh --list --bootstrap-server your-broker-ip:9092
   
Expected output:
   ```bash
   __consumer_offsets
   kafka_connect_configs
   kafka_connect_offsets
   kafka_connect_statuses
   schema-changes
   patients
   hospital.hospital.patients
   ```

5. Consume data from the hospital.hospital.patients topic to monitor table data:
   ```bash
   bin/kafka-console-consumer.sh --bootstrap-server your-broker-ip:9092 --topic testdb.testdb.test_table --from-beginning

Example output:
   ```bash
{"before":null,"after":{"PatientID":"M4125","PatientName":"Otmane^Elkastali","DateOfBirth":-8916,"Gender":"M","Address":"820 JORIE BLVD^^CHICAGO^IL^60523","PhoneNumber":"(314)555-1212","MedicalRecordNumber":"20-98-4000","SSN":null},"source":{"version":"3.0.0.Final","connector":"mysql","name":"hospital","ts_ms":1730996374000,"snapshot":"false","db":"hospital","sequence":null,"ts_us":1730996374000000,"ts_ns":1730996374000000000,"table":"patients","server_id":1,"gtid":null,"file":"binlog.000021","pos":792,"row":0,"thread":12,"query":null},"transaction":null,"op":"c","ts_ms":1730996374211,"ts_us":1730996374211528,"ts_ns":1730996374211528196}
   ```


## Step 4
1. Access the MySQL container:
   ```` bash
   docker exec -it container_mysql mysql -h localhost -u root -p hospital
Note: The root password is password.

2. Insert a patient :
   ```bash
   INSERT INTO patients (PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber, MedicalRecordNumber, SSN)
   VALUES
   ('M4126', 'test^test', '1945-08-04', 'M', '820 JORIE BLVD^^CHICAGO^IL^60523', '(314)555-1212', '20-98-4000', NULL);

3. Check dcm4chee ui :

   















