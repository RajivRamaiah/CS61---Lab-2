-- RAJIV RAMAIAH
-- DATABASES


-- CREATE TABLES

-- USED MYSQL WORKBENCH FORWARD ENGINEERING TO GENERATE TABLES WITH MODIFICATIONS OF MY OWN

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema rajiv_db
-- -----------------------------------------------------
-- Reset Database
-- DROP DATABASE IF EXISTS `rajiv_db`;
-- -- -----------------------------------------------------
-- Schema rajiv_db
-- -----------------------------------------------------
-- CREATE SCHEMA IF NOT EXISTS `rajiv_db` DEFAULT CHARACTER SET utf8 ;
USE `rajiv_db` ;

-- -----------------------------------------------------
-- Table `rajiv_db`.`EDITOR`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`EDITOR`;
-- 
CREATE TABLE `rajiv_db`.`EDITOR` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FNAME` VARCHAR(45) NOT NULL,
  `LNAME` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rajiv_db`.`REVIEWER`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`REVIEWER`;
-- 
CREATE TABLE `rajiv_db`.`REVIEWER` (
  `NUMBER` INT NOT NULL AUTO_INCREMENT,
  `FNAME` VARCHAR(45) NOT NULL,
  `LNAME` VARCHAR(45) NOT NULL,
  `EMAIL` VARCHAR(45) NOT NULL,
  `AFFILIATION` VARCHAR(45) NOT NULL,
  `STATUS` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`NUMBER`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rajiv_db`.`RI_CODE`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`RI_CODE`;
-- 
CREATE TABLE `rajiv_db`.`RI_CODE` (
  `RI_CODE` INT NOT NULL AUTO_INCREMENT,
  `SUBJECT` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`RI_CODE`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rajiv_db`.`AUTHOR`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`AUTHOR`;
-- 
CREATE TABLE `rajiv_db`.`AUTHOR` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FNAME` VARCHAR(45) NOT NULL,
  `LNAME` VARCHAR(45) NOT NULL,
  `MAILING_ADDRESS` VARCHAR(45) NOT NULL,
  `E_MAIL` VARCHAR(45) NOT NULL,
  `AFFILIATION` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB
COMMENT = 'AUTH_MAILING_ADDRESS';


-- -----------------------------------------------------
-- Table `rajiv_db`.`JOURNAL_ISSUE`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`JOURNAL_ISSUE`;
-- 
CREATE TABLE `rajiv_db`.`JOURNAL_ISSUE` (
  `YEAR` INT NOT NULL,
  `PERIOD` INT NOT NULL,
  `DATE_PUBLISHED` DATETIME NULL,
  PRIMARY KEY (`YEAR`, `PERIOD`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rajiv_db`.`MANUSCRIPT`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`MANUSCRIPT`;
-- 
CREATE TABLE `rajiv_db`.`MANUSCRIPT` (
  `NUMBER` INT NOT NULL AUTO_INCREMENT,
  `TITLE` VARCHAR(45) NOT NULL,
  `STATUS` VARCHAR(45) NOT NULL,
  `CONTENT` BLOB NOT NULL,
  `DATE_RECEIVED` DATETIME NOT NULL,
  `RI_CODE` INT NOT NULL,
  `AUTHOR_ID` INT NOT NULL,
  `EDITOR_ID` INT NULL,
  `PAGE_NUMBER_IN_ISSUE` INT NULL,
  `ORDER_IN_ISSUE` INT NULL,
  `DATE_ACCEPTED` VARCHAR(45) NULL,
  `NUMBER_OF_PAGES` INT NULL,
  `JOURNAL_ISSUE_YEAR` INT NULL,
  `JOURNAL_ISSUE_PERIOD` INT NULL,
  PRIMARY KEY (`NUMBER`),
  INDEX `fk_MANUSCRIPT_RI_CODE1_idx` (`RI_CODE` ASC),
  INDEX `fk_MANUSCRIPT_AUTHOR1_idx` (`AUTHOR_ID` ASC),
  INDEX `fk_MANUSCRIPT_EDITOR1_idx` (`EDITOR_ID` ASC),
  INDEX `fk_MANUSCRIPT_JOURNAL_ISSUE1_idx` (`JOURNAL_ISSUE_YEAR` ASC, `JOURNAL_ISSUE_PERIOD` ASC),
  CONSTRAINT `fk_MANUSCRIPT_RI_CODE1`
    FOREIGN KEY (`RI_CODE`)
    REFERENCES `rajiv_db`.`RI_CODE` (`RI_CODE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MANUSCRIPT_AUTHOR1`
    FOREIGN KEY (`AUTHOR_ID`)
    REFERENCES `rajiv_db`.`AUTHOR` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MANUSCRIPT_EDITOR1`
    FOREIGN KEY (`EDITOR_ID`)
    REFERENCES `rajiv_db`.`EDITOR` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MANUSCRIPT_JOURNAL_ISSUE1`
    FOREIGN KEY (`JOURNAL_ISSUE_YEAR` , `JOURNAL_ISSUE_PERIOD`)
    REFERENCES `rajiv_db`.`JOURNAL_ISSUE` (`YEAR` , `PERIOD`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rajiv_db`.`REVIEW`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`REVIEW`;
-- 
CREATE TABLE `rajiv_db`.`REVIEW` (
  `REVIEWER_NUMBER` INT NOT NULL,
  `MANUSCRIPT_NUMBER` INT NOT NULL,
  `DATE_REVIEW_RECEIVED` DATETIME NOT NULL,
  `APPROPRIATENESS` INT NOT NULL,
  `CLARITY` INT NOT NULL,
  `METHODOLOGY` INT NOT NULL,
  `CONTRIBUTION` INT NOT NULL,
  `RECOMMENDATION` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MANUSCRIPT_NUMBER`, `REVIEWER_NUMBER`),
  INDEX `fk_REVIEW_REVIEWER1_idx` (`REVIEWER_NUMBER` ASC),
  CONSTRAINT `fk_REVIEW_REVIEWER1`
    FOREIGN KEY (`REVIEWER_NUMBER`)
    REFERENCES `rajiv_db`.`REVIEWER` (`NUMBER`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `rajiv_db`.`SECONDARY_AUTHOR`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`SECONDARY_AUTHOR`;
-- 
CREATE TABLE `rajiv_db`.`SECONDARY_AUTHOR` (
  `MANUSCRIPT_NUMBER` INT NOT NULL,
  `ORDER_IN_MANUSCRIPT` INT NOT NULL,
  `FNAME` VARCHAR(45) NOT NULL,
  `LNAME` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MANUSCRIPT_NUMBER`, `ORDER_IN_MANUSCRIPT`),
  INDEX `fk_SECONDARY_AUTHOR_MANUSCRIPT1_idx` (`MANUSCRIPT_NUMBER` ASC),
  CONSTRAINT `fk_SECONDARY_AUTHOR_MANUSCRIPT1`
    FOREIGN KEY (`MANUSCRIPT_NUMBER`)
    REFERENCES `rajiv_db`.`MANUSCRIPT` (`NUMBER`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rajiv_db`.`REVIEWER_GROUP`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`REVIEWER_GROUP`;
-- 
CREATE TABLE `rajiv_db`.`REVIEWER_GROUP` (
  `MANUSCRIPT_NUMBER` INT NOT NULL,
  `REVIEWER_NUMBER` INT NOT NULL,
  `DATE_MAN_SENT_FOR_REVIEW` DATETIME NOT NULL,
  PRIMARY KEY (`MANUSCRIPT_NUMBER`, `REVIEWER_NUMBER`),
  CONSTRAINT `fk_MANUSCRIPT_has_REVIEWER_MANUSCRIPT1`
    FOREIGN KEY (`MANUSCRIPT_NUMBER`)
    REFERENCES `rajiv_db`.`MANUSCRIPT` (`NUMBER`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MANUSCRIPT_has_REVIEWER_REVIEWER1`
    FOREIGN KEY (`REVIEWER_NUMBER`)
    REFERENCES `rajiv_db`.`REVIEWER` (`NUMBER`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `rajiv_db`.`CODE_GROUP`
-- -----------------------------------------------------
-- DROP TABLE IF EXISTS `rajiv_db`.`CODE_GROUP`;
-- 
CREATE TABLE `rajiv_db`.`CODE_GROUP` (
  `REVIEWER_NUMBER` INT NOT NULL,
  `RI_CODE` INT NOT NULL,
  PRIMARY KEY (`REVIEWER_NUMBER`, `RI_CODE`),
  INDEX `fk_REVIEWER_has_RI_CODE_RI_CODE1_idx` (`RI_CODE` ASC),
  INDEX `fk_REVIEWER_has_RI_CODE_REVIEWER1_idx` (`REVIEWER_NUMBER` ASC),
  CONSTRAINT `fk_REVIEWER_has_RI_CODE_REVIEWER1`
    FOREIGN KEY (`REVIEWER_NUMBER`)
    REFERENCES `rajiv_db`.`REVIEWER` (`NUMBER`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_REVIEWER_has_RI_CODE_RI_CODE1`
    FOREIGN KEY (`RI_CODE`)
    REFERENCES `rajiv_db`.`RI_CODE` (`RI_CODE`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;





-- INSERT DATA


-- Delete Current Data From Tables
DELETE FROM CODE_GROUP;
DELETE FROM REVIEWER_GROUP;
DELETE FROM SECONDARY_AUTHOR;
DELETE FROM MANUSCRIPT;
DELETE FROM EDITOR;
DELETE FROM RI_CODE;
DELETE FROM AUTHOR;
DELETE FROM MANUSCRIPT;
DELETE FROM JOURNAL_ISSUE;
DELETE FROM REVIEW;
DELETE FROM REVIEWER;



-- Reset Auto Incrementing Keys
ALTER TABLE EDITOR AUTO_INCREMENT = 1;
ALTER TABLE REVIEWER AUTO_INCREMENT = 1;
ALTER TABLE AUTHOR AUTO_INCREMENT = 1;
ALTER TABLE MANUSCRIPT AUTO_INCREMENT = 1;
ALTER TABLE RI_CODE AUTO_INCREMENT = 1;

-- 3 editors
INSERT INTO EDITOR (FNAME,LNAME) VALUES 
  ("Fulton","Zahir"),
  ("Hunter","Yardley"),
  ("Todd","Clayton");


-- 4 authors
INSERT INTO AUTHOR (FNAME,LNAME,MAILING_ADDRESS,E_MAIL,AFFILIATION) VALUES 
  ("George","Travis","546-220 Ac Av.","a.odio@augue.org","Magnis Dis LLC"),
  ("Dalton","Alfonso","434-6898 Lacus Avenue","Aenean.massa.Integer@dui.org","Aliquet Associates"),
  ("Gareth","Nehru","P.O. Box 174, 8982 A St.","et.malesuada@adipiscingelitEtiam.edu","Ut Semper Pretium Limited"),
  ("Elmo","Kasper","721-9959 Habitant Rd.","posuere.at.velit@Nullam.co.uk","Montes Inc.");

-- 7 reviewers
INSERT INTO REVIEWER (FNAME,LNAME,EMAIL,AFFILIATION,STATUS) VALUES 
  ("Carter","Stuart","velit.in@vestibulumneque.org","Euismod In Foundation", "Resigned"),
  ("David","Amos","eleifend.Cras.sed@elitsed.com","Sodales At Industries", "Active"),
  ("Carlos","Gray","aliquet.vel@duinec.net","Suspendisse PC", "Active"),
  ("Ignatius","Zane","sem.Pellentesque.ut@utlacusNulla.edu","Justo Eu Arcu LLP", "Active"),
  ("Cain","Dolan","Integer.mollis@duiSuspendisseac.co.uk","Nunc PC", "Active"),
  ("Ronan","Brenden","eu@purusNullamscelerisque.co.uk","Euismod Urna Nullam Ltd", "Active"),
  ("Chester","Jin","malesuada.id@scelerisque.ca","Aenean Euismod Mauris Ltd", "Active");

INSERT INTO JOURNAL_ISSUE (YEAR,PERIOD,DATE_PUBLISHED) VALUES 
  (1990,3,"2018-02-23 11:53:24"),
  (1995,4,"2017-09-22 00:06:36"),
  (2009,4,"2017-08-30 15:55:51"),
  (2007,4,"2018-04-21 07:03:43"),
  (2001,1,NULL),
  (2011,2,NULL),
  (2013,4,NULL);


INSERT INTO RI_CODE (SUBJECT) VALUES
  ('Agricultural engineering'),
  ('Biochemical engineering'),
  ('Biomechanical engineering'),
  ('Ergonomics'),
  ('Food engineering'),
  ('Bioprocess engineering'),
  ('Genetic engineering'),
  ('Human genetic engineering'),
  ('Metabolic engineering'),
  ('Molecular engineering'),
  ('Neural engineering'),
  ('Protein engineering'),
  ('Rehabilitation engineering'),
  ('Tissue engineering'),
  ('Aquatic and environmental engineering'),
  ('Architectural engineering'),
  ('Civionic engineering'),
  ('Construction engineering'),
  ('Earthquake engineering'),
  ('Earth systems engineering and management'),
  ('Ecological engineering'),
  ('Environmental engineering'),
  ('Geomatics engineering'),
  ('Geotechnical engineering'),
  ('Highway engineering'),
  ('Hydraulic engineering'),
  ('Landscape engineering'),
  ('Land development engineering'),
  ('Pavement engineering'),
  ('Railway systems engineering'),
  ('River engineering'),
  ('Sanitary engineering'),
  ('Sewage engineering'),
  ('Structural engineering'),
  ('Surveying'),
  ('Traffic engineering'),
  ('Transportation engineering'),
  ('Urban engineering'),
  ('Irrigation and agriculture engineering'),
  ('Explosives engineering'),
  ('Biomolecular engineering'),
  ('Ceramics engineering'),
  ('Broadcast engineering'),
  ('Building engineering'),
  ('Signal Processing'),
  ('Computer engineering'),
  ('Power systems engineering'),
  ('Control engineering'),
  ('Telecommunications engineering'),
  ('Electronic engineering'),
  ('Instrumentation engineering'),
  ('Network engineering'),
  ('Neuromorphic engineering'),
  ('Engineering Technology'),
  ('Integrated engineering'),
  ('Value engineering'),
  ('Cost engineering'),
  ('Fire protection engineering'),
  ('Domain engineering'),
  ('Engineering economics'),
  ('Engineering management'),
  ('Engineering psychology'),
  ('Ergonomics'),
  ('Facilities Engineering'),
  ('Logistic engineering'),
  ('Model-driven engineering'),
  ('Performance engineering'),
  ('Process engineering'),
  ('Product Family Engineering'),
  ('Quality engineering'),
  ('Reliability engineering'),
  ('Safety engineering'),
  ('Security engineering'),
  ('Support engineering'),
  ('Systems engineering'),
  ('Metallurgical Engineering'),
  ('Surface Engineering'),
  ('Biomaterials Engineering'),
  ('Crystal Engineering'),
  ('Amorphous Metals'),
  ('Metal Forming'),
  ('Ceramic Engineering'),
  ('Plastics Engineering'),
  ('Forensic Materials Engineering'),
  ('Composite Materials'),
  ('Casting'),
  ('Electronic Materials'),
  ('Nano materials'),
  ('Corrosion Engineering'),
  ('Vitreous Materials'),
  ('Welding'),
  ('Acoustical engineering'),
  ('Aerospace engineering'),
  ('Audio engineering'),
  ('Automotive engineering'),
  ('Building services engineering'),
  ('Earthquake engineering'),
  ('Forensic engineering'),
  ('Marine engineering'),
  ('Mechatronics'),
  ('Nanoengineering'),
  ('Naval architecture'),
  ('Sports engineering'),
  ('Structural engineering'),
  ('Vacuum engineering'),
  ('Military engineering'),
  ('Combat engineering'),
  ('Offshore engineering'),
  ('Optical engineering'),
  ('Geophysical engineering'),
  ('Mineral engineering'),
  ('Mining engineering'),
  ('Reservoir engineering'),
  ('Climate engineering'),
  ('Computer-aided engineering'),
  ('Cryptographic engineering'),
  ('Information engineering'),
  ('Knowledge engineering'),
  ('Language engineering'),
  ('Release engineering'),
  ('Teletraffic engineering'),
  ('Usability engineering'),
  ('Web engineering'),
  ('Systems engineering'); 

INSERT INTO MANUSCRIPT (NUMBER, TITLE, STATUS, CONTENT, DATE_RECEIVED, RI_CODE, AUTHOR_ID, EDITOR_ID, PAGE_NUMBER_IN_ISSUE, ORDER_IN_ISSUE, DATE_ACCEPTED, 
  NUMBER_OF_PAGES, JOURNAL_ISSUE_YEAR, JOURNAL_ISSUE_PERIOD) VALUES 
  (1,"Title 1","Under Review","asdf","2017-03-11 01:11:47",54,2,1,NULL,NULL,NULL,NULL,NULL,NULL),
  (2,"Title 2","Under Review","asdf","2017-10-14 00:47:42",113,2,3,NULL,NULL,NULL,NULL,NULL,NULL),
  (3,"Title 3","Under Review","asdf","2017-02-04 13:13:04",109,2,2,NULL,NULL,NULL,NULL,NULL,NULL),
  (4,"Title 4","Under Review","asdf","2016-07-15 13:41:30",115,1,3,NULL,NULL,"2018-01-17 06:08:38",NULL,NULL,NULL),
  (5,"Title 5","Accepted","asdf","2017-03-10 05:14:30",51,3,2,NULL,NULL,"2016-05-16 09:57:47",NULL,NULL,NULL),
  (6,"Title 6","Published","asdf","2018-03-27 03:55:25",12,4,1,53,4,"2017-01-25 18:46:49",33,1990,3),
  (7,"Title 7","Rejected","asdf","2016-06-18 05:53:47",39,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (8,"Title 8","Typeset","asdf","2016-12-10 01:04:32",77,4,1,NULL,NULL,"2018-04-05 18:31:52",NULL,NULL,NULL),
  (9,"Title 9","Rejected","asdf","2017-09-02 16:26:54",92,3,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (10,"Title 10","Typeset","asdf","2018-02-19 08:40:03",63,4,2,NULL,NULL,"2016-09-06 12:15:53",NULL,NULL,NULL),
  (11,"Title 11","Published","asdf","2017-11-29 00:11:54",78,4,1,31,7,"2017-08-27 21:15:58",25,1995,4),
  (12,"Title 12","Received","asdf","2018-04-24 15:28:51",17,1,3,NULL,NULL,NULL,NULL,NULL,NULL),
  (13,"Title 13","Received","asdf","2018-04-17 21:53:33",1,4,3,NULL,NULL,NULL,NULL,NULL,NULL),
  (14,"Title 14","Received","asdf","2018-01-18 15:31:28",14,2,1,NULL,NULL,NULL,NULL,NULL,NULL),
  (15,"Title 15","Published","asdf","2017-07-21 15:00:04",36,1,2,284,0,"2016-07-24 21:00:42",12,2007,4),
  (16,"Title 16","Published","asdf","2017-08-14 05:53:38",9,1,1,436,3,"2018-03-25 10:28:41",32,2007,4),
  (17,"Title 17","Published","asdf","2017-11-24 18:04:13",104,2,1,290,9,"2017-01-14 23:26:35",37,2007,4),
  (18,"Title 18","Typeset","asdf","2018-01-04 14:05:26",43,4,3,NULL,NULL,"2016-08-15 21:08:43",NULL,NULL,NULL),
  (19,"Title 19","Under Review","asdf","2017-10-09 22:58:27",79,4,3,NULL,NULL,NULL,NULL,NULL,NULL),
  (20,"Title 20","Scheduled","asdf","2017-02-22 02:13:59",56,2,3,434,6,"2017-12-05 19:32:37",11,2009,4),
  (21,"Title 21","Received","asdf","2017-03-03 18:02:50",61,1,2,NULL,NULL,NULL,NULL,NULL,NULL),
  (22,"Title 22","Rejected","asdf","2017-06-26 18:38:29",41,3,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (23,"Title 23","Rejected","asdf","2016-08-07 06:52:35",75,3,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (24,"Title 24","Received","Received","2017-07-21 15:00:04",36,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (25,"Title 25","Published","asdf","2011-11-24 18:04:13",104,2,1,296,9,"2013-01-14 23:26:35",37,2007,4),
  (26,"Title 26","Received","asdf","2017-11-24 18:04:13",104,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (27,"Title 27","Received","asdf","2018-01-04 14:05:26",43,4,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (28,"Title 28","Received","asdf","2017-10-09 22:58:27",79,4,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (29,"Title 29","Received","asdf","2017-02-22 02:13:59",56,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (30,"Title 30","Received","asdf","2017-03-03 18:02:50",61,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
  (31,"Title 31","Under Review","asdf","2017-03-11 01:21:47",39,2,1,NULL,NULL,NULL,NULL,NULL,NULL);


INSERT INTO REVIEWER_GROUP (MANUSCRIPT_NUMBER,REVIEWER_NUMBER,DATE_MAN_SENT_FOR_REVIEW) VALUES 
  (7,2,"2016-04-13 17:27:09"),
  (4,4,"2016-09-17 06:49:17"),
  (7,1,"2018-03-19 02:28:44"),
  (19,2,"2016-04-19 01:38:03"),
  (5,4,"2017-10-07 10:47:57"),
  (3,3,"2016-07-02 07:50:34"),
  (1,6,"2017-05-24 20:11:03"),
  (2,4,"2016-09-20 01:09:39"),
  (5,5,"2018-04-09 02:06:54"),
  (31,7,"2016-04-19 01:38:04");

INSERT INTO SECONDARY_AUTHOR (FNAME,LNAME,MANUSCRIPT_NUMBER,ORDER_IN_MANUSCRIPT) VALUES 
  ("Kerry","Aladdin",7,6),
  ("Dalton","Alfonso",4,6),
  ("Quinn","Brent",2,2),
  ("Audrey","Basil",9,8),
  ("Quon","Coby",19,4),
  ("McKenzie","Lawrence",11,5),
  ("MacKensie","Kasper",17,3),
  ("Patience","Caesar",16,2),
  ("Ursula","Patrick",18,8),
  ("Shay","Lyle",5,9),
  ("Maggy","Ronan",16,1),
  ("Lani","Ferris",11,6),
  ("April","Ralph",12,9),
  ("Libby","Brock",7,4),
  ("Karina","Keith",21,7);

INSERT INTO REVIEW (REVIEWER_NUMBER,MANUSCRIPT_NUMBER,DATE_REVIEW_RECEIVED,APPROPRIATENESS,CLARITY,METHODOLOGY,CONTRIBUTION,RECOMMENDATION) VALUES 
  (2,7,"2017-10-22 21:18:41",10,2,5,5,"accept"),
  (4,4,"2017-09-08 11:19:59",1,8,2,3,"reject"),
  (1,7,"2018-01-27 05:49:38",5,2,7,6,"reject"),
  (2,19,"2016-07-01 19:06:26",2,1,5,3,"reject"),
  (4,5,"2016-09-02 09:15:11",7,4,8,3,"reject"),
  (3,3,"2017-08-07 23:27:52",9,8,6,1,"accept"),
  (6,1,"2018-02-25 17:12:25",1,10,9,6,"reject"),
  (4,2,"2017-05-07 20:40:21",5,1,2,9,"reject"),
  (5,5,"2017-11-16 01:10:40",6,8,4,10,"reject");

INSERT INTO CODE_GROUP (REVIEWER_NUMBER,RI_CODE) VALUES 
  (1,94),
  (1,70),
  (1,51),
  (2,51),
  (2,94),
  (2,57),
  (2,39),
  (3,110),
  (3,109),
  (3,20),
  (4,34),
  (4,7),
  (5,99),
  (5,114),
  (6,109),
  (6,36),
  (7,54);



-- CREATE VIEWS

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


