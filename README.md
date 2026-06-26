Attendance Recovery Tool for Aeries

GitHub: https://github.com/darthelwer/Attendance-Recovery-In-Aeries

Created by Adam Elwer (https://github.com/darthelwer)



**-----------------------------------------------------------------------------------------**

\- ***For the love of all things holy, please read this document before using the software.*** -

\- It contains important setup information and assumptions used by the application.      -

**-----------------------------------------------------------------------------------------**





SUPPORT FUTURE MAINTAINCE AND DEVELOPMENT!

This started as me trying to find a solution to a problem in our district, and blossomed into this

using my nights and weekends, If this tool saved your district hours of manual work and you'd like

to support future development (or just support my Dr Pepper Zero habit)

Venmo: @darthelwer





DISCLAIMER



Not affiliated with or endorsed by Aeries Software.This tool updates attendance records in Aeries. Always review the generated CSV and test in a non-production environment before updating production data. Your LEA is responsible for ensuring compliance with California Education Code and any local attendance policies.





WELCOME



If you used my original steps and tool and youve been waiting for improvements thanks for hanging in there.

This application automates the entire Attendance Recovery workflow while still allowing you to review every change before anything is written back to Aeries.



This app

* Loads supplemental and daily attendance
* Limits sessions to whole hour increments as required by CA ED Code
* Combines multiple shorter sessions to reach required minutes for AR under ED code by grade.
* Matches AR days to Absences and will check for previously applied days and when they were used limiting the total number of AR days to 10 per ED Code
* Allows you to choose which supplemental attendance programs to include by school
* Allowing you to choose which absence codes qualify for AR (this assumes you are pushing from school 0 to all other schools - if that is NOT the case, please reach out for help)
* Creates a CSV output for both internal auditing before making changes to student records but also as a document to give auditors.
* Optionally will uploads changes directly to the ATT table in Aeries.





THIS IS A PYTHON FILE 



Sorry I ran into some issues creating this as an EXE, namely that some districts that I test ran this with AND MY OWN have alot of restrictions against running EXE files made by PyInstaller. I'm working on sorting this out but I know we have deadlines fast approaching

* You will need to install the latest version of python
* You will only need to install 1 library (I tried to stay with native libraries as much as possible)
  * pyodbc (for talking to the SQL server)
* The app requires some JSON Config files to store info between uses like server and username (not Password) 
  * If you dont download the sample one - it will go ahead and make one for you on first run.
* You will also need the Microsoft ODBC Driver 18 for SQL Server which can be downloaded directly from Microsoft.






AERIES UPLOAD RESULTS



Successful Attendance Recovery days appear in Aeries as:



* Green attendance indicators
* Green attendance boxes
* ADA Make-up Notes



The attendance comment includes:

* ADA Makeup code of "M'
* Supplemental Attendance Program Name
* Date (or dates) used to recover the absence

&#x09;Example:

&#x09;	Super Summer Camp: 07/24/2025

&#x09;	T1 ASES ELOP: 09/03/25 09/04/25 09/05/25 09/08/25





IMPORTANT NOTE ON SUPPLIMENTAL ATTENDANCE NAMES!



The ATT.ACO field in Aeries is limited to 50 characters. Our auditors wanted both the program name and all dates used for the attendance Recovery.

Example - We had to shorten "Trimester 1 ASES ELOP After School Genius Hour" to T1 ASES ELOP (I did NOT name that BTW)

If a program name combined with multiple recovery dates exceeds this limit, the application will stop and display an error noting the following :



* School
* Session (SE)
* Program Name
* Maximum allowable program name length (50 minues the characters needed for the dates)

And a note: "Please shorten the Supplemental Attendance Session name in Aeries before continuing."

It will NOT let you proceed before you do





WHAT THIS PROGRAM DOES **NOT** DO



This application does not:

* Import your Supplemental Attendance into Aeries if its stored in spreadsheets(Sorry)
* Verify Supplemental Attendance class size or student/teacher ratios. (Currently 10:1 for TK/K and 20:1 for All others - they WILL be looking at this)
* Validate compliance with California Education Code beyond the attendance matching logic implemented in this application.
* Divide Attendance Recovery into reporting periods (P1, P2, EOY).



If you need the data sorted by P1, P2, EOY you can sort the generated CSV by ATT.DY. You will need to know which Aeries attendance day corresponds to each instructional day in your own district calendar. It was a level of complexity that I wasnt ready to add as the corespondance between aeries day, instructional days and dates is not consistant from district to district. In my district P2 date of march 20 is instructional day 132 but is aereis attendance day of 160.



BEFORE UPLOADING



The application intentionally pauses before updating Aeries so you can review the generated CSV.



Please verify:

* Student ID list
* Absence dates
* Attendance Recovery dates
* Attendance comments
* Programs selected



Only continue with the SQL upload once you are satisfied the CSV is correct.





ISSUES, IDEAS, CONTRIBUTIONS AND COLABORATION



If you find a bug, have an idea for a new feature, or your district has a unique Attendance Recovery workflow, please open an Issue on GitHub.

If your district, county, or Aeries would like to colaborate on this or other feature please reach out to me at *adamelwer \[AT] gmail \[DOT] com*

Feedback from other districts helps improve the application for everyone.



Thank you for reading this to the end! I hope this saves you time, energy and stress!



May the force be with you, always!





Version History



1.0.0

\- Initial public GUI release

\- Direct SQL upload

\- Attendance code configuration

\- Automatic audit CSV generation

\- Duplicate detection and prevention

