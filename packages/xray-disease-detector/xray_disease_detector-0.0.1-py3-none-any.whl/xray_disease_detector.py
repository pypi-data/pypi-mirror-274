import torch
from torchvision import transforms
from PIL import Image
import sys

class XRayDiseaseDetector:
    def __init__(self, model_path):
        self.model = torch.load(model_path)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
    def predict(self, img_path):
        img = Image.open(img_path).convert('RGB')
        img = self.transform(img)
        img = img.unsqueeze(0)  # Add batch dimension
        
        with torch.no_grad():
            outputs = self.model(img)
            _, predicted = torch.max(outputs, 1)
        
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
