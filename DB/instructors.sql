CREATE TABLE IF NOT EXISTS lecturers (
    lecturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nms TEXT,
    office TEXT,
    contact TEXT
);

CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL,
    diploma_level TEXT NOT NULL,
    course_name TEXT NOT NULL,
    department TEXT NOT NULL,
    credit_units INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS instructor_courses (
    instructor_course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lecturer_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (lecturer_id) REFERENCES lecturers(lecturer_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);


INSERT INTO lecturers (nms, office, contact) VALUES
('MRS BASSAMA ALHASSAN', 'Room 101', '123-456-7890'),
('MAL BUHARI', 'Room 102', '123-456-7891'),
('DR JOSEPHINE ODENGELE', 'Room 103', '123-456-7892'),
('DR NURA MUSA', 'Room 104', '123-456-7893'),
('MAL KAMALUDEEN', 'Room 105', '123-456-7894'),
('MALLAM MD ABDULLAHI', 'Room 106', '123-456-7895'),
('MRS AIGBE PATIENCE', 'Room 107', '123-456-7896'),
('MAL MUTTAKA JIBRIL', 'Room 108', '123-456-7897'),
('MAL ABUBAKAR SHUAIBU', 'Room 109', '123-456-7898'),
('MR FRIDAY YAKUBU', 'Room 110', '123-456-7899'),
('MAL MAIWADA SHUIABU', 'Room 201', '123-456-7900'),
('MAL ELSADIQ', 'Room 202', '123-456-7901'),
('MAL NURA DARI', 'Room 203', '123-456-7902'),
('ENGNR ABDULWAHAB IBRAHIM', 'Room 204', '123-456-7903'),
('ENGNR ISYAKU YAU', 'Room 205', '123-456-7904'),
('MAL ALIYU NASIR', 'Room 206', '123-456-7905'),
('MRS HALIMA MUSA', 'Room 207', '123-456-7906'),
('MR OZIGI ABDULRAZAK', 'Room 208', '123-456-7907'),
('Mrs Esther Gabriel Baba', 'Room 209', '123-456-7908');


INSERT INTO courses (course_code, diploma_level, course_name, department, credit_units, description) VALUES
('DCS101', 'Diploma 1', 'Introduction to Computer technology', 'Computer Science', 2, 'History of technology, First Computers, Types of Computers.'),
('DCS102', 'Diploma 1', 'Discrete Mathematics', 'Computer Science', 3, 'Study of mathematical structures in computer science.'),
('DCS103', 'Diploma 1', 'Digital Logic Design', 'Computer Science', 4, 'Introduction to digital circuits and logic design.'),
('DCS104', 'Diploma 1', 'Data Structures', 'Computer Science', 4, 'Introduction to data structures and algorithms.'),
('DCS105', 'Diploma 1', 'Computer Organization', 'Computer Science', 3, 'Understanding computer architecture and organization.'),
('DCS106', 'Diploma 1', 'Object-Oriented Programming', 'Computer Science', 4, 'Advanced programming using object-oriented concepts.'),
('DCS107', 'Diploma 1', 'Operating Systems', 'Computer Science', 3, 'Principles of operating systems and processes.'),
('DCS108', 'Diploma 1', 'Database Systems', 'Computer Science', 4, 'Introduction to database design and SQL.'),
('DCS109', 'Diploma 1', 'Computer Networks', 'Computer Science', 3, 'Basics of networking and data communication.'),
('DCS110', 'Diploma 1', 'Software Engineering', 'Computer Science', 4, 'Fundamentals of software development and management.'),
('DCS202', 'Diploma 2', 'Theory of Computation', 'Computer Science', 4, 'Study of automata, computability, and complexity.'),
('DCS203', 'Diploma 2', 'Compiler Design', 'Computer Science', 4, 'Introduction to the design and implementation of compilers.'),
('DCS204', 'Diploma 2', 'Artificial Intelligence', 'Computer Science', 3, 'Basics of AI, including machine learning and robotics.'),
('DCS205', 'Diploma 2', 'Machine Learning', 'Computer Science', 4, 'Introduction to machine learning algorithms and applications.'),
('DCS206', 'Diploma 2', 'Computer Graphics', 'Computer Science', 4, 'Fundamentals of computer graphics and visualization.'),
('DCS207', 'Diploma 2', 'Web Development', 'Computer Science', 3, 'Study of web technologies and development practices.'),
('DCS208', 'Diploma 2', 'Mobile Application Development', 'Computer Science', 4, 'Design and development of mobile applications.'),
('DCS209', 'Diploma 2', 'Cyber Security', 'Computer Science', 3, 'Principles of cybersecurity and information protection.'),
('DCS210', 'Diploma 2', 'Distributed Systems', 'Computer Science', 4, 'Introduction to distributed computing systems.'),
('DCE101', 'Diploma 1', 'Circuit Theory', 'Computer Engineering', 3, 'Fundamentals of electrical circuits and systems.'),
('DCE103', 'Diploma 1', 'Signals and Systems', 'Computer Engineering', 4, 'Study of signals, systems, and signal processing.'),
('DCE104', 'Diploma 1', 'Electromagnetics', 'Computer Engineering', 4, 'Introduction to electromagnetic fields and waves.'),
('DCE105', 'Diploma 1', 'Microprocessors', 'Computer Engineering', 4, 'Basics of microprocessor architecture and programming.'),
('DCE106', 'Diploma 1', 'Digital Electronics', 'Computer Engineering', 4, 'Advanced study of digital circuits and systems.'),
('DCE107', 'Diploma 1', 'Communication Systems', 'Computer Engineering', 3, 'Principles of communication systems and networks.'),
('DCE108', 'Diploma 1', 'Control Systems', 'Computer Engineering', 4, 'Study of control systems and automation.'),
('DCE109', 'Diploma 1', 'Power Electronics', 'Computer Engineering', 3, 'Introduction to power electronics and converters.'),
('DCE110', 'Diploma 1', 'Embedded Systems', 'Computer Engineering', 4, 'Fundamentals of embedded systems design.'),
('DCE201', 'Diploma 2', 'Advanced Circuit Theory', 'Computer Engineering', 4, 'Advanced study of electrical circuit analysis and design.'),
('DCE202', 'Diploma 2', 'Electronics II', 'Computer Engineering', 4, 'Continuation of electronics with complex circuits.'),
('DCE203', 'Diploma 2', 'Digital Signal Processing', 'Computer Engineering', 4, 'Introduction to digital signal processing techniques.'),
('DCE204', 'Diploma 2', 'Antennas and Wave Propagation', 'Computer Engineering', 4, 'Study of antennas and electromagnetic wave propagation.'),
('DCE205', 'Diploma 2', 'VLSI Design', 'Computer Engineering', 4, 'Basics of VLSI technology and circuit design.'),
('DCE206', 'Diploma 2', 'Robotics and Automation', 'Computer Engineering', 4, 'Principles of robotics, automation, and control.'),
('DCE207', 'Diploma 2', 'Analog and Digital Communication', 'Computer Engineering', 4, 'Study of analog and digital communication techniques.'),
('DCE208', 'Diploma 2', 'Power Systems', 'Computer Engineering', 3, 'Introduction to power generation, transmission, and distribution.'),
('DCE209', 'Diploma 2', 'Advanced Embedded Systems', 'Computer Engineering', 4, 'In-depth study of embedded systems design and applications.'),
('DCE210', 'Diploma 2', 'Renewable Energy Systems', 'Computer Engineering', 3, 'Fundamentals of renewable energy technologies and systems.');


-- Assuming the 'instructor_id' and 'course_id' are mapped as follows:
-- We are using pseudo IDs here; you would need to replace these with actual IDs from your 'instructors' and 'courses' tables.

INSERT INTO instructor_courses (lecturer_id, course_id) VALUES
-- MRS BASSAMA ALHASSAN
(1, 1),  -- DCS101
(1, 19), -- DCE101
(1, 39), -- DCE210

-- MAL BUHARI
(2, 2),  -- DCS102
(2, 20), -- DCE102

-- DR JOSEPHINE ODENGELE
(3, 3),  -- DCS103
(3, 21), -- DCE103

-- DR NURA MUSA
(4, 4),  -- DCS104
(4, 22), -- DCE104

-- MAL KAMALUDEEN
(5, 5),  -- DCS105
(5, 23), -- DCE105

-- MALLAM MD ABDULLAHI
(6, 6),  -- DCS106
(6, 24), -- DCE106

-- MRS AIGBE PATIENCE
(7, 7),  -- DCS107
(7, 25), -- DCE107

-- MAL MUTTAKA JIBRIL
(8, 8),  -- DCS108
(8, 26), -- DCE108

-- MAL ABUBAKAR SHUAIBU
(9, 9),  -- DCS109
(9, 27), -- DCE109

-- MR FRIDAY YAKUBU
(10, 10), -- DCS110
(10, 28), -- DCE110

-- MAL MAIWADA SHUIABU
(11, 11), -- DCS202
(11, 29), -- DCE201

-- MAL ELSADIQ
(12, 12), -- DCS203
(12, 30), -- DCE202

-- MAL NURA DARI
(13, 13), -- DCS204
(13, 31), -- DCE203

-- ENGNR ABDULWAHAB IBRAHIM
(14, 14), -- DCS205
(14, 32), -- DCE204

-- ENGNR ISYAKU YAU
(15, 15), -- DCS206
(15, 33), -- DCE205

-- MAL ALIYU NASIR
(16, 16), -- DCS207
(16, 34), -- DCE206

-- MRS HALIMA MUSA
(17, 17), -- DCS208
(17, 35), -- DCE207

-- MR OZIGI ABDULRAZAK
(18, 18), -- DCS209
(18, 36), -- DCE208

-- Mrs Esther Gabriel Baba
(19, 19), -- DCS210
(19, 37); -- DCE209
