import numpy as np

def read_training_data(file_name):
    """Reads the data from a file and returns it as a list of records."""
    records = []
    with open(file_name, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                try:
                    records.append(list(map(int, stripped_line.split())))
                except ValueError:
                    print(f"Skipping invalid line: {line}")
    return records

def calculate_probabilities(data):
    """Computes the marginal and conditional probabilities."""
    data_array = np.array(data)
    total_records = len(data)

    # Initialize probability dictionaries
    baseball_probability = {}
    cat_food_probability = {}
    tv_given_baseball = {}
    cat_feed_given_tv_and_food = {}

    # Baseball (B) and Cat Food (C) marginal probabilities
    baseball_probability[0] = np.sum(data_array[:, 0] == 0) / total_records
    baseball_probability[1] = np.sum(data_array[:, 0] == 1) / total_records

    cat_food_probability[0] = np.sum(data_array[:, 2] == 0) / total_records
    cat_food_probability[1] = np.sum(data_array[:, 2] == 1) / total_records

    # Conditional probability of TV (G) given Baseball (B)
    for b in [0, 1]:
        tv_prob = {}
        count_baseball = np.sum(data_array[:, 0] == b)
        for g in [0, 1]:
            count_comb = np.sum((data_array[:, 0] == b) & (data_array[:, 1] == g))
            tv_prob[g] = count_comb / count_baseball if count_baseball > 0 else 0.0
        tv_given_baseball[b] = tv_prob

    # Conditional probability of Feeding Cat (F) given TV (G) and Cat Food (C)
    for g in [0, 1]:
        for c in [0, 1]:
            feed_cat_prob = {}
            count_combo = np.sum((data_array[:, 1] == g) & (data_array[:, 2] == c))
            for f in [0, 1]:
                count_feed = np.sum((data_array[:, 1] == g) & (data_array[:, 2] == c) & (data_array[:, 3] == f))
                feed_cat_prob[f] = count_feed / count_combo if count_combo > 0 else 0.0
            cat_feed_given_tv_and_food[(g, c)] = feed_cat_prob

    return baseball_probability, cat_food_probability, tv_given_baseball, cat_feed_given_tv_and_food

def infer_probability(query, evidence, baseball_probability, cat_food_probability, tv_given_baseball, cat_feed_given_tv_and_food):
    """Performs inference using enumeration."""
    if not query:
        return None

    variables = ["B", "G", "C", "F"]
    all_combinations = get_all_combinations()

    query_values = parse_conditions(query)
    evidence_values = parse_conditions(evidence)

    if not query_values:  # If the query contains invalid conditions, skip the computation
        return None

    total_prob = 0.0
    matching_prob = 0.0

    for combo in all_combinations:
        b, g, c, f = combo

        # Joint probability for the current combination of variables
        joint_prob = (
            baseball_probability[b]
            * cat_food_probability[c]
            * tv_given_baseball[b][g]
            * cat_feed_given_tv_and_food[(g, c)][f]
        )

        # Check if the combination matches the evidence
        if does_match_evidence(evidence_values, variables, combo):
            total_prob += joint_prob
            if does_match_evidence(query_values, variables, combo):
                matching_prob += joint_prob

    return matching_prob / total_prob if total_prob > 0 else 0.0

def does_match_evidence(evidence_values, variables, combination):
    """Checks if a given combination matches the evidence."""
    for var, val in evidence_values.items():
        idx = variables.index(var.upper())  # Ensure case insensitivity by converting to uppercase
        if combination[idx] != val:
            return False
    return True

def get_all_combinations():
    """Generates all possible combinations of variables."""
    return [
        [b, g, c, f]
        for b in [0, 1]
        for g in [0, 1]
        for c in [0, 1]
        for f in [0, 1]
    ]

def parse_conditions(conditions):
    """Parses the conditions for query and evidence."""
    if not conditions:
        return {}

    parsed_conditions = {}
    for cond in conditions:
        var = cond[0].upper()  # Convert the variable to uppercase for consistency
        if var not in ['B', 'G', 'C', 'F']:
            print(f"Invalid variable '{var}' in the condition.")
            return {}  # Return empty dict to indicate invalid input
        parsed_conditions[var] = 1 if cond.endswith("t") else 0
    return parsed_conditions


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python ProbabilisticNetwork.py <data_file>")
        sys.exit(1)

    data_file = sys.argv[1]

    # Load the training data
    training_data = read_training_data(data_file)

    # Compute the probabilities
    baseball_probability, cat_food_probability, tv_given_baseball, cat_feed_given_tv_and_food = calculate_probabilities(training_data)

    # Interactive query loop
    while True:
        query_input = input("Enter query (or type 'none' to exit): ").strip()

        if query_input.lower() == "none":
            print("Exiting the program...")
            break

        # Split the input into query and evidence parts
        query_parts = query_input.split(" given ")
        query_vars = query_parts[0].split() if query_parts[0] else []
        evidence_vars = query_parts[1].split() if len(query_parts) > 1 else []

        # Check if the input is valid (i.e., contains exactly two conditions in the correct format)
        if len(query_vars) != 2 or not all(len(var) == 2 for var in query_vars) or any(var not in ['Bt', 'Gf'] for var in query_vars):
            print("Invalid input format. Please enter in the format 'Bt Gf' or 'Bt Gf given Bt Gf'.")
            continue

        # If query_vars are present, compute the probability
        result = infer_probability(query_vars, evidence_vars, baseball_probability, cat_food_probability, tv_given_baseball, cat_feed_given_tv_and_food)
        
        if result is None:
            print("Invalid input or unprocessable query. Please try again.")
        else:
            print(f"Computed Probability: {result:.6f}")


if __name__ == "__main__":
    main()
