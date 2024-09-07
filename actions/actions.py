import sqlite3
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
import textwrap
import os
import random
import urllib.parse



class ActionCourseDetails(Action):

    def name(self) -> Text:
        return "action_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("ActionCourseDetails has been triggered")  # Debugging
        
        # Connect to the SQLite database
        conn = sqlite3.connect('DB/courses.db')
        cursor = conn.cursor()
    
        # Extract the course_code and course_name from the user's message
        course_code = next(tracker.get_latest_entity_values("course_code"), None)
        course_name = next(tracker.get_latest_entity_values("course_name"), None)
        print(f"course_code: {course_code}, course_name: {course_name}")  # Debugging

        # Get the intent name to determine the type of query
        intent_name = tracker.get_intent_of_latest_message()

        # Handle course registration queries specifically
        if "course registration" in tracker.latest_message['text'].lower() or \
           ("register" in tracker.latest_message['text'].lower() and "course" in tracker.latest_message['text'].lower()):
            dispatcher.utter_message(text="To perform your course registration, please follow the steps below:")
            dispatcher.utter_message(text="""
                1. Visit the school portal at https://www.portal.abu.edu.ng and login with your registration number and password.
                2. Click on the Course Registration Tab and select the current session which you wish to register.
                3. Wait for it to load and then select the semester which you wish to register (either first or second semester).
                4. Wait for it to load and then click on 'Show More Courses'.
                5. After the dialog box opens, select IAIICT as the Faculty and either Computer Science or Computer Engineering as the department. Then select your level (either Diploma 1 or Diploma 2).
                6. Click on 'Courses' to select the courses you wish to register.
                7. Carefully follow through and select all courses you have for the semester.
                8. After selecting a course, click the button titled 'Show on List'.
                9. Select your respective lecture and lab groups.
                10. Activate the checkbox at the end of each course row, which will prompt you to input the course name for confirmation.
                11. After confirming all desired courses, click on the 'Print Form' button at the bottom of the page and save your course form as a PDF file.
            """)
            dispatcher.utter_message(text="Congratulations! You have successfully completed your course registration.")
        
        # Handle course details queries
        elif intent_name == "course_details":
            if course_code:
                if "title" in tracker.latest_message['text'].lower():
                    cursor.execute("SELECT title FROM courses WHERE course_code = ?", (course_code,))
                    result = cursor.fetchone()
                    if result:
                        dispatcher.utter_message(text=f"The course title for {course_code} is {result[0]}.")
                    else:
                        dispatcher.utter_message(text=f"Sorry, the title for {course_code} not found.")
                
                elif "credit units" in tracker.latest_message['text'].lower():
                    cursor.execute("SELECT credit_units FROM courses WHERE course_code = ?", (course_code,))
                    result = cursor.fetchone()
                    if result:
                        dispatcher.utter_message(text=f"The credit units for {course_code} are {result[0]}.")
                    else:
                        dispatcher.utter_message(text=f"No credit units information found for {course_code}.")
                
                elif "department" in tracker.latest_message['text'].lower():
                    cursor.execute("SELECT department FROM courses WHERE course_code = ?", (course_code,))
                    result = cursor.fetchone()
                    if result:
                        dispatcher.utter_message(text=f"The department offering {course_code} is {result[0]}.")
                    else:
                        dispatcher.utter_message(text=f"No department information found for {course_code}.")
                
                elif "description" in tracker.latest_message['text'].lower():
                    cursor.execute("SELECT description FROM courses WHERE course_code = ?", (course_code,))
                    result = cursor.fetchone()
                    if result:
                        dispatcher.utter_message(text=f"The description for {course_code} is: {result[0]}.")
                    else:
                        dispatcher.utter_message(text=f"No description found for {course_code}.")
                
                elif "outline" in tracker.latest_message['text'].lower():
                    cursor.execute("SELECT outline FROM courses WHERE course_code = ?", (course_code,))
                    result = cursor.fetchone()
                    if result:
                        dispatcher.utter_message(text=f"The course outline for {course_code} is: {result[0]}.")
                    else:
                        dispatcher.utter_message(text=f"No outline found for {course_code}.")
                        
                elif "tell me" in tracker.latest_message['text'].lower() or "about" in tracker.latest_message['text'].lower():
                    cursor.execute("SELECT course_code, title, credit_units, department, lev, outline FROM courses WHERE course_code = ?", (course_code,))
                    result = cursor.fetchone()
                    
                    if result:
                        course_code, title, credit_units, department, lev, outline = result
                        dispatcher.utter_message(
                            text=(
                                f"Here are the details for course {course_code}:\n\n"
                                f"**Title**: {title}\n"
                                f"**Credit Units**: {credit_units}\n"
                                f"**Department**: {department}\n"
                                f"**Level**: {lev}\n"
                                f"**Outline**: {outline}\n"
                            )
                        )
                    else:
                        dispatcher.utter_message(text=f"No course details found for {course_code}.")
       
            
            elif course_name:
                cursor.execute("SELECT course_code, title FROM courses WHERE title LIKE ?", ('%' + course_name + '%',))
                result = cursor.fetchone()
                if result:
                    dispatcher.utter_message(text=f"The course code for {course_name} is {result[0]} and the title is {result[1]}.")
                else:
                    dispatcher.utter_message(text=f"No course found with the name {course_name}.")
            else:
                dispatcher.utter_message(text="Please provide a valid course code or course name.")     

        else:
            dispatcher.utter_message(text="Please provide a course code or course name to proceed.")
        
        # Close the database connection
        conn.close()

        return []
    


class ActionTimeTableDetails(Action):
    def name(self) -> Text:
        return "action_timetable_details"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("ActionTimeTableDetails has been triggered")  # Debugging
        
        # Connect to the SQLite database
        conn = sqlite3.connect('DB/timetable.db')
        cursor = conn.cursor()
        print("Timetable Database has been connected successfully")  # Debugging
        
        # Extract entities from the user's message
        day = next(tracker.get_latest_entity_values("day"), None)
        course_code = next(tracker.get_latest_entity_values("course_code"), None)
        print(f"day: {day}, course_code: {course_code}")  # Debugging
        
        # Get the full user message text to handle more complex queries
        user_message = tracker.latest_message['text'].lower()
        
        # Use today's date only if "today" is explicitly mentioned and no day is provided
        if not day and "today" in user_message:
            day = datetime.now().strftime('%A')  # Get the current day name (e.g., "Monday")
            print(f"Defaulting to today's day: {day}")  # Debugging
        
        # Handle weekly timetable query
    
        if "week" in user_message and ("timetable" in user_message or "schedule" in user_message):
            cursor.execute("""
                SELECT dayz, course_code, timez, venue, instructor 
                FROM timetable 
                ORDER BY id, timez
            """)
            results = cursor.fetchall()
            if results:
                timetable_message = "Your schedule for this week is:\n"
                
                current_day = None
                for day, course, time, venue, instructor in results:
                    if day != current_day:
                        if current_day is not None:
                            timetable_message += "\n"  # Add a blank line before starting a new day
                        timetable_message += f"{day}:\n"
                        current_day = day
                    timetable_message += f"  - {course} at {time} in {venue}, taught by {instructor}\n"
                
                dispatcher.utter_message(text=timetable_message)
            else:
                dispatcher.utter_message(text="No schedule found for this week.")

        
        # Handle specific day or course code query
        elif day or course_code:
            query = "SELECT dayz, course_code, timez, venue, instructor FROM timetable WHERE 1=1"
            params = []
            
            if day:
                query += " AND dayz = ?"
                params.append(day.capitalize())
                
            if course_code:
                query += " AND course_code = ?"
                params.append(course_code.upper())
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            if results:
                timetable_message = f"Your schedule for {day.capitalize()} is:\n" if day else "The Classes you have on {day} are:\n"
                for day, course, time, venue, instructor in results:
                    timetable_message += f"- {day}:\n\n\n {course} at {time} in {venue}, taught by {instructor}\n"
                dispatcher.utter_message(text=timetable_message)
            else:
                if day:
                    dispatcher.utter_message(text=f"You have no classes scheduled for {day.capitalize()}.")
                else:
                    dispatcher.utter_message(text="No classes found.")
        
        # Handle queries about a particular course (time and venue)
        elif "where" in user_message or "when" in user_message:
            if course_code:
                cursor.execute("""
                    SELECT dayz, timez, venue, instructor 
                    FROM timetable 
                    WHERE course_code = ?
                """, (course_code.upper(),))
                result = cursor.fetchone()
                if result:
                    dispatcher.utter_message(text=f"{course_code.upper()} is held on {result[0]} at {result[1]} in {result[2]}, taught by {result[3]}.")
                else:
                    dispatcher.utter_message(text=f"No schedule found for {course_code.upper()}.")
            else:
                dispatcher.utter_message(text="Please provide a valid course code.")
        
        else:
            dispatcher.utter_message(text="I'm not sure how to help with that. Could you please provide more details?")
        
        # Close the database connection
        conn.close()

        return []

class ActionInstructorDetails(Action):
    def name(self) -> Text:
        return "action_instructor_details"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("ActionInstructorDetails has been triggered")  # Debugging
        
        # Connect to the SQLite database
        conn = sqlite3.connect('DB/instructors.db')
        cursor = conn.cursor()
        print("Instructors Database has been connected successfully")  # Debugging
        
        # Extract entities from the user's message
        course_code = next(tracker.get_latest_entity_values("course_code"), None)
        instructor_name = next(tracker.get_latest_entity_values("instructor"), None)
        user_message = tracker.latest_message['text'].lower()
        # Normalize extracted entities
        if instructor_name:
            instructor_name = instructor_name.strip().title()  # Normalize to title case
        
        print(f"Extracted course_code: {course_code}, instructor_name: {instructor_name}")
        
        
        if course_code:
            # If the user is asking about the lecturer for a specific course
            if "who" in user_message and ("lecturer" in user_message or "teaching" in user_message or "taking" in user_message):
                cursor.execute("""
                    SELECT l.nms 
                    FROM lecturers l
                    JOIN instructor_courses ic ON l.lecturer_id = ic.lecturer_id
                    JOIN courses c ON c.course_id = ic.course_id
                    WHERE c.course_code = ?
                """, (course_code,))
                result = cursor.fetchone()
                if result:
                    name = result[0]
                    dispatcher.utter_message(text=f"The lecturer for {course_code} is {name}.")
                else:
                    dispatcher.utter_message(text=f"No lecturer found for {course_code}.")
            
            # If the user is asking for the lecturer's contact details
            elif "contact" in user_message or "phone" in user_message:
                cursor.execute("""
                    SELECT l.nms, l.contact 
                    FROM lecturers l
                    JOIN instructor_courses ic ON l.lecturer_id = ic.lecturer_id
                    JOIN courses c ON c.course_id = ic.course_id
                    WHERE c.course_code = ?
                """, (course_code,))
                result = cursor.fetchone()
                if result:
                    name, contact = result
                    dispatcher.utter_message(text=f"The contact for the lecturer of {course_code} ({name}) is {contact}.")
                else:
                    dispatcher.utter_message(text=f"No contact details found for the lecturer of {course_code}.")
            
            # If the user is asking for the lecturer's office location
            elif "office" in user_message or "where" in user_message:
                cursor.execute("""
                    SELECT l.nms, l.office 
                    FROM lecturers l
                    JOIN instructor_courses ic ON l.lecturer_id = ic.lecturer_id
                    JOIN courses c ON c.course_id = ic.course_id
                    WHERE c.course_code = ?
                """, (course_code,))
                result = cursor.fetchone()
                if result:
                    name, office = result
                    dispatcher.utter_message(text=f"The office for the lecturer of {course_code} ({name}) is at {office}.")
                else:
                    dispatcher.utter_message(text=f"No office details found for the lecturer of {course_code}.")
        
        elif instructor_name:
            # If the user is asking what course(s) a specific lecturer is teaching
            if "course" in user_message or "teaching" in user_message or "taking" in user_message:
                cursor.execute("""
                    SELECT c.course_code 
                    FROM courses c
                    JOIN instructor_courses ic ON c.course_id = ic.course_id
                    JOIN lecturers l ON l.lecturer_id = ic.lecturer_id
                    WHERE l.nms = ?
                """, (instructor_name,))
                result = cursor.fetchall()
                if result:
                    courses = ', '.join([row[0] for row in result])
                    dispatcher.utter_message(text=f"{instructor_name} is teaching the following course(s): {courses}.")
                else:
                    dispatcher.utter_message(text=f"No courses found for lecturer {instructor_name}.")
            
            # If the user is asking for the lecturer's office location by name
            elif "office" in user_message or "where" in user_message:
                cursor.execute("""
                    SELECT office 
                    FROM lecturers 
                    WHERE nms = ?
                """, (instructor_name,))
                result = cursor.fetchone()
                if result:
                    office = result[0]
                    dispatcher.utter_message(text=f"The office for {instructor_name} is at {office}.")
                else:
                    dispatcher.utter_message(text=f"No office details found for {instructor_name}.")
            
            # If the user is asking for the lecturer's contact details by name
            elif "contact" in user_message or "phone" in user_message:
                cursor.execute("""
                    SELECT contact 
                    FROM lecturers 
                    WHERE nms = ?
                """, (instructor_name,))
                result = cursor.fetchone()
                if result:
                    contact = result[0]
                    dispatcher.utter_message(text=f"The contact for {instructor_name} is {contact}.")
                else:
                    dispatcher.utter_message(text=f"No contact details found for {instructor_name}.")
                    
            elif ("who is" in user_message or "tell me about" in user_message) and instructor_name:
                instructor_namez = instructor_name.upper()
                cursor.execute("""
                    SELECT l.contact, l.office, c.course_code, c.course_name 
                    FROM lecturers l
                    JOIN instructor_courses ic ON l.lecturer_id = ic.lecturer_id
                    JOIN courses c ON c.course_id = ic.course_id
                    WHERE l.nms = ?
                """, (instructor_namez,))
                result = cursor.fetchone()
                if result:
                    contact, office, course_code, course_name = result
                    dispatcher.utter_message(
                        text=f"{instructor_name} is an instructor at IAIICT, located at {office}. "
                            f"{instructor_name} is taking {course_code}: {course_name}. "
                            f"The contact for {instructor_name} is: {contact}."
                    )
                else:
                    dispatcher.utter_message(text=f"No details found for {instructor_name}.")
                
                    
        else:
            dispatcher.utter_message(text="Please provide a valid course code or instructor name.")
        
        # Close the database connection
        conn.close()

        return []



class ActionIAIICTInfo(Action):
    def name(self) -> Text:
        return "action_iaiict_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get('text').lower()
        
        if "tell me about" in user_message and "iaiict" in user_message:
            response = """IAIICT, which stands for IYA ABUBAKAR INSTITUTE OF ICT, is a leading institution focused on providing education and training in computer technology. It is located in Ahmadu Bello University, Zaria.

The institute, originally named Iya Abubakar Computer Centre (IACC) in 1982, was established in 1973 after being detached from the Department of Mathematics, which had set it up in 1967 to provide computer services. The Centre was strategically important to ABU as its staff provided computing support to academic departments, contributing to the advancement of knowledge at the highest levels.

At that time, IACC was a hub of research activities, attracting researchers from across the country and beyond who leveraged its computing facilities and staff to create knowledge in their fields. Both staff and students received programming instruction at the Centre, which eventually led to a growing demand for training in computing activities.

By the 1990s, the computing field had exploded in technology and education, providing further impetus for the Centre to grow and address emerging needs in the broader society. The Centre faced increasing pressure to reinvigorate its longstanding mandate of pioneering computing services and education.

The experience gained through its multifaceted services connected well with the telecommunications and software development sectors of the economy. In response, the University Senate, at its 116th meeting, approved the introduction of two new diploma programs: Diploma in Computer Science and Diploma in Computer Engineering. These programs aimed to (1) develop skilled manpower in software development, database administration, network maintenance, web application development, and computer systems administration, and (2) create a breeding ground for feeding degree-level computing programs with quality students.

The duration of each diploma program is two academic years, comprising four semesters. The programs formally commenced in the 2008/2009 academic year with an initial intake of 56 students.
"""

        elif "where is" in user_message and "iaiict" in user_message:
            response = "IAIICT, which stands for IYA ABUBAKAR INSTITUTE OF ICT, is a leading institution focused on providing education and training in computer technology. It is located in Ahmadu Bello University, Zaria."
        
        elif "programs offered" in user_message or "tell me about the programs" in user_message:
            response = """IAIICT offers a variety of programs aimed at developing skilled professionals in the field of information and communication technology. The major programs include:

1. **Diploma in Computer Science:** This program focuses on foundational and advanced topics in computer science, preparing students for careers in software development, database management, and systems administration.

2. **Diploma in Computer Engineering:** This program emphasizes the hardware and software aspects of computing, training students in areas such as network maintenance, computer hardware design, and embedded systems.

3. **Diploma in Information Technology:** A comprehensive program that covers various IT disciplines, including web development, cybersecurity, and IT project management.

4. **Advanced Diploma in Networking:** This program is designed for students who wish to specialize in network administration, covering topics like network security, wireless communications, and advanced networking protocols.

5. **Certificate Courses:** IAIICT also offers short-term certificate courses in areas like programming languages, database management, and cybersecurity, providing specialized training for specific skills.

Each program is designed to equip students with the necessary skills and knowledge to excel in the rapidly evolving ICT industry.
"""

        
        elif "how much is the school fees" in user_message or "tuition" in user_message:
            response = """Registration fees for the Diploma programmes is the same for each of the programmes but is
subject to change with time and courses requirements. The management of the Iya Abubakar
Computer Centre is responsible for the review of fees to be paid. From the 2008/2009 academic
session, the registration fees shall be N60, 000.00. A candidate who fails to pay up his/her
registration within the stipulated period shall be required to pay late registration fee before
he/she will be registered.
Please visit our fees section or contact our admissions office for detailed information. You can also visit our website at https://www.https://institutes.abu.edu.ng/iaiict/"""


        elif "history of" in user_message and "iaiict" in user_message:
            response = """The IYA ABUBAKAR INSTITUTE OF ICT (IAIICT) was established in 1973 and has grown into a renowned institution known for its commitment to quality education in the field of information and communication technology.

Initially known as the Iya Abubakar Computer Centre (IACC), it served as the main computing hub for Ahmadu Bello University, providing essential computing services and support to academic departments. The Centre has been in existence for over four decades, playing a pivotal role in advancing computing knowledge and research.

The mandate of the Centre included creating a conducive learning environment, which led to the development of key competencies foundational to the computing discipline. Over the years, IAIICT has evolved to meet the growing demands of the ICT industry, offering specialized programs that have produced skilled professionals contributing to various sectors.

Today, IAIICT continues to uphold its legacy of excellence, maintaining its status as a leading institution in the field of ICT education and training.
The institute, originally named Iya Abubakar Computer Centre (IACC) in 1982, was established in 1973 after being detached from the Department of Mathematics, which had set it up in 1967 to provide computer services. The Centre was strategically important to ABU as its staff provided computing support to academic departments, contributing to the advancement of knowledge at the highest levels.

At that time, IACC was a hub of research activities, attracting researchers from across the country and beyond who leveraged its computing facilities and staff to create knowledge in their fields. Both staff and students received programming instruction at the Centre, which eventually led to a growing demand for training in computing activities.

By the 1990s, the computing field had exploded in technology and education, providing further impetus for the Centre to grow and address emerging needs in the broader society. The Centre faced increasing pressure to reinvigorate its longstanding mandate of pioneering computing services and education.

The experience gained through its multifaceted services connected well with the telecommunications and software development sectors of the economy. In response, the University Senate, at its 116th meeting, approved the introduction of two new diploma programs: Diploma in Computer Science and Diploma in Computer Engineering. These programs aimed to (1) develop skilled manpower in software development, database administration, network maintenance, web application development, and computer systems administration, and (2) create a breeding ground for feeding degree-level computing programs with quality students.

The duration of each diploma program is two academic years, comprising four semesters. The programs formally commenced in the 2008/2009 academic year with an initial intake of 56 students.
"""

        
        elif "who is the director" in user_message or "current director" in user_message and "iaiict" in user_message:
            response = "The current director of IAIICT is Dr. Shu'aibu Umar, who has a rich background in Database and Information Technology."

        elif "programs" in user_message or "programs they offer" in user_message and "iaiict" in user_message:
            response = """ Currently, IAIICT offer Diploma programs in Computer Science, Computer Engineering and CyberSecurity.
            """


        elif "mission" in user_message and "iaiict" in user_message or "vision" in user_message:
            response = """The 2-year Diploma programs at IAIICT have a three-fold mission to provide participants with:
    1. The skills necessary to enter the local workforce in the West African Sub-region and beyond.
    2. The foundation to transfer into a 200-level University Undergraduate Degree Program in a computing discipline.
    3. Professional enrichment for driving a wide range of community events, activities, and services.

    The programs are designed to develop a critical mass of computer technicians and prepare them to be responsible professionals, scientists, and engineers who will contribute to software development and the indigenous manufacture of computing artifacts.
        """

        elif "what" in user_message and "admission" in user_message or "requirements" in user_message or "requirement" in user_message:
            response = """Candidates seeking admission into the diploma programs are required to possess the following minimum entry qualifications:

    **Computer Science:**
    - Five (5) credits in West African Examination Council (WAEC)/National Examination Council (NECO) including Mathematics, Physics, English Language, and any two relevant science subjects, in NOT more than two sittings.

    **Computer Engineering:**
    - Five (5) credits in WAEC/NECO including Mathematics, Physics, Chemistry, English Language, and any other relevant science subject, in NOT more than two sittings.

    **SPECIAL ADMISSION:**
    - For admission into Diploma II of any of the Diploma programs: Candidates MUST have completed Diploma I from a comparable program with a minimum of 2.50 on a scale of 4.00. This condition is in addition to the normal admission requirements. Candidates from a recognized Polytechnic or College of Education must meet similar criteria. Admission may be considered based on the number of available slots in Diploma II.
        """

        elif "accommodation" in user_message or "hostel" in user_message or "room" in user_message or "sleep" in user_message:
            response = """At present, there is no arrangement to accommodate Diploma students within the University. All students MUST be aware of this and are personally responsible for making their accommodation arrangements.
        """

        elif "screening" in user_message or "process" in user_message or "admission" in user_message and "process" in user_message:
            response = """During the screening process, every new student is required to present the originals of their relevant credentials to the screening officer, including WAEC and/or NECO result scratch cards. Students must be aware of the time scheduled for registration and must complete all required steps on or before the final date. All materials screened and approved by the screening officer MUST be returned to the Administrative Secretary. Students are advised to check the Notice Board for details of courses to be registered. A student is allowed to register for a minimum of 17 credit units and a maximum of 24 credit units per semester.
        """

        elif "late" in user_message and "registration" in user_message:
            response = """The Director may approve an extension of the registration period. Late registration incurs a late registration fee. Registration issues caused by travel accidents or ill-health may be considered if supported by an authenticated medical report from the University Health Service and an application addressed to the Director of IACC through the Coordinator of Education and Research Division.
        """

        elif "deferment" in user_message or "defer" in user_message:
            response = """Students who wish to apply for deferment of either a semester or an entire academic year must provide a valid reason. Applications should be made to the Director through the Coordinator of Education and Research Division for appropriate action by the IACC Management.
        """

        elif "counseling" in user_message or "course registration" in user_message or "spillover" in user_message or "carryover" in user_message or "resit" in user_message:
            response = """The office of the Coordinator of Education and Research is responsible for issues related to learning within the period stipulated for the Diploma programs and provides counseling to students having problems with course registration and the number of credit units to be registered per semester. Specific issues related to carryover, spillover, and repeat can also be addressed with the Coordinator.
        """

        elif "sick" in user_message or "health" in user_message or "hospital" in user_message or "medical" in user_message or "sickness" in user_message:
            response = """The University Sickbay, located to the right of the first roundabout on the road entering through the North Gate next to Suleiman Hall, is the facility provided for the health care of all university staff and students, including the Centre's Diploma students. The clinic offers medical care, medical examination, antenatal care, and child welfare services to all registered students. Students are required to register at the clinic to benefit from these services. Registration is free, and with your admission letter and student identity card, the clinic receptionist will explain all the procedures required to obtain medical care. Health services are available from 7:30 am to 8:30 pm, Monday through Saturday (except on public holidays).
        """

        elif "security" in user_message or "theft" in user_message or "steal" in user_message or "missing" in user_message:
            response = """All security matters within the University fall under the office of the Vice Chancellor and are coordinated by the University Security Services Division, located beside the University Microfinance Bank along Aku-Uka Road, South-West of the Senate Building. The Director of IAIICT liaises directly with the Security Division on all security issues within the Centre. Every student MUST carry their student identity card and produce it upon request by security personnel.

    Students MUST avoid involvement in vices such as cultism, rape, theft, unauthorized violence/riots, and other activities punishable under ABU laws. The Director of IAIICT reserves the right, upon investigation, to hand over any student involved in such activities to the Security Division for appropriate action. Students should be vigilant and promptly report any security breaches to the Administrative Secretary of IAIICT.
        """

        elif "examination rules" in user_message or "examination guidelines" in user_message or "examination instruction" in user_message or "examination conduct" in user_message:
            response = """Examinations are typically held at the end of each semester. They may take the form of written papers, oral examinations, practicals, projects, or a combination of these, as modeled by the Senate and implemented by the Centre. Continuous Assessment (C.A.) of coursework is usually included in determining examination results.

    **Eligibility:**
    To be eligible for a Diploma examination, a student must be registered for the course to be examined and must have fulfilled the IACC requirements regarding fees and other registration-related matters. At least 75% attendance is required in all classes, laboratories (if applicable), etc., to qualify to sit for examinations.

    **Conduct:**
    (a) A student must be at the examination venue at least ten (10) minutes before the start of the examination. Latecomers may be admitted up to thirty (30) minutes after the exam has started, but they will not be allowed extra time. Students are not allowed to leave the venue during the first hour or the last fifteen (15) minutes of the examination. All scripts must be handed to the invigilator before leaving the venue.
    (b) A student who leaves the examination room will not be readmitted unless, during their absence, they were under the continuous surveillance of an Invigilator/Assistant Invigilator.
    (c) Students must bring their I.D. card and Examination card (if any) to each examination and display them conspicuously on their desk. They must also complete an attendance form, which will be collected by the Invigilator during each examination.
    (d) No books, papers, or unauthorized materials are allowed into the examination room, except as specified in the exam rules. Students must not give or receive assistance during the exam. If suspected of any misconduct, students will be reported, investigated, and dealt with accordingly.
    (e) If a student is suspected of cheating or disturbing the exam, they will be allowed to continue but will be investigated later. The Board of Examiners may recommend whether the student's paper should be accepted and what other actions should be taken.

    **Punishment for Examination Malpractices:**

    **A. Misconducts by Students:**
    1. **Expulsion:** 
    - Impersonation in exams.
    - Introduction of unauthorized materials into the exam hall.
    - Exchange of materials or collaboration during the exam.
    - Removal or destruction of exam scripts.
    - Copying from cheat notes.
    - Facilitating cheating.

    2. **Rustication for one academic session:**
    - Non-submission or incomplete submission of exam scripts.
    - Introduction of unauthorized materials.
    - Non-appearance at the Examination Irregularities and Malpractices Committee.
    - Use of mobile phones in the exam hall.

    3. **Written Warning:**
    - Speaking or conversing during the exam.
    - Writing on question papers or scripts.

    **B. Misconducts involving Staff:**
    Any act of commission or omission related to exam malpractice by a staff member will be referred to University Administration for disciplinary action.
        """
                
        elif "examination malpractice" in user_message or "exam malpractice" in user_message or "malpractice" in user_message or "examination misconduct" in user_message:
            response = """            
    **Punishment for Examination Malpractices:**

    **A. Misconducts by Students:**
    1. **Expulsion:** 
    - Impersonation in exams.
    - Introduction of unauthorized materials into the exam hall.
    - Exchange of materials or collaboration during the exam.
    - Removal or destruction of exam scripts.
    - Copying from cheat notes.
    - Facilitating cheating.

    2. **Rustication for one academic session:**
    - Non-submission or incomplete submission of exam scripts.
    - Introduction of unauthorized materials.
    - Non-appearance at the Examination Irregularities and Malpractices Committee.
    - Use of mobile phones in the exam hall.

    3. **Written Warning:**
    - Speaking or conversing during the exam.
    - Writing on question papers or scripts.

    **B. Misconducts involving Staff:**
    Any act of commission or omission related to exam malpractice by a staff member will be referred to University Administration for disciplinary action.
        """

        elif "certificate" in user_message or "transcript" in user_message or "diploma" in user_message or "result" in user_message:
            response = """Issuance of certificates, transcripts, and results are processed by the IAIICT in accordance with university procedures. Students are advised to ensure that all fees and dues are settled before requesting these documents. The exact timeline for issuance will be communicated by the IAIICT administration.
        """
        elif "what" in user_message and "facilities" in user_message and "available" in user_message or "use" in user_message:
            response = "The institute has a library, computer labs, and free internet connection for students."
        elif "result" in user_message or "result grading" in user_message or "grading system" in user_message or "grade" in user_message:
            response = """The grading system for the Diploma program is based on a four-point scale:

    | Grade | Point | Score Range (%) |
    |-------|-------|----------------|
    | A     | 4.00  | 70 – 100       |
    | B     | 3.00  | 60 – 69        |
    | C     | 2.00  | 50 – 59        |
    | D     | 1.00  | 40 – 49        |
    | F     | 0.00  | 0 – 39         |

    **Classification of Diploma:**

    1. **Distinction:** Cumulative Grade Point Average (CGPA) of 3.50 – 4.00
    2. **Credit:** CGPA of 2.50 – 3.49
    3. **Merit:** CGPA of 1.40 – 2.49
    4. **Pass:** CGPA of 1.00 – 1.39
    5. **Fail:** CGPA below 1.00
        """

        else:
            response = "I'm sorry, I didn't understand that. Could you please clarify your question or Reach out to the Institute's Examination Officer at 09077650455 for more information. Thank you"

        dispatcher.utter_message(text=response)
        return []


class ActionProspectiveStudents(Action):

    def name(self) -> Text:
        return "action_prospective_students"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text', '').lower()

        if "how can i be a student" in user_message or "how can i apply" in user_message:
            response = """
            To become a student at IAIICT, you need to apply for one of the diploma programs. The application process typically involves obtaining the application form, filling it out with your personal and academic details, and submitting it along with the required documents.
            You can access the form at the application portal which is https://www.forms.abu.ng
            """
        
        elif "admission requirements" in user_message or "requirements" in user_message:
            response = """
            The admission requirements for the diploma programs at IAIICT are as follows:
            For Computer Science: Five (5) credits in WAEC/NECO in Mathematics, Physics, English Language, and any two relevant science subjects in not more than two sittings.
            For Computer Engineering: Five (5) credits in WAEC/NECO in Mathematics, Physics, Chemistry, English Language, and any other relevant science subject in not more than two sittings.
            """
        
        elif "scholarships" in user_message:
            response = """
            Currently, IAIICT does not offer scholarships specifically for diploma students. However, students can explore external scholarship opportunities and apply independently.
            """
        
        elif "how many years" in user_message or "duration" in user_message:
            response = """
            The diploma programs at IAIICT typically take two academic years to complete, comprising four semesters.
            """
        
        elif "when is admission starting" in user_message or "admission date" in user_message:
            response = """
            Admission for IAIICT usually begins in the first quarter of the year. However, specific dates vary, so it's advisable to regularly check the IAIICT website or contact the admission office for the most accurate information.
            """
        
        elif "how can i apply" in user_message or "where to apply" in user_message:
            response = """
            You can apply to IAIICT at any cybercafelocated at Ahmadu Bello University, Zaria. Alternatively, you can also apply online through their official website which is at https://www.forms.abu.edu.ng """

        else:
            response = """
            For more information on how to apply to IAIICT or other admission-related inquiries, please visit our official website at https://www.https://institutes.abu.edu.ng/iaiict/ or contact our admission office directly.
            """

        dispatcher.utter_message(text=response)
        return []



class ActionProvideAcademicResource(Action):
    def name(self) -> Text:
        return "action_provide_academic_resource"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract course code from the entities
        course_code = next(tracker.get_latest_entity_values("course_code"), None)
        
        # Base URL where academic resources are served
        base_url = "http://localhost:8100/assets"  # Ensure this matches your server URL or public URL

        # Determine if the user is asking for tutorials, handouts, or PQs
        user_message = tracker.latest_message.get('text', '').lower()

        # Initialize file_url to None
        file_url = None

        if course_code:
            course_code = course_code.upper()
            encoded_course_code = urllib.parse.quote(course_code)  # Encode course code if necessary
            
            if any(keyword in user_message for keyword in ["tutorials", "link", "external"]):
                response = f"You can find external tutorials for {course_code} at https://moodle.abu.edu.ng/course/index.php?categoryid=115"
                dispatcher.utter_message(text=response)
            elif "handout" in user_message:
                file_url = f"{base_url}/handouts/{encoded_course_code}.pdf"
            elif "pq" in user_message:
                file_url = f"{base_url}/PQ/{encoded_course_code}.pdf"
        
        # Debugging: Print out the file URL to verify it's correct
        print(f"Providing file at: {file_url}")

        # Check if the file URL exists and send the appropriate message
        if file_url:
            dispatcher.utter_message(text=f"Here is the file you requested: {file_url}")
        elif not any(keyword in user_message for keyword in ["tutorials", "link", "external"]):
            dispatcher.utter_message(text="Sorry, I couldn't find the resource you're looking for. Please check the course code or try again later.")

        return []


    
class ActionStudyBuddy(Action):
    def name(self) -> Text:
        return "action_study_buddy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract course code from the entities
        course_code = next(tracker.get_latest_entity_values("course_code"), None)
        
        # Extract user message to identify if they need quiz or advice
        user_message = tracker.latest_message.get('text').lower()

        # Determine if user is requesting a quiz or study advice
        if "practice questions" in user_message or "practice" in user_message or "practice exercise" in user_message or "quiz" in user_message and course_code in user_message:
            # Redirect to Quizizz for the specific course
            quiz_url = f"https://www.abu.edu.ng"  # Adjust the URL format if needed
            dispatcher.utter_message(text=f"Here is a quiz for {course_code}: {quiz_url}")
        elif "study" in user_message or "advice" in user_message:
            
            # Different groups of study tips
            study_tips_1 = [
                "1. Create a study schedule and stick to it.",
                "2. Use active recall and spaced repetition techniques.",
                "3. Practice with quizzes and past papers.",
                "4. Find a study group or study buddy.",
                "5. Stay organized and take regular breaks."
            ]

            study_tips_2 = [
                "1. Teach what you've learned to someone else.",
                "2. Prioritize understanding concepts over memorization.",
                "3. Use visual aids like mind maps and charts.",
                "4. Set specific goals for each study session.",
                "5. Make sure to get plenty of sleep and stay hydrated."
            ]
            
            study_tips_3 = [
                "1. Break down your study material into manageable chunks.",
                "2. Set up a dedicated and distraction-free study space.",
                "3. Review your notes regularly, not just before exams.",
                "4. Use a timer to work in focused intervals, such as the Pomodoro technique.",
                "5. Reward yourself after completing study sessions to stay motivated."
            ]

            study_tips_4 = [
                "1. Engage in discussions about the material with peers.",
                "2. Summarize what you've learned in your own words.",
                "3. Incorporate multimedia resources like videos and podcasts.",
                "4. Focus on understanding the 'why' behind concepts, not just the 'what'.",
                "5. Track your progress to see how much you've improved over time."
            ]

            study_tips_5 = [
                "1. Start your study sessions with the most challenging tasks.",
                "2. Mix up different subjects to avoid burnout and maintain focus.",
                "3. Avoid cramming by spreading out your study sessions.",
                "4. Take care of your physical health with regular exercise.",
                "5. Use mnemonic devices to help remember key facts and figures."
            ]

            study_tips_6 = [
                "1. Study in short, frequent sessions rather than long marathons.",
                "2. Use apps and tools to stay organized and on track.",
                "3. Explain complex ideas to a friend or family member.",
                "4. Create practice tests to challenge your understanding.",
                "5. Prioritize tasks using the Eisenhower Matrix (urgent vs. important)."
            ]
            
            study_tips_7 = [
                "1. Review feedback from assignments and exams to identify areas for improvement.",
                "2. Practice mindfulness or meditation to reduce stress before studying.",
                "3. Join online forums or study groups related to your subject.",
                "4. Balance your study time with social activities to maintain well-being.",
                "5. Keep a study journal to reflect on what strategies work best for you."
            ]

            
            all_tips = [study_tips_1, study_tips_2, study_tips_3, study_tips_4, study_tips_5, study_tips_6, study_tips_7]

# Select a random group of tips
            selected_tips = random.choice(all_tips)
            
            # Dispatch each tip in the selected group
            dispatcher.utter_message(text="Here are some study tips:")
            for tip in selected_tips:
                dispatcher.utter_message(text=tip)
        else:
            # Handle other general study-related requests
            dispatcher.utter_message(text="I can help with quizzes or provide study advice. How can I assist you?")
        
        return []
    
    
    
    
class ActionFallbackResponse(Action):

    def name(self) -> Text:
        return "action_fallback_response"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        fallback_message = (
            "Hello! My name is I-Sac, which stands for IYA ABUBAKAR STUDENT ASSISTANT CHATBOT. "
            "I'm a conversational AI assistant designed to support students at the Iya Abubakar Institute of ICT. "
            "Whether you're a prospective student or a current student, I'm here to assist you with a wide range of information and services.\n\n"
            "Here are some of the ways I can help you:\n\n"
            "1. **Class Schedules:**\n"
            "   - I can provide details about your class schedules, including times, venues, and instructors.\n\n"
            "2. **Course Information:**\n"
            "   - I can provide information on available courses, their contents, and how to enroll.\n\n"
            "3. **Program Details:**\n"
            "   - I can give you information about different programs offered at the institute, including their structure and requirements.\n\n"
            "4. **Institute Information:**\n"
            "   - I can offer details about the institute’s facilities, services, and general information about campus life.\n\n"
            "5. **Admission Queries:**\n"
            "   - I can help you with questions related to the admission process, including application procedures and deadlines.\n\n"
            "6. **Exam and Result Information:**\n"
            "   - I can provide information about exam schedules, result announcements, and related procedures.\n\n"
            "7. **Campus Events:**\n"
            "   - I can inform you about upcoming events, workshops, and activities happening on campus.\n\n"
            "8. **Support Services:**\n"
            "   - I can guide you to various support services available, such as academic counseling and student assistance.\n\n"
            "If you have any questions or need assistance with anything related to the institute, feel free to ask. "
            "I'm here to support you!\n\n"
            "For more information, please refer to [this link](https://institutes.abu.edu.ng/iaiict/). Thank you!"
        )

        dispatcher.utter_message(text=fallback_message)

        return []
