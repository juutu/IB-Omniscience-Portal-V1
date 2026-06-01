import os
import json
from google import genai
from google.genai import types

# Initialize the authoritative Client (automatically reads your GEMINI_API_KEY env)
client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

SYLLABUS_DB = "toddle.syllabus.json"
FORMULA_DB = "formula_vault.json"

# LAYER 1: DATA PERSISTENCE (JSON File Storage)
# =====================================================================
def load_secondary_contexts(subject_name):
    syllabus_content = {}
    formula_content = {}
    
    # Title-case subject parsing logic to keep lookups clean
    sub_title = subject_name.title().strip()

    if os.path.exists(SYLLABUS_DB):
        try:
            with open(SYLLABUS_DB, 'r', encoding="utf-8") as f:
                all_syllabus = json.load(f)
            # FIXED: Removed trailing comma typo to keep it as a clean dictionary
            syllabus_content = all_syllabus.get(sub_title, {})
        except Exception:
            print("⚠️ Could not parse Toddle syllabus database.")
    
    if os.path.exists(FORMULA_DB):
        try:
            with open(FORMULA_DB, 'r', encoding="utf-8") as f:
                all_formulas = json.load(f)
            # FIXED: Removed trailing comma typo to keep it as a clean dictionary
            formula_content = all_formulas.get(sub_title, {})
        except Exception:
            print("⚠️ Could not parse Formula vault database.")

    return syllabus_content, formula_content

# LAYER 2: LAB FUNCTIONS (CORE LOGIC RULES)
# =====================================================================
def process_academic_note(note_path, subject_name, num_problems=3):
    if not os.path.exists(note_path):
        return "File not found."
        
    with open(note_path, 'r', encoding="utf-8") as f:
        raw_note_content = f.read()

    syllabus_data, formula_data = load_secondary_contexts(subject_name)

    # 🗂️ SUBJECT DETECTION FLAGS
    sub_lower = subject_name.lower().strip()
    
    is_stem = sub_lower in ["physics", "mathematics", "math"]
    is_spanish = sub_lower in ["spanish", "español", "spanish b", "spanish a"]
    is_econ = sub_lower in ["economics", "econ"]
    is_english = sub_lower in ["english", "english language and literature", "english lang lit", "english a"]
    is_compsci = sub_lower in ["computer science", "comp sci", "cs"]

    # 🛠️ DYNAMIC INSTRUCTION GENERATOR (Section 4)
    if is_stem:
        stem_instruction = (
            f"4. STEM PRACTICE PROBLEMS: Because this is a STEM subject ({subject_name.title()}), "
            f"you must generate EXACTLY {num_problems} custom practice problems based on the vault "
            f"formulas and notes. Number them clearly 1 to {num_problems}. "
            f"Provide a hidden/collapsed 'Worked Solution' block using clear LaTeX formatting for each."
        )
    elif is_compsci:
        stem_instruction = (
            f"4. COMPUTER SCIENCE CHALLENGE: Because this is Computer Science, generate ONE custom algorithmic "
            f"problem or pseudocode/code trace exercise based on these notes. Provide a collapsed 'Solution & Code Walkthrough' block."
        )
    elif is_econ:
        stem_instruction = (
            f"4. ECONOMICS DIAGRAM BLUEPRINT: Because this is Economics, explicitly describe the exact IB Economics diagram "
            f"that matches this concept (e.g., Supply/Demand, Externalities, AD/AS). Outline what should be on the X/Y axes, "
            f"the curve shifts, and provide a 3-point analytical explanation of the real-world market outcome."
        )
    elif is_english:
        stem_instruction = (
            f"4. LITERARY ANALYSIS PROMPT: Because this is English Lang Lit, generate a critical commentary prompt or a "
            f"stylistic analysis question targeting the text's formal features, audience, or subtext. Provide a 3-line "
            f"high-scoring thesis statement blueprint that an IB student could use to answer it."
        )
    elif is_spanish:
        stem_instruction = "4. EJERCICIOS DE PRÁCTICA: Dado que esta es una asignatura de Español, omite los problemas matemáticos pero incluye un breve ejercicio de análisis de texto o gramática al final basado en las notas."
    else:
        stem_instruction = "4. SUPPLEMENTARY PRACTICE: Skip technical formatting. Provide two high-yield conceptual review questions."

    # 🌐 CHOOSE SYSTEM PERSPECTIVE & LANGUAGE
    if is_spanish:
        system_instruction = (
            f"Eres el motor central automatizado de procesamiento de notas de IB Omniscience.\n"
            f"DEBES responder, formatear y generar todo el documento final COMPLETAMENTE EN ESPAÑOL.\n\n"
            f"--- CONTEXTO DEL PLAN DE ESTUDIOS DE TODDLE ---\n"
            f"{json.dumps(syllabus_data, indent=2)}\n\n"
            f"--- CONTEXTO DEL BAÚL DE FÓRMULAS ---\n"
            f"{json.dumps(formula_data, indent=2)}\n\n"
            f"INSTRUCCIONES OPERATIVAS:\n"
            f"1. LIMPIEZA Y FORMATO ESENCIAL: Lee las notas en sucio del usuario. Corrige la gramática y la estructura usando títulos en Markdown (##, ###).\n"
            f"2. AUDITORÍA DEL TEMARIO: Compara el contenido con los objetivos del programa de Toddle proporcionados arriba. Documenta brechas de aprendizaje.\n"
            f"3. TARJETAS DE ESTUDIO UNIVERSALES: Genera 3 a 5 tarjetas de memoria (Frente/Reverso).\n"
            f"{stem_instruction}"
        )
    else:
        persona_modifier = "the ultimate automated IB Omniscience Note-Processor Core Engine."
        if is_econ:
            persona_modifier = "a world-class IB Economics Chief Examiner specialized in micro, macro, and global market policies."
        elif is_english:
            persona_modifier = "an expert IB English A Literature textual analyst specialized in structural critique, stylistic features, and text types."
        elif is_compsci:
            persona_modifier = "a Senior Software Architect and IB Computer Science internal assessment systems auditor."

        system_instruction = (
            f"You are {persona_modifier}\n\n"
            f"--- LAYER 1: AUTHORITATIVE TODDLE SYLLABUS CONTEXT ---\n"
            f"{json.dumps(syllabus_data, indent=2)}\n\n"
            f"--- LAYER 2: AUTHORITATIVE FORMULA/DATA VAULT CONTEXT ---\n"
            f"{json.dumps(formula_data, indent=2)}\n\n"
            f"OPERATIONAL INSTRUCTIONS:\n"
            f"1. CORE CLEAN-UP & FORMATTING: Read the user's raw notes. Clean up grammar and structure "
            f"using Markdown headings and clean formatting. Keep their true intent intact.\n"
            f"2. SYLLABUS AUDIT: Cross-reference the content against the Toddle Syllabus objectives provided above. "
            f"Explicitly document any learning gaps or missing curriculum indicators based on the database.\n"
            f"3. UNIVERSAL STUDY FLASHCARDS: Generate a set of 3 to 5 high-yield study flashcards based directly "
            f"on the text concepts. Include clear Front/Back components.\n"
            f"{stem_instruction}"
        )

    print(f"[NOTE PROCESSOR Core] Initiating unified audit and build pipeline for '{subject_name.title()}'...")

    # FIXED: Reconfigured generation endpoint to match structural standard
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=raw_note_content,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=2500,
            temperature=0.2
        )
    )
    return response.text

# FIXED: Un-indented function block completely so it is globally exposed to workspace.py
def evaluate_user_response(problem_text, user_answer_text, subject_name):
    """Grades and breaks down an submitted student work response against criteria."""
    sub_lower = subject_name.lower().strip()
    is_spanish = sub_lower in ["espanol", "spanish", "español", "spanish a", "spanish b"]

    # FIXED: Changed curly brackets to raw multi-line strings
    if is_spanish:
        system_instruction = (
            "Eres un evaluador y tutor experto del Bachillerato Internacional (IB).\n"
            "Tu tarea es calificar la respuesta del estudiante a un problema dado de forma estricta pero constructiva.\n\n"
            "DEBES RESPONDER COMPLETAMENTE EN ESPAÑOL USANDO ESTE FORMATO:\n"
            "## 📊 EVALUACIÓN DE RESPUESTA\n"
            "* **Resultado:** [¿Correcto, Parcialmente Correcto, o Incorrecto?]\n"
            "* **Puntuación estimada de criterios IB:** [Por ejemplo, 2/4 o 7/7]\n\n"
            "## 🔍 ANÁLISIS DE ERRORES\n"
            "[Explica detalladamente qué hizo bien el estudiante y exactamente dónde ocurrió un malentendido o error de cálculo.]\n\n"
            "## 💡 GUÍA PASO A PASO PARA LLEGAR A LA SOLUCIÓN CORRECTA\n"
            "[Muestra el camino analítico o matemático correcto. Si es un tema técnico o STEM, usa bloques de LaTeX para las ecuaciones.]"
        )
    else:
        system_instruction = (
            "You are an expert International Baccalaureate (IB) Examiner and personal academic tutor.\n"
            "Your task is to grade the student's submitted answer against the provided question string.\n\n"
            "YOU MUST OUPUT YOUR EVALUATION IN MARKDOWN USING THIS EXACT FORMAT:\n"
            "## 📊 ANSWER EVALUATION\n"
            "* **Verdict:** [Correct, Partially Correct, or Incorrect]\n"
            "* **Estimated IB Criterion Marks:** [e.g., 3/5 or 7/7 based on IB rubric standards]\n\n"
            "## 🔍 ERROR ANALYSIS\n"
            "[Break down what the student did right, and exactly where a misconception, structural gap, or math error occurred.]\n\n"
            "## 💡 STEP-BY-STEP PATH TO THE RIGHT ANSWER\n"
            "[Show the pristine analytical or mathematical breakdown required to score full marks. Use clean LaTeX styling for variables or formulas if applicable.]"
        )
    
    prompt = (
        f"ORIGINAL QUESTION:\n{problem_text}\n\n"
        f"STUDENT'S SUBMITTED ANSWER:\n{user_answer_text}\n"
    )

    # FIXED: Cleared internal trailing syntax commas and variable naming conflicts
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=2500,
            temperature=0.2
        )
    )
    return response.text
            
            


   
    
