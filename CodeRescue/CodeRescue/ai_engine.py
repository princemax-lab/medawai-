import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import logging

logger = logging.getLogger(__name__)

def get_medicine_recommendations(user_symptoms, age, gender, symptoms_data, medicines_data):
    """
    Generate medicine recommendations based on user symptoms.
    
    Args:
        user_symptoms (list): List of symptom IDs selected by the user
        age (int): User's age
        gender (str): User's gender
        symptoms_data (list): Database of symptoms
        medicines_data (list): Database of medicines
    
    Returns:
        list: Recommended medicines sorted by relevance
    """
    logger.debug(f"Processing recommendations for symptoms: {user_symptoms}")
    
    # Ensure user_symptoms are integers
    user_symptom_ids = [int(s) for s in user_symptoms if s]
    
    # Calculate medicine scores based on matching symptoms
    medicine_scores = []
    
    # Add priority for pediatric medicines for young children
    is_young_child = age <= 5
    
    for medicine in medicines_data:
        # Skip medicines that are not appropriate for the user's age
        min_age = medicine.get('age_restrictions', {}).get('min', 0)
        max_age = medicine.get('age_restrictions', {}).get('max')
        
        if age < min_age:
            continue
        if max_age is not None and age > max_age:
            continue
            
        # Skip prescription medicines (for this basic version)
        if medicine.get('prescription_required', False):
            continue
        
        # Calculate score based on number of matching symptoms and age appropriateness
        matching_symptoms = set(medicine['indications']).intersection(set(user_symptom_ids))
        score = len(matching_symptoms)
        
        # Prioritize pediatric medicines for young children
        if is_young_child:
            if "Children's" in medicine['name'] or "Pediatric" in medicine['name']:
                score *= 1.5  # Boost score for pediatric medicines
            
            # Additional safety check for minimum age
            if age < min_age:
                continue
        
        # Only include medicines that treat at least one of the user's symptoms
        if score > 0:
            medicine_scores.append({
                'medicine': medicine,
                'score': score,
                'matched_symptoms': list(matching_symptoms)
            })
    
    # Sort medicines by score (highest first)
    medicine_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Get the final recommendations with additional information
    recommendations = []
    
    # Calculate max possible score to determine best match percentage
    max_possible_score = len(user_symptom_ids)
    
    for item in medicine_scores:
        medicine = item['medicine']
        matched_symptoms = item['matched_symptoms']
        
        # Get the names of the matched symptoms
        matched_symptom_names = []
        for symptom_id in matched_symptoms:
            for symptom in symptoms_data:
                if symptom['id'] == symptom_id:
                    matched_symptom_names.append(symptom['name'])
                    break
        
        # Calculate match percentage
        match_percentage = (item['score'] / max_possible_score) * 100
        
        # Calculate effectiveness score based on symptom coverage and medicine properties
        effectiveness_score = item['score']
        
        # Add age appropriateness bonus (if medicine is specifically designed for the age group)
        min_age = medicine.get('age_restrictions', {}).get('min', 0)
        max_age = medicine.get('age_restrictions', {}).get('max')
        
        # Check if age is within the medicine's age range
        if min_age <= age and (max_age is None or age <= max_age):
            # Add pediatric bonus for medicines specifically designed for children/teenagers
            if max_age is not None and max_age <= 18:
                effectiveness_score += 0.5  # Pediatric bonus
        
        recommendations.append({
            'id': medicine['id'],
            'name': medicine['name'],
            'description': medicine['description'],
            'dosage': medicine['dosage'],
            'side_effects': medicine['side_effects'],
            'contraindications': medicine.get('contraindications', ''),
            'matched_symptoms': matched_symptom_names,
            'relevance_score': item['score'],
            'match_percentage': round(match_percentage),
            'effectiveness_score': effectiveness_score,
            'is_best_match': False  # Will be set below
        })
    
    # Find the best match based on effectiveness score
    if recommendations:
        max_effectiveness = max(r['effectiveness_score'] for r in recommendations)
        for rec in recommendations:
            if rec['effectiveness_score'] == max_effectiveness:
                rec['is_best_match'] = True
                break
    
    logger.debug(f"Generated {len(recommendations)} recommendations")
    return recommendations
