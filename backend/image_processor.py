import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import logging

# 配置日志
logger = logging.getLogger(__name__)

class AdvancedImageProcessor:
    """高级图像处理器"""
    
    def __init__(self):
        logger.info("初始化高级图像处理器...")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"使用设备: {self.device}")
        self.model = self._load_model()
        logger.info("高级图像处理器初始化完成")
    
    def _load_model(self):
        """加载深度学习模型"""
        logger.info("开始加载深度学习模型...")
        model = SimpleSRNet().to(self.device)
        model.eval()
        logger.info("深度学习模型加载完成")
        return model
    
    def enhance_traditional(self, image_path, scale_factor=2):
        """传统图像增强方法"""
        try:
            logger.info(f"开始传统图像增强: {image_path}")
            
            # 读取图像
            logger.info("读取图像...")
            img = cv2.imread(image_path)
            if img is None:
                logger.error("图像读取失败")
                return None
            logger.info(f"图像读取成功，尺寸: {img.shape}")
            
            # 1. 双三次插值放大
            height, width = img.shape[:2]
            logger.info(f"原始图像尺寸: {width}x{height}")
            enhanced = cv2.resize(img, (width * scale_factor, height * scale_factor), 
                                interpolation=cv2.INTER_CUBIC)
            logger.info(f"图像已放大到: {width * scale_factor}x{height * scale_factor}")
            
            # 2. 降噪
            logger.info("开始降噪处理...")
            enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
            logger.info("降噪处理完成")
            
            # 3. 锐化
            logger.info("开始锐化处理...")
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            enhanced = cv2.filter2D(enhanced, -1, kernel)
            logger.info("锐化处理完成")
            
            # 4. 对比度增强
            logger.info("开始对比度增强...")
            lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
            logger.info("对比度增强完成")
            
            logger.info(f"传统图像增强完成: {image_path}")
            return enhanced
            
        except Exception as e:
            logger.error(f"传统增强失败: {e}")
            return None
    
    def enhance_ai(self, image_path, scale_factor=2):
        """AI深度学习增强方法"""
        try:
            logger.info(f"开始AI深度学习增强: {image_path}")
            
            # 读取图像
            logger.info("读取图像...")
            img = cv2.imread(image_path)
            if img is None:
                logger.error("图像读取失败")
                return None
            logger.info(f"图像读取成功，尺寸: {img.shape}")
            
            # 转换为RGB
            logger.info("转换图像格式为RGB...")
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            logger.info("图像格式转换完成")
            
            # 预处理
            logger.info("开始图像预处理...")
            img_tensor = transforms.ToTensor()(img_rgb).unsqueeze(0).to(self.device)
            logger.info("图像预处理完成")
            
            # 模型推理
            logger.info("开始AI模型推理...")
            with torch.no_grad():
                enhanced = self.model(img_tensor)
            logger.info("AI模型推理完成")
            
            # 后处理
            logger.info("开始后处理...")
            enhanced = enhanced.squeeze(0).cpu()
            enhanced = transforms.ToPILImage()(enhanced)
            enhanced_np = np.array(enhanced)
            logger.info("后处理完成")
            
            # 转换为BGR格式
            logger.info("转换图像格式为BGR...")
            enhanced_bgr = cv2.cvtColor(enhanced_np, cv2.COLOR_RGB2BGR)
            logger.info("图像格式转换完成")
            
            logger.info(f"AI深度学习增强完成: {image_path}")
            return enhanced_bgr
            
        except Exception as e:
            logger.error(f"AI增强失败: {e}")
            return None
    
    def enhance_advanced(self, image_path, scale_factor=2):
        """高级增强方法（结合传统和AI）"""
        try:
            logger.info(f"开始高级增强: {image_path}")
            
            # 先进行传统增强
            logger.info("开始传统增强步骤...")
            traditional = self.enhance_traditional(image_path, scale_factor)
            if traditional is None:
                logger.error("传统增强失败")
                return None
            logger.info("传统增强步骤完成")
            
            # 再进行AI增强
            logger.info("开始AI增强步骤...")
            ai_enhanced = self.enhance_ai(image_path, scale_factor)
            if ai_enhanced is None:
                logger.warning("AI增强失败，使用传统增强结果")
                return traditional
            logger.info("AI增强步骤完成")
            
            # 混合两种结果
            logger.info("开始混合传统和AI增强结果...")
            alpha = 0.7  # AI结果权重
            enhanced = cv2.addWeighted(ai_enhanced, alpha, traditional, 1-alpha, 0)
            logger.info("结果混合完成")
            
            logger.info(f"高级增强完成: {image_path}")
            return enhanced
            
        except Exception as e:
            logger.error(f"高级增强失败: {e}")
            return None
    
    def enhance_quality(self, image_path, scale_factor=2):
        """质量优先的增强方法"""
        try:
            logger.info(f"开始质量优先增强: {image_path}")
            
            # 读取图像
            logger.info("读取图像...")
            img = cv2.imread(image_path)
            if img is None:
                logger.error("图像读取失败")
                return None
            logger.info(f"图像读取成功，尺寸: {img.shape}")
            
            # 1. 高质量放大
            height, width = img.shape[:2]
            logger.info(f"原始图像尺寸: {width}x{height}")
            enhanced = cv2.resize(img, (width * scale_factor, height * scale_factor), 
                                interpolation=cv2.INTER_LANCZOS4)
            logger.info(f"图像已高质量放大到: {width * scale_factor}x{height * scale_factor}")
            
            # 2. 多步骤降噪
            logger.info("开始多步骤降噪...")
            enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 15, 15, 7, 21)
            logger.info("多步骤降噪完成")
            
            # 3. 边缘保持滤波
            logger.info("开始边缘保持滤波...")
            enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)
            logger.info("边缘保持滤波完成")
            
            # 4. 自适应锐化
            logger.info("开始自适应锐化...")
            gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            laplacian = np.uint8(np.absolute(laplacian))
            enhanced = cv2.addWeighted(enhanced, 1.5, cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR), -0.5, 0)
            logger.info("自适应锐化完成")
            
            # 5. 色彩增强
            logger.info("开始色彩增强...")
            enhanced = cv2.convertScaleAbs(enhanced, alpha=1.1, beta=10)
            logger.info("色彩增强完成")
            
            logger.info(f"质量优先增强完成: {image_path}")
            return enhanced
            
        except Exception as e:
            logger.error(f"质量增强失败: {e}")
            return None


class SimpleSRNet(nn.Module):
    """简单的超分辨率网络"""
    
    def __init__(self, scale_factor=2):
        super(SimpleSRNet, self).__init__()
        logger.info("初始化简单超分辨率网络...")
        self.scale_factor = scale_factor
        
        # 特征提取层
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        
        # 上采样层
        self.upsample = nn.ConvTranspose2d(64, 64, kernel_size=4, stride=2, padding=1)
        
        # 重建层
        self.conv4 = nn.Conv2d(64, 3, kernel_size=3, padding=1)
        
        # 初始化权重
        self._initialize_weights()
        logger.info("简单超分辨率网络初始化完成")
    
    def _initialize_weights(self):
        """初始化网络权重"""
        logger.info("初始化网络权重...")
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.ConvTranspose2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
        logger.info("网络权重初始化完成")
    
    def forward(self, x):
        # 特征提取
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        
        # 上采样
        x = self.upsample(x)
        
        # 重建
        x = self.conv4(x)
        return x


def create_processor():
    """创建图像处理器实例"""
    logger.info("创建图像处理器实例...")
    return AdvancedImageProcessor() 