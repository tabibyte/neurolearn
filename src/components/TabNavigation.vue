<template>
    <nav>
      <ul>
        <li
          v-for="tab in tabs"
          :key="tab"
          @click="selectTab(tab)"
          :class="{ active: tab === activeTab }"
        >
          {{ tab }}
        </li>
      </ul>
    </nav>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue'
  
  const props = defineProps({
    tabs: {
      type: Array,
      required: true
    },
    activeTab: {
      type: String,
      required: true
    }
  })
  
  const emit = defineEmits(['update:activeTab'])
  
  function selectTab(tab) {
    if (tab !== props.activeTab) {
      emit('update:activeTab', tab)
    }
  }
  </script>
  
  <style scoped>
  nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 1rem;
    border-bottom: 2px solid #e5e7eb;
  }
  
  nav li {
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    color: #4b5563;
    transition: color 0.2s;
    position: relative;
  }
  
  nav li:hover {
    color: #1f2937;
  }
  
  nav li.active {
    color: #4f46e5;
  }
  
  nav li.active::after {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    bottom: -2px;
    height: 2px;
    background-color: #4f46e5;
  }
  </style>
  