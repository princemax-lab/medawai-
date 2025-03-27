# This file contains the symptom and medicine data for the recommendation system

# List of common symptoms with age appropriateness
symptoms_data = [
    {"id": 1, "name": "Headache", "description": "Pain in the head or upper neck", "min_age": 5, "max_age": None},
    {"id": 2, "name": "Fever", "description": "Elevated body temperature above normal range", "min_age": 5, "max_age": None},
    {"id": 3, "name": "Cough", "description": "Sudden expulsion of air from the lungs", "min_age": 5, "max_age": None},
    {"id": 4, "name": "Sore Throat", "description": "Pain or irritation in the throat", "min_age": 5, "max_age": None},
    {"id": 5, "name": "Runny Nose", "description": "Excessive discharge of fluid from the nose", "min_age": 5, "max_age": None},
    {"id": 6, "name": "Body Ache", "description": "Diffuse pain in muscles throughout the body", "min_age": 5, "max_age": None},
    {"id": 7, "name": "Fatigue", "description": "Extreme tiredness or exhaustion", "min_age": 5, "max_age": None},
    {"id": 8, "name": "Nausea", "description": "Feeling of sickness with an urge to vomit", "min_age": 5, "max_age": None},
    {"id": 9, "name": "Vomiting", "description": "Forceful expulsion of stomach contents through the mouth", "min_age": 5, "max_age": None},
    {"id": 10, "name": "Diarrhea", "description": "Loose, watery stools occurring more frequently than usual", "min_age": 5, "max_age": None},
    {"id": 11, "name": "Constipation", "description": "Difficulty passing stools or infrequent bowel movements", "min_age": 5, "max_age": None},
    {"id": 12, "name": "Dizziness", "description": "Feeling faint, lightheaded, or unsteady", "min_age": 8, "max_age": None},
    {"id": 13, "name": "Chest Pain", "description": "Discomfort or pain in the chest area", "min_age": 12, "max_age": None},
    {"id": 14, "name": "Shortness of Breath", "description": "Difficulty breathing or feeling breathless", "min_age": 5, "max_age": None},
    {"id": 15, "name": "Abdominal Pain", "description": "Pain in the area between the chest and groin", "min_age": 5, "max_age": None},
    {"id": 16, "name": "Joint Pain", "description": "Discomfort, aches, or soreness in joints", "min_age": 5, "max_age": None},
    {"id": 17, "name": "Rash", "description": "Abnormal change in skin color or texture", "min_age": 5, "max_age": None},
    {"id": 18, "name": "Itching", "description": "Irritating sensation causing the desire to scratch", "min_age": 5, "max_age": None},
    {"id": 19, "name": "Swelling", "description": "Enlargement or bloating of a body part", "min_age": 5, "max_age": None},
    {"id": 20, "name": "Insomnia", "description": "Difficulty falling asleep or staying asleep", "min_age": 5, "max_age": None},
    {"id": 21, "name": "Ear Pain", "description": "Pain or discomfort in one or both ears", "min_age": 5, "max_age": None},
    {"id": 22, "name": "Nasal Congestion", "description": "Blockage of nasal passages", "min_age": 5, "max_age": None},
    {"id": 23, "name": "Motion Sickness", "description": "Nausea and dizziness from movement", "min_age": 6, "max_age": None},
    {"id": 24, "name": "Allergic Reaction", "description": "Immune response to allergens", "min_age": 5, "max_age": None},
    {"id": 25, "name": "Sunburn", "description": "Skin irritation caused by overexposure to sun", "min_age": 5, "max_age": None},
    {"id": 26, "name": "Minor Burns", "description": "First-degree burn affecting only the outer layer of skin", "min_age": 5, "max_age": None},
    {"id": 27, "name": "Muscle Cramps", "description": "Sudden, involuntary contraction of muscles", "min_age": 8, "max_age": None},
    {"id": 28, "name": "Indigestion", "description": "Discomfort in the upper abdomen", "min_age": 12, "max_age": None},
    {"id": 29, "name": "Dry Eyes", "description": "Insufficient tear production or tear evaporation", "min_age": 12, "max_age": None},
    {"id": 30, "name": "Dry Skin", "description": "Skin that lacks moisture and feels rough", "min_age": 5, "max_age": None}
]

# Medicine database with indications (symptoms they treat)
medicines_data = [
    {
        "id": 1,
        "name": "Acetaminophen (Tylenol)",
        "indications": [1, 2, 6, 21],  # Headache, Fever, Body Ache, Ear Pain
        "description": "Pain reliever and fever reducer",
        "dosage": "Adults and children 12+: 325-650mg every 4-6 hours as needed, not exceeding 3000mg in 24 hours\nChildren 6-11: 160-320mg every 4-6 hours as needed\nChildren 2-5: Consult pediatrician for proper dosing",
        "side_effects": "Rare but may include liver damage with high doses or allergic reactions",
        "contraindications": "Liver disease, alcohol consumption of 3 or more drinks per day",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 2,
        "name": "Ibuprofen (Advil, Motrin)",
        "indications": [1, 2, 6, 16, 21, 27],  # Headache, Fever, Body Ache, Joint Pain, Ear Pain, Muscle Cramps
        "description": "Nonsteroidal anti-inflammatory drug (NSAID) for pain and inflammation",
        "dosage": "Adults and children 12+: 200-400mg every 4-6 hours as needed, not exceeding 1200mg in 24 hours\nChildren 6-11: 100-200mg every 6-8 hours, not exceeding 600mg in 24 hours",
        "side_effects": "Stomach upset, heartburn, nausea, dizziness",
        "contraindications": "Heart problems, stomach ulcers, aspirin allergy, pregnancy (third trimester)",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 3,
        "name": "Loratadine (Claritin)",
        "indications": [5, 17, 18, 24],  # Runny Nose, Rash, Itching, Allergic Reaction
        "description": "Antihistamine for allergy symptoms",
        "dosage": "Adults and children 6+: 10mg once daily\nChildren 2-5: 5mg once daily",
        "side_effects": "Headache, drowsiness, dry mouth",
        "contraindications": "Liver or kidney disease (may need dose adjustment)",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 4,
        "name": "Pseudoephedrine (Sudafed)",
        "indications": [5],  # Runny Nose
        "description": "Decongestant that relieves nasal congestion",
        "dosage": "Adults: 60mg every 4-6 hours, not exceeding 240mg in 24 hours",
        "side_effects": "Nervousness, dizziness, difficulty sleeping, increased heart rate",
        "contraindications": "High blood pressure, heart disease, thyroid disease, diabetes",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 5,
        "name": "Dextromethorphan (Robitussin DM)",
        "indications": [3],  # Cough
        "description": "Cough suppressant",
        "dosage": "Adults: 10-20mg every 4 hours or 30mg every 6-8 hours, not exceeding 120mg in 24 hours",
        "side_effects": "Dizziness, drowsiness, nausea",
        "contraindications": "MAO inhibitor use within 14 days",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 6,
        "name": "Bismuth Subsalicylate (Pepto-Bismol)",
        "indications": [8, 9, 10, 15],  # Nausea, Vomiting, Diarrhea, Abdominal Pain
        "description": "Relief for digestive issues",
        "dosage": "Adults: 30ml or 2 tablets every 30-60 minutes as needed, not exceeding 8 doses in 24 hours",
        "side_effects": "Darkening of tongue or stool, temporary graying of tongue",
        "contraindications": "Aspirin allergy, bleeding disorders, reye's syndrome, pregnancy",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 7,
        "name": "Loperamide (Imodium)",
        "indications": [10],  # Diarrhea
        "description": "Anti-diarrheal medication",
        "dosage": "Adults: 4mg initially, then 2mg after each loose stool, not exceeding 8mg in 24 hours",
        "side_effects": "Constipation, abdominal pain, dry mouth, drowsiness",
        "contraindications": "Bloody diarrhea, severe colitis, pseudomembranous colitis",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 8,
        "name": "Diphenhydramine (Benadryl)",
        "indications": [17, 18, 20],  # Rash, Itching, Insomnia
        "description": "Antihistamine for allergies and sleep aid",
        "dosage": "Adults: 25-50mg every 4-6 hours, not exceeding 300mg in 24 hours",
        "side_effects": "Drowsiness, dry mouth, dizziness, constipation",
        "contraindications": "Glaucoma, prostate problems, respiratory diseases",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 9,
        "name": "Docusate Sodium (Colace)",
        "indications": [11],  # Constipation
        "description": "Stool softener",
        "dosage": "Adults: 50-500mg daily in divided doses",
        "side_effects": "Mild abdominal cramps, throat irritation",
        "contraindications": "Intestinal obstruction, abdominal pain, nausea, vomiting",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 10,
        "name": "Meclizine (Dramamine)",
        "indications": [8, 12],  # Nausea, Dizziness
        "description": "Anti-nausea and dizziness medication",
        "dosage": "Adults: 25-50mg 1 hour before travel, then every 24 hours as needed",
        "side_effects": "Drowsiness, dry mouth, blurred vision",
        "contraindications": "Glaucoma, urinary retention, MAO inhibitor use within 14 days",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 11,
        "name": "Amoxicillin",
        "indications": [3, 4],  # Cough, Sore Throat (bacterial)
        "description": "Antibiotic for bacterial infections",
        "dosage": "Adults: 250-500mg three times daily for 7-10 days",
        "side_effects": "Diarrhea, rash, nausea, vomiting",
        "contraindications": "Penicillin allergy, infectious mononucleosis",
        "age_restrictions": {
            "min": 0,
            "max": 60
        },
        "prescription_required": True
    },
    {
        "id": 12,
        "name": "Omeprazole (Prilosec)",
        "indications": [15],  # Abdominal Pain (related to acid reflux)
        "description": "Proton pump inhibitor for reducing stomach acid",
        "dosage": "Adults: 20mg once daily before a meal",
        "side_effects": "Headache, abdominal pain, diarrhea, nausea",
        "contraindications": "Vitamin B12 deficiency, osteoporosis risk",
        "age_restrictions": {
            "min": 18,
            "max": 60
        }
    },
    {
        "id": 13,
        "name": "Hydrocortisone Cream",
        "indications": [17, 18],  # Rash, Itching
        "description": "Topical steroid for skin inflammation",
        "dosage": "Apply thin layer to affected area 2-4 times daily",
        "side_effects": "Skin irritation, thinning of skin with prolonged use",
        "contraindications": "Fungal skin infections, open wounds",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 14,
        "name": "Aspirin",
        "indications": [1, 2, 6, 16],  # Headache, Fever, Body Ache, Joint Pain
        "description": "Pain reliever, fever reducer, anti-inflammatory",
        "dosage": "Adults: 325-650mg every 4-6 hours as needed, not exceeding 4000mg in 24 hours",
        "side_effects": "Stomach upset, heartburn, risk of bleeding",
        "contraindications": "Children under 18 (risk of Reye's syndrome), bleeding disorders, ulcers",
        "age_restrictions": {
            "min": 18,
            "max": 60
        }
    },
    {
        "id": 15,
        "name": "Melatonin",
        "indications": [20],  # Insomnia
        "description": "Sleep aid hormone supplement",
        "dosage": "Adults: 1-5mg 30 minutes before bedtime",
        "side_effects": "Headache, dizziness, nausea, drowsiness",
        "contraindications": "Autoimmune disorders, depression, pregnancy",
        "age_restrictions": {
            "min": 18,
            "max": 60
        }
    },
    {
        "id": 16,
        "name": "Children's Acetaminophen (Tylenol Children's)",
        "indications": [1, 2, 6, 21],  # Headache, Fever, Body Ache, Ear Pain
        "description": "Pediatric pain reliever and fever reducer",
        "dosage": "Children 5-8 years (48-59 lbs): 240mg every 4 hours as needed\nChildren 9-10 years (60-71 lbs): 320mg every 4 hours as needed\nNot to exceed 5 doses in 24 hours",
        "side_effects": "Rare when used as directed, may include allergic reactions",
        "contraindications": "Known allergy to acetaminophen",
        "age_restrictions": {
            "min": 1,
            "max": 11
        }
    },
    {
        "id": 17,
        "name": "Children's Ibuprofen (Motrin Children's, Advil Children's)",
        "indications": [1, 2, 6, 16, 21],  # Headache, Fever, Body Ache, Joint Pain, Ear Pain
        "description": "Pediatric pain reliever, fever reducer, and anti-inflammatory",
        "dosage": "Children 5-8 years: 100mg every 6-8 hours\nChildren 9-10 years: 150mg every 6-8 hours\nNot to exceed 4 doses in 24 hours",
        "side_effects": "Upset stomach, rare risk of stomach bleeding",
        "contraindications": "Allergy to NSAIDs, active stomach problems",
        "age_restrictions": {
            "min": 1,
            "max": 11
        }
    },
    {
        "id": 18,
        "name": "Cetirizine (Zyrtec Children's)",
        "indications": [5, 17, 18, 24],  # Runny Nose, Rash, Itching, Allergic Reaction
        "description": "Antihistamine for allergy symptoms in children",
        "dosage": "Children 5-10 years: 5-10mg once daily depending on severity of symptoms",
        "side_effects": "Drowsiness, dry mouth, fatigue",
        "contraindications": "Known allergy to cetirizine",
        "age_restrictions": {
            "min": 1,
            "max": 11
        }
    },
    {
        "id": 19,
        "name": "Pediatric Electrolyte Solution",
        "indications": [9, 10],  # Vomiting, Diarrhea
        "description": "Oral rehydration solution to prevent dehydration",
        "dosage": "Children 5+ years: 1-2 cups (8-16 oz) after each loose stool or vomiting episode",
        "side_effects": "None when used as directed",
        "contraindications": "None",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 20,
        "name": "Benzocaine Topical (Orajel)",
        "indications": [4],  # Sore Throat (for mouth/throat pain)
        "description": "Topical anesthetic for mouth and throat pain",
        "dosage": "Children 5+ years: Apply small amount to affected area up to 4 times daily",
        "side_effects": "Temporary numbness, rare allergic reactions",
        "contraindications": "Known benzocaine allergy",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 21,
        "name": "Aloe Vera Gel",
        "indications": [25],  # Sunburn
        "description": "Cooling gel for sunburn relief",
        "dosage": "Apply liberally to affected area as needed",
        "side_effects": "Rare skin irritation in sensitive individuals",
        "contraindications": "Known allergy to aloe vera",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    },
    {
        "id": 22,
        "name": "Saline Nasal Spray",
        "indications": [5, 22],  # Runny Nose, Nasal Congestion
        "description": "Saltwater solution to relieve nasal congestion",
        "dosage": "Children 5+ years: 1-2 sprays in each nostril as needed",
        "side_effects": "None when used as directed",
        "contraindications": "None",
        "age_restrictions": {
            "min": 1,
            "max": 60
        }
    }
]