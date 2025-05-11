import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

def make_line(data, width, height):
    fig, ax = plt.subplots(figsize=(width, height))
    x = np.arange(len(data))
    ax.plot(x, data)
    return fig

def make_bar(data, width, height):
    fig, ax = plt.subplots(figsize=(width, height))
    x = np.arange(len(data))
    ax.bar(x, data)
    return fig

def make_scatter(data, width, height):
    fig, ax = plt.subplots(figsize=(width, height))
    x = np.arange(len(data))
    ax.scatter(x, data)
    return fig

def make_hist(data, width, height, bins=10):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.hist(data, bins=bins)
    return fig

def make_pie(data, width, height):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.pie(data)
    return fig