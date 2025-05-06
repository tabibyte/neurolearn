<template>
  <div id="app">
    <div class="sidebar">
      <div class="logo">
        <h1>NeuroLearn</h1>
      </div>
      <nav>
        <router-link to="/" exact>
          <i class="icon home-icon"></i>
          <span>Ana Sayfa</span>
        </router-link>
        <router-link to="/dyslexia">
          <i class="icon dyslexia-icon"></i>
          <span>Disleksi</span>
        </router-link>
        <router-link to="/adhd">
          <i class="icon adhd-icon"></i>
          <span>DEHB</span>
        </router-link>
        <router-link to="/autism">
          <i class="icon autism-icon"></i>
          <span>Otizm</span>
        </router-link>
        <router-link to="/dyscalculia">
          <i class="icon dyscalculia-icon"></i>
          <span>Diskalkuli</span>
        </router-link>
      </nav>
    </div>
    
    <main>
      <div class="content-area">
        <router-view />
      </div>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

body {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  color: #333;
  background-color: #f5f7fb;
  line-height: 1.6;
}

#app {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: white;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100%;
  z-index: 100;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #f1f1f1;
}

.logo h1 {
  margin: 0;
  color: #6A11CB;
  font-size: 24px;
}

nav {
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  flex: 1;
}

nav a {
  display: flex;
  align-items: center;
  color: #555;
  text-decoration: none;
  padding: 12px 25px;
  margin: 5px 0;
  border-radius: 0 30px 30px 0;
  transition: all 0.3s;
}

nav a.router-link-active {
  background: linear-gradient(135deg, rgba(106, 17, 203, 0.1) 0%, rgba(37, 117, 252, 0.1) 100%);
  color: #6A11CB;
  font-weight: 500;
}

nav a:hover {
  background-color: rgba(106, 17, 203, 0.05);
}

.icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
  display: inline-block;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0.7;
}

.home-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23555' viewBox='0 0 24 24'%3E%3Cpath d='M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z'/%3E%3C/svg%3E");
}

.dyslexia-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23555' viewBox='0 0 24 24'%3E%3Cpath d='M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2zm-4 4H9v-2h6v2zm4-8H9V5h10v2z'/%3E%3C/svg%3E");
}

.adhd-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23555' viewBox='0 0 24 24'%3E%3Cpath d='M13.5.67s.74 2.65.74 4.8c0 2.06-1.35 3.73-3.41 3.73-2.07 0-3.63-1.67-3.63-3.73l.03-.36C5.21 7.51 4 10.62 4 14c0 4.42 3.58 8 8 8s8-3.58 8-8C20 8.61 17.41 3.8 13.5.67zM11.71 19c-1.78 0-3.22-1.4-3.22-3.14 0-1.62 1.05-2.76 2.81-3.12 1.77-.36 3.6-1.21 4.62-2.58.39 1.29.59 2.65.59 4.04 0 2.65-2.15 4.8-4.8 4.8z'/%3E%3C/svg%3E");
}

.autism-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23555' viewBox='0 0 24 24'%3E%3Cpath d='M15 4c-4.42 0-8 3.58-8 8s3.58 8 8 8 8-3.58 8-8-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zM3 12c0-2.61 1.67-4.83 4-5.65V4.26C3.55 5.15 1 8.27 1 12s2.55 6.85 6 7.74v-2.09c-2.33-.82-4-3.04-4-5.65z'/%3E%3C/svg%3E");
}

.anxiety-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23555' viewBox='0 0 24 24'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z'/%3E%3C/svg%3E");
}

.dyscalculia-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23555' viewBox='0 0 24 24'%3E%3Cpath d='M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14h-2v-2h2v2zm0-4h-2V7h2v6z'/%3E%3C/svg%3E");
}

main {
  flex: 1;
  margin-left: 250px;
  width: calc(100% - 250px);
}

.content-area {
  padding: 20px 40px;
  max-width: 1200px;
  margin: 0 auto;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .sidebar {
    width: 60px;
  }
  
  .logo h1 {
    font-size: 0;
  }
  
  .logo h1:first-letter {
    font-size: 24px;
  }
  
  nav a span {
    display: none;
  }
  
  main {
    margin-left: 60px;
    width: calc(100% - 60px);
  }
}
</style>