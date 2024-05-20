import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PROD.utils import transform_pd_to_npy
from PROD.metrics.dtw_barycenter import METHODS_LABEL_DICT
import pickle
from scipy.interpolate import interp1d


def draw_roc_from_dict(roc_dict, save_fig = None, title = None, scatter = False, fig = None):
    def mean_roc(roc_curves, num_points=100):
        mean_fpr = np.linspace(0, 1, num_points)
        interp_tprs = []
        for roc in roc_curves:
            fpr, tpr = roc[1], roc[0]
            interp_func = interp1d(fpr, tpr, kind='linear', fill_value="extrapolate")
            interp_tprs.append(interp_func(mean_fpr))
        mean_tpr = np.mean(interp_tprs, axis=0) 
        return mean_fpr, mean_tpr
    #plt.figure(figsize=(4,4))
    colors = ["red", "green", "blue", "orange", "brown"]
    if isinstance(roc_dict, str):
        with open(roc_dict, "rb") as f:
            total_roc = pickle.load(f)
    elif isinstance(roc_dict, dict):
        total_roc = roc_dict
    aucs = []
    curves = [np.flip(i["ROC"], axis=1) for i in total_roc]
    fpr_m, tpr_m = mean_roc(curves)
    for i in range(len(curves)):
        if scatter:
            plt.scatter(curves[i][1,:], curves[i][0,:], color = colors[i%5], marker="x", s=10)
        else:
            plt.plot(curves[i][1,:], curves[i][0,:], color = "tab:green", alpha = 0.75, label="")
        #auc = np.trapz(np.nan_to_num(np.flip(np.append(np.flip(np.append(curves[i][0, :], 1)), 0))), np.nan_to_num(np.flip(np.append(np.flip(np.append(curves[i][1, :], 1)), 0))))
        auc = np.trapz(np.nan_to_num(np.flip(np.append(curves[i][0, :], 0))), np.nan_to_num(np.flip(np.append(curves[i][1, :], 0))))
        aucs.append(auc)
        print(f"AUC is {auc}")
    if scatter:
        pass
        #plt.plot(tpr_m, fpr_m, color = "blue", label="Mean ROC")
    else:
        #plt.plot(np.nan_to_num(np.flip(np.append(np.flip(np.append(fpr_m, 1)), 0))), np.nan_to_num(np.flip(np.append(np.flip(np.append(tpr_m, 1)), 0))), color = "blue", label="Mean ROC")
        plt.plot(fpr_m, tpr_m, color = "blue", label="Mean ROC")
    print(f"Mean AUC is: {np.mean(aucs)}")
    plt.plot([0,1], [0,1], color="black", linestyle= "dotted")
    plt.legend(loc="lower right")
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.grid()
    if title is not None:
        plt.title(title)
    if save_fig is not None:
        name = str(save_fig) if len(save_fig) > 4 and str(save_fig)[-4:] == ".pdf" else str(save_fig) + ".pdf"
        plt.savefig(name , format='pdf', bbox_inches='tight')
    #plt.show()
    return total_roc

def plot_one_6dim_signal(signal1, avg = None, std = None, sensitivity = None, save_fig = None, anomaly_highlight = False, anomalies = [], anomalies_all = [], real_len = 0):
    fig, ax = plt.subplots(6, 1, figsize=(6.5, 5), sharex=False)
    ylabels = [ "Force x",
                "Force y",
                "Force z",
                "Torque x",
                "Torque y",
                "Torque z"
             ]
    signal_len = np.shape(signal1)[0] if real_len==0 else real_len
    xaxis = np.arange(signal_len)
    for i in range(0, 6):
        if avg is not None:
            upper_bound = avg[:, i] + sensitivity * std[:, i]
            lower_bound = avg[:, i] - sensitivity * std[:, i]
            upper_bound = upper_bound[:signal_len]
            lower_bound = lower_bound[:signal_len]
            ax[i].plot(xaxis, upper_bound, color = "#378CE7")
            ax[i].plot(xaxis, lower_bound, color = "#378CE7")
            ax[i].fill_between(xaxis, lower_bound, upper_bound, color = "#378CE7", alpha = 0.3)
        ax[i].plot(xaxis[:signal_len], signal1[:signal_len, i], color = "black", linewidth = 1)
        ax[i].set_ylabel(ylabels[i])
        if i < 5:
            ax[i].set_xticklabels([])
    ax[5].set_xlabel("Time")
    #fig.suptitle("Sample signal of a process", fontweight="bold", fontsize = 12)
    fig.align_ylabels()
    if anomaly_highlight:
        for i in range(0,6):
            for j in range(len(anomalies)):
                ax[i].axvspan(*anomalies[j], color='red', alpha=0.2)
            for k in range(len(anomalies_all[i])):
                ax[i].axvspan(*anomalies_all[i][k], color='red', alpha = 0.6)
    if save_fig is not None:
        name = str(save_fig) if len(save_fig) > 4 and str(save_fig)[-4:] == ".pdf" else str(save_fig) + ".pdf"
        plt.savefig(name , format='pdf', bbox_inches='tight')
    plt.show()

def plot_6dim_signal_dataset(signal_dataset, save_fig = None, anomaly_highlight = False, anomalies_start = [], anomalies_end = []):
    fig, ax = plt.subplots(6, 1, figsize=(6.5, 5), sharex=True)
    ylabels = [ "Force x",
                "Force y",
                "Force z",
                "Torque x",
                "Torque y",
                "Torque z"
             ]
    for signal in signal_dataset:
        xaxis = np.arange(np.shape(signal[0])[0])
        color = "blue" if signal[1] else "red"
        sig = transform_pd_to_npy(signal[0])
        for i in range(0, 6):
            ax[i].plot(xaxis, sig[ : , i], color = color, linewidth = 1)
            ax[i].set_ylabel(ylabels[i])
            if i < 5:
                ax[i].set_xticklabels([])
        ax[5].set_xlabel("Time")
        #fig.suptitle("Sample signal of a process", fontweight="bold", fontsize = 12)
        fig.align_ylabels()
    if anomaly_highlight:
        assert len(anomalies_start) == len(anomalies_end)
        for i in range(0,6):
            for j in range(len(anomalies_start)):
                ax[i].axvspan(anomalies_start[j], anomalies_end[j], color='red', alpha=0.3)
    if save_fig is not None:
        name = str(save_fig) if len(save_fig) > 4 and str(save_fig)[-4:] == ".pdf" else str(save_fig) + ".pdf"
        plt.savefig(name , format='pdf', bbox_inches='tight')
    plt.show()

def plot_samples(correct_points, wrong_points, barycenters, ebarycenters = [[], []], method = [1, 5], title = "", correct_idx = [], anom_idx = [], save_fig1 = "samples"):
    scatter_if_not_empty(correct_points, color="blue", marker="+")
    scatter_if_not_empty(wrong_points, color="red", marker="x")
    #scatter_if_not_empty(barycenters, color="green", marker="o")
    #scatter_if_not_empty(ebarycenters, color="orange", marker="o")
    plt.grid(True)
    plt.xlabel(METHODS_LABEL_DICT[method[0]])
    plt.ylabel(METHODS_LABEL_DICT[method[1]])
    plt.title(title)
    plt.legend(["Successfull process",
                "Failed process",
                "Barycenter distance",
                "Euclidean barycenter distance"], loc="lower right")
    plt.xlim([0, 50000])
    plt.ylim([0, 5000])
    if correct_idx:
        for i, label in enumerate(correct_idx):
            plt.annotate(label+1, (correct_points[i]))
    if anom_idx:
        for i, label in enumerate(anom_idx):
            plt.annotate(label+1, (wrong_points[i]))
    if save_fig1 is not None:
        name = str(save_fig1) if len(save_fig1) > 4 and str(save_fig1)[-4:] == ".pdf" else str(save_fig1) + ".pdf"
        plt.savefig(name , format='pdf', bbox_inches='tight')
    plt.show()

def scatter_if_not_empty(points, color, marker):
    if points:
        if np.shape(points)[0] != 2:
            points = np.array(points).T
        if points is not None:
            plt.scatter(*points, color=color, marker=marker)
    