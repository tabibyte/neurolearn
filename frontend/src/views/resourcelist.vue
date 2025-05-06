<template>
  <div class="resource-list">
    <h1>Learning Resources</h1>
    
    <div class="actions">
      <button @click="showForm = !showForm" class="btn">
        {{ showForm ? 'Cancel' : 'Add New Resource' }}
      </button>
    </div>
    
    <div v-if="showForm" class="resource-form">
      <h2>Create New Learning Resource</h2>
      <form @submit.prevent="createResource">
        <div class="form-group">
          <label for="title">Title</label>
          <input 
            type="text" 
            id="title" 
            v-model="newResource.title" 
            required
          >
        </div>
        
        <div class="form-group">
          <label for="content">Content</label>
          <textarea 
            id="content" 
            v-model="newResource.content" 
            rows="6" 
            required
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="resourceType">Resource Type</label>
          <select id="resourceType" v-model="newResource.resource_type" required>
            <option value="text">Text</option>
            <option value="video">Video</option>
            <option value="interactive">Interactive</option>
            <option value="audio">Audio</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="difficultyLevel">Difficulty Level (1-5)</label>
          <input 
            type="number" 
            id="difficultyLevel" 
            v-model="newResource.difficulty_level"
            min="1"
            max="5"
          >
        </div>
        
        <div class="checkbox-group">
          <label>
            <input type="checkbox" v-model="newResource.has_visual_aids">
            Has Visual Aids
          </label>
          
          <label>
            <input type="checkbox" v-model="newResource.has_audio">
            Has Audio
          </label>
          
          <label>
            <input type="checkbox" v-model="newResource.has_simplified_text">
            Has Simplified Text
          </label>
          
          <label>
            <input type="checkbox" v-model="newResource.is_sample">
            Is Sample Resource
          </label>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn primary">Save Resource</button>
          <button type="button" @click="resetForm" class="btn">Reset</button>
        </div>
      </form>
    </div>
    
    <div v-if="loading" class="loading">
      Loading resources...
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-if="!loading && resources.length === 0" class="empty-state">
      <p>No learning resources available yet. Add your first resource!</p>
    </div>
    
    <div v-else class="resources-grid">
      <div 
        v-for="resource in resources" 
        :key="resource.id"
        class="resource-card"
      >
        <div class="resource-header">
          <h2>{{ resource.title }}</h2>
          <span class="badge">{{ resource.resource_type }}</span>
        </div>
        
        <div class="content-preview">
          {{ truncateContent(resource.content, 150) }}
        </div>
        
        <div class="resource-meta">
          <div class="difficulty" v-if="resource.difficulty_level">
            Difficulty: {{ resource.difficulty_level }}/5
          </div>
          
          <div class="tags">
            <span v-if="resource.has_visual_aids" class="tag">Visual</span>
            <span v-if="resource.has_audio" class="tag">Audio</span>
            <span v-if="resource.has_simplified_text" class="tag">Simplified</span>
            <span v-if="resource.is_sample" class="tag sample">Sample</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'ResourceList',
  data() {
    return {
      showForm: false,
      newResource: this.getEmptyResource()
    }
  },
  computed: {
    ...mapState(['resources', 'loading', 'error'])
  },
  methods: {
    ...mapActions(['fetchResources', 'createResource']),
    
    getEmptyResource() {
      return {
        title: '',
        content: '',
        resource_type: 'text',
        difficulty_level: 3,
        has_visual_aids: false,
        has_audio: false,
        has_simplified_text: false,
        is_sample: false
      }
    },
    
    async submitResource() {
      try {
        await this.createResource(this.newResource)
        this.resetForm()
        this.showForm = false
      } catch (error) {
        console.error('Failed to create resource:', error)
      }
    },
    
    resetForm() {
      this.newResource = this.getEmptyResource()
    },
    
    truncateContent(content, maxLength) {
      if (content.length <= maxLength) {
        return content
      }
      return content.substr(0, maxLength) + '...'
    }
  },
  created() {
    this.fetchResources()
  }
}
</script>

<style scoped>
.resource-list {
  max-width: 1200px;
  margin: 0 auto;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
}

.btn {
  background-color: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn:hover {
  background-color: #e9ecef;
}

.btn.primary {
  background-color: #6A11CB;
  color: white;
  border: none;
}

.btn.primary:hover {
  background-color: #5900b3;
}

.resource-form {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.checkbox-group {
  margin: 1.5rem 0;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  cursor: pointer;
}

.checkbox-group input {
  margin-right: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.resource-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.resource-card:hover {
  transform: translateY(-5px);
}

.resource-header {
  padding: 1rem;
  background-color: #f8f9fa;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.resource-header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.badge {
  background-color: #e9ecef;
  color: #495057;
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  text-transform: capitalize;
}

.content-preview {
  padding: 1rem;
  color: #495057;
  min-height: 100px;
}

.resource-meta {
  padding: 1rem;
  border-top: 1px solid #f1f1f1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.difficulty {
  font-size: 0.9rem;
  color: #6c757d;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  font-size: 0.7rem;
  background-color: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.tag.sample {
  background-color: #6A11CB;
  color: white;
}

.loading {
  text-align: center;
  padding: 2rem 0;
  color: #6c757d;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: #6c757d;
}
</style>