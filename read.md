# 图片高清化处理系统

## 项目简介

这是一个基于深度学习和传统图像处理技术的图片高清化处理系统，能够将低分辨率图片转换为高分辨率、高质量的图片。系统提供了多种算法选择，从快速处理到极致清晰，满足不同用户的需求。

## 功能特性

### 🚀 多种算法选择
- **简单增强**：快速基础处理，适合批量处理
- **标准增强**：平衡质量和速度的中等处理
- **高级增强**：深度学习算法，高质量输出
- **超级清晰**：8倍放大算法，追求极致清晰度

### 🎯 核心功能
- 图片上传和预览
- 实时处理进度显示
- 多种放大倍数选择（2x, 4x, 8x）
- 处理前后对比
- 结果图片下载
- 详细的处理日志

### 📊 技术特性
- 支持多种图片格式（JPG, PNG, BMP等）
- 自动图片方向修复
- 内存优化处理
- 异步处理支持
- 详细的执行日志

## 技术架构

### 后端技术栈
- **Web框架**：Sanic (高性能异步框架)
- **图像处理**：OpenCV, PIL, NumPy
- **深度学习**：PyTorch
- **日志系统**：Python logging
- **CORS支持**：sanic-cors

### 前端技术栈
- **框架**：Vue.js 3
- **构建工具**：Vite
- **UI组件**：原生HTML/CSS/JavaScript
- **HTTP客户端**：Fetch API

### 项目结构
```
图片高清/
├── backend/                 # 后端服务
│   ├── app.py              # 主服务文件
│   ├── image_processor.py  # 图像处理模块
│   ├── requirements.txt    # 依赖包
│   └── uploads/           # 上传文件目录
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── App.vue        # 主应用组件
│   │   └── components/
│   │       └── ImageEnhancer.vue  # 图像增强组件
│   ├── index.html         # 入口HTML
│   └── package.json       # 前端依赖
├── templates/              # 模板文件
└── 各种说明文档.md        # 项目文档
```

## 安装和使用

### 环境要求
- Python 3.8+
- Node.js 16+
- 至少4GB内存（推荐8GB+）
- 支持CUDA的显卡（可选，用于GPU加速）

### 快速启动

1. **安装后端依赖**
```bash
cd backend
pip install -r requirements.txt
```

2. **安装前端依赖**
```bash
cd frontend
npm install
```

3. **启动服务**
```bash
# 启动后端服务
cd backend
python app.py

# 启动前端服务（新终端）
cd frontend
npm run dev
```

4. **访问应用**
打开浏览器访问：`http://localhost:5173`

### 一键启动
使用提供的批处理文件：
- `start.bat` - 启动完整服务
- `start-backend.bat` - 仅启动后端
- `start-frontend.bat` - 仅启动前端

## 算法说明

### 1. 简单增强
- **处理速度**：快速（1-3秒）
- **适用场景**：批量处理，快速预览
- **特点**：基础锐化和对比度增强

### 2. 标准增强
- **处理速度**：中等（3-6秒）
- **适用场景**：日常图片处理
- **特点**：多级锐化，智能降噪

### 3. 高级增强
- **处理速度**：较慢（6-10秒）
- **适用场景**：高质量需求
- **特点**：深度学习算法，细节重建

### 4. 超级清晰
- **处理速度**：较慢（8-15秒）
- **适用场景**：极致清晰度需求
- **特点**：8倍放大，多级锐化，强对比度增强

## API接口

### 图片增强接口
```
POST /enhance
Content-Type: multipart/form-data

参数：
- image: 图片文件
- algorithm: 算法选择 (simple/standard/advanced/super)
- scale_factor: 放大倍数 (2/4/8)
```

### 响应格式
```json
{
  "success": true,
  "message": "处理成功",
  "data": {
    "original_size": "原始尺寸",
    "enhanced_size": "增强后尺寸",
    "processing_time": "处理时间",
    "image_data": "base64编码的图片数据"
  }
}
```

## 配置说明

### 后端配置
- **上传目录**：`uploads/`
- **最大文件大小**：无限制
- **日志级别**：INFO
- **日志文件**：`image_enhancer.log`

### 前端配置
- **开发服务器**：`http://localhost:5173`
- **API地址**：`http://localhost:8000`
- **构建输出**：`dist/`

## 性能优化

### 内存优化
- 图片处理时及时释放内存
- 使用流式处理大文件
- 定期清理临时文件

### 处理速度优化
- 异步处理支持
- 多线程图像处理
- GPU加速（可选）

### 用户体验优化
- 实时进度显示
- 处理状态反馈
- 错误处理和重试机制

## 故障排除

### 常见问题

1. **依赖安装失败**
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. **端口被占用**
```bash
# 查找占用端口的进程
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# 结束进程
taskkill /PID <进程ID> /F
```

3. **内存不足**
- 减少同时处理的图片数量
- 降低放大倍数
- 关闭其他占用内存的程序

### 日志查看
```bash
# 查看后端日志
tail -f backend/image_enhancer.log

# 查看前端构建日志
cd frontend && npm run build
```

## 开发指南

### 添加新算法
1. 在 `backend/image_processor.py` 中添加新方法
2. 在 `backend/app.py` 中注册新算法
3. 在前端组件中添加选项

### 修改UI界面
1. 编辑 `frontend/src/components/ImageEnhancer.vue`
2. 修改样式和交互逻辑
3. 重新构建前端

### 部署到生产环境
1. 构建前端：`npm run build`
2. 配置生产环境变量
3. 使用生产级Web服务器（如Nginx）
4. 配置反向代理

## 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 支持4种增强算法
- 基础UI界面
- 日志系统

### 计划功能
- [ ] 批量处理功能
- [ ] 更多算法选择
- [ ] 移动端适配
- [ ] 云端部署支持

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发环境设置
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 代码规范
- 使用中文注释
- 遵循PEP 8 Python代码规范
- 添加适当的错误处理
- 编写单元测试

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至：[您的邮箱]

---

**注意**：本项目仅供学习和研究使用，请遵守相关法律法规。 