import os
import json

PLANNER_DB = "assignment_planner_vault.json"

def load_assignments_from_file():
    """Loads tasks from the local JSON vault. Used by the watchdog daemon."""
    if not os.path.exists(PLANNER_DB):
        return []
    try:
        with open(PLANNER_DB, 'r', encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_assignments_to_file(tasks):
    """Saves current tasks back to the local JSON file storage."""
    try:
        with open(PLANNER_DB, 'w', encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Failed to save assignment vault updates: {e}")

def add_assignment(tasks, task_title, metadata_dict):
    """
    Automated interface used by the watchdog daemon to inject tasks.
    Prevents duplicates and instantly commits to disk.
    """
    # Prevent duplicate injections
    for t in tasks:
        if t.get("title") == task_title:
            return "Task already synced."
            
    new_task = {
        "subject": "Automated Sync",
        "title": task_title,
        "due_date": metadata_dict.get("due_date", "2026-06-01")
    }
    tasks.append(new_task)
    save_assignments_to_file(tasks)
    return "Successfully committed to database."

def view_active_tasks(tasks):
    """Prints out all currently tracked academic assignments."""
    print("\n📅 --- CURRENT ACTIVE ASSIGNMENTS ---")
    if not tasks:
        print("🎉 No pending assignments found! Your schedule is completely clear.")
        return
        
    print(f"{'Index':<6} | {'Subject':<12} | {'Assignment Name':<30} | {'Due Date':<12}")
    print("-" * 68)
    for idx, task in enumerate(tasks, start=1):
        subject = task.get("subject", "General")
        title = task.get("title", "Untitled Task")
        due = task.get("due_date", "N/A")
        print(f"[{idx}]   | {subject:<12} | {title:<30} | {due:<12}")

def add_custom_task(tasks):
    """Allows manual entry of new school assignments or deadlines from the menu."""
    print("\n➕ --- ADD NEW CUSTOM ASSIGNMENT ---")
    subject = input("Enter Subject (e.g., Math, Physics, English): ").strip()
    title = input("Enter Assignment Name/Description: ").strip()
    due_date = input("Enter Due Date (e.g., DD/MM/YYYY or 'Friday'): ").strip()
    
    if not title:
        print("❌ Task name cannot be blank. Aborting creation.")
        return
        
    new_task = {
        "subject": subject if subject else "General",
        "title": title,
        "due_date": due_date if due_date else "No Date Specified"
    }
    
    tasks.append(new_task)
    save_assignments_to_file(tasks)
    print(f"✨ Successfully added assignment: '{title}'")

def trigger_toddle_sync():
    """Manual sync simulation engine option inside the menu console."""
    print("\n🔄 --- CONNECTING TO TODDLE PLATFORM MATRIX ---")
    print("📡 Initializing secure sync handshake...")
    print("📥 Scanning local synchronization pipelines...")
    print("✨ Sync Complete! Check the background daemon terminal for automatic data updates.")

def assignment_planner_menu(tasks):
    """Main menu endpoint called by workspace.py"""
    # Always pull latest data from disk when opening the menu
    disk_tasks = load_assignments_from_file()
    if disk_tasks:
        tasks.clear()
        tasks.extend(disk_tasks)
        
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=====================================================")
        print("📅  ENGINE 3: IB ASSIGNMENT PLANNER & TODDLE SYNC    ")
        print("=====================================================")
        print("[1] View Active Assignments & Deadlines")
        print("[2] Append New Custom Homework / IA Milestone Task")
        print("[3] Run Automated Toddle Sync Pipeline 🔄")
        print("[0] Return to Main Hub Menu")
        print("=====================================================")
        
        choice = input("Select planner operation: ").strip()
        
        if choice == '1':
            view_active_tasks(tasks)
            input("\nPress Enter to continue...")
        elif choice == '2':
            add_custom_task(tasks)
            input("\nPress Enter to continue...")
        elif choice == '3':
            trigger_toddle_sync()
            input("\nPress Enter to continue...")
        elif choice == '0':
            print("Returning to main workspace...")
            break
        

        
    

               


            

