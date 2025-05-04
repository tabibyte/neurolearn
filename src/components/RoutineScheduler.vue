<template>
    <div>
      <h2 class="text-lg font-semibold mb-3">Günlük Rutin</h2>
      <ul class="space-y-2">
        <li v-for="(step, idx) in steps" :key="idx" class="flex items-center">
          <span class="text-2xl mr-2">{{ step.icon }}</span>
          <span :class="step.done ? 'line-through text-gray-400' : ''">{{ step.text }}</span>
          <button @click="toggle(idx)" class="ml-auto px-2 py-1 bg-green-200 rounded text-sm">
            {{ step.done ? 'Geri Al' : 'Tamamlandı' }}
          </button>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { reactive } from 'vue'
  
  const steps = reactive([
    { icon: '🍽️', text: 'Kahvaltı yap', done: false },
    { icon: '📚', text: 'Ödev zaman', done: false },
    { icon: '🎨', text: 'Sanat etkinliği', done: false },
    { icon: '🚶', text: 'Kısa yürüyüş', done: false }
  ])
  
  function toggle(i) {
    steps[i].done = !steps[i].done
  }
  </script>
  
  <style scoped>
  /* İsterseniz ek stiller ekleyebilirsiniz */
  </style>
  