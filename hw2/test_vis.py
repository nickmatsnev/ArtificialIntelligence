# importing the required module
import matplotlib.pyplot as plt

# x axis values
x = [1, 2, 3]
# corresponding y axis values
y = [2, 4, 1]

names = ["moscow", "prague", "warsaw"]
# plotting the points
plt.plot(x, y, label=names, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12)

for i in range(0, len(x)):
    plt.text(x[i] + 0.07, y[i], names[i])
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('Map!')

# function to show the plot
plt.show()