<template>
  <div id="app">
    <el-container class="app-container">
      <!-- <el-header class="app-header">
        <div class="header-content">
          <h1>🖼️ 图片高清化工具</h1>
          <p>使用先进的AI技术，将您的图片转换为高清版本</p>
        </div>
      </el-header> -->
      
      <el-main class="app-main">
        <ImageEnhancer />
      </el-main>
      

    </el-container>
  </div>
</template>

<script>
import ImageEnhancer from './components/ImageEnhancer.vue'

export default {
  name: 'App',
  components: {
    ImageEnhancer
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
  background: white;
  border-radius: 20px;
  margin: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 40px 20px;
}

.header-content h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  font-weight: 300;
}

.header-content p {
  font-size: 1.1em;
  opacity: 0.9;
}

.app-main {
  padding: 40px;
  flex: 1;
}



@media (max-width: 768px) {
  .app-container {
    margin: 10px;
  }
  
  .header-content h1 {
    font-size: 2em;
  }
  
  .app-main {
    padding: 20px;
  }
}
</style> 