#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志功能测试脚本
"""

import logging
import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_logging.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def test_basic_logging():
    """测试基础日志功能"""
    logger.info("=== 开始测试基础日志功能 ===")
    
    # 测试不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息日志")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    
    logger.info("=== 基础日志功能测试完成 ===")

def test_image_processor_logging():
    """测试图像处理器的日志功能"""
    logger.info("=== 开始测试图像处理器日志功能 ===")
    
    try:
        from image_processor import create_processor
        logger.info("成功导入图像处理器模块")
        
        # 创建处理器实例
        processor = create_processor()
        logger.info("成功创建图像处理器实例")
        
        # 测试一个简单的图像处理（使用不存在的文件来测试错误日志）
        test_image_path = "test_nonexistent_image.jpg"
        logger.info(f"测试处理不存在的图像: {test_image_path}")
        
        # 这会触发错误日志
        result = processor.enhance_traditional(test_image_path)
        if result is None:
            logger.info("预期的错误处理：图像不存在，返回None")
        
        logger.info("=== 图像处理器日志功能测试完成 ===")
        
    except Exception as e:
        logger.error(f"测试图像处理器日志功能时出错: {e}")

def test_app_logging():
    """测试应用日志功能"""
    logger.info("=== 开始测试应用日志功能 ===")
    
    try:
        # 模拟一些应用级别的日志
        logger.info("模拟收到图片上传请求")
        logger.info("检查文件格式...")
        logger.info("文件格式验证通过")
        logger.info("开始图像处理...")
        logger.info("图像处理完成")
        logger.info("返回处理结果")
        
        logger.info("=== 应用日志功能测试完成 ===")
        
    except Exception as e:
        logger.error(f"测试应用日志功能时出错: {e}")

def main():
    """主测试函数"""
    logger.info("开始日志功能测试")
    
    # 测试基础日志
    test_basic_logging()
    
    # 测试图像处理器日志
    test_image_processor_logging()
    
    # 测试应用日志
    test_app_logging()
    
    logger.info("所有日志功能测试完成")
    print("日志测试完成，请查看控制台输出和 test_logging.log 文件")

if __name__ == "__main__":
    main() 