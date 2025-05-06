<template>
  <div class="adhd-container">
    <div class="page-header">
      <h1>ADHD Learning Tools</h1>
      <p>Focus-friendly study environment with built-in timers and structured learning</p>
    </div>
    
    <div class="content-section">
      <div class="focus-tools">
        <div class="pomodoro-timer">
          <h2>Pomodoro Focus Timer</h2>
          
          <div class="timer-display">
            <div class="time">{{ formatTime }}</div>
            <div class="timer-label">{{ isBreak ? 'Break Time' : 'Focus Time' }}</div>
          </div>
          
          <div class="timer-controls">
            <button @click="startTimer" v-if="!timerActive">Start</button>
            <button @click="pauseTimer" v-else>Pause</button>
            <button @click="resetTimer">Reset</button>
          </div>
          
          <div class="timer-settings">
            <div class="setting">
              <label>Focus Duration (minutes)</label>
              <input type="number" v-model="focusDuration" :disabled="timerActive" min="1" max="60">
            </div>
            <div class="setting">
              <label>Break Duration (minutes)</label>
              <input type="number" v-model="breakDuration" :disabled="timerActive" min="1" max="30">
            </div>
          </div>
        </div>
        
        <div class="task-manager">
          <h2>Task Breakdown</h2>
          <p>Break your study session into manageable chunks</p>
          
          <div class="task-input">
            <input 
              v-model="newTask" 
              @keyup.enter="addTask" 
              placeholder="Add a task..."
            >
            <button @click="addTask">Add</button>
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
              No tasks yet. Add some to get started!
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="content-section">
      <div class="study-workspace">
        <h2>Learning Workspace</h2>
        
        <div class="workspace-tabs">
          <button 
            @click="activeTab = 'notes'" 
            :class="{ active: activeTab === 'notes' }"
          >
            Notes
          </button>
          <button 
            @click="activeTab = 'resources'" 
            :class="{ active: activeTab === 'resources' }"
          >
            Study Materials
          </button>
          <button 
            @click="activeTab = 'ai'" 
            :class="{ active: activeTab === 'ai' }"
          >
            AI Assistant
          </button>
        </div>
        
        <div class="workspace-content">
          <div v-if="activeTab === 'notes'" class="notes-tab">
            <textarea 
              v-model="notes" 
              placeholder="Take your notes here. Try to use bullet points and clear headings to organize your thoughts."
              rows="10"
            ></textarea>
            <div class="note-tips">
              <h4>Note-Taking Tips for ADHD</h4>
              <ul>
                <li>Use color coding for different topics</li>
                <li>Keep sentences short and to the point</li>
                <li>Use bullet points instead of paragraphs</li>
                <li>Create mind maps to visualize concepts</li>
                <li>Take short breaks to stay focused</li>
              </ul>
            </div>
          </div>
          
          <div v-if="activeTab === 'resources'" class="resources-tab">
            <h3>Recommended Learning Resources</h3>
            <div class="resource-list">
              <div class="resource-card">
                <h4>Active Reading Strategies</h4>
                <p>Learn techniques to stay engaged with text materials</p>
                <button>View Resource</button>
              </div>
              <div class="resource-card">
                <h4>Visual Learning Tools</h4>
                <p>Mind mapping and visual organization techniques</p>
                <button>View Resource</button>
              </div>
              <div class="resource-card">
                <h4>Focus Training Exercises</h4>
                <p>Activities to improve attention span and concentration</p>
                <button>View Resource</button>
              </div>
            </div>
          </div>
          
          <div v-if="activeTab === 'ai'" class="ai-tab">
            <div class="ai-prompt">
              <h3>AI Learning Assistant</h3>
              <p>Ask for help with your learning material or get suggestions for focus strategies</p>
              
              <textarea 
                v-model="aiPrompt" 
                placeholder="Explain this topic, help me organize my notes, suggest focus strategies..."
                rows="4"
              ></textarea>
              
              <div class="ai-options">
                <button 
                  @click="getAIResponse" 
                  :disabled="!aiPrompt.trim() || isLoadingAI"
                >
                  Get Help
                </button>
                <div class="ai-preferences">
                  <label>
                    <input type="checkbox" v-model="aiPreferences.structured_format">
                    Structure response in clear steps
                  </label>
                  <label>
                    <input type="checkbox" v-model="aiPreferences.visual_aids">
                    Include visual descriptions
                  </label>
                </div>
              </div>
            </div>
            
            <div v-if="isLoadingAI" class="ai-loading">
              <div class="loading-spinner"></div>
              <p>Thinking...</p>
            </div>
            
            <div v-if="aiResponse" class="ai-response">
              <h3>Response</h3>
              <div class="response-content" v-html="aiResponse"></div>
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
  name: 'ADHD',
  data() {
    return {
      // Timer variables
      timerActive: false,
      isBreak: false,
      timeLeft: 0,
      focusDuration: 25,
      breakDuration: 5,
      timer: null,
      
      // Task management
      newTask: '',
      tasks: [],
      
      // Workspace variables
      activeTab: 'notes',
      notes: '',
      
      // AI assistant
      aiPrompt: '',
      aiResponse: '',
      isLoadingAI: false,
      aiPreferences: {
        structured_format: true,
        visual_aids: false
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
          // Initial state or reset state
          this.timeLeft = this.focusDuration * 60;
          this.isBreak = false;
        }
        
        this.timerActive = true;
        
        this.timer = setInterval(() => {
          if (this.timeLeft > 0) {
            this.timeLeft--;
          } else {
            // Time is up, toggle between focus and break
            this.playNotificationSound();
            
            if (this.isBreak) {
              // Break time over, start focus time
              this.timeLeft = this.focusDuration * 60;
              this.isBreak = false;
            } else {
              // Focus time over, start break
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
      // Simple browser notification sound
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
    async getAIResponse() {
      if (!this.aiPrompt.trim() || this.isLoadingAI) return;
      
      this.isLoadingAI = true;
      
      try {
        // Add ADHD context to help the AI provide more relevant responses
        const prompt = `${this.aiPrompt} (Please provide a response that's helpful for someone with ADHD - clear structure, concise points, visual elements where helpful)`;
        
        const response = await axios.post('/api/assistant', {
          prompt: prompt,
          learning_preferences: {
            ...this.aiPreferences,
            simplified_language: true // Always use clear language for ADHD
          }
        });
        
        this.aiResponse = response.data.response;
      } catch (error) {
        console.error('Error getting AI response:', error);
        this.aiResponse = '<p>Sorry, there was an error getting a response. Please try again.</p>';
      } finally {
        this.isLoadingAI = false;
      }
    }
  },
  beforeUnmount() {
    // Clean up timer when component is destroyed
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  mounted() {
    // Initialize timer
    this.timeLeft = this.focusDuration * 60;
    
    // Load saved tasks from localStorage if available
    const savedTasks = localStorage.getItem('adhd-tasks');
    if (savedTasks) {
      try {
        this.tasks = JSON.parse(savedTasks);
      } catch (e) {
        console.error('Error loading saved tasks', e);
      }
    }
    
    // Load saved notes if available
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
}

.focus-tools {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .focus-tools {
    grid-template-columns: 1fr;
  }
}

.pomodoro-timer {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
  text-align: center;
}

.pomodoro-timer h2 {
  color: #6A11CB;
  margin-bottom: 20px;
}

.timer-display {
  margin: 30px 0;
}

.time {
  font-size: 3rem;
  font-weight: 700;
  color: #333;
}

.timer-label {
  font-size: 1.2rem;
  color: #666;
  margin-top: 10px;
}

.timer-controls {
  margin: 20px 0;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.timer-controls button {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.timer-controls button:hover {
  opacity: 0.9;
}

.timer-settings {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.setting {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.setting label {
  margin-bottom: 5px;
  font-size: 0.9rem;
  color: #666;
}

.setting input {
  width: 60px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  text-align: center;
}

.task-manager {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.task-manager h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.task-manager p {
  color: #666;
  margin-bottom: 20px;
  font-size: 0.95rem;
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
}

.task-input button {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 0 6px 6px 0;
  cursor: pointer;
  font-weight: 500;
}

.task-list {
  max-height: 300px;
  overflow-y: auto;
}

.task-item {
  display: flex;
  align-items: center;
  padding: 12px;
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
  padding-left: 35px;
  cursor: pointer;
  font-size: 16px;
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
  height: 20px;
  width: 20px;
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
  left: 7px;
  top: 3px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.task-text {
  flex: 1;
  margin-left: 15px;
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
  padding: 20px 0;
  font-style: italic;
}

.study-workspace {
  padding: 10px;
}

.study-workspace h2 {
  color: #6A11CB;
  margin-bottom: 20px;
}

.workspace-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.workspace-tabs button {
  background: none;
  border: none;
  padding: 12px 25px;
  font-size: 16px;
  cursor: pointer;
  opacity: 0.7;
  position: relative;
}

.workspace-tabs button:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: transparent;
}

.workspace-tabs button.active {
  opacity: 1;
  font-weight: 600;
}

.workspace-tabs button.active:after {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
}

.workspace-content {
  min-height: 400px;
}

.notes-tab {
  display: flex;
  gap: 30px;
}

.notes-tab textarea {
  flex: 2;
  min-height: 300px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-size: 16px;
  line-height: 1.6;
}

.note-tips {
  flex: 1;
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

.resources-tab h3 {
  margin-bottom: 20px;
  color: #333;
}

.resource-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.resource-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  transition: transform 0.2s;
}

.resource-card:hover {
  transform: translateY(-5px);
}

.resource-card h4 {
  color: #6A11CB;
  margin-bottom: 8px;
}

.resource-card p {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 15px;
}

.resource-card button {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
}

.ai-tab {
  padding: 10px;
}

.ai-prompt {
  margin-bottom: 30px;
}

.ai-prompt h3 {
  margin-bottom: 5px;
  color: #333;
}

.ai-prompt p {
  color: #666;
  margin-bottom: 15px;
  font-size: 0.95rem;
}

.ai-prompt textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  resize: vertical;
  margin-bottom: 15px;
}

.ai-options {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.ai-options button {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
}

.ai-options button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.ai-preferences {
  display: flex;
  gap: 20px;
}

.ai-preferences label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.ai-preferences input {
  margin-right: 8px;
}

.ai-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
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
}

.ai-response h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.response-content {
  line-height: 1.7;
}

@media (max-width: 768px) {
  .notes-tab {
    flex-direction: column;
  }
  
  .ai-options {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>