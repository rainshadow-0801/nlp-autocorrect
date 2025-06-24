import nltk
import re
import string
from nltk.stem import WordNetLemmatizer

# Download NLTK data (only needed once)
nltk.download('wordnet')
nltk.download('omw-1.4')

# Read local text file
file_name = r"D:\Python\final.txt"
with open(file_name, 'r', encoding="utf8") as f:
    text_data = f.read().lower()
    words = re.findall(r'\w+', text_data)

vocab = set(words)

def count_word_frequency(words):
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

word_count = count_word_frequency(words)

def calculate_probability(word_count):
    total_words = sum(word_count.values())
    return {word: count / total_words for word, count in word_count.items()}

probabilities = calculate_probability(word_count)
lemmatizer = WordNetLemmatizer()

def lemmatize_word(word):
    return lemmatizer.lemmatize(word)

def delete_letter(word):
    return [word[:i] + word[i+1:] for i in range(len(word))]

def swap_letters(word):
    return [word[:i] + word[i+1] + word[i] + word[i+2:] for i in range(len(word)-1)]

def replace_letter(word):
    letters = string.ascii_lowercase
    return [word[:i] + l + word[i+1:] for i in range(len(word)) for l in letters]

def insert_letter(word):
    letters = string.ascii_lowercase
    return [word[:i] + l + word[i:] for i in range(len(word)+1) for l in letters]

def generate_candidates(word):
    candidates = set()
    candidates.update(delete_letter(word))
    candidates.update(swap_letters(word))
    candidates.update(replace_letter(word))
    candidates.update(insert_letter(word))
    return candidates

def generate_candidates_level2(word):
    level1 = generate_candidates(word)
    level2 = set()
    for w in level1:
        level2.update(generate_candidates(w))
    return level2

def get_best_correction(word, probs, vocab, max_suggestions=3):
    candidates = (
        [word] if word in vocab else list(generate_candidates(word).intersection(vocab)) or 
        list(generate_candidates_level2(word).intersection(vocab))
    )
    return sorted([(w, probs.get(w, 0)) for w in candidates], key=lambda x: x[1], reverse=True)[:max_suggestions]

# --------- INPUT ----------
user_input = input("\nEnter a word for autocorrection: ")
suggestions = get_best_correction(user_input.lower(), probabilities, vocab, max_suggestions=3)

# --------- OUTPUT ----------
print("\nTop suggestions:")
for suggestion in suggestions:
    print(suggestion[0])
