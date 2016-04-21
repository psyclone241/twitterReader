# Helper script for setting up your apps local instance
# Contributors:
# Roy Keyes <keyes@ufl.edu>

help:
	@echo "Available tasks :"
	@echo "\tread - Print the output from your feeds to the terminal"
	@echo "\treadtofile - Save the output from your feeds to a file (FILE=filename.json)"
	@echo "\ttraffic - Save the output specifically for my traffic script"

read:
	@python twitterReader.py

readtofile:
	@python twitterReader.py -o json -s $$FILE

traffic:
	@python twitterReader.py -f GACSmarttraffic -o json -s GACSmarttraffic.json -c 30

police:
	@python twitterReader.py -f GainesvillePD -o json -s GainesvillePD.json -c 30

fire:
	@python twitterReader.py -f GFR1882 -o json -s GFR1882.json -c 30
