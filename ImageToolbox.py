import dearpygui.dearpygui as gui 
from dearpygui.dearpygui import *
from PIL import Image
import math

filename = ""

gui.create_context()
gui.create_viewport(title='Image Processing Toolbox', width=800, height=600)


def callback(sender, app_data, user_data):
    # function opens selected image file from file selectors and displays it
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global filename
    key = list(app_data['selections'])[0]
    filename = app_data['selections'][key]
    print(filename)
    img = Image.open(filename)
    img.show()

def crop_function(sender, data, user_data): 
    # set the user inputted values
    left_bound = (get_value(user_data[0]))
    upper_bound = (get_value(user_data[1]))
    right_bound = (get_value(user_data[2]))
    lower_bound = (get_value(user_data[3]))
    new_x = 0
    new_y = 0
    img = Image.open(filename)
    # create new image with dimentions of cropped box
    new_image = Image.new(mode='RGB', size=(right_bound-left_bound, upper_bound-lower_bound), color=(0, 0, 0))
    for y in range(lower_bound,upper_bound):
        new_x = 0
        for x in range(left_bound,right_bound):
            #copy pixel within the cropped box to new image
            new_image.putpixel((new_x, new_y), img.getpixel((x,y))) 
            new_x+=1
        new_y+=1
    # Save the image to a file and shows it to the user
    new_image.save('croped_image.jpg')
    new_image.show()

def crop():
    # creates new window for crop tool
    with gui.window(label="Crop Tool", width=1200, height=1200): 
        img = Image.open(filename)
        width, height = img.size
        add_text("Input coordinates of the box to crop:", indent=10)
        left_bound = add_input_int(label="Left Boundary Coordinate",indent=10,width=100,min_value=1, max_value=width, min_clamped=True, max_clamped=True)
        upper_bound = add_input_int(label="Upper Boundary Coordinate",indent=10,width=100,min_value=1, max_value=height, min_clamped=True, max_clamped=True)
        right_bound = add_input_int(label="Right Boundary Coordinate",indent=10,width=100,min_value=1, max_value=width, min_clamped=True, max_clamped=True)
        lower_bound = add_input_int(label="Lower Boundary Coordinate",indent=10,width=100,min_value=1, max_value=height, min_clamped=True, max_clamped=True)
        add_button(label="Crop Image", indent=10, callback=crop_function, user_data=[left_bound, upper_bound, right_bound, lower_bound])

def flip_vert_function():
    # open image file and initializes new image
    img = Image.open(filename)
    width, height = img.size
    new_image = Image.new(mode='RGB', size=(width, height), color=(0, 0, 0))
    for x in range(width):
        new_y = height-1
        for y in range(height):
            # for every column of pixels the order get reversed in new image
            new_image.putpixel((x,new_y), img.getpixel((x,y)))
            new_y-=1
    # Save the image to a file
    new_image.save('vert_flip_image.jpg')
    # Display image to user
    new_image.show()

def flip_hori_function():
    # open image file and initializes new image
    img = Image.open(filename)
    width, height = img.size
    new_image = Image.new(mode='RGB', size=(width, height), color=(0, 0, 0))
    for y in range(height):
        new_x = width-1
        for x in range(width):
            # for every row of pixels the order get reversed in new image
            new_image.putpixel((new_x,y), img.getpixel((x,y)))
            new_x-=1
    # Save the image to a file
    new_image.save('hori_flip_image.jpg')
    # Display image to user
    new_image.show()

def flip():
    # creates a new window for flip tool
    with gui.window(label="Flip Tool", width=1200, height=1200):
        add_text("Select which direction you wish to flip image:", indent=10)
        add_spacer(height=5)
        add_button(label="Flip Image Verically", indent=10, callback=flip_vert_function)
        add_spacer(height=2)
        add_button(label="Flip Image Horizontally", indent=10, callback=flip_hori_function)

def scale_function(sender, data, user_data):
    # open image file and initializes new image
    img = Image.open(filename)
    width, height = img.size
    factor = (get_value(user_data[0]))
    new_image = Image.new(mode='RGB', size=(width*factor, height*factor), color=(0, 0, 0))
    for y in range(height*factor):
        for x in range(width*factor):
            # iterates through all pixels and applies linear interpolation to pixel original image
            new_image.putpixel((x,y), img.getpixel((int(x/factor),int(y/factor))))
    # Save the image to a file
    new_image.save('scaled_image.jpg')
    # Display image to user
    new_image.show()

def scale():
    # create new window for scaling tool
    with gui.window(label="Flip Tool", width=1200, height=1200):
        add_text("Enter the scaling factor you wish to apply to image:", indent=10)
        add_spacer(height=5)
        factor = add_input_int(indent=10,width=100,min_value=1, max_value=5, min_clamped=True, max_clamped=True)
        add_spacer(height=3)
        add_button(label="Scale Image", indent=10, callback=scale_function, user_data=[factor])

def rotate_function(sender, data, user_data):
    # open image file
    img = Image.open(filename)
    width, height = img.size
    angle = (get_value(user_data[0]))
    new_angle = math.radians(angle)

    # calculate the new width and height using pythagorean theorem
    new_width = round(math.sqrt(width**2 + height**2) * abs(math.cos(new_angle - math.atan(height/width))))
    new_height = math.ceil(abs(height * math.cos(new_angle)) + abs(width * math.sin(new_angle)))
    # calculate the center position of image
    center_x = int(new_width / 2)
    center_y = int(new_height / 2)
    new_image = Image.new(mode='RGB', size=(new_width, new_height), color=(0, 0, 0))
    for x in range(new_height):
        for y in range(new_width):
            # iterates through all pixels and get corresponding pixel
            old_x = int((x - center_x) * math.cos(-new_angle) - (y - center_y) * math.sin(-new_angle)) + int(width / 2)
            old_y = int((x - center_x) * math.sin(-new_angle) + (y - center_y) * math.cos(-new_angle)) + int(height / 2)
            
            # check if the old pixel is within bounds
            if old_x >= 0 and old_x < width and old_y >= 0 and old_y < height:
                # set pixel from old image as pixel in new image
                pixel = img.getpixel((old_x, old_y))
                new_image.putpixel((x, y), pixel)
    # Save the image to a file
    new_image.save('rotated_image.jpg')
    # Display image to user
    new_image.show()


def rotate():
    # create new window for rotate tool
    with gui.window(label="Rotate Tool", width=1200, height=1200):
        add_text("Enter the degree you wish to rotate the image by:", indent=10)
        add_spacer(height=5)
        degree = add_input_int(indent=10,width=100,min_value=1, max_value=360, min_clamped=True, max_clamped=True)
        add_spacer(height=3)
        add_button(label="Rotate Image", indent=10, callback=rotate_function, user_data=[degree]) 


def zero_padding_function(sender, data, user_data):
    # open image file 
    img = Image.open(filename)
    width, height = img.size
    padding = (get_value(user_data[0]))
    # initializes new image with value set to black
    new_image = Image.new(mode='RGB', size=(width+(padding*2), height+(padding*2)), color=(0, 0, 0))
    
    # goes through all pixels, adds padding to x and y and sets pixel in new image
    for y in range(height):
        for x in range(width):
            new_image.putpixel((x+padding,y+padding), img.getpixel((x,y)))
    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('padded_image.jpg')
    

def zero_padding():
    # create new window for zero padding tool
    with gui.window(label="Zero Padding Tool", width=1200, height=1200):
        add_text("Enter the amount of padding you wish to add to image (in pixels):", indent=10)
        add_spacer(height=5)
        padding = add_input_int(indent=10,width=100,min_value=1, max_value=400, min_clamped=True, max_clamped=True)
        add_spacer(height=3)
        add_button(label="Apply Padding", indent=10, callback=zero_padding_function, user_data=[padding]) 


def linear_mapping_function(sender, data, user_data):
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    width, height = img.size
    # set a and b values
    a = (get_value(user_data[0]))
    b = (get_value(user_data[1]))
    new_image = Image.new(mode='L', size=(width, height), color=0)
    image_gray = img.convert("L")
    image_gray.show()

    # iterates through all pixels in image
    for y in range(height):
        for x in range(width):
            # apply formula to grey value
            u = image_gray.getpixel((x,y))
            mapped = int(a*u+b)
            # Make sure resulting grey value doesn't go above or below limit
            if mapped > 255:
                mapped = 255
            elif mapped < 0:
                mapped = 0
            # set grey value for pixel in new image
            new_image.putpixel((x,y), mapped)
    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('linear_mapped_image.jpg')


def linear_mapping():
    # creates new window for linear mapping tool
    with gui.window(label="Linear Mapping Tool", width=1200, height=1200):
        add_text("Enter the values you wish to use for the gain and bais:", indent=10)
        add_spacer(height=5) # can the input only be an integer
        a = add_input_int(label="Bais (Changes Image Brightness)",indent=10,width=100,min_value=1, max_value=40, min_clamped=True, max_clamped=True)
        add_spacer(height=2)
        b = add_input_int(label="Gain (Changes Image Contrast)",indent=10,width=100,min_value=-40, max_value=40, min_clamped=True, max_clamped=True)
        add_spacer(height=3)
        add_button(label="Apply Linear Mappping", indent=10, callback=linear_mapping_function, user_data=[a,b]) 


def powerlaw_mapping_function(sender, data, user_data):
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    width, height = img.size
    # sets gamma value from user input
    gamma = (get_value(user_data[0]))
    new_image = Image.new(mode='L', size=(width, height), color=0)
    image_gray = img.convert("L")
    image_gray.show()

    # iterates through all pixels in image
    for y in range(height):
        for x in range(width):
            # for each pixel calculate using formula
            u = image_gray.getpixel((x,y))
            mapped = int(255*math.pow(u/255, gamma))
            # Make sure resulting grey value doesn't go above or below limit
            if mapped > 255:
                mapped = 255
            elif mapped < 0:
                mapped = 0
            # set grey value for pixel in new image
            new_image.putpixel((x,y), mapped)
    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('powerlaw_mapped_image.jpg')



def powerlaw_mapping():
    # create new window for power-law mappong tool
    with gui.window(label="Power-Law Mapping Tool", width=1200, height=1200):
        add_text("Enter the values you wish to use for gamma:", indent=10)
        add_spacer(height=5)
        gamma = add_input_float(label="Gamma (Changes Contrast Enhancement)",indent=10,width=100,min_value=-40, max_value=40, min_clamped=True, max_clamped=True)
        add_spacer(height=3)
        add_button(label="Apply Power-Law Mappping", indent=10, callback=powerlaw_mapping_function, user_data=[gamma]) 

def convolution_function(sender, data, user_data):
    kernel = [[ 1,  1,  1],
              [ 1,  1,  1],
              [ 1,  1,  1]]
    img = Image.open(filename)
    width, height = img.size
    # set the kernel value using user input values
    kernel[0][0] = (get_value(user_data[0]))
    kernel[0][1] = (get_value(user_data[1]))
    kernel[0][2] = (get_value(user_data[2]))
    kernel[1][0] = (get_value(user_data[3]))
    kernel[1][1] = (get_value(user_data[4]))
    kernel[1][2] = (get_value(user_data[5]))
    kernel[2][0] = (get_value(user_data[6]))
    kernel[2][1] = (get_value(user_data[7]))
    kernel[2][2] = (get_value(user_data[8]))
    new_image = Image.new(mode='L', size=(width, height), color=0)
    image_gray = img.convert("L")
    image_gray.show()

    # iterate through all pixels in orginal image
    for y in range(height):
        for x in range(width):
            # if its a border pixel then continue
            if y == 0 or y == height-1 or x == 0 or x == width-1:
                continue
            value = 0
            for neighbour_x in range(-1,2):
                for neighbour_y in range(-1,2):
                    # calculate sum of all pixels times the kernel value in 3x3 neigbourhood 
                    u = image_gray.getpixel((x+neighbour_x,y+neighbour_y))
                    value += u * kernel[neighbour_y+1][neighbour_x+1] 
            # Make sure grey value doesn't go above or below limit
            if value > 255:
                value = 255
            if value < 0:
                value = 0
            new_image.putpixel((x,y), value)

    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('convolution_image.jpg')


def convolution():
    # creates new window for convolution tool
    with gui.window(label="Convolution Tool", width=1200, height=1200):
        add_text("Enter the values you wish to use for the kernel:", indent=10)
        add_spacer(height=5)
        with group(horizontal=True): 
            zero = add_input_int(indent=10,width=30, step=0, step_fast=0)
            one = add_input_int(indent=50,width=30, step=0, step_fast=0)
            two = add_input_int(indent=90,width=30, step=0, step_fast=0)
        with group(horizontal=True): 
            three = add_input_int(indent=10,width=30, step=0, step_fast=0)
            four = add_input_int(indent=50,width=30, step=0, step_fast=0)
            five = add_input_int(indent=90,width=30, step=0, step_fast=0)
        with group(horizontal=True): 
            six = add_input_int(indent=10,width=30, step=0, step_fast=0)
            seven = add_input_int(indent=50,width=30, step=0, step_fast=0)
            eight = add_input_int(indent=90,width=30, step=0, step_fast=0)
        add_spacer(height=3)
        add_button(label="Apply Convolution", indent=10, callback=convolution_function, user_data=[zero,one,two,three,four,five,six,seven,eight]) 


def min_filtering_function():
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    width, height = img.size
    image_gray = img.convert("L")
    image_gray.show()
    new_image = Image.new(mode='L', size=(width, height), color=0)
    for y in range(height):
        for x in range(width):
            minimum = 0
            # if its a border pixel then continue
            if y == 0 or y == height-1 or x == 0 or x == width-1:
                continue
            for neighbour_x in range(-1,2):
                for neighbour_y in range(-1,2):
                    grey_level = image_gray.getpixel((x+neighbour_x, y+neighbour_y))
                    # calculates the 3 x 3 neigbourhood pixel grey value is new minimum
                    if grey_level > minimum:
                        minimum = grey_level
                    if y==1 and x==1:
                        print(grey_level)
            # minimum value of neighbourhood is set for the pixel in new image
            new_image.putpixel((x,y), minimum)

    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('min_filtering_image.jpg')


def max_filtering_function():
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    width, height = img.size
    image_gray = img.convert("L")
    image_gray.show()
    new_image = Image.new(mode='L', size=(width, height), color=0)
    for y in range(height):
        for x in range(width):
            maximum = 0
            # if its a border pixel then continue
            if y == 0 or y == height-1 or x == 0 or x == width-1:
                continue
            for neighbour_x in range(-1,2):
                for neighbour_y in range(-1,2):
                    grey_level = image_gray.getpixel((x+neighbour_x, y+neighbour_y))
                    # calculates the 3 x 3 neigbourhood pixel grey value is new max
                    if grey_level > maximum:
                        maximum = grey_level
            # max value of neighbourhood is set for the pixel in new image
            new_image.putpixel((x,y), maximum)

    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('max_filtering_image.jpg')


def median_filtering_function():
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    width, height = img.size
    image_gray = img.convert("L")
    image_gray.show()
    new_image = Image.new(mode='L', size=(width, height), color=0)
    for y in range(height):
        for x in range(width):
            neighbour_values = []
            # if its a border pixel then continue
            if y == 0 or y == height-1 or x == 0 or x == width-1:
                continue
            for neighbour_x in range(-1,2):
                for neighbour_y in range(-1,2):
                    # appends all the 3 x 3 neighbouring pixels to an array
                    neighbour_values.append(image_gray.getpixel((x+neighbour_x, y+neighbour_y)))
            # sorts the array and gets the median value
            neighbour_values.sort()
            # median value of neighbourhood is set for the pixel in new image
            colour = neighbour_values[int((len(neighbour_values)+1)/2)-1]
            new_image.putpixel((x,y), colour)

    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('median_filtering_image.jpg')
    

def filtering():
    # creates new window for non-linear filtering tool
    with gui.window(label="Non-linear Filtering Tool", width=1200, height=1200):
        add_text("Select which type of filtering you wish to apply to image:", indent=10)
        add_spacer(height=5)
        add_button(label="Min Filtering", indent=10, callback=min_filtering_function)
        add_spacer(height=2)
        add_button(label="Max Filtering", indent=10, callback=max_filtering_function)
        add_spacer(height=2)
        add_button(label="Median Filtering", indent=10, callback=median_filtering_function)


# SUPRISE FEATURE - EDGE DETECTION
def edge_detection_function():
    horizontal=[[-1, -2, -1],
                [ 0,  0,  0],
                [ 1,  2,  1]]
    vertical = [[-1,  0,  1],
                [-2,  0,  2],
                [-1,  0,  1]]
    
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    width, height = img.size
    image_gray = img.convert("L")
    image_gray.show()
    new_image = Image.new(mode='L', size=(width, height), color=0)
    for y in range(height):
        for x in range(width):
            x_gradient = 0
            y_gradient = 0
            # if its a border pixel then continue
            if y == 0 or y == height-1 or x == 0 or x == width-1:
                continue
            for neighbour_x in range(-1,2):
                for neighbour_y in range(-1,2):
                    # sums up the x and y gradient for every neighbourhood pixel
                    x_gradient+=image_gray.getpixel((x+neighbour_x, y+neighbour_y))*horizontal[neighbour_y+1][neighbour_x+1]
                    y_gradient+=image_gray.getpixel((x+neighbour_x, y+neighbour_y))*vertical[neighbour_y+1][neighbour_x+1]
            # calculates the magnitude for every pixel
            magnitude = int(math.sqrt(x_gradient**2 + y_gradient**2))
            threshold = 150
            # Set the pixel in the new image to white if magnitude is above gradient
            if magnitude > threshold:
                new_image.putpixel((x, y), 255)

    # Display image to user
    new_image.show()
    # Save the image to a file
    new_image.save('edge_detection_image.jpg')


# SUPRISE FEATURE - EDGE DETECTION
def edge_detection():
    # creates new window for histogram tool
    with gui.window(label="Edge Detection Tool", width=1200, height=1200):
        add_text("Click button to detect edges in the image:", indent=10)
        add_spacer(height=5)
        add_button(label="Apply Edge Detection", indent=10, callback=edge_detection_function)


def histogram_equalization():
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    histogram = calculate_histogram()
    width, height = img.size
    image_gray = img.convert("L")
    image_gray.show()
    new_image = Image.new(mode='L', size=(width, height), color=0)

    ## calculate the cumulative distribution function of the histogram
    sum = 0
    distribution_function = [0] * 256
    for index in range(0,len(histogram)):
        distribution_function[index] = sum
        sum += histogram[index]

    # Normalize the cumaltive distribution function
    normalized_function = [0] * 256
    for index in range(0,len(distribution_function)):
        H = distribution_function[index] / (width * height)
        normalized_function[index] = int(255 * H)

    # apply histogram equalization to the image
    for y in range(height):
        for x in range(width):
            new_graylevel = normalized_function[image_gray.getpixel((x, y))]
            new_image.putpixel((x, y), (new_graylevel))
    # Displays image to user
    new_image.show()
    # Save the image to a file
    new_image.save('histogram_equalization_image.jpg')


def calculate_histogram():
    # open image file, convert to greyscale and show image
    img = Image.open(filename)
    width, height = img.size
    image_gray = img.convert("L")
    image_gray.show()

    # initializes histogram
    histogram = [0] * 256
    for y in range(height):
        for x in range(width):
            # sets the values in the histogram
            histogram[image_gray.getpixel((x, y))] += 1
    return histogram


def histogram():
    # creates the new window for the histogram tool
    with gui.window(label="Histogram Calculation Tool", width=1200, height=1200):
        add_text("Select which option you wish to apply to image:", indent=10)
        add_spacer(height=5)
        add_button(label="Calculate Histogram", indent=10, callback=calculate_histogram) 
        add_spacer(height=2)
        add_button(label="Histogram Equalization", indent=10, callback=histogram_equalization)
    
# adds the file selector button
with gui.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=700 ,height=400):
    gui.add_file_extension(".*")
    # colours directories grean
    gui.add_file_extension("", color=(0, 150, 150, 255))
    gui.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255)) 
    gui.add_file_extension(".h", color=(255, 0, 255, 255), custom_text="[header]")
    gui.add_file_extension(".py", custom_text="[Python]")
    # colours image files green
    gui.add_file_extension(".png", color=(150, 255, 150, 255))
    gui.add_file_extension(".jpeg", color=(150, 255, 150, 255))
    gui.add_file_extension(".jpg", color=(150, 255, 150, 255))

# add a font registry which changes the font
with gui.font_registry():
    # first argument ids the path to the .ttf or .otf file
    default_font = gui.add_font("NotoSerifCJKjp-Medium.otf", 20)

# loads all the images used for the buttons
width, height, channels, data = load_image("icons/crop_icon.jpeg")
width2, height2, channels2, data2 = load_image("icons/flip_icon.png")
width3, height3, channels3, data3 = load_image("icons/scale_icon.jpeg")
width4, height4, channels4, data4 = load_image("icons/rotate_icon.png")
width5, height5, channels5, data5 = load_image("icons/padding_icon.png")
width6, height6, channels6, data6 = load_image("icons/linear_map_icon.png")
width7, height7, channels7, data7 = load_image("icons/powerlaw_icon.png")
width8, height8, channels8, data8 = load_image("icons/histogram_icon.png")
width9, height9, channels9, data9 = load_image("icons/convolution_icon.png")
width10, height10, channels10, data10 = load_image("icons/filter_icon.png")
width11, height11, channels11, data11 = load_image("icons/edge_icon.png")

with texture_registry():
    # adds all the tools to the registry so images can be used
    texture_id1 = add_static_texture(width, height, data)
    texture_id2 = add_static_texture(width2, height2, data2)
    texture_id3 = add_static_texture(width3, height3, data3)
    texture_id4 = add_static_texture(width4, height4, data4)
    texture_id5 = add_static_texture(width5, height5, data5)
    texture_id6 = add_static_texture(width6, height6, data6)
    texture_id7 = add_static_texture(width7, height7, data7)
    texture_id8 = add_static_texture(width8, height8, data8)
    texture_id9 = add_static_texture(width9, height9, data9)
    texture_id10 = add_static_texture(width10, height10, data10)
    texture_id11 = add_static_texture(width11, height11, data11)

# Creates user interface window
with gui.window(label="Welcome to your Digital Image Toolbox!", width=1200, height=1200):
    add_text("1) Please upload an image:", indent=10)
    add_button(label="File Selector", callback=lambda: gui.show_item("file_dialog_id"), indent=10)
    add_spacer(height=20)
    
    add_text("2) Select which tool you would like to use on the image:", indent=10)
    add_spacer(height=5)
    # creates the first row of buttons and calls to the associated function
    with group(horizontal=True): 
        add_image_button(texture_tag=texture_id1, width=40, height=40, callback=crop, indent=20) 
        add_image_button(texture_tag=texture_id2, width=40, height=40, callback=flip, indent=95)
        add_image_button(texture_tag=texture_id3, width=40, height=40, callback=scale, indent=170)
        add_image_button(texture_tag=texture_id4, width=40, height=40, callback=rotate, indent=240)

    # label for buttons in first row
    with group(horizontal=True): 
        add_text("Crop", indent=25)
        add_text("Flip", indent=100)
        add_text("Scale", indent=175)
        add_text("Rotate", indent=245)

    # creates the second row of buttons and calls to the associated function
    add_spacer(height=3)
    with group(horizontal=True):
        add_image_button(texture_tag=texture_id5, width=40, height=40, callback=zero_padding, indent=20)
        add_image_button(texture_tag=texture_id6, width=40, height=40, callback=linear_mapping, indent=95)
        add_image_button(texture_tag=texture_id7, width=40, height=40, callback=powerlaw_mapping, indent=170)
        add_image_button(texture_tag=texture_id8, width=40, height=40, callback=histogram, indent=240)

    # label for buttons in second row
    with group(horizontal=True):
        add_text("Zero \nPadding", indent=25) 
        add_text("Linear \nMapping", indent=95)
        add_text("Power-Law \nMapping", indent=162)
        add_text("Histogram \nEqualization", indent=246)

    # creates the third row of buttons and calls to the associated function
    add_spacer(height=5)
    with group(horizontal=True):
        add_image_button(texture_tag=texture_id9, width=40, height=40, callback=convolution, indent=20)
        add_image_button(texture_tag=texture_id10, width=40, height=40, callback=filtering, indent=95)
        add_image_button(texture_tag=texture_id11, width=40, height=40, callback=edge_detection, indent=170)

    # label for buttons in third row
    with group(horizontal=True):
        add_text("Con-\nvolution", indent=20) 
        add_text("Non-\nLinear \nFiltering", indent=95)
        add_text("Edge \nDetection", indent=170)

    # binds the new text font to the user interface
    gui.bind_font(default_font)

gui.setup_dearpygui()
gui.show_viewport()
gui.start_dearpygui()
gui.destroy_context()
