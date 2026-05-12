import os
from PIL import Image

def process_images(root_dir, target_size_kb=(500, 1000)):
    """
    全自动处理：统一格式为 .jpg + 重命名为序号 + 压缩体积
    """
    if not os.path.exists(root_dir):
        print(f"找不到文件夹: {root_dir}")
        return

    # 遍历 images 文件夹下的城市子文件夹
    for city_folder in os.listdir(root_dir):
        city_path = os.path.join(root_dir, city_folder)
        
        if os.path.isdir(city_path):
            print(f"--- 正在处理城市: {city_folder} ---")
            
            # 获取该文件夹下所有图片文件
            valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.heic', '.JPG', '.PNG')
            files = [f for f in os.listdir(city_path) if f.lower().endswith(valid_extensions)]
            
            # 排序确保重命名逻辑一致
            files.sort()

            for index, filename in enumerate(files):
                old_path = os.path.join(city_path, filename)
                new_name = f"{index + 1}.jpg"
                new_path = os.path.join(city_path, new_name)
                
                try:
                    # 1. 转换与格式统一
                    with Image.open(old_path) as img:
                        rgb_img = img.convert('RGB') # 强制转为 RGB 模式
                        
                        # 2. 压缩逻辑
                        quality = 95
                        while quality > 10:
                            rgb_img.save(new_path, "JPEG", quality=quality, optimize=True)
                            file_size = os.path.getsize(new_path) / 1024 # 转换为 KB
                            
                            if file_size <= target_size_kb[1]: # 满足小于 1MB
                                break
                            quality -= 5
                    
                    # 3. 清理旧文件（如果原名不是 1.jpg 这种格式，或者是 .png 等）
                    if old_path != new_path:
                        os.remove(old_path)
                        
                    print(f"成功: {filename} -> {new_name} ({file_size:.1f} KB)")
                
                except Exception as e:
                    print(f"处理失败 {filename}: {e}")

if __name__ == "__main__":
    # 执行处理
    process_images('images')
    print("\n✅ 所有照片已就位，准备好 git push 了！")