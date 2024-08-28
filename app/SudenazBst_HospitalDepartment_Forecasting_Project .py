import tkinter as tk
from tkinter import ttk
import google.generativeai as genai

# Google Generative AI configuration
genai.configure(api_key="AIzaSyAqmTiN69Kbf2sqm2J8MP-qGV06JUBftPM")
model = genai.GenerativeModel(model_name="gemini-pro")

#priority order
priority_map = {
    "kalp krizi": {"department": "Acil Servis veya Kardiyoloji", "priority": 10},
    "beyin kanaması": {"department": "Acil Servis veya Nöroloji", "priority": 9},
    "astım krizi": {"department": "Acil Servis veya Pulmonoloji", "priority": 8},
    "anafilaksi": {"department": "Acil Servis veya Alerji ve Immunoloji", "priority": 8},
    "yüksek ateş": {"department": "Acil Servis veya İç Hastalıkları", "priority": 7},
}

def determine_department(symptoms, age, gender, medical_history):
    max_priority = 0
    priority_department = ""

    for condition in medical_history.split(','):
        if condition.strip() in priority_map:
            if priority_map[condition.strip()]["priority"] > max_priority:
                max_priority = priority_map[condition.strip()]["priority"]
                priority_department = priority_map[condition.strip()]["department"]

    if priority_department:
        return priority_department

    text = f"I have a {age}-year-old {gender} patient with {', '.join(symptoms)}. Their medical history includes {medical_history}. Which department should they go to?"
    response = model.generate_content(text)
    response_text = response.text.strip()

    if not response_text:
        return "Bilinmeyen"

    return response_text

def on_submit():
    symptoms = symptoms_entry.get().split(',')
    age = age_entry.get()
    gender = gender_entry.get()
    medical_history = medical_history_entry.get()

    department = determine_department(symptoms, age, gender, medical_history)

    result_label.config(text=f"Proposed Hospital Unit: {department}")

# Creating a main window and frame
root = tk.Tk()
root.title("Hospital Unit Recommendation Interface")

# Adding widgets to the main frame
symptoms_label = ttk.Label(root, text="Symptoms (separated by commas):")
symptoms_entry = ttk.Entry(root, width=40)

age_label = ttk.Label(root, text="Age:")
age_entry = ttk.Entry(root, width=40)

gender_label = ttk.Label(root, text="Gender:")
gender_entry = ttk.Entry(root, width=40)

medical_history_label = ttk.Label(root, text="Medical History (if available, otherwise write 'None'):")
medical_history_entry = ttk.Entry(root, width=40)

submit_button = ttk.Button(root, text="Send", command=on_submit)

result_label = ttk.Label(root, text="")

# Embed widgets
symptoms_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
symptoms_entry.grid(row=0, column=1, padx=10, pady=5)

age_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
age_entry.grid(row=1, column=1, padx=10, pady=5)

gender_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
gender_entry.grid(row=2, column=1, padx=10, pady=5)

medical_history_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
medical_history_entry.grid(row=3, column=1, padx=10, pady=5)

submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

result_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Close window for logout
root.mainloop()
