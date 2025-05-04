<template>
    <div class="flex flex-col items-center">
      <h2 class="text-lg font-semibold mb-3">Nefes Egzersizi</h2>
      <div
        :style="{ width: size + 'px', height: size + 'px' }"
        class="rounded-full bg-indigo-100 mb-4 transition-all duration-400">
      </div>
      <button @click="startCycle" class="px-4 py-2 bg-indigo-500 text-white rounded">
        Başlat
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const size = ref(100)
  let phase = 0
  let interval
  
  function startCycle() {
    if (interval) clearInterval(interval)
    phase = 0
    size.value = 100
    interval = setInterval(() => {
      phase = (phase + 1) % 4
      // 0: nefes al → büyüt, 1: tut, 2: nefes ver → küçült, 3: tut
      size.value = phase === 0 ? 200 : phase === 2 ? 100 : size.value
    }, 4000)
  }
  </script>
  
  <style scoped>
  /* İsterseniz ekstra animasyon veya responsive ayar ekleyin */
  </style>
  