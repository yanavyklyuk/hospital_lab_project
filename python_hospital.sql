CREATE TABLE IF NOT EXISTS python_hospital.patient (
id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
sex ENUM('male', 'female') NOT NULL,
date_of_birth DATE NOT NULL,
phone_number VARCHAR(15) UNIQUE NOT NULL,
country VARCHAR(100) NOT NULL,
city VARCHAR(100) NOT NULL,
street VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS python_hospital.specialisation (
id INT AUTO_INCREMENT PRIMARY KEY,
specialisation_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS python_hospital.doctor (
id INT AUTO_INCREMENT PRIMARY KEY,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
sex ENUM('male', 'female') NOT NULL,
date_of_birth DATE NOT NULL,
phone_number VARCHAR(100) UNIQUE NOT NULL,
experience INT UNSIGNED NOT NULL,
specialisation_id INT NOT NULL,
CONSTRAINT fk_doctor_specialisation FOREIGN KEY (specialisation_id) 
REFERENCES specialisation(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS python_hospital.schedule (
id INT AUTO_INCREMENT PRIMARY KEY,
start_of_work DATETIME NOT NULL,
end_of_work DATETIME NOT NULL,
time_per_patient_minutes INT NOT NULL,
cabinet_number INT NOT NULL,
doctor_id INT NOT NULL,
CONSTRAINT fk_schedule_doctor FOREIGN KEY (doctor_id)
REFERENCES doctor(id) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT ck_schedule_end_of_work CHECK (end_of_work > start_of_work),
CONSTRAINT ck_schedule_time_per_patient_minutes CHECK (time_per_patient_minutes > 0),
CONSTRAINT ck_schedule_cabinet_number CHECK (cabinet_number > 0),
CONSTRAINT uq_schedule_time_of_work_cabinet_number UNIQUE(start_of_work, end_of_work, cabinet_number)
);

CREATE TABLE IF NOT EXISTS python_hospital.disease (
id INT AUTO_INCREMENT PRIMARY KEY,
disease_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE python_hospital.disease_history (
id INT AUTO_INCREMENT PRIMARY KEY,
disease_duration_days INT NOT NULL,
patient_id INT NOT NULL,
doctor_id INT,
disease_id INT NOT NULL,
CONSTRAINT fk_disease_history_patient FOREIGN KEY (patient_id)
REFERENCES patient(id) ON DELETE RESTRICT ON UPDATE CASCADE,
CONSTRAINT fk_disease_history_doctor FOREIGN KEY (doctor_id)
REFERENCES doctor(id) ON DELETE SET NULL ON UPDATE CASCADE,
CONSTRAINT fk_disease_history_disease FOREIGN KEY (disease_id)
REFERENCES disease(id) ON DELETE RESTRICT ON UPDATE CASCADE,
CONSTRAINT ck_disease_history_disease_duration_days CHECK (disease_duration_days > 0)
); 

CREATE TABLE IF NOT EXISTS python_hospital.favor(
id INT AUTO_INCREMENT PRIMARY KEY,
favor_name VARCHAR(100) NOT NULL,
cost DECIMAL(10, 2) NOT NULL,
CONSTRAINT ck_favor_cost CHECK(cost >= 0)
);

CREATE TABLE IF NOT EXISTS python_hospital.appointment(
id INT AUTO_INCREMENT PRIMARY KEY,
datetime_of_appointment DATETIME NOT NULL,
doctor_id INT NOT NULL,
patient_id INT NOT NULL,
status_name ENUM('scheduled', 'cancelled', 'happened') NOT NULL,
favor_id INT,
CONSTRAINT fk_appointment_doctor FOREIGN KEY (doctor_id)
REFERENCES doctor(id) ON DELETE CASCADE ON UPDATE CASCADE,
CONSTRAINT fk_appointment_patient FOREIGN KEY (patient_id)
REFERENCES patient(id) ON DELETE RESTRICT ON UPDATE CASCADE,
CONSTRAINT fk_appointment_favor FOREIGN KEY (favor_id)
REFERENCES favor(id) ON DELETE SET NULL ON UPDATE CASCADE,
CONSTRAINT uq_appointment_datetime_doctor UNIQUE(datetime_of_appointment, doctor_id),
CONSTRAINT uq_appointment_datetime_patient UNIQUE(datetime_of_appointment, patient_id)
);