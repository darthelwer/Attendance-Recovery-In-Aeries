WITH AR_Calculated AS
(
    SELECT
        a.ID AS StudentID,
        a.SCL AS School,
        s.GR AS Grade,
        SUM(ISNULL(a.TM,0)) AS ARTotalMinutes,
        CAST(SUM(ISNULL(a.TM,0)) / 240.0 AS DECIMAL(10,1)) AS ARDays,
        MAX(ISNULL(h.AB, 0)) AS Absences,
        -- AppliedAR calculation
        CASE
            WHEN FLOOR(CAST(SUM(ISNULL(a.TM,0)) / 240.0 AS DECIMAL(10,1))) > 10 THEN 
                CASE WHEN MAX(ISNULL(h.AB,0)) < 10 THEN MAX(ISNULL(h.AB,0)) ELSE 10 END
            ELSE 
                CASE WHEN FLOOR(CAST(SUM(ISNULL(a.TM,0)) / 240.0 AS DECIMAL(10,1))) > MAX(ISNULL(h.AB,0)) THEN MAX(ISNULL(h.AB,0))
                     ELSE FLOOR(CAST(SUM(ISNULL(a.TM,0)) / 240.0 AS DECIMAL(10,1)))
                END
        END AS AppliedAR
    FROM ATD a
    LEFT JOIN STU s
        ON a.ID = s.ID
    LEFT JOIN AHS h
        ON a.ID = h.ID
       AND h.YR = '2025-2026'
    WHERE a.DEL = 0
    GROUP BY
        a.ID,
        a.SCL,
        s.GR
)
SELECT
    SUM(CASE WHEN Grade BETWEEN -2 AND 3 THEN AppliedAR ELSE 0 END) AS Sum_Grade_Neg2_3,
    SUM(CASE WHEN Grade BETWEEN 4 AND 6 THEN AppliedAR ELSE 0 END) AS Sum_Grade_4_6,
    SUM(CASE WHEN Grade BETWEEN 7 AND 8 THEN AppliedAR ELSE 0 END) AS Sum_Grade_7_8
FROM AR_Calculated;
