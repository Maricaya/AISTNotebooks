import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy import stats
import cartopy.crs as ccrs
import pyhdf.SD as H
import math

# Read HDF4 file to a dictionary
def read_sds(filename):
    out = {}
    a = H.SD(filename)
    dic = a.datasets()
    keys = dic.keys()
    for n in keys:
        sd = a.select(n)
        d = sd.get()
        out[n] = d
    return out

# Assign histogram bin edge values for each column name in a pandas dataframe
def bins_dfs(df1):
    keys = list(df1)
    dict_bins = {}
    dict_log = {}
    for i in range(len(keys)):
        min = df1[keys[i]].values.min()
        max = df1[keys[i]].values.max()
        nbins = 30
        if min <= 0.0:
            if keys[i] in ["LON", "R_LON", "LAT", "R_LAT", "R_ORIENTATION"]:
                min1 = math.floor(min)
                max1 = math.ceil(max)
                nbins = int((max1 - min1) / 2.0) + 1
                bins = np.linspace(min1, max1, nbins)
                dict_bins[keys[i]] = bins
                dict_log[keys[i]] = False
            elif keys[i] in ["RAINGRID_5", "VOLRAINGRID_5", "RAINAREA_5", "VOLRAIN_5"]:
                min1 = 0.0
                max1 = math.ceil(math.log10(max))
                bins = np.logspace(min1, max1, nbins)
                dict_bins[keys[i]] = bins
                dict_log[keys[i]] = True
            else:
                bins = np.linspace(min, max, nbins)
                dict_bins[keys[i]] = bins
                dict_log[keys[i]] = False
        elif keys[i] in ["YEAR", "MONTH", "DAY", "HOUR"]:
            bins = np.linspace(min, max, nbins)
            dict_bins[keys[i]] = bins
            dict_log[keys[i]] = False
        elif keys[i] in ["R_MINOR", "R_MAJOR"]:
            bins = np.logspace(1., 4., nbins)
            dict_bins[keys[i]] = bins
            dict_log[keys[i]] = True
        else:
            min1 = math.floor(math.log10(min))
            max1 = math.ceil(math.log10(max))
            bins = np.logspace(min1, max1, nbins)
            dict_bins[keys[i]] = bins
            dict_log[keys[i]] = True
    return dict_bins, dict_log

# 1D histogram comparisons and plots
def hist1d_dfs(df1, df2, df1_name, df2_name, dict_bins, dict_log, arg_list, output_dir):
    n = 0
    for x in arg_list:
        var1 = df1[x].to_numpy()
        var2 = df2[x].to_numpy()
        xlog = dict_log[x]
        xbin = dict_bins[x]

        i = n % 4
        if i == 0:
            fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

        ax = axes.flatten()[i]
        ax.hist((var1, var2), bins=xbin, log=xlog, alpha=0.5, color=('red', 'blue'),
                label=(df1_name, df2_name))
        ax.legend(prop={'size': 10})
        if xlog:
            ax.set_xscale('log')
        ax.set_title(x)
        ax.set_xlabel(x)
        ax.set_ylabel("PF Counts")

        if i == 3 or n == len(arg_list) - 1:
            title = f"Comparison of {df1_name} and {df2_name} Population (counts)"
            fig.suptitle(title)
            fig.tight_layout()
            plt.savefig(f"{output_dir}/comparison_1d_{n // 4}.png")
            plt.close(fig)
        n += 1
    return

# 2D histogram comparisons and plots
def hist2d_dfs(df1, df2, df1_name, df2_name, dict_bins, dict_log, arg_list, output_dir):
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    n = 0
    for x in arg_list:
        xname, yname = x
        xvar1 = df1[xname].to_numpy()
        xvar2 = df2[xname].to_numpy()
        yvar1 = df1[yname].to_numpy()
        yvar2 = df2[yname].to_numpy()
        xlog = dict_log[xname]
        xbin = dict_bins[xname]
        ylog = dict_log[yname]
        ybin = dict_bins[yname]

        i = n % 2
        if i == 0:
            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 12))
        ax = axes.flatten()[i]
        hist1, xedges, yedges, im = ax.hist2d(xvar1, yvar1, bins=[xbin, ybin], density=True, alpha=1.0,
                                              norm=colors.LogNorm(), cmap="hot")
        if xlog:
            ax.set_xscale('log')
        if ylog:
            ax.set_yscale('log')
        ax.set_title(df1_name + " NORMALIZED 2D HISTOGRAM")
        ax.set_xlabel(xname)
        ax.set_ylabel(yname)
        im.set_clim(1.0e-3, 1.e-12)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')

        ax = axes.flatten()[i + 2]
        hist2, xedges, yedges, im = ax.hist2d(xvar2, yvar2, bins=[xbin, ybin], density=True, alpha=1.0,
                                              norm=colors.LogNorm(), cmap="hot")
        if xlog:
            ax.set_xscale('log')
        if ylog:
            ax.set_yscale('log')
        ax.set_title(df2_name + " NORMALIZED 2D HISTOGRAM")
        ax.set_xlabel(xname)
        ax.set_ylabel(yname)
        im.set_clim(1.0e-3, 1.e-12)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical')

        ax = axes.flatten()[i + 4]
        diff = (hist2 - hist1).T
        cntr = ax.contourf(xedges[0:-1], yedges[0:-1], diff, levels=14, cmap="RdBu_r")
        fig.colorbar(cntr, ax=ax)
        if xlog:
            ax.set_xscale('log')
        if ylog:
            ax.set_yscale('log')
        ax.set_title(df2_name + " - " + df1_name)
        ax.set_xlabel(xname)
        ax.set_ylabel(yname)

        if i == 1 or n == len(arg_list) - 1:
            title = f"Comparison of {df1_name} and {df2_name} 2D Histogram"
            fig.suptitle(title)
            fig.tight_layout()
            plt.savefig(f"{output_dir}/comparison_2d_{n // 2}.png")
            plt.close(fig)
        n += 1
    return

# Local contribution histogram comparisons and plots
def loc_contri_dfs(df1, df2, df1_name, df2_name, dict_bins, dict_log, arg_list, output_dir):
    lonbins = np.linspace(-180., 180.0, 181)
    latbins = np.linspace(-90., 90.0, 91)
    n = 0
    for x in arg_list:
        zname, varname, operator, threshold = x
        xcoord1 = df1["LON"].to_numpy()
        xcoord2 = df2["LON"].to_numpy()
        ycoord1 = df1["LAT"].to_numpy()
        ycoord2 = df2["LAT"].to_numpy()
        zcoord1 = df1[zname].to_numpy()
        zcoord2 = df2[zname].to_numpy()
        var1 = df1[varname].to_numpy()
        var2 = df2[varname].to_numpy()
        arrs1 = [xcoord1, ycoord1, zcoord1]
        arrs2 = [xcoord2, ycoord2, zcoord2]
        zbins = dict_bins[zname]
        if operator == ">":
            idxs = np.where(zbins[0:-1] > threshold)
            n1 = idxs[0][0]
            n2 = idxs[0][-1] + 1
        else:
            idxs = np.where(zbins < threshold)
            n1 = idxs[0][0]
            n2 = idxs[0][-1] + 1

        stat_bin1, edges, binnumber = stats.binned_statistic_dd(arrs1, var1, 'sum', bins=[lonbins, latbins, zbins])
        stat_bin2, edges, binnumber = stats.binned_statistic_dd(arrs2, var2, 'sum', bins=[lonbins, latbins, zbins])

        # compute local contribution percentages
        tmp1 = 100.0 * np.sum(stat_bin1[:, :, n1:n2], axis=2) / np.sum(stat_bin1, axis=2)
        tmp2 = 100.0 * np.sum(stat_bin2[:, :, n1:n2], axis=2) / np.sum(stat_bin2, axis=2)
        loc_cont1 = tmp1.transpose()
        loc_cont2 = tmp2.transpose()
        levels = np.linspace(0., 100., 21)
        cmap = 'jet'

        i = n % 2
        if i == 0:
            fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree()})
            ax = axes.flatten()[i]
            ax.set_title(df1_name + " Local Contribution " + zname + " " + operator + " " + str(threshold))
            cf = ax.contourf(lonbins[0:-1], latbins[0:-1], loc_cont1, levels=levels,
                             transform=ccrs.PlateCarree(), cmap=cmap, extend="both")
            ax.coastlines()
            g = ax.gridlines(draw_labels=True)
            g.top_labels = False
            g.right_labels = False
            fig.colorbar(cf, ax=ax, location='right', shrink=0.7)

            ax = axes.flatten()[i + 2]
            ax.set_title(df2_name + " Local Contribution " + zname + " " + operator + " " + str(threshold))
            cf = ax.contourf(lonbins[0:-1], latbins[0:-1], loc_cont2, levels=levels,
                             transform=ccrs.PlateCarree(), cmap=cmap, extend="both")
            ax.coastlines()
            g = ax.gridlines(draw_labels=True)
            g.top_labels = False
            g.right_labels = False
            fig.colorbar(cf, ax=ax, location='right', shrink=0.7)

            ax = axes.flatten()[i + 4]
            diff = loc_cont2 - loc_cont1
            levels = np.linspace(-60, 60, 21)
            ax.set_title(df2_name + "-" + df1_name + " Local Contribution " + zname + " " + operator + " " + str(threshold))
            cf = ax.contourf(lonbins[0:-1], latbins[0:-1], diff, levels=levels,
                             transform=ccrs.PlateCarree(), cmap=cmap, extend="both")
            ax.coastlines()
            g = ax.gridlines(draw_labels=True)
            g.top_labels = False
            g.right_labels = False
            fig.colorbar(cf, ax=ax, location='right', shrink=0.7)
        else:
            ax = axes.flatten()[i]
            ax.set_title(df1_name + " Local Contribution " + zname + " " + operator + " " + str(threshold))
            cf = ax.contourf(lonbins[0:-1], latbins[0:-1], loc_cont1, levels=levels,
                             transform=ccrs.PlateCarree(), cmap=cmap, extend="both")
            ax.coastlines()
            g = ax.gridlines(draw_labels=True)
            g.top_labels = False
            g.right_labels = False
            fig.colorbar(cf, ax=ax, location='right', shrink=0.7)

            ax = axes.flatten()[i + 2]
            ax.set_title(df2_name + " Local Contribution " + zname + " " + operator + " " + str(threshold))
            cf = ax.contourf(lonbins[0:-1], latbins[0:-1], loc_cont2, levels=levels,
                             transform=ccrs.PlateCarree(), cmap=cmap, extend="both")
            ax.coastlines()
            g = ax.gridlines(draw_labels=True)
            g.top_labels = False
            g.right_labels = False
            fig.colorbar(cf, ax=ax, location='right', shrink=0.7)

            ax = axes.flatten()[i + 4]
            diff = loc_cont2 - loc_cont1
            levels = np.linspace(-60, 60, 21)
            ax.set_title(df2_name + "-" + df1_name + " Local Contribution " + zname + " " + operator + " " + str(threshold))
            cf = ax.contourf(lonbins[0:-1], latbins[0:-1], diff, levels=levels,
                             transform=ccrs.PlateCarree(), cmap=cmap, extend="both")
            ax.coastlines()
            g = ax.gridlines(draw_labels=True)
            g.top_labels = False
            g.right_labels = False
            fig.colorbar(cf, ax=ax, location='right', shrink=0.7)

        if i == 1 or n == len(arg_list) - 1:
            title = f"Comparison of {df1_name} and {df2_name}"
            fig.suptitle(title)
            fig.tight_layout()
            plt.savefig(f"{output_dir}/comparison_loc_{n // 2}.png")
            plt.close(fig)
        n += 1
    return

# Main comparison function
def compare_dfs(df1, df2, df1_name, df2_name, output_dir):
    dict_bins, dict_log = bins_dfs(df1)

    var1d_list = ["RAINAREA", "MEANRAINRATE", "VOLRAIN", "RAINAREA_5", "VOLRAIN_5", "LON", "LAT", "R_ORIENTATION"]
    hist1d_dfs(df1, df2, df1_name, df2_name, dict_bins, dict_log, var1d_list, output_dir)

    var2d_list = [["RAINAREA", "MEANRAINRATE"], ["RAINAREA", "VOLRAIN"]]
    hist2d_dfs(df1, df2, df1_name, df2_name, dict_bins, dict_log, var2d_list, output_dir)

    arg_list = [["RAINAREA", "VOLRAIN", ">", 2000.0], ["R_SOLID", "VOLRAIN", "<", 0.2]]
    loc_contri_dfs(df1, df2, df1_name, df2_name, dict_bins, dict_log, arg_list, output_dir)
    return

# Main function
if __name__ == "__main__":
    # read IMERG dataset
    file_IMERG_l2 = '/flexfs/bayesics/source/POMD/POMD-PF/IMERG-PF/level2/202002.HDF'
    dict_IMERG = read_sds(file_IMERG_l2)

    # read GEOS5 dataset
    file_GEOS5_l2 = '/flexfs/bayesics/source/POMD/POMD-PF/GEOS5-PF/level2/202002.HDF'
    dict_GEOS5 = read_sds(file_GEOS5_l2)

    # convert IMERG PF and GEOS5 PF to pandas dataframe
    df_IMERG = pd.DataFrame.from_dict(dict_IMERG)
    df_GEOS5 = pd.DataFrame.from_dict(dict_GEOS5)

    # Produce process-oriented subset dataframes
    df_IMERG_rainarea_500 = df_IMERG.loc[df_IMERG['RAINAREA'] > 500.0]
    df_GEOS5_rainarea_500 = df_GEOS5.loc[df_GEOS5['RAINAREA'] > 500.0]
    df_IMERG_meanrainrate_02 = df_IMERG.loc[df_IMERG['MEANRAINRATE'] <= 0.2]
    df_GEOS5_meanrainrate_02 = df_GEOS5.loc[df_GEOS5['MEANRAINRATE'] <= 0.2]
    df_IMERG_rainarea_2000 = df_IMERG.loc[df_IMERG['RAINAREA'] > 2000.0]
    df_GEOS5_rainarea_2000 = df_GEOS5.loc[df_GEOS5['RAINAREA'] > 2000.0]
    df_IMERG_r_solid_02 = df_IMERG.loc[df_IMERG['R_SOLID'] < 0.2]
    df_GEOS5_r_solid_02 = df_GEOS5.loc[df_GEOS5['R_SOLID'] < 0.2]
    df_IMERG_r_solid_06 = df_IMERG.loc[df_IMERG['R_SOLID'] > 0.6]
    df_GEOS5_r_solid_06 = df_GEOS5.loc[df_GEOS5['R_SOLID'] > 0.6]
    df_IMERG_MCSs_02 = df_IMERG.loc[(df_IMERG['RAINAREA'] > 2000.0) & (df_IMERG['RAINAREA_5'] > 100.0)]
    df_GEOS5_MCSs_02 = df_IMERG.loc[(df_GEOS5['RAINAREA'] > 2000.0) & (df_GEOS5['RAINAREA_5'] > 100.0)]

    output_dir = "output_images"
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # compare IMERG and GEOS5 subset dfs
    print("Compare PFs with rainarea > 500 $km^2$")
    compare_dfs(df_IMERG_rainarea_500, df_GEOS5_rainarea_500, 'IMERG', 'GEOS5', output_dir)
    print("Compare PFs with mean rain rate <= 0.2 mm/hr")
    compare_dfs(df_IMERG_meanrainrate_02, df_GEOS5_meanrainrate_02, 'IMERG', 'GEOS5', output_dir)
    print("Compare PFs with rainarea > 2000 $km^2$")
    compare_dfs(df_IMERG_rainarea_2000, df_GEOS5_rainarea_2000, 'IMERG', 'GEOS5', output_dir)
    print("Compare PFs with rainarea > 2000 $km^2$ and rainarea_5 > 200 $km^2$")
    compare_dfs(df_IMERG_MCSs_02, df_GEOS5_MCSs_02, 'IMERG', 'GEOS5', output_dir)
