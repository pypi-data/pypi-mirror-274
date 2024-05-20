import numpy as np
import pandas as pd
from tslearn.utils import to_time_series_dataset
import matplotlib.pyplot as plt
from PROD.visual import plot_one_6dim_signal, plot_6dim_signal_dataset
from PROD.utils import incremental_mean_update, incremental_variance_update, transform_pd_to_npy, get_swich_points, set_signals_to_same_length
import pickle



class deviationClassifier():
    def __init__(self, n_dim, sensitivity, anom_tresh = 12, learn_from_signal = False, learning_treshold = 0.95):
        self.n_dim = n_dim
        self.anomaly_treshold = anom_tresh
        self.sensitivity = sensitivity
        self.magnitude = 0
        self.learning_treshold = learning_treshold
        self.mean_ts = None
        self.std_ts = None
        self.learn_from_signal = learn_from_signal
        self.time_threshold = 1
        self.true_thresh = 0
    
    def show_params(self):
        plot_one_6dim_signal(self.mean_ts, self.mean_ts, self.std_ts, sensitivity=self.sensitivity, anomaly_highlight = False)
    
    def freeze(self):
        self.learn_from_signal = False
        print("INFO: Learning is freezed.")
    
    def unfreeze(self):
        self.learn_from_signal = True
        print("INFO: Learning is unfreezed.")
    
    def status(self):
        message = "learning (unfreezed)" if self.learn_from_signal else "not learning (freezed)" 
        print(f"INFO: Model is {message}.")
        return self.learn_from_signal
    
    def set_true_thresh(self, value):
        self.true_thresh = value
        print(f"The True threshold set to {self.true_thresh}")
    
    
    def fit_whole_supervised_dataset(self, training_dataset, criterion = "ACC", value = None):
        correct_signals = [i[0] for i in training_dataset if i[1] == False]
        anom_signals = [i[0] for i in training_dataset if i[1] == True]
        correct_ds = to_time_series_dataset(correct_signals)
        mean_ts = np.nanmean(correct_ds, axis = 0)
        std_ts = np.nanstd(correct_ds, axis = 0)
        self.mean_ts = transform_pd_to_npy(mean_ts)
        self.std_ts = transform_pd_to_npy(std_ts)
        self.magnitude = len(correct_signals)
        self.freeze()
        n_of_correct_anomalies = [self.get_number_of_anomalies(sig, np.shape(sig)[0])[0] for sig in correct_signals]
        n_of_wrong_anomalies = [self.get_number_of_anomalies(sig, np.shape(sig)[0])[0] for sig in anom_signals]
        print("Correct: ", n_of_correct_anomalies)
        print("Wrong: ", n_of_wrong_anomalies)
        last_thresh = 1
        n_of_correct_anomalies.sort()
        n_of_wrong_anomalies.sort()
        if criterion == "ACC":
            candidates = np.unique(np.concatenate((n_of_correct_anomalies, n_of_wrong_anomalies)))
            max_count = 0
            best_thresh = None
            for tresh in candidates:
                count_good = np.sum(n_of_correct_anomalies < tresh)
                count_bad = np.sum(n_of_wrong_anomalies > tresh)
                total_count = count_good + count_bad
                if total_count > max_count:
                    max_count = total_count
                    best_thresh = tresh
        elif criterion == "sACC":
            candidates = np.unique(np.concatenate((n_of_correct_anomalies, n_of_wrong_anomalies)))
            max_count = 0
            best_thresh = None
            for tresh in candidates:
                count_good = np.sum(n_of_correct_anomalies < tresh)
                count_bad = np.sum(n_of_wrong_anomalies > tresh)
                value = 1 if value is None else value
                total_count = count_good + (len(n_of_correct_anomalies)/ len(n_of_wrong_anomalies)) * value * count_bad
                if total_count > max_count:
                    max_count = total_count
                    best_thresh = tresh
            
            self.anomaly_treshold = best_thresh
        elif criterion == "TPR":
            n_of_wrong_anomalies = np.array(n_of_wrong_anomalies)
            for thresh in range(1, max(n_of_wrong_anomalies)):
                max_idx = np.sum(n_of_wrong_anomalies >= thresh)
                if max_idx >= len(n_of_wrong_anomalies) * value:
                    last_thresh = thresh
                else:
                    self.anomaly_treshold = last_thresh
                    break
        elif criterion == "TNR":
            n_of_correct_anomalies = np.array(n_of_correct_anomalies)
            for thresh in range(1, max(n_of_correct_anomalies)):
                max_idx = np.sum(n_of_correct_anomalies >= thresh)
                if max_idx >= len(n_of_correct_anomalies) * value:
                    last_thresh = thresh
                else:
                    self.anomaly_treshold = last_thresh
                    break
        
        print("Threshold is set to: ", self.anomaly_treshold)
        print("INFO: Learning is freezed.")
        return max(n_of_wrong_anomalies)
    
    def set_anomaly_threshold(self, value):
        self.anomaly_treshold = value
    
    def fit_whole_unsupervised_dataset(self, training_dataset, success_ratio = 0.95, n_of_filtration_steps = 2, criterion = "ACC", value = 0.8):
        def filtration(train_ds):
            signals = [i[0] for i in train_ds]
            dataset = to_time_series_dataset(signals)
            mean_ts = np.nanmean(dataset, axis = 0)
            std_ts = np.nanstd(dataset, axis = 0)
            self.mean_ts = transform_pd_to_npy(mean_ts)
            self.std_ts = transform_pd_to_npy(std_ts)
            n_anomalies = [self.get_number_of_anomalies(sample, np.shape(sample)[0])[0] for sample in signals]
            anoms_idx_sorted_ = np.argsort(n_anomalies)
            anoms_idx_sorted_c = anoms_idx_sorted_[:int(success_ratio * len(anoms_idx_sorted_))]
            anoms_idx_sorted_a = anoms_idx_sorted_[int(success_ratio * len(anoms_idx_sorted_)):]
            filtered_sigs = [(signals[i], False) for i in anoms_idx_sorted_c]
            anom_sigs = [(signals[i], True) for i in anoms_idx_sorted_a]
            return filtered_sigs, anom_sigs
        anom_sigs = []
        new_corr = training_dataset
        for _ in range(n_of_filtration_steps):
            new_corr, new_anom = filtration(new_corr)
            anom_sigs.extend(new_anom)
        resulting_dataset = [*new_corr, *anom_sigs]
        self.fit_whole_supervised_dataset(resulting_dataset, criterion, value)


            
    
    def fit_incremental_dataset(self, training_dataset, vis = False, sens = 3):
        correct_signals = [i[0] for i in training_dataset if i[1] == False]
        for i, sample in enumerate(correct_signals):
            sample_len = np.shape(sample)[0]
            if self.mean_ts is not None:
                self.mean_ts, sample_ = set_signals_to_same_length(self.mean_ts, sample)
                self.std_ts, sample_ = set_signals_to_same_length(self.std_ts, sample)
            else:
                self.mean_ts = transform_pd_to_npy(sample)
                self.std_ts = np.zeros_like(self.mean_ts)
                if vis:
                    sample_ = transform_pd_to_npy(sample)
                    #plot_one_6dim_signal(sample_, self.mean_ts, self.std_ts, sensitivity=sens, anomaly_highlight = False)
                continue
            mean_ts, std_ts, sample_ = (transform_pd_to_npy(self.mean_ts),
                                        transform_pd_to_npy(self.std_ts),
                                        transform_pd_to_npy(sample))
            mean_ts, std_ts, sample_ = mean_ts[:sample_len, :], std_ts[:sample_len, :], sample_[:sample_len, :]
            old_mean = mean_ts
            mean_ts = incremental_mean_update(mean_ts, sample_, self.magnitude)
            self.mean_ts[:sample_len, :] = mean_ts
            std_ts = incremental_variance_update(std_ts, sample_, self.magnitude, old_mean, mean_ts)
            self.std_ts[:sample_len, :] = std_ts
            sample_ = transform_pd_to_npy(sample_)
            if vis:
                plot_one_6dim_signal(sample_, self.mean_ts, self.std_ts, sensitivity=sens, anomaly_highlight = False, real_len = sample_len)
                #plot_6dim_signal_dataset([(transform_pd_to_npy(sig), True) for sig in correct_signals[:i]])
            self.magnitude += 1

    def set_time_threshold(self, value):
        self.time_threshold = value
        print(f"INFO: Setting time threshold to {self.time_threshold}")

    def online_fit(self, dataset, criterion = "ACC", value = None, thresh_steps : np.ndarray|int = 20, time_steps: np.ndarray|int = 10, print_progress = False):
        self.fit_whole_supervised_dataset(dataset, criterion = "ACC", value = None)
        correct_signals = [transform_pd_to_npy(i[0]) for i in dataset if i[1] == False]
        anom_signals = [transform_pd_to_npy(i[0]) for i in dataset if i[1] == True]
        candidates = thresh_steps if type(thresh_steps) == np.ndarray else np.linspace(0.1, 10, thresh_steps)
        timestamps = time_steps if type(time_steps) == np.ndarray else np.linspace(300, 1000, time_steps)
        scores = np.zeros((thresh_steps,4))
        len_c = len(candidates)
        for idx, num in enumerate(candidates):
            if print_progress:
                print(f"INFO: Computing {idx + 1} out of {len_c}")
            counter, positive = 0, 0
            self.time_threshold = num
            for signal in correct_signals:
                for timestamp in timestamps:
                    counter += 1
                    positive += self.predict_partial_signal(signal[:int(timestamp), :], vis = False)
            TP_pos, TN_pos, FP_pos, FN_pos = 0, counter - positive, positive, 0
            TP_anom, TN_anom, FP_anom, FN_anom = 0,0,0,0
            for signal in anom_signals:
                lastpred = False
                for timestamp in timestamps:
                    counter += 1
                    prediction = self.predict_partial_signal(signal[:int(timestamp), :], vis = False)
                    if not lastpred and not prediction:
                        if timestamp == timestamps[-1]:
                            TN_anom -= len(timestamps)
                            FN_anom += len(timestamps)
                        TN_anom += 1
                    elif (not lastpred and prediction) or (lastpred and prediction):
                        TP_anom += 1
                    elif lastpred and not prediction:
                        FN_anom += 1
            TP, TN, FP, FN = TP_pos + TP_anom, TN_pos + TN_anom, FP_pos + FP_anom, FN_pos + FN_anom
            scores[idx, :] = np.array((TP, TN, FP, FN))
        accuracies = np.sum(scores[:, :2], axis=1)/np.sum(scores, axis=1)
        if criterion == "ACC":
            max_idx = np.argmax(accuracies)
            pass
        elif criterion == "sACC":
            value = 1 if value is None else value
            accuracies = (value * scores[:, 0] + scores[:, 1])/ ((2/(value + 1)) * np.shape(scores)[0])
            max_idx = np.argmax(accuracies)
            pass
           
        elif criterion == "TPR":
            value = 0.7 if value is None else value
            tpr = scores[:, 0]/(scores[:, 0] + scores[:, 3] + 0.0001)
            max_idx = np.argmax(np.sum(scores[:, :2], axis=1)*(tpr >= value))
            pass
        elif criterion == "TNR":
            value = 0.7 if value is None else value
            tnr = scores[:, 1]/(scores[:, 1] + scores[:, 2] + 0.0001)
            max_idx = np.argmax(np.sum(scores[:, :2], axis=1)*(tnr >= value))
            pass
        self.time_threshold = candidates[max_idx]
        print(f"Time threshold set to {self.time_threshold}")
        tpr = scores[max_idx, 0]/ (scores[max_idx, 0] + scores[max_idx, 3])
        tnr = scores[max_idx, 1]/ (scores[max_idx, 1] + scores[max_idx, 2])
        acc = sum(scores[max_idx, : 2])/sum(scores[max_idx, :])
        if print_progress:
            print(f"TPR: {tpr}, TNR: {tnr}, ACC:{acc}")



        
    def predict_full_signal(self, sample, vis = True, save_fig = None):
        if self.magnitude == 0:
            print("WARN: The classifier is not trained, aborting classification!")
            if self.learn_from_signal:
                self.mean_ts = sample
                self.std_ts = np.zeros_like(sample)
                self.magnitude = 1
            return
        sample = transform_pd_to_npy(sample)
        sample_len = np.shape(sample)[0]
        mean_len = np.shape(self.mean_ts)[0]
        self.mean_ts, sample = set_signals_to_same_length(self.mean_ts, sample)
        anomalies_sum_all, anomalies_sum, anomalies = self.get_number_of_anomalies(sample, sample_len)
        ls = get_swich_points(anomalies_sum)
        anomalies = transform_pd_to_npy(anomalies)
        anomalies_sw_points = [get_swich_points(anomalies[:, i]) for i in range(self.n_dim)]
        if vis:
            plot_one_6dim_signal(sample, self.mean_ts, self.std_ts,
                                 self.sensitivity, anomalies = ls, anomalies_all = anomalies_sw_points, save_fig=save_fig, real_len = sample_len)
        is_anomaly = anomalies_sum_all > self.anomaly_treshold
        #print(anomalies_sum_all)
        if not is_anomaly and self.learn_from_signal:
            old_mean = self.mean_ts
            self.mean_ts = incremental_mean_update(self.mean_ts, sample, self.magnitude)
            self.std_ts = incremental_variance_update(self.std_ts, sample, self.magnitude, old_mean, self.mean_ts)
            self.magnitude += 1
        return is_anomaly

    def predict_partial_signal(self, sample, vis = True, save_fig = None):
        sample = transform_pd_to_npy(sample)
        if self.magnitude == 0:
            print("WARN: The classifier is not trained, aborting classification!")
            if self.learn_from_signal and self.learning_treshold < (sample_len/mean_len):
                self.mean_ts = sample
                self.std_ts = np.zeros_like(sample)
                self.magnitude = 1
            return
        sample_len = np.shape(sample)[0]
        if sample_len < self.true_thresh:
            return False
        mean_len = np.shape(self.mean_ts)[0]
        self.mean_ts, sample = set_signals_to_same_length(self.mean_ts, sample)
        diff = np.abs(sample[:sample_len, :] - self.mean_ts[:sample_len, :])
        anomalies = diff > np.abs(self.sensitivity * self.std_ts[:sample_len, :])
        anomalies_sum = np.sum(anomalies, axis=1)
        ls = get_swich_points(anomalies_sum)
        anomalies = transform_pd_to_npy(anomalies)
        anomalies_sw_points = [get_swich_points(anomalies[:, i]) for i in range(self.n_dim)]
        if vis:
            sample = transform_pd_to_npy(sample)
            plot_one_6dim_signal(sample[:sample_len, :], self.mean_ts[:sample_len, :], self.std_ts[:sample_len, :],
                                 self.sensitivity, anomalies = ls, anomalies_all = anomalies_sw_points, save_fig=save_fig, real_len = sample_len)
        is_anomaly = np.sum(anomalies) > self.anomaly_treshold * (sample_len/mean_len) * self.time_threshold
        if not is_anomaly and self.learn_from_signal and self.learning_treshold < (sample_len/mean_len):
            old_mean = self.mean_ts
            self.mean_ts = incremental_mean_update(self.mean_ts, sample, self.magnitude)
            self.std_ts = incremental_variance_update(self.std_ts, sample, self.magnitude, old_mean, self.mean_ts)
            self.magnitude += 1
        return is_anomaly
    
    def get_number_of_anomalies(self, signal, sample_len):
        sample = transform_pd_to_npy(signal)
        diff = np.abs(sample[:sample_len, :] - self.mean_ts[:sample_len, :])
        anomalies = diff > np.abs(self.sensitivity * self.std_ts[:sample_len, :])
        anomalies_sum = np.sum(anomalies, axis=1)
        anomalies_sum_all = np.sum(anomalies_sum)
        return anomalies_sum_all, anomalies_sum, anomalies
    
    def save_params(self, name, dirpath = "./model_params/"):
        path = dirpath + (name if len(name) > 4 and name[-4:] == ".pkl" else name + ".pkl")
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    def load_params(self, path):
        with open(path, 'rb') as f:
            loaded_object : deviationClassifier = pickle.load(f)
        self.n_dim = loaded_object.n_dim
        self.anomaly_treshold = loaded_object.anomaly_treshold
        self.sensitivity = loaded_object.sensitivity
        self.magnitude = loaded_object.magnitude
        self.learning_treshold = loaded_object.learning_treshold
        self.mean_ts = loaded_object.mean_ts
        self.std_ts = loaded_object.std_ts

    
    def __repr__(self):
        return f"""n-Sigma anomaly detector:
                    n: {self.sensitivity}
                    Number of training signals: {self.magnitude}"""
    