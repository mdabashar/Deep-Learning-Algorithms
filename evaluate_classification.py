# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 18:19:08 2020

@author: User
"""

from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.metrics import classification_report
import numpy as np
import datetime

class EvaluateBinaryClassification:
    
    def __init__(self, gnd_truths, predictions):
        print('EvaluateBinaryClassification Object Created\n')
        self.gnd_truths = np.array(gnd_truths)
        self.predictions = np.array(predictions)
        
    def get_basic_report(self):
        
        actual = self.gnd_truths
        predicted = self.predictions
        
        tp = np.count_nonzero(predicted * actual)
        tn = np.count_nonzero((predicted - 1) * (actual - 1))
        fp = np.count_nonzero(predicted * (actual - 1))
        fn = np.count_nonzero((predicted - 1) * actual)
        
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1measure = (2 * precision * recall) / (precision + recall)
        
        cks = cohen_kappa_score(predicted, actual)
        false_positive_rate, true_positive_rate, thresholds = roc_curve(actual, predicted)
        auc_ = auc(false_positive_rate, true_positive_rate)
        #roc_auc_ = roc_auc_score(actual, predicted)
        
        basic_report = {}
        basic_report['Total Samples'] =	len(actual)
        basic_report['Positive Samples'] = sum(actual)
        basic_report['Negative Samples'] = len(actual)-sum(actual)
        basic_report['True Positive'] = tp
        basic_report['True Negative'] = tn
        basic_report['False Positive'] = fp
        basic_report['False Negative'] = fn
        basic_report['Accuracy'] = accuracy
        basic_report['Precision'] = precision
        basic_report['Recall'] = recall
        basic_report['F1 Measure'] = f1measure
        basic_report['Cohen Kappa Score'] = cks
        basic_report['Area Under Curve'] = auc_
        #basic_report['ROC_AUC'] = roc_auc_
        
        return basic_report
    
    def get_full_report(self):
        actual = self.gnd_truths
        predicted = self.predictions
        full_report = self.get_str(self.get_basic_report()) + '\n'
        full_report += classification_report(actual, predicted)
        return full_report
    
    def save_basic_report(self, path=''):
        basic_report = '============'+str(datetime.datetime.now())+'============\n'
        basic_report += self.get_str(self.get_basic_report())
        with open(path+'basic_report.txt', 'a+') as FO:
            FO.write(basic_report)
    
    def save_full_report(self, model_name='', path=''):
        full_report = '============{}============\n'.format(model_name)
        full_report += '============'+str(datetime.datetime.now())+'============\n'
        full_report += self.get_full_report()
        with open(path+'full_report.txt', 'a+') as FO:
            FO.write(full_report)
    
    def get_str(self, report):
        str_ = ''
        for key in report.keys():
            str_ += key + '\t' + str(report[key]) + '\n'
        return str_
    
    
    
def main():
    ebc = EvaluateBinaryClassification([0, 1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 0, 1])
    #print(ebc.get_str(ebc.get_basic_report()))
    print(ebc.get_full_report())
    ebc.save_basic_report()
    ebc.save_full_report()

if __name__ == '__main__':
    main()