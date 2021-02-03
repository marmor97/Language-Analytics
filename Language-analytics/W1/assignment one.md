## Assignment one 
### Language Analytics
February 2021

_Marie Damsgaard Mortensen_

__Basic scripting with Python__

Using the corpus called 100-english-novels found on the cds-language GitHub repo, write a Python programme which does the following:

- Calculate the total word count for each novel
- Calculate the total number of unique words for each novel
- Save result as a single file consisting of three columns: filename, total_words, unique_words

__General instructions__

- For this exercise, you can upload either a standalone script OR a Jupyter Notebook
- Save your script as word_counts.py OR word_counts.ipynb
- You can either upload the script/notebook here or push to GitHub and include a link - or both!
- Your code should be clearly documented in a way that allows others to easily follow the structure of your script.
- Similarly, remember to use descriptive variable names! A name like word_count is more readable than wcnt.

__Purpose__

This assignment is designed to test that you have a understanding of:

1. how to structure, document, and share a Python script;
2. how to effectively make use of native Python data structures, functions, and flow control;
3. how to load, save, and process text files.

### Loading files

importing modules and using os to specify the path.


```python
import os
import pandas as pd
from pathlib import Path
```


```python
data_path = os.path.join("..", "cds-language", "data", "100_english_novels", "corpus")
```


```python
# checking my path if it looks correct
data_path
```




    '../cds-language/data/100_english_novels/corpus'




```python
# defining list to save information there
file_name = []
total_words = []
unique_words = []
```

Below, I have made a loop that reads every file and saves filename, total number of words in every file and amount of unique words.

The first word _for_ instantiates a loop that performs several actions on each of the filenames found in the path. 

_Path_ from _pathlib_ creates a concrete path with all text files in data_path. 

Afterwards, the specific text file is saved in a variable with file.read(). This variable is then split up at every point of a whitespace meaning that words are seperated and are now each a variable in a list called split_text. 

The length of split_text is appended to the list mentioned in the chunk above and is saved here. The same goes for the filename in question. 

To save the amount of unique words in every novel, the splitted text is made into the _set_ data type where there are no duplicates. By taking the length of this list unique words are counted and appended to the unique_words list.


```python
for filename in Path(data_path).glob("*.txt"):
    with open(filename, "r", encoding = "utf-8") as file:
        loaded_text = file.read()
        
        #splitting text whenever there is a whitespace 
        split_text = loaded_text.split()
        total_words.append(len(split_text))
        
        #filename
        file_name.append(filename.name)
        
        #unique words
        unique_words.append(len(set(split_text)))
```

Now, it is time to make the three lists file_name, total_words and unique_words into one dataframe. Using pandas DataFrame function, each of the lists are made into columns.


```python
#collecting lists to make a dataframe
novel_info = pd.DataFrame({'filename': file_name, 'total_words': total_words, 'unique_words': unique_words})
```


```python
#inspecting the dataframe
novel_info
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>filename</th>
      <th>total_words</th>
      <th>unique_words</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Cbronte_Villette_1853.txt</td>
      <td>196557</td>
      <td>29084</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Forster_Angels_1905.txt</td>
      <td>50477</td>
      <td>9464</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Woolf_Lighthouse_1927.txt</td>
      <td>70185</td>
      <td>11157</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Meredith_Richmond_1871.txt</td>
      <td>214985</td>
      <td>28892</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Stevenson_Treasure_1883.txt</td>
      <td>68448</td>
      <td>10831</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>95</th>
      <td>Chesterton_Thursday_1908.txt</td>
      <td>58299</td>
      <td>10385</td>
    </tr>
    <tr>
      <th>96</th>
      <td>Burnett_Lord_1886.txt</td>
      <td>58698</td>
      <td>8131</td>
    </tr>
    <tr>
      <th>97</th>
      <td>Braddon_Phantom_1883.txt</td>
      <td>180676</td>
      <td>22474</td>
    </tr>
    <tr>
      <th>98</th>
      <td>Gaskell_Ruth_1855.txt</td>
      <td>161797</td>
      <td>18148</td>
    </tr>
    <tr>
      <th>99</th>
      <td>Kipling_Captains_1896.txt</td>
      <td>53467</td>
      <td>11709</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 3 columns</p>
</div>



Lastly, I'm making a new output folder where the file is saved as .csv. The path is made in the same way as the data-path in the beginning. The function to_csv() saves the file novel_info with the path specified.


```python
# making a directory to keep track of output files
os.mkdir("output")
```


```python
outpath = os.path.join("output", "novel_info.csv")
```


```python
novel_info.to_csv(outpath)
```
