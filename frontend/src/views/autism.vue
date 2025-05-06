<template>
  <div class="autism-container">
    <div class="page-header">
      <h1>Autism Learning Tools</h1>
      <p>Structured learning with predictable patterns and sensory considerations</p>
    </div>
    
    <div class="content-section">
      <div class="environment-controls">
        <h2>Learning Environment Settings</h2>
        <p>Customize your learning environment to minimize distractions and sensory overload</p>
        
        <div class="control-options">
          <div class="control-group">
            <label>Visual Theme</label>
            <div class="theme-options">
              <button 
                v-for="theme in visualThemes" 
                :key="theme.name"
                :class="['theme-btn', { active: settings.theme === theme.name }]"
                :style="{ backgroundColor: theme.backgroundColor, color: theme.textColor }"
                @click="changeTheme(theme.name)"
              >
                {{ theme.name }}
              </button>
            </div>
          </div>
          
          <div class="control-group">
            <label>Animation Level</label>
            <div class="slider-container">
              <input type="range" min="0" max="2" v-model="settings.animationLevel">
              <span>{{ animationLevelText }}</span>
            </div>
          </div>
          
          <div class="control-group">
            <label>Text Presentation</label>
            <div class="option-buttons">
              <button 
                :class="{ active: settings.textChunking === 'normal' }"
                @click="settings.textChunking = 'normal'"
              >
                Normal
              </button>
              <button 
                :class="{ active: settings.textChunking === 'chunked' }"
                @click="settings.textChunking = 'chunked'"
              >
                Chunked
              </button>
              <button 
                :class="{ active: settings.textChunking === 'highlighted' }"
                @click="settings.textChunking = 'highlighted'"
              >
                Highlighted
              </button>
            </div>
          </div>
          
          <div class="control-group">
            <label>Learning Elements</label>
            <div class="checkbox-options">
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.showVisuals">
                Include visual supports
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.showAgenda">
                Show agenda/schedule
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="settings.showTransitions">
                Announce transitions
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="content-section">
      <div class="learning-module" :class="settings.theme">
        <transition name="fade" v-if="settings.showAgenda">
          <div class="agenda-panel" v-show="settings.showAgenda">
            <h3>Learning Session Agenda</h3>
            <ol class="agenda-list">
              <li :class="{ active: currentStep === 1 }">Introduction to the topic</li>
              <li :class="{ active: currentStep === 2 }">Key concepts and definitions</li>
              <li :class="{ active: currentStep === 3 }">Visual examples and demonstrations</li>
              <li :class="{ active: currentStep === 4 }">Practice activities</li>
              <li :class="{ active: currentStep === 5 }">Review and summarize</li>
            </ol>
            
            <div class="progress-bar">
              <div class="progress" :style="{ width: `${(currentStep / 5) * 100}%` }"></div>
            </div>
          </div>
        </transition>
        
        <div class="module-content">
          <div v-if="settings.showTransitions && transitionMessage" class="transition-message">
            {{ transitionMessage }}
          </div>
          
          <div class="step-navigator">
            <button @click="previousStep" :disabled="currentStep === 1">Previous</button>
            <span class="step-indicator">Step {{ currentStep }} of 5</span>
            <button @click="nextStep" :disabled="currentStep === 5">Next</button>
          </div>
          
          <div class="current-step-content">
            <div v-if="currentStep === 1">
              <h2>Introduction to Planets of the Solar System</h2>
              
              <div class="content-block" :class="{ 'text-chunked': settings.textChunking === 'chunked' }">
                <p v-if="settings.textChunking !== 'highlighted'">
                  Our solar system consists of the Sun, eight planets, dwarf planets, moons, asteroids, and comets. 
                  Each planet is unique and has different characteristics. Today, we will learn about the planets 
                  in our solar system and what makes each one special.
                </p>
                <p v-else v-html="highlightedIntroText"></p>
              </div>
              
              <div v-if="settings.showVisuals" class="visual-support">
                <div class="image-placeholder">
                  <span>[Solar system diagram showing all planets orbiting the sun]</span>
                </div>
              </div>
            </div>
            
            <div v-if="currentStep === 2">
              <h2>Key Concepts: The Planets</h2>
              
              <div class="content-block" :class="{ 'text-chunked': settings.textChunking === 'chunked' }">
                <p v-if="settings.textChunking !== 'highlighted'">
                  There are eight planets in our solar system. They are: Mercury, Venus, Earth, Mars, Jupiter, Saturn, 
                  Uranus, and Neptune. The planets are divided into two categories: inner rocky planets (Mercury, 
                  Venus, Earth, Mars) and outer gas giants (Jupiter, Saturn, Uranus, Neptune).
                </p>
                <p v-else v-html="highlightedConceptsText"></p>
                
                <div class="definition-box">
                  <strong>Planet:</strong> A celestial body that orbits the Sun, has sufficient mass for gravity to make it round, 
                  and has cleared its orbit of other objects.
                </div>
              </div>
              
              <div v-if="settings.showVisuals" class="visual-support">
                <div class="image-placeholder">
                  <span>[Diagram showing comparison of planet sizes]</span>
                </div>
              </div>
            </div>
            
            <div v-if="currentStep === 3">
              <h2>Visual Examples: Planet Features</h2>
              
              <div class="planet-features">
                <div class="planet-card">
                  <div class="planet-image earth"></div>
                  <h3>Earth</h3>
                  <ul>
                    <li>Has liquid water oceans</li>
                    <li>Has breathable atmosphere</li>
                    <li>One natural satellite (Moon)</li>
                    <li>Has life</li>
                  </ul>
                </div>
                
                <div class="planet-card">
                  <div class="planet-image mars"></div>
                  <h3>Mars</h3>
                  <ul>
                    <li>Red color from iron oxide</li>
                    <li>Has thin atmosphere</li>
                    <li>Two small moons</li>
                    <li>Has polar ice caps</li>
                  </ul>
                </div>
                
                <div class="planet-card">
                  <div class="planet-image jupiter"></div>
                  <h3>Jupiter</h3>
                  <ul>
                    <li>Largest planet</li>
                    <li>Great Red Spot storm</li>
                    <li>79 known moons</li>
                    <li>Composed of gas</li>
                  </ul>
                </div>
              </div>
            </div>
            
            <div v-if="currentStep === 4">
              <h2>Practice Activity: Planet Identification</h2>
              
              <div class="practice-activity">
                <div class="instruction-block">
                  <p>Match each characteristic with the correct planet.</p>
                </div>
                
                <div class="quiz-container">
                  <div 
                    v-for="(question, index) in quizQuestions" 
                    :key="index"
                    class="quiz-question"
                  >
                    <div class="question-text">{{ question.text }}</div>
                    <div class="answer-options">
                      <button 
                        v-for="option in question.options" 
                        :key="option"
                        :class="{ 
                          selected: question.selected === option,
                          correct: question.showAnswer && question.answer === option,
                          incorrect: question.showAnswer && question.selected === option && question.selected !== question.answer
                        }"
                        @click="selectAnswer(index, option)"
                        :disabled="question.showAnswer"
                      >
                        {{ option }}
                      </button>
                    </div>
                    <div v-if="question.showAnswer" class="answer-feedback">
                      {{ question.selected === question.answer ? 'Correct!' : `The correct answer is ${question.answer}` }}
                    </div>
                  </div>
                  
                  <button class="check-answers-btn" @click="checkAnswers" v-if="!quizChecked">
                    Check Answers
                  </button>
                  <div v-else class="quiz-results">
                    You got {{ correctAnswers }} out of {{ quizQuestions.length }} correct!
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="currentStep === 5">
              <h2>Review and Summary</h2>
              
              <div class="content-block" :class="{ 'text-chunked': settings.textChunking === 'chunked' }">
                <p v-if="settings.textChunking !== 'highlighted'">
                  Today we learned about the planets in our solar system. We discussed the inner rocky planets 
                  (Mercury, Venus, Earth, Mars) and the outer gas giants (Jupiter, Saturn, Uranus, Neptune). 
                  Each planet has unique features that make it different from the others.
                </p>
                <p v-else v-html="highlightedSummaryText"></p>
              </div>
              
              <div class="key-takeaways">
                <h3>Key Takeaways</h3>
                <ul>
                  <li>The solar system has eight official planets</li>
                  <li>Planets are divided into rocky planets and gas giants</li>
                  <li>Earth is the only known planet with life</li>
                  <li>Jupiter is the largest planet</li>
                  <li>Each planet has unique features and characteristics</li>
                </ul>
              </div>
              
              <div class="ai-help-section">
                <h3>Need Additional Help?</h3>
                <p>Ask our AI Assistant to explain any concept in a different way:</p>
                
                <div class="ai-input">
                  <textarea 
                    v-model="aiPrompt" 
                    placeholder="Ask a question about the solar system or planets..."
                    rows="2"
                  ></textarea>
                  <button 
                    @click="getAIExplanation" 
                    :disabled="!aiPrompt.trim() || isLoadingAI"
                  >
                    Get Explanation
                  </button>
                </div>
                
                <div v-if="isLoadingAI" class="ai-loading">
                  <div class="loading-spinner"></div>
                  Processing...
                </div>
                
                <div v-if="aiResponse" class="ai-response" :class="settings.theme">
                  <div v-html="aiResponse"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Autism',
  data() {
    return {
      // Environment settings
      settings: {
        theme: 'neutral',
        animationLevel: 1,
        textChunking: 'normal',
        showVisuals: true,
        showAgenda: true,
        showTransitions: true
      },
      
      visualThemes: [
        { name: 'neutral', backgroundColor: '#ffffff', textColor: '#333333' },
        { name: 'calm-blue', backgroundColor: '#edf6ff', textColor: '#333333' },
        { name: 'soft-beige', backgroundColor: '#f7f3eb', textColor: '#333333' },
        { name: 'dark-mode', backgroundColor: '#222222', textColor: '#e0e0e0' }
      ],
      
      // Learning module state
      currentStep: 1,
      transitionMessage: null,
      
      // Quiz state
      quizQuestions: [
        {
          text: "Which planet is known as the 'Red Planet'?",
          options: ['Earth', 'Mars', 'Venus', 'Jupiter'],
          answer: 'Mars',
          selected: null,
          showAnswer: false
        },
        {
          text: "Which is the largest planet in our solar system?",
          options: ['Saturn', 'Earth', 'Jupiter', 'Neptune'],
          answer: 'Jupiter',
          selected: null,
          showAnswer: false
        },
        {
          text: "Which planet is known for its prominent rings?",
          options: ['Jupiter', 'Saturn', 'Uranus', 'Neptune'],
          answer: 'Saturn',
          selected: null,
          showAnswer: false
        }
      ],
      quizChecked: false,
      
      // AI assistance
      aiPrompt: '',
      aiResponse: null,
      isLoadingAI: false
    }
  },
  computed: {
    animationLevelText() {
      const levels = ['None', 'Minimal', 'Standard'];
      return levels[this.settings.animationLevel];
    },
    correctAnswers() {
      return this.quizQuestions.filter(q => q.selected === q.answer).length;
    },
    highlightedIntroText() {
      return 'Our solar system consists of <span class="highlight">the Sun</span>, <span class="highlight">eight planets</span>, dwarf planets, moons, asteroids, and comets. Each planet is <span class="highlight">unique</span> and has different characteristics. Today, we will learn about the planets in our solar system and what makes each one special.';
    },
    highlightedConceptsText() {
      return 'There are <span class="highlight">eight planets</span> in our solar system. They are: <span class="highlight">Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune</span>. The planets are divided into two categories: <span class="highlight">inner rocky planets</span> (Mercury, Venus, Earth, Mars) and <span class="highlight">outer gas giants</span> (Jupiter, Saturn, Uranus, Neptune).';
    },
    highlightedSummaryText() {
      return 'Today we learned about the <span class="highlight">planets in our solar system</span>. We discussed the <span class="highlight">inner rocky planets</span> (Mercury, Venus, Earth, Mars) and the <span class="highlight">outer gas giants</span> (Jupiter, Saturn, Uranus, Neptune). Each planet has <span class="highlight">unique features</span> that make it different from the others.';
    }
  },
  methods: {
    changeTheme(theme) {
      this.settings.theme = theme;
      // Save preference to localStorage
      localStorage.setItem('autism-theme', theme);
    },
    
    previousStep() {
      if (this.currentStep > 1) {
        this.showTransition(`Moving to previous step: ${this.getStepName(this.currentStep - 1)}`);
        this.currentStep -= 1;
      }
    },
    
    nextStep() {
      if (this.currentStep < 5) {
        this.showTransition(`Moving to next step: ${this.getStepName(this.currentStep + 1)}`);
        this.currentStep += 1;
      }
    },
    
    getStepName(stepNumber) {
      const steps = [
        'Introduction',
        'Key Concepts',
        'Visual Examples',
        'Practice Activity',
        'Review and Summary'
      ];
      return steps[stepNumber - 1];
    },
    
    showTransition(message) {
      if (!this.settings.showTransitions) return;
      
      this.transitionMessage = message;
      setTimeout(() => {
        this.transitionMessage = null;
      }, 2000);
    },
    
    selectAnswer(questionIndex, option) {
      this.quizQuestions[questionIndex].selected = option;
    },
    
    checkAnswers() {
      // Show answers for all questions
      this.quizQuestions.forEach(question => {
        question.showAnswer = true;
      });
      this.quizChecked = true;
    },
    
    async getAIExplanation() {
      if (!this.aiPrompt.trim() || this.isLoadingAI) return;
      
      this.isLoadingAI = true;
      
      try {
        const response = await axios.post('/api/assistant', {
          prompt: `${this.aiPrompt} (Please explain in a way that's helpful for someone with autism - clear, precise language, avoid idioms, and include visual descriptions)`,
          learning_preferences: {
            visual_aids: true,
            structured_format: true,
            simplified_language: false // Autism often benefits from precise rather than simplified language
          }
        });
        
        this.aiResponse = response.data.response;
      } catch (error) {
        console.error('Error getting AI explanation:', error);
        this.aiResponse = '<p>Sorry, there was an error getting a response. Please try again.</p>';
      } finally {
        this.isLoadingAI = false;
      }
    }
  },
  mounted() {
    // Load saved preferences if available
    const savedTheme = localStorage.getItem('autism-theme');
    if (savedTheme && this.visualThemes.some(theme => theme.name === savedTheme)) {
      this.settings.theme = savedTheme;
    }
  }
}
</script>

<style scoped>
.autism-container {
  max-width: 100%;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.page-header p {
  font-size: 1.1rem;
  color: #666;
}

.content-section {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  margin-bottom: 30px;
}

.environment-controls h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.environment-controls p {
  color: #666;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

.control-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 25px;
}

.control-group {
  margin-bottom: 20px;
}

.control-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 10px;
}

.theme-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.theme-btn {
  padding: 8px 16px;
  border: 2px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: transform 0.2s;
}

.theme-btn.active {
  border-color: #6A11CB;
  font-weight: 600;
  transform: scale(1.05);
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.slider-container input {
  flex: 1;
}

.option-buttons {
  display: flex;
  gap: 10px;
}

.option-buttons button {
  padding: 8px 16px;
  background: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-buttons button.active {
  background: #6A11CB;
  color: white;
  border-color: #6A11CB;
}

.checkbox-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-label input {
  margin-right: 10px;
}

/* Learning module styles */
.learning-module {
  display: flex;
  gap: 30px;
  min-height: 600px;
  padding: 0;
  background-color: white;
}

.learning-module.calm-blue {
  background-color: #edf6ff;
}

.learning-module.soft-beige {
  background-color: #f7f3eb;
}

.learning-module.dark-mode {
  background-color: #222;
  color: #e0e0e0;
}

.agenda-panel {
  flex: 0 0 250px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
}

.dark-mode .agenda-panel {
  background: rgba(255, 255, 255, 0.1);
}

.agenda-panel h3 {
  margin-bottom: 15px;
  color: #6A11CB;
}

.dark-mode .agenda-panel h3 {
  color: #a17edd;
}

.agenda-list {
  padding-left: 20px;
  margin-bottom: 20px;
}

.agenda-list li {
  padding: 8px 0;
  color: #666;
}

.dark-mode .agenda-list li {
  color: #bbb;
}

.agenda-list li.active {
  color: #6A11CB;
  font-weight: 600;
}

.dark-mode .agenda-list li.active {
  color: #a17edd;
}

.progress-bar {
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  transition: width 0.5s ease;
}

.module-content {
  flex: 1;
  padding: 20px;
}

.transition-message {
  background: #f0e8fa;
  color: #6A11CB;
  padding: 12px 15px;
  border-radius: 6px;
  margin-bottom: 20px;
  text-align: center;
  animation: fadeIn 0.5s, fadeOut 0.5s 1.5s;
}

.dark-mode .transition-message {
  background: #3a2a50;
  color: #c9b8e2;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

.step-navigator {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.step-navigator button {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.step-navigator button:hover {
  opacity: 0.9;
}

.step-navigator button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.step-indicator {
  font-size: 1.1rem;
  color: #666;
}

.dark-mode .step-indicator {
  color: #bbb;
}

.current-step-content {
  padding: 10px;
}

.current-step-content h2 {
  color: #6A11CB;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.dark-mode .current-step-content h2 {
  color: #a17edd;
  border-color: #444;
}

.content-block {
  margin-bottom: 30px;
  line-height: 1.7;
}

.text-chunked p {
  max-width: 60ch;
}

.text-chunked p::after {
  content: "";
  display: block;
  height: 0.5em;
}

.highlight {
  background-color: rgba(106, 17, 203, 0.1);
  padding: 0 3px;
  font-weight: 500;
}

.dark-mode .highlight {
  background-color: rgba(161, 126, 221, 0.2);
}

.definition-box {
  background: #f8f9fa;
  border-left: 4px solid #6A11CB;
  padding: 15px;
  margin: 20px 0;
  border-radius: 4px;
}

.dark-mode .definition-box {
  background: #333;
  border-left-color: #a17edd;
}

.visual-support {
  margin: 30px 0;
  text-align: center;
}

.image-placeholder {
  background: #f0f0f0;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: #666;
}

.dark-mode .image-placeholder {
  background: #333;
  color: #bbb;
}

.planet-features {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.planet-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  transition: transform 0.2s;
}

.dark-mode .planet-card {
  background: #333;
}

.planet-card:hover {
  transform: translateY(-5px);
}

.planet-card h3 {
  margin: 15px 0;
  color: #6A11CB;
}

.dark-mode .planet-card h3 {
  color: #a17edd;
}

.planet-card ul {
  text-align: left;
  padding-left: 20px;
  margin-top: 15px;
}

.planet-card li {
  margin-bottom: 5px;
}

.planet-image {
  height: 100px;
  width: 100px;
  border-radius: 50%;
  margin: 0 auto;
}

.earth {
  background: linear-gradient(135deg, #2666CF 0%, #57A944 100%);
}

.mars {
  background: linear-gradient(135deg, #E65C4F 0%, #B1361E 100%);
}

.jupiter {
  background: linear-gradient(135deg, #E8B88F 0%, #BE7242 100%);
}

.practice-activity {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.dark-mode .practice-activity {
  background: #333;
}

.instruction-block {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.dark-mode .instruction-block {
  border-color: #444;
}

.quiz-container {
  max-width: 600px;
  margin: 0 auto;
}

.quiz-question {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.dark-mode .quiz-question {
  border-color: #444;
}

.question-text {
  font-weight: 600;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.answer-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.answer-options button {
  padding: 10px 15px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  flex: 1;
  min-width: 100px;
}

.dark-mode .answer-options button {
  background: #444;
  border-color: #555;
  color: #e0e0e0;
}

.answer-options button:hover:not(:disabled) {
  background: #e8e8e8;
}

.dark-mode .answer-options button:hover:not(:disabled) {
  background: #555;
}

.answer-options button.selected {
  background: #d9e8ff;
  border-color: #6A11CB;
  font-weight: 500;
}

.dark-mode .answer-options button.selected {
  background: #2a3a59;
  border-color: #a17edd;
}

.answer-options button.correct {
  background: #d4edda;
  border-color: #28a745;
  color: #155724;
}

.dark-mode .answer-options button.correct {
  background: #1e3e2f;
  border-color: #28a745;
  color: #8fd19e;
}

.answer-options button.incorrect {
  background: #f8d7da;
  border-color: #dc3545;
  color: #721c24;
}

.dark-mode .answer-options button.incorrect {
  background: #3e1f24;
  border-color: #dc3545;
  color: #eb8c95;
}

.answer-feedback {
  padding: 10px 15px;
  border-radius: 6px;
  font-weight: 500;
}

.check-answers-btn {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  display: block;
  margin: 20px auto 10px;
}

.quiz-results {
  text-align: center;
  margin: 20px 0;
  padding: 15px;
  background: #d9e8ff;
  border-radius: 6px;
  font-weight: 600;
}

.dark-mode .quiz-results {
  background: #2a3a59;
}

.key-takeaways {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.dark-mode .key-takeaways {
  background: #333;
}

.key-takeaways h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.dark-mode .key-takeaways h3 {
  color: #a17edd;
}

.key-takeaways ul {
  padding-left: 20px;
}

.key-takeaways li {
  margin-bottom: 8px;
}

.ai-help-section {
  margin-top: 40px;
}

.ai-help-section h3 {
  color: #6A11CB;
  margin-bottom: 10px;
}

.dark-mode .ai-help-section h3 {
  color: #a17edd;
}

.ai-input {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  margin-bottom: 20px;
}

.ai-input textarea {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
}

.dark-mode .ai-input textarea {
  background: #333;
  border-color: #555;
  color: #e0e0e0;
}

.ai-input button {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
}

.ai-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.ai-loading {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 20px;
}

.dark-mode .ai-loading {
  background: #333;
}

.loading-spinner {
  width: 25px;
  height: 25px;
  border: 3px solid rgba(106, 17, 203, 0.3);
  border-radius: 50%;
  border-top-color: #6A11CB;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.ai-response {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 20px;
  line-height: 1.7;
}

.dark-mode .ai-response {
  background: #333;
}

/* Theme-specific styles */
.calm-blue h2, .calm-blue h3 {
  color: #3a7bd5;
}

.soft-beige h2, .soft-beige h3 {
  color: #b3825c;
}

/* Transition animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .learning-module {
    flex-direction: column;
  }
  
  .agenda-panel {
    flex: none;
  }
  
  .planet-features {
    grid-template-columns: 1fr;
  }
  
  .ai-input {
    flex-direction: column;
  }
}
</style>