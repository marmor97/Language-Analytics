import re #regex
import string #regex
import numpy as np #numerical operations
import os #file navigation
from pathlib import Path
import pandas as pd
from glob import glob as gg
from collections import Counter

def file_load(data_path):
    text_list = []    
    for file in Path(data_path).glob("*.txt"): # List all files with .txt extension
        with open(file, "r", encoding = "utf-8") as file: # Opens the file with correct encoding
            loaded_text = file.read()
            text_list.append(loaded_text) # Appends it as an element in our list - now each txt file is an element which we now have to concatenate
    text_concat =" ".join(text_list) # .join concatenates the text with spaces to seperate them - this does mean that when we calculate MI each ending and beginning of two files are included..
    return text_concat # Returns one string file

# A quick regex tokenizer for splitting strings
def tokenize(input_string):
    # Split on any non-alphanumeric character
    tokenizer = re.compile(r"\W+")
    # Tokenize
    token_list = tokenizer.split(input_string)
    token_list = [item.lower() for item in token_list]
    # Return token_list
    return token_list

def collocate_calc(text, keyword, window_size = 2):
    collocate = []
    # word_count_collocates = []
    raw_frequency = []
    MI = []
    window_collocate = []

    counter_object = Counter(text) # Counter works by taking all unique words in text file and counts all the times they occur
    keyword_n = counter_object.get(keyword) # From the counter object we save all the times our keyword occurs in the text
    
    for word_n in range(len(text)): # Takes every position of elements in the text list

        if text[word_n] == keyword: # It the element corresponds to our keyword we will make a window 
            index_value = word_n
            left_window = max(0, index_value - window_size) #2 words on left side
            right_window = index_value + window_size + 1 #2 words on right side -  Plus one to include equal sizes on each side
            window_list = text[left_window : right_window] # Making a specific list with words

            for word in window_list:
                if word == keyword: 
                    pass
                else:
                    window_collocate.append(word) # Save what the word is                         
                    #word_count_collocates.append(counter_object.get(word))

    window_freq = Counter(window_collocate)                
    collocate = [x for x in window_freq.keys()] #extracting collocates from dictionary to a list
    O11 = [x for x in window_freq.values()] # Taking 'values' from the counter object means we take the frequencies of each word without the 'key' i-e the word

    O12 = [x1 - x2 for (x1, x2) in zip(([keyword_n] * len(O11)), O11)] # Taking the times the keyword occurs * by the length of O11 value and subtracts O11 from total keyword n
    R1 = [x1 + x2 for (x1, x2) in zip(O11, O12)] # Calculating R1 and C1
    
    C1 = []
    for w in collocate:
        C1.append(counter_object.get(w))
            
    N = len(text) # length of text
       
    E11 = [x1 * x2 for (x1, x2) in zip(R1, C1)]  # Expected
    E11 = [x1 / x2 for (x1, x2) in zip(E11, ([N]*len(E11)))]
        
    MI = [np.log2(x1/x2) for (x1, x2) in zip(O11, E11)]

    df = pd.DataFrame()
    df["collocate"] = collocate
    df["raw_frequency"] = C1
    df["MI"] = MI
    return df 

def main():
    data_path = os.path.join("..","data")
    text_concat = file_load(data_path)
    text = tokenize(text_concat)
    MI_df = collocate_calc(text, "child")
    outpath = os.path.join("collocations_info.csv")
    MI_df.to_csv(outpath)

# Define behaviour when called from command line
if __name__=="__main__":
    main()
    
    

