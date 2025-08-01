# 图片高清化工具

一个基于Vue3前端 + Sanic后端的图片高清化Web应用，可以将低分辨率图片转换为高清版本。

## 项目架构

- **前端**: Vue 3 + Element Plus + Vite
- **后端**: Sanic (Python异步框架)
- **图像处理**: OpenCV + PyTorch + 深度学习模型

## 功能特点

- 🖼️ **多种增强方法**：支持传统图像处理和AI深度学习
- 🎨 **现代化界面**：基于Element Plus的美观界面
- ⚡ **异步处理**：Sanic提供高性能异步API
- 📱 **响应式设计**：支持手机和桌面设备
- 💾 **一键下载**：处理完成后可直接下载高清图片

## 项目结构

```
图片高清/
├── backend/                 # 后端服务
│   ├── app.py              # Sanic主应用
│   ├── image_processor.py  # 图像处理模块
│   ├── requirements.txt    # Python依赖
│   └── uploads/           # 临时上传目录
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/    # Vue组件
│   │   ├── App.vue        # 主应用组件
│   │   └── main.js        # 入口文件
│   ├── package.json       # Node.js依赖
│   ├── vite.config.js     # Vite配置
│   └── index.html         # HTML模板
├── README.md              # 项目说明
└── start.bat             # Windows启动脚本
```

## 快速开始

### 1. 启动后端服务

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端服务将在 `http://localhost:8000` 启动

### 2. 启动前端服务

```bash
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

### 3. 使用Windows批处理文件

直接双击 `start.bat` 文件，将自动安装依赖并启动服务。

## 增强方法说明

### 传统增强
- 双三次插值放大
- 图像锐化
- 降噪处理
- 处理速度快

### AI深度学习
- 基于卷积神经网络的超分辨率
- 更高质量的图像重建
- 需要更多处理时间
- 适合高质量需求

### 高级混合
- 结合传统和AI方法
- 平衡质量和速度
- 适合一般用途

### 质量优先
- 最高质量处理
- 多步骤降噪和锐化
- 处理时间较长

## API接口

### 上传图片
```
POST /api/upload
Content-Type: multipart/form-data

参数:
- file: 图片文件
- method: 增强方法 (traditional/deep_learning/advanced/quality)
```

### 获取增强方法
```
GET /api/methods
```

### 健康检查
```
GET /api/health
```

## 技术栈

### 后端
- **Sanic**: 高性能异步Web框架
- **OpenCV**: 图像处理
- **PyTorch**: 深度学习
- **NumPy**: 数值计算

### 前端
- **Vue 3**: 渐进式JavaScript框架
- **Element Plus**: UI组件库
- **Vite**: 构建工具
- **Axios**: HTTP客户端

## 系统要求

- Python 3.7+
- Node.js 16+
- 4GB+ RAM
- 支持CUDA的GPU（可选，用于加速AI处理）

## 开发说明

### 后端开发
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

### 构建生产版本
```bash
cd frontend
npm run build
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 修改后端端口
   # backend/app.py
   app.run(host="0.0.0.0", port=8001, debug=True)
   
   # 修改前端代理
   # frontend/vite.config.js
   proxy: {
     '/api': {
       target: 'http://localhost:8001',
       changeOrigin: true
     }
   }
   ```

2. **依赖安装失败**
   ```bash
   # 后端
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   
   # 前端
   npm cache clean --force
   npm install
   ```

3. **内存不足**
   - 减少图片大小
   - 使用传统增强方法
   - 增加系统内存

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v2.0.0
- 重构为Vue3 + Sanic架构
- 前后端分离
- 异步图像处理
- 现代化UI界面
- 更好的错误处理

### v1.0.0
- 初始版本发布
- 支持传统增强和AI深度学习
- 现代化Web界面
- 拖拽上传功能 