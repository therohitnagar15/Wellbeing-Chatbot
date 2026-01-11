import google.generativeai as genai
from textblob import TextBlob
from excercises import breathing_exercise, mindfulness_exercise
from professor_exercises import academic_time_management_exercise, tenure_track_stress_management, work_life_boundary_setting, imposter_syndrome_academia, grading_overwhelm_relief, research_block_planning, student_interaction_recharge, academic_social_connection, sabbatical_preparation
from health_knowledge import get_health_info, get_symptom_info, get_wellness_advice, search_health_database
from models import User, MoodLog, ChatHistory

from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import os
import random
import difflib

load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
gemini_model = genai.GenerativeModel('gemini-pro')

def find_matching_intents(text, intents, threshold=0.8):
    """Find intents that match words in the text using fuzzy matching"""
    words = text.split()
    matches = []
    for word in words:
        for intent in intents:
            ratio = difflib.SequenceMatcher(None, intent, word).ratio()
            if ratio >= threshold:
                matches.append(intent)
    return list(set(matches))  # Return unique matches

CRISIS_WORDS = {
    "suicide": [
        "suicide", "kill myself", "end my life", "end it all", "not worth living",
        "better off dead", "want to die", "suicidal", "suicidal thoughts", "suicidal ideation",
        "overdose", "poison myself", "hang myself", "jump off", "shoot myself",
        "drown myself", "crash my car", "drive off a cliff", "take my life"
    ],
    "self_harm": [
        "self harm", "self-harm", "cutting", "hurting myself", "self injury", "self-injury"
    ],
    "mental_crisis": [
        "crisis", "emergency", "breakdown", "losing it", "falling apart",
        "can't go on", "give up", "no hope", "hopeless", "desperate", "desperation",
        "rock bottom", "hitting rock bottom", "breaking point", "at my limit",
        "psychotic", "psychosis", "hallucinations", "delusions", "paranoid",
        "hearing voices", "can't trust anyone", "everyone against me",
        "losing my mind", "going crazy", "insane", "mad"
    ],
    "violence": [
        "kill someone", "hurt someone", "harm others", "violent thoughts",
        "rage", "uncontrollable anger", "blackout rage"
    ],
    "severe_depression": [
        "worthless", "useless", "burden", "everyone better without me",
        "no one cares", "no one would miss me", "hate myself", "loathe myself",
        "empty inside", "numb", "nothing matters", "pointless", "meaningless"
    ],
    "addiction": [
        "can't stop", "out of control", "need help now", "intervention needed",
        "hitting bottom", "rock bottom addiction"
    ],
    "trauma_abuse": [
        "abuse", "rape", "sexual assault", "domestic violence", "being beaten",
        "threatened", "stalked", "in danger", "unsafe", "afraid for my life"
    ]
}

# Flatten crisis words for checking
ALL_CRISIS_WORDS = [word for category in CRISIS_WORDS.values() for word in category]
BREATHING_WORDS = ["breathing", "panic", "anxiety"]
MINDFUL_WORDS = ["mindfulness", "calm", "relax"]
RELAXATION_WORDS = ["tense", "muscle", "relaxation", "progressive", "tight"]
GRATITUDE_WORDS = ["grateful", "gratitude", "thankful", "appreciate"]
VISUALIZATION_WORDS = ["visualize", "imagine", "peaceful place", "mental imagery"]
MEDITATION_WORDS = ["meditate", "meditation", "body scan", "loving kindness"]
WALKING_WORDS = ["walk", "walking", "movement", "exercise"]
AFFIRMATION_WORDS = ["affirmation", "positive", "confidence", "self-esteem"]
COMPASSION_WORDS = ["self-compassion", "kindness", "gentle", "forgiving"]
NATURE_WORDS = ["nature", "outside", "fresh air", "natural"]
PREVENTION_WORDS = ["prevent", "avoid", "stop", "tips for", "how to prevent", "solutions for", "help with", "coping with", "prevention", "coping", "manage", "deal with"]

# Intent keywords for INTENT_RESPONSES
STRESS_WORDS = ["stress", "stressed", "overwhelmed", "pressure", "tension"]
ANXIETY_WORDS = ["anxiety", "anxious", "worried", "nervous", "panic"]
SADNESS_WORDS = ["sad", "sadness", "depressed", "down", "blue"]
FATIGUE_WORDS = ["fatigue", "tired", "exhausted", "fatigued", "sleepy"]
SLEEP_ISSUE_WORDS = ["sleep", "insomnia", "can't sleep", "sleepless"]
BURNOUT_WORDS = ["burnout", "burned out", "exhausted", "drained"]
HEADACHE_WORDS = ["headache", "head ache", "migraine"]
BODY_PAIN_WORDS = ["pain", "ache", "hurt", "sore"]
LIFESTYLE_WORDS = ["lifestyle", "habits", "routine", "daily life"]
HYDRATION_WORDS = ["hydration", "water", "dehydrated", "thirsty"]
SCREEN_FATIGUE_WORDS = ["screen", "eyes", "fatigue", "strain"]
MOTIVATION_WORDS = ["motivation", "motivated", "unmotivated", "lazy"]
DEPRESSION_WORDS = ["depression", "depressed", "hopeless", "worthless"]
PANIC_ATTACK_WORDS = ["panic attack", "panic", "heart racing", "can't breathe"]
LONELINESS_WORDS = ["lonely", "loneliness", "isolated", "alone"]
OVEREATING_WORDS = ["overeating", "binge eating", "emotional eating"]
INSOMNIA_WORDS = ["insomnia", "can't sleep", "sleepless nights"]
DIGESTIVE_ISSUES_WORDS = ["digestive", "stomach", "nausea", "bloating"]
BACK_PAIN_WORDS = ["back pain", "backache", "lower back"]
NECK_PAIN_WORDS = ["neck pain", "neck ache", "stiff neck"]
EYE_STRAIN_WORDS = ["eye strain", "eyes hurt", "blurry vision"]
CONCENTRATION_WORDS = ["concentration", "focus", "distracted", "can't concentrate"]
MEMORY_ISSUES_WORDS = ["memory", "forgetful", "can't remember"]
IRRITABILITY_WORDS = ["irritable", "irritated", "short tempered"]
SOCIAL_ANXIETY_WORDS = ["social anxiety", "shy", "awkward in groups"]
RELATIONSHIP_ISSUES_WORDS = ["relationship", "partner", "marriage", "breakup"]
GRIEF_WORDS = ["grief", "loss", "bereavement", "mourning"]
ADDICTION_WORDS = ["addiction", "addicted", "substance", "alcohol"]
EATING_DISORDER_WORDS = ["eating disorder", "bulimia", "anorexia"]
SELF_HARM_WORDS = ["self harm", "cutting", "hurting myself"]
SUICIDAL_THOUGHTS_WORDS = ["suicidal", "kill myself", "end it all"]
TRAUMA_WORDS = ["trauma", "traumatic", "abuse", "ptsd"]
PTSD_WORDS = ["ptsd", "flashbacks", "nightmares"]
OCD_WORDS = ["ocd", "obsessive", "compulsive"]
BIPOLAR_WORDS = ["bipolar", "mood swings", "manic"]
ADHD_WORDS = ["adhd", "attention deficit", "hyperactive"]
AUTISM_WORDS = ["autism", "autistic", "spectrum"]
CHRONIC_ILLNESS_WORDS = ["chronic illness", "chronic pain", "long term illness"]
DISABILITY_WORDS = ["disability", "disabled", "handicap"]
AGING_CONCERNS_WORDS = ["aging", "getting old", "elderly"]
MENOPAUSE_WORDS = ["menopause", "hot flashes", "hormonal changes"]
PREGNANCY_WORDS = ["pregnancy", "pregnant", "expecting"]
POSTPARTUM_WORDS = ["postpartum", "after birth", "new mother"]
INFERTILITY_WORDS = ["infertility", "can't conceive", "trying to get pregnant"]
CHRONIC_PAIN_WORDS = ["chronic pain", "persistent pain"]
ARTHRITIS_WORDS = ["arthritis", "joint pain"]
DIABETES_WORDS = ["diabetes", "blood sugar", "insulin"]
HEART_HEALTH_WORDS = ["heart", "cardiovascular", "cholesterol"]
CANCER_SUPPORT_WORDS = ["cancer", "chemotherapy", "radiation"]
WEIGHT_CONCERNS_WORDS = ["weight", "overweight", "body image"]
ALLERGY_WORDS = ["allergy", "allergies", "allergic"]
ASTHMA_WORDS = ["asthma", "breathing difficulty"]
THYROID_WORDS = ["thyroid", "hypothyroidism", "hyperthyroidism"]
HORMONAL_IMBALANCE_WORDS = ["hormonal", "hormones", "imbalance"]
IMMUNE_SYSTEM_WORDS = ["immune", "immunity", "sick often"]
DETOX_WORDS = ["detox", "cleansing", "purify"]
SUPPLEMENTS_WORDS = ["supplements", "vitamins", "minerals"]
VACCINATION_WORDS = ["vaccination", "vaccine", "immunization"]
MENTAL_HEALTH_STIGMA_WORDS = ["stigma", "judged", "ashamed"]
THERAPY_OPTIONS_WORDS = ["therapy", "counseling", "psychotherapy"]
MEDICATION_CONCERNS_WORDS = ["medication", "drugs", "side effects"]
EMERGENCY_MENTAL_HEALTH_WORDS = ["emergency", "crisis", "urgent help"]
PEER_SUPPORT_WORDS = ["peer support", "support group"]
MINDFULNESS_PRACTICE_WORDS = ["mindfulness", "mindful", "present moment"]
YOGA_BENEFITS_WORDS = ["yoga", "yoga practice"]
MEDITATION_TYPES_WORDS = ["meditation", "meditating"]
EXERCISE_MOTIVATION_WORDS = ["exercise", "workout", "physical activity"]
NUTRITION_MENTAL_HEALTH_WORDS = ["nutrition", "diet", "eating healthy"]
SLEEP_HYGIENE_WORDS = ["sleep hygiene", "sleep habits"]
SOCIAL_CONNECTION_WORDS = ["social", "friends", "community"]
WORKPLACE_MENTAL_HEALTH_WORDS = ["workplace", "office", "job stress"]
STUDENT_MENTAL_HEALTH_WORDS = ["student", "school", "academic stress"]
PARENTING_STRESS_WORDS = ["parenting", "parent", "raising children"]
CAREGIVER_BURDEN_WORDS = ["caregiver", "caring for", "elderly parent"]
FINANCIAL_STRESS_WORDS = ["financial", "money", "debt"]
CLIMATE_ANXIETY_WORDS = ["climate", "environment", "global warming"]
TECHNOLOGY_ADDICTION_WORDS = ["technology addiction", "phone addiction"]
GAMING_ADDICTION_WORDS = ["gaming addiction", "video games"]
INTERNET_ADDICTION_WORDS = ["internet addiction", "online addiction"]
SOCIAL_MEDIA_IMPACT_WORDS = ["social media", "facebook", "instagram"]
BODY_IMAGE_WORDS = ["body image", "appearance", "looks"]
AGING_FEARS_WORDS = ["aging fears", "fear of aging"]
EXISTENTIAL_CONCERNS_WORDS = ["existential", "meaning of life", "purpose"]
SPIRITUALITY_WORDS = ["spirituality", "spiritual", "faith"]
CREATIVITY_BLOCKS_WORDS = ["creativity", "creative block", "writer's block"]
DECISION_MAKING_WORDS = ["decision making", "choices", "hard decisions"]
PERFECTIONISM_WORDS = ["perfectionism", "perfectionist"]
PROCRASTINATION_WORDS = ["procrastination", "procrastinating"]
TIME_MANAGEMENT_WORDS = ["time management", "organizing time"]
GOAL_SETTING_WORDS = ["goal setting", "goals", "achievements"]
RESILIENCE_BUILDING_WORDS = ["resilience", "bouncing back"]
EMOTIONAL_INTELLIGENCE_WORDS = ["emotional intelligence", "emotions", "feelings"]
COMMUNICATION_SKILLS_WORDS = ["communication", "talking", "expressing"]
BOUNDARY_SETTING_WORDS = ["boundaries", "setting limits"]
FORGIVENESS_WORDS = ["forgiveness", "forgiving"]
GRATITUDE_PRACTICE_WORDS = ["gratitude", "thankful"]
MINDSET_SHIFTS_WORDS = ["mindset", "positive thinking"]
POSITIVE_AFFIRMATIONS_WORDS = ["affirmations", "positive self-talk"]
SELF_COMPASSION_WORDS = ["self-compassion", "kind to myself"]
MINDFUL_EATING_WORDS = ["mindful eating", "eating mindfully"]
NATURE_THERAPY_WORDS = ["nature therapy", "forest bathing"]
MUSIC_THERAPY_WORDS = ["music therapy", "healing music"]
ART_THERAPY_WORDS = ["art therapy", "therapeutic art"]
PET_THERAPY_WORDS = ["pet therapy", "animal therapy"]
LAUGHTER_BENEFITS_WORDS = ["laughter", "laughing"]
HUMOR_COPING_WORDS = ["humor", "jokes", "funny"]
VOLUNTEERING_WORDS = ["volunteering", "volunteer"]
ACTS_OF_KINDNESS_WORDS = ["kindness", "random acts"]
COMMUNITY_INVOLVEMENT_WORDS = ["community", "local groups"]
CULTURAL_ACTIVITIES_WORDS = ["cultural", "arts", "museums"]
LEARNING_NEW_SKILLS_WORDS = ["learning", "new skills", "education"]
TRAVEL_BENEFITS_WORDS = ["travel", "vacation"]
ADVENTURE_SEEKING_WORDS = ["adventure", "thrill seeking"]
ROUTINE_IMPORTANCE_WORDS = ["routine", "structure"]
FLEXIBILITY_BALANCE_WORDS = ["flexibility", "adaptability"]
WORK_LIFE_BALANCE_WORDS = ["work life balance", "balance"]
SELF_CARE_ROUTINES_WORDS = ["self care", "self-care"]
PERSONAL_GROWTH_WORDS = ["personal growth", "self improvement"]
LIFE_TRANSITIONS_WORDS = ["life transitions", "changes"]
RETIREMENT_PLANNING_WORDS = ["retirement", "retiring"]
EMPTY_NEST_WORDS = ["empty nest", "children leaving"]
RELATIONSHIP_CHANGES_WORDS = ["relationship changes", "divorce"]
FRIENDSHIP_DYNAMICS_WORDS = ["friendships", "friends changing"]
FAMILY_DYNAMICS_WORDS = ["family dynamics", "family issues"]
DIVORCE_RECOVERY_WORDS = ["divorce", "separation"]
DATING_ADULT_WORDS = ["dating", "dating as adult"]
SINGLE_LIFE_WORDS = ["single", "being single"]
MARRIAGE_SATISFACTION_WORDS = ["marriage", "married life"]
PARENTING_STYLES_WORDS = ["parenting styles", "how to parent"]
TEEN_MENTAL_HEALTH_WORDS = ["teen mental health", "teenage depression"]
COLLEGE_TRANSITION_WORDS = ["college", "university transition"]
CAREER_CHANGES_WORDS = ["career change", "job change"]
JOB_SEARCH_STRESS_WORDS = ["job search", "looking for job"]
LEADERSHIP_CHALLENGES_WORDS = ["leadership", "leading"]
TEAM_CONFLICTS_WORDS = ["team conflicts", "work conflicts"]
REMOTE_WORK_WORDS = ["remote work", "working from home"]
OFFICE_POLITICS_WORDS = ["office politics", "workplace politics"]
ENTREPRENEURSHIP_WORDS = ["entrepreneurship", "starting business"]
FINANCIAL_PLANNING_WORDS = ["financial planning", "budgeting"]
DEBT_MANAGEMENT_WORDS = ["debt", "loans"]
RETIREMENT_ANXIETY_WORDS = ["retirement anxiety", "fear of retirement"]
HEALTHCARE_NAVIGATION_WORDS = ["healthcare", "medical system"]
INSURANCE_UNDERSTANDING_WORDS = ["insurance", "health insurance"]
MEDICAL_APPOINTMENTS_WORDS = ["medical appointments", "doctor visits"]
HOSPITAL_STAYS_WORDS = ["hospital", "hospitalization"]
SURGERY_ANXIETY_WORDS = ["surgery", "operation"]
RECOVERY_PROCESS_WORDS = ["recovery", "healing"]
CHRONIC_CONDITION_WORDS = ["chronic condition", "long term health"]
DISABILITY_ACCOMMODATION_WORDS = ["disability accommodation", "accessibility"]
ACCESSIBLE_TECHNOLOGY_WORDS = ["accessible technology", "assistive devices"]
AGING_GRACEFULLY_WORDS = ["aging gracefully", "healthy aging"]
END_OF_LIFE_WORDS = ["end of life", "dying"]
BEREAVEMENT_SUPPORT_WORDS = ["bereavement", "grieving"]
LEGACY_BUILDING_WORDS = ["legacy", "leaving a mark"]
LIFE_PURPOSE_WORDS = ["life purpose", "meaning"]
HAPPINESS_RESEARCH_WORDS = ["happiness", "what is happiness"]
FLOW_STATES_WORDS = ["flow", "in the zone"]
OPTIMAL_EXPERIENCE_WORDS = ["optimal experience", "peak experience"]
AUTHENTIC_LIVING_WORDS = ["authentic living", "being yourself"]
MINIMALISM_BENEFITS_WORDS = ["minimalism", "simplicity"]
DECLUTTERING_WORDS = ["decluttering", "organizing"]
DIGITAL_MINIMALISM_WORDS = ["digital minimalism", "less screen time"]
SLOW_LIVING_WORDS = ["slow living", "mindful living"]
MINDFUL_CONSUMPTION_WORDS = ["mindful consumption", "conscious buying"]
SUSTAINABLE_LIVING_WORDS = ["sustainable living", "eco friendly"]
ENVIRONMENTAL_STEWARDSHIP_WORDS = ["environmental stewardship", "protecting environment"]
CLIMATE_ACTION_WORDS = ["climate action", "fighting climate change"]
SOCIAL_JUSTICE_WORDS = ["social justice", "equality"]
EQUITY_EDUCATION_WORDS = ["equity", "fairness"]
CULTURAL_COMPETENCE_WORDS = ["cultural competence", "cultural awareness"]
INCLUSION_PRACTICES_WORDS = ["inclusion", "inclusive"]
ALLYSHIP_WORDS = ["allyship", "being an ally"]
ADVOCACY_SKILLS_WORDS = ["advocacy", "speaking up"]
COMMUNITY_ORGANIZING_WORDS = ["community organizing", "grassroots"]
POLITICAL_ENGAGEMENT_WORDS = ["political engagement", "voting"]
CIVIC_PARTICIPATION_WORDS = ["civic participation", "citizenship"]
GLOBAL_CITIZENSHIP_WORDS = ["global citizenship", "world citizen"]
INTERCULTURAL_COMMUNICATION_WORDS = ["intercultural communication", "cross cultural"]
LANGUAGE_LEARNING_WORDS = ["language learning", "learning languages"]
TRAVEL_ETHICS_WORDS = ["travel ethics", "responsible travel"]
CULTURAL_EXCHANGE_WORDS = ["cultural exchange", "cultural sharing"]
WORLDVIEW_EXPANSION_WORDS = ["worldview", "broadening horizons"]
EMPATHY_DEVELOPMENT_WORDS = ["empathy", "understanding others"]
COMPASSION_FATIGUE_WORDS = ["compassion fatigue", "helper burnout"]
BURNOUT_PREVENTION_WORDS = ["burnout prevention", "preventing burnout"]
SELF_AWARENESS_WORDS = ["self awareness", "knowing yourself"]
EMOTIONAL_AWARENESS_WORDS = ["emotional awareness", "recognizing emotions"]
COGNITIVE_BIASES_WORDS = ["cognitive biases", "thinking errors"]
CRITICAL_THINKING_WORDS = ["critical thinking", "analytical thinking"]
PROBLEM_SOLVING_WORDS = ["problem solving", "solving problems"]
DECISION_MAKING_WORDS = ["decision making", "making choices"]
CONFLICT_RESOLUTION_WORDS = ["conflict resolution", "resolving disputes"]
NEGOTIATION_SKILLS_WORDS = ["negotiation", "bargaining"]
LEADERSHIP_DEVELOPMENT_WORDS = ["leadership development", "becoming a leader"]
TEAM_BUILDING_WORDS = ["team building", "building teams"]
COLLABORATION_WORDS = ["collaboration", "working together"]
INNOVATION_WORDS = ["innovation", "creativity"]
CREATIVITY_TECHNIQUES_WORDS = ["creativity techniques", "brainstorming"]
DESIGN_THINKING_WORDS = ["design thinking", "human centered design"]
SYSTEMS_THINKING_WORDS = ["systems thinking", "seeing connections"]
HOLISTIC_HEALTH_WORDS = ["holistic health", "whole person health"]
INTEGRATIVE_MEDICINE_WORDS = ["integrative medicine", "complementary medicine"]
PREVENTIVE_CARE_WORDS = ["preventive care", "preventing illness"]
HEALTH_LITERACY_WORDS = ["health literacy", "understanding health"]
PATIENT_ADVOCACY_WORDS = ["patient advocacy", "health advocacy"]
MEDICAL_ETHICS_WORDS = ["medical ethics", "health ethics"]
INFORMED_CONSENT_WORDS = ["informed consent", "consent"]
PRIVACY_RIGHTS_WORDS = ["privacy rights", "medical privacy"]
HEALTH_EQUITY_WORDS = ["health equity", "health equality"]
GLOBAL_HEALTH_WORDS = ["global health", "world health"]
PUBLIC_HEALTH_WORDS = ["public health", "population health"]
EPIDEMIC_RESPONSE_WORDS = ["epidemic", "pandemic response"]
PANDEMIC_MENTAL_HEALTH_WORDS = ["pandemic mental health", "covid mental health"]
HEALTH_CRISIS_MANAGEMENT_WORDS = ["health crisis", "crisis management"]
DISASTER_PSYCHOLOGY_WORDS = ["disaster psychology", "trauma psychology"]
TRAUMA_INFORMED_CARE_WORDS = ["trauma informed care", "trauma sensitive"]
RESILIENCE_RESEARCH_WORDS = ["resilience research", "bouncing back research"]
POST_TRAUMATIC_GROWTH_WORDS = ["post traumatic growth", "growth after trauma"]
COPING_STRATEGIES_WORDS = ["coping strategies", "coping skills"]
STRESS_MANAGEMENT_WORDS = ["stress management", "managing stress"]
ANXIETY_MANAGEMENT_WORDS = ["anxiety management", "managing anxiety"]
DEPRESSION_TREATMENT_WORDS = ["depression treatment", "treating depression"]
MOOD_DISORDER_MANAGEMENT_WORDS = ["mood disorder", "mood management"]
PERSONALITY_DISORDER_SUPPORT_WORDS = ["personality disorder", "personality issues"]
EATING_DISORDER_RECOVERY_WORDS = ["eating disorder recovery", "recovering from eating disorder"]
SUBSTANCE_USE_RECOVERY_WORDS = ["substance use recovery", "sobriety"]
GAMBLING_ADDICTION_WORDS = ["gambling addiction", "gambling problems"]
SEX_ADDICTION_WORDS = ["sex addiction", "sexual addiction"]
PROCESS_ADDICTION_WORDS = ["process addiction", "behavioral addiction"]
DUAL_DIAGNOSIS_WORDS = ["dual diagnosis", "co occurring disorders"]
CO_OCCURRING_DISORDERS_WORDS = ["co occurring", "dual disorders"]
MEDICATION_ASSISTED_TREATMENT_WORDS = ["medication assisted treatment", "mat"]
HARM_REDUCTION_WORDS = ["harm reduction", "safer use"]
RECOVERY_CAPITAL_WORDS = ["recovery capital", "recovery resources"]
RELAPSE_PREVENTION_WORDS = ["relapse prevention", "staying sober"]
SOBRIETY_CELEBRATION_WORDS = ["sobriety celebration", "milestones"]
FAMILY_RECOVERY_WORDS = ["family recovery", "family healing"]
CODEPENDENCY_WORDS = ["codependency", "codependent"]
ENABLING_BEHAVIORS_WORDS = ["enabling", "enabling behaviors"]
INTERVENTION_PLANNING_WORDS = ["intervention", "staging intervention"]
TREATMENT_MATCHING_WORDS = ["treatment matching", "right treatment"]
AFTERCARE_PLANNING_WORDS = ["aftercare", "continuing care"]
PEER_RECOVERY_COACHING_WORDS = ["peer recovery coaching", "recovery coaching"]
RECOVERY_COMMUNITIES_WORDS = ["recovery communities", "sober communities"]
SPIRITUAL_RECOVERY_WORDS = ["spiritual recovery", "spiritual healing"]
CREATIVE_RECOVERY_WORDS = ["creative recovery", "artistic healing"]
NATURE_BASED_RECOVERY_WORDS = ["nature based recovery", "outdoor recovery"]
ANIMAL_ASSISTED_RECOVERY_WORDS = ["animal assisted recovery", "pet recovery"]
ADVENTURE_THERAPY_WORDS = ["adventure therapy", "outdoor therapy"]
EQUINE_THERAPY_WORDS = ["equine therapy", "horse therapy"]
ART_THERAPY_WORDS = ["art therapy", "artistic therapy"]
MUSIC_THERAPY_WORDS = ["music therapy", "musical therapy"]
DANCE_MOVEMENT_THERAPY_WORDS = ["dance movement therapy", "movement therapy"]
DRAMA_THERAPY_WORDS = ["drama therapy", "theatrical therapy"]
PLAY_THERAPY_WORDS = ["play therapy", "therapeutic play"]
SAND_TRAY_THERAPY_WORDS = ["sand tray therapy", "sandplay"]
BIBLIOTHERAPY_WORDS = ["bibliotherapy", "reading therapy"]
JOURNALING_THERAPY_WORDS = ["journaling therapy", "writing therapy"]
MINDFULNESS_BASED_THERAPY_WORDS = ["mindfulness based therapy", "mindfulness therapy"]
ACCEPTANCE_COMMITMENT_THERAPY_WORDS = ["acceptance commitment therapy", "act"]
DIALECTICAL_BEHAVIOR_THERAPY_WORDS = ["dialectical behavior therapy", "dbt"]
COGNITIVE_BEHAVIORAL_THERAPY_WORDS = ["cognitive behavioral therapy", "cbt"]
PSYCHODYNAMIC_THERAPY_WORDS = ["psychodynamic therapy", "psychoanalytic"]
HUMANISTIC_THERAPY_WORDS = ["humanistic therapy", "person centered"]
EXISTENTIAL_THERAPY_WORDS = ["existential therapy", "existential psychotherapy"]
FAMILY_THERAPY_WORDS = ["family therapy", "family counseling"]
COUPLES_THERAPY_WORDS = ["couples therapy", "marriage counseling"]
GROUP_THERAPY_WORDS = ["group therapy", "group counseling"]
SUPPORT_GROUPS_WORDS = ["support groups", "self help groups"]
ONLINE_THERAPY_WORDS = ["online therapy", "teletherapy"]
TELETHERAPY_WORDS = ["teletherapy", "remote therapy"]
APP_BASED_THERAPY_WORDS = ["app based therapy", "therapy apps"]
SELF_HELP_RESOURCES_WORDS = ["self help", "self help books"]
PSYCHOEDUCATION_WORDS = ["psychoeducation", "mental health education"]
WELLNESS_PLANNING_WORDS = ["wellness planning", "wellness plan"]
RECOVERY_PLANNING_WORDS = ["recovery planning", "recovery plan"]
SAFETY_PLANNING_WORDS = ["safety planning", "crisis plan"]
CRISIS_PLANNING_WORDS = ["crisis planning", "emergency plan"]
ADVANCE_DIRECTIVES_WORDS = ["advance directives", "living will"]
POWER_OF_ATTORNEY_WORDS = ["power of attorney", "medical poa"]
GUARDIANSHIP_WORDS = ["guardianship", "legal guardianship"]
CIVIL_COMMITMENT_WORDS = ["civil commitment", "involuntary commitment"]
INVOLUNTARY_TREATMENT_WORDS = ["involuntary treatment", "forced treatment"]
PATIENT_RIGHTS_WORDS = ["patient rights", "mental health rights"]
MENTAL_HEALTH_LAWS_WORDS = ["mental health laws", "psychiatric laws"]
DISCRIMINATION_PROTECTION_WORDS = ["discrimination protection", "anti discrimination"]
WORKPLACE_ACCOMMODATION_WORDS = ["workplace accommodation", "job accommodation"]
REASONABLE_ACCOMMODATION_WORDS = ["reasonable accommodation", "ada accommodation"]
DISCLOSURE_DECISIONS_WORDS = ["disclosure decisions", "when to tell"]
MENTAL_HEALTH_WORKPLACE_WORDS = ["mental health workplace", "office mental health"]
EMPLOYEE_ASSISTANCE_WORDS = ["employee assistance", "eap"]
WORKPLACE_WELLNESS_WORDS = ["workplace wellness", "corporate wellness"]
LEADERSHIP_MENTAL_HEALTH_WORDS = ["leadership mental health", "managerial mental health"]
TOXIC_WORKPLACES_WORDS = ["toxic workplaces", "bad work environments"]
WORKPLACE_BULLYING_WORDS = ["workplace bullying", "office bullying"]
HARASSMENT_PREVENTION_WORDS = ["harassment prevention", "anti harassment"]
DIVERSITY_INCLUSION_WORDS = ["diversity inclusion", "dei"]
CULTURAL_COMPETENCY_WORDS = ["cultural competency", "cultural competence"]
TRAUMA_CULTURAL_WORDS = ["cultural trauma", "historical trauma"]
INDIGENOUS_MENTAL_HEALTH_WORDS = ["indigenous mental health", "native mental health"]
RACIAL_TRAUMA_WORDS = ["racial trauma", "racism trauma"]
IMMIGRANT_MENTAL_HEALTH_WORDS = ["immigrant mental health", "migration mental health"]
REFUGEE_MENTAL_HEALTH_WORDS = ["refugee mental health", "asylum seeker mental health"]
LGBTQ_MENTAL_HEALTH_WORDS = ["lgbtq mental health", "queer mental health"]
GENDER_AFFIRMING_CARE_WORDS = ["gender affirming care", "transgender care"]
TRANSGENDER_MENTAL_HEALTH_WORDS = ["transgender mental health", "trans mental health"]
NON_BINARY_SUPPORT_WORDS = ["non binary support", "enby support"]
WOMEN_MENTAL_HEALTH_WORDS = ["women mental health", "female mental health"]
MEN_MENTAL_HEALTH_WORDS = ["men mental health", "male mental health"]
OLDER_ADULT_MENTAL_HEALTH_WORDS = ["older adult mental health", "senior mental health"]
GERIATRIC_PSYCHIATRY_WORDS = ["geriatric psychiatry", "elder psychiatry"]
DEMENTIA_CARE_WORDS = ["dementia care", "alzheimer care"]
ALZHEIMER_SUPPORT_WORDS = ["alzheimer support", "dementia support"]
NEUROCOGNITIVE_DISORDERS_WORDS = ["neurocognitive disorders", "cognitive disorders"]
DEVELOPMENTAL_DISABILITIES_WORDS = ["developmental disabilities", "developmental disorders"]
INTELLECTUAL_DISABILITY_WORDS = ["intellectual disability", "cognitive disability"]
AUTISM_SPECTRUM_WORDS = ["autism spectrum", "asd"]
ADHD_ADULT_WORDS = ["adult adhd", "adhd adult"]
LEARNING_DISABILITIES_WORDS = ["learning disabilities", "learning disorders"]
NEUROLOGICAL_DISORDERS_WORDS = ["neurological disorders", "brain disorders"]
EPILEPSY_MENTAL_HEALTH_WORDS = ["epilepsy mental health", "seizure mental health"]
MULTIPLE_SCLEROSIS_WORDS = ["multiple sclerosis", "ms"]
PARKINSON_DISEASE_WORDS = ["parkinson disease", "parkinson"]
STROKE_RECOVERY_WORDS = ["stroke recovery", "stroke rehabilitation"]
BRAIN_INJURY_WORDS = ["brain injury", "tbi"]
SPINAL_CORD_INJURY_WORDS = ["spinal cord injury", "sci"]
CHRONIC_ILLNESS_PSYCHOLOGY_WORDS = ["chronic illness psychology", "chronic disease psychology"]
PAIN_MANAGEMENT_WORDS = ["pain management", "chronic pain management"]
PALLIATIVE_CARE_WORDS = ["palliative care", "comfort care"]
HOSPICE_CARE_WORDS = ["hospice care", "end of life care"]
GRIEF_COUNSELING_WORDS = ["grief counseling", "bereavement counseling"]
COMPLICATED_GRIEF_WORDS = ["complicated grief", "prolonged grief"]
BEREAVEMENT_GROUPS_WORDS = ["bereavement groups", "grief groups"]
ANTICIPATORY_GRIEF_WORDS = ["anticipatory grief", "preparatory grief"]
AMBIGUOUS_LOSS_WORDS = ["ambiguous loss", "unclear loss"]
DISENFRANCHISED_GRIEF_WORDS = ["disenfranchised grief", "unacknowledged grief"]
COLLECTIVE_TRAUMA_WORDS = ["collective trauma", "community trauma"]
HISTORICAL_TRAUMA_WORDS = ["historical trauma", "generational trauma"]
INTERGENERATIONAL_TRAUMA_WORDS = ["intergenerational trauma", "ancestral trauma"]
EPIGENETICS_MENTAL_HEALTH_WORDS = ["epigenetics mental health", "gene environment"]
NEUROSCIENCE_MENTAL_HEALTH_WORDS = ["neuroscience mental health", "brain mental health"]
PSYCHONEUROIMMUNOLOGY_WORDS = ["psychoneuroimmunology", "pni"]
BIOFEEDBACK_WORDS = ["biofeedback", "biological feedback"]
NEUROFEEDBACK_WORDS = ["neurofeedback", "eeg biofeedback"]
LIGHT_THERAPY_WORDS = ["light therapy", "bright light therapy"]
SLEEP_RESTRICTION_WORDS = ["sleep restriction", "sleep restriction therapy"]
CHRONOTHERAPY_WORDS = ["chronotherapy", "circadian therapy"]
EXERCISE_THERAPY_WORDS = ["exercise therapy", "physical activity therapy"]
NUTRITION_PSYCHIATRY_WORDS = ["nutrition psychiatry", "food psychiatry"]
GUT_BRAIN_AXIS_WORDS = ["gut brain axis", "microbiome gut brain"]
MICROBIOME_MENTAL_HEALTH_WORDS = ["microbiome mental health", "gut flora mental health"]
HORMONE_MENTAL_HEALTH_WORDS = ["hormone mental health", "endocrine mental health"]
ENDOCRINE_MENTAL_HEALTH_WORDS = ["endocrine mental health", "hormonal mental health"]
REPRODUCTIVE_MENTAL_HEALTH_WORDS = ["reproductive mental health", "fertility mental health"]
PERINATAL_MENTAL_HEALTH_WORDS = ["perinatal mental health", "pregnancy mental health"]
MATERNAL_MENTAL_HEALTH_WORDS = ["maternal mental health", "mother mental health"]
PATERNAL_MENTAL_HEALTH_WORDS = ["paternal mental health", "father mental health"]
INFANT_MENTAL_HEALTH_WORDS = ["infant mental health", "baby mental health"]
CHILD_PSYCHIATRY_WORDS = ["child psychiatry", "pediatric psychiatry"]
ADOLESCENT_PSYCHIATRY_WORDS = ["adolescent psychiatry", "teen psychiatry"]
FAMILY_BASED_TREATMENT_WORDS = ["family based treatment", "family therapy"]
MULTISYSTEMIC_THERAPY_WORDS = ["multisystemic therapy", "mst"]
WRAPAROUND_SERVICES_WORDS = ["wraparound services", "comprehensive services"]
CASE_MANAGEMENT_WORDS = ["case management", "care coordination"]
PEER_SPECIALISTS_WORDS = ["peer specialists", "peer support specialists"]
RECOVERY_COACHES_WORDS = ["recovery coaches", "wellness coaches"]
NAVIGATORS_WORDS = ["navigators", "patient navigators"]
COMMUNITY_HEALTH_WORKERS_WORDS = ["community health workers", "chw"]
HEALTH_EDUCATORS_WORDS = ["health educators", "health education"]
PREVENTION_SPECIALISTS_WORDS = ["prevention specialists", "prevention workers"]
CRISIS_INTERVENTION_WORDS = ["crisis intervention", "crisis response"]
MOBILE_CRISIS_WORDS = ["mobile crisis", "crisis teams"]
CRISIS_STABILIZATION_WORDS = ["crisis stabilization", "stabilization"]
RESPITE_CARE_WORDS = ["respite care", "relief care"]
ADULT_DAY_CARE_WORDS = ["adult day care", "day programs"]
ASSISTED_LIVING_WORDS = ["assisted living", "senior living"]
SKILLED_NURSING_WORDS = ["skilled nursing", "nursing home"]
LONG_TERM_CARE_WORDS = ["long term care", "ltc"]
HOME_HEALTH_CARE_WORDS = ["home health care", "home care"]
TELEHEALTH_SERVICES_WORDS = ["telehealth services", "remote health"]
DIGITAL_HEALTH_WORDS = ["digital health", "e health"]
AI_MENTAL_HEALTH_WORDS = ["ai mental health", "artificial intelligence therapy"]
VIRTUAL_REALITY_THERAPY_WORDS = ["virtual reality therapy", "vr therapy"]
GAMIFICATION_HEALTH_WORDS = ["gamification health", "game based health"]
WEARABLE_TECHNOLOGY_WORDS = ["wearable technology", "fitness trackers"]
DIGITAL_PHENOTYPING_WORDS = ["digital phenotyping", "behavioral sensing"]
PRECISION_MEDICINE_WORDS = ["precision medicine", "personalized medicine"]
PHARMACOGENOMICS_WORDS = ["pharmacogenomics", "personalized medication"]

# Professor-specific keywords
ACADEMIC_STRESS_WORDS = ["grading", "papers", "deadlines", "tenure", "publish", "research", "students", "committee", "teaching", "lectures", "exams", "syllabus"]
WORK_LIFE_WORDS = ["work-life", "balance", "overwhelmed", "burnout", "exhausted", "time management"]
PROFESSIONAL_WORDS = ["career", "promotion", "review", "evaluation", "colleagues", "department"]

def get_crisis_support_response(text):
    """Provide supportive crisis response with tips and suggestions to help users come out of crisis thoughts"""
    text_lower = text.lower()

    # Determine the type of crisis based on keywords
    crisis_type = None
    if any(word in text_lower for word in CRISIS_WORDS["suicide"]):
        crisis_type = "suicidal"
    elif any(word in text_lower for word in CRISIS_WORDS["self_harm"]):
        crisis_type = "self_harm"
    elif any(word in text_lower for word in CRISIS_WORDS["severe_depression"]):
        crisis_type = "severe_depression"
    elif any(word in text_lower for word in CRISIS_WORDS["mental_crisis"]):
        crisis_type = "mental_crisis"
    elif any(word in text_lower for word in CRISIS_WORDS["trauma_abuse"]):
        crisis_type = "trauma"
    elif any(word in text_lower for word in CRISIS_WORDS["addiction"]):
        crisis_type = "addiction"
    else:
        crisis_type = "general_crisis"

    # Base response with immediate help resources
    response = "I'm really concerned about what you're going through, and I want you to know you're not alone. Please reach out immediately to:\n\n"
    response += "**🚨 Emergency Services (India):**\n"
    response += "• **Police**: Call 100\n"
    response += "• **Ambulance/Medical Emergency**: Call 108 or 112\n"
    response += "• **Fire**: Call 101\n\n"
    response += "**🆘 Mental Health Crisis Helplines (India):**\n"
    response += "• **AASRA (Mumbai)**: 9820466726 (24/7)\n"
    response += "• **Sneha India Foundation (Chennai)**: 044-24640050 (24/7)\n"
    response += "• **Vandrevala Foundation**: 1860 266 2345 (24/7)\n"
    response += "• **1Life (Youth Mental Health)**: 78930 78930 (24/7)\n"
    response += "• **Trusted person**: Call a friend, family member, or mental health professional\n\n"

    # Specific tips and suggestions based on crisis type
    if crisis_type == "suicidal":
        response += "**While waiting for help, here are some immediate steps that might help:**\n\n"
        response += "• **Ground yourself in the present**: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste\n"
        response += "• **Remove immediate dangers**: Put away anything that could cause harm\n"
        response += "• **Connect with others**: Even a brief conversation can help - call someone you trust\n"
        response += "• **Remember this passes**: These feelings are intense but they won't last forever\n"
        response += "• **Hold on**: You matter, and help is available right now\n\n"

    elif crisis_type == "self_harm":
        response += "**While getting professional help, consider these coping strategies:**\n\n"
        response += "• **Delay the urge**: Wait 15 minutes - use a timer, do something else\n"
        response += "• **Physical alternatives**: Hold ice cubes, snap a rubber band on your wrist, take a cold shower\n"
        response += "• **Express emotions safely**: Draw, write, scream into a pillow, punch a cushion\n"
        response += "• **Distract yourself**: Call a friend, watch a favorite show, go for a walk\n"
        response += "• **Self-soothe**: Wrap yourself in a blanket, drink something warm, listen to comforting music\n\n"

    elif crisis_type == "severe_depression":
        response += "**Ways to cope while working toward recovery:**\n\n"
        response += "• **Start very small**: One tiny step at a time - make your bed, brush your teeth\n"
        response += "• **Connect with others**: Even brief interactions matter - text a friend\n"
        response += "• **Move your body**: A short walk or stretching can release endorphins\n"
        response += "• **Practice self-compassion**: Treat yourself like you would a dear friend\n"
        response += "• **Seek light and nature**: Open curtains, step outside, get some sunlight\n\n"

    elif crisis_type == "mental_crisis":
        response += "**Strategies to help stabilize in a crisis:**\n\n"
        response += "• **Breathe deeply**: 4 counts in, hold 4, 6 counts out - repeat several times\n"
        response += "• **Ground yourself**: Use the 5-4-3-2-1 technique (senses)\n"
        response += "• **Step away**: Remove yourself from overwhelming situations if possible\n"
        response += "• **Reach out**: Talk to someone safe about what's happening\n"
        response += "• **Wait it out**: Intense feelings usually pass, even if it doesn't feel like it\n\n"

    elif crisis_type == "trauma":
        response += "**Support for trauma-related crisis:**\n\n"
        response += "• **Find a safe space**: Go somewhere you feel secure\n"
        response += "• **Use grounding techniques**: Focus on your breath or physical sensations\n"
        response += "• **Reach out to support**: Contact a trauma-informed counselor or hotline\n"
        response += "• **Practice self-care**: Rest, eat, hydrate - basic needs matter\n"
        response += "• **Remember you're safe now**: The trauma is in the past\n\n"

    elif crisis_type == "addiction":
        response += "**Support for addiction crisis:**\n\n"
        response += "• **Contact support immediately**: Call SAMHSA helpline at 1-800-662-HELP\n"
        response += "• **Remove triggers**: Step away from substances or situations\n"
        response += "• **Use coping skills**: Deep breathing, distraction techniques\n"
        response += "• **Reach out to sober support**: Call a sponsor or support group member\n"
        response += "• **Focus on one hour at a time**: Take it moment by moment\n\n"

    else:  # general crisis
        response += "**Immediate coping strategies:**\n\n"
        response += "• **Breathe**: Slow, deep breaths to calm your nervous system\n"
        response += "• **Ground yourself**: Notice your surroundings and physical sensations\n"
        response += "• **Connect**: Reach out to someone you trust\n"
        response += "• **Move**: Physical activity can help process intense emotions\n"
        response += "• **Wait**: Intense feelings typically pass with time\n\n"

    response += "**Remember**: These are temporary measures while you get professional help. You're taking an important step by reaching out, and help is available. You don't have to go through this alone."

    return response

# Intent-based responses for common health and wellbeing concerns
INTENT_RESPONSES = {
    "stress": "Stress can feel overwhelming. Taking short breaks, deep breathing, or talking about what's bothering you can help.",

    "anxiety": "Feeling anxious is common. Let's slow things down. Would you like to try a breathing exercise?",

    "sadness": "I'm sorry you're feeling low. You're not alone. Talking about your feelings can sometimes help.",

    "fatigue": "Feeling tired often comes from stress or poor rest. Try gentle movement, hydration, and proper sleep.",

    "sleep_issue": "Sleep problems are common when stress levels are high. A calm routine before bed can help.",

    "burnout": "Burnout happens when we push ourselves too hard. Rest and small boundaries are important.",

    "headache": "Headaches can come from stress, dehydration, poor posture, or screen fatigue. If headaches are frequent or severe, consult a healthcare professional.",

    "body_pain": "Long sitting hours can cause body pain. Stretching and posture changes can help reduce discomfort.",

    "lifestyle": "Small lifestyle changes like regular meals, sleep, and movement can improve wellbeing.",

    "hydration": "Staying hydrated supports energy and focus. Try keeping a water bottle nearby.",

    "screen_fatigue": "Too much screen time can strain your eyes. Follow the 20-20-20 rule to reduce strain.",

    "motivation": "Lack of motivation happens sometimes. Start with small achievable goals.",

    # Additional health-related responses from my knowledge
    "depression": "Depression can make everything feel heavy. Small steps like connecting with others or gentle activities can help. Professional support is valuable too.",

    "panic_attack": "Panic attacks can be frightening. Focus on your breathing - inhale for 4 counts, hold for 4, exhale for 4. You're safe, and this will pass.",

    "loneliness": "Feeling lonely is a valid experience. Consider reaching out to a friend, joining a community, or practicing self-compassion. You're not alone in this.",

    "overeating": "Emotional eating is common when stressed. Try mindful eating - pause before eating and ask if you're truly hungry. Be kind to yourself.",

    "insomnia": "Insomnia can be frustrating. Create a calming bedtime routine, avoid screens before bed, and try relaxation techniques. Consistent sleep hygiene helps.",

    "digestive_issues": "Digestive discomfort can be stress-related. Eat slowly, stay hydrated, and consider gentle walks after meals. Probiotics and fiber-rich foods may help.",

    "back_pain": "Back pain affects many people. Check your posture, take regular breaks to stretch, and consider strengthening core muscles. Consult a professional if persistent.",

    "neck_pain": "Neck tension often comes from poor posture or stress. Gentle neck rolls, shoulder shrugs, and proper screen positioning can help relieve discomfort.",

    "eye_strain": "Eye strain from screens is common. Remember the 20-20-20 rule: every 20 minutes, look 20 feet away for 20 seconds. Proper lighting helps too.",

    "concentration": "Difficulty concentrating can stem from stress, fatigue, or distractions. Try the Pomodoro technique: 25 minutes focused work, then a 5-minute break.",

    "memory_issues": "Memory lapses happen to everyone, especially when stressed. Good sleep, regular exercise, and stress management can improve cognitive function.",

    "irritability": "Feeling irritable is often a sign of underlying stress or fatigue. Adequate rest, healthy eating, and stress-relief techniques can help stabilize mood.",

    "social_anxiety": "Social anxiety can make interactions challenging. Start with small, low-pressure social activities. Breathing exercises can help in the moment.",

    "relationship_issues": "Relationship challenges can be stressful. Open communication, setting boundaries, and self-reflection are important. Professional counseling can help.",

    "grief": "Grieving is a natural process that takes time. Allow yourself to feel your emotions. Connecting with supportive people and self-care are important.",

    "addiction": "Struggling with addiction is challenging. Recovery is possible with support. Consider reaching out to professionals or support groups. You're taking a brave step.",

    "eating_disorder": "Eating disorders are serious but treatable. Recovery involves professional help, supportive relationships, and gentle self-compassion. You're not alone.",

    "self_harm": "If you're hurting yourself, please know help is available. Reach out to a crisis hotline, trusted person, or mental health professional immediately.",

    "suicidal_thoughts": "I'm really concerned about you. Please reach out to emergency services (911) or the National Suicide Prevention Lifeline (988) right now. You matter.",

    "trauma": "Trauma can have lasting effects. Healing takes time and professional support. Therapy modalities like EMDR or CBT can be very helpful.",

    "ptsd": "PTSD symptoms can be managed with professional help. Therapies like trauma-focused CBT and grounding techniques can support recovery.",

    "ocd": "OCD involves unwanted thoughts and repetitive behaviors. Exposure therapy and medication can be effective treatments. Professional diagnosis is important.",

    "bipolar": "Bipolar disorder involves mood swings. Mood stabilizers, therapy, and lifestyle management are key. Working with mental health professionals is crucial.",

    "adhd": "ADHD affects focus and impulsivity. Medication, behavioral therapy, and organizational strategies can help. Finding the right support system matters.",

    "autism": "Autism is a neurodevelopmental difference. Support includes understanding your needs, building on strengths, and finding accommodating environments.",

    "chronic_illness": "Living with chronic illness requires self-compassion. Building a support network, pacing yourself, and communicating your needs are important strategies.",

    "disability": "Living with a disability takes strength. Focus on what you can do, advocate for accommodations, and connect with supportive communities.",

    "aging_concerns": "Aging brings changes and wisdom. Stay active, maintain social connections, and focus on meaningful activities. Regular health check-ups are important.",

    "menopause": "Menopause involves hormonal changes. Hot flashes, mood changes, and sleep issues are common. Hormone therapy and lifestyle changes can help.",

    "pregnancy": "Pregnancy brings physical and emotional changes. Prenatal care, stress management, and support systems are important. Listen to your body's needs.",

    "postpartum": "Postpartum adjustment can be challenging. Baby blues are common, but postpartum depression needs professional attention. Rest and support are crucial.",

    "infertility": "Infertility can be emotionally challenging. Consider counseling, support groups, and exploring all options. Your feelings are valid.",

    "chronic_pain": "Chronic pain management involves multiple approaches. Physical therapy, medication, mindfulness, and lifestyle adjustments can help improve quality of life.",

    "arthritis": "Arthritis affects joints and mobility. Exercise, weight management, and anti-inflammatory foods can help. Consult rheumatologists for treatment options.",

    "diabetes": "Diabetes management involves blood sugar monitoring, healthy eating, and regular exercise. Working with healthcare providers ensures optimal control.",

    "heart_health": "Heart health involves diet, exercise, and stress management. Regular check-ups, healthy cholesterol levels, and blood pressure monitoring are important.",

    "cancer_support": "Cancer diagnosis brings many emotions. Treatment plans, support groups, and self-care are important. You're not alone in this journey.",

    "weight_concerns": "Body image and weight concerns affect many people. Focus on health rather than appearance. Intuitive eating and body acceptance are helpful approaches.",

    "allergy": "Allergies can impact quality of life. Identifying triggers, carrying medications, and working with allergists help manage symptoms effectively.",

    "asthma": "Asthma requires trigger avoidance and rescue inhaler use. Regular check-ups and action plans help maintain control and prevent attacks.",

    "thyroid": "Thyroid issues affect energy and mood. Medication management and regular monitoring are important. Symptoms vary by thyroid condition.",

    "hormonal_imbalance": "Hormonal changes affect many aspects of health. Blood tests, lifestyle changes, and medical treatment can restore balance.",

    "immune_system": "Strong immunity comes from sleep, nutrition, stress management, and regular exercise. Listen to your body when you need rest.",

    "detox_cleansing": "The body naturally detoxifies. Focus on whole foods, hydration, and healthy lifestyle rather than extreme cleanses. Sustainable habits matter.",

    "supplements": "Supplements can support health but aren't substitutes for balanced nutrition. Consult healthcare providers before starting new supplements.",

    "vaccination": "Vaccinations protect individual and community health. Discuss concerns with healthcare providers to make informed decisions.",

    "mental_health_stigma": "Mental health stigma prevents many from seeking help. Education and open conversations help reduce stigma. Your mental health matters.",

    "therapy_options": "Therapy comes in many forms:\n• CBT (Cognitive Behavioral Therapy)\n• DBT (Dialectical Behavior Therapy)\n• Psychodynamic therapy\n• Group therapy\n\nFinding the right therapeutic approach takes time and patience.",

    "medication_concerns": "Mental health medications can be helpful but have side effects.\n\nImportant considerations:\n• Work closely with prescribers\n• Monitor how you feel and report side effects",

    "emergency_mental_health": "Mental health crises need immediate attention.\n\nAvailable urgent support:\n• Crisis hotlines\n• Emergency rooms\n• Mobile crisis teams",

    "peer_support": "Peer support connects you with others who've had similar experiences.\n\nBenefits include:\n• Shared understanding\n• Practical tips from lived experience",

    "mindfulness_practice": "Mindfulness involves present-moment awareness.\n\nGetting started:\n• Start with short daily practices\n• Use apps and guided meditations for beginners",

    "yoga_benefits": "Yoga combines movement, breathing, and mindfulness.\n\nTips:\n• Different styles suit different needs\n• Start gently and listen to your body",

    "meditation_types": "Meditation includes various types:\n• Mindfulness meditation\n• Transcendental meditation\n• Guided meditation\n• Loving-kindness meditation\n\nExperiment to find what resonates with you.",

    "exercise_motivation": "Exercise benefits mental health.\n\nTips to get started:\n• Start small - even 10-minute walks help\n• Find activities you enjoy for sustainability",

    "nutrition_mental_health": "Nutrition affects mood and brain function.\n\nKey nutrients that support mental wellbeing:\n• Omega-3s\n• B vitamins\n• Complex carbs",

    "sleep_hygiene": "Good sleep hygiene includes:\n• Consistent schedules\n• Cool, dark rooms\n• Limiting screens before bed\n\nQuality sleep supports mental health.",

    "social_connection": "Social connections are vital for mental health. Even small interactions matter. Online communities can supplement in-person connections.",

    "workplace_mental_health": "Workplace stress affects many. Set boundaries, take breaks, and use employee assistance programs when available.",

    "student_mental_health": "Academic pressure affects students. Time management, self-care, and campus counseling services are important resources.",

    "parenting_stress": "Parenting brings joy and challenges. Self-care, support networks, and realistic expectations help manage stress.",

    "caregiver_burden": "Caring for others can be rewarding but draining. Set boundaries, ask for help, and prioritize your wellbeing too.",

    "political_stress": "Political events can be stressful. Limit news exposure, focus on local actions, and maintain perspective.",

    "financial_stress": "Financial worries affect mental health. Budgeting, seeking advice, and focusing on what you can control help reduce anxiety.",

    "climate_anxiety": "Climate concerns cause real anxiety. Channel energy into sustainable actions, connect with others, and practice self-care.",

    "technology_addiction": "Technology overuse affects sleep and relationships. Set device boundaries and create tech-free zones.",

    "gaming_addiction": "Gaming addiction can impact daily life. Balance gaming with other activities and seek help if it interferes with responsibilities.",

    "internet_addiction": "Internet addiction affects many. Set boundaries, develop offline interests, and seek professional support.",

    "social_media_impact": "Social media affects mental health variably. Curate your feed, limit time, and compare yourself less to highlight reels.",

    "body_image": "Body image concerns are common. Practice body neutrality, challenge media messages, and focus on body functionality.",

    "aging_fears": "Aging brings changes but also wisdom. Focus on healthy aging through lifestyle choices and maintaining social connections.",

    "existential_concerns": "Questions about meaning and purpose are normal. Explore through reading, conversations, and personal reflection.",

    "spirituality": "Spirituality can provide comfort and meaning. Explore practices that resonate with you, whether religious or secular.",

    "creativity_blocks": "Creative blocks happen to everyone. Try changing environments, free writing, or walking to spark inspiration.",

    "decision_making": "Big decisions cause stress. Break them down, gather information, trust your intuition, and remember you can change course.",

    "perfectionism": "Perfectionism creates stress. Practice 'good enough' standards, celebrate progress, and learn from mistakes.",

    "procrastination": "Procrastination often stems from fear or overwhelm. Break tasks into small steps and start with the easiest part.",

    "time_management": "Effective time management reduces stress. Prioritize tasks, use calendars, and build in buffer time for unexpected events.",

    "goal_setting": "SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound) help turn aspirations into achievements.",

    "resilience_building": "Resilience grows through challenges. Practice self-compassion, maintain routines, and seek support during difficult times.",

    "emotional_intelligence": "Emotional intelligence involves recognizing and managing emotions. Practice mindfulness and self-reflection to develop this skill.",

    "communication_skills": "Clear communication reduces misunderstandings. Practice active listening, express needs directly, and stay calm during conflicts.",

    "boundary_setting": "Healthy boundaries protect your energy. Learn to say no, communicate limits clearly, and enforce consequences consistently.",

    "forgiveness": "Forgiveness frees you from past hurts. It doesn't excuse harm but releases you from carrying resentment's burden.",

    "gratitude_practice": "Gratitude shifts focus to positives. Try daily gratitude journaling or sharing appreciations with others.",

    "mindset_shifts": "Growth mindset sees challenges as learning opportunities. Fixed mindset believes abilities are innate. Choose growth for resilience.",

    "positive_affirmations": "Positive affirmations rewire thought patterns. Use present tense, be specific, and repeat regularly for best effect.",

    "self_compassion": "Self-compassion treats yourself with the same kindness you'd offer a friend. Practice during difficult moments.",

    "mindful_eating": "Mindful eating involves eating without distraction, savoring each bite, and listening to hunger/fullness cues.",

    "nature_therapy": "Nature exposure reduces stress and improves mood. Even brief time outdoors or viewing nature scenes helps.",

    "music_therapy": "Music affects emotions powerfully. Create playlists for different moods and use music for stress relief or motivation.",

    "art_therapy": "Art expresses emotions non-verbally. Drawing, painting, or crafting can process feelings and reduce stress.",

    "pet_therapy": "Pets provide companionship and stress relief. Animal interactions can lower blood pressure and increase oxytocin.",

    "laughter_benefits": "Laughter reduces stress hormones and boosts mood. Watch comedies, share jokes, or practice laughter yoga.",

    "humor_coping": "Humor helps cope with stress. Find appropriate humor in situations and use it to gain perspective.",

    "volunteering": "Helping others boosts wellbeing. Find causes you care about and volunteer time or skills regularly.",

    "acts_of_kindness": "Performing kind acts increases happiness. Small gestures like compliments or helping neighbors create positive ripples.",

    "random_acts_kindness": "Random acts of kindness surprise and delight. Pay for someone's coffee, leave encouraging notes, or help strangers.",

    "community_involvement": "Community involvement creates belonging. Join local groups, attend events, or participate in neighborhood activities.",

    "cultural_activities": "Cultural activities enrich life. Attend concerts, museums, theater, or festivals to broaden perspectives and enjoy beauty.",

    "learning_new_skills": "Learning keeps minds sharp and builds confidence. Try new hobbies, languages, or skills that interest you.",

    "travel_benefits": "Travel broadens perspectives and creates memories. Even local exploration can provide adventure and stress relief.",

    "adventure_seeking": "Healthy risks build confidence. Try new activities that push comfort zones safely and gradually.",

    "routine_importance": "Routines provide stability during chaos. Include sleep, meals, exercise, and relaxation in daily schedules.",

    "flexibility_balance": "Balance routine with flexibility. Life brings changes, so adapt while maintaining core healthy habits.",

    "self_care_routines": "Self-care routines recharge you. Include activities you enjoy that restore energy and bring joy.",

    "personal_growth": "Personal growth is lifelong. Set goals, seek feedback, learn from experiences, and celebrate progress.",

    "life_transitions": "Life transitions bring uncertainty. Accept change, seek support, and focus on what you can control.",

    "retirement_planning": "Retirement planning includes financial and lifestyle preparation. Consider interests, social connections, and purpose beyond work.",

    "empty_nest": "Empty nest brings mixed emotions. Rediscover personal interests, strengthen relationships, and find new purposes.",

    "relationship_changes": "Relationships evolve over time. Communicate openly, adapt to changes, and seek counseling if needed.",

    "friendship_dynamics": "Friendships change with life stages. Nurture meaningful connections and accept natural evolution of relationships.",

    "family_dynamics": "Family relationships can be complex. Set boundaries, practice forgiveness, and focus on healthy patterns.",

    "divorce_recovery": "Divorce brings grief and change. Allow healing time, build support networks, and focus on personal growth.",

    "dating_adult": "Adult dating differs from youth. Be authentic, communicate needs clearly, and take time to know partners.",

    "single_life": "Single life offers freedom and self-discovery. Build fulfilling social networks and pursue personal goals.",

    "marriage_satisfaction": "Healthy marriages require effort. Practice appreciation, communicate needs, and seek couples counseling when needed.",

    "parenting_styles": "Different parenting approaches work for different families. Focus on love, boundaries, and age-appropriate expectations.",

    "teen_mental_health": "Teen mental health involves identity formation and peer pressure. Open communication and professional support help.",

    "college_transition": "College brings independence and challenges. Build support systems, manage time well, and seek campus resources.",

    "career_changes": "Career changes can be daunting but rewarding. Assess skills, explore options, and seek career counseling.",
}


def generate_response(username, text, db, target_lang=None):
    text_l = text.lower()

    # Get user's language preference and latest mood
    user = db.query(User).filter(User.username == username).first()
    if user:
        today = date.today()
        mood_record = db.query(MoodLog).filter(
            MoodLog.user_id == user.id,
            MoodLog.log_date == today
        ).first()
        current_mood = mood_record.mood if mood_record else None
        user_lang = user.language if user.language else 'en'
    else:
        current_mood = None
        user_lang = 'en'

    # Use provided target_lang or user's preference
    target_language = target_lang if target_lang else user_lang

    if any(word in text_l for word in ALL_CRISIS_WORDS):
        return get_crisis_support_response(text)

    # Check for greetings
    greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings", "howdy", "sup", "yo"]
    if any(word in text_l for word in greeting_words) and len(text.split()) <= 3:
        greeting_responses = [
            "Hi there! How's your day going?",
            "Hello! It's great to hear from you. What's new?",
            "Hey! How are you feeling today?",
            "Hi! I'm here whenever you need to talk. How's everything?"
        ]
        response = greeting_responses[len(text) % len(greeting_responses)]

        # Save to database
        if user:
            chat_entry = ChatHistory(
                user_id=user.id,
                user_message=text,
                bot_response=response
            )
            db.add(chat_entry)
            db.commit()

        return response

    # Check for daily routine questions
    routine_words = ["daily routine", "your day", "how is your day", "what's your routine", "tell me about your day", "how was your day", "what do you do daily", "your daily life"]
    if any(phrase in text_l for phrase in routine_words):
        routine_responses = [
            "My day usually involves helping people like you with wellbeing support, learning about health topics, and being here whenever someone needs to talk. How about you - what's been happening in your daily routine lately?",
            "As an AI wellbeing companion, my 'routine' is being available 24/7 to listen and support. I spend my time learning about mental health, wellness practices, and how to best help people. What's a typical day like for you?",
            "I don't have a traditional daily routine like humans do, but I'm always here to chat about wellbeing, share exercises, and provide support. What does your daily routine look like these days?",
            "My purpose is to support wellbeing, so my 'day' is filled with conversations like this one. I love hearing about people's daily lives - what's been going on with you?"
        ]
        response = routine_responses[len(text) % len(routine_responses)]

        # Save to database
        if user:
            chat_entry = ChatHistory(
                user_id=user.id,
                user_message=text,
                bot_response=response
            )
            db.add(chat_entry)
            db.commit()

        return response

    if any(word in text_l for word in BREATHING_WORDS):
        return breathing_exercise()

    if any(word in text_l for word in MINDFUL_WORDS):
        return mindfulness_exercise()

    # Skip health search for professor-specific queries to avoid false matches
    professor_keywords = ['professor', 'academic', 'teaching', 'research', 'grading', 'tenure', 'students', 'university', 'college', 'faculty']
    is_professor_query = any(keyword in text.lower() for keyword in professor_keywords)

    # Check for prevention-focused queries first to prioritize them over health searches
    is_prevention_query = any(word in text_l for word in PREVENTION_WORDS)
    if is_prevention_query:
        prevention_response = get_prevention_solutions(text)
        if prevention_response:
            return prevention_response

    # Check for intent-based responses (general responses for emotions/issues) before health database
    for intent in INTENT_RESPONSES:
        if intent in text_l:
            return INTENT_RESPONSES[intent]

    # Health information queries - skip for professor or prevention queries to avoid false matches
    if not is_professor_query and not is_prevention_query:
        health_results = search_health_database(text)
        if health_results:
            return format_health_response(health_results, text)

    # Professor-specific exercises - check after general responses to avoid overriding
    if any(word in text_l for word in ACADEMIC_STRESS_WORDS):
        if "grading" in text_l or "grade" in text_l:
            return grading_overwhelm_relief()
        elif "research" in text_l or "publish" in text_l:
            return research_block_planning()
        elif "tenure" in text_l:
            return tenure_track_stress_management()
        elif "time" in text_l or "deadline" in text_l:
            return academic_time_management_exercise()
        else:
            return get_academic_stress_response(text, current_mood)

    if any(word in text_l for word in WORK_LIFE_WORDS):
        if "burnout" in text_l:
            return work_life_boundary_setting()
        else:
            return get_work_life_balance_response(text, current_mood)

    if any(word in text_l for word in PROFESSIONAL_WORDS):
        if "imposter" in text_l or "fraud" in text_l or "not good enough" in text_l:
            return imposter_syndrome_academia()
        elif "student" in text_l or "teaching" in text_l:
            return student_interaction_recharge()
        elif "social" in text_l or "connection" in text_l or "isolated" in text_l:
            return academic_social_connection()
        elif "sabbatical" in text_l or "break" in text_l:
            return sabbatical_preparation()
        else:
            return get_professional_support_response(text, current_mood)

    # Doctor consultation requests
    if any(word in text_l for word in ["doctor", "consult", "appointment", "medical help", "see a doctor", "healthcare", "physician"]):
        return provide_doctor_consultation_info()

    # Get recent conversation history for context
    conversation_history = []
    if user:
        recent_chats = db.query(ChatHistory).filter(
            ChatHistory.user_id == user.id
        ).order_by(ChatHistory.timestamp.desc()).limit(10).all()

        # Reverse to get chronological order (oldest first)
        recent_chats.reverse()

        for chat in recent_chats:
            conversation_history.append({"role": "user", "content": chat.user_message})
            conversation_history.append({"role": "assistant", "content": chat.bot_response})

    # Enhanced data integration for comprehensive responses
    health_results = search_health_database(text)
    professor_keywords = ['academic', 'professor', 'teaching', 'research', 'grading', 'tenure', 'students', 'university', 'college', 'faculty']
    is_academic_context = any(keyword in text.lower() for keyword in professor_keywords)

    # Use Gemini for natural conversation
    try:
        system_prompt = f"""You are a friendly, supportive wellbeing companion - like a trusted friend who genuinely cares about {username}'s wellbeing. You're not a therapist, but you're always there to listen and help."""
        if current_mood:
            system_prompt += f" They mentioned feeling {current_mood} recently."
        system_prompt += """

Your personality:
- Talk like a caring friend: warm, genuine, and approachable
- Use casual language but stay supportive and professional
- Share that you understand feelings without pretending to be a therapist
- Be encouraging and positive without being overly cheerful when they're struggling
- Ask questions that show you care about their experience
- Keep responses conversational (150-200 words) - not robotic or clinical
- End naturally, like you'd end a chat with a friend
- Remember you're here to support, not diagnose or treat

Be conversational about daily life:
- Respond warmly to greetings like "hello" or "hi" and ask about their day or routine
- Engage in casual talk about daily routines, habits, and everyday experiences
- Share relatable thoughts about normal life things (morning coffee, commute, hobbies, etc.)
- Ask open-ended questions about their daily life to keep conversation flowing
- Make small talk feel natural and comfortable, like chatting with a good friend
- Connect wellbeing topics to daily life (how stress affects routines, building healthy habits)

Available resources you can draw from:
- Comprehensive health knowledge database (conditions, symptoms, treatments, prevention)
- General wellbeing exercises (breathing, mindfulness)
- Academic-specific exercises (time management, stress relief for professors)
- Symptom prevention strategies
- Wellness advice on nutrition, exercise, sleep, mental health

When suggesting exercises or activities:
- Present them as friendly suggestions, not prescriptions
- Explain why they might help in simple terms
- Make it feel like you're doing it together
- For academics, prioritize professor-specific exercises when relevant

Always prioritize their emotional safety and encourage professional help for serious concerns."""

        # Format conversation for Gemini
        prompt = system_prompt + "\n\nConversation history:\n"
        for msg in conversation_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        prompt += f"user: {text}"

        response = gemini_model.generate_content(prompt)
        bot_response = response.text.strip()

        # Translate response if target language is not English
        if target_language and target_language != 'en':
            try:
                bot_response = translation_service.translate(bot_response, target_language)
            except Exception as e:
                # If translation fails, keep original English response
                print(f"Translation failed: {str(e)}")

        # Save conversation to database
        if user:
            chat_entry = ChatHistory(
                user_id=user.id,
                user_message=text,
                bot_response=bot_response
            )
            db.add(chat_entry)
            db.commit()

        return bot_response
    except Exception as e:
        # Debug: Print the exception to understand the issue
        print(f"OpenAI API Error: {str(e)}")
        # Enhanced fallback to rule-based responses if OpenAI fails
        return get_enhanced_fallback_response(text, current_mood)

def get_academic_stress_response(text, current_mood):
    """Provide professor-specific responses for academic stress"""
    responses = [
        "I understand the unique pressures of academic life - grading, research deadlines, and student expectations can be overwhelming. As a professor, you're doing important work that matters. Would you like some strategies for managing academic stress?",
        "Teaching and research are demanding roles. It's normal to feel stressed about deadlines and student needs. Remember that taking care of your wellbeing allows you to better serve your students and advance your research.",
        "Academic workloads can be intense. Consider breaking large tasks into smaller, manageable steps. Would you like me to suggest some time management techniques specifically for professors?",
        "The pressure to publish, teach effectively, and meet tenure requirements is significant. You're not alone in feeling this way - many academics struggle with these demands. Let's work on some coping strategies together."
    ]

    if current_mood and current_mood.lower() in ["stressed", "overwhelmed", "anxious"]:
        return responses[0] + " Given that you're feeling " + current_mood.lower() + " today, a quick breathing exercise might help you regain focus."

    return responses[len(text) % len(responses)]

def get_work_life_balance_response(text, current_mood):
    """Provide responses for work-life balance challenges"""
    responses = [
        "Work-life balance is crucial for professors, who often work beyond traditional hours. Setting boundaries between your professional and personal life is essential for long-term wellbeing.",
        "Academic life can blur the lines between work and personal time. Consider creating a 'shutdown ritual' at the end of your workday to help transition into personal time.",
        "Burnout is common in academia. Remember that your worth isn't defined solely by your professional achievements. Taking time for hobbies, family, and self-care is not selfish - it's necessary.",
        "Many professors struggle with work-life balance. Try the 'academic sabbath' approach - designating certain times or days for complete disconnection from work emails and grading."
    ]

    if "burnout" in text.lower():
        return "Burnout in academia is real and serious. Consider speaking with a counselor or mentor about your workload. In the meantime, let's try a mindfulness exercise to help you reconnect with what matters most."

    return responses[len(text) % len(responses)]

def get_professional_support_response(text, current_mood):
    """Provide responses for professional challenges"""
    responses = [
        "Professional evaluations and career advancement in academia can be stressful. Remember that your value extends beyond metrics and reviews - your impact on students and knowledge is immeasurable.",
        "Department politics and colleague relationships can be challenging. Focus on what you can control: your teaching, your research, and your professional development.",
        "Career advancement in academia often feels competitive. Celebrate your unique contributions and remember that success comes in many forms, not just traditional academic metrics.",
        "Professional relationships in academia can be complex. Consider finding mentors or peers who understand your challenges and can offer support and perspective."
    ]

    if "review" in text.lower() or "evaluation" in text.lower():
        return "Performance reviews can be anxiety-inducing. Remember that feedback, even critical, is an opportunity for growth. You've built a career through dedication and expertise - that's something to be proud of."

    return responses[len(text) % len(responses)]

def format_health_response(results, query):
    """Format health information responses professionally - provide targeted information based on query"""
    query_lower = query.lower()

    # Determine query intent
    is_symptom_query = any(word in query_lower for word in ["symptoms of", "symptom", "signs of", "what are the symptoms"])
    is_cause_query = any(word in query_lower for word in ["cause", "causes", "why", "what causes"])
    is_treatment_query = any(word in query_lower for word in ["treatment", "treatments", "cure", "how to treat", "medicine"])
    is_prevention_query = any(word in query_lower for word in ["prevent", "prevention", "avoid"])
    is_describing_symptoms = any(word in query_lower for word in ["i have", "i'm experiencing", "feeling", "pain", "ache", "hurt"])

    response = ""

    for result in results[:2]:  # Limit to top 2 results for conciseness
        if result["type"] == "condition":
            info = result["info"]
            condition_name = result['name'].replace('_', ' ').title()

            if is_describing_symptoms:
                # User is describing symptoms - suggest possible conditions
                response += f"Based on your description, this could be related to {condition_name}.\n\n"
                response += f"Key symptoms: {', '.join(info.get('symptoms', [])[:4])}\n\n"
                response += "Please consult a healthcare professional for proper diagnosis.\n\n"

            elif is_symptom_query:
                # User asking about symptoms of a specific disease
                response += f"Symptoms of {condition_name}:\n"
                symptoms = info.get('symptoms', [])
                for symptom in symptoms:
                    response += f"• {symptom}\n"
                response += "\n"

            elif is_cause_query:
                # User asking about causes
                response += f"Causes of {condition_name}:\n"
                causes = info.get('causes', [])
                for cause in causes:
                    response += f"• {cause}\n"
                response += "\n"

            elif is_treatment_query:
                # User asking about treatments
                response += f"Treatments for {condition_name}:\n"
                treatments = info.get('treatments', [])
                for treatment in treatments:
                    response += f"• {treatment}\n"
                response += "\n"

            elif is_prevention_query:
                # User asking about prevention
                response += f"Prevention of {condition_name}:\n"
                prevention = info.get('prevention', [])
                for item in prevention:
                    response += f"• {item}\n"
                response += "\n"

            else:
                # General query about disease - provide brief overview
                response += f"{condition_name}:\n"
                response += f"A condition characterized by: {', '.join(info.get('symptoms', [])[:3])}\n\n"

        elif result["type"] == "symptom":
            # User asking about possible causes of symptoms
            response += f"Possible conditions for {result['name']}:\n"
            causes = result['causes'][:5]  # Limit to 5 causes
            for cause in causes:
                response += f"• {cause}\n"
            response += "\n"

        elif result["type"] == "prevention":
            # User asking about prevention tips for symptoms
            response += f"Prevention tips for {result['name']}:\n"
            prevention_tips = result['prevention_tips'][:6]  # Limit to 6 tips
            for tip in prevention_tips:
                response += f"• {tip}\n"
            response += "\n"

    if response:
        response += "This is general information only. Please consult a healthcare professional for personalized medical advice."
    else:
        response = "I don't have specific information about that health topic. Please consult a healthcare professional for medical advice."

    return response

def get_prevention_solutions(text):
    """Provide prevention tips and solutions for health issues based on user query"""
    text_lower = text.lower()

    # Map common prevention/solution queries to health conditions
    prevention_mappings = {
        "sadness": ["depression"],
        "depression": ["depression"],
        "anxiety": ["anxiety"],
        "stress": ["stress"],
        "heart disease": ["hypertension", "heart_disease"],
        "diabetes": ["diabetes"],
        "cancer": ["breast_cancer", "lung_cancer", "colorectal_cancer"],
        "stroke": ["stroke"],
        "arthritis": ["arthritis"],
        "osteoporosis": ["osteoporosis"],
        "back pain": ["back_pain"],
        "migraine": ["migraine"],
        "insomnia": ["insomnia"],
        "obesity": ["obesity"],
        "asthma": ["asthma"],
        "copd": ["chronic_obstructive_pulmonary_disease"],
        "pneumonia": ["pneumonia"],
        "covid": ["covid_19"],
        "flu": ["influenza"],
        "tuberculosis": ["tuberculosis"],
        "eczema": ["eczema"],
        "psoriasis": ["psoriasis"],
        "allergies": ["allergies"],
        "thyroid": ["thyroid_disorders"],
        "hormonal": ["thyroid_disorders"],
        "immune": ["immune_system"],
        "infection": ["covid_19", "influenza", "pneumonia"],
        "mental health": ["depression", "anxiety", "stress"],
        "mood": ["depression", "bipolar_disorder"],
        "sleep": ["insomnia"],
        "weight": ["obesity", "diabetes"],
        "bone": ["osteoporosis"],
        "joint": ["arthritis"],
        "skin": ["eczema", "psoriasis"],
        "respiratory": ["asthma", "chronic_obstructive_pulmonary_disease"],
        "cardiovascular": ["hypertension", "heart_disease"],
        "digestive": ["irritable_bowel_syndrome", "gastroesophageal_reflux_disease"],
        "ibs": ["irritable_bowel_syndrome"],
        "gerd": ["gastroesophageal_reflux_disease"],
        "ulcerative colitis": ["ulcerative_colitis"],
        "alzheimers": ["alzheimers_disease"],
        "dementia": ["alzheimers_disease"],
        "parkinsons": ["parkinsons_disease"],
        "ptsd": ["ptsd"],
        "ocd": ["ocd"],
        "bipolar": ["bipolar_disorder"],
        "adhd": ["adhd"],
        "autism": ["autism"],
        "chronic illness": ["chronic_illness"],
        "disability": ["disability"],
        "aging": ["aging_concerns"],
        "menopause": ["menopause"],
        "pregnancy": ["pregnancy"],
        "postpartum": ["postpartum"],
        "infertility": ["infertility"],
        "chronic pain": ["chronic_pain"],
        "addiction": ["addiction"],
        "eating disorder": ["eating_disorders"],
        "self harm": ["self_harm"],
        "suicidal": ["suicidal_thoughts"],
        "trauma": ["trauma"]
    }

    # Check for wellness topics
    wellness_mappings = {
        "nutrition": "nutrition",
        "exercise": "exercise",
        "sleep": "sleep",
        "mental wellness": "mental_wellness",
        "wellness": "mental_wellness",
        "healthy eating": "nutrition",
        "physical activity": "exercise",
        "rest": "sleep",
        "mindfulness": "mental_wellness"
    }

    response = ""

    # Check for specific health conditions
    for keyword, conditions in prevention_mappings.items():
        if keyword in text_lower:
            for condition in conditions:
                if condition in HEALTH_CONDITIONS:
                    info = HEALTH_CONDITIONS[condition]
                    condition_name = condition.replace('_', ' ').title()

                    response += f"**Prevention and Solutions for {condition_name}:**\n\n"

                    # Add prevention tips
                    if 'prevention' in info and info['prevention']:
                        response += "**Prevention Tips:**\n"
                        for tip in info['prevention'][:5]:  # Limit to 5 tips
                            response += f"• {tip}\n"
                        response += "\n"

                    # Add immediate help if available
                    if 'immediate_help' in info and info['immediate_help']:
                        response += f"**Immediate Help:** {info['immediate_help']}\n\n"

                    # Add general wellness advice
                    if condition in ["depression", "anxiety", "stress"]:
                        response += "**Additional Support:**\n"
                        response += "• Practice daily gratitude journaling\n"
                        response += "• Maintain social connections\n"
                        response += "• Regular exercise (even 20 minutes daily)\n"
                        response += "• Consider professional counseling\n\n"

                    break
            if response:
                break

    # Check for wellness topics
    for keyword, topic in wellness_mappings.items():
        if keyword in text_lower:
            if topic in WELLNESS_TOPICS:
                advice = WELLNESS_TOPICS[topic]
                topic_name = topic.replace('_', ' ').title()
                response += f"**{topic_name} Tips:**\n\n"
                response += f"{advice}\n\n"
                break

    # General prevention advice if no specific match
    if not response:
        if "prevent" in text_lower or "avoid" in text_lower:
            response = """**General Health Prevention Tips:**

• **Maintain a healthy lifestyle:** Regular exercise, balanced nutrition, adequate sleep
• **Stay hydrated:** Drink plenty of water throughout the day
• **Practice stress management:** Meditation, deep breathing, hobbies
• **Regular health check-ups:** Annual physical exams and screenings
• **Build strong social connections:** Maintain relationships and community ties
• **Limit harmful substances:** Moderate alcohol, avoid smoking, be cautious with medications
• **Practice good hygiene:** Regular handwashing, vaccination when appropriate
• **Mental health awareness:** Address stress early, seek help when needed

For specific health concerns, please consult a healthcare professional for personalized advice."""

    if response:
        response += "\n*This information is for educational purposes. Please consult healthcare professionals for personalized medical advice.*"

    return response if response else None

def provide_doctor_consultation_info():
    """Provide doctor consultation information and resources"""
    consultation_info = """
Doctor Consultation Options

Immediate Medical Attention (Emergency):
• Call emergency services (911) for life-threatening situations
• Go to the nearest emergency room

Primary Care Physician:
• Schedule an appointment with your regular doctor
• Use telehealth services for virtual consultations
• Walk-in clinics for urgent but non-emergency care

Specialist Referrals:
• Ask your primary care doctor for specialist recommendations
• Use healthcare provider directories online

Mental Health Support:
• Psychiatrists for medication management
• Therapists/Counselors for talk therapy
• Crisis hotlines: National Suicide Prevention Lifeline (988)

Telemedicine Options:
• Apps like Teladoc, Amwell, or Doctor on Demand
• Many insurance plans cover virtual visits
• Available 24/7 for non-emergency care

Finding a Doctor:
• Use Healthgrades, Zocdoc, or Vitals for reviews
• Check insurance provider directories
• Ask for recommendations from trusted friends/family

Preparation Tips:
• Write down your symptoms and when they started
• List current medications and allergies
• Prepare questions about your condition
• Bring a list of previous medical history

Would you like me to help you find specific resources or prepare for a doctor's visit?
"""
    return consultation_info

def get_enhanced_fallback_response(text, current_mood):
    """Enhanced rule-based fallback responses when OpenAI API is unavailable - focused on practical, specific help"""
    text_lower = text.lower()

    # Expanded keyword detection for better matching
    expressing_sadness = any(word in text_lower for word in ["sad", "depressed", "depression", "down", "blue", "unhappy", "miserable", "hopeless", "crying", "tears", "heartbroken", "low mood"])
    expressing_anxiety = any(word in text_lower for word in ["anxious", "anxiety", "worried", "worry", "nervous", "panic", "panicking", "scared", "fear", "frightened", "heart racing", "chest tight", "can't breathe"])
    expressing_stress = any(word in text_lower for word in ["stressed", "stress", "overwhelmed", "overwhelming", "pressure", "tension", "burnout", "burned out", "can't cope", "too much", "breaking point"])
    expressing_loneliness = any(word in text_lower for word in ["lonely", "alone", "isolated", "isolation", "no one", "abandoned", "friendless", "empty", "disconnect"])
    expressing_tiredness = any(word in text_lower for word in ["tired", "exhausted", "fatigued", "fatigue", "no energy", "sleepy", "drained", "worn out", "lethargic"])
    expressing_anger = any(word in text_lower for word in ["angry", "anger", "frustrated", "frustration", "irritated", "irritation", "mad", "furious", "upset", "annoyed"])

    # Check for specific needs and requests
    seeking_help = any(phrase in text_lower for phrase in ["help me", "i need help", "what can i do", "how can i", "what should i", "give me advice", "suggest", "recommend"])
    is_question = text.endswith('?') or text_lower.startswith(('what', 'how', 'why', 'when', 'where', 'can you', 'do you', 'should i'))
    expressing_gratitude = any(word in text_lower for word in ["grateful", "thankful", "appreciate", "blessed", "gratitude", "thanks"])
    expressing_happiness = any(word in text_lower for word in ["happy", "joy", "excited", "great", "wonderful", "good", "positive", "amazing"])

    # Specific actionable responses based on detected emotions and needs
    if expressing_sadness and seeking_help:
        return "I hear you're feeling sad and need help. Right now, try this 3-step approach: 1) Take 5 slow deep breaths, 2) Name one small thing you're grateful for, 3) Do one tiny comforting action like drinking water or stretching. Would you like me to guide you through a full breathing exercise?"

    elif expressing_sadness:
        return "Sadness can be really heavy. You're not alone in this feeling. Try reaching out to one person you trust, even just to say 'I'm having a tough day.' Or do something nurturing like a warm shower or favorite comfort food. What usually helps when you feel this way?"

    elif expressing_anxiety and seeking_help:
        return "For your anxiety right now: Sit comfortably, place one hand on your belly. Breathe in slowly for 4 counts (feel your belly rise), hold for 4, breathe out for 6 counts. Repeat 4 times. This calms your nervous system. Would you like me to walk you through this breathing exercise step by step?"

    elif expressing_anxiety:
        return "Anxiety can make everything feel scary and uncertain. Try this grounding technique: Look around and name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, 1 thing you can taste. This brings you back to the present moment. What triggers your anxiety most?"

    elif expressing_stress and seeking_help:
        return "Let's tackle your stress with specific steps: 1) Stop what you're doing for 2 minutes, 2) Do shoulder rolls and neck stretches, 3) Take 10 slow breaths, 4) Write down one thing you can control. Which of these would you like to try first?"

    elif expressing_stress:
        return "Stress can feel like carrying a heavy load. Try this quick reset: Step away from your tasks, do 10 jumping jacks or march in place, then take 3 deep breaths. What's the main thing stressing you out right now that I can help you think through?"

    elif expressing_loneliness and seeking_help:
        return "For loneliness, start with small connections: 1) Send a text to one friend saying 'Thinking of you', 2) Join an online community related to your interests, 3) Consider volunteering virtually. Would you like specific suggestions for online communities or social activities?"

    elif expressing_loneliness:
        return "Feeling lonely hurts, and it's more common than people think. Consider calling a family member, joining a local club, or even talking to someone at a store. Sometimes just hearing another person's voice helps. What kind of social connection do you miss most?"

    elif expressing_tiredness and seeking_help:
        return "To combat fatigue: 1) Get bright light (open curtains or go outside), 2) Do 5 minutes of light movement like walking, 3) Drink a glass of water, 4) Eat something with protein. Would you like detailed sleep hygiene tips or energy-boosting food suggestions?"

    elif expressing_tiredness:
        return "Fatigue can make everything feel harder. Try getting some natural sunlight, taking a short walk, or doing gentle stretches. What do you think might be causing your tiredness - lack of sleep, stress, or something else?"

    elif expressing_anger and seeking_help:
        return "For anger management: 1) Step back physically from the situation, 2) Take slow breaths - inhale for 4, exhale for 6, 3) Write down what's making you angry and why. Would you like a full anger management technique or ways to express anger constructively?"

    elif expressing_anger:
        return "Anger is a valid emotion that needs healthy expression. Try going for a brisk walk, punching a pillow, or writing down your feelings. Understanding what triggered your anger can help you respond better. What happened to make you feel this way?"

    elif expressing_gratitude:
        return "It's beautiful that you're feeling grateful! Gratitude is one of the best ways to boost wellbeing. Try writing down 3 specific things you're thankful for today. What are you most grateful for in this moment?"

    elif expressing_happiness:
        return "I'm so glad you're feeling positive! What's bringing you joy right now? Sharing and savoring positive moments helps build emotional strength. Would you like suggestions to maintain or increase this good feeling?"

    elif seeking_help:
        return "I want to help you specifically. Could you tell me what's bothering you or what you need support with? I can provide breathing exercises, stress management techniques, mindfulness practices, or just listen to whatever is on your mind."

    elif is_question:
        return "I'd love to answer your question! Could you give me a bit more detail about what you're asking? I'm here to provide practical advice, exercises, or information to support your wellbeing."

    # Mood-based responses when no specific emotion detected but mood is tracked
    elif current_mood:
        mood_lower = current_mood.lower()

        if mood_lower in ["sad", "depressed", "low"]:
            return "I see you're tracking sadness today - that's an important step in self-awareness. Try this self-compassion practice: Place your hand on your heart and say 'This is a difficult moment, and I'm here with myself.' What would help you feel a little more supported right now?"

        elif mood_lower in ["anxious", "worried", "nervous"]:
            return "Your anxiety tracking shows you're paying attention to your feelings. Try this quick grounding: Name 5 things you see around you, 4 you can touch, 3 you can hear. This helps bring you back to the present. What usually helps when anxiety builds?"

        elif mood_lower in ["stressed", "overwhelmed", "tense"]:
            return "Stress tracking is valuable awareness. Try this 1-minute reset: Close your eyes, take 3 deep breaths, and drop your shoulders. What's one small thing you could let go of to feel less stressed?"

        elif mood_lower in ["lonely", "isolated"]:
            return "Tracking loneliness takes courage. Consider reaching out to someone today - even a simple 'hello' can help. Or try a loving-kindness meditation: Send kind thoughts to yourself first, then others. What kind of connection would feel good right now?"

        elif mood_lower in ["tired", "exhausted", "fatigued"]:
            return "Fatigue tracking helps you prioritize rest. Try a 2-minute body scan: Notice where you hold tension and consciously relax those areas. What would help you feel more energized - rest, movement, or nutrition?"

        elif mood_lower in ["happy", "content", "good"]:
            return "It's wonderful you're tracking positive feelings! What's contributing to this good mood? Noticing what works helps you cultivate more of it. Would you like ways to build on this positivity?"

        elif mood_lower in ["angry", "frustrated"]:
            return "Anger tracking is important self-awareness. Try channeling that energy into something constructive like exercise or creative expression. What triggered these feelings, and how would you like to process them?"

        else:
            return f"Thanks for tracking your mood as {current_mood.lower()}. Self-awareness is a powerful tool for wellbeing. What would be most helpful for you right now - an exercise, advice, or just to talk?"

    # General fallback with specific offers of help
    else:
        return "I'm here to support your wellbeing journey. Whether you're dealing with stress, anxiety, sadness, or just need someone to listen, I'm here. What specific support are you looking for today - breathing exercises, coping strategies, or something else?"
