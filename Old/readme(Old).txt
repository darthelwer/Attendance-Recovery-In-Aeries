Hi all,
If you are here, you are interested in working with Areies and Attendance Recovery. Feel free to use for free (unless you are AERIES Then cough up the big bucks) but if you 
want to say thanks and support my Dr Pepper Zero habit... send a venmo to @darthelwer.

Originally i was told we only needed numbers not when they were applied. This was a fairly straight forward SQL script
you can find here: (https://github.com/darthelwer/Attendance-Recovery-In-Aeries/blob/main/Attendance%20Recovery%20Report%20(Detail).sql ) 
and a second one that provides sums of AR days for each grade group - TK to 3, 4 to 6, and 7-8)  
(https://github.com/darthelwer/Attendance-Recovery-In-Aeries/blob/main/Attendance%20Recovery%20Report%20(Overview).sql)
[We are PS to 8 district you would need to add the sum cases for upper grades]

BUT then I was told we needed to actually match the dates of absense to the date(s) of the AR (some of our AR is only an
hour long and we have to sum 4 of those into one absence.) To keep track of these you may be familiar with ADA makeup
notes in the Attendance system. (https://support.aeries.com/support/solutions/articles/14000088722-attendance-note-ada-make-up)
But this is both cumberson (many clicks to do) and manual (have to do it for each student) We had +4000 days - we would have 
needed to do each one individually.

So here is how I automated it. 

Step 1 
Ensure that your ELOP data is in Aeries which is a bit of a hassel itself. You have to create the program, create the sessions, 
put the students and teachers in, then add the attendance. If you are capturing in the moment for these programs great. Our school
was using a differnt check-in, check-out system so we had to import this data.

Step 2 
Run these two Aeries Queries below and save as CSV files - keep in mind we are working with all day attendance per the ed code arround AR
- this wont see if they have an absence only in 1 class 
(I think I said in my original post these were SQL scrips but they are actually AQL - I was thinking of the ones above) 
These queries are actually documented in the Python file as well under each function that uses them
   LIST ATD STU ATD.ID ATD.SC STU.SN ATD.DT ATD.TM ATD.SE
   LIST ATT STU STU.ID ATT.DY ATT.DT ATT.AL ATT.ADA ATT.ADT ATT.ACO IF ATT.AL = 2 OR ATT.AL = A OR ATT.AL = B OR ATT.AL = E OR ATT.AL = I OR ATT.AL = J OR ATT.AL = U

   The first one will pull all the supplemental data. The second one will pull all the attendance data. 
   ***IMPORTANT*** You will need to change the ATT.AL to capture whatever attendence codes you use for absences. Consult with your district on this. There are rules 
   about which absensces can and cant be recovered and please check with your LEA

Step 3
Run the python script, it will prompt you for two files which it will use to create members of a class called Student
(https://github.com/darthelwer/Attendance-Recovery-In-Aeries/blob/main/AR%20and%20ABS.py)
One of the peices of data it uses from the supplemental attendance is time. If the time is over 240 minutes (4 hours) it treats it as one day of AR.
If less than 240 minutes it logs as partial and waits to add to another partial
***Please make sure your AR minutes are in 60 min blocks (per Ed Code we can only count the hours, if you do 40 minutues that = 0 hours recovered) 

Step 4 
That will generate an output file that looks like this
STU.ID  STU.SC	STU.SN	ATT.DY	 ATT.ADA	  ATT.ADT	    ATT.ACO	                      
#####	  ###	    700	    8	       M	        7/24/2025	  Super Summer Camp:07/24/2025	

Step 5 
Creating the SQL input - we want that data to look like this (####,###,700,8,'M','2025-07-24','Super Summer Camp:07/24/2025')
So now we need to take that data and get it in an inputable form. Open in excel, In column H put this and then copy down
="("&A2&","&B2&","&C2&","&D2&",'"&E2&"','"&TEXT(F2,"yyyy-mm-dd")&"','"&SUBSTITUTE(G2,"'","''")&"'),"

***note step 5 could easily be wraped into step 4 but at this point I didnt know HOW i was going to get the data into Aeries. ***

Step 6 
This is where it gets fun. Depending on how balsy you are... you can either just run the code or as i suggest below use the TRAN command so you can undo if needed.
The aeries SQL server doesnt allow for creating a new table (which you kinda need for your CSV to get into SQL) so we have to use a temp table.

6a 
Run this to creeat a temp table

    CREATE TABLE #ATT_CSV_STAGE (
        STU_ID int,
        SC     int,
        SN     int,
        DY     int,
        ADA    varchar(5),
        ADT    date,
        ACO    varchar(50)
    );

6b
Populate the temp table. You will need to do in batches most likely as SMSS chokes on large single inserts.
I did 500 at a time and it seemed to work well. USe the code and copy the column you created in step 5 - 
you will need to delete the last comma and turn into a ";" before you run it.

    INSERT INTO #ATT_CSV_STAGE (STU_ID, SC, SN, DY, ADA, ADT, ACO)
    VALUES
    (…, …),
    (…, …),
    (…, …);

Run this as many times as you need to get all the data in- i had to do 9 batches.

**Warning** Dont log out or you will ahve to start over at the begining of step 6 since this is a temp table

6c 
This is just a check to make sure you are doing things right. Compare the result to your excel row count.
    SELECT COUNT(*) AS StageCount
    FROM #ATT_CSV_STAGE;

6d
Also a check. This compares what you have in old ADA data vs what you are about to enter. 
    SELECT
        A.SC,
        A.SN,
        A.DY,
        A.ADA AS OLD_ADA,
        C.ADA AS NEW_ADA,
        A.ADT AS OLD_ADT,
        C.ADT AS NEW_ADT,
        A.ACO AS OLD_ACO,
        C.ACO AS NEW_ACO
    FROM ATT A
    JOIN #ATT_CSV_STAGE C
        ON A.SC = C.SC
       AND A.SN = C.SN
       AND A.DY = C.DY
    WHERE A.DEL = 0;

6e 
Heres where the magic happens

    BEGIN TRAN;
    
    UPDATE A
    SET
        A.ADA = C.ADA,
        A.ADT = C.ADT,
        A.ACO = C.ACO
    FROM ATT A
    JOIN #ATT_CSV_STAGE C
        ON A.SC = C.SC
       AND A.SN = C.SN
       AND A.DY = C.DY
    WHERE A.DEL = 0
      AND (
           ISNULL(A.ADA,'') <> ISNULL(C.ADA,'')
        OR ISNULL(A.ADT,'1900-01-01') <> ISNULL(C.ADT,'1900-01-01')
        OR ISNULL(A.ACO,'') <> ISNULL(C.ACO,'')
      );
    
    SELECT @@ROWCOUNT AS RowsUpdated;

6f
Quick spot check to make sure it looks okay

    SELECT TOP 50
        A.SC, A.SN, A.DY, A.ADA, A.ADT, A.ACO
    FROM ATT A
    JOIN #ATT_CSV_STAGE C
        ON A.SC = C.SC
       AND A.SN = C.SN
       AND A.DY = C.DY
    ORDER BY A.SC, A.SN, A.DY;

6g
If good
  COMMIT;
If not
  ROLLBACK;

7
Pick one of your students and search in aeries. Go to Student Data >> Attendance.
You should now see a green note indicator and a green box arround the day indicating 
ADA make up!

Feel free to use for free (unless you are AERIES Then cough up the big bucks) but if you 
want to say thanks and support my Dr Pepper Zero habit... send a venmo to @darthelwer.
