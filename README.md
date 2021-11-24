
# Direct Assessment Evaluation.

A python program to parse a csv containing a Direct Assessment of machine translation. The program contains a class Parse which can read in the scores contained in the csv file, calculate the mean average, calculate the highest and lowest scores and output information to a json file.

## Usage

`python solution.py <file_path>`

<file_path> is path to csv file containing Direct Assessment results.

This program was written using Python 3.9.6 and no external pip packages.


## Input

This program can take input of a csv file with the following columns. So far the program only uses the columns "Sentence Pair ID", "Evaluator ID" and "q1 score". The q2 score was excluded as it provided no new information.

| Sentence Pair ID | Sentence Pair Type | Evaluator ID | q1 score | q2 score | target language | human translation | machine translation | original |
|------------------|--------------------|--------------|----------|----------|----------------|-------------------|---------------------|----------|
|BG_SE_1|A|BBC_Bulgarian_01|0|0|BG|Защо американският флаг се развява?|Как се развява това американско знаме?|How did that US flag wave?|