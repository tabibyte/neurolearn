<template>
  <div class="dyscalculia-container">
    <div class="page-header">
      <h1>Dyscalculia Learning Tools</h1>
      <p>Visual and interactive math learning tools for dyscalculia</p>
    </div>
    
    <!-- AI Math Assistant (Main Focus) -->
    <div class="content-section">
      <div class="ai-support">
        <h2>AI Math Assistant</h2>
        <p>Get personalized help with math concepts and problems</p>
        
        <div class="ai-input">
          <textarea 
            v-model="aiPrompt" 
            placeholder="Describe a math problem you're working on, or ask for help with a math concept..."
            rows="4"
          ></textarea>
          
          <div class="ai-options">
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
            
            <button @click="getAIHelp" :disabled="!aiPrompt.trim() || isLoadingAI">
              Get Math Help
            </button>
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
    
    <!-- Interactive Math Tools (Secondary) -->
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Dyscalculia',
  data() {
    return {
      // AI support variables
      aiPrompt: '',
      aiResponse: null,
      isLoadingAI: false,
      aiOptions: {
        visual: true,        // Include visual explanations by default
        stepByStep: true,    // Show step-by-step solutions by default
        simplified: false    // Use simplified language (optional)
      },
      
      // Math tools variables
      activeToolTab: 'numberLine',
      toolTabs: [
        { id: 'numberLine', name: 'Number Line' },
        { id: 'countingBlocks', name: 'Counting Blocks' },
        { id: 'fractions', name: 'Fractions' }
      ],
      
      // Number Line Tool
      numberLineSettings: {
        min: 0,
        max: 10
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
      
      // Counting Blocks Tool
      blockCount: 10,
      blockGrouping: 5,
      groupings: [1, 2, 5, 10],
      selectedBlockColor: '#6A11CB',
      blockColors: [
        { name: 'Purple', value: '#6A11CB' },
        { name: 'Blue', value: '#2575FC' },
        { name: 'Green', value: '#4CAF50' },
        { name: 'Orange', value: '#FF9800' }
      ],
      
      // Fraction Tool
      fraction: {
        numerator: 1,
        denominator: 2
      },
      currentFractionViz: 'circle',
      fractionVisualizations: [
        { id: 'circle', name: 'Pie Chart' },
        { id: 'bar', name: 'Bar Model' }
      ]
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
        const startPos = this.firstValuePosition;
        const endPos = this.resultPosition;
        return Math.abs(endPos - startPos);
      } else if (this.currentOperation === 'subtract') {
        const startPos = this.firstValuePosition;
        const endPos = this.resultPosition;
        return Math.abs(startPos - endPos);
      }
      return 0;
    },
    visualBlocks() {
      const groups = [];
      let remaining = this.blockCount;
      
      while (remaining > 0) {
        const groupSize = Math.min(this.blockGrouping, remaining);
        groups.push(groupSize);
        remaining -= groupSize;
      }
      
      return groups;
    },
    fractionDecimal() {
      return this.fraction.numerator / (this.fraction.denominator || 1);
    },
    fractionCircleSlices() {
      const slices = [];
      const denom = this.fraction.denominator || 1;
      const angleStep = 360 / denom;
      
      for (let i = 0; i < denom; i++) {
        const startAngle = i * angleStep;
        const endAngle = (i + 1) * angleStep;
        const path = this.describeArc(50, 50, 45, startAngle, endAngle);
        slices.push({ path });
      }
      
      return slices;
    }
  },
  methods: {
    updateNumberLine() {
      this.numberLineMarkers = [];
      const range = this.numberLineSettings.max - this.numberLineSettings.min;
      const step = range <= 20 ? 1 : Math.ceil(range / 10);
      
      for (let i = this.numberLineSettings.min; i <= this.numberLineSettings.max; i += step) {
        const position = this.calculatePositionPercentage(i);
        this.numberLineMarkers.push({
          value: i,
          position
        });
      }
    },
    
    calculatePositionPercentage(value) {
      const min = this.numberLineSettings.min;
      const max = this.numberLineSettings.max;
      const range = max - min;
      
      if (range === 0) return 50;
      
      return ((value - min) / range) * 100;
    },
    
    calculateResult() {
      if (this.operationValues.first === null || this.operationValues.second === null) {
        return;
      }
      
      const a = this.operationValues.first;
      const b = this.operationValues.second;
      
      switch(this.currentOperation) {
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
          this.calculatedResult = b !== 0 ? a / b : null;
          break;
      }
      
      this.showFirstValue = true;
      this.showResult = true;
      this.showOperation = true;
    },
    
    incrementBlocks() {
      if (this.blockCount < 100) {
        this.blockCount++;
      }
    },
    
    decrementBlocks() {
      if (this.blockCount > 1) {
        this.blockCount--;
      }
    },
    
    describeArc(x, y, radius, startAngle, endAngle) {
      const start = this.polarToCartesian(x, y, radius, endAngle);
      const end = this.polarToCartesian(x, y, radius, startAngle);
      const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
      
      return [
        "M", x, y,
        "L", start.x, start.y,
        "A", radius, radius, 0, largeArcFlag, 0, end.x, end.y,
        "Z"
      ].join(" ");
    },
    
    polarToCartesian(centerX, centerY, radius, angleInDegrees) {
      const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
      return {
        x: centerX + (radius * Math.cos(angleInRadians)),
        y: centerY + (radius * Math.sin(angleInRadians))
      };
    },
    
    async getAIHelp() {
      if (!this.aiPrompt.trim() || this.isLoadingAI) return;
      
      this.isLoadingAI = true;
      
      try {
        // Create a prompt that specifies the needs of someone with dyscalculia
        const prompt = `Please explain this math concept or solve this problem for someone with dyscalculia: ${this.aiPrompt}
        
        ${this.aiOptions.visual ? 'Include visual explanations using text-based diagrams or descriptions.' : ''}
        ${this.aiOptions.stepByStep ? 'Show all steps clearly with explanations for each step.' : ''}
        ${this.aiOptions.simplified ? 'Use simplified language and avoid complex math terminology where possible.' : ''}
        
        Focus on building number sense, make connections to real-world examples, and use concrete representations.`;
        
        const response = await axios.post('/api/assistant', {
          prompt: prompt,
          learning_preferences: {
            visual_aids: this.aiOptions.visual,
            structured_format: this.aiOptions.stepByStep,
            simplified_language: this.aiOptions.simplified
          }
        });
        
        // Clean up the response by removing code block markers
        let cleanedResponse = response.data.response;
        cleanedResponse = cleanedResponse.replace(/```html/g, '');
        cleanedResponse = cleanedResponse.replace(/```/g, '');
        
        this.aiResponse = cleanedResponse;
      } catch (error) {
        console.error('Error getting AI help:', error);
        this.aiResponse = '<p>Sorry, there was an error processing your request. Please try again.</p>';
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

input, textarea, select {
  box-sizing: border-box;
  max-width: 100%;
}

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

/* AI Math Assistant Section */
.ai-support h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.ai-support > p {
  color: #666;
  margin-bottom: 20px;
  font-size: 1rem;
}

.ai-input {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ai-input textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px 8px 0 0;
  resize: vertical;
  min-height: 120px;
  font-size: 16px;
}

.ai-options {
  background: #f8f9fa;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 0 0 8px 8px;
  border-top: none;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.help-options {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 10px;
}

.help-options label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.95rem;
}

.help-options label input {
  margin-right: 8px;
}

.ai-options button {
  align-self: flex-end;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s;
}

.ai-options button:hover {
  opacity: 0.9;
}

.ai-options button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.loading {
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

.loading p {
  color: #666;
}

.ai-response {
  margin-top: 25px;
  padding: 20px;
  background: #f9f8ff;
  border-radius: 8px;
  border-left: 4px solid #6A11CB;
}

.ai-response h3 {
  color: #6A11CB;
  margin-bottom: 15px;
}

/* Math Tools Section */
.math-tools h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.math-tools > p {
  color: #666;
  margin-bottom: 20px;
  font-size: 1rem;
}

.tools-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.tools-tabs button {
  padding: 10px 20px;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.tools-tabs button.active {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border-color: transparent;
}

.tools-content {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.tools-content h3 {
  color: #333;
  margin-bottom: 10px;
}

.tools-content p {
  color: #666;
  margin-bottom: 20px;
  font-size: 0.95rem;
}

/* Number Line Tool */
.number-line-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 30px;
}

.control-group {
  flex: 1;
  min-width: 200px;
}

.control-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 500;
  color: #555;
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
  color: #777;
  margin-bottom: 5px;
}

.number-input input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.operation-selection {
  display: flex;
  gap: 10px;
}

.operation-selection button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ddd;
  background: white;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.operation-selection button.active {
  background: #6A11CB;
  color: white;
  border-color: #6A11CB;
}

.value-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
}

.value-inputs input {
  width: 80px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.operation-symbol {
  font-size: 18px;
  font-weight: bold;
}

.calculate-btn {
  background: #6A11CB;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.number-line-visualization {
  margin-top: 30px;
  padding: 20px 10px;
}

.number-line {
  position: relative;
  height: 150px;
}

.line {
  position: absolute;
  top: 70px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #333;
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
  background: #333;
  margin-left: auto;
  margin-right: auto;
}

.value {
  text-align: center;
  margin-top: 5px;
  font-size: 0.9rem;
}

.point {
  position: absolute;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  top: 35px;
}

.point.result {
  top: 0;
}

.point-dot {
  width: 12px;
  height: 12px;
  background: #6A11CB;
  border-radius: 50%;
}

.point-label {
  margin-top: 5px;
  background: #6A11CB;
  color: white;
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 0.9rem;
  white-space: nowrap;
}

.operation-arrow {
  position: absolute;
  top: 55px;
  height: 2px;
  background: #2575FC;
}

.operation-arrow.reverse {
  transform: rotate(180deg);
  transform-origin: left center;
}

.arrow-line {
  width: 100%;
  height: 2px;
  background: #2575FC;
}

.arrow-head {
  position: absolute;
  right: -1px;
  top: -4px;
  width: 0;
  height: 0;
  border-top: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 10px solid #2575FC;
}

.arrow-label {
  position: absolute;
  top: -25px;
  width: 100%;
  text-align: center;
  color: #2575FC;
  font-weight: bold;
}

/* Counting Blocks Tool */
.blocks-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 30px;
}

.counter-input {
  display: flex;
  align-items: center;
}

.counter-btn {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.counter-input input {
  width: 60px;
  text-align: center;
  padding: 5px;
  margin: 0 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.grouping-selection {
  display: flex;
  gap: 10px;
}

.grouping-selection button {
  padding: 5px 15px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
}

.grouping-selection button.active {
  background: #6A11CB;
  color: white;
  border-color: #6A11CB;
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
  border: 2px solid transparent;
}

.color-option.active {
  border-color: #333;
  transform: scale(1.1);
}

.blocks-visualization {
  margin-top: 20px;
}

.total-count {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.block-groups {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.block-group {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
  position: relative;
  padding-bottom: 25px;
  max-width: 300px;
}

.block {
  width: 30px;
  height: 30px;
  border-radius: 5px;
}

.group-label {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  font-size: 0.9rem;
  color: #555;
}

/* Fraction Visualizer */
.fraction-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 30px;
}

.fraction-input {
  display: flex;
  align-items: center;
}

.fraction-input input {
  width: 60px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  text-align: center;
}

.fraction-divider {
  width: 20px;
  height: 2px;
  background: #333;
  margin: 0 5px;
}

.visualization-selection {
  display: flex;
  gap: 10px;
}

.visualization-selection button {
  padding: 8px 15px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
}

.visualization-selection button.active {
  background: #6A11CB;
  color: white;
  border-color: #6A11CB;
}

.fraction-visualization {
  margin-top: 30px;
  text-align: center;
}

.circle-visualization, .bar-visualization {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.fraction-bar-container {
  width: 300px;
  height: 40px;
  display: flex;
}

.bar-segment {
  flex: 1;
  height: 100%;
  background: #e9e9e9;
  border: 1px solid white;
}

.bar-segment.filled {
  background: #6A11CB;
}

.fraction-display {
  font-size: 18px;
  color: #333;
  margin-top: 10px;
}

/* Practice Zone */
.dyscalculia-practice h2 {
  color: #6A11CB;
  margin-bottom: 5px;
}

.dyscalculia-practice > p {
  color: #666;
  margin-bottom: 20px;
  font-size: 1rem;
}

.practice-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-bottom: 20px;
}

.skill-selection {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.skill-selection button {
  padding: 8px 16px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.2s;
}

.skill-selection button.active {
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
  color: #555;
}

.difficulty-buttons {
  display: flex;
  gap: 10px;
}

.difficulty-buttons button {
  padding: 6px 12px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
}

.difficulty-buttons button.active {
  background: #6A11CB;
  color: white;
  border-color: #6A11CB;
}

.practice-area {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.practice-start {
  text-align: center;
  padding: 30px;
}

.practice-start h3 {
  color: #333;
  margin-bottom: 10px;
}

.practice-start p {
  color: #666;
  margin-bottom: 20px;
}

.start-btn {
  padding: 12px 25px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
}

.practice-exercise {
  padding: 20px 0;
}

.exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.exercise-header h3 {
  color: #333;
  margin: 0;
}

.score {
  font-weight: 600;
  color: #6A11CB;
}

.problem-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.problem {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 30px;
}

.visual-aid {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  max-width: 500px;
  justify-content: center;
  margin-bottom: 30px;
}

.visual-item {
  width: 25px;
  height: 25px;
  border-radius: 5px;
}

.answer-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.answer-input input {
  width: 100px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.answer-input button {
  padding: 10px 20px;
  background: #6A11CB;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.answer-input button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.feedback {
  margin: 20px 0;
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: 500;
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
  padding: 10px 25px;
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .number-line-controls,
  .blocks-controls,
  .fraction-controls,
  .practice-controls {
    flex-direction: column;
    gap: 20px;
  }
  
  .range-inputs {
    flex-direction: column;
  }
  
  .value-inputs {
    flex-direction: column;
  }
  
  .block-groups {
    justify-content: center;
  }
  
  .ai-options {
    align-items: stretch;
  }
  
  .help-options {
    flex-direction: column;
  }
  
  .ai-options button {
    align-self: center;
    width: 100%;
  }
}
</style>