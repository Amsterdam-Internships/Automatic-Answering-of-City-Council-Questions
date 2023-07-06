import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import math
from matplotlib import colors as mcolors

def plot_distribution(data, x_label, y_label, title, figsize=(10, 6), show_outliers=True):
    """
    Plot a boxplot and histogram for the given data.
    
    Parameters:
    - data: List or array-like object containing the data to plot.
    - x_label: Label for the x-axis.
    - y_label: Label for the y-axis.
    - title: Title of the plot.
    - figsize: Tuple specifying the figure size (default: (10, 6)).
    - show_outliers: Boolean indicating whether to show outliers (default: True).
    """
    # Create a figure with two subplots
    fig, (ax_boxplot, ax_histogram) = plt.subplots(1, 2, figsize=figsize)

    # Customize boxplot style
    boxplot_props = dict(
        notch=True,
        patch_artist=True,
        capprops=dict(color='black'),
        whiskerprops=dict(color='black'),
        flierprops=dict(marker='o', markerfacecolor='red', markersize=5, linestyle='none'),
        medianprops=dict(color='blue', linewidth=2)
    )

    # Plot the boxplot
    ax_boxplot.boxplot(data, vert=False, showfliers=show_outliers, boxprops=dict(facecolor='lightblue'), **boxplot_props)
    ax_boxplot.set_xlabel(x_label)
    ax_boxplot.set_ylabel(y_label)
    ax_boxplot.set_title(f'Boxplot - {title}')
    ax_boxplot.spines['top'].set_visible(False)
    ax_boxplot.spines['right'].set_visible(False)

    # Plot the histogram
    ax_histogram.hist(data, bins='auto', edgecolor='black')
    ax_histogram.set_xlabel(x_label)
    ax_histogram.set_ylabel('Frequency')
    ax_histogram.set_title(f'Histogram - {title}')
    ax_histogram.spines['top'].set_visible(False)
    ax_histogram.spines['right'].set_visible(False)

    # Adjust the spacing between subplots
    plt.subplots_adjust(wspace=0.3)

    # Show the plot
    plt.show()



def plot_most_common(data, label, top_n=10):
    """
    Plot the most common items from the given data.
    
    Parameters:
    - data: List or iterable containing the data to plot.
    - label: Label for the data being plotted.
    - top_n: Number of top items to display (default: 10).
    """
    counter = Counter(data)
    most_common_items = counter.most_common(top_n)

    # Extract the item names and their frequencies
    items, frequencies = zip(*most_common_items)

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(items, frequencies)

    # Customize labels and title
    plt.xlabel(label)
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Common {label}s')

    # Rotate x-axis labels if needed
    plt.xticks(rotation=45)

    # Show the plot
    plt.show()


def plot_wordcloud_grid(lda_model, num_topics, num_words, ncols, width=4, height=4):
    """
    Create a grid of word clouds for multiple topics from an LDA model.
    
    Parameters:
    - lda_model: Trained LDA model.
    - num_topics: Number of topics to display.
    - num_words: Number of top words to include in each topic's word cloud.
    - ncols: Number of columns in the grid.
    - width: Width of each word cloud plot (default: 4).
    - height: Height of each word cloud plot (default: 4).
    """
    nb_rows = math.ceil(num_topics / ncols)
    
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()] 
    cols = cols * math.ceil(num_topics / len(cols))

    cloud = WordCloud(background_color='white',
                      width=400,
                      height=400,
                      max_words=num_words,
                      color_func=lambda *args, **kwargs: cols[i],
                      prefer_horizontal=1.0)

    topics = lda_model.show_topics(num_topics=num_topics, num_words=num_words, formatted=False)

    fig, axes = plt.subplots(ncols=ncols, nrows=nb_rows, 
                             figsize=(width*ncols, height*nb_rows), 
                             sharex=True, sharey=True)

    for i, (topic, ax) in enumerate(zip(topics, axes.flatten())):
        topic_words = dict(topic[1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        ax.imshow(cloud)
        ax.set_title('Topic ' + str(i), fontdict=dict(size=16))
        ax.axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    plt.show()
