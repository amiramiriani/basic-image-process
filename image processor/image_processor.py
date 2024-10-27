import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()

    def calculator_processor(self, x, gray_matrix):
        # Create a copy to avoid modifying the original grayscale matrix
        modified_matrix = np.copy(gray_matrix)

        # Subtract x from each pixel, ensuring values do not go below 0
        for i in range(len(modified_matrix)):
            for j in range(len(modified_matrix[i])):
                if (int(modified_matrix[i][j]) - x) < 0 : # in this position int most be there if we don't use it 0 - 1 = 255 then the program fails
                    modified_matrix[i][j] = 0 #  (cause its we have in binary 0 - 1 = 1 and if we have 8 bytes then 0 - 1 = 11111111)
                else:
                    modified_matrix[i][j] = modified_matrix[i][j] - x
        return modified_matrix
        

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Picture", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)", options=options)
        
        if file_name:
            # Read the image using OpenCV
            image = cv2.imread(file_name)
            
            # Show the original image
            cv2.imshow('Original', image)
            cv2.waitKey(0)

            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_matrix = np.array(gray_image)

            # Show the grayscale image
            cv2.imshow('Grayscale', gray_image)
            cv2.waitKey(0)
            return gray_matrix

if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    # Create an instance of the ImageProcessor class
    processor = ImageProcessor()

    # Call the method to open and process the image
    gray_matrix = processor.open_file()
    # Apply the calculator_processor
    if gray_matrix is not None:
        for z in [1, 3, 7, 15, 31, 63, 127, 255]:
            modified_matrix = processor.calculator_processor(z, gray_matrix)
            cv2.imshow(f'Modified Grayscale (x={z})', modified_matrix)
            cv2.waitKey(0)
    cv2.destroyAllWindows()
    
