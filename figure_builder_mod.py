import matplotlib.pyplot as plt
import pandas as pd

class DataDisplay:
    def bar_chart(data:str, labels:list, title:str, filename:str):
        """Makes a bar chart"""
        plt.figure(figsize=(8, 6))
        plt.bar(labels, data, color='skyblue')
        plt.xlabel("Categories")
        plt.ylabel("Values")
        plt.title(title)
        plt.savefig(filename)
        plt.close()
    
    def line_chart(data:list, labels:list, title:str, filename:str, axis_labels:list):
        """makes a line chart"""
        if len(axis_labels) == 2:
            plt.figure(figsize=(8, 6))
            plt.plot(labels, data, marker='o', linestyle='-', color='red')
            plt.xlabel(axis_labels[0])
            plt.ylabel(axis_labels[1])
            plt.title(title)
            plt.grid()
            plt.savefig(filename)
            plt.close()
        else:
            raise "Only 2 items in axis_label allowed"
    
    def pie_chart(data:list, labels:list, title:str, filename:str):
        """Creates a pie chart"""
        plt.figure(figsize=(8, 6))
        plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140, colors=['blue', 'red', 'green', 'orange'])
        plt.title(title)
        plt.savefig(filename)
        plt.close()
    
    def table_display(data:list, columns:list, filename:str):
        """Creates a table"""
        df = pd.DataFrame(data, columns=columns)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width([0, 1, 2])
        plt.savefig(filename)
        plt.close()
    
    def make_figures(labels:list, data:list, figure_path:list, title_figures:list, axis_label:list):
        """Creates one of every figure, figure list in order: barchart, linechart, piechart, table"""
        if len(figure_path) != 4 or len(title_figures) != 4:
            raise "4 items for figure_path AND title_figures is required for this method, in order barchart, linechart, piechart, table"
        else:
            DataDisplay.bar_chart(data, labels, title_figures[0], figure_path[0])
            DataDisplay.line_chart(data, labels, title_figures[1], figure_path[1], axis_label)
            DataDisplay.pie_chart(data, labels, title_figures[2], figure_path[2])
            DataDisplay.table_display([["Sunday", 2, 456, 22], ["Monday", 5, 6,20], ["Tuesday", 8, 9,10]], ["Day", "Number of deaths", "Number of Craniums", "Number of pies"], figure_path[3])


