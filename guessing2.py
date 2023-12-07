from nltk.corpus import wordnet
import random
import time

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def get_hypernyms(word):
    hypernyms = []
    for syn in wordnet.synsets(word):
        for hypernym in syn.hypernyms():
            hypernyms.extend(hypernym.lemma_names())
    return hypernyms

def choose_word(word_category):
    word_list = wordnet.words()
    filtered_words = [word for word in word_list if wordnet.synsets(word) and wordnet.synsets(word)[0].pos() == 'n']
    if word_category:
        filtered_words = [word for word in filtered_words if wordnet.synsets(word)[0].lexname() == word_category]
    word = random.choice(filtered_words)
    return word

def provide_synonym_hint(word):
    synonyms = get_synonyms(word)
    if synonyms:
        return f"Hint: A synonym of the word is '{random.choice(synonyms)}'."
    else:
        return "Hint: No synonyms available."
def main():
    print("Welcome to the WordNet Word Game!")
    word_category = input("Press Enter for a random category: ").strip().lower()
    time_limit = 10  # Set the time limit for each round in seconds
    score = 0

    while True:
        word = choose_word(word_category)
        synonyms = get_synonyms(word)
        hypernyms = get_hypernyms(word)
        
        options = synonyms + hypernyms
        random.shuffle(options)
        
        print("\nOptions:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        start_time = time.time()
        try:
            guess = int(input("Enter your guess number: ")) - 1
            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time > time_limit:
                print("Time's up! You lose this round.")
            elif options[guess] in hypernyms:
                print("Correct! It's a hypernym.")
                word_length = len(options[guess])
                score += word_length
                
            elif options[guess] in synonyms:
                print("Incorrect guess.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

        print("Your current score:", score)

        play_again = input("Play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print("Thanks for playing! Your final score is:", score)
            break

if __name__ == "__main__":
    main()