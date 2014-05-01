get_tweets:

This will get the tweets for a particular movie. You will have to specify the movie name as command line argument
Also to control the number of tweets, you can change the loop counter break condition value.

senti_word.py:

This parses SentiWordNet list - the sentiword.txt file and then create the senti word dictionary - the file senti_word_final that we use for our sentiment analysis.
Preferably this code is run only once and then saving it using a dump. This dictionary to be used in preprocess.py is then loaded in that code.

preprocess.py:

The code runs only in windows
This file does the pre-processing on the raw twitter data file - file_name variable.
After running this, it spits out processed.txt file which is then further used to doing the sentiment analysis.


Project_mainfile : It is the main file where the entire algorithm runs as described in the paper . Currently this is an offline where we manually enter the movie name 
					  This code also generates positive or negative rating of each category of movie (like acting etc) and also it generates top tweets within each category.
					  This file takes lot of time for execution.
					  Note : we need to manually set the movie names and paths of various file names within the code. (all filenames follow this path C:\IRProject)
					  
GetFeatures.py : This file categorizes different nouns into the main five categories as mentioned in the report

We have generated two files by running our code offline. We stored these files which are given as an input to the php code

In order to run the website run movie.php and enter the movie name (for now enter "rockstar" or "highway") then the output of ratings will be shown