## Student Information ##
 
Name: Bathala Venkata Harshitha
UTA ID: 1002204412


**  Programming Language  **
This program is written in Python.
Python Version: 3.8.x or higher


**  Code Structure  **

The program consists of the following components:

read_training_data(file_name):
    This function reads training data from the specified file and returns it as a list of records. It expects the file to have space-separated integers.

calculate_probabilities(data):
    Computes the marginal and conditional probabilities from the training data. It calculates:

        - Marginal probabilities for Baseball and Cat Food
        - Conditional probabilities for TV given Baseball
        - Conditional probabilities for Feeding Cat given TV and Cat Food
infer_probability(query, evidence, ...):
    This function performs inference using enumeration to compute the probability of a query given evidence. It handles parsing the query and evidence, generating all combinations of variables, and calculating joint probabilities.
    does_match_evidence(evidence_values, ...):
    Checks if a given combination of variables matches the evidence conditions.

get_all_combinations():
    Generates all possible combinations of the variables (Baseball, TV, Cat Food, and Feeding Cat).

parse_conditions(conditions):
     Parses the query or evidence conditions, ensuring valid format and converting them to a dictionary.

main():
    The main entry point for the program, which loads training data, computes probabilities, and continuously allows for user interaction to input queries and evidence, calculating and displaying the results.


**  How to Run the Code  **

1. Open a terminal or command prompt.
2. Navigate to the directory containing bnet.py.
3. Run the script with the training data file as an argument:
      -> python bnet.py training_data.txt

Exampe Queries:

Enter query (or type 'none' to exit): Gf Bt                                                                                                       
Computed Probability: 0.021918
Enter query (or type 'none' to exit): Bt Gf 
Computed Probability: 0.021918
Enter query (or type 'none' to exit): Bt Gf given Ff                                                                                              
Computed Probability: 0.013529
Enter query (or type 'none' to exit): Gf Bt given Ff 
Computed Probability: 0.013529
Enter query (or type 'none' to exit): None
Exiting the program...


Notes:
If the user enters invalid input or the query format is incorrect, the program will provide an error message and prompt again.
For an empty input, the program will display Invalid input.

