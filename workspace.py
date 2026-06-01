import os
import note_processor
import assignment_planner
import ib_grade_tracker
import spanish_suite
import glob
import threading
import watchdog_daemon

try:
    daemon_thread = threading.Thread(target=watchdog_daemon.start_background_daemon, daemon=True)
    daemon_thread.start()

except Exception as e:
    print(f"⚠️ Error starting watchdog daemon: {e}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_automated_note_processor():
    clear_screen()
    print("--- AUTOMATED AI NOTE PROCESSOR PORTAL ---")

    INPUT_DIR = "raw_notes"
    OUTPUT_DIR = "processed_notes"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(INPUT_DIR, exist_ok=True)

    detected_files = glob.glob(os.path.join(INPUT_DIR, "*.txt"))

    if not detected_files:
        print(f"\n ⚠️ No raw text documents detected inside '{INPUT_DIR}'.")
        print("Please drop a (.txt) file into that folder to run the auto-pipeline.")
        input("\nPress Enter to return to the Main Menu Hub.")
        return

    print(f"\nFound {len(detected_files)} file(s) waiting for generation:")
    for idx, file_path in enumerate(detected_files, start=1):
        print(f"{idx}. {os.path.basename(file_path)}")

    print("\n---------------------------------------")
    confirm = input("Execute unified AI build pipeline on these files? (y/n): ").strip().lower()

    if confirm != 'y':
        print("Pipeline execution cancelled.")
        input("\nPress Enter to return to the Main Menu Hub.")
        return
    
    target_subject = input("Enter The Subject Name for this batch (e.g., Physics, Mathematics, Math): ").strip()

    if not target_subject:
        target_subject = "General"
    
    try:
        problem_count_input = input("Enter the number of problems to generate: ").strip()
        if problem_count_input:
            num_problems = int(problem_count_input)
            if num_problems <= 0:
                print("Number must be greater than 0. Defaulting to 3.")
                num_problems = 3
        else:
            print("No value has been provided. Defaulting to 3.")
            num_problems = 3
            
    except ValueError:
        print("The provided value is not a valid integer. Defaulting to 3.")
        num_problems = 3


    for file_path in detected_files:
        base_name = os.path.basename(file_path)
        output_filename = f"{os.path.splitext(base_name)[0]}_study_guide.md"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        print(f"\nParsing data payload from: {base_name}...")
        
        with open(output_path, 'w', encoding='utf-8') as output_file:
            generated_guide = note_processor.process_academic_note(file_path, target_subject)
            output_file.write(generated_guide)
        
        print(f"✨ Study Guide successfully built and written to: {output_path}")

        try:
            os.remove(file_path)
            print(f"Raw text document '{base_name}' has been removed from queue.")
        except Exception as e:
            print(f"Error removing raw text document: {e}")
    
    print("\n=============================================")
    print("🎉 All detected batches successfully compiled!")
    input("Press Enter to return to Main Hub Menu...")


# ✅ RESTORED: This is the main orchestration loop engine
def main():
    # Load persistence contexts on initialization
    ib_data = ib_grade_tracker.load_ib_data_from_file()
    tasks = assignment_planner.load_assignments_from_file()

    if "core_bonus" not in ib_data:
        ib_data["core_bonus"] = {"tok": None, "ee": None, "points": 0}

    while True:
        clear_screen()
        print("\n" + "="*45)
        print("⚡ CENTRAL IB STUDENT WORKSPACE HUB ⚡")
        print("="*45)
        print("[1] AI Note Processor & Study Guide Engine (Auto-Detect)")
        print("[2] IB Grade Tracker Dashboard (20/40/40 Split)")
        print("[3] Assignment Planner & Toddle Sync")
        print("-" * 45)
        print("[4] Spanish Suite")
        print( "[5] Interactive AI Problem Grader (Submit an Answer) ")
        print("[0] Shutdown Workspace")
        print("-" * 45)
       
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            handle_automated_note_processor()

        elif choice == '2':
            ib_grade_tracker.grade_tracker_menu(ib_data)

        elif choice == '3':
            assignment_planner.assignment_planner_menu(tasks)
        
        elif choice == '4':
            spanish_suite.spanish_suite_menu()
        
        elif choice == '5':
            clear_screen()
            print("🧠 --- INTERACTIVE AI PROBLEM GRADER PORTAL ---")
            print("Copy/paste a problem from your study guide and test your answer.")
            print("---------------------------------------------------------------\n")
            
            subject = input("Enter the Subject Name (e.g., Physics, Econ, Spanish): ").strip()
            if not subject:
                subject = "General"
                
            print("\n📋 Step 1: Paste the original question or practice problem below:")
            print("(Press Enter twice or leave a blank line when you are finished pasting)")
            
            # Allows multi-line copying and pasting of long text problems
            question_lines = []
            while True:
                line = input()
                if line == "":
                    break
                question_lines.append(line)
            question_text = "\n".join(question_lines)
            
            if not question_text.strip():
                print("❌ Question cannot be empty. Returning to menu.")
                input("\nPress Enter to return...")
                continue

            print("\n✍️  Step 2: Type or paste YOUR answer here:")
            print("(Press Enter twice or leave a blank line when you are finished pasting)")
            
            answer_lines = []
            while True:
                line = input()
                if line == "":
                    break
                answer_lines.append(line)
            user_answer = "\n".join(answer_lines)

            print("\n🤖 Commencing assessment analysis... Checking your work against IB matrix...")
            
            # Send data to your note_processor engine function
            grading_feedback = note_processor.evaluate_user_response(question_text, user_answer, subject)
            
            clear_screen()
            print("===============================================================")
            print("📝 OFFICIAL TUTOR EVALUATION REPORT")
            print("===============================================================\n")
            print(grading_feedback)
            print("\n===============================================================")
            
            # Optional: Ask if they want to save their evaluation report
            save_report = input("\nWould you like to save this grading report as a markdown file? (y/n): ").strip().lower()
            if save_report == 'y':
                os.makedirs("grading_reports", exist_ok=True)
                filename = f"grading_reports/{subject.lower()}_report.md"
                with open(filename, "w", encoding="utf-8") as rf:
                    rf.write(grading_feedback)
                print(f"💾 Report saved successfully to '{filename}'!")
                
            input("\nPress Enter to return to Main Hub Menu...")
        


        elif choice == '0':
            print("\nGoodbye! Have a nice day. Sleep well, DP Student! 😴")
            break  # ✅ This break statement works perfectly now because it sits inside a while loop

        else:
            print("\n❌ Invalid choice. Please select an option from the system menu matrix.")
            input("Press Enter to refresh...")

if __name__ == "__main__":
    main()