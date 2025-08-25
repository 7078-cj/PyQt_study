from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QListWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os
from PIL import Image, ImageFilter, ImageEnhance

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Image Editing App")
main_window.resize(900, 700)

btn_folder = QPushButton("Open Folder")
file_list = QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror = QPushButton("Mirror")
sharpness  = QPushButton("Sharpness")
gray = QPushButton("B/W")
saturation = QPushButton("Color")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")

#dropdown box
filter_box = QComboBox()
filter_box.addItems(["Original","Left", "Right", "Mirror", "Sharpness", "B/W", "Saturation", "Contrast", "Blur"])
picture_box = QLabel("No Image")

#app design
main_layout = QHBoxLayout()
left_layout = QVBoxLayout()
right_layout = QVBoxLayout()

left_layout.addWidget(btn_folder)
left_layout.addWidget(file_list)
left_layout.addWidget(filter_box)
left_layout.addWidget(btn_left)
left_layout.addWidget(btn_right)
left_layout.addWidget(mirror)
left_layout.addWidget(sharpness)
left_layout.addWidget(gray)
left_layout.addWidget(saturation)
left_layout.addWidget(contrast)
left_layout.addWidget(blur)

right_layout.addWidget(picture_box)

#you can adjust the stretch factors to change the relative sizes of the layouts
main_layout.addLayout(left_layout, 20)
main_layout.addLayout(right_layout, 80)

main_window.setLayout(main_layout)

#all app functionality
working_directory = ""

#filter file and extensions
def filter(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
                
    return results

#choose current work directory
def getWorkDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = ['.jpg','.jpeg', '.png', '.svg']
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)
        
class Editor():
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = "edits/"
        
    def load_image(self, filename):
        self.filename = filename
        fullname  = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()
        
    def save_image(self):
        path = os.path.join(working_directory, self.save_folder)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
            
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
        
    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w, h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()
        
    def save_show_edit(self):
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename) # to access the edited picture
        self.show_image(image_path)
        
    def gray(self):
        self.image = self.image.convert("L")
        self.save_show_edit()
    
    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_show_edit()
    
    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_show_edit()
    
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_show_edit()
        
    def sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_show_edit()
    
    def color(self):
        self.image = ImageEnhance.Color(self.image).enhance(1.2)
        self.save_show_edit()
    
    def contrast(self):
        self.image = ImageEnhance.Contrast(self.image).enhance(1.2)
        self.save_show_edit()
    
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.save_show_edit()
        
    def apply_filter(self, filter_name):
        if filter_name == "Original":
            self.image = self.original.copy()
            self.save_show_edit()
        
        else:
            filter_mapping = {
                "Left": self.left, 
                "Right": self.right, 
                "Mirror": self.mirror, 
                "Sharpness": self.sharpen, 
                "B/W": self.gray, 
                "Saturation": self.color, 
                "Contrast": self.contrast, 
                "Blur": self.blur
            }
            filter_function = filter_mapping.get(filter_name)
            if filter_function:
                filter_function()
        

main = Editor()
  
def displayImage():
    if file_list.currentRow()  >= 0 :
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_directory, main.filename))
        
def handle_filter():
    if file_list.currentRow() >= 0:
        select_filter = filter_box.currentText()
        main.apply_filter(select_filter)
        

        
    

btn_folder.clicked.connect(getWorkDirectory)
file_list.currentRowChanged.connect(displayImage)
filter_box.currentTextChanged.connect(handle_filter)

gray.clicked.connect(lambda: main.gray())
btn_left.clicked.connect(lambda: main.left())
btn_right.clicked.connect(lambda: main.right())
mirror.clicked.connect(lambda: main.mirror())
sharpness.clicked.connect(lambda: main.sharpen())
saturation.clicked.connect(lambda: main.color())
contrast.clicked.connect(lambda: main.contrast())
blur.clicked.connect(lambda: main.blur())


main_window.show()
app.exec_()