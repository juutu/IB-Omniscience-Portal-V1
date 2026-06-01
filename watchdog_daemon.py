import time
import os
import csv
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# AUTOMATION HANDSHAKE: Directly interact with pre-existing architecture modules
import assignment_planner 
import ib_grade_tracker

# DYNAMIC ABSOLUTE TRACKING PATHWAYS
HOME_DIRECTORY_PATH = os.path.expanduser("~")
WATCH_DIRECTORY = os.path.join(HOME_DIRECTORY_PATH, "Library/Mobile Documents/com~apple~CloudDocs/IB_School_Notes")
SYLLABUS_DB = "toddle_syllabus.json"

class AcademicPipelineHandler(FileSystemEventHandler):
    """Monitors system drive files and streams Toddle metrics into planners, trackers, and syllabus databases."""
    
    def on_modified(self, event):
        if event.is_directory:
            return
            
        absolute_path = event.src_path
        filename = os.path.basename(absolute_path)
        
        # Filter out OS temporary locks/metadata tags completely
        if filename.startswith("~$") or filename.startswith("."):
            return
            
        # Verify valid academic file tracking targets
        if filename.endswith(".txt") or filename.endswith(".pdf") or filename.endswith(".csv"):
            print(f"\n⚡ [AUTOMATION DETECTED] Intercepted academic resource: '{filename}'")
            
            # STABILIZATION LOOP: Halt processing until file writes complete fully on disk (Cloud Sync Protection)
            prior_size = -1
            while True:
                if not os.path.exists(absolute_path):
                    return
                try:
                    current_size = os.path.getsize(absolute_path)
                except os.error:
                    # Catch brief file locks during operating system write procedures
                    time.sleep(0.5)
                    continue
                    
                if current_size == prior_size and current_size > 0:
                    break
                prior_size = current_size
                time.sleep(0.6)
            
            # TODDLE INTEGRATION ROUTING INTERFACES
            if "toddle" in filename.lower() and filename.endswith(".csv"):
                try:
                    with open(absolute_path, mode='r', encoding='utf-8-sig') as csv_file:
                        # Use a list to read rows so we can safely read multiple pathways if needed
                        content_list = list(csv.DictReader(csv_file))
                        if not content_list:
                            return
                        
                        # Gather lowercase field names from the first dict item
                        headers = [h.lower() for h in content_list[0].keys()] if content_list else []
                        
                        # --- PATHWAY A: TOPICS, UNITS, AND LESSON SCHEMAS ---
                        if any(k in headers for k in ["topic", "unit", "lesson", "objective"]):
                            print(f"🧠 [SYLLABUS INGESTION ENGAGED] Extracting curriculum tracking profiles...")
                            
                            syllabus_data = {}
                            if os.path.exists(SYLLABUS_DB):
                                try:
                                    with open(SYLLABUS_DB, 'r', encoding='utf-8') as f:
                                        syllabus_data = json.load(f)
                                except json.JSONDecodeError:
                                    syllabus_data = {}

                            for row in content_list:
                                subject = (row.get("Subject") or row.get("Class") or "General").strip().title()
                                unit = (row.get("Unit") or row.get("Unit Title") or "Core Unit").strip()
                                topic = (row.get("Topic") or row.get("Lesson Topic") or "").strip()
                                objective = (row.get("Objective") or row.get("Lesson Objective") or row.get("Description") or "").strip()
                                
                                if subject not in syllabus_data:
                                    syllabus_data[subject] = {"Units": {}}
                                if unit not in syllabus_data[subject]["Units"]:
                                    syllabus_data[subject]["Units"][unit] = {"Topics": [], "Lesson_Objectives": []}
                                    
                                if topic and topic not in syllabus_data[subject]["Units"][unit]["Topics"]:
                                    syllabus_data[subject]["Units"][unit]["Topics"].append(topic)
                                if objective and objective not in syllabus_data[subject]["Units"][unit]["Lesson_Objectives"]:
                                    syllabus_data[subject]["Units"][unit]["Lesson_Objectives"].append(objective)
                            
                            with open(SYLLABUS_DB, 'w', encoding='utf-8') as f:
                                json.dump(syllabus_data, f, indent=4, ensure_ascii=False)
                            print(f"📁 [SYLLABUS SYNC] Secondary reference database '{SYLLABUS_DB}' updated instantly.")
                        
                        # --- PATHWAY B: PERFORMANCE GRADES ---
                        elif any(k in headers for k in ["score", "percentage", "grade"]):
                            print(f"📊 [GRADE INGESTION ENGAGED] Processing Toddle Grade Matrix...")
                            ib_profile = ib_grade_tracker.load_ib_data_from_file()
                            
                            for row in content_list:
                                subject = row.get("Subject") or row.get("Class") or row.get("subject")
                                score_val = row.get("Score") or row.get("Percentage") or row.get("score")
                                level = row.get("Level") or row.get("level") or "HL"
                                
                                if subject and score_val:
                                    try:
                                        ib_grade_tracker.add_subject(ib_profile, subject, level)
                                        response = ib_grade_tracker.update_subject_score(ib_profile, subject, float(score_val))
                                        print(f"   -> Sync Score: {subject} -> {response}")
                                    except ValueError:
                                        continue
                                        
                        # --- PATHWAY C: DEADLINES AND ASSIGNMENTS ---
                        else:
                            print(f"📬 [PLANNER INGESTION ENGAGED] Processing Toddle Task Schedule Matrix...")
                            active_schedule_map = assignment_planner.load_assignments_from_file()
                            
                            for row in content_list:
                                task_name = row.get("Task Name") or row.get("Assignment") or row.get("title")
                                due_date = row.get("Due Date") or row.get("Deadline") or "2026-06-01"
                                if task_name:
                                    automated_task_title = f"Toddle Portal Task: {task_name.strip()}"
                                    automated_task_metadata = {"due_date": due_date.strip(), "status": "Not Started"}
                                    pipeline_callback_log = assignment_planner.add_assignment(
                                        active_schedule_map, automated_task_title, automated_task_metadata
                                    )
                                    print(f"   -> Sync Assignment: {pipeline_callback_log}")
                                    
                except Exception as e:
                    print(f"❌ [TODDLE AUTOMATION ERROR] Ingestion system crash: {e}")
            
            # --- STANDARD ACADEMIC DOCUMENT DETECTED ---
            else:
                try:
                    active_schedule_map = assignment_planner.load_assignments_from_file()
                    automated_task_title = f"Review Uploaded Notes: {filename}"
                    automated_task_metadata = {"due_date": "2026-06-01", "status": "Not Started"}
                    pipeline_callback_log = assignment_planner.add_assignment(
                        active_schedule_map, automated_task_title, automated_task_metadata
                    )
                    print(f"📬 [AUTOMATION PIPELINE SYNC] Database Response: {pipeline_callback_log}")
                except Exception as e:
                    print(f"❌ [AUTOMATION CRASH] Failed to synchronize files to planner: {e}")

def start_background_daemon():
    """Initializes tracking boundaries and locks the monitor onto your iCloud container path."""
    if not os.path.exists(WATCH_DIRECTORY):
        try:
            os.makedirs(WATCH_DIRECTORY)
            print(f"[DAEMON INITIALIZATION] Created sync path inside iCloud container: '{WATCH_DIRECTORY}'")
        except Exception as e:
            print(f"[DAEMON ABORTED] Critical failure creating directory structures: {e}")
            return
            
    event_handler = AcademicPipelineHandler()
    observer_engine = Observer()
    observer_engine.schedule(event_handler, path=WATCH_DIRECTORY, recursive=False)
    observer_engine.start()
    
    print(f"\n🚀 [DAEMON STATUS: ONLINE] Actively monitoring iCloud targets:")
    print(f"📁 PATH: '{WATCH_DIRECTORY}'")
    print("[DAEMON STATUS] Core syllabus tracking engine armed. Awaiting Toddle Matrix streams.")
    print("💡 Press Ctrl+C to terminate cleanly.")
    
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\n[DAEMON SHUTDOWN] Terminating observer loops safely...")
        observer_engine.stop()
    observer_engine.join()

if __name__ == "__main__":
    start_background_daemon()