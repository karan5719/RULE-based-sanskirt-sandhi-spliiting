import re
import pandas as pd

# Function to read words from a file and store them in a set for fast lookup
def read_words(file_path):
    try:
        with open(file_path) as reader:
            return {word for line in reader for word in line.split()[0].split("_")}
    except Exception as e:
        print(f"Error reading words from {file_path}: {e}")
        return set()

# Load sets for fast lookup
list_index = read_words('/Users/himanshukumar/Documents/sanskrit/Text.txt')
list_noun = read_words('/Users/himanshukumar/Documents/sanskrit/Noun.txt')
list_adverb = read_words('/Users/himanshukumar/Documents/sanskrit/Adverb.txt')
list_adjective = read_words('/Users/himanshukumar/Documents/sanskrit/Adjective.txt')

# Combine all word lists into a master set for efficient lookups
master_set = set.union(list_index, list_noun, list_adverb, list_adjective)

# Define the sandhi rules dictionary
sandhi_dict = {
    'ा': [['', 'अ'], ['', 'आ'], ['ा', 'अ'], ['ा', 'आ']],
    'ी': [['ि', 'इ'], ['ि', 'ई'], ['ी', 'इ'], ['ी', 'ई'], ['िः', '']],
    'ू': [['ु', 'उ'], ['ु', 'ऊ'], ['ू', 'उ'], ['ू', 'ऊ'], ['ुः', '']],
    'ृ': [['ृ', 'ऋ']],
    'े': [['', 'इ'], ['', 'ई'], ['ा', 'इ'], ['ा', 'ई']],
    'ो': [['', 'उ'], ['', 'ऊ'], ['ा', 'उ'], ['ा', 'ऊ'], ['ः', '']],
    'र्': [['', 'ऋ'], ['ा', 'ऋ']],
    'ै': [['', 'ए'], ['', 'ऐ'], ['ा', 'ए'], ['ा', 'ऐ']],
    'ौ': [['', 'ओ'], ['', 'औ'], ['ा', 'ओ'], ['ा', 'औ']],
    'य': [['ि', 'अ'], ['ी', 'अ'], ['े', 'अ'], ['े', 'इ'], ['े', 'उ']],
    # Add more rules here...
}

# Function to process each line of the input file
def process_line(line):
    m = line.strip().split(",")
    if len(m) < 4:
        return None
    text_input, f, s, flag = m[0], m[1], m[2], int(m[3])
    return text_input, f, s, flag

# Function to apply sandhi rules and find valid combinations
def apply_sandhi_rules(text_input, sandhi_dict, master_set):
    final_answers = []
    for char in sandhi_dict.keys():
        temp = re.split(char, text_input)
        if len(temp) > 1:
            temp_list = sandhi_dict[char]
            for x in temp_list:
                for d in range(len(temp) - 1):
                    t_f = "".join(temp[:d + 1]) + char
                    t_s = "".join(temp[d + 1:])
                    first = re.sub(char, '', t_f) + x[0]
                    second = x[1] + t_s
                    
                    if first in master_set and second in master_set:
                        final_answers.append((first, second))
    return final_answers

# Main function
def main():
    count = 0
    total = 0
    output_file = '/Users/himanshukumar/Documents/sanskrit/output_results.csv'

    try:
        df = pd.read_csv('/Users/himanshukumar/Documents/sanskrit/text_input.txt', header=None)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    print("Processing inputs...\n")
    results = []

    for _, row in df.iterrows():
        result = process_line(",".join(map(str, row)))
        if result:
            text_input, f, s, flag = result
            final_answers = apply_sandhi_rules(text_input, sandhi_dict, master_set)
            total += 1
            
            correct = False
            for ans in final_answers:
                if f == ans[0] and s == ans[1]:
                    count += 1
                    correct = True
                    break
            
            # Save results for this input
            results.append({
                "Input": text_input,
                "Expected First": f,
                "Expected Second": s,
                "Found": str(final_answers),
                "Correct": correct
            })

    # Calculate accuracy
    accuracy = (count / total * 100) if total > 0 else 0
    print(f"\nTotal Accuracy: {accuracy:.2f}%")
    
    # Save results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

# Run the main function
if __name__ == "__main__":
    main()



