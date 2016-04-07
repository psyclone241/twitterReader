# Helper script for setting up your apps local instance
# Contributors:
# Roy Keyes <keyes@ufl.edu>

help:
	@echo "Available tasks :"
	@echo "\tread - Print the output from your feeds to the terminal"
	@echo "\treadtofile - Save the output from your feeds to a file (FILE=filename.json)"

read:
	@python twitterReader.py

readtofile:
	@python twitterReader.py -o json -s $$FILE
