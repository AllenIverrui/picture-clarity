<template>
  <div class="ai-image-enhancer">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-content">
                 <div class="logo">
           <el-icon class="logo-icon"><picture-filled /></el-icon>
           <span class="logo-text">AI Image Enhancer</span>
         </div>
        <nav class="nav-menu">
          <el-button size="small" type="text">首页</el-button>
          <el-button size="small" type="text">关于</el-button>
          <el-button size="small" type="text">帮助</el-button>
        </nav>
      </div>
    </header>

    <!-- 主体区域 -->
    <main class="main-content">
      <!-- 左侧：图片上传与管理区 -->
      <div class="left-panel">
        <!-- 图片列表 -->
        <div class="image-list" v-if="imageList.length > 0">
          <div class="list-header">
            <el-button size="small" @click="clearAllImages">清空</el-button>
          </div>
          <div class="image-grid">
            <div
              v-for="(image, index) in imageList"
              :key="index"
              class="image-item"
              :class="{ 'selected': selectedImages.includes(index) }"
              @click="toggleImageSelection(index)"
            >
              <el-image
                :src="image.url"
                fit="cover"
                class="thumbnail"
              />
                             <div class="image-overlay">
                 <el-checkbox 
                   :model-value="selectedImages.includes(index)"
                   @change="toggleImageSelection(index)"
                   size="mini"
                 />
               </div>
              
            </div>
          </div>
        </div>

        <!-- 拖拽上传区域 -->
        <div 
          class="upload-area"
          @drop="handleDrop"
          @dragover.prevent
          @dragenter.prevent
          @click="triggerFileInput"
        >
          <div class="upload-content">
            <el-icon class="upload-icon"><upload-filled /></el-icon>
            <p class="upload-text">拖拽图片到此处或点击上传</p>
            <p class="upload-hint">支持批量上传，无大小限制</p>
          </div>
          <input
            ref="fileInput"
            type="file"
            multiple
            accept="image/*"
            @change="handleFileSelect"
            style="display: none"
          />
        </div>
      </div>

                           <!-- 右侧：处理与预览区 -->
        <div class="right-panel">
          <!-- 图片显示区域 -->
          <div class="image-display-area">
            <!-- 对比区，始终在顶部 -->
            <div class="preview-container" v-if="currentImage && enhancedImage">
              <div class="comparison-mode-switch" v-if="enhancedImage">
                <el-radio-group v-model="comparisonMode">
                  <el-radio-button label="slider">滑动对比</el-radio-button>
                  <el-radio-button label="side-by-side">并排对比</el-radio-button>
                </el-radio-group>
              </div>
              <div v-if="enhancedImage">
                <div v-if="comparisonMode === 'slider'">
                  <div class="comparison-slider">
                    <img :src="currentImage.url" class="comparison-image original" />
                    <img :src="enhancedImage" class="comparison-image enhanced" />
                    <div class="slider-handle" @mousedown="startDrag" @touchstart="startDrag">
                      <div class="slider-line"></div>
                      <div class="slider-circle"></div>
                    </div>
                  </div>
                </div>
                <div v-else-if="comparisonMode === 'side-by-side'" class="side-by-side-section">
                  <div class="side-by-side-container">
                    <div class="image-card" @click="openFullscreen('original')">
                      <h5>原图</h5>
                      <el-image :src="currentImage.url" fit="contain" class="side-image" />
                    </div>
                    <div class="image-card" @click="openFullscreen('enhanced')">
                      <h5>高清图</h5>
                      <el-image :src="enhancedImage" fit="contain" class="side-image" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 单张图片显示 -->
            <div v-else-if="currentImage" class="single-image-container">
              <el-image :src="currentImage.url" fit="contain" class="single-image" @click="openFullscreen('original')" />
            </div>
            
            <!-- 默认提示 -->
            <div v-else class="default-prompt">
              <el-icon class="prompt-icon"><picture-filled /></el-icon>
              <p class="prompt-text">请上传图片开始处理</p>
            </div>
          </div>
          
                     <!-- 工具栏区域 -->
           <div class="toolbar-area">
             <!-- 工具选项卡 -->
            <div class="tools-tabs">
              <el-tabs v-model="activeToolTab" type="card" size="small">
                <el-tab-pane label="图像高清" name="enhance">
                  <!-- 高清化方法选择 -->
                  <div class="method-section">
                    <div class="method-cards">
                      <div
                        v-for="method in methods"
                        :key="method.id"
                        class="method-card"
                        :class="{ 'selected': selectedMethod === method.id }"
                        @click="selectedMethod = method.id"
                      >
                        <div class="method-header">
                          <h6 class="method-name">{{ method.name }}</h6>
                          <div class="method-speed" :class="method.speed">
                            {{ method.speed === 'fast' ? '快速' : method.speed === 'medium' ? '中等' : '慢速' }}
                          </div>
                        </div>
                        <p class="method-description-text">{{ method.description }}</p>
                      </div>
                    </div>
                    <!-- 一键高清化按钮 -->
                    <el-button 
                      type="primary" 
                      size="small" 
                      @click="enhanceImages" 
                      :disabled="selectedImages.length === 0 || processing"
                      style="margin-top: 0.8rem; width: 100%;"
                      :loading="processing"
                    >
                      <el-icon v-if="!processing"><magic-stick /></el-icon>
                      {{ processing ? '处理中...' : '一键高清化' }}
                    </el-button>
                    
                    <!-- 处理进度条 -->
                    <div v-if="processing" class="progress-container">
                      <el-progress 
                        :percentage="progressPercentage" 
                        :stroke-width="8"
                        :show-text="false"
                        color="#2979FF"
                      />
                      <div class="progress-text">
                        <span>正在处理第 {{ currentProcessingIndex + 1 }}/{{ selectedImages.length }} 张图片</span>
                        <span class="progress-percentage">{{ progressPercentage }}%</span>
                      </div>
                    </div>
                  </div>
                </el-tab-pane>
                
                <el-tab-pane label="滤镜" name="filter">
                  <!-- 滤镜分类 -->
                  <div class="filter-section">
                    <div class="filter-grid">
                      <el-button
                        v-for="filter in filters"
                        :key="filter.id"
                        size="small"
                        :type="selectedFilter === filter.id ? 'primary' : 'default'"
                        @click="selectFilter(filter.id)"
                      >
                        {{ filter.name }}
                      </el-button>
                    </div>
                    <el-button 
                      size="small" 
                      type="primary" 
                      @click="applyFilters" 
                      style="margin-top: 0.5rem;"
                      :disabled="!selectedFilter || selectedFilter === 'none' || !currentImage"
                    >
                      应用滤镜
                    </el-button>
                  </div>
                </el-tab-pane>
                
                <el-tab-pane label="调整" name="adjust">
                  <!-- 图像调整 -->
                  <div class="adjustment-section">
                    <div class="adjustment-sliders">
                      <div class="slider-item">
                        <label>亮度</label>
                        <el-slider
                          v-model="adjustments.brightness"
                          :min="0"
                          :max="200"
                          :step="5"
                          @change="applyAdjustments"
                          size="small"
                          :show-tooltip="false"
                          style="margin: 0;"
                          :disabled="!currentImage"
                        />
                      </div>
                      <div class="slider-item">
                        <label>对比度</label>
                        <el-slider
                          v-model="adjustments.contrast"
                          :min="0"
                          :max="200"
                          :step="5"
                          @change="applyAdjustments"
                          size="small"
                          :show-tooltip="false"
                          style="margin: 0;"
                          :disabled="!currentImage"
                        />
                      </div>
                      <div class="slider-item">
                        <label>饱和度</label>
                        <el-slider
                          v-model="adjustments.saturation"
                          :min="0"
                          :max="200"
                          :step="5"
                          @change="applyAdjustments"
                          size="small"
                          :show-tooltip="false"
                          style="margin: 0;"
                          :disabled="!currentImage"
                        />
                      </div>
                      <div class="slider-item">
                        <label>锐化</label>
                        <el-slider
                          v-model="adjustments.sharpness"
                          :min="0"
                          :max="100"
                          :step="5"
                          @change="applyAdjustments"
                          size="small"
                          :show-tooltip="false"
                          style="margin: 0;"
                          :disabled="!currentImage"
                        />
                      </div>
                    </div>
                  </div>
                </el-tab-pane>
              </el-tabs>
            </div>
          </div>
        </div>
     </main>

                       <!-- 底部功能按钮 -->
       <div class="bottom-actions">
         <el-button 
           type="success" 
           size="small" 
           @click="batchProcess" 
           :disabled="selectedImages.length === 0"
         >
           <el-icon><operation /></el-icon>
           批量处理
         </el-button>
         <el-button 
           type="warning" 
           size="small" 
           @click="generatePoster" 
           :disabled="selectedImages.length < 2"
         >
           <el-icon><brush /></el-icon>
           生成海报
         </el-button>
                   <el-button 
            type="info" 
            size="small" 
            @click="exportPoster" 
            :disabled="!enhancedImage || !currentImage"
          >
            <el-icon><download /></el-icon>
            导出海报
          </el-button>
         <el-button size="small" @click="resetAll">
           <el-icon><refresh /></el-icon>
           重置
         </el-button>
       </div>

       <!-- 浮动下载按钮 -->
       <div class="floating-download" v-if="enhancedImage && currentImage">
         <el-button 
           type="primary" 
           size="large" 
           @click="downloadEnhanced"
           class="floating-download-btn"
         >
           <el-icon><download /></el-icon>
           下载高清图
         </el-button>
       </div>

           <!-- 底部版权信息 -->
      <footer class="app-footer">
        <p>&copy; 2024 AI Image Enhancer. Powered by Advanced AI Technology</p>
      </footer>
      
      <!-- 全屏图片查看模态框 -->
      <div v-if="fullscreenVisible" class="fullscreen-modal" @click="closeFullscreen">
        <div class="fullscreen-content" @click.stop>
          <div class="fullscreen-header">
            <span class="fullscreen-title">{{ fullscreenMode === 'original' ? '原图' : '高清图' }}</span>
            <div class="fullscreen-controls">
              <el-button 
                v-if="currentImage && enhancedImage" 
                size="small" 
                @click="switchFullscreenImage"
                class="switch-btn"
              >
                <el-icon><refresh /></el-icon>
                切换图片
              </el-button>
              <el-button size="small" @click="closeFullscreen" class="close-btn">
                <el-icon><close /></el-icon>
                关闭
              </el-button>
            </div>
          </div>
          <div class="fullscreen-image-container">
            <el-image 
              :src="fullscreenImageSrc" 
              fit="contain" 
              class="fullscreen-image"
              :preview-src-list="[fullscreenImageSrc]"
              :initial-index="0"
              :preview-teleported="true"
            />
          </div>
        </div>
      </div>
   </div>
 </template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  UploadFilled,
  MagicStick,
  Download,
  Refresh,
  ArrowLeft,
  ArrowRight,
  Brush,
  Operation,
  PictureFilled,
  Close
} from '@element-plus/icons-vue'
import axios from 'axios'

// 响应式数据
const fileInput = ref(null)
const imageList = ref([])
const selectedImages = ref([])
const currentImage = ref(null)
const enhancedImage = ref('')
const processing = ref(false)
const progressPercentage = ref(0)
const currentProcessingIndex = ref(0)
const activeTab = ref('original')
const activeToolTab = ref('enhance')
const selectedFilter = ref('')
const sliderPosition = ref(50)
const selectedMethod = ref('gentle')
const comparisonMode = ref('slider')

// 全屏查看相关
const fullscreenVisible = ref(false)
const fullscreenMode = ref('original') // 'original' 或 'enhanced'
const fullscreenImageSrc = computed(() => {
  if (!currentImage.value) return ''
  return fullscreenMode.value === 'original' ? currentImage.value.url : enhancedImage.value
})

// 滤镜选项
const filters = reactive([
  { id: 'none', name: '无滤镜' },
  { id: 'blackwhite', name: '黑白' },
  { id: 'vintage', name: '复古' },
  { id: 'film', name: '胶片' },
  { id: 'fresh', name: '清新' },
  { id: 'hdr', name: 'HDR' },
  { id: 'warm', name: '暖色' },
  { id: 'cool', name: '冷色' }
])

// 图像调整参数
const adjustments = reactive({
  brightness: 100,
  contrast: 100,
  saturation: 100,
  sharpness: 0
})

// 增强方法
const methods = reactive([
  {
    id: 'traditional',
    name: '传统增强',
    description: '基于传统图像处理算法，温和提升分辨率与清晰度，保持自然效果',
    speed: 'fast'
  },
  {
    id: 'super_clear',
    name: '超级清晰',
    description: '8倍放大算法，多级锐化处理，强对比度和饱和度增强，追求极致清晰度',
    speed: 'slow'
  },
  {
    id: 'advanced',
    name: '高级增强',
    description: '结合传统和AI技术，温和的图像增强，保持自然色彩和清晰度',
    speed: 'medium'
  },
  {
    id: 'super_quality',
    name: '超级质量',
    description: '高质量图像处理，温和的增强参数，确保图片清晰自然',
    speed: 'slow'
  }
])

// 计算属性
const hasSelectedImages = computed(() => selectedImages.value.length > 0)
const canGeneratePoster = computed(() => selectedImages.value.length >= 2)

// 方法
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files)
  addFiles(files)
}

const handleDrop = (event) => {
  event.preventDefault()
  const files = Array.from(event.dataTransfer.files).filter(file => file.type.startsWith('image/'))
  addFiles(files)
}

const addFiles = (files) => {
  files.forEach(file => {
    const reader = new FileReader()
    reader.onload = (e) => {
      imageList.value.push({
        file: file,
        name: file.name,
        url: e.target.result,
        size: file.size
      })
    }
    reader.readAsDataURL(file)
  })
  
  if (imageList.value.length === 1) {
    currentImage.value = imageList.value[0]
  }
}

const toggleImageSelection = (index) => {
  const selectedIndex = selectedImages.value.indexOf(index)
  if (selectedIndex > -1) {
    selectedImages.value.splice(selectedIndex, 1)
  } else {
    selectedImages.value.push(index)
  }
}

const clearAllImages = () => {
  imageList.value = []
  selectedImages.value = []
  currentImage.value = null
  enhancedImage.value = ''
}

const selectFilter = (filterId) => {
  selectedFilter.value = filterId
}

const applyAdjustments = async () => {
  if (!currentImage.value) {
    ElMessage.warning('请先选择一张图片')
    return
  }
  
  processing.value = true
  progressPercentage.value = 0
  
  try {
    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progressPercentage.value < 90) {
        progressPercentage.value += 25
      }
    }, 150)
    
    const response = await axios.post('http://localhost:8000/api/adjust-image', {
      image: currentImage.value.url,
      adjustments: adjustments.value
    })
    
    clearInterval(progressInterval)
    progressPercentage.value = 100
    
    if (response.data.success) {
      enhancedImage.value = response.data.adjusted_image
      ElMessage.success('图像调整应用成功')
    }
  } catch (error) {
    ElMessage.error('图像调整失败: ' + error.message)
  } finally {
    processing.value = false
    progressPercentage.value = 0
  }
}

const enhanceImages = async () => {
  if (selectedImages.value.length === 0) {
    ElMessage.warning('请先选择要处理的图片')
    return
  }

  processing.value = true
  progressPercentage.value = 0
  currentProcessingIndex.value = 0
  
  try {
    for (let i = 0; i < selectedImages.value.length; i++) {
      const index = selectedImages.value[i]
      const image = imageList.value[index]
      
      // 更新进度
      currentProcessingIndex.value = i
      progressPercentage.value = Math.round(((i + 1) / selectedImages.value.length) * 100)
      
      await processSingleImage(image, selectedMethod.value)
      currentImage.value = image
      enhancedImage.value = image.enhancedUrl
    }
    
    ElMessage.success('批量高清化完成')
  } catch (error) {
    ElMessage.error('处理失败: ' + error.message)
  } finally {
    processing.value = false
    progressPercentage.value = 0
    currentProcessingIndex.value = 0
  }
}

const processSingleImage = async (image, method) => {
  const formData = new FormData()
  formData.append('file', image.file)
  formData.append('method', method)

  const response = await axios.post('http://localhost:8000/api/upload', formData)
  
  if (response.data.success) {
    image.enhancedUrl = response.data.enhanced_image
  } else {
    throw new Error(response.data.error)
  }
}

const applyFilters = async () => {
  if (selectedFilter.value === 'none') {
    ElMessage.info('请选择滤镜效果')
    return
  }
  
  if (!currentImage.value) {
    ElMessage.warning('请先选择一张图片')
    return
  }
  
  processing.value = true
  progressPercentage.value = 0
  
  try {
    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progressPercentage.value < 90) {
        progressPercentage.value += 20
      }
    }, 200)
    
    const response = await axios.post('http://localhost:8000/api/apply-filter', {
      image: currentImage.value.url,
      filter: selectedFilter.value
    })
    
    clearInterval(progressInterval)
    progressPercentage.value = 100
    
    if (response.data.success) {
      enhancedImage.value = response.data.filtered_image
      ElMessage.success(`已应用${filters.find(f => f.id === selectedFilter.value)?.name}滤镜`)
    }
  } catch (error) {
    ElMessage.error('滤镜应用失败: ' + error.message)
  } finally {
    processing.value = false
    progressPercentage.value = 0
  }
}

const batchProcess = async () => {
  if (selectedImages.value.length === 0) {
    ElMessage.warning('请先选择要处理的图片')
    return
  }
  
  processing.value = true
  progressPercentage.value = 0
  currentProcessingIndex.value = 0
  
  try {
    const files = selectedImages.value.map(index => imageList.value[index].url)
    
    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progressPercentage.value < 90) {
        progressPercentage.value += 10
      }
    }, 200)
    
    const response = await axios.post('http://localhost:8000/api/batch-enhance', {
      files: files,
      method: selectedMethod.value
    })
    
    clearInterval(progressInterval)
    progressPercentage.value = 100
    
    if (response.data.success) {
      response.data.results.forEach((result, index) => {
        if (result.success) {
          const imageIndex = selectedImages.value[index]
          imageList.value[imageIndex].enhancedUrl = result.enhanced_image
        }
      })
      
      ElMessage.success('批量处理完成')
    }
  } catch (error) {
    ElMessage.error('批量处理失败: ' + error.message)
  } finally {
    processing.value = false
    progressPercentage.value = 0
    currentProcessingIndex.value = 0
  }
}

const generatePoster = async () => {
  if (selectedImages.value.length === 0) {
    ElMessage.warning('请先选择要生成海报的图片')
    return
  }
  
  processing.value = true
  progressPercentage.value = 0
  
  try {
    const images = selectedImages.value.map(index => imageList.value[index].url)
    
    // 模拟进度更新
    const progressInterval = setInterval(() => {
      if (progressPercentage.value < 90) {
        progressPercentage.value += 15
      }
    }, 300)
    
    const response = await axios.post('http://localhost:8000/api/generate-poster', {
      images: images,
      layout: 'grid'
    })
    
    clearInterval(progressInterval)
    progressPercentage.value = 100
    
    if (response.data.success) {
      const posterImage = {
        name: '生成的海报',
        url: response.data.poster,
        file: null,
        size: 0,
        enhancedUrl: response.data.poster
      }
      
      imageList.value.push(posterImage)
      currentImage.value = posterImage
      enhancedImage.value = response.data.poster
      
      ElMessage.success('海报生成成功')
    }
  } catch (error) {
    ElMessage.error('海报生成失败: ' + error.message)
  } finally {
    processing.value = false
    progressPercentage.value = 0
  }
}

const downloadEnhanced = () => {
  if (enhancedImage.value) {
    const link = document.createElement('a')
    link.href = enhancedImage.value
    link.download = 'enhanced_image.jpg'
    link.click()
    ElMessage.success('下载成功')
  } else {
    ElMessage.warning('没有可下载的高清图片')
  }
}

const exportPoster = () => {
  if (enhancedImage.value) {
    const link = document.createElement('a')
    link.href = enhancedImage.value
    link.download = 'poster.jpg'
    link.click()
    ElMessage.success('海报导出成功')
  } else {
    ElMessage.warning('没有可导出的海报')
  }
}

const resetAll = () => {
  ElMessageBox.confirm('确定要清空所有图片吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    clearAllImages()
    ElMessage.success('已清空所有图片')
  })
}

// 滑动对比相关
const startDrag = (event) => {
  event.preventDefault()
  const handle = event.target.closest('.slider-handle')
  const container = handle.parentElement
  const enhancedImage = container.querySelector('.comparison-image.enhanced')
  
  const handleDrag = (e) => {
    const rect = container.getBoundingClientRect()
    const x = (e.clientX || e.touches[0].clientX) - rect.left
    const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100))
    
    handle.style.left = percentage + '%'
    
    if (enhancedImage) {
      enhancedImage.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`
    }
  }
  
  const stopDrag = () => {
    document.removeEventListener('mousemove', handleDrag)
    document.removeEventListener('touchmove', handleDrag)
    document.removeEventListener('mouseup', stopDrag)
    document.removeEventListener('touchend', stopDrag)
  }
  
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('touchmove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchend', stopDrag)
}

// 全屏查看方法
const openFullscreen = (mode) => {
  if (!currentImage.value) return
  
  fullscreenMode.value = mode
  fullscreenVisible.value = true
}

const closeFullscreen = () => {
  fullscreenVisible.value = false
}

const switchFullscreenImage = () => {
  if (fullscreenMode.value === 'original' && enhancedImage.value) {
    fullscreenMode.value = 'enhanced'
  } else if (fullscreenMode.value === 'enhanced') {
    fullscreenMode.value = 'original'
  }
}

// 工具函数
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

onMounted(() => {
  // 初始化
})
</script>

<style scoped>
/* 主容器 */
.ai-image-enhancer {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #e3f2fd 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 顶部导航栏 */
.app-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
  border-bottom: 1px solid rgba(41, 121, 255, 0.1);
  padding: 1rem 0;
  box-shadow: 0 4px 20px rgba(41, 121, 255, 0.08);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.app-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #2979FF, #1565C0, #2979FF);
}

.header-content {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 0.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  background: rgba(41, 121, 255, 0.05);
  transition: all 0.3s ease;
}

.logo:hover {
  background: rgba(41, 121, 255, 0.1);
  transform: translateY(-1px);
}

.logo-icon {
  font-size: 1.8rem;
  color: #2979FF;
  filter: drop-shadow(0 2px 4px rgba(41, 121, 255, 0.2));
}

.logo-text {
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #2979FF, #1565C0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

.nav-menu {
  display: flex;
  gap: 1.5rem;
}

.nav-menu .el-button {
  color: #666;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-menu .el-button:hover {
  color: #2979FF;
  background: rgba(41, 121, 255, 0.05);
  transform: translateY(-1px);
}

.nav-menu .el-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: #2979FF;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-menu .el-button:hover::after {
  width: 80%;
}

/* 底部功能按钮 */
.bottom-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 1.2rem 0;
  background: linear-gradient(135deg, #f8faff 0%, #ffffff 100%);
  border-top: 1px solid rgba(41, 121, 255, 0.1);
  margin-top: 1rem;
  box-shadow: 0 -4px 20px rgba(41, 121, 255, 0.05);
  flex-wrap: wrap;
}

.bottom-actions .el-button {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-width: 100px;
}

.bottom-actions .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(41, 121, 255, 0.2);
}

.bottom-actions .el-button--primary {
  background: linear-gradient(135deg, #2979FF, #1565C0);
  border: none;
}

.bottom-actions .el-button--primary:hover {
  background: linear-gradient(135deg, #1565C0, #0D47A1);
}

/* 主体区域 */
.main-content {
  display: grid;
  grid-template-columns: 1fr 9fr;
  gap: 0.8rem;
  max-width: 1600px;
  margin: 0.3rem auto;
  padding: 0 0.8rem;
  min-height: calc(100vh - 160px);
  margin-top: 80px;
}

/* 左侧面板 */
.left-panel {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(41, 121, 255, 0.1);
  border-radius: 12px;
  padding: 0.8rem;
  box-shadow: 0 4px 12px rgba(41, 121, 255, 0.1);
  max-width: 200px;
  min-width: 160px;
  backdrop-filter: blur(10px);
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 1rem 0;
  letter-spacing: -0.25px;
}

/* 上传区域 */
.upload-area {
  border: 2px dashed #2979FF;
  border-radius: 12px;
  padding: 0.7rem 0.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafbfc;
  position: relative;
  overflow: hidden;
}

.upload-area:hover {
  border-color: #1565C0;
  background: #f0f4ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(41, 121, 255, 0.1);
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  position: relative;
  z-index: 1;
}

.upload-icon {
  font-size: 1.3rem;
  color: #2979FF;
  transition: all 0.3s ease;
}

.upload-area:hover .upload-icon {
  transform: scale(1.05);
  color: #1565C0;
}

.upload-text {
  font-size: 0.7rem;
  font-weight: 500;
  color: #1a1a1a;
  margin: 0;
}

.upload-hint {
  font-size: 0.6rem;
  color: #666;
  margin: 0;
}

/* 图片列表 */
.image-list {
  margin-bottom: 1.2rem;
}

.list-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 0.6rem;
  padding: 0.2rem 0;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.6rem;
  max-height: 400px;
  overflow-y: auto;
  padding: 0.6rem;
  background: #fafbfc;
  border-radius: 12px;
}

.image-item {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  background: white;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.12);
  aspect-ratio: 1;
  min-height: 80px;
}

.image-item:hover {
  border-color: #2979FF;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(41, 121, 255, 0.2);
}

.image-item.selected {
  border-color: #2979FF;
  background: #f8faff;
  box-shadow: 0 4px 15px rgba(41, 121, 255, 0.3);
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.3s ease;
}

.image-item:hover .thumbnail {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
  padding: 2px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
  z-index: 2;
}



/* 右侧面板 */
.right-panel {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(41, 121, 255, 0.1);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(41, 121, 255, 0.1);
  display: flex;
  flex-direction: column;
  height: 100%;
  backdrop-filter: blur(10px);
}

/* 图片显示区域 */
.image-display-area {
  flex: 1;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

/* 单张图片显示 */
.single-image-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
  border-radius: 8px;
  border: 2px dashed #e0e0e0;
}

.single-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* 默认提示 */
.default-prompt {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fafbfc;
  border-radius: 8px;
  border: 2px dashed #e0e0e0;
  color: #999;
}

.prompt-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ccc;
}

.prompt-text {
  font-size: 1rem;
  color: #999;
  margin: 0;
}

/* 工具栏区域 */
.toolbar-area {
  background: #f8faff;
  border-top: 1px solid #e0e0e0;
  padding: 1rem;
  border-radius: 0 0 12px 12px;
}

/* 预览容器 */
.preview-container {
  margin-bottom: 1rem;
}

.preview-image {
  width: 100%;
  max-height: 400px;
  border-radius: 8px;
}

/* 对比滑动器 */
.comparison-container {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
}

.comparison-slider {
  position: relative;
  width: 100%;
  height: 550px;
}

.comparison-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.comparison-image.enhanced {
  clip-path: inset(0 50% 0 0);
  transition: clip-path 0.1s ease;
}

.slider-handle {
  position: absolute;
  top: 0;
  left: 50%;
  width: 4px;
  height: 100%;
  background: #4a90e2;
  cursor: ew-resize;
}

.slider-line {
  width: 100%;
  height: 100%;
  background: #4a90e2;
}

.slider-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: #4a90e2;
  border-radius: 50%;
  border: 3px solid white;
}



/* 工具选项卡 */
.tools-tabs {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  border: 1px solid rgba(41, 121, 255, 0.15);
  box-shadow: 0 2px 8px rgba(41, 121, 255, 0.1);
  backdrop-filter: blur(10px);
}

.tools-tabs .el-tabs__header {
  margin: 0;
  padding: 0.5rem 0.5rem 0;
}

.tools-tabs .el-tabs__content {
  padding: 1rem;
}



/* 工具选项卡内容样式 */
.tools-tabs .el-tab-pane {
  padding: 0;
}

.method-section {
  margin-bottom: 0.6rem;
}

.method-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.method-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(41, 121, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(5px);
}

.method-card:hover {
  border-color: #2979FF;
  box-shadow: 0 2px 8px rgba(41, 121, 255, 0.15);
}

.method-card.selected {
  border-color: #2979FF;
  background: #f8faff;
  box-shadow: 0 2px 8px rgba(41, 121, 255, 0.2);
}

.method-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.3rem;
}

.method-name {
  margin: 0;
  font-size: 0.85rem;
  font-weight: 600;
  color: #2c3e50;
}

.method-speed {
  padding: 0.1rem 0.3rem;
  border-radius: 6px;
  font-size: 0.6rem;
  font-weight: 500;
}

.method-speed.fast {
  background: #e8f5e8;
  color: #2e7d32;
}

.method-speed.medium {
  background: #fff3e0;
  color: #f57c00;
}

.method-speed.slow {
  background: #ffebee;
  color: #c62828;
}

.method-description-text {
  margin: 0;
  font-size: 0.7rem;
  color: #666;
  line-height: 1.3;
}

.filter-section,
.adjustment-section {
  margin-bottom: 0.6rem;
}

.filter-section h5,
.adjustment-section h5 {
  margin: 0 0 0.4rem 0;
  color: #2c3e50;
  font-weight: 600;
  font-size: 0.8rem;
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(45px, 1fr));
  gap: 0.15rem;
}

.adjustment-sliders {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.slider-item {
  display: flex;
  flex-direction: column;
  gap: 0.05rem;
}

.slider-item label {
  font-size: 0.65rem;
  color: #666;
}



/* 响应式设计 */
@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr 3fr;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 0 1rem;
  }
  
  .left-panel {
    padding: 1rem;
    max-width: none;
  }
  
  .right-panel {
    padding: 1.5rem;
  }
}

/* 简单的过渡效果 */
.left-panel,
.right-panel {
  transition: all 0.2s ease;
}

/* 滚动条样式 */
.image-grid::-webkit-scrollbar {
  width: 4px;
}

.image-grid::-webkit-scrollbar-thumb {
  background: #4a90e2;
  border-radius: 2px;
}

.comparison-mode-switch {
  text-align: center;
  margin-bottom: 0.6rem;
}

.side-by-side-section {
  margin-top: 0.8rem;
  width: 100%;
}

.side-by-side-container {
  display: flex;
  justify-content: space-between;
  gap: 0.4rem;
  width: 100%;
}

.image-card {
  background: #fff;
  border-radius: 6px;
  padding: 6px;
  text-align: center;
  flex: 1;
  min-width: 0;
  max-width: 48%;
}

.image-card h5 {
  margin-bottom: 3px;
  color: #333;
  font-size: 11px;
  font-weight: 600;
}

.side-image {
  width: 100%;
  height: 280px;
  object-fit: contain;
  border-radius: 4px;
}

/* 进度条样式 */
.progress-container {
  margin-top: 0.8rem;
  padding: 0.8rem;
  background: #f8faff;
  border-radius: 8px;
  border: 1px solid rgba(41, 121, 255, 0.1);
}

.progress-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #666;
}

.progress-percentage {
  font-weight: 600;
  color: #2979FF;
}

/* 底部版权信息 */
.app-footer {
  background: linear-gradient(135deg, #fafbfc 0%, #f0f4ff 100%);
  border-top: 1px solid rgba(41, 121, 255, 0.1);
  padding: 2rem 0;
  text-align: center;
  margin-top: auto;
  position: relative;
}

.app-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(41, 121, 255, 0.3), transparent);
}

.app-footer p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* 全屏模态框样式 */
.fullscreen-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.95);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.fullscreen-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.fullscreen-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  background: rgba(0, 0, 0, 0.7);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(10px);
}

.fullscreen-title {
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
}

.fullscreen-controls {
  display: flex;
  gap: 0.5rem;
}

.switch-btn {
  background: rgba(41, 121, 255, 0.8);
  border: none;
  color: white;
}

.switch-btn:hover {
  background: rgba(41, 121, 255, 1);
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.fullscreen-image-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem 2rem;
  width: 100%;
  height: 100%;
}

.fullscreen-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* 并排对比优化 */
.side-by-side-container {
  display: flex;
  justify-content: center;
  gap: 0;
  width: 100%;
  overflow: hidden;
}

.image-card {
  background: #fff;
  border-radius: 6px;
  padding: 6px;
  text-align: center;
  flex: 1;
  min-width: 0;
  max-width: 49.5%;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid rgba(41, 121, 255, 0.1);
}

.image-card:hover {
  border-color: #2979FF;
  box-shadow: 0 2px 8px rgba(41, 121, 255, 0.15);
}

.image-card h5 {
  margin-bottom: 3px;
  color: #333;
  font-size: 11px;
  font-weight: 600;
}

.side-image {
  width: 100%;
  height: 400px;
  object-fit: contain;
  border-radius: 4px;
  transition: transform 0.2s ease;
}

.image-card:hover .side-image {
  transform: scale(1.02);
}

/* 浮动下载按钮样式 */
.floating-download {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
  animation: floatIn 0.5s ease-out;
}

.floating-download-btn {
  padding: 1rem 1.5rem;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  box-shadow: 0 8px 25px rgba(41, 121, 255, 0.3);
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #2979FF, #1565C0);
  border: none;
  min-width: 140px;
}

.floating-download-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(41, 121, 255, 0.4);
  background: linear-gradient(135deg, #1565C0, #0D47A1);
}

.floating-download-btn .el-icon {
  margin-right: 0.5rem;
  font-size: 1.1rem;
}

@keyframes floatIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .floating-download {
    bottom: 1rem;
    right: 1rem;
  }
  
  .floating-download-btn {
    padding: 0.8rem 1.2rem;
    font-size: 0.8rem;
    min-width: 120px;
  }
}
</style> 