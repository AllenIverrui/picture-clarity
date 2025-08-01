import os
import base64
import aiofiles
from sanic import Sanic, Request
from sanic.response import json
from sanic_cors import CORS
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import traceback
import json as json_lib
from datetime import datetime
import numpy as np
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('image_enhancer.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

app = Sanic("image_enhancer")
CORS(app)

# 配置
app.config.UPLOAD_FOLDER = "uploads"
app.config.MAX_CONTENT_LENGTH = 0  # 无限制

# 确保上传目录存在
os.makedirs(app.config.UPLOAD_FOLDER, exist_ok=True)

def fix_image_orientation(image):
    """修复图片方向问题，处理EXIF信息"""
    try:
        logger.info("开始修复图片方向...")
        # 检查是否有EXIF信息
        if hasattr(image, '_getexif') and image._getexif() is not None:
            exif = image._getexif()
            if exif is not None:
                # 获取方向信息
                orientation = exif.get(274)  # 274 是方向标签的ID
                if orientation is not None:
                    logger.info(f"检测到图片方向信息: {orientation}")
                    # 根据方向信息旋转图片
                    if orientation == 3:
                        image = image.rotate(180, expand=True)
                        logger.info("图片旋转180度")
                    elif orientation == 6:
                        image = image.rotate(270, expand=True)
                        logger.info("图片旋转270度")
                    elif orientation == 8:
                        image = image.rotate(90, expand=True)
                        logger.info("图片旋转90度")
                else:
                    logger.info("未检测到方向信息，保持原方向")
            else:
                logger.info("无EXIF信息，保持原方向")
        else:
            logger.info("图片无EXIF属性，保持原方向")
    except Exception as e:
        logger.error(f"修复图片方向时出错: {e}")
    
    return image



def allowed_file(filename):
    """检查文件格式是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {
        'png', 'jpg', 'jpeg', 'gif', 'bmp'
    }

def enhance_basic(image_path, scale_factor=2):
    """基础图像增强方法 - 优化版本，避免过度处理"""
    try:
        logger.info(f"开始基础增强: {image_path}")
        # 读取图像
        img = Image.open(image_path)
        
        # 修复图片方向
        img = fix_image_orientation(img)
        
        # 转换为RGB模式（处理RGBA等格式）
        if img.mode != 'RGB':
            img = img.convert('RGB')
            logger.info("图片已转换为RGB模式")
        
        # 1. 放大图像
        width, height = img.size
        new_width = width * scale_factor
        new_height = height * scale_factor
        enhanced = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logger.info(f"图片已放大到 {new_width}x{new_height}")
        
        # 2. 轻微锐化
        enhanced = enhanced.filter(ImageFilter.SHARPEN)
        logger.info("图片已轻微锐化")
        
        # 3. 适中的对比度增强
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.05)  # 降低对比度增强强度
        logger.info("图片对比度已增强")
        
        # 4. 轻微的亮度增强
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.01)  # 轻微提升亮度
        logger.info("图片亮度已增强")
        
        logger.info(f"基础增强完成: {image_path}")
        return enhanced
        
    except Exception as e:
        logger.error(f"基础增强失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return None

def enhance_quality_basic(image_path, scale_factor=2):
    """质量优先的基础增强方法 - 优化版本，避免过度处理"""
    try:
        logger.info(f"开始质量增强: {image_path}")
        img = Image.open(image_path)
        
        # 修复图片方向
        img = fix_image_orientation(img)
        
        # 转换为RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
            logger.info("图片已转换为RGB模式")
        
        # 1. 高质量放大
        width, height = img.size
        new_width = width * scale_factor
        new_height = height * scale_factor
        enhanced = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logger.info(f"图片已高质量放大到 {new_width}x{new_height}")
        
        # 2. 温和的锐化
        enhanced = enhanced.filter(ImageFilter.SHARPEN)
        logger.info("图片已温和锐化")
        
        # 3. 适中的对比度增强
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.08)  # 降低对比度增强强度
        logger.info("图片对比度已增强")
        
        # 4. 轻微的饱和度增强
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.03)  # 降低饱和度增强强度
        logger.info("图片饱和度已增强")
        
        # 5. 轻微的亮度调整
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.01)  # 轻微提升亮度
        logger.info("图片亮度已调整")
        
        logger.info(f"质量增强完成: {image_path}")
        return enhanced
        
    except Exception as e:
        logger.error(f"质量增强失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return None

def enhance_advanced(image_path, scale_factor=2):
    """高级图像增强方法 - 优化版本，避免过度处理"""
    try:
        logger.info(f"开始高级增强: {image_path}")
        img = Image.open(image_path)
        
        # 修复图片方向
        img = fix_image_orientation(img)
        
        # 转换为RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
            logger.info("图片已转换为RGB模式")
        
        # 1. 高质量放大
        width, height = img.size
        new_width = width * scale_factor
        new_height = height * scale_factor
        
        # 使用LANCZOS进行高质量放大
        enhanced = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logger.info(f"图片已高质量放大到 {new_width}x{new_height}")
        
        # 2. 温和的锐化处理
        enhanced = enhanced.filter(ImageFilter.SHARPEN)
        logger.info("图片已温和锐化处理")
        
        # 3. 适中的对比度增强
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.1)  # 降低对比度增强强度
        logger.info("图片对比度已增强")
        
        # 4. 轻微的饱和度增强
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.05)  # 降低饱和度增强强度
        logger.info("图片饱和度已增强")
        
        # 5. 轻微的亮度调整
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.02)  # 轻微提升亮度
        logger.info("图片亮度已调整")
        
        # 6. 边缘增强（只做一次）
        enhanced = enhanced.filter(ImageFilter.EDGE_ENHANCE)
        logger.info("图片已边缘增强")
        
        logger.info(f"高级增强完成: {image_path}")
        return enhanced
        
    except Exception as e:
        logger.error(f"高级增强失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return None

def enhance_super_clear(image_path, scale_factor=5):
    """极致超级清晰算法 - 重新优化版本，追求极致清晰度"""
    try:
        logger.info(f"开始极致超级清晰增强: {image_path}")
        img = Image.open(image_path)
        
        # 修复图片方向
        img = fix_image_orientation(img)
        
        # 转换为RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
            logger.info("图片已转换为RGB模式")
        
        # 第一阶段：高质量放大
        width, height = img.size
        target_width = width * scale_factor
        target_height = height * scale_factor
        
        # 使用LANCZOS进行高质量放大
        enhanced = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        logger.info(f"图片已高质量放大到 {target_width}x{target_height}")
        
        # 第二阶段：多级锐化处理 - 增强清晰度
        enhanced = enhanced.filter(ImageFilter.SHARPEN)
        logger.info("图片已多级锐化处理")
        enhanced = enhanced.filter(ImageFilter.EDGE_ENHANCE)
        logger.info("图片已多级锐化处理")
        enhanced = enhanced.filter(ImageFilter.EDGE_ENHANCE_MORE)
        logger.info("图片已多级锐化处理")
        
        # 第三阶段：强对比度增强 - 突出细节
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.25)  # 增强对比度强度
        logger.info("图片对比度已增强")
        
        # 第四阶段：饱和度增强 - 让色彩更鲜艳
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.2)  # 增强饱和度强度
        logger.info("图片饱和度已增强")
        
        # 第五阶段：亮度调整 - 确保细节可见
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.05)  # 适度提升亮度
        logger.info("图片亮度已调整")
        
        # 第六阶段：再次锐化 - 强化边缘细节
        enhanced = enhanced.filter(ImageFilter.SHARPEN)
        logger.info("图片已再次锐化")
        
        # 第七阶段：最终边缘增强 - 确保极致清晰
        enhanced = enhanced.filter(ImageFilter.EDGE_ENHANCE_MORE)
        logger.info("图片已最终边缘增强")
        
        # 第八阶段：最终锐化 - 确保每个细节都清晰可见
        enhanced = enhanced.filter(ImageFilter.SHARPEN)
        logger.info("图片已最终锐化")
        
        logger.info(f"极致超级清晰增强完成: {image_path}")
        return enhanced
        
    except Exception as e:
        logger.error(f"极致超级清晰增强失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return None

def enhance_super_quality(image_path, scale_factor=2):
    """超级质量增强方法 - 优化版本，避免过度处理"""
    try:
        logger.info(f"开始超级质量增强: {image_path}")
        img = Image.open(image_path)
        
        # 修复图片方向
        img = fix_image_orientation(img)
        
        # 转换为RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
            logger.info("图片已转换为RGB模式")
        
        # 1. 高质量放大 - 使用LANCZOS算法
        width, height = img.size
        target_width = width * scale_factor
        target_height = height * scale_factor
        
        # 直接使用LANCZOS进行高质量放大，避免分步放大导致的失真
        enhanced = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        logger.info(f"图片已高质量放大到 {target_width}x{target_height}")
        
        # 2. 温和的锐化处理 - 避免过度锐化
        enhanced = enhanced.filter(ImageFilter.SHARPEN)
        logger.info("图片已温和锐化处理")
        
        # 3. 对比度增强 - 使用适中的参数
        enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = enhancer.enhance(1.1)  # 降低对比度增强强度
        logger.info("图片对比度已增强")
        
        # 4. 饱和度增强 - 保持自然色彩
        enhancer = ImageEnhance.Color(enhanced)
        enhanced = enhancer.enhance(1.05)  # 降低饱和度增强强度
        logger.info("图片饱和度已增强")
        
        # 5. 亮度微调 - 轻微提升
        enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = enhancer.enhance(1.02)  # 轻微提升亮度
        logger.info("图片亮度已调整")
        
        # 6. 细节增强 - 使用边缘增强而非锐化
        enhanced = enhanced.filter(ImageFilter.EDGE_ENHANCE)
        logger.info("图片已细节增强")
        
        logger.info(f"超级质量增强完成: {image_path}")
        return enhanced
        
    except Exception as e:
        logger.error(f"超级质量增强失败: {e}")
        print(f"错误详情: {traceback.format_exc()}")
        return None



def apply_filter(image, filter_type):
    """应用滤镜效果"""
    try:
        logger.info(f"开始应用滤镜: {filter_type}")
        if filter_type == "blackwhite":
            image = image.convert('L').convert('RGB')
            logger.info("应用黑白滤镜")
        elif filter_type == "vintage":
            # 复古效果：降低饱和度，增加对比度
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(0.7)
            logger.info("应用复古滤镜")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            logger.info("应用复古滤镜")
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(0.9)
            logger.info("应用复古滤镜")
        elif filter_type == "film":
            # 胶片效果：轻微褪色
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(0.8)
            logger.info("应用胶片滤镜")
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            logger.info("应用胶片滤镜")
            return image
        elif filter_type == "fresh":
            # 清新效果：提高饱和度和亮度
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.3)
            logger.info("应用清新滤镜")
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            logger.info("应用清新滤镜")
        elif filter_type == "hdr":
            # HDR效果：高对比度
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            logger.info("应用HDR滤镜")
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.2)
            logger.info("应用HDR滤镜")
        elif filter_type == "warm":
            # 暖色调
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.4)
            logger.info("应用暖色调滤镜")
        elif filter_type == "cool":
            # 冷色调：降低饱和度
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(0.6)
            logger.info("应用冷色调滤镜")
        else:
            logger.info(f"未知的滤镜类型: {filter_type}, 保持原图")
            return image
        logger.info(f"滤镜应用完成: {filter_type}")
        return image
    except Exception as e:
        logger.error(f"滤镜应用失败: {e}")
        return image

def apply_adjustments(image, adjustments):
    """应用图像调整参数"""
    try:
        logger.info("开始应用图像调整...")
        # 亮度调整
        if 'brightness' in adjustments:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(adjustments['brightness'])
            logger.info(f"亮度调整: {adjustments['brightness']}")
        
        # 对比度调整
        if 'contrast' in adjustments:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(adjustments['contrast'])
            logger.info(f"对比度调整: {adjustments['contrast']}")
        
        # 饱和度调整
        if 'saturation' in adjustments:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(adjustments['saturation'])
            logger.info(f"饱和度调整: {adjustments['saturation']}")
        
        # 锐化调整
        if 'sharpness' in adjustments and adjustments['sharpness'] > 1.0:
            for _ in range(int(adjustments['sharpness'] - 1)):
                image = image.filter(ImageFilter.SHARPEN)
            logger.info(f"锐化调整: {adjustments['sharpness'] - 1}次")
        
        logger.info("图像调整完成")
        return image
    except Exception as e:
        logger.error(f"图像调整失败: {e}")
        return image

def create_poster(images, layout="grid"):
    """生成海报"""
    try:
        logger.info("开始生成海报...")
        if not images:
            logger.warning("没有图片数据，无法生成海报")
            return None
        
        # 计算海报尺寸
        if layout == "grid":
            cols = min(3, len(images))
            rows = (len(images) + cols - 1) // cols
            poster_width = cols * 300
            poster_height = rows * 300
        else:  # horizontal
            poster_width = len(images) * 300
            poster_height = 300
        
        # 创建海报画布
        poster = Image.new('RGB', (poster_width, poster_height), (255, 255, 255))
        logger.info(f"海报尺寸: {poster_width}x{poster_height}")
        
        # 放置图片
        for i, img_data in enumerate(images):
            try:
                # 解码base64图片
                img_bytes = base64.b64decode(img_data.split(',')[1])
                img = Image.open(io.BytesIO(img_bytes))
                
                # 修复图片方向
                img = fix_image_orientation(img)
                
                # 调整图片大小
                img = img.resize((280, 280), Image.Resampling.LANCZOS)
                logger.info(f"处理海报图片 {i}: 调整大小到 280x280")
                
                # 计算位置
                if layout == "grid":
                    x = (i % cols) * 300 + 10
                    y = (i // cols) * 300 + 10
                else:
                    x = i * 300 + 10
                    y = 10
                
                poster.paste(img, (x, y))
                logger.info(f"处理海报图片 {i}: 粘贴到位置 ({x}, {y})")
            except Exception as e:
                logger.error(f"处理海报图片 {i} 失败: {e}")
                continue
        
        logger.info("海报生成完成")
        return poster
    except Exception as e:
        logger.error(f"海报生成失败: {e}")
        return None

@app.route("/")
async def index(request: Request):
    """健康检查"""
    logger.info("收到健康检查请求")
    return json({"status": "healthy", "message": "图片高清化API服务运行中"})

@app.route("/api/upload", methods=["POST"])
async def upload_file(request: Request):
    """处理图片上传和增强"""
    try:
        logger.info("收到图片上传请求")
        # 检查是否有文件上传
        if "file" not in request.files:
            logger.warning("未上传文件")
            return json({"error": "没有文件上传"}, status=400)
        
        file_obj = request.files["file"][0]
        method = request.form.get("method", "traditional")
        
        if not file_obj.name:
            logger.warning("文件名为空")
            return json({"error": "没有选择文件"}, status=400)
        
        if not allowed_file(file_obj.name):
            logger.warning(f"不支持的文件格式: {file_obj.name}")
            return json({"error": "不支持的文件格式"}, status=400)
        
        # 保存上传的文件
        filename = f"{os.urandom(8).hex()}_{file_obj.name}"
        filepath = os.path.join(app.config.UPLOAD_FOLDER, filename)
        
        try:
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(file_obj.body)
            logger.info(f"文件保存成功: {filepath}")
            
            # 处理图片
            if method == "super_clear":
                enhanced_img = enhance_super_clear(filepath)
            elif method == "advanced":
                enhanced_img = enhance_advanced(filepath)
            elif method == "super_quality":
                enhanced_img = enhance_super_quality(filepath)
            else:
                enhanced_img = enhance_basic(filepath)
            
            if enhanced_img is None:
                logger.error(f"图片处理失败: {filepath}")
                return json({"error": "图片处理失败"}, status=500)
            
            # 转换为base64
            buffer = io.BytesIO()
            enhanced_img.save(buffer, format='JPEG', quality=95)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logger.info(f"图片处理成功: {filepath}")
            return json({
                "success": True,
                "enhanced_image": f"data:image/jpeg;base64,{img_base64}",
                "method": method
            })
            
        except Exception as e:
            logger.error(f"处理过程中出错: {e}")
            print(f"错误详情: {traceback.format_exc()}")
            return json({"error": f"处理失败: {str(e)}"}, status=500)
        
        finally:
            # 清理临时文件
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    logger.info(f"临时文件清理成功: {filepath}")
                except:
                    logger.error(f"清理临时文件失败: {filepath}")
    
    except Exception as e:
        logger.error(f"服务器错误: {e}")
        return json({"error": f"服务器错误: {str(e)}"}, status=500)

@app.route("/api/methods")
async def get_methods(request: Request):
    """获取可用的增强方法"""
    logger.info("收到获取增强方法请求")
    methods = [
        {
            "id": "traditional",
            "name": "传统增强",
            "description": "基于传统图像处理算法，温和提升分辨率与清晰度，保持自然效果。处理速度：极快（1-3秒）",
            "speed": "fast"
        },
        {
            "id": "super_clear",
            "name": "超级清晰",
            "description": "重新优化版8倍放大算法，多级锐化处理，强对比度和饱和度增强，追求极致清晰度。处理速度：较慢（8-15秒）",
            "speed": "slow"
        },
        {
            "id": "advanced",
            "name": "高级增强",
            "description": "结合传统和AI技术，温和的图像增强，保持自然色彩和清晰度。处理速度：中等（3-6秒）",
            "speed": "medium"
        },
        {
            "id": "super_quality",
            "name": "超级质量",
            "description": "高质量图像处理，温和的增强参数，确保图片清晰自然。处理速度：较慢（8-15秒）",
            "speed": "slow"
        }
    ]
    logger.info("返回增强方法列表")
    return json({"methods": methods})

@app.route("/api/health")
async def health_check(request: Request):
    """健康检查"""
    logger.info("收到健康检查请求")
    return json({
        "status": "healthy",
        "version": "basic"
    })

@app.route("/api/batch-enhance", methods=["POST"])
async def batch_enhance(request: Request):
    """批量高清化处理"""
    try:
        logger.info("收到批量高清化请求")
        data = request.json
        files = data.get("files", [])
        method = data.get("method", "traditional")
        
        if not files:
            logger.warning("批量处理无文件")
            return json({"error": "没有文件"}, status=400)
        
        results = []
        for file_data in files:
            try:
                # 解码base64图片
                img_bytes = base64.b64decode(file_data.split(',')[1])
                
                # 保存临时文件
                temp_filename = f"temp_{os.urandom(8).hex()}.jpg"
                temp_path = os.path.join(app.config.UPLOAD_FOLDER, temp_filename)
                
                with open(temp_path, 'wb') as f:
                    f.write(img_bytes)
                
                # 处理图片
                if method == "super_clear":
                    enhanced_img = enhance_super_clear(temp_path)
                elif method == "advanced":
                    enhanced_img = enhance_advanced(temp_path)
                elif method == "super_quality":
                    enhanced_img = enhance_super_quality(temp_path)
                else:
                    enhanced_img = enhance_basic(temp_path)
                
                if enhanced_img:
                    # 转换为base64
                    buffer = io.BytesIO()
                    enhanced_img.save(buffer, format='JPEG', quality=95)
                    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    results.append({
                        "success": True,
                        "enhanced_image": f"data:image/jpeg;base64,{img_base64}"
                    })
                else:
                    results.append({
                        "success": False,
                        "error": "处理失败"
                    })
                
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    logger.info(f"临时文件清理成功: {temp_path}")
                    
            except Exception as e:
                logger.error(f"批量处理图片失败: {e}")
                results.append({
                    "success": False,
                    "error": str(e)
                })
        
        logger.info("批量处理完成")
        return json({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        logger.error(f"批量处理失败: {e}")
        return json({"error": f"批量处理失败: {str(e)}"}, status=500)

@app.route("/api/apply-filter", methods=["POST"])
async def apply_filter_api(request: Request):
    """应用滤镜效果"""
    try:
        logger.info("收到滤镜应用请求")
        data = request.json
        image_data = data.get("image")
        filter_type = data.get("filter")
        
        if not image_data or not filter_type:
            logger.warning("滤镜应用缺少参数")
            return json({"error": "缺少参数"}, status=400)
        
        # 解码base64图片
        img_bytes = base64.b64decode(image_data.split(',')[1])
        img = Image.open(io.BytesIO(img_bytes))
        
        # 修复图片方向
        img = fix_image_orientation(img)
        
        # 应用滤镜
        filtered_img = apply_filter(img, filter_type)
        
        # 转换为base64
        buffer = io.BytesIO()
        filtered_img.save(buffer, format='JPEG', quality=95)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        logger.info(f"滤镜应用成功: {filter_type}")
        return json({
            "success": True,
            "filtered_image": f"data:image/jpeg;base64,{img_base64}",
            "filter": filter_type
        })
        
    except Exception as e:
        logger.error(f"滤镜应用失败: {e}")
        return json({"error": f"滤镜应用失败: {str(e)}"}, status=500)

@app.route("/api/adjust-image", methods=["POST"])
async def adjust_image_api(request: Request):
    """应用图像调整"""
    try:
        logger.info("收到图像调整请求")
        data = request.json
        image_data = data.get("image")
        adjustments = data.get("adjustments", {})
        
        if not image_data:
            logger.warning("图像调整缺少图片数据")
            return json({"error": "缺少图片数据"}, status=400)
        
        # 解码base64图片
        img_bytes = base64.b64decode(image_data.split(',')[1])
        img = Image.open(io.BytesIO(img_bytes))
        
        # 修复图片方向
        img = fix_image_orientation(img)
        
        # 应用调整
        adjusted_img = apply_adjustments(img, adjustments)
        
        # 转换为base64
        buffer = io.BytesIO()
        adjusted_img.save(buffer, format='JPEG', quality=95)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        logger.info("图像调整完成")
        return json({
            "success": True,
            "adjusted_image": f"data:image/jpeg;base64,{img_base64}"
        })
        
    except Exception as e:
        logger.error(f"图像调整失败: {e}")
        return json({"error": f"图像调整失败: {str(e)}"}, status=500)

@app.route("/api/generate-poster", methods=["POST"])
async def generate_poster_api(request: Request):
    """生成海报"""
    try:
        logger.info("收到海报生成请求")
        data = request.json
        images = data.get("images", [])
        layout = data.get("layout", "grid")
        
        if not images:
            logger.warning("海报生成无图片")
            return json({"error": "没有图片"}, status=400)
        
        # 生成海报
        poster = create_poster(images, layout)
        
        if poster:
            # 转换为base64
            buffer = io.BytesIO()
            poster.save(buffer, format='JPEG', quality=95)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            logger.info("海报生成成功")
            return json({
                "success": True,
                "poster": f"data:image/jpeg;base64,{img_base64}"
            })
        else:
            logger.error("海报生成失败")
            return json({"error": "海报生成失败"}, status=500)
        
    except Exception as e:
        logger.error(f"海报生成失败: {e}")
        return json({"error": f"海报生成失败: {str(e)}"}, status=500)

@app.route("/api/filters")
async def get_filters(request: Request):
    """获取可用的滤镜列表"""
    logger.info("收到获取滤镜列表请求")
    filters = [
        {"id": "blackwhite", "name": "黑白", "description": "经典黑白效果"},
        {"id": "vintage", "name": "复古", "description": "怀旧复古风格"},
        {"id": "film", "name": "胶片", "description": "胶片质感效果"},
        {"id": "fresh", "name": "清新", "description": "明亮清新风格"},
        {"id": "hdr", "name": "HDR", "description": "高动态范围效果"},
        {"id": "warm", "name": "暖色", "description": "温暖色调"},
        {"id": "cool", "name": "冷色", "description": "冷色调效果"}
    ]
    logger.info("返回滤镜列表")
    return json({"filters": filters})

if __name__ == "__main__":
    logger.info("应用启动")
    app.run(host="0.0.0.0", port=8000, debug=True) 