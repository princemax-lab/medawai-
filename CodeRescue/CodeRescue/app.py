import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from gtts import gTTS
import tempfile
import os
from flask_cors import CORS
from ai_engine import get_medicine_recommendations
from data import symptoms_data, medicines_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Render the main page of the application."""
    maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY', '')
    return render_template('index.html', symptoms=symptoms_data, maps_api_key=maps_api_key)

@app.route('/api/age-appropriate-symptoms/<int:age>')
def get_age_appropriate_symptoms(age):
    """API endpoint to get age-appropriate symptoms."""
    # Filter symptoms by min_age
    appropriate_symptoms = [
        symptom for symptom in symptoms_data 
        if 'min_age' in symptom and symptom['min_age'] <= age and 
        (symptom.get('max_age') is None or symptom.get('max_age') >= age)
    ]

    return jsonify({'symptoms': appropriate_symptoms})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API endpoint to recommend medicines based on symptoms."""
    try:
        # Get symptom data from request
        data = request.get_json()
        user_symptoms = data.get('symptoms', [])
        user_age = data.get('age', 0)
        user_gender = data.get('gender', '')
        symptom_text = data.get('symptom_text', '')

        # Validate age and gender
        if not isinstance(user_age, (int, float)) or user_age <= 0:
            return jsonify({'error': 'Invalid age provided'}), 400

        if user_gender not in ['male', 'female', 'other', '']:
            return jsonify({'error': 'Invalid gender provided'}), 400

        # Process indirect symptom text if provided
        if symptom_text and not user_symptoms:
            # Advanced natural language processing for symptoms
            symptom_text = symptom_text.lower().strip()
            # Replace common text variations
            symptom_text = symptom_text.replace('i have ', '')\
                                         .replace('having ', '')\
                                         .replace('getting ', '')\
                                         .replace('feeling ', '')\
                                         .replace('suffering from ', '')\
                                         .replace('experiencing ', '')
            matched_symptoms = []
            symptom_matches = {}  # Dictionary to store symptom matches with confidence scores

            # List of common symptom synonyms and related terms including Hinglish and informal language
            symptom_synonyms = {
                'headache': ['head pain', 'head ache', 'migraine', 'head pressure', 'sar dard', 'sir dard', 'head m dard', 'sir me dard', 'sr drd', 'headche', 'sir m pain', 'dimag phat raha'],
                'fever': ['temperature', 'hot', 'burning up', 'chills', 'sweating', 'bukhar', 'fever h', 'temp h', 'garmi', 'thand lag rahi', 'bkhr', 'fvr', 'bukhaar', 'bukhaar aa gya', 'tap aa gya', 'body garam', 'mujhe bukhaar ha', 'bukhaar hai', 'bukhar hai', 'fever hai', 'tap', 'bukar', 'bukhr', 'bukhar h', 'bukhaar h'],
                'cough': ['coughing', 'hack', 'throat clearing', 'chest cough', 'khansi', 'khasi', 'khans raha hu', 'khansi ho rahi', 'khasi lg gyi', 'cnstnt cough', 'khnsi'],
                'sore throat': ['throat pain', 'painful throat', 'throat irritation', 'scratchy throat', 'gale me dard', 'gala kharab', 'throat me pain', 'gla dukh rha', 'gla khrab', 'gale m prblm'],
                'fatigue': ['tired', 'exhausted', 'no energy', 'weakness', 'lack of energy', 'thakan', 'kamzori', 'thak gaya', 'no enrgy', 'bahut thaka hua', 'thkn', 'kmzori', 'no nrgy', 'bohot thak gya'],
                'nausea': ['sick to stomach', 'queasy', 'upset stomach', 'feeling sick', 'ulti jaisa', 'matlii', 'pet me garbar', 'pet kharab', 'ulti si lg rhi', 'mtli', 'nausea feel ho rha'],
                'dizziness': ['lightheaded', 'vertigo', 'spinning', 'balance problems', 'chakkar', 'sir ghum raha', 'dizzy feel', 'spinning feel', 'chkkr', 'ghumri', 'head spin ho rha'],
                'pain': ['ache', 'sore', 'hurts', 'discomfort', 'tender', 'dard', 'pain h', 'dard ho raha', 'takleef', 'drd', 'pn', 'bohot dard', 'pain bohot h'],
                'runny nose': ['nasal discharge', 'nasal drip', 'rhinorrhea', 'nose running', 'drippy nose', 'nak beh rahi', 'runny nose h', 'naak se pani', 'nk beh rhi', 'nose beh rha', 'nk se paani'],
                'nasal congestion': ['stuffy nose', 'blocked nose', 'congested nose', 'clogged nose', 'blocked sinuses', 'nak band', 'stuffed nose h', 'nk block', 'nose block ho gya', 'naak band h'],
                'cold': ['common cold', 'head cold', 'coryza', 'seasonal cold', 'cold symptoms', 'zukam', 'sardi', 'cold lag gaya', 'sardi lag gayi', 'zukm', 'srdi', 'cold lg gya', 'srdii'],
                'sneezing': ['achoo', 'fits of sneezing', 'chronic sneezing', 'nasal irritation', 'chink', 'cheenk', 'sneeze aa raha', 'baar baar sneeze', 'chink aa rhi', 'sneeze lg gyi', 'chinke'],
                'stomach ache': ['pet dard', 'stomach pain', 'pet me dard', 'tummy ache', 'stomch pain', 'pet ki problem', 'pt drd', 'stmch pn', 'tummy m pain', 'pet m dard'],
                'body ache': ['body pain', 'badan dard', 'pure body me dard', 'body m pain', 'poore sharir me dard', 'bdy pn', 'pura badan dard', 'body m drd', 'sharir dard'],
                'vomiting': ['throwing up', 'ulti', 'vomit', 'ulti aa rahi', 'vomiting ho rahi', 'puke', 'vmt', 'ulti lg rhi', 'vomit aa rha', 'throwing up feel']
            }

            # Common cold symptoms for better matching
            cold_related_symptoms = {
                'runny nose': 5,  # ID for Runny Nose 
                'nasal congestion': 22,  # ID for Nasal Congestion
                'cough': 3,  # ID for Cough
                'sore throat': 4,  # ID for Sore Throat
                'headache': 1,  # ID for Headache
                'fever': 2,  # ID for Fever
            }

            # Check for "cold" keyword to add common cold symptoms
            if 'cold' in symptom_text.lower():
                cold_confidence = 3  # Default confidence if just "cold" is mentioned

                # Check how strongly the user is describing a cold
                cold_indicators = ['bad cold', 'terrible cold', 'caught a cold', 'have a cold', 'common cold']
                for indicator in cold_indicators:
                    if indicator in symptom_text.lower():
                        cold_confidence = 4
                        break

                # Check for stuffy or runny nose specifically
                if 'stuffy nose' in symptom_text.lower() or 'blocked nose' in symptom_text.lower():
                    # Add nasal congestion directly with high confidence
                    for s in symptoms_data:
                        if s['id'] == 22:  # Nasal congestion
                            symptom_matches[22] = {
                                'symptom': s,
                                'confidence': 5  # High confidence since it's directly mentioned
                            }

                if 'runny nose' in symptom_text.lower() or 'nose running' in symptom_text.lower():
                    # Add runny nose directly with high confidence
                    for s in symptoms_data:
                        if s['id'] == 5:  # Runny nose
                            symptom_matches[5] = {
                                'symptom': s,
                                'confidence': 5  # High confidence since it's directly mentioned
                            }

                # Add cold symptoms with appropriate confidence if cold is mentioned
                if cold_confidence > 0:
                    for symptom_name, symptom_id in cold_related_symptoms.items():
                        # Check if this symptom is age-appropriate
                        for s in symptoms_data:
                            if s['id'] == symptom_id:
                                min_age = s.get('min_age', 0)
                                max_age = s.get('max_age')
                                if min_age <= user_age and (max_age is None or max_age >= user_age):
                                    # Add the cold symptom if not already added
                                    if symptom_id not in [k for k in symptom_matches.keys()]:
                                        symptom_matches[symptom_id] = {
                                            'symptom': s,
                                            'confidence': cold_confidence - 1  # Slightly lower confidence for inferred symptoms
                                        }

            for symptom in symptoms_data:
                # Check if symptom is age-appropriate
                min_age = symptom.get('min_age', 0)
                max_age = symptom.get('max_age')
                if min_age <= user_age and (max_age is None or max_age >= user_age):
                    symptom_name = symptom['name'].lower()
                    symptom_desc = symptom['description'].lower()
                    confidence = 0

                    # Check for exact symptom name in text (highest confidence)
                    if symptom_name in symptom_text:
                        confidence = 5
                    # Check for partial matches in the symptom name
                    elif any(word in symptom_text for word in symptom_name.split() if len(word) > 3):
                        confidence = 3

                    # Check synonyms and related terms
                    for base_symptom, synonyms in symptom_synonyms.items():
                        if base_symptom in symptom_name or base_symptom in symptom_desc:
                            if any(syn in symptom_text for syn in synonyms):
                                confidence = max(confidence, 4)

                    # Check for symptom description matches (looking for meaningful words)
                    desc_words = [word for word in symptom_desc.split() if len(word) > 3]
                    if any(word in symptom_text for word in desc_words):
                        confidence = max(confidence, 2)

                    # Location-based matching (body parts)
                    body_parts = ['head', 'chest', 'stomach', 'throat', 'eye', 'ear', 'nose', 
                                 'back', 'leg', 'arm', 'neck', 'joint', 'muscle', 'skin']

                    for part in body_parts:
                        if part in symptom_name and part in symptom_text:
                            confidence = max(confidence, 3)

                    # If we have any confidence, add to the potential matches
                    if confidence > 0:
                        symptom_matches[symptom['id']] = {
                            'symptom': symptom,
                            'confidence': confidence
                        }

            # Sort matches by confidence level and take the top ones
            sorted_matches = sorted(
                symptom_matches.items(), 
                key=lambda x: x[1]['confidence'], 
                reverse=True
            )

            # Add the top matches to our list (confidence >= 2)
            for symptom_id, match_data in sorted_matches:
                if match_data['confidence'] >= 2:
                    matched_symptoms.append(symptom_id)

            user_symptoms = matched_symptoms
            logger.debug(f"Extracted symptoms from text: {matched_symptoms}")
            logger.debug(f"Matched with confidence levels: {[(s_id, symptom_matches[s_id]['confidence']) for s_id in matched_symptoms]}")

        # Validate that we have symptoms to work with
        if not user_symptoms:
            return jsonify({'error': 'No symptoms provided or identified from text'}), 400

        logger.debug(f"Received symptoms: {user_symptoms}")
        logger.debug(f"User age: {user_age}, gender: {user_gender}")

        # Get recommendations from AI engine
        recommendations = get_medicine_recommendations(
            user_symptoms, 
            user_age, 
            user_gender,
            symptoms_data,
            medicines_data
        )

        # Include the identified symptoms in the response
        identified_symptoms = []
        for symptom_id in user_symptoms:
            for symptom in symptoms_data:
                if symptom['id'] == symptom_id:
                    identified_symptoms.append({
                        'id': symptom['id'],
                        'name': symptom['name'],
                        'description': symptom['description']
                    })
                    break

        return jsonify({
            'recommendations': recommendations,
            'identified_symptoms': identified_symptoms
        })

    except Exception as e:
        logger.error(f"Error in recommendation process: {str(e)}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/api/symptoms')
def get_symptoms():
    """API endpoint to get all available symptoms."""
    return jsonify({'symptoms': symptoms_data})

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500