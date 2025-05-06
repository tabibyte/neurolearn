<template>
  <div class="home">
    <section class="hero">
      <h1>Welcome to NeuroLearn</h1>
      <p>A specialized learning platform designed for neurodivergent individuals</p>
      <div class="cta-buttons">
        <router-link to="/resources" class="btn primary">Explore Resources</router-link>
        <router-link to="/ai-assistant" class="btn secondary">AI Assistant</router-link>
      </div>
    </section>
    
    <section class="features">
      <h2>Our Platform Features</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <h3>Adaptable Content</h3>
          <p>Learning materials that adapt to different cognitive styles and preferences</p>
        </div>
        <div class="feature-card">
          <h3>AI-Powered Support</h3>
          <p>Gemini AI integration to provide personalized learning assistance</p>
        </div>
        <div class="feature-card">
          <h3>Visual Aids</h3>
          <p>Enhanced visual representations for complex concepts</p>
        </div>
        <div class="feature-card">
          <h3>Simplified Text</h3>
          <p>Text simplification options for different reading levels</p>
        </div>
      </div>
    </section>
    
    <section class="about">
      <h2>About NeuroLearn</h2>
      <p>
        NeuroLearn is designed to support neurodivergent learners including those with dyslexia, 
        autism, ADHD, and anxiety. Our platform provides customizable learning experiences that 
        adapt to individual needs and preferences, making education more accessible for everyone.
      </p>
    </section>
  </div>
</template>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 3rem 0;
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #666;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.primary {
  background-color: #6A11CB;
  color: white;
}

.primary:hover {
  background-color: #5900b3;
}

.secondary {
  background-color: #f8f9fa;
  color: #6A11CB;
  border: 1px solid #6A11CB;
}

.secondary:hover {
  background-color: #e9ecef;
}

.features {
  margin: 3rem 0;
}

.features h2 {
  text-align: center;
  margin-bottom: 2rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #6A11CB;
  margin-bottom: 0.5rem;
}

.about {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 3rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.about h2 {
  color: #333;
  margin-bottom: 1rem;
}

.about p {
  line-height: 1.8;
}
</style>