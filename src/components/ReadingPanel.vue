<template>
    <div>
      <div class="mb-4">
        <button @click="toggleFont" class="px-3 py-1 bg-gray-200 rounded">
          {{ isOpenDyslexic ? 'Lexend Fontu' : 'Disleksi Dostu Font' }}
        </button>
        <button @click="speakText" class="px-3 py-1 bg-indigo-500 text-white rounded ml-2">
          Sesli Oku
        </button>
      </div>
      <div
        ref="textContainer"
        :class="isOpenDyslexic ? 'open-dyslexic' : ''"
        @mousemove="highlightLine"
        class="p-4 border rounded max-h-64 overflow-y-auto"
      >
        <p v-for="(line, i) in lines" :key="i" :class="i === highlighted ? 'bg-yellow-100' : ''">
          {{ line }}
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const sample = `Disleksi, okuma ve yazma güçlüğüyle karakterize edilen yaygın bir öğrenme farklılığıdır. Bu modülde metin satırlarını vurgulayarak ve sesli okuma desteğiyle okuma deneyimini kolaylaştırıyoruz.`
  
  const lines = sample.split(/\n/)
  const highlighted = ref(null)
  const isOpenDyslexic = ref(false)
  const textContainer = ref(null)
  
  function toggleFont() {
    isOpenDyslexic.value = !isOpenDyslexic.value
  }
  
  function speakText() {
    const utter = new SpeechSynthesisUtterance(sample)
    speechSynthesis.speak(utter)
  }
  
  function highlightLine(e) {
    const children = textContainer.value.children
    for (let i = 0; i < children.length; i++) {
      const rect = children[i].getBoundingClientRect()
      if (e.clientY >= rect.top && e.clientY <= rect.bottom) {
        highlighted.value = i
        return
      }
    }
  }
  </script>
  