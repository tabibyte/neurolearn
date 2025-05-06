<template>
  <div class="ai-assistant">
    <h1>AI Learning Assistant</h1>
    
    <div class="assistant-container">
      <div class="chat-area">
        <div class="messages" ref="messagesContainer">
          <!-- Welcome message -->
          <div class="message ai">
            <div class="message-content">
              <p>👋 Hello! I'm your NeuroLearn AI Assistant powered by Gemini.</p>
              <p>I can help you with:</p>
              <ul>
                <li>Explaining complex topics in simpler terms</li>
                <li>Creating visual explanations for concepts</li>
                <li>Adapting learning material to your preferences</li>
                <li>Answering questions about your learning resources</li>
              </ul>
              <p>How can I assist you with your learning today?</p>
            </div>
          </div>
          
          <!-- Dynamic messages -->
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            :class="['message', message.sender]"
          >
            <div class="message-content" v-html="formatMessage(message.text)"></div>
          </div>
          
          <!-- Loading indicator -->
          <div class="message ai" v-if="isLoading">
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="input-area">
          <textarea 
            v-model="userInput"
            @keydown.enter.prevent="sendMessage"
            placeholder="Type your question or request here..."
            rows="2"
          ></textarea>
          <button 
            @click="sendMessage" 
            :disabled="!userInput.trim() || isLoading"
            class="send-btn"
          >
            Send
          </button>
        </div>
      </div>
      
      <div class="features-panel">
        <h3>Learning Preferences</h3>
        <div class="preferences">
          <label>
            <input type="checkbox" v-model="preferences.visualAids">
            Include visual aids
          </label>
          
          <label>
            <input type="checkbox" v-model="preferences.simplifiedLanguage">
            Use simplified language
          </label>
          
          <label>
            <input type="checkbox" v-model="preferences.structuredFormat">
            Structure content with clear steps
          </label>
        </div>
        
        <h3>Example Prompts</h3>
        <div class="example-prompts">
          <button 
            v-for="(prompt, index) in examplePrompts" 
            :key="index"
            @click="useExamplePrompt(prompt)"
            class="prompt-btn"
          >
            {{ prompt }}
          </button>
        </div>
      </div>
    </div>
    
    <p class="note">
      Note: This is a demo version of the AI Assistant. 
      In the production version, we'll integrate fully with Gemini AI.
      For now, the responses are simulated.
    </p>
  </div>
</template>

<script>
export default {
  name: 'AIAssistant',
  data() {
    return {
      userInput: '',
      messages: [],
      isLoading: false,
      preferences: {
        visualAids: false,
        simplifiedLanguage: false,
        structuredFormat: false
      },
      examplePrompts: [
        "Explain photosynthesis in simple terms",
        "Help me understand fractions",
        "Create a study plan for algebra",
        "Summarize the water cycle"
      ]
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return
      
      // Add user message
      this.messages.push({
        sender: 'user',
        text: this.userInput
      })
      
      const userQuestion = this.userInput
      this.userInput = ''
      this.isLoading = true
      
      // Simulate API delay
      setTimeout(() => {
        // In a real implementation, this would call the Gemini API
        // through our backend
        const aiResponse = this.simulateAIResponse(userQuestion)
        
        this.messages.push({
          sender: 'ai',
          text: aiResponse
        })
        
        this.isLoading = false
        this.$nextTick(() => this.scrollToBottom())
      }, 1500)
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      container.scrollTop = container.scrollHeight
    },
    
    useExamplePrompt(prompt) {
      this.userInput = prompt
    },
    
    simulateAIResponse(question) {
      // This is a placeholder function that simulates AI responses
      // In the real implementation, we would call our backend API
      // which would then use Gemini API
      
      let response = ''
      
      if (question.toLowerCase().includes('photosynthesis')) {
        response = `<h3>Photosynthesis Explained</h3>
          <p>Photosynthesis is how plants make their food. Here's the simple version:</p>
          <ol>
            <li>Plants take in sunlight through their leaves</li>
            <li>They absorb water through their roots</li>
            <li>They take in carbon dioxide from the air</li>
            <li>Using these ingredients, they create sugar (food) and oxygen</li>
          </ol>
          <p>The oxygen is released into the air, and we breathe it!</p>`
          
        if (this.preferences.visualAids) {
          response += `<div class="visual-aid">
            <p>[Diagram: Sunlight → Leaf → (Water + CO2) → Sugar + Oxygen]</p>
          </div>`
        }
      } 
      else if (question.toLowerCase().includes('fractions')) {
        response = `<h3>Understanding Fractions</h3>
          <p>A fraction represents a part of a whole. The bottom number (denominator) tells you how many parts the whole is divided into. The top number (numerator) tells you how many of those parts you have.</p>
          <p>For example, in 3/4:</p>
          <ul>
            <li>4 (denominator) means the whole is divided into 4 equal parts</li>
            <li>3 (numerator) means we have 3 of those parts</li>
          </ul>`
          
        if (this.preferences.visualAids) {
          response += `<div class="visual-aid">
            <p>[Diagram: Circle divided into 4 parts with 3 colored in]</p>
          </div>`
        }
      }
      else {
        response = `<p>I'd be happy to help with "${question}".</p>
          <p>This is a demo version of the AI Assistant. In the full version, I would provide a complete, personalized response using Gemini AI.</p>
          <p>The actual implementation will connect to the Gemini API through our FastAPI backend to generate helpful, adapted learning content.</p>`
      }
      
      if (this.preferences.simplifiedLanguage) {
        response += `<div class="note">
          <p><strong>Simplified Version:</strong> I've used simpler words and shorter sentences to make this easier to understand.</p>
        </div>`
      }
      
      return response
    },
    
    formatMessage(text) {
      // Simple formatting function that preserves HTML
      // In a production app, you'd want to sanitize this
      return text
    }
  },
  mounted() {
    this.scrollToBottom()
  }
}
</script>

<style scoped>
.ai-assistant {
  max-width: 1200px;
  margin: 0 auto;
}

.assistant-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1.5rem;
  margin: 2rem 0;
}

.chat-area {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 600px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.message {
  margin-bottom: 1rem;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message-content {
  max-width: 80%;
  padding: 1rem;
  border-radius: 8px;
}

.user .message-content {
  background-color: #6A11CB;
  color: white;
}

.ai .message-content {
  background-color: #f8f9fa;
  color: #333;
}

.input-area {
  padding: 1rem;
  border-top: 1px solid #f1f1f1;
  display: flex;
  gap: 0.5rem;
}

textarea {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: none;
  font-family: inherit;
}

.send-btn {
  background-color: #6A11CB;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.send-btn:hover {
  background-color: #5900b3;
}

.send-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.features-panel {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.preferences {
  margin-bottom: 2rem;
}

.preferences label {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  cursor: pointer;
}

.preferences input {
  margin-right: 0.5rem;
}

.example-prompts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.prompt-btn {
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: left;
  cursor: pointer;
  transition: background-color 0.2s;
}

.prompt-btn:hover {
  background-color: #e9ecef;
}

.typing-indicator {
  display: flex;
  padding: 0.5rem 0;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  border-radius: 50%;
  background-color: #6c757d;
  margin-right: 5px;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.visual-aid {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #e9ecef;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  text-align: center;
}

.note {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  margin-top: 2rem;
}
</style>