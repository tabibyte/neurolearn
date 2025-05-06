<template>
  <div class="dyslexia-container">
    <div class="page-header">
      <h1>Disleksi Öğrenme Araçları</h1>
      <p>Disleksi olan okuyucular için uyarlanmış kaynaklar ve araçlar</p>
    </div>
    
    <div class="content-section">
      <div class="reading-tools">
        <!-- Reading Settings Panel - Unchanged -->
        <div class="tool-controls">
          <h3>Okuma Ayarları</h3>
          
          <div class="control-group">
            <label>Yazı Fontu</label>
            <select v-model="settings.fontFamily">
              <option value="OpenDyslexic">OpenDyslexic</option>
              <option value="Arial">Arial</option>
              <option value="Comic Sans MS">Comic Sans MS</option>
              <option value="Verdana">Verdana</option>
            </select>
          </div>
          
          <div class="control-group">
            <label>Yazı Boyutu</label>
            <div class="slider-container">
              <input type="range" min="14" max="32" v-model="settings.fontSize">
              <span>{{ settings.fontSize }}px</span>
            </div>
          </div>
          
          <div class="control-group">
            <label>Satır Aralığı</label>
            <div class="slider-container">
              <input type="range" min="1" max="3" step="0.1" v-model="settings.lineSpacing">
              <span>{{ settings.lineSpacing }}</span>
            </div>
          </div>
          
          <div class="control-group">
            <label>Arka Plan Rengi</label>
            <div class="color-options">
              <div 
                v-for="color in backgroundColors" 
                :key="color.value"
                :class="['color-option', { active: settings.backgroundColor === color.value }]"
                :style="{ backgroundColor: color.value }"
                @click="settings.backgroundColor = color.value"
              ></div>
            </div>
          </div>
        </div>
        
        <!-- AI Reading Assistant (Replacing the sample text card) -->
        <div class="reading-input">
          <h3>Yapay Zeka Okuma Asistanı</h3>
          
          <textarea 
            v-model="userText" 
            placeholder="Seçtiğiniz ayarlarla görmek için metninizi buraya yapıştırın veya yazın..."
            rows="6"
          ></textarea>
          
          <div class="ai-options">
            <p>İsteğe bağlı: Bir yapay zeka işleme seçeneği seçin</p>
            <div class="radio-options">
              <label v-for="option in assistanceOptions" :key="option.id" class="radio-label">
                <input 
                  type="radio" 
                  name="aiOption" 
                  :value="option.id" 
                  v-model="selectedAIOption"
                >
                <span>{{ option.label }}</span>
              </label>
            </div>
          </div>
          
          <button 
            @click="processText" 
            class="submit-btn" 
            :disabled="!userText.trim() || isLoading"
          >
            Metni İşle
          </button>
        </div>
      </div>
    </div>
    
    <!-- Results Section -->
    <div class="content-section" v-if="processedText">
      <div class="results-section">
        <h2>Metniniz</h2>
        
        <div v-if="isLoading" class="loading">
          <div class="loading-spinner"></div>
          <p>İsteğiniz işleniyor...</p>
        </div>
        
        <div v-else class="processed-text" :style="readingStyle">
          <div v-html="processedText"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dyslexia',
  data() {
    return {
      settings: {
        fontFamily: 'OpenDyslexic',
        fontSize: 18,
        lineSpacing: 1.5,
        backgroundColor: '#f0f8ff'  // Light blue default
      },
      backgroundColors: [
        { name: 'Açık Mavi', value: '#f0f8ff' },
        { name: 'Krem', value: '#faf5e9' },
        { name: 'Nane', value: '#f1faee' },
        { name: 'Lavanta', value: '#f0e8fa' },
        { name: 'Beyaz', value: '#ffffff' }
      ],
      userText: '',
      processedText: '',
      isLoading: false,
      selectedAIOption: '', 
      assistanceOptions: [
        { id: 'simplify', label: 'Basitleştir' },
        { id: 'summarize', label: 'Özetle' },
        { id: 'explain', label: 'Zor Kelimeleri Açıkla' },
        { id: 'visualize', label: 'Görsel Hafıza Yardımcıları Oluştur' }
      ]
    }
  },
  computed: {
    readingStyle() {
      return {
        fontFamily: this.settings.fontFamily,
        fontSize: `${this.settings.fontSize}px`,
        lineHeight: this.settings.lineSpacing,
        backgroundColor: this.settings.backgroundColor,
        padding: '20px',
        borderRadius: '8px'
      }
    }
  },
  methods: {
    async processText() {
      if (!this.userText.trim() || this.isLoading) return;
      
      this.isLoading = true;
      

      if (!this.selectedAIOption) {
        this.processedText = `<p>${this.userText.replace(/\n/g, '</p><p>')}</p>`;
        this.isLoading = false;
        return;
      }
      
      try {
        let prompt = '';
        let preferences = {
          visual_aids: false,
          simplified_language: false,
          structured_format: false
        };
        
        switch(this.selectedAIOption) {
          case 'simplify':
            prompt = `Aşağıdaki metni disleksi olan bir okuyucu için daha kısa cümleler ve daha basit kelimeler kullanarak basitleştiriniz: "${this.userText}"`;
            preferences.simplified_language = true;
            break;
          case 'summarize':
            prompt = `Bu metnin ana noktalarını disleksi olan bir okuyucu için net ve yapılandırılmış bir şekilde özetleyiniz: "${this.userText}"`;
            preferences.structured_format = true;
            break;
          case 'explain':
            prompt = `Bu metindeki zor kelimeleri veya kavramları disleksi dostu bir şekilde belirleyiniz ve açıklayınız: "${this.userText}"`;
            preferences.simplified_language = true;
            break;
          case 'visualize':
            prompt = `Bu metindeki önemli bilgileri hatırlamaya yardımcı olacak metin tabanlı görsel hafıza yardımcıları veya anımsatıcı teknikler oluşturunuz: "${this.userText}"`;
            preferences.visual_aids = true;
            break;
        }
        

        prompt += " Lütfen yanıtınızı Türkçe olarak veriniz.";
        
        const response = await axios.post('/api/assistant', {
          prompt,
          learning_preferences: preferences,
          language: "tr" 
        });
        
        let cleanedResponse = response.data.response;
        cleanedResponse = cleanedResponse.replace(/```html/g, '');
        cleanedResponse = cleanedResponse.replace(/```/g, '');
        
        this.processedText = cleanedResponse;
      } catch (error) {
        console.error('Metin işlenirken hata oluştu:', error);
        this.processedText = '<p>Üzgünüz, isteğinizi işlerken bir hata oluştu. Lütfen daha sonra tekrar deneyin.</p>';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');

/* Special font for dyslexia - hosted locally or via CDN */
@font-face {
  font-family: 'OpenDyslexic';
  src: url('https://cdn.jsdelivr.net/npm/open-dyslexic@1.0.3/woff/OpenDyslexic-Regular.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}
</style>

<style scoped>

input, textarea, select {
  box-sizing: border-box;
  max-width: 100%;
}

.dyslexia-container {
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

.reading-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.tool-controls {
  flex: 1;
  min-width: 250px;
}

.tool-controls h3 {
  margin-bottom: 20px;
  color: #333;
}

.control-group {
  margin-bottom: 20px;
}

.control-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.control-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.slider-container input {
  flex: 1;
}

.slider-container span {
  min-width: 40px;
  text-align: right;
}

.color-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.color-option {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
  border: 2px solid transparent;
}

.color-option:hover {
  transform: scale(1.1);
}

.color-option.active {
  border-color: #6A11CB;
  transform: scale(1.1);
}

.reading-input {
  flex: 2;
  min-width: 300px;
}

.reading-input h3 {
  margin-bottom: 15px;
  color: #333;
}

.reading-input textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  resize: vertical;
  margin-bottom: 20px;
  font-size: 16px;
  min-height: 150px;
}

.ai-options {
  margin-bottom: 20px;
}

.ai-options p {
  margin-bottom: 10px;
  color: #666;
}

.radio-options {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 16px;
  background: #f8f8f8;
  border-radius: 25px;
  transition: all 0.2s;
}

.radio-label:hover {
  background: #f0f0f0;
}

.radio-label input {
  margin-right: 8px;
}

.radio-label input:checked + span {
  font-weight: 600;
  color: #6A11CB;
}

.submit-btn {
  padding: 12px 25px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
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

.results-section h2 {
  color: #6A11CB;
  margin-bottom: 20px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
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

.processed-text {
  line-height: 1.6;
}

@media (max-width: 768px) {
  .reading-tools {
    flex-direction: column;
  }
}
</style>