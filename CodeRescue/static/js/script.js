document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Form elements
    const symptomForm = document.getElementById('symptom-form');
    const ageInput = document.getElementById('age');
    const genderSelect = document.getElementById('gender');
    const symptomCheckboxes = document.querySelectorAll('.symptom-checkbox');
    const symptomSearch = document.getElementById('symptom-search');
    const symptomItems = document.querySelectorAll('.symptom-item');
    const recommendBtn = document.getElementById('recommend-btn');
    const loadingIndicator = document.getElementById('loading');
    const resultsSection = document.getElementById('results-section');
    const recommendationsContainer = document.getElementById('recommendations-container');
    const noResultsAlert = document.getElementById('no-results');
    const errorAlert = document.getElementById('error-alert');
    const errorMessage = document.getElementById('error-message');
    const symptomsFeedback = document.getElementById('symptoms-feedback');
    
    // Tab content elements
    const selectSymptomsTab = document.getElementById('select-symptoms-tab');
    const describeSymptomsTab = document.getElementById('describe-symptoms-tab');
    const symptomDescription = document.getElementById('symptom-description');
    
    // Form submission
    symptomForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate form inputs
        if (!validateForm()) {
            return;
        }
        
        // Show loading indicator
        loadingIndicator.classList.remove('d-none');
        
        // Hide previous results and errors
        resultsSection.classList.add('d-none');
        errorAlert.classList.add('d-none');
        
        // Disable submit button
        recommendBtn.disabled = true;
        
        try {
            // Determine active tab
            const isDescribeTabActive = describeSymptomsTab.classList.contains('active') || 
                                       document.querySelector('#describe-symptoms.active') !== null;
            
            // Prepare request data
            const requestData = {
                age: parseInt(ageInput.value),
                gender: genderSelect.value
            };
            
            if (isDescribeTabActive) {
                // Get symptom description
                requestData.symptom_text = symptomDescription.value.trim();
            } else {
                // Get selected symptoms
                const selectedSymptoms = [];
                symptomCheckboxes.forEach(checkbox => {
                    if (checkbox.checked) {
                        selectedSymptoms.push(parseInt(checkbox.value));
                    }
                });
                requestData.symptoms = selectedSymptoms;
            }
            
            // Make API request
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            // Process response
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Hide loading indicator
            loadingIndicator.classList.add('d-none');
            
            // Display results
            displayRecommendations(data.recommendations, data.identified_symptoms);
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            // Hide loading indicator
            loadingIndicator.classList.add('d-none');
            
            // Show error message
            errorMessage.textContent = error.message || 'An error occurred while processing your request. Please try again.';
            errorAlert.classList.remove('d-none');
            
            console.error('Error:', error);
        } finally {
            // Re-enable submit button
            recommendBtn.disabled = false;
        }
    });
    
    // Validate form inputs
    function validateForm() {
        let isValid = true;
        
        // Validate age
        if (!ageInput.value || ageInput.value < 1 || ageInput.value > 120) {
            ageInput.classList.add('is-invalid');
            isValid = false;
        } else {
            ageInput.classList.remove('is-invalid');
        }
        
        // Determine active tab
        const isDescribeTabActive = describeSymptomsTab.classList.contains('active') || 
                                   document.querySelector('#describe-symptoms.active') !== null;
        
        if (isDescribeTabActive) {
            // Validate symptom description
            if (!symptomDescription.value.trim()) {
                symptomDescription.classList.add('is-invalid');
                symptomsFeedback.style.display = 'block';
                isValid = false;
            } else {
                symptomDescription.classList.remove('is-invalid');
                symptomsFeedback.style.display = 'none';
            }
        } else {
            // Validate symptoms (at least one must be selected)
            let atLeastOneSymptomSelected = false;
            symptomCheckboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    atLeastOneSymptomSelected = true;
                }
            });
            
            if (!atLeastOneSymptomSelected) {
                symptomsFeedback.style.display = 'block';
                isValid = false;
            } else {
                symptomsFeedback.style.display = 'none';
            }
        }
        
        return isValid;
    }
    
    // Display medicine recommendations
    function displayRecommendations(recommendations, identifiedSymptoms) {
        // Clear previous results
        recommendationsContainer.innerHTML = '';
        
        // Show/hide no results message
        if (!recommendations || recommendations.length === 0) {
            noResultsAlert.classList.remove('d-none');
            resultsSection.classList.remove('d-none');
            return;
        }
        
        noResultsAlert.classList.add('d-none');
        
        // If we have identified symptoms from text, show them first
        if (identifiedSymptoms && identifiedSymptoms.length > 0) {
            const identifiedSymptomsCard = document.createElement('div');
            identifiedSymptomsCard.className = 'card mb-4 shadow-sm';
            
            const symptomsList = identifiedSymptoms
                .map(s => `<li><strong>${s.name}</strong>: ${s.description}</li>`)
                .join('');
                
            identifiedSymptomsCard.innerHTML = `
                <div class="card-header bg-info text-white">
                    <h4 class="mb-0"><i class="fas fa-stethoscope me-2"></i>Identified Symptoms</h4>
                </div>
                <div class="card-body">
                    <p>Based on your description, we identified the following symptoms:</p>
                    <ul>${symptomsList}</ul>
                </div>
            `;
            
            recommendationsContainer.appendChild(identifiedSymptomsCard);
        }
        
        // Sort recommendations to show best match first
        // Clone the array to not modify the original
        const sortedRecommendations = [...recommendations].sort((a, b) => {
            // Best match always comes first
            if (a.is_best_match && !b.is_best_match) return -1;
            if (!a.is_best_match && b.is_best_match) return 1;
            // Otherwise sort by effectiveness score
            return b.effectiveness_score - a.effectiveness_score;
        });
        
        // Create a "Best Match" section if we have a best match
        const bestMatch = sortedRecommendations.find(med => med.is_best_match);
        if (bestMatch) {
            const bestMatchCard = document.createElement('div');
            bestMatchCard.className = 'card mb-4 border-success shadow';
            bestMatchCard.innerHTML = `
                <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                    <h3 class="mb-0">
                        <i class="fas fa-star me-2"></i>Best Recommended Medicine
                    </h3>
                    <span class="badge bg-white text-success">Match: ${bestMatch.match_percentage}%</span>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-8">
                            <h4>${bestMatch.name}</h4>
                            <p class="card-text">${bestMatch.description}</p>
                            
                            <div class="mt-3">
                                <h5 class="mb-2">
                                    <i class="fas fa-check-circle text-success me-2"></i>
                                    Why This Is Recommended:
                                </h5>
                                <p>This medicine is the best match for your symptoms because it effectively treats 
                                ${bestMatch.matched_symptoms.length} of your symptoms: 
                                <strong>${bestMatch.matched_symptoms.join(', ')}</strong>.</p>
                            </div>
                        </div>
                        <div class="col-md-4 d-flex align-items-center justify-content-center">
                            <div class="text-center">
                                <div class="position-relative">
                                    <div class="display-1 text-success">
                                        <i class="fas fa-pills"></i>
                                    </div>
                                    <div class="position-absolute top-0 end-0">
                                        <span class="badge rounded-pill bg-success">
                                            <i class="fas fa-check"></i>
                                        </span>
                                    </div>
                                </div>
                                <p class="mt-2 text-success fw-bold">Highest Effectiveness</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row mt-3">
                        <div class="col-md-6">
                            <h5 class="mb-2">
                                <i class="fas fa-prescription me-2"></i>
                                Recommended Dosage
                            </h5>
                            <p>${bestMatch.dosage}</p>
                        </div>
                        <div class="col-md-6">
                            <h5 class="mb-2">
                                <i class="fas fa-exclamation-circle text-warning me-2"></i>
                                Side Effects
                            </h5>
                            <p>${bestMatch.side_effects}</p>
                        </div>
                    </div>
                    
                    <div class="alert alert-warning mt-3" role="alert">
                        <i class="fas fa-ban me-2"></i>
                        <strong>Contraindications:</strong> ${bestMatch.contraindications || 'No specific contraindications listed.'}
                    </div>
                </div>
                <div class="card-footer bg-light">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-info-circle text-info me-2 fs-4"></i>
                        <span>Always consult a healthcare professional before taking any medication.</span>
                    </div>
                </div>
            `;
            
            recommendationsContainer.appendChild(bestMatchCard);
        }
        
        // Add a header for alternative recommendations if we have more than one
        if (sortedRecommendations.length > 1) {
            const alternativesHeader = document.createElement('h4');
            alternativesHeader.className = 'mt-4 mb-3';
            alternativesHeader.innerHTML = '<i class="fas fa-list-alt me-2"></i>Alternative Recommendations';
            recommendationsContainer.appendChild(alternativesHeader);
        }
        
        // Create cards for each recommendation (skipping the best match as we've already shown it)
        sortedRecommendations.forEach((medicine, index) => {
            // Skip if this is the best match (already displayed)
            if (medicine.is_best_match) return;
            
            // Determine relevance class
            let relevanceClass, relevanceText;
            if (medicine.match_percentage > 70) {
                relevanceClass = 'relevance-high';
                relevanceText = 'High';
            } else if (medicine.match_percentage > 40) {
                relevanceClass = 'relevance-medium';
                relevanceText = 'Medium';
            } else {
                relevanceClass = 'relevance-low';
                relevanceText = 'Low';
            }
            
            // Create medicine card
            const medicineCard = document.createElement('div');
            medicineCard.className = 'card medicine-card mb-4 shadow-sm';
            medicineCard.innerHTML = `
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h4 class="mb-0">${medicine.name}</h4>
                    <span class="badge bg-dark ${relevanceClass}">Match: ${medicine.match_percentage}%</span>
                </div>
                <div class="card-body">
                    <p class="card-text">${medicine.description}</p>
                    
                    <h5 class="mt-3 mb-2">
                        <i class="fas fa-check-circle text-success me-2"></i>
                        Treats Symptoms
                    </h5>
                    <div>
                        ${medicine.matched_symptoms.map(symptom => 
                            `<span class="symptom-tag"><i class="fas fa-circle-dot me-1"></i>${symptom}</span>`
                        ).join(' ')}
                    </div>
                    
                    <h5 class="mt-3 mb-2">
                        <i class="fas fa-prescription me-2"></i>
                        Recommended Dosage
                    </h5>
                    <p>${medicine.dosage}</p>
                    
                    <div class="accordion mt-3" id="accordion-${index}">
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-side-effects-${index}">
                                    <i class="fas fa-exclamation-circle me-2"></i>
                                    Side Effects
                                </button>
                            </h2>
                            <div id="collapse-side-effects-${index}" class="accordion-collapse collapse" data-bs-parent="#accordion-${index}">
                                <div class="accordion-body">
                                    ${medicine.side_effects}
                                </div>
                            </div>
                        </div>
                        
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-contraindications-${index}">
                                    <i class="fas fa-ban me-2"></i>
                                    Contraindications
                                </button>
                            </h2>
                            <div id="collapse-contraindications-${index}" class="accordion-collapse collapse" data-bs-parent="#accordion-${index}">
                                <div class="accordion-body">
                                    ${medicine.contraindications || 'No specific contraindications listed.'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-footer text-muted">
                    <small><i class="fas fa-info-circle me-1"></i>Always consult a healthcare professional before taking any medication.</small>
                </div>
            `;
            
            recommendationsContainer.appendChild(medicineCard);
        });
        
        // Show results section
        resultsSection.classList.remove('d-none');
    }
    
    // Input validation listeners
    ageInput.addEventListener('input', function() {
        if (this.value && this.value >= 1 && this.value <= 120) {
            this.classList.remove('is-invalid');
        }
    });
    
    // Symptom description validation
    symptomDescription.addEventListener('input', function() {
        if (this.value.trim()) {
            this.classList.remove('is-invalid');
            symptomsFeedback.style.display = 'none';
        }
    });
    
    // Symptom checkbox listeners
    symptomCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            let anyChecked = false;
            symptomCheckboxes.forEach(cb => {
                if (cb.checked) anyChecked = true;
            });
            
            if (anyChecked) {
                symptomsFeedback.style.display = 'none';
            }
        });
    });
    
    // Symptom search functionality
    symptomSearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        
        symptomItems.forEach(item => {
            const symptomLabel = item.querySelector('.form-check-label').textContent.toLowerCase();
            
            if (searchTerm === '' || symptomLabel.includes(searchTerm)) {
                item.style.display = 'block';
                
                // Add highlight class if search term is not empty and there's a match
                if (searchTerm !== '' && symptomLabel.includes(searchTerm)) {
                    item.classList.add('highlight');
                } else {
                    item.classList.remove('highlight');
                }
            } else {
                item.style.display = 'none';
                item.classList.remove('highlight');
            }
        });
        
        // Show a message if no symptoms match the search
        const visibleItems = [...symptomItems].filter(item => item.style.display !== 'none');
        
        // If no symptoms match search, add a "no results" message
        let noResultsMsg = document.getElementById('no-symptom-results');
        
        if (visibleItems.length === 0 && searchTerm !== '') {
            if (!noResultsMsg) {
                noResultsMsg = document.createElement('div');
                noResultsMsg.id = 'no-symptom-results';
                noResultsMsg.className = 'alert alert-info mt-2';
                noResultsMsg.innerHTML = '<i class="fas fa-info-circle me-2"></i>No symptoms match your search.';
                
                const searchContainer = symptomSearch.closest('.input-group').parentNode;
                searchContainer.appendChild(noResultsMsg);
            }
        } else if (noResultsMsg) {
            noResultsMsg.remove();
        }
    });
});
