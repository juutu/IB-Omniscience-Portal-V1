import os
import json

GRADE_DB = "ib_grade_matrix_vault.json"

def load_ib_data_from_file():
    """Loads current grades from the local JSON file matrix repository."""
    if not os.path.exists(GRADE_DB):
        return {}
    try:
        with open(GRADE_DB, 'r', encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_ib_data_to_file(data):
    """Saves grade adjustments permanently to disk storage layouts."""
    try:
        with open(GRADE_DB, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Failed to write to Grade Vault matrix file: {e}")

def add_subject(ib_profile, subject_name, level="HL"):
    """Adds a course structure track profile to your tracker profile framework."""
    sub_title = subject_name.title().strip()
    if sub_title not in ib_profile:
        ib_profile[sub_title] = {
            "level": level,
            "current_score": 0.0,
            "assessments": {}
        }
        save_ib_data_to_file(ib_profile)

def update_subject_score(ib_profile, subject_name, numeric_score):
    """Updates the overarching baseline target score metric for a specific track subject."""
    sub_title = subject_name.title().strip()
    if sub_title in ib_profile:
        ib_profile[sub_title]["current_score"] = numeric_score
        save_ib_data_to_file(ib_profile)
        return f"Updated baseline target score to {numeric_score}"
    return "Subject tracking target missing."

def calculate_ib_points(ib_data):
    """Calculates total point indicators out of 45."""
    total_points = 0
    for sub, content in ib_data.items():
        score = content.get("current_score", 0)
        # Safely convert to a standard 1-7 score boundary integer
        if score > 0:
            total_points += int(min(max(score, 1), 7))
    return total_points

def grade_tracker_menu(ib_data):
    ib_data = {}
    """Overarching UI routing matrix layout entry interface."""
    while True:
        # 1. Pull latest changes from file tracking metrics to sync states
        try:
            fresh_data = load_ib_data_from_file()
            ib_data.clear()
            ib_data.update(fresh_data)
        except Exception as e:
            # Fallback if the file tracker isn't built yet, keeps the menu live
            pass

        # 2. Clear Screen and Render UI
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=====================================================")
        print("📊  ENGINE 2: OFFICIAL IB DIPLOMA GRADE TRACKER      ")
        print("=====================================================")
        print("[1] View Current Subject Grades & Boundaries")
        print("[2] Add New Assessment Marks (IA, EE, TOK, Exams)")
        print("[3] Edit/Update Existing Assessment Marks")
        print("[4] Remove Assessment Records")
        print("[5] Configure Subject Details (Class, Level)")
        print("[6] Calculate Total Projected Points (Target /45)")
        print("[0] Return to Main Hub Menu")
        print("=====================================================")
        
        choice = input("Select tracking operation: ").strip()
        
        # --------------------------------------------------------
        # [1] VIEW SUBJECT GRADES
        # --------------------------------------------------------
        if choice == '1':
            print("\n📋 CURRENT TRACKED GRADE MATRIX SCHEMA:")
            if not ib_data:
                print("No active subjects configured yet. Awaiting automated cloud sync stream feeds.")
            else:
                for sub, metrics in ib_data.items():
                    level = metrics.get('level', 'SL/HL Unset')
                    score = metrics.get('current_score', 0)
                    print(f" 📘 {sub} ({level}): Baseline Score: {score}")
            input("\nPress Enter to continue...")
        
        # --------------------------------------------------------
        # [2] ADD ASSESSMENT MARKS
        # --------------------------------------------------------
        elif choice == '2':
            print("\n✍️ Enter Custom Assessment Addition Wizard:")
            sub = input("Enter subject name (e.g., Physics_HL): ").strip()
            
            if sub not in ib_data:
                print(f"❌ Subject '{sub}' not found. Please configure it using option [5] first.")
            else:
                score = input("Enter percentage score value: ").strip()
                try:
                    update_subject_score(ib_data, sub, float(score))
                    print(f"✨ Successfully added score of {score}% to {sub}.")
                except ValueError:
                    print("❌ Input Error: Please enter a valid numerical percentage.")
            input("\nPress Enter to continue...")
            
        # --------------------------------------------------------
        # [3] EDIT/UPDATE MARKS
        # --------------------------------------------------------
        elif choice == '3':
            print("\n✍️ Enter Custom Track Update Wizard:")
            sub = input("Enter subject name to update manually: ").strip()
            
            if sub not in ib_data:
                print(f"❌ Subject '{sub}' does not exist.")
            else:
                score = input("Enter new numerical achievement value: ").strip()
                try:
                    update_subject_score(ib_data, sub, float(score))
                    print(f"✨ Successfully updated metrics for {sub}.")
                except ValueError:
                    print("❌ Invalid entry: Data must be a number.")
            input("\nPress Enter to continue...")
        
        # --------------------------------------------------------
        # [4] REMOVE RECORDS
        # --------------------------------------------------------
        elif choice == '4':
            print("\n✍️ Enter Custom Track Removal Wizard:")
            subject = input("Enter subject name: ").strip()
            name = input("What is the exact name of the assessment to remove? ").strip()

            if subject in ib_data and "assessments" in ib_data[subject]:
                if name in ib_data[subject]["assessments"]:
                    ib_data[subject]["assessments"].pop(name)
                    print(f"✨ Successfully removed assessment '{name}'.")
                else:
                    print(f"❌ Assessment '{name}' not found under {subject}.")
            else:
                print(f"❌ Subject '{subject}' or its assessment sub-vault does not exist.")
            input("\nPress Enter to continue...")
        
        # --------------------------------------------------------
        # [5] CONFIGURE SUBJECT
        # --------------------------------------------------------
        elif choice == '5':
            print("\n✍️ Enter Custom Subject Configuration Wizard:")
            subject = input("Enter subject name (e.g., Physics_HL): ").strip()
            level = input("Enter subject level (HL/SL): ").upper().strip()
            
            if not subject:
                print("❌ Subject name cannot be blank.")
            elif level not in ['HL', 'SL']:
                print("❌ Invalid level. Please enter exactly 'HL' or 'SL'.")
            else:
                add_subject(ib_data, subject, level)
                print(f"✨ Successfully added/configured {subject} as {level}.")
            input("\nPress Enter to continue...")

        # --------------------------------------------------------
        # [6] CALCULATE POINTS
        # --------------------------------------------------------
        elif choice == '6':
            try:
                points = calculate_ib_points(ib_data)
                print(f"\n🏆 Your current projected total: {points}/45 points.")
            except Exception as e:
                print(f"❌ Error calculating points: {e}")
            input("\nPress Enter to continue...")

        # --------------------------------------------------------
        # [0] EXIT MENU
        # --------------------------------------------------------
        elif choice == '0':
            print("Returning to main workspace...")
            break
            
        else:
            print("❌ Invalid menu option. Please select 0-6.")
            input("\nPress Enter to continue...")
