#the code translates a given input sentence from any language to English using Google Translate API. 
# Then, it tokenizes the translated sentence, performs part-of-speech tagging, 
# and identifies named entities in the translated text. The results of each step are printed to the console.

import nltk
from googletrans import Translator
from requests.exceptions import RequestException
from pprint import pprint

# Download NLTK resources (if not already downloaded)
# nltk.download('punkt')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# Initialize the translator
translator = Translator()
user_sentence = input("Type a sentce in any language: ")

def translate_with_retry(sentence, target_language, retries=3):
    try:
        translated_text = translator.translate(sentence, dest=target_language).text
        return translated_text
    except RequestException as e:
        print(f"Translation failed due to a network error: {e}")
        if retries > 0:
            print(f"Retrying... ({retries} attempts left)")
            return translate_with_retry(sentence, target_language, retries - 1)
        else:
            print("Max retries reached. Unable to translate the sentence.")
            return None

def process_and_display_results(translated_sentence):
    # Tokenize the translated sentence
    tokenized_sentence = nltk.word_tokenize(translated_sentence)

    # Part-of-speech tagging for the translated sentence
    pos_tags = nltk.pos_tag(tokenized_sentence)

    # Named Entity Recognition (NER) for the translated sentence
    named_entities = nltk.ne_chunk(pos_tags)

    # Display the results
    print("Translation:")
    print(translated_sentence)

    print("\nTokenization:")
    pprint(tokenized_sentence)

    print("\nPart-of-Speech Tags:")
    pprint(pos_tags)

    print("\nNamed Entity Recognition:")
    pprint(named_entities)

if __name__ == "__main__":
    # Example input sentence in the source language
    #source_sentence = "Je suis étudiant en informatique."
    source_sentence = user_sentence
    # Target language code (e.g., 'en' for English)
    target_language = 'en'

    # Translate the input sentence to the target language with retries
    translated_sentence = translate_with_retry(source_sentence, target_language)

    if translated_sentence:
        process_and_display_results(translated_sentence)
    else:
        print("Translation failed. Please check your network connection and try again.")
