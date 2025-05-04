<template>
  <div id="app" :class="{ dark: darkMode }">
    <!-- Header with Title & Theme Toggle -->
    <header class="app-bar">
      <h1>Öğrenme Destek Asistanı</h1>
      <button class="theme-toggle" @click="toggleTheme">
        <span v-if="!darkMode">🌙</span>
        <span v-else>☀️</span>
      </button>
    </header>

    <!-- Animated Tabs -->
    <nav>
      <ul class="tabs">
        <transition-group name="tab" tag="ul" class="tabs-list">
          <li
            v-for="tab in tabs"
            :key="tab"
            @click="selectTab(tab)"
            :class="{ active: tab === activeTab }"
          >
            {{ tab }}
          </li>
        </transition-group>
      </ul>
    </nav>

    <!-- Module Panel with Slide-Fade Animation -->
    <transition name="slide-fade" mode="out-in">
      <component
        :is="activeComponent"
        :key="activeTab"
        class="module-panel"
      />
    </transition>

    <!-- Chatbot Widget -->
    <ChatbotWidget />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import TabNavigation from './components/TabNavigation.vue'
import ReadingPanel from './components/ReadingPanel.vue'
import RoutineScheduler from './components/RoutineScheduler.vue'
import BreathingExercise from './components/BreathingExercise.vue'
import ChatbotWidget from './components/ChatbotWidget.vue'

// Tabs & Active Component Mapping
const tabs = ['Disleksi', 'Otizm', 'Anksiyete']
const activeTab = ref(tabs[0])
const map = {
  Disleksi: ReadingPanel,
  Otizm: RoutineScheduler,
  Anksiyete: BreathingExercise
}
const activeComponent = computed(() => map[activeTab.value])

function selectTab(tab) {
  activeTab.value = tab
}

// Dark/Light Mode
const darkMode = ref(false)
function toggleTheme() {
  darkMode.value = !darkMode.value
}
</script>
