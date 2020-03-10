#!/usr/bin/env python3

# block class to make a single figure panel.
# with some defaults, rather than having to work directly
# with grid and lots of labeling
# Seaborn is not yet really great for this
# particularly when wanting to combine multiple types of plots

import sys, string, re, subprocess
import os.path
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import rcParams
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from matplotlib import cm


class MultiPanel:


    # make a multipanel figure
    def __init__(
            self
            ,panel_widths
            ,panel_heights
            ,filename
            ,width=5
            ,height=5
            ,wspace=0.2
            ,hspace=0.2
            ,pad_inches=0.5
            ):

        # initialize the fig
        self.fig = plt.figure(figsize=(width, height))

        self.rows = len(panel_heights)
        self.cols = len(panel_widths)

        # initialize a gridspec object
        self.gs = gridspec.GridSpec(
                nrows=self.rows
                ,ncols=self.cols
                ,width_ratios=panel_widths 
                ,height_ratios=panel_heights
                ,wspace=wspace
                ,hspace=hspace
                )

        self.filename = filename

        # figure out what file type we want
        file_plus_extension = os.path.splitext(filename)

        if len(file_plus_extension) < 2:
            self.filename += ".pdf"
            self.filetype = "pdf"
        else:
            self.filetype = re.sub(r"^\.","",file_plus_extension[1])

        self.pad_inches = pad_inches

        # counter remembering how many blocks 
        # were already printed
        self.block_counter = 0

    # a single graph panel
    def start_block(self
            ,row
            ,col
            ,projection=None):

        # initialize figure in grid
        ax = plt.subplot(self.gs[row,col], projection=projection)

        return(ax)

    def end_block(
            self
            ,ax
            ,xlabel=None
            ,ylabel=None
            ,xticks=False
            ,yticks=False
            ,title=""
            ,xlim=None
            ,ylim=[0.0,1.0]
            ,loc_title=False
            ,loc_title_pos=[0.05,1.05]
            ,x_axis_diff=0.15
            ,legend=False
            ,x_ticks_minor=5
            ,y_ticks_minor=5
            ,x_ticks_major_multiple=0.2
            ,y_ticks_major_multiple=0.2
            ):

        # do the other axis stuff
        ax.set_ylim(ylim)

        if xlim is not None:
            ax.set_xlim(xlim)


        ax.xaxis.set_major_locator(MultipleLocator(x_ticks_major_multiple))
        ax.yaxis.set_major_locator(MultipleLocator(y_ticks_major_multiple))
        ax.xaxis.set_minor_locator(AutoMinorLocator(x_ticks_minor))
        ax.yaxis.set_minor_locator(AutoMinorLocator(y_ticks_minor))

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")
        

        if type(ylabel) == type("sample_string"):
            ax.set_ylabel(ylabel=ylabel)

        if type(xlabel) == type("sample_string"):
            ax.set_xlabel(xlabel=xlabel)
        
        if xticks is False:
            ax.set_xticklabels([])

        if yticks is False:
            ax.set_yticklabels([])

        if title: 
            ax.set_title(
                    label=title
                    ,position=(0.5,1.05))

        # set the indication label
        if loc_title:
            ax.set_title(
                    label=string.ascii_uppercase[self.block_counter]
                    ,loc="left"
                    ,position=loc_title_pos)

        if legend:
            ax.legend()

        self.block_counter += 1

    def close(self
            ,extra_artists=None
            ,tight=False):

        bbox_inches=None

        if tight != False:
            bbox_inches="tight"
        
        if self.filetype == "svg":
            filename_pdf = os.path.splitext(self.filename)[0] + ".pdf"

            plt.savefig(filename_pdf
                    ,bbox_inches=bbox_inches
                    ,pad_inches=self.pad_inches
                    ,bbox_extra_artists=extra_artists)

            filename_svg = os.path.splitext(self.filename)[0] + ".svg"
            subprocess.call(["pdf2svg",filename_pdf, filename_svg])

        else:

            plt.savefig(self.filename
                    ,bbox_inches=bbox_inches
                    ,pad_inches=self.pad_inches
                    ,bbox_extra_artists=extra_artists)

        plt.close('all')



