"""
Comprehensive Health Knowledge Base for Wellbeing Chatbot
Contains information on various health conditions, symptoms, treatments, and wellness advice
"""

HEALTH_CONDITIONS = {
    # Mental Health Conditions
    "anxiety": {
        "symptoms": ["racing heart", "sweating", "trembling", "shortness of breath", "feeling of impending doom", "chest pain", "dizziness", "fear of losing control"],
        "causes": ["stress", "genetics", "brain chemistry", "environmental factors", "medical conditions"],
        "treatments": ["cognitive behavioral therapy", "medication", "relaxation techniques", "exercise", "healthy diet", "adequate sleep"],
        "immediate_help": "Practice deep breathing: inhale for 4 counts, hold for 4, exhale for 4. If symptoms persist, seek immediate medical attention.",
        "prevention": ["regular exercise", "stress management", "healthy sleep habits", "limiting caffeine", "mindfulness practices"]
    },
    "depression": {
        "symptoms": ["persistent sadness", "loss of interest", "fatigue", "sleep changes", "appetite changes", "difficulty concentrating", "feelings of worthlessness", "suicidal thoughts"],
        "causes": ["genetics", "brain chemistry", "stress", "trauma", "medical conditions", "substance abuse"],
        "treatments": ["antidepressant medication", "psychotherapy", "cognitive behavioral therapy", "interpersonal therapy", "electroconvulsive therapy", "light therapy"],
        "immediate_help": "Reach out to a trusted friend or family member. If you have suicidal thoughts, call emergency services immediately.",
        "prevention": ["regular exercise", "healthy diet", "adequate sleep", "stress management", "social connections", "hobbies and interests"]
    },
    "stress": {
        "symptoms": ["headaches", "muscle tension", "fatigue", "sleep problems", "irritability", "anxiety", "depression", "digestive issues"],
        "causes": ["work pressure", "financial problems", "relationship issues", "health concerns", "major life changes"],
        "treatments": ["stress management techniques", "relaxation exercises", "time management", "exercise", "healthy eating", "adequate sleep"],
        "immediate_help": "Take deep breaths, step away from the stressor, practice progressive muscle relaxation.",
        "prevention": ["time management", "setting boundaries", "regular exercise", "healthy diet", "good sleep habits", "social support"]
    },
    "insomnia": {
        "symptoms": ["difficulty falling asleep", "waking up frequently", "waking up too early", "feeling tired after sleep", "daytime fatigue"],
        "causes": ["stress", "anxiety", "depression", "caffeine", "alcohol", "medical conditions", "poor sleep habits"],
        "treatments": ["cognitive behavioral therapy for insomnia", "sleep hygiene education", "relaxation techniques", "medication"],
        "immediate_help": "Create a relaxing bedtime routine, avoid screens before bed, ensure your bedroom is cool and dark.",
        "prevention": ["consistent sleep schedule", "relaxing bedtime routine", "comfortable sleep environment", "limiting caffeine and alcohol"]
    },

    # Cardiovascular Diseases
    "hypertension": {
        "symptoms": ["usually asymptomatic", "headaches", "dizziness", "chest pain", "shortness of breath"],
        "causes": ["genetics", "poor diet", "lack of exercise", "obesity", "stress", "smoking", "excess alcohol"],
        "treatments": ["lifestyle changes", "medication", "dietary modifications", "regular exercise"],
        "immediate_help": "If experiencing chest pain or shortness of breath, seek immediate medical attention.",
        "prevention": ["healthy diet", "regular exercise", "weight management", "stress reduction", "limiting alcohol and salt"]
    },
    "heart_disease": {
        "symptoms": ["chest pain", "shortness of breath", "fatigue", "irregular heartbeat", "dizziness", "nausea"],
        "causes": ["atherosclerosis", "high blood pressure", "high cholesterol", "smoking", "diabetes", "family history"],
        "treatments": ["medication", "angioplasty", "bypass surgery", "lifestyle changes", "cardiac rehabilitation"],
        "immediate_help": "Call emergency services immediately if experiencing chest pain, shortness of breath, or dizziness.",
        "prevention": ["heart-healthy diet", "regular exercise", "not smoking", "weight management", "stress reduction"]
    },
    "stroke": {
        "symptoms": ["sudden numbness", "confusion", "trouble speaking", "vision problems", "walking difficulties", "severe headache"],
        "causes": ["high blood pressure", "smoking", "diabetes", "high cholesterol", "atrial fibrillation", "family history"],
        "treatments": ["clot-busting drugs", "mechanical thrombectomy", "rehabilitation therapy", "medication"],
        "immediate_help": "Call emergency services immediately. Time is critical - treatment within 3 hours can prevent permanent damage.",
        "prevention": ["control blood pressure", "don't smoke", "manage diabetes", "healthy diet", "regular exercise"]
    },

    # Respiratory Diseases
    "asthma": {
        "symptoms": ["wheezing", "coughing", "shortness of breath", "chest tightness", "difficulty speaking"],
        "causes": ["genetics", "environmental factors", "allergies", "respiratory infections"],
        "treatments": ["inhaled corticosteroids", "bronchodilators", "allergy medications", "avoiding triggers"],
        "immediate_help": "Use quick-relief inhaler. Sit upright and try to stay calm. Seek emergency help if symptoms worsen.",
        "prevention": ["avoid triggers", "take medications as prescribed", "regular check-ups", "flu shots"]
    },
    "chronic_obstructive_pulmonary_disease": {
        "symptoms": ["chronic cough", "shortness of breath", "wheezing", "chest tightness", "frequent respiratory infections"],
        "causes": ["smoking", "air pollution", "genetics", "occupational exposure"],
        "treatments": ["bronchodilators", "inhaled steroids", "oxygen therapy", "pulmonary rehabilitation", "surgery"],
        "immediate_help": "Use prescribed inhalers. Sit in a comfortable position. Seek medical help if breathing becomes very difficult.",
        "prevention": ["quit smoking", "avoid air pollution", "get vaccinated", "regular exercise", "healthy diet"]
    },
    "pneumonia": {
        "symptoms": ["cough", "fever", "chills", "shortness of breath", "chest pain", "fatigue", "nausea"],
        "causes": ["bacterial infection", "viral infection", "fungal infection", "aspiration"],
        "treatments": ["antibiotics", "antiviral medications", "rest", "fluids", "oxygen therapy"],
        "immediate_help": "Rest and drink plenty of fluids. Seek medical attention if symptoms worsen or if you have difficulty breathing.",
        "prevention": ["vaccination", "good hygiene", "quit smoking", "healthy diet", "regular exercise"]
    },

    # Metabolic Diseases
    "diabetes": {
        "symptoms": ["frequent urination", "increased thirst", "increased hunger", "fatigue", "slow-healing sores", "frequent infections", "blurred vision"],
        "causes": ["type 1: autoimmune", "type 2: insulin resistance", "genetics", "lifestyle factors"],
        "treatments": ["insulin therapy", "oral medications", "diet management", "exercise", "blood sugar monitoring"],
        "immediate_help": "Monitor blood sugar levels. If experiencing hypoglycemia, consume fast-acting glucose.",
        "prevention": ["healthy diet", "regular exercise", "weight management", "regular medical check-ups"]
    },
    "thyroid_disorders": {
        "symptoms": ["weight changes", "fatigue", "mood changes", "temperature sensitivity", "hair loss", "heart rate changes"],
        "causes": ["autoimmune disorders", "iodine deficiency", "genetics", "medications"],
        "treatments": ["hormone replacement", "antithyroid medications", "radioactive iodine", "surgery"],
        "immediate_help": "Monitor symptoms and consult a doctor for proper diagnosis and treatment.",
        "prevention": ["adequate iodine intake", "regular thyroid screening", "manage stress", "healthy lifestyle"]
    },
    "obesity": {
        "symptoms": ["excess body fat", "shortness of breath", "joint pain", "fatigue", "sleep apnea"],
        "causes": ["poor diet", "lack of exercise", "genetics", "medical conditions", "medications"],
        "treatments": ["dietary changes", "exercise", "behavioral therapy", "medication", "bariatric surgery"],
        "immediate_help": "Focus on gradual, sustainable lifestyle changes rather than crash diets.",
        "prevention": ["balanced diet", "regular physical activity", "portion control", "healthy sleep habits"]
    },

    # Musculoskeletal Diseases
    "arthritis": {
        "symptoms": ["joint pain", "stiffness", "swelling", "reduced range of motion", "fatigue"],
        "causes": ["wear and tear", "autoimmune disorders", "infection", "crystal-induced"],
        "treatments": ["pain relievers", "anti-inflammatory drugs", "physical therapy", "joint injections", "surgery"],
        "immediate_help": "Rest the affected joint, apply ice or heat, use over-the-counter pain relievers.",
        "prevention": ["maintain healthy weight", "regular exercise", "proper posture", "joint protection"]
    },
    "osteoporosis": {
        "symptoms": ["bone fractures", "loss of height", "back pain", "stooped posture"],
        "causes": ["aging", "hormone changes", "nutrient deficiencies", "lack of exercise", "medications"],
        "treatments": ["calcium supplements", "vitamin D", "bisphosphonates", "hormone therapy", "exercise"],
        "immediate_help": "Be careful with movements to avoid fractures. Consult a doctor for bone density testing.",
        "prevention": ["adequate calcium intake", "vitamin D", "weight-bearing exercise", "no smoking", "limit alcohol"]
    },
    "back_pain": {
        "symptoms": ["aching", "stiffness", "sharp pain", "radiating pain", "muscle spasms"],
        "causes": ["poor posture", "muscle strain", "herniated disc", "arthritis", "osteoporosis"],
        "treatments": ["rest", "ice/heat therapy", "pain relievers", "physical therapy", "exercise"],
        "immediate_help": "Rest, apply ice for 20 minutes, avoid strenuous activities. Use over-the-counter pain relievers.",
        "prevention": ["good posture", "regular exercise", "proper lifting techniques", "ergonomic workspace"]
    },

    # Neurological Diseases
    "migraine": {
        "symptoms": ["severe headache", "nausea", "vomiting", "sensitivity to light", "sensitivity to sound", "aura", "neck stiffness"],
        "causes": ["genetics", "hormonal changes", "stress", "certain foods", "environmental factors", "medications"],
        "treatments": ["pain relievers", "triptans", "preventive medications", "lifestyle changes", "stress management"],
        "immediate_help": "Rest in a dark, quiet room. Apply cold compresses. Over-the-counter pain relievers may help if taken early.",
        "prevention": ["identify triggers", "stress management", "regular sleep schedule", "regular meals", "exercise"]
    },
    "alzheimers_disease": {
        "symptoms": ["memory loss", "confusion", "difficulty with familiar tasks", "mood changes", "behavioral changes"],
        "causes": ["aging", "genetics", "lifestyle factors", "cardiovascular disease"],
        "treatments": ["medication", "cognitive therapy", "supportive care", "lifestyle modifications"],
        "immediate_help": "Create a safe environment and establish routines. Seek medical evaluation for proper diagnosis.",
        "prevention": ["regular exercise", "healthy diet", "mental stimulation", "social engagement", "cardiovascular health"]
    },
    "parkinsons_disease": {
        "symptoms": ["tremor", "stiffness", "bradykinesia", "postural instability", "speech changes"],
        "causes": ["genetics", "environmental factors", "aging", "head trauma"],
        "treatments": ["medication", "physical therapy", "occupational therapy", "speech therapy", "surgery"],
        "immediate_help": "Work with healthcare providers to manage symptoms and maintain independence.",
        "prevention": ["regular exercise", "healthy diet", "avoid head trauma", "environmental toxin avoidance"]
    },

    # Digestive Diseases
    "irritable_bowel_syndrome": {
        "symptoms": ["abdominal pain", "bloating", "gas", "diarrhea", "constipation", "mucus in stool"],
        "causes": ["gut-brain axis dysfunction", "stress", "diet", "infection", "food intolerances"],
        "treatments": ["dietary changes", "stress management", "medication", "fiber supplements", "probiotics"],
        "immediate_help": "Identify and avoid trigger foods. Manage stress. Use over-the-counter remedies for symptoms.",
        "prevention": ["high-fiber diet", "regular meals", "stress management", "adequate hydration", "regular exercise"]
    },
    "gastroesophageal_reflux_disease": {
        "symptoms": ["heartburn", "regurgitation", "chest pain", "difficulty swallowing", "chronic cough"],
        "causes": ["hiatal hernia", "obesity", "pregnancy", "smoking", "certain foods"],
        "treatments": ["lifestyle changes", "medication", "surgery"],
        "immediate_help": "Avoid trigger foods, eat smaller meals, don't lie down after eating, elevate head of bed.",
        "prevention": ["maintain healthy weight", "avoid trigger foods", "don't smoke", "eat smaller meals"]
    },
    "ulcerative_colitis": {
        "symptoms": ["abdominal pain", "diarrhea", "rectal bleeding", "weight loss", "fatigue"],
        "causes": ["autoimmune disorder", "genetics", "environmental factors"],
        "treatments": ["anti-inflammatory drugs", "immune suppressants", "surgery", "dietary management"],
        "immediate_help": "Stay hydrated, eat small frequent meals, avoid irritants. Seek medical attention for severe symptoms.",
        "prevention": ["regular medical follow-up", "stress management", "healthy diet", "avoid smoking"]
    },

    # Infectious Diseases
    "covid_19": {
        "symptoms": ["fever", "cough", "fatigue", "loss of taste/smell", "shortness of breath", "body aches"],
        "causes": ["SARS-CoV-2 virus infection"],
        "treatments": ["supportive care", "antiviral medications", "vaccination", "rest", "hydration"],
        "immediate_help": "Isolate yourself, monitor symptoms, seek medical help if breathing difficulties occur.",
        "prevention": ["vaccination", "mask wearing", "social distancing", "hand hygiene", "ventilation"]
    },
    "influenza": {
        "symptoms": ["fever", "cough", "sore throat", "body aches", "fatigue", "headache"],
        "causes": ["influenza virus infection"],
        "treatments": ["rest", "fluids", "antiviral medications", "pain relievers"],
        "immediate_help": "Rest, stay hydrated, use over-the-counter medications for symptoms. Seek medical help if symptoms worsen.",
        "prevention": ["annual vaccination", "hand hygiene", "avoid close contact with sick people", "cover coughs"]
    },
    "tuberculosis": {
        "symptoms": ["chronic cough", "weight loss", "night sweats", "fatigue", "fever", "chest pain"],
        "causes": ["Mycobacterium tuberculosis infection"],
        "treatments": ["antibiotic therapy", "directly observed therapy", "supportive care"],
        "immediate_help": "Seek medical evaluation if you suspect TB. Cover your mouth when coughing.",
        "prevention": ["vaccination", "infection control", "treatment of latent TB", "healthy immune system"]
    },

    # Autoimmune Diseases
    "rheumatoid_arthritis": {
        "symptoms": ["joint pain", "swelling", "stiffness", "fatigue", "fever", "weight loss"],
        "causes": ["autoimmune disorder", "genetics", "environmental factors"],
        "treatments": ["disease-modifying antirheumatic drugs", "biologics", "physical therapy", "surgery"],
        "immediate_help": "Rest affected joints, apply ice, use assistive devices. Consult rheumatologist for management.",
        "prevention": ["early diagnosis and treatment", "regular exercise", "healthy diet", "stress management"]
    },
    "lupus": {
        "symptoms": ["fatigue", "joint pain", "rash", "fever", "hair loss", "mouth sores", "organ involvement"],
        "causes": ["autoimmune disorder", "genetics", "environmental factors", "hormones"],
        "treatments": ["anti-inflammatory drugs", "immunosuppressants", "corticosteroids", "lifestyle management"],
        "immediate_help": "Protect skin from sun, manage stress, get adequate rest. Seek medical care for flares.",
        "prevention": ["sun protection", "regular medical monitoring", "healthy lifestyle", "avoid smoking"]
    },
    "multiple_sclerosis": {
        "symptoms": ["vision problems", "numbness", "weakness", "balance issues", "fatigue", "cognitive changes"],
        "causes": ["autoimmune attack on myelin", "genetics", "environmental factors"],
        "treatments": ["disease-modifying therapies", "symptom management", "physical therapy", "rehabilitation"],
        "immediate_help": "Rest during exacerbations, manage symptoms, work with healthcare team for optimal management.",
        "prevention": ["regular medical follow-up", "healthy lifestyle", "stress management", "exercise"]
    },

    # Cancer
    "breast_cancer": {
        "symptoms": ["lump in breast", "breast pain", "nipple changes", "skin changes", "swelling"],
        "causes": ["genetics", "hormonal factors", "lifestyle factors", "environmental factors"],
        "treatments": ["surgery", "radiation", "chemotherapy", "hormone therapy", "targeted therapy"],
        "immediate_help": "Perform regular self-exams, get mammograms as recommended. Consult doctor for any changes.",
        "prevention": ["regular screening", "healthy diet", "regular exercise", "limit alcohol", "maintain healthy weight"]
    },
    "lung_cancer": {
        "symptoms": ["persistent cough", "chest pain", "shortness of breath", "weight loss", "fatigue"],
        "causes": ["smoking", "radon exposure", "asbestos", "air pollution", "genetics"],
        "treatments": ["surgery", "radiation", "chemotherapy", "targeted therapy", "immunotherapy"],
        "immediate_help": "Don't ignore persistent respiratory symptoms. Seek medical evaluation promptly.",
        "prevention": ["quit smoking", "avoid radon", "reduce air pollution exposure", "regular check-ups"]
    },
    "colorectal_cancer": {
        "symptoms": ["blood in stool", "changes in bowel habits", "abdominal pain", "weight loss", "fatigue"],
        "causes": ["age", "family history", "diet", "lifestyle factors", "inflammatory bowel disease"],
        "treatments": ["surgery", "chemotherapy", "radiation", "targeted therapy"],
        "immediate_help": "Don't ignore changes in bowel habits or blood in stool. Get screened regularly.",
        "prevention": ["colonoscopy screening", "healthy diet", "regular exercise", "maintain healthy weight"]
    },

    # Other Common Conditions
    "allergies": {
        "symptoms": ["sneezing", "runny nose", "itchy eyes", "skin rash", "hives", "swelling"],
        "causes": ["environmental allergens", "food allergens", "medications", "insect stings"],
        "treatments": ["antihistamines", "corticosteroids", "allergy shots", "avoiding triggers"],
        "immediate_help": "For severe allergic reactions (anaphylaxis), use epinephrine auto-injector and seek emergency help.",
        "prevention": ["identify triggers", "allergy-proof home", "medication for severe allergies", "allergy shots"]
    },
    "eczema": {
        "symptoms": ["itchy skin", "red patches", "dry skin", "cracked skin", "oozing lesions"],
        "causes": ["genetics", "environmental factors", "immune system dysfunction"],
        "treatments": ["moisturizers", "corticosteroid creams", "antihistamines", "light therapy"],
        "immediate_help": "Keep skin moisturized, avoid scratching, use cool compresses for itching.",
        "prevention": ["moisturize regularly", "avoid triggers", "gentle skin care", "humid environment"]
    },
    "psoriasis": {
        "symptoms": ["red patches", "silvery scales", "itchy skin", "thickened skin", "joint pain"],
        "causes": ["autoimmune disorder", "genetics", "environmental triggers"],
        "treatments": ["topical treatments", "light therapy", "systemic medications", "biologics"],
        "immediate_help": "Keep skin moisturized, avoid picking scales, use prescribed treatments consistently.",
        "prevention": ["stress management", "avoid triggers", "regular treatment", "healthy lifestyle"]
    }
}

MENTAL_HEALTH_CONDITIONS = {
    "bipolar_disorder": {
        "symptoms": ["manic episodes", "depressive episodes", "mixed episodes", "rapid mood swings"],
        "treatments": ["mood stabilizers", "antipsychotics", "antidepressants", "psychotherapy"],
        "management": ["medication adherence", "regular sleep schedule", "stress management", "support system"],
        "prevention": ["maintain consistent sleep patterns", "avoid substance abuse", "regular therapy sessions", "stress management techniques", "build strong support networks", "monitor mood changes early"]
    },
    "ptsd": {
        "symptoms": ["flashbacks", "nightmares", "avoidance", "hypervigilance", "emotional numbness"],
        "treatments": ["trauma-focused therapy", "medication", "exposure therapy", "cognitive processing therapy"],
        "management": ["establishing routines", "avoiding triggers", "building support network", "self-care practices"],
        "prevention": ["seek immediate support after trauma", "practice stress management", "maintain social connections", "develop coping skills", "avoid isolation", "regular mental health check-ups"]
    },
    "ocd": {
        "symptoms": ["obsessive thoughts", "compulsive behaviors", "anxiety", "time-consuming rituals"],
        "treatments": ["cognitive behavioral therapy", "exposure therapy", "medication"],
        "management": ["therapy adherence", "stress reduction", "support groups", "healthy lifestyle"],
        "prevention": ["early intervention for anxiety symptoms", "stress management training", "cognitive behavioral techniques", "family education", "avoiding perfectionism triggers", "regular mental health monitoring"]
    },
    "eating_disorders": {
        "symptoms": ["restrictive eating", "binge eating", "purging", "body image distortion"],
        "treatments": ["nutritional counseling", "psychotherapy", "medical monitoring", "support groups"],
        "management": ["regular meals", "challenging negative thoughts", "building healthy relationships", "professional support"],
        "prevention": ["promote positive body image", "healthy relationship with food", "early intervention for body dissatisfaction", "stress management", "family support and education", "regular mental health screenings"]
    }
}

WELLNESS_TOPICS = {
    "nutrition": {
        "balanced_diet": "Include fruits, vegetables, whole grains, lean proteins, and healthy fats in your diet.",
        "hydration": "Drink at least 8 glasses of water daily. More if you're active or in hot weather.",
        "meal_planning": "Plan meals ahead to ensure nutritional balance and reduce stress."
    },
    "exercise": {
        "cardiovascular": "Aim for 150 minutes of moderate aerobic activity weekly.",
        "strength_training": "Include strength training 2-3 times per week for all major muscle groups.",
        "flexibility": "Practice stretching or yoga to maintain flexibility and reduce injury risk."
    },
    "sleep": {
        "duration": "Adults need 7-9 hours of sleep per night.",
        "hygiene": "Maintain consistent sleep schedule, create relaxing bedtime routine, optimize sleep environment.",
        "daytime": "Limit naps, avoid caffeine late in day, get morning sunlight exposure."
    },
    "mental_wellness": {
        "mindfulness": "Practice being present in the moment through meditation or mindful activities.",
        "social_connections": "Maintain relationships and build new connections for emotional support.",
        "stress_management": "Use techniques like deep breathing, progressive relaxation, or hobbies to manage stress."
    }
}

SYMPTOM_CHECKER = {
    "chest_pain": ["heart attack", "angina", "anxiety", "muscle strain", "seek immediate medical attention"],
    "shortness_of_breath": ["asthma", "pneumonia", "anxiety", "heart problems", "consult doctor"],
    "severe_headache": ["migraine", "tension headache", "cluster headache", "aneurysm", "see healthcare provider"],
    "abdominal_pain": ["appendicitis", "gallstones", "ulcer", "food poisoning", "medical evaluation needed"],
    "fever": ["infection", "flu", "COVID-19", "other illnesses", "monitor and consult if persistent"],
    "fatigue": ["anemia", "depression", "thyroid issues", "sleep disorders", "comprehensive check-up"],
    "dizziness": ["dehydration", "low blood pressure", "inner ear problems", "anxiety", "medical assessment"],
    "nausea": ["food poisoning", "pregnancy", "migraine", "medication side effects", "seek medical advice"]
}

SYMPTOM_PREVENTION = {
    "headache": ["stay hydrated", "maintain regular sleep schedule", "practice stress management", "limit caffeine intake", "regular exercise", "avoid trigger foods"],
    "diarrhea": ["practice good hand hygiene", "drink clean water", "avoid contaminated food", "get vaccinated for rotavirus", "proper food storage", "regular hand washing"],
    "stomach_pain": ["eat regular balanced meals", "stay hydrated", "manage stress levels", "avoid trigger foods", "practice portion control", "regular exercise"],
    "body_pain": ["maintain good posture", "regular stretching exercises", "ergonomic workspace setup", "adequate rest between activities", "proper lifting techniques", "regular physical activity"],
    "sadness": ["maintain social connections", "regular exercise routine", "practice mindfulness", "adequate sleep", "healthy diet", "seek support when needed"],
    "back_pain": ["maintain proper posture", "regular core strengthening exercises", "ergonomic chair and desk setup", "avoid prolonged sitting", "proper lifting techniques", "regular stretching"],
    "joint_pain": ["maintain healthy weight", "regular low-impact exercise", "proper posture", "warm-up before activities", "use supportive footwear", "avoid repetitive stress"],
    "neck_pain": ["maintain good posture", "regular neck stretches", "ergonomic computer setup", "avoid prolonged phone use", "proper pillow support", "regular breaks from screen time"],
    "toothache": ["regular dental check-ups", "proper brushing technique", "daily flossing", "limit sugary foods", "wear mouthguard for sports", "avoid chewing hard objects"],
    "ear_pain": ["keep ears dry", "avoid inserting objects in ears", "protect ears from loud noise", "regular ear cleaning", "avoid smoking", "manage allergies"],
    "sore_throat": ["stay hydrated", "avoid irritants like smoke", "practice good hand hygiene", "get adequate rest", "use humidifier", "avoid overuse of voice"],
    "cough": ["stay hydrated", "avoid irritants", "practice good hand hygiene", "get adequate rest", "use humidifier", "avoid smoking"],
    "runny_nose": ["practice good hand hygiene", "avoid allergens", "stay hydrated", "use saline nasal spray", "regular exercise", "adequate sleep"],
    "skin_rash": ["moisturize regularly", "avoid irritants", "wear protective clothing", "practice good hygiene", "manage stress", "avoid hot showers"],
    "itching": ["moisturize regularly", "avoid irritants", "wear breathable clothing", "manage allergies", "avoid hot water", "keep nails short"],
    "muscle_cramps": ["stay hydrated", "maintain electrolyte balance", "regular stretching", "gradual exercise increase", "proper warm-up", "adequate calcium intake"],
    "insomnia": ["maintain consistent sleep schedule", "create relaxing bedtime routine", "limit screen time before bed", "regular exercise", "manage stress", "optimize sleep environment"],
    "loss_of_appetite": ["eat small frequent meals", "stay hydrated", "regular physical activity", "manage stress", "avoid strong odors", "consult healthcare provider"],
    "constipation": ["increase fiber intake", "stay hydrated", "regular exercise", "establish regular toilet routine", "avoid delaying bowel movements", "eat probiotic-rich foods"],
    "heartburn": ["eat smaller meals", "avoid trigger foods", "don't lie down after eating", "elevate head of bed", "maintain healthy weight", "avoid tight clothing"],
    "bloating": ["eat slowly", "avoid carbonated drinks", "chew food thoroughly", "manage stress", "regular exercise", "limit salt intake"],
    "fever": ["practice good hygiene", "get vaccinated", "stay hydrated", "rest when needed", "monitor temperature", "seek medical attention if high"],
    "nausea": ["eat small frequent meals", "stay hydrated", "avoid strong odors", "rest in fresh air", "ginger tea", "acupressure wristbands"],
    "vomiting": ["stay hydrated with small sips", "rest stomach", "bland diet", "avoid strong odors", "gradual food reintroduction", "seek medical help if persistent"],
    "dizziness": ["stay hydrated", "rise slowly from sitting", "regular meals", "adequate sleep", "balance exercises", "avoid sudden movements"],
    "fatigue": ["maintain regular sleep schedule", "balanced nutrition", "regular exercise", "stress management", "limit caffeine", "take breaks"],
    "cold": ["practice good hand hygiene", "avoid touching face", "get adequate rest", "stay hydrated", "eat nutritious foods", "regular exercise"],
    "flu": ["annual vaccination", "good hand hygiene", "avoid close contact when sick", "cover coughs", "stay home when ill", "boost immune system"],
    "infection": ["practice good hygiene", "keep wounds clean", "vaccination", "healthy diet", "adequate sleep", "avoid sharing personal items"],
    "anxiety": ["practice deep breathing", "regular exercise", "adequate sleep", "limit caffeine", "mindfulness meditation", "seek support"],
    "depression": ["maintain social connections", "regular physical activity", "healthy diet", "adequate sleep", "practice gratitude", "seek professional help"],
    "stress": ["practice relaxation techniques", "regular exercise", "healthy diet", "adequate sleep", "time management", "social support"],
    "migraine": ["identify triggers", "maintain regular schedule", "stress management", "adequate hydration", "regular exercise", "avoid trigger foods"],
    "allergies": ["identify allergens", "keep environment clean", "use air purifiers", "medication as prescribed", "allergy shots", "avoid peak pollen times"],
    "asthma": ["avoid triggers", "take medications as prescribed", "regular exercise", "maintain healthy weight", "flu vaccination", "monitor symptoms"],
    "arthritis": ["maintain healthy weight", "regular exercise", "proper posture", "joint protection", "warm-up before activities", "assistive devices"],
    "diabetes": ["maintain healthy weight", "regular exercise", "balanced diet", "blood sugar monitoring", "regular medical check-ups", "stress management"],
    "hypertension": ["reduce salt intake", "maintain healthy weight", "regular exercise", "limit alcohol", "stress management", "regular monitoring"],
    "heart_disease": ["heart-healthy diet", "regular exercise", "no smoking", "weight management", "stress reduction", "regular check-ups"],
    "stroke": ["control blood pressure", "healthy diet", "regular exercise", "no smoking", "limit alcohol", "manage diabetes"],
    "cancer": ["healthy diet", "regular exercise", "no smoking", "limit alcohol", "regular screenings", "sun protection"],
    "osteoporosis": ["adequate calcium intake", "vitamin D", "weight-bearing exercise", "no smoking", "limit alcohol", "fall prevention"],
    "alzheimers": ["regular exercise", "healthy diet", "mental stimulation", "social engagement", "cardiovascular health", "regular check-ups"],
    "parkinsons": ["regular exercise", "healthy diet", "avoid head trauma", "environmental toxin avoidance", "regular medical care", "physical therapy"]
}

def get_health_info(condition):
    """Get comprehensive information about a health condition"""
    if condition in HEALTH_CONDITIONS:
        return HEALTH_CONDITIONS[condition]
    elif condition in MENTAL_HEALTH_CONDITIONS:
        return MENTAL_HEALTH_CONDITIONS[condition]
    return None

def get_symptom_info(symptom):
    """Get possible causes for a symptom"""
    return SYMPTOM_CHECKER.get(symptom.lower(), ["consult healthcare professional"])

def get_symptom_prevention(symptom):
    """Get prevention tips for a symptom"""
    return SYMPTOM_PREVENTION.get(symptom.lower(), ["maintain healthy lifestyle", "consult healthcare professional for personalized advice"])

def get_wellness_advice(topic):
    """Get wellness advice for a specific topic"""
    return WELLNESS_TOPICS.get(topic.lower(), "General wellness advice: maintain healthy diet, regular exercise, adequate sleep, and manage stress.")

def search_health_database(query):
    """Search the health database for relevant information"""
    query_lower = query.lower()
    results = []

    # Search conditions - handle both underscore and space versions
    for condition, info in HEALTH_CONDITIONS.items():
        condition_normalized = condition.replace('_', ' ')
        if condition in query_lower or condition_normalized in query_lower or any(symptom in query_lower for symptom in info.get('symptoms', [])):
            results.append({"type": "condition", "name": condition, "info": info})

    for condition, info in MENTAL_HEALTH_CONDITIONS.items():
        condition_normalized = condition.replace('_', ' ')
        if condition in query_lower or condition_normalized in query_lower:
            results.append({"type": "mental_health", "name": condition, "info": info})

    # Search symptoms
    for symptom, causes in SYMPTOM_CHECKER.items():
        if symptom in query_lower:
            results.append({"type": "symptom", "name": symptom, "causes": causes})

    # Search wellness topics
    for topic, advice in WELLNESS_TOPICS.items():
        if topic in query_lower:
            results.append({"type": "wellness", "name": topic, "advice": advice})

    # Search symptom prevention
    for symptom, prevention_tips in SYMPTOM_PREVENTION.items():
        if symptom in query_lower:
            results.append({"type": "prevention", "name": symptom, "prevention_tips": prevention_tips})

    return results
