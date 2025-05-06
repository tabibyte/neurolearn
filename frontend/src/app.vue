<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/resources">Learning Resources</router-link> |
        <router-link to="/ai-assistant">AI Assistant</router-link>
      </nav>
      <div class="logo">
        <h1>NeuroLearn</h1>
        <p>Adaptive Learning for Everyone</p>
      </div>
    </header>
    
    <main>
      <router-view />
    </main>
    
    <footer>
      <p>&copy; 2025 NeuroLearn - A specialized learning platform for neurodivergent individuals</p>
    </footer>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: 'Open Sans', sans-serif;
  color: #333;
  background-color: #f9f9f9;
  line-height: 1.6;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background: linear-gradient(135deg, #6A11CB 0%, #2575FC 100%);
  color: white;
  padding: 1rem;
  text-align: center;
}

nav {
  padding: 1rem 0;
}

nav a {
  color: white;
  text-decoration: none;
  margin: 0 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

nav a:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

main {
  flex: 1;
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  width: 100%;
  box-sizing: border-box;
}

footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

.logo h1 {
  margin-bottom: 0.2rem;
}

.logo p {
  margin-top: 0;
  font-size: 0.9rem;
  opacity: 0.9;
}
</style>