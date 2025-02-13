
import mplfinance as mpf
import pandas as pd
import numpy

import statsmodels.api as sm
import matplotlib.pyplot as plt

def plot_candlestick(df, path):
    # configure mpf to return fig and axes
    fig, axes = mpf.plot(df,
            type='candle',
            #  style='yahoo',
            volume=True,
            returnfig=True,
            tight_layout=True,
            mav=(3, 10, 15),
            style='yahoo',
            )

    axes[0].yaxis.set_label_position("left")
    axes[0].yaxis.tick_left()

    # For the volume panel: set the y-axis label and ticks to the left
    # Note: if volume is True and no additional panels are specified,
    # mplfinance usually returns two axes: axes[0] for the main panel and axes[1] for volume.
    axes[1].yaxis.set_label_position("left")
    axes[1].yaxis.tick_left()

    axes[2].yaxis.set_label_position("left")
    axes[2].yaxis.tick_left()

    # Optionally, you can set your own labels:
    axes[0].set_ylabel("Price")
    axes[1].set_ylabel("Volume")
    axes[2].set_ylabel("Volume")

    # add $ on price axis
    axes[0].yaxis.set_major_formatter('${x:,.0f}')

    # Display the figure
    # fig.show()
    # Save the figure to a file
    fig.savefig(path)

    plt.close(fig)

def plot_decomposition(prix_cloture, path):
    decomposition = sm.tsa.seasonal_decompose(prix_cloture, model='additive', period=24)
    fig = decomposition.plot()
    
    # plt.show()
    # plt save fig 
    fig.savefig(path)