# Ex8: Let user type 2 words in English as input. Print out the output
# which is the shortest chain according to the following rules:
# - Each word in the chain has at least 3 letters
# - The 2 input words from user will be used as the first and the last words of the chain
# - 2 last letters of 1 word will be the same as 2 first letters of the next word in the chain
# - All the words are from the file wordsEn.txt
# - If there are multiple shortest chains, return any of them is sufficient

def read_file(file_name):
    """Read the content of a text file"""
    try:
        with open(file_name, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_filtered_valid_words(file_name):
    words = read_file(file_name).splitlines()
    filtered_min_3_letters_words = set(word for word in words if len(word) >= 3)
    return filtered_min_3_letters_words


def ensure_input_words_valid(word1, word2, word_list):
    if word1 not in word_list or word2 not in word_list:
        raise ValueError("Input words must exist in the word list.")
    if len(word1) < 3 or len(word2) < 3:
        raise ValueError("Input words must have at least 3 letters.")


def build_prefix_dicts(word_list):
    prefix_dict = {}

    for word in word_list:
        prefix = word[:2]

        if prefix not in prefix_dict:
            prefix_dict[prefix] = []
        prefix_dict[prefix].append(word)

    return prefix_dict


from collections import deque


def find_shortest_chain(word1, word2, prefix_dict):
    queue = deque([(word1, [word1])])
    visited: set = {word1}

    while queue:
        current_word, path = queue.popleft()
        current_suffix = current_word[-2:]

        if current_suffix in prefix_dict:
            for next_word in prefix_dict[current_suffix]:
                if next_word == word2 and len(path) >= 2:
                    return path + [word2]
                if next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, path + [next_word]))

    raise ValueError("No valid chain found.")


def main():
    word_list = get_filtered_valid_words('wordsEn.txt')
    while True:
        word1 = input("Enter the first word: ")
        word2 = input("Enter the second word: ")
        try:
            ensure_input_words_valid(word1, word2, word_list)
            prefix_dict = build_prefix_dicts(word_list)
            chain = find_shortest_chain(word1, word2, prefix_dict)
            print("Shortest chain of words:")
            print(chain)
            break  # Exit the loop if a valid chain is found
        except ValueError as e:
            print(e)
            print("Please try again.")

if __name__ == "__main__":
    main()