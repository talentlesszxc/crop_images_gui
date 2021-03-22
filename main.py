from PyQt5 import QtWidgets
import sys
import design
import os
import cv2
import numpy as np

class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.input_folder_button.clicked.connect(self.get_input_folder)
        self.input_folder_button_2.clicked.connect(self.get_input_folder)
        self.input_folder_button_3.clicked.connect(self.get_input_folder)
        self.input_folder_button_4.clicked.connect(self.get_input_folder)
        self.output_folder_button.clicked.connect(self.get_output_folder)
        self.output_folder_button_2.clicked.connect(self.get_output_folder)
        self.output_folder_button_3.clicked.connect(self.get_output_folder)
        self.output_folder_button_4.clicked.connect(self.get_output_folder)
        
        self.start_button.clicked.connect(self.crop_images)
        
    
    def get_input_folder(self):
        self.input_directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if self.input_directory:
            self.input_path_edit.setText(self.input_directory) 
            self.input_path_edit_2.setText(self.input_directory)
            self.input_path_edit_3.setText(self.input_directory)
            self.input_path_edit_4.setText(self.input_directory)
    
    def get_output_folder(self):
        self.output_directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if self.output_directory:
            self.output_path_edit.setText(self.output_directory) 
            self.output_path_edit_2.setText(self.output_directory) 
            self.output_path_edit_3.setText(self.output_directory) 
            self.output_path_edit_4.setText(self.output_directory) 
            
    def crop_images(self):        
        root_path = self.input_path_edit.text()
        img_width = int(self.required_width_edit.text())
        img_height = int(self.required_height_edit.text())
        
        files = next(os.walk(root_path))[2]
        print('Total number of files =',len(files))
        number_of_file = 0
        for image_file in os.listdir(root_path):            
            image_path = root_path + '/' + image_file
            image = cv2.imread(image_path)
            number_of_file += 1
            counter = 0
            for r in range(0, image.shape[0], img_height):
                for c in range(0, image.shape[1], img_width):
                    counter += 1
                    blank_image = np.zeros((img_height ,img_width, 3), dtype = int)
                    new_image_path = self.output_path_edit.text()+ '/' + str(counter) + '_' +image_file
                    new_image = np.array(image[r:r+img_height, c:c+img_width,:])
                    blank_image[:new_image.shape[0], :new_image.shape[1], :] += new_image
                    cv2.imwrite(new_image_path, blank_image)                    
                    
            value = number_of_file/len(files)*100
            self.progressBar.setValue(value)      
            
    def crop_masks(self):          
        root_path = self.input_path_edit_2.text()
        mask_width = int(self.required_width_edit_2.text())
        mask_height = int(self.required_height_edit_2.text())
        
        files = next(os.walk(root_path))[2]
        print('Total number of files =',len(files))
        
        for mask_file in os.listdir(root_path):            
            mask_path = root_path + '/' + mask_file
            mask = cv2.imread(mask_path)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            mask = mask//38
            
            counter = 0
            for r in range(0, mask.shape[0], mask_height):
                for c in range(0, mask.shape[1], mask_width):
                    counter += 1
                    blank_mask = np.zeros((mask_height ,mask_width), dtype = int)
                    new_mask_path = self.output_path_edit.text()+ '/' + str(counter) + '_' +mask_file
                    new_mask = np.array(mask[r:r+mask_height, c:c+mask_width])
                    blank_mask[:new_mask.shape[0], :new_mask.shape[1]] += new_mask
                    cv2.imwrite(new_mask_path, blank_mask)  
            value = number_of_file/len(files)*100
            self.progressBar_2.setValue(value)
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
    
    #сделать галочку для грейскейла, если грейскейл, то при чтении будет mask = cv2.imread(mask_path,0)
    #возможность делать даунскейл для того чтобы идеально порезать без черных рамок