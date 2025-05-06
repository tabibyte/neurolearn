<template>
  <div class="adhd-container">
    <div class="page-header">
      <h1>DEHB Öğrenme Araçları</h1>
      <p>Odaklanma, organizasyon ve verimli öğrenme için araçlar</p>
    </div>
    
    <div class="content-section">
      <div class="learning-tools">

        <div class="focus-panel">
          <div class="pomodoro-timer">
            <h3>Odaklanma Zamanlayıcısı</h3>
            
            <div class="timer-display">
              <div class="time">{{ formatTime }}</div>
              <div class="timer-label">{{ isBreak ? 'Mola Zamanı' : 'Odaklanma Zamanı' }}</div>
            </div>
            
            <div class="timer-controls">
              <button @click="startTimer" v-if="!timerActive">Başlat</button>
              <button @click="pauseTimer" v-else>Duraklat</button>
              <button @click="resetTimer">Sıfırla</button>
            </div>
            
            <div class="timer-settings">
              <div class="setting">
                <label>Odaklanma: {{ focusDuration }}dk</label>
                <input type="range" v-model="focusDuration" :disabled="timerActive" min="1" max="60">
              </div>
              <div class="setting">
                <label>Mola: {{ breakDuration }}dk</label>
                <input type="range" v-model="breakDuration" :disabled="timerActive" min="1" max="30">
              </div>
            </div>
          </div>
          
          <div class="task-manager">
            <h3>Görev Analizi</h3>
            
            <div class="task-input">
              <input 
                v-model="newTask" 
                @keyup.enter="addTask" 
                placeholder="Görev ekle..."
              >
              <button @click="addTask">+</button>
            </div>
            
            <div class="task-list">
              <div 
                v-for="(task, index) in tasks" 
                :key="index"
                class="task-item"
                :class="{ completed: task.completed }"
              >
                <label class="checkbox-container">
                  <input type="checkbox" v-model="task.completed">
                  <span class="checkmark"></span>
                </label>
                <span class="task-text">{{ task.text }}</span>
                <button @click="removeTask(index)" class="delete-btn">×</button>
              </div>
              
              <div v-if="tasks.length === 0" class="empty-tasks">
                Çalışmanızı bölmek için görevler ekleyin
              </div>
            </div>
          </div>
        </div>
        
        <div class="ai-assistant">
          <h2>Yapay Zeka Öğrenme Asistanı</h2>
          <p>Odaklanma, organizasyon ve öğrenme stratejileri konusunda kişiselleştirilmiş yardım alın</p>
          
          <div class="ai-input">
            <textarea 
              v-model="aiPrompt" 
              placeholder="Öğrenme materyaliniz için yardım isteyin, odaklanmak için stratejiler isteyin veya bilgileri organize etmek için yardım alın..."
              rows="5"
            ></textarea>
            
            <div class="ai-options">
              <div class="help-options">
                <button @click="applyTemplate('explain')" class="template-btn">Konuyu Açıkla</button>
                <button @click="applyTemplate('organize')" class="template-btn">Bilgiyi Düzenle</button>
                <button @click="applyTemplate('focus')" class="template-btn">Odaklanma İpuçları</button>
              </div>
              
              <div class="preferences">
                <label>
                  <input type="checkbox" v-model="aiPreferences.structured_format">
                  Yapılandırılmış format (liste, başlıklar vb.)
                </label>
                <label>
                  <input type="checkbox" v-model="aiPreferences.visual_aids">
                  Görsel destek öğeleri ekle
                </label>
              </div>
              
              <button 
                @click="getAIResponse" 
                :disabled="!aiPrompt.trim() || isLoadingAI"
                class="submit-btn"
              >
                Yardım Al
              </button>
            </div>
          </div>
          
          <div v-if="isLoadingAI" class="loading">
            <div class="loading-spinner"></div>
            <p>İsteğiniz işleniyor...</p>
          </div>
          
          <div v-if="aiResponse" class="ai-response">
            <h3>Yanıt</h3>
            <div class="response-content" v-html="aiResponse"></div>
            
            <div class="notes-integration">
              <button @click="saveToNotes" class="save-notes-btn">Notlara Kaydet</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="content-section" v-if="notes.trim()">
      <div class="notes-section">
        <div class="notes-header">
          <h2>Notlarınız</h2>
          <button @click="clearNotes" class="clear-btn">Temizle</button>
        </div>
        
        <textarea 
          v-model="notes" 
          placeholder="Önemli bilgileri buraya not alın..."
          rows="8"
        ></textarea>
        
        <div class="note-tips">
          <h4>DEHB için Not Alma İpuçları</h4>
          <ul>
            <li>Farklı konular için renk kodlaması kullanın</li>
            <li>Cümleleri kısa ve öz tutun</li>
            <li>Paragraflar yerine madde işaretleri kullanın</li>
            <li>Kavramları görselleştirmek için zihin haritaları oluşturun</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ADHD',
  data() {
    return {
      timerActive: false,
      isBreak: false,
      timeLeft: 0,
      focusDuration: 25,
      breakDuration: 5,
      timer: null,
      

      newTask: '',
      tasks: [],
      

      notes: '',
      

      aiPrompt: '',
      aiResponse: '',
      isLoadingAI: false,
      aiPreferences: {
        structured_format: true,
        visual_aids: false
      },
      templates: {
        explain: "Bu konuyu DEHB dostu bir şekilde Türkçe olarak açıklayabilir misiniz: ",
        organize: "Bu bilgileri yapılandırılmış bir formatta Türkçe olarak düzenlememde yardımcı olur musunuz: ",
        focus: "Şu konuda çalışırken odaklanma stratejilerini Türkçe olarak önerebilir misiniz: "
      }
    }
  },
  computed: {
    formatTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
  },
  methods: {
    startTimer() {
      if (!this.timerActive) {
        if (this.timeLeft === 0) {

          this.timeLeft = this.focusDuration * 60;
          this.isBreak = false;
        }
        
        this.timerActive = true;
        
        this.timer = setInterval(() => {
          if (this.timeLeft > 0) {
            this.timeLeft--;
          } else {

            this.playNotificationSound();
            
            if (this.isBreak) {

              this.timeLeft = this.focusDuration * 60;
              this.isBreak = false;
            } else {

              this.timeLeft = this.breakDuration * 60;
              this.isBreak = true;
            }
          }
        }, 1000);
      }
    },
    pauseTimer() {
      clearInterval(this.timer);
      this.timerActive = false;
    },
    resetTimer() {
      this.pauseTimer();
      this.timeLeft = this.focusDuration * 60;
      this.isBreak = false;
    },
    playNotificationSound() {

      const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
      audio.play();
    },
    addTask() {
      if (this.newTask.trim()) {
        this.tasks.push({
          text: this.newTask,
          completed: false
        });
        this.newTask = '';
      }
    },
    removeTask(index) {
      this.tasks.splice(index, 1);
    },
    applyTemplate(templateName) {
      if (this.templates[templateName]) {

        const prefix = this.aiPrompt.trim() ? this.aiPrompt + "\n\n" : "";
        

        this.aiPrompt = prefix + this.templates[templateName];
        

        if (!this.aiPrompt.includes("Türkçe")) {
          this.aiPrompt += " (Lütfen yanıtınızı Türkçe olarak verin.)";
        }
      }
    },
    async getAIResponse() {
      if (!this.aiPrompt.trim() || this.isLoadingAI) return;
      
      this.isLoadingAI = true;
      
      try {

        const prompt = `${this.aiPrompt}
        
        (Lütfen DEHB'li biri için yararlı olacak bir yanıt sağlayın - net yapı, özlü noktalar ve yararlı olduğu durumlarda görsel öğeler. Yanıtınızı kesinlikle Türkçe dilinde verin. Yanıtınızda HTML etiketlerinin açıklamalarını eklemeyin veya HTML yapısını açıklamayın.)`;
        
        const response = await axios.post('/api/assistant', {
          prompt: prompt,
          learning_preferences: {
            ...this.aiPreferences,
            simplified_language: true 
          },
          language: "tr" 
        });
        

        let cleanedResponse = response.data.response;
        

        cleanedResponse = cleanedResponse.replace(/```html/g, '');
        cleanedResponse = cleanedResponse.replace(/```/g, '');
        

        cleanedResponse = cleanedResponse.replace(/\*\*Clear headings:\*\* Each section starts with an.+?separation\./g, '');
        cleanedResponse = cleanedResponse.replace(/\*\*Simple language:\*\*.+?sentences\./g, '');
        cleanedResponse = cleanedResponse.replace(/\*\*Structured format:\*\*.+?information\./g, '');
        cleanedResponse = cleanedResponse.replace(/\*\*Visual aid suggestion:\*\*.+?accessibility\./g, '');
        cleanedResponse = cleanedResponse.replace(/\*\*Turkish language:\*\*.+?requested\./g, '');
        cleanedResponse = cleanedResponse.replace(/\*\*Focus on ADHD:\*\*.+?motivation\./g, '');
        cleanedResponse = cleanedResponse.replace(/This improved response.+?follow\./g, '');
        cleanedResponse = cleanedResponse.replace(/Remember to replace.+?sections\./g, '');
        cleanedResponse = cleanedResponse.replace(/This HTML provides:.+$/gs, '');
        
        this.aiResponse = cleanedResponse;
      } catch (error) {
        console.error('Yapay zeka yanıtı alınırken hata:', error);
        this.aiResponse = '<p>Üzgünüz, yanıt alınırken bir hata oluştu. Lütfen tekrar deneyin.</p>';
      } finally {
        this.isLoadingAI = false;
      }
    },
    saveToNotes() {
      if (!this.aiResponse) return;
      

      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = this.aiResponse;
      const textContent = tempDiv.textContent || tempDiv.innerText || '';
      

      const now = new Date();
      const timestamp = `${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;
      

      const notesToAdd = `--- YAPAY ZEKA YANITI (${timestamp}) ---\n\n${textContent}\n\n`;
      

      this.notes = this.notes.trim() ? this.notes + '\n\n' + notesToAdd : notesToAdd;
    },
    clearNotes() {
      if (confirm("Tüm notlarınızı temizlemek istediğinizden emin misiniz?")) {
        this.notes = '';
      }
    }
  },
  beforeUnmount() {

    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  mounted() {

    this.timeLeft = this.focusDuration * 60;
    

    const savedTasks = localStorage.getItem('adhd-tasks');
    if (savedTasks) {
      try {
        this.tasks = JSON.parse(savedTasks);
      } catch (e) {
        console.error('Kaydedilmiş görevler yüklenirken hata', e);
      }
    }
    

    const savedNotes = localStorage.getItem('adhd-notes');
    if (savedNotes) {
      this.notes = savedNotes;
    }
  },
  watch: {
    tasks: {
      handler(newTasks) {
        localStorage.setItem('adhd-tasks', JSON.stringify(newTasks));
      },
      deep: true
    },
    notes(newNotes) {
      localStorage.setItem('adhd-notes', newNotes);
    }
  }
}
</script>

<style scoped>
input, textarea, select {
  box-sizing: border-box;
  max-width: 100%;
}

.adhd-container {
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
  overflow: hidden;
  box-sizing: border-box;
}


.learning-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.focus-panel {
  flex: 1;
  min-width: 250px;
  max-width: 350px;
}

.ai-assistant {
  flex: 2;
  min-width: 400px;
}


.pomodoro-timer {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  text-align: center;
  margin-bottom: 20px;
}

.pomodoro-timer h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.timer-display {
  margin: 20px 0;
}

.time {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
}

.timer-label {
  font-size: 1.1rem;
  color: #666;
  margin-top: 5px;
}

.timer-controls {
  margin: 15px 0;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.timer-controls button {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.timer-controls button:hover {
  opacity: 0.9;
}

.timer-settings {
  margin-top: 15px;
}

.setting {
  margin-bottom: 10px;
}

.setting label {
  display: block;
  margin-bottom: 5px;
  font-size: 0.9rem;
  color: #666;
}

.setting input {
  width: 100%;
  max-width: 200px;
}


.task-manager {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.task-manager h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.task-input {
  display: flex;
  margin-bottom: 15px;
}

.task-input input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px 0 0 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.task-input button {
  width: 40px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  border-radius: 0 6px 6px 0;
  cursor: pointer;
  font-weight: 500;
  font-size: 18px;
}

.task-list {
  max-height: 250px;
  overflow-y: auto;
}

.task-item {
  display: flex;
  align-items: center;
  padding: 10px;
  background: #fff;
  border-radius: 6px;
  margin-bottom: 8px;
  transition: background-color 0.2s;
}

.task-item.completed .task-text {
  text-decoration: line-through;
  color: #888;
}

.task-item:hover {
  background-color: #f1f1f1;
}

.checkbox-container {
  display: block;
  position: relative;
  padding-left: 30px;
  cursor: pointer;
  user-select: none;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 18px;
  width: 18px;
  background-color: #eee;
  border-radius: 3px;
}

.checkbox-container:hover input ~ .checkmark {
  background-color: #ccc;
}

.checkbox-container input:checked ~ .checkmark {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.task-text {
  flex: 1;
  margin-left: 10px;
  font-size: 0.95rem;
}

.delete-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  padding: 0 5px;
}

.delete-btn:hover {
  color: #d33;
}

.empty-tasks {
  color: #888;
  text-align: center;
  padding: 15px 0;
  font-style: italic;
  font-size: 0.9rem;
}

/* AI Assistant - Main Focus Area */
.ai-assistant h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.ai-assistant > p {
  color: #666;
  margin-bottom: 20px;
  font-size: 1rem;
}

.ai-input {
  margin-bottom: 20px;
}

.ai-input textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px 8px 0 0;
  font-size: 16px;
  resize: vertical;
  min-height: 120px;
  border-bottom: none;
  box-sizing: border-box;
}

.ai-input textarea:focus {
  border-color: #6A11CB;
  outline: none;
}

.ai-options {
  background: #f8f9fa;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 0 0 8px 8px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  box-sizing: border-box;
}

.help-options {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.template-btn {
  background: #e9ecef;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 6px 12px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.template-btn:hover {
  background: #dee2e6;
}

.preferences {
  display: flex;
  gap: 15px;
}

.preferences label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.9rem;
}

.preferences input {
  margin-right: 6px;
}

.submit-btn {
  align-self: flex-end;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
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

.ai-response {
  padding: 20px;
  background: #f9f8ff;
  border-radius: 8px;
  margin-top: 20px;
  width: 100%;
  box-sizing: border-box;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.ai-response h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.response-content {
  line-height: 1.7;
}

.notes-integration {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.save-notes-btn {
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 8px 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s;
}

.save-notes-btn:hover {
  background: #e0e0e0;
}

/* Notes Section */
.notes-section {
  display: flex;
  flex-direction: column;
}

.notes-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.notes-header h2 {
  color: #6A11CB;
  margin: 0;
}

.clear-btn {
  background: none;
  border: 1px solid #ddd;
  border-radius: 20px;
  padding: 5px 12px;
  color: #666;
  cursor: pointer;
}

.clear-btn:hover {
  background: #f0f0f0;
}

.notes-section textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.note-tips {
  background: #f9f8ff;
  padding: 20px;
  border-radius: 8px;
}

.note-tips h4 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.note-tips ul {
  padding-left: 20px;
}

.note-tips li {
  margin-bottom: 10px;
  color: #555;
}

@media (max-width: 768px) {
  .learning-tools {
    flex-direction: column;
  }
  
  .focus-panel {
    max-width: 100%;
  }
  
  .ai-assistant {
    min-width: unset;
  }
  
  .help-options, .preferences {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>