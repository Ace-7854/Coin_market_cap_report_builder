import matplotlib.pyplot as plt
import pandas as pd

class DataDisplay:
    def bar_chart(data:list, labels:list, title:str, filename:str):
        """Makes a bar chart"""
        plt.figure(figsize=(8, 6))
        plt.bar(labels, data, color='skyblue')
        plt.xlabel("Coin")
        plt.ylabel("Amount")
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
        table.set_fontsize(8)
        table.auto_set_column_width([0, 1, 2])
        plt.savefig(filename)
        plt.close()
    
    def make_figures(labels, data, figure_paths, titles, axis_labels, table_data=None):
        """Creates one of every figure, figure list in order: barchart, linechart, piechart, table"""
        if len(figure_paths) != 4 or len(titles) != 4:
            raise "4 items for figure_path AND title_figures is required for this method, in order barchart, linechart, piechart, table"
        else:
            DataDisplay.bar_chart(data, labels, titles[0], figure_paths[0])
            DataDisplay.line_chart(data, labels, titles[1], figure_paths[1], axis_labels)
            DataDisplay.pie_chart(data, labels, titles[2], figure_paths[2])
            if table_data:
                DataDisplay.table_display(table_data, ["Rank", "Name", "Price ($)", "Circulating Supply", "Abbreviation"], figure_paths[3])

            



