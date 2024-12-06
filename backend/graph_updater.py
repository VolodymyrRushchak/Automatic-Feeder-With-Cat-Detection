import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def update_graph(dataframe: pd.DataFrame):
    plt.clf()
    plt.title('Cat history')
    plt.xticks(fontsize=8, rotation=30, ha='right')
    plt.xlabel('Time')
    frmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(frmt)
    plt.ylabel('Cat on camera')
    plt.plot(dataframe.time_point, dataframe.cat_present)
    plt.savefig('static/graph.jpg')
