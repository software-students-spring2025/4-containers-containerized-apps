import logging
import time
from typing import Dict, List, Tuple, Any, Optional

import cv2
import numpy as np
from PIL import Image

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class YOLOv8Detector:

    def __init__(
        self,
        confidence_threshold: float = 0.5,
        model_size: str = "n",  # 'n', 's', 'm', 'l', 'x'
        model_path: Optional[str] = None,
    ):

        self.confidence_threshold = confidence_threshold
        self.model_size = model_size
        self.model_path = model_path
        self.model = None
        
        logger.info("Initializing YOLOv8 detector with confidence threshold %s", confidence_threshold)
        
    def load_model(self) -> bool:
        try:
            from ultralytics import YOLO   
            self.model = YOLO('yolov8n')
            
            logger.info("Loaded YOLOv8 model: yolov8n")
            return True
                
        except Exception as e:
            logger.error("Error loading YOLOv8 model: %s", str(e))
            return False
    
    def detect_objects(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        if self.model is None:
            logger.error("Model not loaded. Call load_model() first.")
            return []
        
        detections = []
        
        try:
            # Run inference
            results = self.model(frame, verbose=False)
            result = results[0]  # First image result
            
            # Process detections
            for box in result.boxes:
                confidence = float(box.conf)
                
                if confidence >= self.confidence_threshold:
                    class_id = int(box.cls)
                    class_name = result.names[class_id]
                    
                    # Get bounding box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    box_width = x2 - x1
                    box_height = y2 - y1
                    
                    # Create detection result in common format
                    detection = {
                        "class_id": class_id,
                        "class_name": class_name,
                        "confidence": confidence,
                        "bbox": (x1, y1, box_width, box_height)
                    }
                    detections.append(detection)
        
        except Exception as e:
            logger.error("Error during object detection: %s", str(e))
            
        return detections
    
    def annotate_frame(
        self, 
        frame: np.ndarray, 
        detections: List[Dict[str, Any]],
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2,
        font_scale: float = 0.5
    ) -> np.ndarray:
        annotated_frame = frame.copy()
        
        for detection in detections:
            # Extract details
            class_name = detection["class_name"]
            confidence = detection["confidence"]
            box_x, box_y, box_width, box_height = detection["bbox"]
            
            # Draw bounding box
            cv2.rectangle(
                annotated_frame, 
                (box_x, box_y), 
                (box_x + box_width, box_y + box_height), 
                color, 
                thickness
            )
            
            # Create label with class name and confidence
            label = f"{class_name}: {confidence:.2f}"
            
            # Calculate label position
            label_y = max(box_y - 10, 10)
            label_x = box_x
            
            # Draw label background
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
            cv2.rectangle(
                annotated_frame, 
                (label_x, label_y - text_size[1] - 10), 
                (label_x + text_size[0], label_y), 
                color, 
                cv2.FILLED
            )
            
            # Draw label text
            cv2.putText(
                annotated_frame, 
                label, 
                (label_x, label_y - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, 
                (0, 0, 0), 
                thickness
            )
            
        return annotated_frame
    
    def get_detection_stats(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not detections:
            return {
                "count": 0,
                "classes": {},
                "avg_confidence": 0,
                "timestamp": time.time()
            }
            
        # Count objects by class
        class_counts = {}
        total_confidence = 0
        
        for detection in detections:
            class_name = detection["class_name"]
            confidence = detection["confidence"]
            
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1
                
            total_confidence += confidence
            
        return {
            "count": len(detections),
            "classes": class_counts,
            "avg_confidence": total_confidence / len(detections) if detections else 0,
            "timestamp": time.time()
        }

def process_image_detection(
    img: Image.Image, 
    confidence_threshold: float = 0.5, 
    model_size: str = "n", 
    model_path: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], Image.Image]:
    # Convert PIL (RGB) to OpenCV format (BGR)
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Initialize detector instance
    detector = YOLOv8Detector(confidence_threshold=confidence_threshold, model_size=model_size, model_path=model_path)
    if not detector.load_model():
        raise RuntimeError("Failed to load YOLOv8 model.")
    
    # Perform detection on the frame
    detections = detector.detect_objects(frame)
    
    # Annotate the frame with detection boxes and labels
    annotated_frame = detector.annotate_frame(frame, detections)
    
    # Convert annotated frame back to PIL Image (convert BGR to RGB)
    annotated_img = Image.fromarray(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
    
    return detections, annotated_img
