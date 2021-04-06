# system tools
import os
import sys
import argparse
sys.path.append(os.path.join(".."))

# data munging tools
import pandas as pd
import numpy as np
import utils.classifier_utils as clf

# Machine learning stuff
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import ShuffleSplit
from sklearn import metrics
from sklearn.model_selection import cross_validate

# Visualisation
import matplotlib.pyplot as plt
import seaborn as sns


class reddit_lr():
    """This is a class for performing a Logistic regression on a Kaggle dataset containing depressed and suicide sub-reddits.
    """
    def __init__(self, args):
        self.args = args
       # Load file
        self.data = pd.read_csv(self.args["filename"], dtype={"text": "string", "class": "string"})
        self.data = self.data.dropna()

        # Balance and split
        self.data_balanced = clf.balance(self.data) # This function uses the same as in class and balances the data based on label - I have changed it to use "class" insteat of "label" and it takes 10000 of each class as default
        self.texts = self.data_balanced["text"] # Assigning to separate objects
        self.labels = self.data_balanced["class"]


    # Vectorization
    def vectorization(self):
        """Function for vectorizing input text.
        """
        vectorizer = TfidfVectorizer(ngram_range = (1,4), # As our input we are taking n-grams / combinations of tokens which appear together in the data. One word is a uni-gram. Here were are using unigrams,  bi-grams, trigrams and fourgrams (?) as input.
                                     lowercase = True, # Telling the vectorizer that we want to take the input data annd make all lowercase
                                     max_df = 0.95, # Filtering based on how common / infrequent a word is - max_df = maximum number of documents that the word is allowed to appear in. If it appears in more than 95 % of the documents - remove it
                                     min_df = 0.05, # Below 5 % occurences are also removed
                                     max_features = 500) # Keep only top 500 features - most informative features
        # Applying it to our texts
        self.X_vect = vectorizer.fit_transform(self.texts) # Full dataset


    def classify(self):
        """Function for making classification and getting results
        """
        self.classifier = LogisticRegression(random_state=2021) # Random state to reproduce results
        self.cv = ShuffleSplit(n_splits = 10, test_size = 0.2, random_state = 2021) # Use this to create 10 different samples of train and test set
        self.cv_results = cross_validate(self.classifier, # Cross validate uses the classfier and cross-validation method specified to get accuracies and f-scores
                       self.X_vect, 
                       self.labels,
                       scoring=["accuracy", "f1_macro"], 
                       cv=self.cv,
                       return_estimator=True)

    def save_results(self):
        """Function for printing evaluation metrics and saving learning curve plot.
        """
        print(pd.DataFrame(self.cv_results)) # Printing information of each of the folds to the terminal
        summary = f"The mean accuracy and f1-score in a 10-fold cv is {np.mean(self.cv_results['test_accuracy']).round(3)} and {np.mean(self.cv_results['test_f1_macro']).round(3)} with a std of {np.std(self.cv_results['test_accuracy']).round(3)} and {np.std(self.cv_results['test_f1_macro']).round(3)}" # Creating a str object with mean accuracy and f-score and sd accuracy and f-score
        with open(self.args["out_filename"], "w", encoding = "utf-8") as file: # Save as .txt file
            file.write(summary)
        
        title = "Learning Curve for model discriminating between suicide and depression subreddits (Logistic Regression)"
        # Taking the model, fitting vectorized data to it w cross-validation
        clf.plot_learning_curve(self.classifier, title, self.X_vect, self.labels, cv = self.cv, n_jobs = 4)
        ## First plot
        # If two curves are close to eachother and both of them have low score = underfitting (High Bias)
        # If there are large gaps between the two curves the model suffr from an overfitting problem (High Variance)
    
    
def main():
    ap = argparse.ArgumentParser(description="[INFO] class made to run logistic regression on Kaggle data set with suicide and depression subreddits") 
    ap.add_argument("-f", 
                "--filename", 
                required=False, 
                type=str, 
                default= "../data/Cleaned_Depression_Vs_Suicide_sample.csv", 
                help="str, filename for dataset name and location")   
    
    ap.add_argument("-fo", 
                "--out_filename", 
                required=False, 
                type=str, 
                default= "../txt/summary_metrics.txt", 
                help="str, filename for dataset name and location") 
    
    args = vars(ap.parse_args())
    
    
    # Making a lr_reddit object
    reddit = reddit_lr(args = args)
    reddit.vectorization()
    reddit.classify()
    reddit.save_results()
    
if __name__=="__main__":
    main()        
        