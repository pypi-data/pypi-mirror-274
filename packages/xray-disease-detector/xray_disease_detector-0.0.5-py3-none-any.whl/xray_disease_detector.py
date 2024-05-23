# src/xray_disease_detector.py

import torch
from torchvision import transforms, models
from torch import nn
from PIL import Image
import sys

class XRayDiseaseDetector:
    def __init__(self, model_path=None):
        self.model = self.load_model(model_path)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
    def load_model(self, model_path):
        model = models.vit_b_16(weights='DEFAULT')
        num_ftrs = model.heads.head.in_features
        model.heads.head = nn.Linear(num_ftrs, 8)  # 假设你的模型有8个输出类别
        if model_path:
            state_dict = torch.load(model_path)
            # 移除分类头的权重
            del state_dict['heads.head.weight']
            del state_dict['heads.head.bias']
            model.load_state_dict(state_dict, strict=False)
        return model
        
    def predict(self, img_path):
        img = Image.open(img_path).convert('RGB')
        img = self.transform(img)
        img = img.unsqueeze(0)  # 添加批次维度
        
        with torch.no_grad():
            outputs = self.model(img)
            _, predicted = torch.max(outputs.logits, 1)  # ViT模型的输出需要访问logits
        
        return predicted.item()

def main():
    if len(sys.argv) != 3:
        print("Usage: xray_disease_detector <model_path> <image_path>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    image_path = sys.argv[2]
    
    detector = XRayDiseaseDetector(model_path)
    result = detector.predict(image_path)
    print(f"Prediction: {result}")

if __name__ == "__main__":
    main()
