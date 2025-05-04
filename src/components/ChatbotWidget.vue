<template>
    <div id="chatbot-widget">
      <button class="chat-button" @click="visible = !visible">💬</button>
      <div v-if="visible" class="chat-window">
        <div class="chat-header">Veli Asistanı</div>
        <div class="chat-body">
          <!-- Örnek statik öneri -->
          <p>Merhaba! Aşağıdan bir konu seçebilirsiniz:</p>
          <ul>
            <li @click="send('disleksi')">Disleksi Destek Önerileri</li>
            <li @click="send('otizm')">Otizm Rutini İpuçları</li>
            <li @click="send('anksiyete')">Anksiyete ile Baş Etme</li>
          </ul>
        </div>
        <div class="chat-input">
          <input v-model="msg" @keyup.enter="reply" placeholder="Mesaj yazın..." />
          <button @click="reply">Gönder</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const visible = ref(false)
  const msg = ref('')
  const history = ref([])
  
  function send(topic) {
    history.value.push({ from: 'bot', text: öneri(topic) })
  }
  function reply() {
    if (!msg.value) return
    history.value.push({ from: 'user', text: msg.value })
    history.value.push({ from: 'bot', text: öneri(msg.value) })
    msg.value = ''
  }
  
  function öneri(t) {
    if (t.includes('disleksi')) {
      return 'Satır vurgulayıcı ve sesli okuma araçlarını kullanın. Font boyutunu büyük tutun.'
    }
    if (t.includes('otizm')) {
      return 'Görsel rutin takvimi oluşturun ve her adıma simge ekleyin.'
    }
    if (t.includes('anksiyete')) {
      return '4-4-4-4 nefes egzersizini günlük uygulayın.'
    }
    return 'Özür dilerim, bu konuda henüz önerim yok.'
  }
  </script>
  