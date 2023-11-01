DROP TABLE IF EXISTS Class_Enrollment;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Trainers;
DROP TABLE IF EXISTS Member;

CREATE TABLE Member (
  member_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone_number TEXT NOT NULL,
  dob DATE NOT NULL,
  date_joined DATE NOT NULL,
  membership_type TEXT NOT NULL
);

CREATE TABLE Trainers (
  trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone_number TEXT NOT NULL,
  specialization TEXT NOT NULL
);

CREATE TABLE Class (
  class_id INTEGER PRIMARY KEY AUTOINCREMENT,
  class_name TEXT NOT NULL,
  description TEXT,
  trainer_id INTEGER NOT NULL,
  schedule_time TIME NOT NULL,
  duration INTEGER NOT NULL,
  max_members INTEGER NOT NULL,
  FOREIGN KEY (trainer_id) REFERENCES Trainers (trainer_id)
);

CREATE TABLE Payment (
  payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id INTEGER NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  date DATE NOT NULL,
  payment_method TEXT NOT NULL,
  payment_status TEXT NOT NULL,
  FOREIGN KEY (member_id) REFERENCES Member (member_id)
);

CREATE TABLE Class_Enrollment (
  enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  member_id INTEGER NOT NULL,
  class_id INTEGER NOT NULL,
  date_enrolled DATE NOT NULL,
  FOREIGN KEY (member_id) REFERENCES Member (member_id),
  FOREIGN KEY (class_id) REFERENCES Class (class_id)
);