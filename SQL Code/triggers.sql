-- RAJIV RAMAIAH
-- DATABASES

USE rajiv_db;


-- Shows all manuscripts with only 1 active reviewer
DROP VIEW IF EXISTS `OnlyReviewer`;

CREATE VIEW `OnlyReviewer` AS
    SELECT REVIEWER_GROUP.MANUSCRIPT_NUMBER as ManuscriptNumber, REVIEWER.NUMBER as ReviewerNumber
    FROM REVIEWER_GROUP  
    LEFT JOIN REVIEWER ON REVIEWER_GROUP.REVIEWER_NUMBER = REVIEWER.NUMBER
    WHERE REVIEWER.STATUS='Active'
    GROUP BY REVIEWER_GROUP.MANUSCRIPT_NUMBER HAVING COUNT(REVIEWER_GROUP.MANUSCRIPT_NUMBER) = 1;

-- TRIGGER 1

DROP TRIGGER IF EXISTS `before_manuscript_submission`;

DELIMITER /

CREATE TRIGGER before_manuscript_submission BEFORE INSERT ON MANUSCRIPT
	
	FOR EACH ROW BEGIN

    DECLARE signal_message VARCHAR(128);
	
    -- check that an active reviewer exists for this manuscripts code
	IF (SELECT COUNT(*) FROM CODE_GROUP WHERE CODE_GROUP.RI_CODE=new.RI_CODE AND 
        ((SELECT REVIEWER.STATUS FROM REVIEWER WHERE REVIEWER.NUMBER=CODE_GROUP.REVIEWER_NUMBER) = 'Active')) = 0 THEN

        SET signal_message = 'RI_CODE EXCEPTION! No reviewer with subject matter expertise 
        	is enrolled to review this manuscript!';

        -- MySQL doc defines SQLSTATE 45000 as "unhandled user-defined exception."
        SIGNAL SQLSTATE '45000' SET message_text = signal_message;
        
    END IF;

END /
DELIMITER ;

-- TRIGGER 2

DROP TRIGGER IF EXISTS `on_reviewer_resignation`;

DELIMITER /

CREATE TRIGGER on_reviewer_resignation BEFORE UPDATE ON REVIEWER
    
    FOR EACH ROW BEGIN

    -- Checks update is for reviewer resigning
    IF NEW.STATUS='Resigned' THEN

        -- IF the reviewer being updated is the only reviewer for one or more manuscripts
        IF(SELECT COUNT(*) FROM OnlyReviewer WHERE OnlyReviewer.ReviewerNumber=OLD.NUMBER) > 0 THEN

            -- update only manuscripts under review and with only one active reviewer
            UPDATE MANUSCRIPT
                SET MANUSCRIPT.STATUS='Received'
                WHERE MANUSCRIPT.STATUS = 'Under Review' AND MANUSCRIPT.NUMBER IN (SELECT OnlyReviewer.ManuscriptNumber 
                    FROM OnlyReviewer WHERE OnlyReviewer.ReviewerNumber=OLD.NUMBER);
            
        END IF;

    END IF;

END /
DELIMITER ;




