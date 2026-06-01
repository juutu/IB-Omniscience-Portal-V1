import os
import json
import random

# Core IB Spanish B Curriculum Framework Themes
PRESCRIBED_THEMES = [
    "Identidades",
    "Experiencias",
    "Ingenio humano",
    "Organización social",
    "Compartimos el planeta"
]

VOCAB_DB = "spanish_vocab_vault.json"

# 1. BASE DATABASE UTILITIES (Must be defined first!)
# =====================================================================
def auto_initialize_database():
    """
    Auto-initializes a fresh JSON skeleton database schema 
    with the 5 core IB themes if the file doesn't exist.
    """
    if not os.path.exists(VOCAB_DB):
        skeleton = {theme: {} for theme in PRESCRIBED_THEMES}
        try:
            with open(VOCAB_DB, 'w', encoding="utf-8") as f:
                json.dump(skeleton, f, indent=4, ensure_ascii=False)
            print(f"📦 [Database Initializer]: Fresh schema generated successfully at '{VOCAB_DB}'.")
        except Exception as e:
            print(f"⚠️ Error initializing database: {e}")

def save_vocab(data):
    """Saves data back to the JSON vault file."""
    try:
        with open(VOCAB_DB, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Failed to save changes to database: {e}")

def load_vocab():
    """Loads current data from the JSON vault file."""
    auto_initialize_database()
    try:
        with open(VOCAB_DB, 'r', encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("⚠️ Could not read Vocabulary Vault. Returning empty schema.")
        return {theme: {} for theme in PRESCRIBED_THEMES}


# 2. CORE FEATURES (These safely call the utilities above)
# =====================================================================
def add_vocabulary_term():
    """Enforces strict verification boundaries against theme keys."""
    data = load_vocab()
    
    print("\n--- 📝 ADD NEW VOCABULARY TERM ---")
    print("Select an IB Spanish B Thematic Framework Category:")
    for idx, theme in enumerate(PRESCRIBED_THEMES, start=1):
        print(f"  [{idx}] {theme}")
        
    try:
        choice = int(input("\nSelect theme number: ").strip())
        if not (1 <= choice <= len(PRESCRIBED_THEMES)):
            print("❌ Verification Boundary Violation: Invalid category selection.")
            return
        selected_theme = PRESCRIBED_THEMES[choice - 1]
    except ValueError:
        print("❌ Verification Boundary Violation: Numeric input required.")
        return

    spanish_word = input("Enter the Spanish term/phrase: ").strip().lower()
    english_translation = input(f"Enter the English translation for '{spanish_word}': ").strip().lower()

    if not spanish_word or not english_translation:
        print("❌ Error: Blank values cannot be processed into the matrix.")
        return

    # Commit entry directly into the specific theme block
    data[selected_theme][spanish_word] = english_translation
    save_vocab(data)  # <--- Python can now see this perfectly!
    print(f"✨ Successfully committed '{spanish_word}' under the '{selected_theme}' framework.")

def run_translation_drill():
    data = load_vocab()

    drill_pool = []
    for theme, words in data.items():
        for spa, eng in words.items():
            drill_pool.append({"spanish": spa, "english": eng, "theme": theme})
    
    if not drill_pool:
        print("⚠️ No vocabulary terms found in the database. Please add some first!")
        input("\nPress Enter to return to the Main Menu Hub.")
        return
    
    random.shuffle(drill_pool)

    print("\n--- 🎯 SPANISH TO ENGLISH TRANSLATION DRILL ---")
    print("Think of the translation, and then flip the card")
    score = 0

    for idx, item in enumerate(drill_pool, start=1):
        print("\n" + "="*50)
        print(f"[Card {idx}]/{len(drill_pool)}] Theme: {item['theme']}")
        print(f"\nSPANISH: {item['spanish'].upper()}")
        print("\n" + "="*50)

        input("\nPress [ENTER] to flip the card and reveal the translation.")

        print("\nENGLISH: {item['english'].upper()}")
        print("\n" + "="*50)

        user_input = input("\nDid you remember the translation? (y/n): ").strip().lower()
        if user_input == 'y':
            score += 1
        
        else:
            print("\n❌ Incorrect translation. The correct answer was: {item['english'].upper()")
        
        quit_choice = input("\nPress [ENTER] for the next card, or type 'q' to quit").strip().lower()
        if quit_choice == 'q':
            break
    
    print(f"\n🏁 Drill complete! Performance metric: {score}/{idx} correct answers.")
    input("\nPress Enter to return to menu...")


# 3. INTERFACE ROUTER Menu
# =====================================================================
def spanish_suite_menu():
    """The central sub-menu interface called by workspace.py"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=====================================================")
        print("🇪🇸  LAB 6: THE LINGUISTIC SPANISH B SYNTHESIS SUITE  ")
        print("=====================================================")
        print("[1] Append New Theme-Verified Vocabulary Term")
        print("[2] Run Randomized Translation Flashcard Drill")
        print("[0] Exit Suite")
        print("=====================================================")
        
        choice = input("Select operation: ").strip()
        if choice == '1':
            add_vocabulary_term()
        elif choice == '2':
            run_translation_drill()
        elif choice == '0':
            break

            
        

            

    

    










