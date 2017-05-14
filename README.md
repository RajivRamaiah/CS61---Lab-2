# CS61---Lab-2
## Rajiv Ramaiah, Dami Apoeso


We have created a simple python driver that allows a user to interact with our manuscript management system developed in the previous parts of the lab. Users can enter in commands by following the specifications of our lab found [here](http://www.cs.dartmouth.edu/~cs61/Labs/Lab%202/Lab%202.html) and by separating command statements using pipes instead of spaces as below:

`register|author|<fname>|<lname>|<email>|<address>`

**TO START: Enter `python Driver.py` at your command line.**

**MASTER KEY: AA12345678**

If you would like to test this on your own database, please run our Setup.sql file and then Triggers.sql file, and then run the program to have data ready to be altered. Or, add your own data from scratch using the program itself!

This program can be extended to be a legitimate manuscript management system for any type of magazine or journal that requires authors to submit articles or papers for review and to be published based on similar criteria as put forward by the domain description from the link above.


## Assumptions and Deviations from Specs
- To log in as an author, reviewer, or editor, use `login|<usertype>|<userID>`
- Use `exit` to exit the main command line when you are not logged in.
- Use `logout` to logout of your user when your are logged in
- We assume that the values will be of appropriate type (i.e String or Int) when inserting data.
- Only a maximum of 3 secondary author can be submitted along with a manuscript.
- We did not implement blob on submit as stated was allowed by the Professor.
- When registering an author, we do mailing address before email, and we allow them to submit a preliminary affiliation as well. This affiliation can be updated if or when they submit a new paper as well.
- A status of `Submitted` is the same as `Received`
- Secondary authors must have a first and last name separated by a space, and cannot have a middle name.
- We do not set a timestamp when manuscript is rejected, as it wasn't included in the domain description originally.
- While the specs show that an editor can schedule a manuscript using `schedule <manu#> <issue>`, issue requires issue year and period to be complete. Thus to include an issue in any query, you must use `schedule|<manu#>|<IssueYear|<IssuePeriod`
- When scheduling, we make sure that the manuscript status is `Typeset`, not `Accepted` as is stated in the specs and contradicted in the domain description
- For any editors/authors/reviewers in the system as a result of running Setup.sql, which is any user you don't register, their password is: `a`
- We check to make sure that when assigning to a reviewer they have the RICode to handle the manuscript.



add checks to make sure status changes follow the correct sequence like accept->typeset->schedule->publish

only assign manuscript to reviewer if it hasn't been assigned