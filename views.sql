-- RAJIV RAMAIAH
-- DATABASES

USE rajiv_db;

-- View: LeadAuthorManuscripts

-- For all authors, their basic information (name etc.) and the manuscript(s) 
-- for which they are the primary author (if any), along with the status of the manuscript(s). 
-- Results ordered by author last name and then by increasing submission timestamp. Permissions: Editor.

-- COMMENTS
-----------------------------------------------------------------------------------------------------------------
-- This view includes secondary authors with NULL values for Manuscript data since they are not primary authors. 
-- To change this, I can simply remove the UNION with the secondary author table. However, I chose to include 
-- this since it was the most literal interpretation of what was required for this view. Thanks!
-----------------------------------------------------------------------------------------------------------------
DROP VIEW IF EXISTS `LeadAuthorManuscripts`;

CREATE VIEW `LeadAuthorManuscripts` AS
	SELECT AUTHOR.FNAME AS AuthorFName, AUTHOR.LNAME AS AuthorLName, MANUSCRIPT.TITLE AS ManuscriptTitle, 
	MANUSCRIPT.NUMBER AS ManuscriptNumber, MANUSCRIPT.STATUS AS ManuscriptStatus, MANUSCRIPT.DATE_RECEIVED AS ManuscriptSubmissionTimestamp
	FROM MANUSCRIPT INNER JOIN AUTHOR ON AUTHOR.ID=MANUSCRIPT.AUTHOR_ID
	UNION
	SELECT SECONDARY_AUTHOR.FNAME AS AuthorFName, SECONDARY_AUTHOR.LNAME AS AuthorLName, NULL, NULL, NULL, NULL
	FROM SECONDARY_AUTHOR
	ORDER BY AuthorLName, ManuscriptSubmissionTimestamp ASC;




-- View: AnyAuthorManuscripts

-- For all authors, their name and the manuscript(s) for which they are among the authors (if any), 
-- along with the status of the manuscript(s). Results ordered by author last name and then by increasing 
-- submission timestamp. Permissions: Author, Editor.
DROP VIEW IF EXISTS `AnyAuthorManuscripts`;

CREATE VIEW `AnyAuthorManuscripts` AS
	SELECT AUTHOR.FNAME AS AuthorFName, AUTHOR.LNAME AS AuthorLName, MANUSCRIPT.TITLE AS ManuscriptTitle, 
	MANUSCRIPT.NUMBER AS ManuscriptNumber, MANUSCRIPT.STATUS AS ManuscriptStatus, MANUSCRIPT.DATE_RECEIVED AS ManuscriptSubmissionTimestamp
	FROM MANUSCRIPT INNER JOIN AUTHOR ON AUTHOR.ID=MANUSCRIPT.AUTHOR_ID
	UNION
	SELECT SECONDARY_AUTHOR.FNAME AS AuthorFName, SECONDARY_AUTHOR.LNAME AS AuthorLName, MANUSCRIPT.TITLE AS ManuscriptTitle, 
	MANUSCRIPT.NUMBER AS ManuscriptNumber,  MANUSCRIPT.STATUS AS ManuscriptStatus, MANUSCRIPT.DATE_RECEIVED AS ManuscriptSubmissionTimestamp
	FROM SECONDARY_AUTHOR INNER JOIN MANUSCRIPT ON SECONDARY_AUTHOR.MANUSCRIPT_NUMBER=MANUSCRIPT.NUMBER
	ORDER BY AuthorLName, ManuscriptSubmissionTimestamp ASC;

-- View: PublishedIssues

-- For all completed (published) issues, the issue year, issue number (1, 2, 3, or 4), 
-- the title of each manuscript included in that issue, with page numbers, ordered by issue name 
-- and page numbers. Permissions: Author, Editor, Reviewer.

-- check if not null to make sure issue contains manuscripts
DROP VIEW IF EXISTS `PublishedIssues`;

CREATE VIEW `PublishedIssues` AS
	SELECT JOURNAL_ISSUE.YEAR AS IssueYear, JOURNAL_ISSUE.PERIOD AS IssuePeriod, 
	MANUSCRIPT.TITLE AS ManuscriptTitle, MANUSCRIPT.PAGE_NUMBER_IN_ISSUE AS PageInIssue
	FROM JOURNAL_ISSUE INNER JOIN MANUSCRIPT ON MANUSCRIPT.JOURNAL_ISSUE_YEAR=JOURNAL_ISSUE.YEAR AND MANUSCRIPT.JOURNAL_ISSUE_PERIOD=JOURNAL_ISSUE.PERIOD
	WHERE MANUSCRIPT.STATUS = 'Published' AND JOURNAL_ISSUE.DATE_PUBLISHED IS NOT NULL
	ORDER BY CONCAT(JOURNAL_ISSUE.YEAR, JOURNAL_ISSUE.PERIOD), MANUSCRIPT.PAGE_NUMBER_IN_ISSUE ASC;


-- View: ReviewQueue

-- For all manuscripts in UnderReview state. The primary author, manuscript id, and assigned reviewer(s) are 
-- included, ordered by increasing manuscript submission timestamp is included in the view. Also used by ReviewStatus view. Permissions: Editor.

-- Ensured that this returns appropriate data even when a manuscript 
DROP VIEW IF EXISTS `ReviewQueue`;

CREATE VIEW `ReviewQueue` AS
	SELECT AUTHOR.FNAME AS AuthorFName, AUTHOR.LNAME AS AuthorLName, MANUSCRIPT.NUMBER AS ManuscriptNumber, 
	REVIEWER.FNAME AS ReviewerFName, REVIEWER.LNAME AS ReviewerLName, MANUSCRIPT.DATE_RECEIVED AS ManuscriptSubmissionTimestamp
	FROM MANUSCRIPT INNER JOIN AUTHOR ON MANUSCRIPT.AUTHOR_ID = AUTHOR.ID
	INNER JOIN REVIEWER_GROUP ON MANUSCRIPT.NUMBER = REVIEWER_GROUP.MANUSCRIPT_NUMBER
	INNER JOIN REVIEWER ON REVIEWER_GROUP.REVIEWER_NUMBER = REVIEWER.NUMBER
	WHERE MANUSCRIPT.STATUS = 'Under Review'
	ORDER BY MANUSCRIPT.DATE_RECEIVED ASC;



-- View: WhatsLeft

-- For all manuscripts, the current status and the remaining steps 
-- (e.g., ‘underreview’, typeset’, etc.) following the current status. 
-- When a manuscript is in ‘underreview’ state its next step will be either
-- ‘accepted’ or ‘rejected’. Permissions: Editor.

-- Received -> Under Review/Rejected
-- Under Review -> Accepted/Rejected
-- Accepted -> Typeset
-- Typeset -> Scheduled
-- Scheduled -> Published
DROP VIEW IF EXISTS `WhatsLeft`;

CREATE VIEW `WhatsLeft` AS
	SELECT MANUSCRIPT.NUMBER AS ManuscriptNumber, MANUSCRIPT.STATUS as ManuscriptStatus, 
	(CASE 
		WHEN MANUSCRIPT.STATUS='Received' THEN 'Under Review or Rejected' 
		WHEN MANUSCRIPT.STATUS='Under Review' THEN 'Accepted or Rejected' 
		WHEN MANUSCRIPT.STATUS='Accepted' THEN 'Typeset' 
		WHEN MANUSCRIPT.STATUS='Typeset' THEN 'Scheduled' 
		WHEN MANUSCRIPT.STATUS='Scheduled' THEN 'Published'  
		WHEN MANUSCRIPT.STATUS='Published' THEN 'N/A' 
		WHEN MANUSCRIPT.STATUS='Rejected' THEN 'N/A' 
		ELSE 'Error' END) AS NextSteps
	FROM MANUSCRIPT
	ORDER BY MANUSCRIPT.STATUS;


-- -   the timestamp when it was assigned to this review
-- -   the manuscript id
-- -   the manuscript title
-- -   the review results (integer values 1-10)
--     -   appropriateness
--     -   clarity
--     -   methodology
--     -   contribution to the field
-- -   recommendation (either "accept" or "reject") ordered by increasing submission timestamp.  **Permissions: Editor, Reviewer.**
DROP VIEW IF EXISTS `ReviewStatus`;

CREATE VIEW `ReviewStatus` AS
	SELECT MANUSCRIPT.NUMBER AS ManuscriptNumber, MANUSCRIPT.TITLE AS ManuscriptTitle, 
	REVIEWER_GROUP.DATE_MAN_SENT_FOR_REVIEW AS DateManSentForReview, REVIEW.APPROPRIATENESS AS Appropriateness, 
	REVIEW.CLARITY AS Clarity, REVIEW.METHODOLOGY AS Methodology, REVIEW.CONTRIBUTION AS Contribution, 
	REVIEW.RECOMMENDATION AS Recommendation, REVIEW.DATE_REVIEW_RECEIVED AS DateReviewReceived
	FROM REVIEW NATURAL JOIN MANUSCRIPT NATURAL JOIN REVIEWER_GROUP
	WHERE MANUSCRIPT.NUMBER=REVIEW.MANUSCRIPT_NUMBER AND REVIEW.REVIEWER_NUMBER=REVIEWER_GROUP.REVIEWER_NUMBER
	ORDER BY REVIEW.DATE_REVIEW_RECEIVED, MANUSCRIPT.NUMBER;


-- Shows all manuscripts with only 1 active reviewer
DROP VIEW IF EXISTS `OnlyReviewer`;

CREATE VIEW `OnlyReviewer` AS
	SELECT REVIEWER_GROUP.MANUSCRIPT_NUMBER as ManuscriptNumber, REVIEWER.NUMBER as ReviewerNumber
	FROM REVIEWER_GROUP  
	LEFT JOIN REVIEWER ON REVIEWER_GROUP.REVIEWER_NUMBER = REVIEWER.NUMBER
	WHERE REVIEWER.STATUS='Active'
	GROUP BY REVIEWER_GROUP.MANUSCRIPT_NUMBER HAVING COUNT(REVIEWER_GROUP.MANUSCRIPT_NUMBER) = 1;





SELECT MANUSCRIPT.STATUS, COUNT(*) FROM MANUSCRIPT WHERE MANUSCRIPT.AUTHOR_ID=2 GROUP BY MANUSCRIPT.STATUS;

SELECT MANUSCRIPT.NUMBER as ManuscriptNumber, MANUSCRIPT.TITLE as ManuscriptTitle, MANUSCRIPT.STATUS
as ManuscriptStatus FROM MANUSCRIPT WHERE MANUSCRIPT.AUTHOR_ID=2;


UPDATE MANUSCRIPT SET STATUS='Accepted', DATE_ACCEPTED="2016-09-17 06:49:17" WHERE MANUSCRIPT.NUMBER=1;





UPDATE MANUSCRIPT SET STATUS='Scheduled', MANUSCRIPT.JOURNAL_ISSUE_YEAR='1990', MANUSCRIPT.JOURNAL_ISSUE_PERIOD='3' WHERE MANUSCRIPT.NUMBER=1;


UPDATE JOURNAL_ISSUE SET DATE_PUBLISHED='2017-09-22 00:06:36' WHERE YEAR=101 AND PERIOD=4;

SELECT JOURNAL_ISSUE.DATE_PUBLISHED as DatePub FROM JOURNAL_ISSUE WHERE YEAR=1990 AND PERIOD=3;



SELECT MANUSCRIPT.NUMBER as Number FROM MANUSCRIPT WHERE MANUSCRIPT.JOURNAL_ISSUE_YEAR=11 AND MANUSCRIPT.JOURNAL_ISSUE_PERIOD=11;




SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT NATURAL JOIN REVIEWER_GROUP 
WHERE MANUSCRIPT.NUMBER=REVIEWER_GROUP.REVIEWER_NUMBER AND REVIEWER_GROUP.REVIEWER_NUMBER=4 GROUP BY MANUSCRIPT.STATUS;

SELECT * FROM MANUSCRIPT NATURAL JOIN REVIEWER_GROUP 
WHERE MANUSCRIPT.NUMBER=REVIEWER_GROUP.REVIEWER_NUMBER AND REVIEWER_GROUP.REVIEWER_NUMBER=4 GROUP BY MANUSCRIPT.STATUS;




