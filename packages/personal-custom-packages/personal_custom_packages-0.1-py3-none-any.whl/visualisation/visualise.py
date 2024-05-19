from data_extractor import log_function_usage
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pyautogui
import logging
# Everything here is designed based on the subplot2grid approach
'''
    1. x = new gridFigure() -> Create the figure
    2. x.create_subplot(["Create the individual item in the figure using the subplot2grid approach
    3. set_data: Add data to the grid
    4. NOT YET -> Manipulate the individual item settings in the grid (e.g. title)
    5. display() -> display the figure

    1. Each subplot is stored in an array
    2. Subplot is created and ordered from left to right
    3. Accessing the subplot require specifying the position.
'''

matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)

class scatterplot_data_manipulation():
    def __init__(self):
        self.gradient = 'None'
        self.y_intercept = 'None'
        self.floated_x = 'None'
        self.floated_y = 'nothing'
        self.linear_y = 'nothing'
    def set_linear_variables(self,xAxis,yAxis): 
        floated_x = np.array(self.convert_array_value_to_float(xAxis))
        floated_y = np.array(self.convert_array_value_to_float(yAxis))
        self.gradient,self.y_intercept = np.polyfit(floated_x,floated_y,1)  # Find the coefficients of the linear regression
        self.floated_x = floated_x
        self.floated_y = floated_y
    def generate_linear_y_values(self): 
        if self.gradient == 'None' or self.y_intercept == 'None':
            ValueError("Gradient or Y-intercept is empty. Cannot compute....")
        if not isinstance(self.floated_x, np.ndarray):
            ValueError("No array to generate y value array....")
        self.linear_y = self.floated_x * self.gradient + self.y_intercept
    def convert_array_value_to_float(self,arr):
        return [float(item) for item in arr]
    def add_line_to_scatterplot(self,item):
        item.plot(self.floated_x,self.linear_y)

class gridFigure(scatterplot_data_manipulation):
    def __init__(self):
        super()
        screen_width, screen_height = pyautogui.size()
        self.fig = self.create_figure(15,8)
        self.grid = []

    def display(self):
        log_function_usage('display-visualisation-visualise.py')
        plt.show()

    def create_figure(self,width, height):
        log_function_usage('create_figure-visualisation-visualise.py')
        return plt.figure(figsize=(width,height))
    
    def create_subplot(self,arr,dimensions=None):
        log_function_usage('create_subplot-visualisation-visualise.py')
        if dimensions == None:
            ValueError("Dimension parameter for create_subplot should not be empty...")
        if dimensions[0] * dimensions[1] < len(arr):
            ValueError("Size of dimension parameter should not be less than array length")
        row = dimensions[0]
        column = dimensions[1]
        counter = 1
        tracker = []
        for rowIndex in range(row):
            for columnIndex in range(column):
                self.check_subplot_type(arr[counter-1])
                tracker.append((rowIndex,columnIndex))
                self.grid.append({
                    "chart_obj": plt.subplot2grid(dimensions,(rowIndex,columnIndex),rowspan=1,colspan=1),
                    "type": arr[counter-1],
                })  
                counter += 1

    def set_data(self,position,xAxis=None,yAxis=None,data=None,label=None):
        log_function_usage('set_data-visualisation-visualise.py')
        self.check_empty_grid()
        item = self.grid[position]["chart_obj"]
        name = self.grid[position]["type"]
        self.set_subplot_type(item, name, xAxis=xAxis, yAxis=yAxis,data=data,label=label)

    def set_subplot_type(self,item,name,xAxis=None,yAxis=None,data=None,label=None):
        log_function_usage('set_subplot_type-visualisation-visualise.py')
        if name == 'pie':
            if data == None or label == None:
                ValueError("Either data parameter or label parameter is empty...")
            item.pie(data,labels=label,autopct='%1.1f%%')
        elif name == 'bar':
            if data == None or label == None:
                ValueError("Either data parameter or label parameter is empty...")
            item.bar(label,data)
        elif name == 'barh':
            if data == None or label == None:
                ValueError("Either data parameter or label parameter is empty...")
            item.barh(label,data)
        elif name == 'line':
            if xAxis == None or yAxis == None:
                ValueError("Either xAxis parameter or yAxis parameter is empty...")
            if label == None:
                item.plot(xAxis,yAxis)
            else:
                print("HELLO: ",label)
                item.plot(xAxis,yAxis,label=label) 
                item.legend()
        elif name == 'scatter':
            if xAxis == None or yAxis == None:
                ValueError("Either xAxis parameter or yAxis parameter is empty...")
            item.scatter(xAxis,yAxis)
        else:
            TypeError(f"Unknown chart type {name}...")

    def add_stuff(self,position,feature_adding,xAxis=None,yAxis=None):
        item_type = self.grid[position]["type"]
        item = self.grid[position]["chart_obj"]
        if item_type == "scatter":
            if feature_adding == "line":
                if xAxis == None or yAxis == None:
                    ValueError("Either xAxis parameter or yAxis parameter or is empty...")
                self.set_linear_variables(xAxis,yAxis)
                self.generate_linear_y_values()
                self.add_line_to_scatterplot(item)
        

    def check_empty_grid(self):
        log_function_usage('check_empty_grid-visualisation-visualise.py')
        if len(self.grid) == 0:
            ValueError("Grid is empty...")

    def set_legend(self,position):
        item = self.grid[position]["chart_obj"]
        item.legend()

    def check_subplot_type(self, name):
        log_function_usage('check_subplot_type-visualisation-visualise.py')
        if name == 'pie' or name == 'bar' or name == 'barh' or name == 'line' or name == 'multi_line' or name == 'scatter':
            return True
        else:
            ValueError(f"No such subplot type: {name}")


    # def sizing():
        

