<template>
  <div class="dyscalculia-container">
    <div class="page-header">
      <h1>Dyscalculia Learning Tools</h1>
      <p>Visual and interactive math learning tools for dyscalculia</p>
    </div>
    
    <div class="content-section">
      <div class="math-tools">
        <h2>Visual Number Tools</h2>
        <p>Explore numbers with visual representations to build number sense</p>
        
        <div class="tools-tabs">
          <button 
            v-for="tab in toolTabs" 
            :key="tab.id"
            :class="{ active: activeToolTab === tab.id }"
            @click="activeToolTab = tab.id"
          >
            {{ tab.name }}
          </button>
        </div>
        
        <div class="tools-content">
          <!-- Number Line Tool -->
          <div v-if="activeToolTab === 'numberLine'" class="number-line-tool">
            <h3>Interactive Number Line</h3>
            <p>Visualize numbers and operations on a number line</p>
            
            <div class="number-line-controls">
              <div class="control-group">
                <label>Range</label>
                <div class="range-inputs">
                  <div class="number-input">
                    <label>From</label>
                    <input type="number" v-model.number="numberLineSettings.min" @change="updateNumberLine">
                  </div>
                  <div class="number-input">
                    <label>To</label>
                    <input type="number" v-model.number="numberLineSettings.max" @change="updateNumberLine">
                  </div>
                </div>
              </div>
              
              <div class="control-group">
                <label>Operations</label>
                <div class="operation-selection">
                  <button 
                    v-for="op in operations" 
                    :key="op.id"
                    :class="{ active: currentOperation === op.id }"
                    @click="currentOperation = op.id"
                  >
                    {{ op.symbol }}
                  </button>
                </div>
              </div>
              
              <div class="control-group">
                <label>Values</label>
                <div class="value-inputs">
                  <input type="number" v-model.number="operationValues.first" placeholder="First value">
                  <span class="operation-symbol">{{ currentOperationSymbol }}</span>
                  <input type="number" v-model.number="operationValues.second" placeholder="Second value">
                  <button class="calculate-btn" @click="calculateResult">Calculate</button>
                </div>
              </div>
            </div>
            
            <div class="number-line-visualization">
              <div class="number-line">
                <div class="line"></div>
                <div class="markers">
                  <div 
                    v-for="marker in numberLineMarkers" 
                    :key="marker.value"
                    class="marker"
                    :style="{ left: marker.position + '%' }"
                  >
                    <div class="mark"></div>
                    <div class="value">{{ marker.value }}</div>
                  </div>
                </div>
                
                <div 
                  v-if="showFirstValue && operationValues.first !== null" 
                  class="point first-value"
                  :style="{ left: firstValuePosition + '%' }"
                >
                  <div class="point-dot"></div>
                  <div class="point-label">{{ operationValues.first }}</div>
                </div>
                
                <div 
                  v-if="showResult && calculatedResult !== null" 
                  class="point result"
                  :style="{ left: resultPosition + '%' }"
                >
                  <div class="point-dot"></div>
                  <div class="point-label">Result: {{ calculatedResult }}</div>
                </div>
                
                <div 
                  v-if="showOperation && operationValues.second !== null && currentOperation === 'add'" 
                  class="operation-arrow"
                  :style="{ 
                    left: firstValuePosition + '%', 
                    width: operationArrowWidth + '%' 
                  }"
                >
                  <div class="arrow-line"></div>
                  <div class="arrow-head"></div>
                  <div class="arrow-label">+{{ operationValues.second }}</div>
                </div>
                
                <div 
                  v-if="showOperation && operationValues.second !== null && currentOperation === 'subtract'" 
                  class="operation-arrow reverse"
                  :style="{ 
                    left: resultPosition + '%', 
                    width: operationArrowWidth + '%' 
                  }"
                >
                  <div class="arrow-line"></div>
                  <div class="arrow-head"></div>
                  <div class="arrow-label">-{{ operationValues.second }}</div>
                </div>
              </div>
            </div>
          </div>
                    <!-- Counting Blocks Tool -->
          <div v-if="activeToolTab === 'countingBlocks'" class="counting-blocks-tool">
            <h3>Visual Counting Blocks</h3>
            <p>Use visual blocks to understand numbers and operations</p>
            
            <div class="blocks-controls">
              <div class="control-group">
                <label>Number of Blocks</label>
                <div class="counter-input">
                  <button @click="decrementBlocks" class="counter-btn">-</button>
                  <input type="number" v-model.number="blockCount" min="1" max="100">
                  <button @click="incrementBlocks" class="counter-btn">+</button>
                </div>
              </div>
              
              <div class="control-group">
                <label>Block Grouping</label>
                <div class="grouping-selection">
                  <button 
                    v-for="group in groupings" 
                    :key="group"
                    :class="{ active: blockGrouping === group }"
                    @click="blockGrouping = group"
                  >
                    {{ group }}
                  </button>
                </div>
              </div>
              
              <div class="control-group">
                <label>Block Color</label>
                <div class="color-selection">
                  <div 
                    v-for="color in blockColors" 
                    :key="color.value"
                    :class="['color-option', { active: selectedBlockColor === color.value }]"
                    :style="{ backgroundColor: color.value }"
                    @click="selectedBlockColor = color.value"
                  ></div>
                </div>
              </div>
            </div>
            
            <div class="blocks-visualization">
              <div class="total-count">Total: {{ blockCount }}</div>
              
              <div class="block-groups">
                <div 
                  v-for="(group, index) in visualBlocks" 
                  :key="index"
                  class="block-group"
                >
                  <div 
                    v-for="i in group" 
                    :key="`block-${index}-${i}`"
                    class="block"
                    :style="{ backgroundColor: selectedBlockColor }"
                  ></div>
                  
                  <div class="group-label" v-if="visualBlocks.length > 1">
                    {{ blockGrouping }} × {{ index + 1 }} = {{ blockGrouping * (index + 1) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Fraction Visualizer -->
          <div v-if="activeToolTab === 'fractions'" class="fractions-tool">
            <h3>Fraction Visualizer</h3>
            <p>Explore fractions with visual models</p>
            
            <div class="fraction-controls">
              <div class="control-group">
                <label>Fraction</label>
                <div class="fraction-input">
                  <input type="number" v-model.number="fraction.numerator" min="0" max="12" placeholder="Numerator">
                  <div class="fraction-divider"></div>
                  <input type="number" v-model.number="fraction.denominator" min="1" max="12" placeholder="Denominator">
                </div>
              </div>
              
              <div class="control-group">
                <label>Visualization Type</label>
                <div class="visualization-selection">
                  <button 
                    v-for="viz in fractionVisualizations" 
                    :key="viz.id"
                    :class="{ active: currentFractionViz === viz.id }"
                    @click="currentFractionViz = viz.id"
                  >
                    {{ viz.name }}
                  </button>
                </div>
              </div>
            </div>
            
            <div class="fraction-visualization">
              <div v-if="currentFractionViz === 'circle'" class="circle-visualization">
                <svg viewBox="0 0 100 100" width="200" height="200">
                  <g v-for="(slice, index) in fractionCircleSlices" :key="index">
                    <path 
                      :d="slice.path" 
                      :fill="index < fraction.numerator ? '#6A11CB' : '#e9e9e9'" 
                      stroke="#fff" 
                      stroke-width="1"
                    ></path>
                  </g>
                </svg>
                <div class="fraction-display">
                  {{ fraction.numerator }} / {{ fraction.denominator }} = {{ fractionDecimal.toFixed(2) }}
                </div>
              </div>
              
              <div v-if="currentFractionViz === 'bar'" class="bar-visualization">
                <div class="fraction-bar-container">
                  <div 
                    v-for="i in fraction.denominator" 
                    :key="`bar-${i}`"
                    class="bar-segment"
                    :class="{ filled: i <= fraction.numerator }"
                  ></div>
                </div>
                <div class="fraction-display">
                  {{ fraction.numerator }} / {{ fraction.denominator }} = {{ fractionDecimal.toFixed(2) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="content-section">
      <div class="dyscalculia-practice">
        <h2>Math Practice Zone</h2>
        <p>Practice math skills with dyscalculia-friendly exercises</p>
        
        <div class="practice-controls">
          <div class="skill-selection">
            <button 
              v-for="skill in practiceSkills" 
              :key="skill.id"
              :class="{ active: currentPracticeSkill === skill.id }"
              @click="setPracticeSkill(skill.id)"
            >
              {{ skill.name }}
            </button>
          </div>
          
          <div class="difficulty-selection">
            <label>Difficulty</label>
            <div class="difficulty-buttons">
              <button 
                v-for="level in difficultyLevels" 
                :key="level.id"
                :class="{ active: currentDifficulty === level.id }"
                @click="setDifficulty(level.id)"
              >
                {{ level.name }}
              </button>
            </div>
          </div>
        </div>
        
        <div class="practice-area">
          <div v-if="!practiceStarted" class="practice-start">
            <h3>{{ currentSkillName }} Practice</h3>
            <p>{{ currentSkillDescription }}</p>
            <button @click="startPractice" class="start-btn">Start Practice</button>
          </div>
          
          <div v-else class="practice-exercise">
            <div class="exercise-header">
              <h3>{{ currentSkillName }}</h3>
              <div class="score">Score: {{ score }} / {{ totalQuestions }}</div>
            </div>
            
            <div class="problem-container">
              <div class="problem">{{ currentProblem.question }}</div>
              
              <div class="visual-aid" v-if="showVisualAid">
                <div 
                  v-for="i in visualAidItems" 
                  :key="`aid-${i}`"
                  class="visual-item"
                  :style="{ backgroundColor: selectedBlockColor }"
                ></div>
              </div>
              
              <div class="answer-input">
                <input 
                  type="number" 
                  v-model.number="userAnswer" 
                  placeholder="Your answer..." 
                  @keyup.enter="checkAnswer"
                  ref="answerInput"
                >
                <button @click="checkAnswer" :disabled="userAnswer === null">Check</button>
              </div>
              
              <div v-if="showFeedback" :class="['feedback', feedbackClass]">
                {{ feedback }}
              </div>
              
              <button 
                v-if="showNextButton" 
                @click="nextQuestion" 
                class="next-btn"
              >
                Next Question
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="content-section">
      <div class="ai-support">
        <h2>AI Math Assistant</h2>
        <p>Get personalized help with math concepts and problems</p>
        
        <div class="ai-input">
          <textarea 
            v-model="aiPrompt" 
            placeholder="Describe a math problem you're working on, or ask for help with a math concept..."
            rows="3"
          ></textarea>
          
          <div class="ai-options">
            <button @click="getAIHelp" :disabled="!aiPrompt.trim() || isLoadingAI">
              Get Math Help
            </button>
            
            <div class="help-options">
              <label>
                <input type="checkbox" v-model="aiOptions.visual">
                Include visual explanations
              </label>
              <label>
                <input type="checkbox" v-model="aiOptions.stepByStep">
                Show step-by-step solution
              </label>
              <label>
                <input type="checkbox" v-model="aiOptions.simplified">
                Use simplified language
              </label>
            </div>
          </div>
        </div>
        
        <div v-if="isLoadingAI" class="loading">
          <div class="loading-spinner"></div>
          <p>Processing your request...</p>
        </div>
        
        <div v-if="aiResponse" class="ai-response">
          <h3>Math Assistant Response</h3>
          <div v-html="aiResponse"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dyscalculia',
  data() {
    return {
      // Tool tabs
      activeToolTab: 'numberLine',
      toolTabs: [
        { id: 'numberLine', name: 'Number Line' },
        { id: 'countingBlocks', name: 'Counting Blocks' },
        { id: 'fractions', name: 'Fractions' }
      ],
      
      // Number line tool state
      numberLineSettings: {
        min: 0,
        max: 10,
        step: 1
      },
      operations: [
        { id: 'add', symbol: '+' },
        { id: 'subtract', symbol: '-' },
        { id: 'multiply', symbol: '×' },
        { id: 'divide', symbol: '÷' }
      ],
      currentOperation: 'add',
      operationValues: {
        first: null,
        second: null
      },
      calculatedResult: null,
      numberLineMarkers: [],
      showFirstValue: false,
      showResult: false,
      showOperation: false,
      
      // Counting blocks tool state
      blockCount: 10,
      blockGrouping: 5,
      groupings: [2, 5, 10],
      blockColors: [
        { name: 'Purple', value: '#b19cd9' },
        { name: 'Blue', value: '#90caf9' },
        { name: 'Green', value: '#a5d6a7' },
        { name: 'Orange', value: '#ffcc80' }
      ],
      selectedBlockColor: '#b19cd9',
      
      // Fraction tool state
      fraction: {
        numerator: 3,
        denominator: 4
      },
      currentFractionViz: 'circle',
      fractionVisualizations: [
        { id: 'circle', name: 'Pie Chart' },
        { id: 'bar', name: 'Bar Model' }
      ],
      
      // Practice zone state
      practiceSkills: [
        { 
          id: 'numberSense', 
          name: 'Number Sense',
          description: 'Practice counting, comparing, and estimating numbers.'
        },
        { 
          id: 'addition', 
          name: 'Addition',
          description: 'Practice adding numbers with visual supports.'
        },
        { 
          id: 'subtraction', 
          name: 'Subtraction',
          description: 'Practice subtracting numbers with visual supports.'
        }
      ],
      currentPracticeSkill: 'numberSense',
      difficultyLevels: [
        { id: 'easy', name: 'Easy' },
        { id: 'medium', name: 'Medium' },
        { id: 'hard', name: 'Hard' }
      ],
      currentDifficulty: 'easy',
      practiceStarted: false,
      currentProblem: null,
      userAnswer: null,
      showFeedback: false,
      feedback: '',
      feedbackClass: '',
      score: 0,
      totalQuestions: 0,
      showNextButton: false,
      showVisualAid: true,
      visualAidItems: 0,
      
      // AI support
      aiPrompt: '',
      aiResponse: null,
      isLoadingAI: false,
      aiOptions: {
        visual: true,
        stepByStep: true,
        simplified: true
      }
    }
  },
  computed: {
    currentOperationSymbol() {
      const op = this.operations.find(o => o.id === this.currentOperation);
      return op ? op.symbol : '+';
    },
    firstValuePosition() {
      if (this.operationValues.first === null) return 0;
      return this.calculatePositionPercentage(this.operationValues.first);
    },
    resultPosition() {
      if (this.calculatedResult === null) return 0;
      return this.calculatePositionPercentage(this.calculatedResult);
    },
    operationArrowWidth() {
      if (this.currentOperation === 'add') {
        return Math.abs(this.calculatePositionPercentage(this.operationValues.second));
      } else if (this.currentOperation === 'subtract') {
        return Math.abs(this.calculatePositionPercentage(this.operationValues.second));
      }
      return 0;
    },
    visualBlocks() {
      if (this.blockCount <= 0 || this.blockGrouping <= 0) return [];
      
      const groups = [];
      const fullGroups = Math.floor(this.blockCount / this.blockGrouping);
      const remainder = this.blockCount % this.blockGrouping;
      
      // Add full groups
      for (let i = 0; i < fullGroups; i++) {
        groups.push(Array(this.blockGrouping).fill(1));
      }
      
      // Add remainder group if any
      if (remainder > 0) {
        groups.push(Array(remainder).fill(1));
      }
      
      return groups;
    },
    fractionDecimal() {
      if (this.fraction.denominator === 0) return 0;
      return this.fraction.numerator / this.fraction.denominator;
    },
    fractionCircleSlices() {
      const slices = [];
      const total = this.fraction.denominator || 1;
      const angle = 360 / total;
      
      for (let i = 0; i < total; i++) {
        const startAngle = i * angle - 90; // Start at top
        const endAngle = (i + 1) * angle - 90;
        
        const startRad = (startAngle * Math.PI) / 180;
        const endRad = (endAngle * Math.PI) / 180;
        
        const x1 = 50 + 40 * Math.cos(startRad);
        const y1 = 50 + 40 * Math.sin(startRad);
        const x2 = 50 + 40 * Math.cos(endRad);
        const y2 = 50 + 40 * Math.sin(endRad);
        
        const largeArcFlag = angle > 180 ? 1 : 0;
        
        const path = `M 50 50 L ${x1} ${y1} A 40 40 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;
        
        slices.push({ path });
      }
      
      return slices;
    },
    currentSkillName() {
      const skill = this.practiceSkills.find(s => s.id === this.currentPracticeSkill);
      return skill ? skill.name : '';
    },
    currentSkillDescription() {
      const skill = this.practiceSkills.find(s => s.id === this.currentPracticeSkill);
      return skill ? skill.description : '';
    }
  },
  methods: {
    updateNumberLine() {
      // Create markers based on range settings
      this.numberLineMarkers = [];
      const range = this.numberLineSettings.max - this.numberLineSettings.min;
      const step = Math.max(1, Math.floor(range / 10)); // Use at most 10 markers
      
      for (let i = this.numberLineSettings.min; i <= this.numberLineSettings.max; i += step) {
        this.numberLineMarkers.push({
          value: i,
          position: this.calculatePositionPercentage(i)
        });
      }
      
      // Always include max value as marker if not already included
      if ((this.numberLineSettings.max - this.numberLineSettings.min) % step !== 0) {
        this.numberLineMarkers.push({
          value: this.numberLineSettings.max,
          position: 100
        });
      }
    },
    calculatePositionPercentage(value) {
      const range = this.numberLineSettings.max - this.numberLineSettings.min;
      if (range === 0) return 0;
      
      return ((value - this.numberLineSettings.min) / range) * 100;
    },
    calculateResult() {
      if (this.operationValues.first === null || this.operationValues.second === null) {
        return;
      }
      
      const a = this.operationValues.first;
      const b = this.operationValues.second;
      
      switch (this.currentOperation) {
        case 'add':
          this.calculatedResult = a + b;
          break;
        case 'subtract':
          this.calculatedResult = a - b;
          break;
        case 'multiply':
          this.calculatedResult = a * b;
          break;
        case 'divide':
          this.calculatedResult = b !== 0 ? a / b : NaN;
          break;
      }
      
      // Show points and operation on number line
      this.showFirstValue = true;
      this.showResult = true;
      this.showOperation = true;
    },
    incrementBlocks() {
      this.blockCount = Math.min(100, this.blockCount + 1);
    },
    decrementBlocks() {
      this.blockCount = Math.max(1, this.blockCount - 1);
    },
    setPracticeSkill(skillId) {
      this.currentPracticeSkill = skillId;
      this.resetPractice();
    },
    setDifficulty(difficultyId) {
      this.currentDifficulty = difficultyId;
      this.resetPractice();
    },
    resetPractice() {
      this.practiceStarted = false;
      this.currentProblem = null;
      this.userAnswer = null;
      this.showFeedback = false;
      this.feedback = '';
      this.score = 0;
      this.totalQuestions = 0;
      this.showNextButton = false;
    },
    startPractice() {
      this.practiceStarted = true;
      this.generateProblem();
      this.totalQuestions = 0;
      this.score = 0;
    },
    generateProblem() {
      let problem = { question: '', answer: 0 };
      let visualItems = 0;
      
      // Generate problem based on skill and difficulty
      if (this.currentPracticeSkill === 'numberSense') {
        if (this.currentDifficulty === 'easy') {
          // Count objects (1-10)
          visualItems = Math.floor(Math.random() * 5) + 1;
          problem.question = `How many objects do you see?`;
          problem.answer = visualItems;
        } else if (this.currentDifficulty === 'medium') {
          // Count objects (5-20)
          visualItems = Math.floor(Math.random() * 15) + 5;
          problem.question = `How many objects do you see?`;
          problem.answer = visualItems;
        } else {
          // Compare numbers
          const a = Math.floor(Math.random() * 50) + 1;
          const b = Math.floor(Math.random() * 50) + 1;
          problem.question = `Which number is larger: ${a} or ${b}?`;
          problem.answer = Math.max(a, b);
          visualItems = 0; // No visual aid for this type
          this.showVisualAid = false;
        }
      } else if (this.currentPracticeSkill === 'addition') {
        let a, b;
        if (this.currentDifficulty === 'easy') {
          a = Math.floor(Math.random() * 5) + 1;
          b = Math.floor(Math.random() * 5) + 1;
        } else if (this.currentDifficulty === 'medium') {
          a = Math.floor(Math.random() * 10) + 1;
          b = Math.floor(Math.random() * 10) + 1;
        } else {
          a = Math.floor(Math.random() * 20) + 10;
          b = Math.floor(Math.random() * 20) + 10;
        }
        problem.question = `${a} + ${b} = ?`;
        problem.answer = a + b;
        visualItems = a + b;
      } else if (this.currentPracticeSkill === 'subtraction') {
        let a, b;
        if (this.currentDifficulty === 'easy') {
          b = Math.floor(Math.random() * 5) + 1;
          a = b + Math.floor(Math.random() * 5) + 1;
        } else if (this.currentDifficulty === 'medium') {
          b = Math.floor(Math.random() * 10) + 1;
          a = b + Math.floor(Math.random() * 10) + 1;
        } else {
          b = Math.floor(Math.random() * 20) + 5;
          a = b + Math.floor(Math.random() * 20) + 5;
        }
        problem.question = `${a} - ${b} = ?`;
        problem.answer = a - b;
        visualItems = a;
      }
      
      this.currentProblem = problem;
      this.visualAidItems = visualItems;
      this.showVisualAid = visualItems > 0;
      this.userAnswer = null;
      this.showFeedback = false;
      this.showNextButton = false;
      
      this.$nextTick(() => {
        if (this.$refs.answerInput) {
          this.$refs.answerInput.focus();
        }
      });
    },
    checkAnswer() {
      if (this.userAnswer === null) return;
      
      this.totalQuestions++;
      this.showFeedback = true;
      
      if (Number(this.userAnswer) === Number(this.currentProblem.answer)) {
        this.feedback = 'Correct! Well done!';
        this.feedbackClass = 'correct';
        this.score++;
      } else {
        this.feedback = `Not quite right. The correct answer is ${this.currentProblem.answer}.`;
        this.feedbackClass = 'incorrect';
      }
      
      this.showNextButton = true;
    },
    nextQuestion() {
      this.generateProblem();
    },
    async getAIHelp() {
      if (!this.aiPrompt.trim() || this.isLoadingAI) return;
      
      this.isLoadingAI = true;
      
      try {
        // Prepare prompt with dyscalculia context
        let prompt = this.aiPrompt;
        
        // Add instructions for the AI
        prompt = `${prompt} (Please provide a dyscalculia-friendly explanation with concrete examples and simple language)`;
        
        const response = await axios.post('/api/assistant', {
          prompt,
          learning_preferences: {
            visual_aids: this.aiOptions.visual,
            structured_format: this.aiOptions.stepByStep,
            simplified_language: this.aiOptions.simplified
          }
        });
        
        this.aiResponse = response.data.response;
      } catch (error) {
        console.error('Error getting AI help:', error);
        this.aiResponse = '<p>Sorry, there was an error processing your request. Please try again later.</p>';
      } finally {
        this.isLoadingAI = false;
      }
    }
  },
  mounted() {
    this.updateNumberLine();
  }
}
</script>

<style scoped>
.dyscalculia-container {
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

.math-tools h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.math-tools p {
  color: #666;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

.tools-tabs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.tools-tabs button {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: #f8f9fa;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s;
}

.tools-tabs button.active {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border-color: transparent;
}

/* Number line tool styles */
.number-line-tool h3, .counting-blocks-tool h3, .fractions-tool h3 {
  color: #6A11CB;
  margin-bottom: 10px;
}

.number-line-controls, .blocks-controls, .fraction-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 25px;
  margin-bottom: 30px;
}

.control-group {
  min-width: 180px;
}

.control-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 500;
}

.range-inputs {
  display: flex;
  gap: 15px;
}

.number-input {
  flex: 1;
}

.number-input label {
  font-size: 0.9rem;
  font-weight: normal;
  margin-bottom: 5px;
}

.number-input input, .value-inputs input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.operation-selection, .grouping-selection, .visualization-selection {
  display: flex;
  gap: 5px;
}

.operation-selection button, .grouping-selection button, .visualization-selection button {
  padding: 8px 12px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  flex: 1;
  font-size: 1rem;
  transition: all 0.2s;
}

.operation-selection button.active, 
.grouping-selection button.active, 
.visualization-selection button.active {
  background: #6A11CB;
  color: white;
  border-color: #6A11CB;
}

.value-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.operation-symbol {
  font-size: 1.2rem;
  font-weight: 500;
  width: 20px;
  text-align: center;
}

.calculate-btn {
  padding: 8px 15px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.number-line-visualization {
  margin-top: 20px;
  padding: 20px 0;
}

.number-line {
  position: relative;
  height: 100px;
  margin: 50px 10px 80px;
}

.line {
  position: absolute;
  top: 50px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #333;
}

.markers {
  position: relative;
}

.marker {
  position: absolute;
  transform: translateX(-50%);
}

.mark {
  width: 2px;
  height: 10px;
  background-color: #333;
  position: absolute;
  top: 46px;
  left: 0;
}

.value {
  position: absolute;
  top: 60px;
  width: 40px;
  text-align: center;
  transform: translateX(-50%);
}

.point {
  position: absolute;
  transform: translateX(-50%);
}

.point-dot {
  width: 12px;
  height: 12px;
  background-color: #6A11CB;
  border-radius: 50%;
  position: absolute;
  top: 46px;
  left: 0;
  transform: translate(-50%, -50%);
}

.first-value .point-dot {
  background-color: #2196F3;
}

.result .point-dot {
  background-color: #4CAF50;
}

.point-label {
  position: absolute;
  top: 25px;
  font-weight: 500;
  background: white;
  padding: 3px 8px;
  border-radius: 4px;
  white-space: nowrap;
  transform: translateX(-50%);
}

.first-value .point-label {
  color: #2196F3;
}

.result .point-label {
  color: #4CAF50;
}

.operation-arrow {
  position: absolute;
  top: 46px;
  height: 2px;
  background-color: transparent;
}

.arrow-line {
  height: 2px;
  background-color: #FF9800;
  width: 100%;
}

.arrow-head {
  position: absolute;
  right: -8px;
  top: -4px;
  width: 0;
  height: 0;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 8px solid #FF9800;
}

.reverse .arrow-head {
  right: auto;
  left: -8px;
  border-left: none;
  border-right: 8px solid #FF9800;
}

.arrow-label {
  position: absolute;
  top: -25px;
  right: 0;
  font-weight: 500;
  color: #FF9800;
  transform: translateX(50%);
  background: white;
  padding: 3px 8px;
  border-radius: 4px;
}

.reverse .arrow-label {
  right: auto;
  left: 0;
  transform: translateX(-50%);
}

/* Counting blocks tool styles */
.counter-input {
  display: flex;
  align-items: center;
}

.counter-btn {
  width: 32px;
  height: 32px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.counter-input input {
  width: 60px;
  height: 32px;
  text-align: center;
  border: 1px solid #ddd;
  border-left: none;
  border-right: none;
}

.color-selection {
  display: flex;
  gap: 10px;
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

.blocks-visualization {
  margin-top: 20px;
}

.total-count {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 15px;
  text-align: center;
}

.block-groups {
  display: flex;
  flex-wrap: wrap;
  gap: 25px;
  justify-content: center;
}

.block-group {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  max-width: 250px;
  background: #f8f8f8;
  padding: 15px;
  border-radius: 8px;
  position: relative;
}

.block {
  width: 30px;
  height: 30px;
  border-radius: 4px;
}

.group-label {
  position: absolute;
  bottom: -25px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}

/* Fraction tool styles */
.fraction-input {
  display: flex;
  align-items: center;
  gap: 5px;
  max-width: 150px;
}

.fraction-input input {
  width: 50px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.fraction-divider {
  width: 20px;
  height: 2px;
  background-color: #333;
}

.fraction-visualization {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.fraction-display {
  margin-top: 20px;
  font-size: 1.2rem;
  font-weight: 500;
}

.circle-visualization, .bar-visualization {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bar-visualization {
  width: 100%;
  max-width: 300px;
}

.fraction-bar-container {
  width: 100%;
  height: 40px;
  display: flex;
  margin-bottom: 20px;
}

.bar-segment {
  flex: 1;
  height: 100%;
  border: 1px solid white;
  background-color: #e9e9e9;
}

.bar-segment.filled {
  background-color: #6A11CB;
}

/* Practice zone styles */
.dyscalculia-practice h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.dyscalculia-practice > p {
  color: #666;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

.practice-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 30px;
}

.skill-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.skill-selection button, .difficulty-buttons button {
  padding: 10px 15px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.2s;
}

.skill-selection button.active, .difficulty-buttons button.active {
  background: #6A11CB;
  color: white;
  border-color: #6A11CB;
}

.difficulty-selection {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.difficulty-selection label {
  font-weight: 500;
}

.difficulty-buttons {
  display: flex;
  gap: 10px;
}

.practice-area {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 25px;
}

.practice-start {
  text-align: center;
  padding: 20px;
}

.practice-start h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

.practice-start p {
  margin-bottom: 25px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.start-btn {
  padding: 12px 25px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
}

.practice-exercise {
  padding: 10px;
}

.exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.exercise-header h3 {
  color: #6A11CB;
}

.score {
  background: #e3f2fd;
  padding: 5px 15px;
  border-radius: 20px;
  font-weight: 500;
  color: #1976d2;
}

.problem-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.problem {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 30px;
}

.visual-aid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-bottom: 30px;
}

.visual-item {
  width: 25px;
  height: 25px;
  border-radius: 3px;
}

.answer-input {
  display: flex;
  gap: 10px;
  max-width: 300px;
  margin: 0 auto;
}

.answer-input input {
  flex: 1;
  padding: 12px 15px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1.1rem;
  text-align: center;
}

.answer-input button, .next-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.feedback {
  margin: 20px auto;
  padding: 15px;
  border-radius: 6px;
  font-weight: 500;
  max-width: 400px;
}

.feedback.correct {
  background: #e8f5e9;
  color: #2e7d32;
}

.feedback.incorrect {
  background: #ffebee;
  color: #c62828;
}

.next-btn {
  margin-top: 20px;
}

/* AI support styles */
.ai-support h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.ai-support > p {
  color: #666;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

.ai-input {
  margin-bottom: 20px;
}

.ai-input textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-size: 1rem;
  margin-bottom: 15px;
}

.ai-options {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.ai-options button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
}

.ai-options button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.help-options {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.help-options label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
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

@media (max-width: 768px) {
  .number-line-controls, .blocks-controls, .fraction-controls {
    flex-direction: column;
    gap: 15px;
  }
  
  .practice-controls {
    flex-direction: column;
    gap: 15px;
  }
  
  .control-group {
    min-width: 0;
  }
  
  .skill-selection, .difficulty-buttons {
    justify-content: center;
  }
}
</style>