-- RAJIV RAMAIAH
-- DATABASES

-- test that insert works where 1 reviewer (#1) with code 94 is resigned but another reviewer(#2) with code 94 isn't
INSERT INTO MANUSCRIPT (NUMBER, TITLE, STATUS, CONTENT, DATE_RECEIVED, RI_CODE, AUTHOR_ID, EDITOR_ID, PAGE_NUMBER_IN_ISSUE, ORDER_IN_ISSUE, DATE_ACCEPTED, 
	NUMBER_OF_PAGES, JOURNAL_ISSUE_YEAR, JOURNAL_ISSUE_PERIOD) VALUES 
	(32,"Title 32","Under Review","asdf","2017-03-11 01:21:47",94,2,1,NULL,NULL,NULL,NULL,NULL,NULL);

 -- this does not work since no reviewer inserted has an ri code of 1
INSERT INTO MANUSCRIPT (NUMBER, TITLE, STATUS, CONTENT, DATE_RECEIVED, RI_CODE, AUTHOR_ID, EDITOR_ID, PAGE_NUMBER_IN_ISSUE, ORDER_IN_ISSUE, DATE_ACCEPTED, 
	NUMBER_OF_PAGES, JOURNAL_ISSUE_YEAR, JOURNAL_ISSUE_PERIOD) VALUES 
	(33,"Title 33","Under Review","asdf","2017-03-11 01:21:47",1,2,1,NULL,NULL,NULL,NULL,NULL,NULL);

-- this does not work since the reviewer(#1) for ri code 70 is resigned and is the only reviewer with that code.
INSERT INTO MANUSCRIPT (NUMBER, TITLE, STATUS, CONTENT, DATE_RECEIVED, RI_CODE, AUTHOR_ID, EDITOR_ID, PAGE_NUMBER_IN_ISSUE, ORDER_IN_ISSUE, DATE_ACCEPTED, 
	NUMBER_OF_PAGES, JOURNAL_ISSUE_YEAR, JOURNAL_ISSUE_PERIOD) VALUES 
	(33,"Title 33","Under Review","asdf","2017-03-11 01:21:47",70,2,1,NULL,NULL,NULL,NULL,NULL,NULL);

-- this works since there are active reviewers with ri code 109
INSERT INTO MANUSCRIPT (NUMBER, TITLE, STATUS, CONTENT, DATE_RECEIVED, RI_CODE, AUTHOR_ID, EDITOR_ID, PAGE_NUMBER_IN_ISSUE, ORDER_IN_ISSUE, DATE_ACCEPTED, 
	NUMBER_OF_PAGES, JOURNAL_ISSUE_YEAR, JOURNAL_ISSUE_PERIOD) VALUES 
	(33,"Title 33","Under Review","asdf","2017-03-11 01:21:47",109,2,1,NULL,NULL,NULL,NULL,NULL,NULL);

-- THIS IS THE DATA FROM OnlyReviewer, showing manuscripts that have only one active reviewer

-- MariaDB [rajiv_db]> SELECT * FROM OnlyReviewer;
-- +------------------+----------------+
-- | ManuscriptNumber | ReviewerNumber |
-- +------------------+----------------+
-- |                1 |              6 |
-- |                2 |              4 |
-- |                3 |              3 |
-- |                4 |              4 |
-- |                7 |              2 |
-- |               19 |              2 |
-- |               31 |              7 |
-- +------------------+----------------+
-- 7 rows in set (0.00 sec)


-- resign reviewer 4, both manuscript 2 and 4 are under review and should be change -> works as expected
UPDATE REVIEWER 
	SET REVIEWER.STATUS = 'Resigned'
	WHERE REVIEWER.NUMBER=4;

-- After executing the above update, manuscript 5 is included int OnlyReviewer since it now only has one active reviewer
-- Also notice that reviewer 4 is no longer included as they have just resigned.
-- MariaDB [rajiv_db]> SELECT * FROM OnlyReviewer;
-- +------------------+----------------+
-- | ManuscriptNumber | ReviewerNumber |
-- +------------------+----------------+
-- |                1 |              6 |
-- |                3 |              3 |
-- |                5 |              5 |
-- |                7 |              2 |
-- |               19 |              2 |
-- |               31 |              7 |
-- +------------------+----------------+
-- 6 rows in set (0.00 sec)

-- test that resigning reviewer 7 changes an under review manuscript (#31) to received
UPDATE REVIEWER 
	SET REVIEWER.STATUS = 'Resigned'
	WHERE REVIEWER.NUMBER=7;


-- can set reviewer 7 back to active for demonstration purposes.
-- UPDATE REVIEWER 
-- 	SET REVIEWER.STATUS = 'Active'
-- 	WHERE REVIEWER.NUMBER=7;

-- this resigns reviewer 2 who is the only reviewer for manuscripts 7 and 19.
-- manuscript 7 is not under review so its status does not change but manuscript 19 is
-- so its status reverts to received and the reviewer is resigned.
UPDATE REVIEWER 
	SET REVIEWER.STATUS = 'Resigned'
	WHERE REVIEWER.NUMBER=2;

-- reviewer 6 is the only reviewer for manuscript 1 which is under reviewer. this works as desired.
UPDATE REVIEWER 
	SET REVIEWER.STATUS = 'Resigned'
	WHERE REVIEWER.NUMBER=6;

-- reviewer 3 is the only reviewer for manuscript 3 which is under review.
UPDATE REVIEWER 
	SET REVIEWER.STATUS = 'Resigned'
	WHERE REVIEWER.NUMBER=3;

-- reviewer number 5 is the only reviewer left for manuscript 5 (not under review)
-- since reviewer 4 resigned earlier. this doesn't changed the manuscripts status as it shouldn't
UPDATE REVIEWER 
	SET REVIEWER.STATUS = 'Resigned'
	WHERE REVIEWER.NUMBER=5;

-- After the above commands are run, no manuscript has only one reviewer as all have resigned.



