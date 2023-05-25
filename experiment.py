for i in range(23): print(f"cnvrg_linechart_LossLog value: '{round((1 / (i + 1) ** 2), 6)}'")
# for i in range(23): print ("cnvrg_linechart_LossLog value: '%.6f'"%(1/(i+1)**2))
print("===")
print("===")
print("===")

for i in range(50): print(f"cnvrg_linechart_AccuracyLog value: '{round((i ** 2 * 0.000001), 6)}'")
for i in range(100): print(f"cnvrg_linechart_Event group: 'ts' value: '{round((i ** 2 * 0.000004), 6)}'")
for i in range(120): print(f"cnvrg_linechart_Event group: 'epochs' value: '{round((i ** 2 * 0.000005), 6)}'")

print("cnvrg_tag_Accuracy: 0.9766")
print("cnvrg_tag_Algorithm: NeuralNetworks")
print("cnvrg_tag_Architecture: RNN (LSTM)")
print("cnvrg_tag_FeaturesDim:200")
print("cnvrg_tag_BatchSize:32")
print("cnvrg_tag_epochs:10")
print("cnvrg_tag_WordEmbedding:FastText")

print("============================")
print("Loading model")

keras_lines = ["Train on 2394 samples, validate on 1027 samples", "Epoch 1/10",
               "2394/2394 [==============================] - 0s - loss: 0.6898 - acc: 0.5455 - val_loss: 0.6835 - val_acc: 0.5716",
               "Epoch 2/10",
               "2394/2394 [==============================] - 0s - loss: 0.6879 - acc: 0.5522 - val_loss: 0.6901 - val_acc: 0.5522",
               "Epoch 3/10",
               "2394/2394 [==============================] - 0s - loss: 0.5555 - acc: 0.6000 - val_loss: 0.6000 - val_acc: 0.6000",
               "Epoch 4/10",
               "2394/2394 [==============================] - 0s - loss: 0.5444 - acc: 0.6777 - val_loss: 0.5800 - val_acc: 0.6777",
               "Epoch 5/10",
               "2394/2394 [==============================] - 0s - loss: 0.4555 - acc: 0.7777 - val_loss: 0.5444 - val_acc: 0.7777",
               "Epoch 6/10",
               "2394/2394 [==============================] - 0s - loss: 0.4220 - acc: 0.8000 - val_loss: 0.5222 - val_acc: 0.8000",
               "Epoch 7/10",
               "2394/2394 [==============================] - 0s - loss: 0.4000 - acc: 0.8200 - val_loss: 0.4344 - val_acc: 0.8200",
               "Epoch 8/10",
               "2394/2394 [==============================] - 0s - loss: 0.3600 - acc: 0.8100 - val_loss: 0.3333 - val_acc: 0.8100",
               "Epoch 9/10",
               "2394/2394 [==============================] - 0s - loss: 0.3685 - acc: 0.9000 - val_loss: 0.2323 - val_acc: 0.9000",
               "Epoch 10/10",
               "2394/2394 [==============================] - 0s - loss: 0.357 - acc: 0.9700 - val_loss: 0.1414 - val_acc: 0.9700",
               "1027/1027 [==============================] - 0s"]

for l in keras_lines:
    print(l)
import os

os.system('cp ../image1.png .')

from cnvrg import Experiment
import time

e = Experiment()
# log metric: single line
e.log_metric("single_log_metric", Ys=[0.1, 0.2, 0.5], Xs=[10, 20, 50])
# log metric: multiple line
e.log_metric("multi_log_metric",
             Ys=[0.1, 0.2, 0.5],
             Xs=[10, 10, 10],
             grouping=["loss", "val_loss", "acc"])
time.sleep(1)
e.log_metric("multi_log_metric",
             Ys=[0.4, 0.2, 0.3],
             Xs=[20, 20, 20],
             grouping=["loss", "val_loss", "acc"])
time.sleep(1)
e.log_metric("multi_log_metric",
             Ys=[0.8, 0.2, 0.1],
             Xs=[50, 50, 70],
             grouping=["loss", "val_loss", "acc"])

from cnvrg.charts import Bar

# bar chart: single
x_value = ["loss", "val_loss", 2010, 2020]
y_value = [0.2, 0.4, 0.8, 2]
e.log_chart("single_bar_chart", title="single_bar_chart",
            data=Bar(x=x_value, y=y_value, name="y_value"))

# bar chart: multi
x_value = ["loss", "val_loss", 2010, 2020]
y_value1 = [0.2, 0.4, 0.8, 2]
y_value2 = [0.4, 0.8, 1, 3]
e.log_chart("multi_bar_chart", title="multi_bar_chart",
            data=[Bar(x=x_value, y=y_value1, name="y_value1"),
                  Bar(x=x_value, y=y_value2, name="y_value2", )])

from cnvrg.charts import MatrixHeatmap

# heat map/confusion matrix
e.log_chart("confusion_matrix", title="Heatmap", x_ticks=['x', 'y'], y_ticks=['a', 'b'],
            data=MatrixHeatmap(matrix=[(0, 6), (2, 4)],
                               color_stops=[[0, '#011580'], [1, '#7EB4EB'], [5, '#000000']],
                               ))

# single scatter plot
from cnvrg.charts import Scatterplot

x_values = [10, 20, 30, 40, 60]
y_values = [15, 10, 5, 2, 1]
e.log_chart("single_scatter_plot", title="single_scatter_plot",
            data=Scatterplot(x=x_values, y=y_values, name="scatter_plot_graph"))

# multi scatter plot
x1_values = [10, 20, 30, 40, 60]
x2_values = [10, 20, 30, 40, 70]
y1_values = [15, 10, 5, 2, 1]
y2_values = [1, 2, 5, 10, 50]
e.log_chart("multi_scatter_plot", title="multi_scatter_plot",
            data=[Scatterplot(x=x1_values, y=y1_values, name="scatter_plot1"),
                  Scatterplot(x=x2_values, y=y2_values, name="scatter_plot2")])
