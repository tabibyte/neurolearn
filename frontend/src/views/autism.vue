<template>
  <div class="autism-container">
    <div class="page-header">
      <h1>Otizm Öğrenme Araçları</h1>
      <p>Öngörülebilir desenlerle yapılandırılmış öğrenme ve duyusal düzenlemeler</p>
    </div>
    
    <!-- Main AI Learning Assistant Section -->
    <div class="content-section">
      <div class="ai-learning-assistant">
        <h2>Yapay Zeka Öğrenme Asistanı</h2>
        <p>Otizm dostu formatlama ile herhangi bir konu hakkında kişiselleştirilmiş bilgi alın</p>
        
        <div class="ai-input-section">
          <textarea 
            v-model="aiPrompt" 
            placeholder="Hangi konu hakkında öğrenmek istersiniz? Bir soru sorun veya herhangi bir konu hakkında bilgi isteyin..."
            rows="4"
          ></textarea>
          
          <div class="ai-preferences">
            <div class="preferences-toggle" @click="showPreferences = !showPreferences">
              <span>Öğrenme Tercihler</span>
              <span class="toggle-icon">{{ showPreferences ? '▼' : '▶' }}</span>
            </div>
            
            <div v-if="showPreferences" class="preferences-panel">
              <div class="preference-item">
                <label>Metin Sunumu</label>
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
                    Parçalanmış
                  </button>
                  <button 
                    :class="{ active: settings.textChunking === 'highlighted' }"
                    @click="settings.textChunking = 'highlighted'"
                  >
                    Vurgulanmış
                  </button>
                </div>
              </div>
              
              <div class="preference-item">
                <label>Görsel Tema</label>
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
              
              <div class="preference-item">
                <label>Öğrenme Öğeleri</label>
                <div class="checkbox-options">
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="settings.showVisuals">
                    Görsel destekler ekle
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="settings.showAgenda">
                    Ajanda/yapı göster
                  </label>
                  <label class="checkbox-label">
                    <input type="checkbox" v-model="settings.showTransitions">
                    Net geçişler göster
                  </label>
                </div>
              </div>
            </div>
          </div>
          
          <button 
            @click="getAIExplanation" 
            :disabled="!aiPrompt.trim() || isLoadingAI"
            class="submit-btn"
          >
            Öğrenme İçeriği Oluştur
          </button>
        </div>
        
        <div v-if="isLoadingAI" class="loading">
          <div class="loading-spinner"></div>
          <p>Kişiselleştirilmiş öğrenme içeriği oluşturuluyor...</p>
        </div>
      </div>
    </div>
    
    <!-- AI Generated Learning Content Section -->
    <div v-if="aiResponse" class="content-section">
      <div class="learning-module" :class="settings.theme">
        <transition name="fade" v-if="settings.showAgenda && processedResponse && processedResponse.sections">
          <div class="agenda-panel" v-show="settings.showAgenda">
            <h3>Content Structure</h3>
            <ol class="agenda-list">
              <li 
                v-for="(section, index) in processedResponse.sections" 
                :key="index"
                :class="{ active: currentStep === index + 1 }"
                @click="currentStep = index + 1"
              >
                {{ section.title || `Section ${index + 1}` }}
              </li>
            </ol>
            
            <div class="progress-bar" v-if="processedResponse && processedResponse.sections">
              <div class="progress" :style="{ width: `${(currentStep / processedResponse.sections.length) * 100}%` }"></div>
            </div>
          </div>
        </transition>
        
        <div class="module-content">
          <div v-if="settings.showTransitions && transitionMessage" class="transition-message">
            {{ transitionMessage }}
          </div>
          
          <div class="step-navigator" v-if="processedResponse && processedResponse.sections && processedResponse.sections.length > 1">
            <button @click="previousStep" :disabled="currentStep === 1">Previous</button>
            <span class="step-indicator">Step {{ currentStep }} of {{ processedResponse.sections.length }}</span>
            <button @click="nextStep" :disabled="currentStep === processedResponse.sections.length">Next</button>
          </div>
          
          <div v-if="processedResponse" class="current-step-content">
            <div v-if="currentSection">
              <h2>{{ currentSection.title || 'Learning Content' }}</h2>
              
              <div class="content-block" :class="{ 'text-chunked': settings.textChunking === 'chunked' }">
                <div v-if="settings.textChunking !== 'highlighted'" v-html="currentSection.content"></div>
                <div v-else v-html="highlightContent(currentSection.content)"></div>
              </div>
              
              <div v-if="settings.showVisuals && currentSection.visualDesc" class="visual-support">
                <div class="image-placeholder">
                  <span>[{{ currentSection.visualDesc }}]</span>
                </div>
              </div>
              
              <div v-if="currentSection.definitions && currentSection.definitions.length > 0" class="definitions-section">
                <h3>Key Terms</h3>
                <div v-for="(def, index) in currentSection.definitions" :key="index" class="definition-box">
                  <strong>{{ def.term }}:</strong> {{ def.definition }}
                </div>
              </div>
            </div>
            
            <div v-if="currentStep === processedResponse.sections.length && processedResponse.summary" class="key-takeaways">
              <h3>Son</h3>
              <ul>
                <li v-for="(point, index) in processedResponse.summary" :key="index">{{ point }}</li>
              </ul>
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
        textChunking: 'normal',
        showVisuals: true,
        showAgenda: true,
        showTransitions: true
      },
      showPreferences: false,
      
      visualThemes: [
        { name: 'neutral', backgroundColor: '#ffffff', textColor: '#333333' },
        { name: 'calm-blue', backgroundColor: '#edf6ff', textColor: '#333333' },
        { name: 'soft-beige', backgroundColor: '#f7f3eb', textColor: '#333333' },
        { name: 'dark-mode', backgroundColor: '#222222', textColor: '#e0e0e0' }
      ],
      
      // AI content
      aiPrompt: '',
      aiResponse: null,
      processedResponse: null,
      isLoadingAI: false,
      
      // Learning module state
      currentStep: 1,
      transitionMessage: null,
    }
  },
  computed: {
    currentSection() {
      if (!this.processedResponse || !this.processedResponse.sections) return null;
      return this.processedResponse.sections[this.currentStep - 1];
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
        const prevSection = this.processedResponse.sections[this.currentStep - 2];
        this.showTransition(`Moving to: ${prevSection.title || 'Previous section'}`);
        this.currentStep -= 1;
      }
    },
    
    nextStep() {
      if (this.processedResponse && this.currentStep < this.processedResponse.sections.length) {
        const nextSection = this.processedResponse.sections[this.currentStep];
        this.showTransition(`Moving to: ${nextSection.title || 'Next section'}`);
        this.currentStep += 1;
      }
    },
    
    showTransition(message) {
      if (!this.settings.showTransitions) return;
      
      this.transitionMessage = message;
      setTimeout(() => {
        this.transitionMessage = null;
      }, 2000);
    },
    
    highlightContent(content) {
      // Find important concepts and add highlight spans
      // This is a simple implementation - AI could help identify key concepts
      
      // Extract key terms from definitions if available
      let keyTerms = [];
      if (this.currentSection && this.currentSection.definitions) {
        keyTerms = this.currentSection.definitions.map(def => def.term);
      }
      
      // If no definitions, use some basic heuristics to find keywords
      if (keyTerms.length === 0) {
        const commonWords = ['the', 'and', 'a', 'an', 'in', 'on', 'with', 'of', 'to', 'is', 'are'];
        const words = content.match(/\b\w+\b/g) || [];
        const wordFrequency = {};
        
        words.forEach(word => {
          const lowerWord = word.toLowerCase();
          if (!commonWords.includes(lowerWord) && lowerWord.length > 3) {
            wordFrequency[lowerWord] = (wordFrequency[lowerWord] || 0) + 1;
          }
        });
        
        keyTerms = Object.entries(wordFrequency)
          .filter(([, count]) => count > 1) // Fixed unused '_' variable
          .map(([word]) => word)
          .slice(0, 5);
      }
      
      // Apply highlights
      let highlightedContent = content;
      keyTerms.forEach(term => {
        // Use regex to replace with highlight spans, case insensitive
        const regex = new RegExp(`\\b${term}\\b`, 'gi');
        highlightedContent = highlightedContent.replace(regex, match => `<span class="highlight">${match}</span>`);
      });
      
      return highlightedContent;
    },
    
    async getAIExplanation() {
      if (!this.aiPrompt.trim() || this.isLoadingAI) return;
      
      this.isLoadingAI = true;
      this.aiResponse = null;
      this.processedResponse = null;
      this.currentStep = 1;
      
      try {
        const prompt = `
        Şu konu hakkında yapılandırılmış, otizm dostu bir öğrenme modülü oluşturun: ${this.aiPrompt}
        
        Yanıtınızı aşağıdaki yapıya sahip bir öğrenme kılavuzu olarak biçimlendirin:
        
        1. Konuya kısa bir giriş
        2. Konunun önemli kısımlarını açıklayan 2-4 ayrı bölüm
        3. Her bölüm için resimlendirebilecek görsel bir açıklama
        4. Her bölümdeki önemli tanımlar veya kavramlar
        5. Sonunda 3-5 ana noktayla bir özet
        
        Kesin dil kullanın, mecazlardan kaçının, somut örnekler kullanın ve net bir yapı sürdürün.
        Potansiyel olarak tanıdık olmayan terimler için tanımlar ekleyin.
        Yanıtınızı Türkçe olarak verin.
        `;
        
        const response = await axios.post('/api/assistant', {
          prompt: prompt,
          learning_preferences: {
            visual_aids: this.settings.showVisuals,
            structured_format: true,
            simplified_language: false 
          }
        });
        
        this.aiResponse = response.data.response;
        

        this.processAIResponse(this.aiResponse);
        
      } catch (error) {
        console.error('Error getting AI explanation:', error);
        this.aiResponse = '<p>Sorry, there was an error getting a response. Please try again.</p>';
      } finally {
        this.isLoadingAI = false;
      }
    },
    
    processAIResponse(response) {

      let cleanedResponse = response.replace(/```html/g, '').replace(/```/g, '');

      try {
        const sections = [];

        const headerMatches = cleanedResponse.match(/<h[1-3][^>]*>.*?<\/h[1-3]>/g) || [];
        let contentParts = cleanedResponse.split(/<h[1-3][^>]*>.*?<\/h[1-3]>/);
        

        if (contentParts[0].trim()) {
          sections.push({
            title: 'Giriş',
            content: contentParts[0].trim(),
            definitions: this.extractDefinitions(contentParts[0]),
            visualDesc: this.extractVisualDescription(contentParts[0])
          });
        }
        
        for (let i = 0; i < headerMatches.length; i++) {
          const headerText = headerMatches[i].replace(/<\/?h[1-3][^>]*>/g, '').trim();
          const content = contentParts[i + 1] || '';
          
          if (headerText.toLowerCase().includes('summary') || 
              headerText.toLowerCase().includes('takeaway') ||
              headerText.toLowerCase().includes('key point')) {
            continue;
          }
          
          sections.push({
            title: headerText,
            content: content.trim(),
            definitions: this.extractDefinitions(content),
            visualDesc: this.extractVisualDescription(content)
          });
        }
        
        // Extract summary points
        const summaryPoints = this.extractSummaryPoints(cleanedResponse);
        
        this.processedResponse = {
          sections: sections,
          summary: summaryPoints
        };
        
        console.log('Processed response:', this.processedResponse);
        
      } catch (error) {
        console.error('Error processing AI response:', error);

        this.processedResponse = {
          sections: [{
            title: 'Learning Content',
            content: cleanedResponse,
            definitions: [],
            visualDesc: null
          }],
          summary: []
        };
      }
    },
    
    extractDefinitions(content) {
      const definitions = [];
      
      const definitionRegex = /<strong>([^:]+):<\/strong>\s*([^<]+)/g;
      let match;
      
      while ((match = definitionRegex.exec(content)) !== null) {
        definitions.push({
          term: match[1].trim(),
          definition: match[2].trim()
        });
      }
      
      // Also look for definition boxes
      const defBoxRegex = /<div class="definition-box">\s*<strong>([^:]+):<\/strong>\s*([^<]+)/g;
      while ((match = defBoxRegex.exec(content)) !== null) {
        definitions.push({
          term: match[1].trim(),
          definition: match[2].trim()
        });
      }
      
      return definitions;
    },
    
    extractVisualDescription(content) {
      // Look for text in square brackets that might describe an image
      const visualRegex = /\[(.*?)]/g; // Fixed unnecessary escape character
      const matches = content.match(visualRegex);
      
      if (matches && matches.length > 0) {
        // Fix: Remove square brackets without unnecessary escape characters
        return matches[0].replace(/[[\]]/g, '');
      }
      
      // Alternative: look for text in parentheses containing visual words
      const visualWords = ['diagram', 'illustration', 'image', 'picture', 'visual'];
      const parenRegex = /\((.*?)\)/g;
      let match;
      
      while ((match = parenRegex.exec(content)) !== null) {
        const text = match[1].toLowerCase();
        if (visualWords.some(word => text.includes(word))) {
          return match[1];
        }
      }
      
      return null;
    },
    
    extractSummaryPoints(content) {
      // Look for a summary section
      const summaryRegex = /<h[1-3][^>]*>.*?(summary|key\s*points|takeaways).*?<\/h[1-3]>([\s\S]*?)(<h[1-3]|$)/i;
      const match = summaryRegex.exec(content);
      
      if (match && match[2]) {
        const summaryContent = match[2];
        
        // Extract points from bullet list
        const listItemRegex = /<li>(.*?)<\/li>/g;
        const points = [];
        let itemMatch;
        
        while ((itemMatch = listItemRegex.exec(summaryContent)) !== null) {
          points.push(itemMatch[1].trim());
        }
        
        // If no list items found, try to extract sentences
        if (points.length === 0) {
          const sentences = summaryContent.split(/[.!?]+/).filter(s => s.trim().length > 10);
          return sentences.map(s => s.trim()).slice(0, 5);
        }
        
        return points;
      }
      
      return [];
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

input, textarea, select {
  box-sizing: border-box;
  max-width: 100%;
}

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

/* AI Learning Assistant */
.ai-learning-assistant h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.ai-learning-assistant > p {
  color: #666;
  margin-bottom: 20px;
  font-size: 1rem;
}

.ai-input-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ai-input-section textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  min-height: 100px;
}

.ai-preferences {
  background: #f9f9f9;
  border-radius: 8px;
  overflow: hidden;
}

.preferences-toggle {
  padding: 12px 15px;
  cursor: pointer;
  background: #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 500;
}

.preferences-toggle:hover {
  background: #e8e8e8;
}

.preferences-panel {
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.preference-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.preference-item label {
  font-weight: 600;
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

.submit-btn {
  align-self: flex-end;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.submit-btn:hover {
  opacity: 0.9;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(106, 17, 203, 0.1);
  border-left-color: #6A11CB;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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
  cursor: pointer;
  transition: all 0.2s;
}

.agenda-list li:hover {
  color: #6A11CB;
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

.definitions-section {
  margin-top: 30px;
}

.definitions-section h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.dark-mode .definitions-section h3 {
  color: #a17edd;
}

.definition-box {
  background: #f8f9fa;
  border-left: 4px solid #6A11CB;
  padding: 15px;
  margin: 15px 0;
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
  padding: 20px;
}

.dark-mode .image-placeholder {
  background: #333;
  color: #bbb;
}

.key-takeaways {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin: 30px 0;
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
  
  .ai-input {
    flex-direction: column;
  }
  
  .submit-btn {
    align-self: center;
    width: 100%;
  }
}
</style>