-- Create the timetable table
CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dayz TEXT,
    timez TEXT,
    course_code TEXT,
    venue TEXT,
    instructor TEXT,
    program TEXT
);

-- Insert timetable for Diploma One
INSERT INTO timetable (dayz, timez, course_code, venue, instructor, program) VALUES
('Monday', '8am to 10am', 'DCS101', 'Room 101', 'MRS BASSAMA ALHASSAN', 'Diploma One'),
('Monday', '10am to 12pm', 'DCS102', 'Room 102', 'MAL BUHARI', 'Diploma One'),
('Monday', '2pm to 4pm', 'DCS103', 'Room 103', 'DR JOSEPHINE ODENGELE', 'Diploma One'),
('Monday', '4pm to 6pm', 'DCS104', 'Room 104', 'DR NURA MUSA', 'Diploma One'),
('Tuesday', '8am to 10am', 'DCS105', 'Room 105', 'MAL KAMALUDEEN', 'Diploma One'),
('Tuesday', '10am to 12pm', 'DCS106', 'Room 106', 'MALLAM MD ABDULLAHI', 'Diploma One'),
('Tuesday', '2pm to 4pm', 'DCS107', 'Room 107', 'MRS AIGBE PATIENCE', 'Diploma One'),
('Tuesday', '4pm to 6pm', 'DCS108', 'Room 108', 'MAL MUTTAKA JIBRIL', 'Diploma One'),
('Wednesday', '8am to 10am', 'DCS109', 'Room 109', 'MAL ABUBAKAR SHUAIBU', 'Diploma One'),
('Wednesday', '10am to 12pm', 'DCS110', 'Room 110', 'MR FRIDAY YAKUBU', 'Diploma One'),
('Wednesday', '2pm to 4pm', 'DCE101', 'Room 201', 'MAL MAIWADA SHUIABU', 'Diploma One'),
('Wednesday', '4pm to 6pm', 'DCE102', 'Room 202', 'MAL ELSADIQ', 'Diploma One'),
('Thursday', '8am to 10am', 'DCE103', 'Room 203', 'MAL NURA DARI', 'Diploma One'),
('Thursday', '10am to 12pm', 'DCE104', 'Room 204', 'ENGNR ABDULWAHAB IBRAHIM', 'Diploma One'),
('Thursday', '2pm to 4pm', 'DCE105', 'Room 205', 'ENGNR ISYAKU YAU', 'Diploma One'),
('Thursday', '4pm to 6pm', 'DCE106', 'Room 206', 'MAL ALIYU NASIR', 'Diploma One'),
('Friday', '8am to 10am', 'DCE107', 'Room 207', 'MRS HALIMA MUSA', 'Diploma One'),
('Friday', '10am to 12pm', 'DCE108', 'Room 208', 'MR OZIGI ABDULRAZAK', 'Diploma One'),
('Friday', '2pm to 4pm', 'DCE109', 'Room 209', 'Mrs Esther Gabriel Baba', 'Diploma One');

-- Insert timetable for Diploma Two
INSERT INTO timetable (dayz, timez, course_code, venue, instructor, program) VALUES
('Monday', '8am to 10am', 'DCS201', 'Room 101', 'MRS BASSAMA ALHASSAN', 'Diploma Two'),
('Monday', '10am to 12pm', 'DCS202', 'Room 102', 'MAL BUHARI', 'Diploma Two'),
('Monday', '2pm to 4pm', 'DCS203', 'Room 103', 'DR JOSEPHINE ODENGELE', 'Diploma Two'),
('Monday', '4pm to 6pm', 'DCS204', 'Room 104', 'DR NURA MUSA', 'Diploma Two'),
('Tuesday', '8am to 10am', 'DCS205', 'Room 105', 'MAL KAMALUDEEN', 'Diploma Two'),
('Tuesday', '10am to 12pm', 'DCS206', 'Room 106', 'MALLAM MD ABDULLAHI', 'Diploma Two'),
('Tuesday', '2pm to 4pm', 'DCS207', 'Room 107', 'MRS AIGBE PATIENCE', 'Diploma Two'),
('Tuesday', '4pm to 6pm', 'DCS208', 'Room 108', 'MAL MUTTAKA JIBRIL', 'Diploma Two'),
('Wednesday', '8am to 10am', 'DCS209', 'Room 109', 'MAL ABUBAKAR SHUAIBU', 'Diploma Two'),
('Wednesday', '10am to 12pm', 'DCS210', 'Room 110', 'MR FRIDAY YAKUBU', 'Diploma Two'),
('Wednesday', '2pm to 4pm', 'DCE201', 'Room 201', 'MAL MAIWADA SHUIABU', 'Diploma Two'),
('Wednesday', '4pm to 6pm', 'DCE202', 'Room 202', 'MAL ELSADIQ', 'Diploma Two'),
('Thursday', '8am to 10am', 'DCE203', 'Room 203', 'MAL NURA DARI', 'Diploma Two'),
('Thursday', '10am to 12pm', 'DCE204', 'Room 204', 'ENGNR ABDULWAHAB IBRAHIM', 'Diploma Two'),
('Thursday', '2pm to 4pm', 'DCE205', 'Room 205', 'ENGNR ISYAKU YAU', 'Diploma Two'),
('Thursday', '4pm to 6pm', 'DCE206', 'Room 206', 'MAL ALIYU NASIR', 'Diploma Two'),
('Friday', '8am to 10am', 'DCE207', 'Room 207', 'MRS HALIMA MUSA', 'Diploma Two'),
('Friday', '10am to 12pm', 'DCE208', 'Room 208', 'MR OZIGI ABDULRAZAK', 'Diploma Two'),
('Friday', '2pm to 4pm', 'DCE209', 'Room 209', 'Mrs Esther Gabriel Baba', 'Diploma Two');
