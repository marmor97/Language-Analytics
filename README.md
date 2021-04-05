# Language-analytics
This repository contains all code for the course Language Analytics as part of the Bachelors tilvalg in Cultural Data Science.
Below, you will find a guide to clone the repository and execute the latest code developed.


## Week 2
To use the files in this repository, please clone this repo to the place you work with the following command:

``git clone https://github.com/marmor97/Language-Analytics``

``cd Language-Analytics/W2``

``bash ./create_venv.sh``


Under W2 you will find a src folder from where you can execute the script collocation.py. To move to this folder and run the script from the terminal type:

``src/python3 collocation.py``

## Week 4
To run the script collecting sentiments for abc news, you first have to set up a virtual environment. This is done by first moving to the W4 folder and then running the bash command:


``cd Language-Analytics/W4``

``bash create_venv_w4.sh``

Now you should be able to run

``python3 sentiment.py``

Saved plots and interpretation of results are in the W4 folder as well.

## Week 6
To run the script generating network from an edgelist, you first have to set up a virtual environment. This is done by first moving to the W6 folder and then running the bash command:

``cd Language-Analytics/W6``

``bash create_venv_w6.sh``

``source marmor_langw6/bin/activate``

Now you should have activated the environment and you can execute the following line to run the script

``python3 network.py``


## Week 9
The script for this assignment performs a logistic regression on Reddit data containing depressed and suicidal subreddits and tries to distinguish between these.  First you have to set up a virtual environment. This is done by first moving to the W9 folder and then running the bash command:

``cd Language-Analytics/W9``

``bash create_venv_w9.sh``

``source marmor_langw9/bin/activate``

Now you should have activated the environment and you can execute the following line to run the script

``python3 src/log_reddit.py``
