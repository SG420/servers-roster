# servers-roster
A simple Python script to generate a servers roster based on a CSV file
specifying the available servers

## Setup & Usage
First, ensure you have [Python](https://www.python.org/) installed and added to your path. You will also need to install
[Git](https://git-scm.com/) if you haven't already, to download the files.
Next, open a terminal and run:
```
git clone https://github.com/SG420/servers-roster.git
cd servers-roster
```
Next, create a file called `servers.csv`, and enter the names of the servers who you
want to be included on the roster for each role. Separate each server with a
comma. MC, TH, AC1, AC2 and CB must be put in that order, any additional
optional roles can also be included, but don't have to be. Optional roles will
only be filled if there are enough servers left after generating the roster for
the main 5 roles. An example `servers.csv` is shown below:

```
MC, Person1, Person2
TH, Person1, Person2, Person3
AC1, Person1, Person2, Person3, Person4
AC2, Person1, Person2, Person3, Person4, Person5
CB, Person3, Person4, Person5
BB, Person5, Person6, Person7
TB1, Person5, Person6, Person7
TB2, Person5, Person6, Person7
```

Torch bearers (`TB`) will only be rostered if it is possible to roster 2 of
them. At present, this only works for the first 2 torch bearers (meaning that if
you include more than 2 TB roles, e.g TB3 and TB4, it is possible it will roster
an odd-number of torch bearers, and you will have to manually adjust the roster)

Once you have specified who is to be included on the roster, run the script
from the directory it is saved in (from the same terminal as before) using:
```
python3 roster.py 
```

By default, 4 rosters (weeks) will be generated, for each week, you will be
asked if you would like to exclude someone from the roster for that week.
When prompted, one at a time, you can put the names of servers to exclude for
that week. Once you have entered a name and hit enter, it will ask you what role
to exclude them from, you can either enter a specific role, or enter `ALL`. It
will allow you to exclude from more roles, hit enter without entering anything
to finish adding roles to exclude for that person.

Once the roster is generated, it will both print it to the terminal, and ask you
for a filename to save the roster as. Leaving this blank will result in the
roster not being saved. It will be saved as a CSV file, which can then easily be
opened in a spreadsheet program for simple viewing/manual editing
