import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from matplotlib.ticker import FuncFormatter


dark_greys =  ["#333333", "#666666", "#999999", "#cccccc", "#e6e6e6"]

def get_linreg_stats(data, cols):
    slope, intercept, r_value, p_value, std_err = stats.linregress(data[cols[0]], data[cols[1]])
    return r_value, p_value,

def bottom_annotate_plot(ax, r_value, p_value, align=['bottom', 'right'], font=16):
    if p_value < 0.001:
        plt.text(0.5, 0.02, f"R\u00B2 = {r_value**2:.2f}, p < 0.001",
                 transform=ax.transAxes, fontsize=font,
                 verticalalignment=align[0], horizontalalignment=align[1])
    else:
        plt.text(0.5, 0.02, f"R\u00B2 = {r_value**2:.2f}, p = {p_value:.3f}",
                 transform=ax.transAxes, fontsize=font,
                 verticalalignment=align[0], horizontalalignment=align[1])
        
def top_annotate_plot(ax, r_value, p_value, align=['top', 'right'], font=16):
    if p_value < 0.001:
        plt.text(0.5, 0.95, f"R\u00B2 = {r_value**2:.2f}, p < 0.001",
                 transform=ax.transAxes, fontsize=font,
                 verticalalignment=align[0], horizontalalignment=align[1])
    else:
        plt.text(0.5, 0.95, f"R\u00B2 = {r_value**2:.2f}, p = {p_value:.3f}",
                 transform=ax.transAxes, fontsize=font,
                 verticalalignment=align[0], horizontalalignment=align[1])

# @overwrite_args
def plot_yearly_sum_trend(yearly_sum, title:str, y='crime_count', save_png=False, category='total', dataset='AllCrime', color='k', align=['top', 'right']):
    font = 16
    plt.figure(figsize=(6,4))
    # overlay a trendline
    sns.regplot(x='year', y=y, data=yearly_sum,color=color, scatter=True)

    # Set the plot title and labels
    plt.xlabel('Year', fontsize=font)
    plt.ylabel('Monthly Crime Count', fontsize=font)
    plt.title(title, fontsize=font)

    # Rotate x-axis labels for better readability
    x_ticks = yearly_sum['year'].unique()
    plt.xticks(ticks=x_ticks, labels=[str(int(year)) for year in x_ticks], fontsize=font)
    plt.yticks(fontsize=font)

    # Annotate each subplot with yearly average
    r_value, p_value = get_linreg_stats(yearly_sum, ['year', y])
    if align[0] == 'top':
       top_annotate_plot(plt.gca(), r_value, p_value, align=align)
    else:
       bottom_annotate_plot(plt.gca(), r_value, p_value, align=align)

    # Save the modified plot
    plt.tight_layout()
    if save_png:
        plt.savefig(f'../reports/figures/{dataset}_yearly_crime_{category}.png', dpi=300)

    # Show the plot
    plt.show()


def thousands_formatter(x, pos):
    return f'{int(x/1000)}K'

def millions_formatter(x, pos):
    return f'{int(x/1000000)}M'


def plot_seasonal_and_total_trends(data, yearly_sum,  title: str, y='crime_count', dataset='AllCrime',  palette=dark_greys, save_png=False, population='ALL', fig_dime=(8, 5)):
    seasonal_trends = data.groupby(['year', 'season'])[y].sum().reset_index()

    # Seasonal Trends Analysis
    fig_dime = fig_dime
    font=16

    # Plotting
    fig, ax1 = plt.subplots(figsize=fig_dime)
    sns.lineplot(ax=ax1, data=seasonal_trends, x='year', y=y, hue='season', estimator='sum', palette=palette, markers=True, linewidth=3, markersize=10, style='season')
    if 2010 in data['year'].unique():
        plt.xticks(fontsize=font, rotation=45)
    ax1.set_ylabel('Seasonal Counts', fontsize=font)
    ax1.set_xlabel('Year', fontsize=font)
    ax1.set_title(title, fontsize=font)

    # Create a second y-axis
    ax2 = ax1.twinx()
    sns.lineplot(ax=ax2, data=yearly_sum, x='year', y=y, markers=True, color='red', label='Total', )
    ax2.legend('')
    ax2.set_ylabel('Total Yearly Reports Count', color='red', fontsize=font)

    # Ensure x-axis ticks are integers
    x_ticks = yearly_sum['year'].unique()
    plt.xticks(ticks=x_ticks, labels=[str(int(year)) for year in x_ticks], fontsize=font)

    # only if yticks > 1000:
    if yearly_sum[y].max() > 1000000:
        ax1.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
        ax1.tick_params(axis='both', which='major', labelsize=font)
        ax2.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
        ax2.tick_params(axis='both', which='major', labelsize=font)
    elif yearly_sum[y].max() > 10000:
        ax1.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
        ax1.tick_params(axis='both', which='major', labelsize=font)
        ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
        ax2.tick_params(axis='both', which='major', labelsize=font)
    else:
        ax1.tick_params(axis='both', which='major', labelsize=font)
        ax2.tick_params(axis='both', which='major', labelsize=font)
    # Add a legend and move it under ax1 legend
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend = ax1.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True, ncol=5, fontsize='large')
    # Save the modified plot
    plt.tight_layout()
    if save_png:
        plt.savefig(f'../reports/figures/{dataset}_seasonal_and_total_{population}.png', dpi=300)

    # Show the plot
    plt.show()
    # return f"plot_seasonal_and_total_trends - y: {y}, data: {dataset}"