#!/usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
#
#======================================================================

"""
@Desc: log_extract_re module
@File: log_extract_re.py
@Author: liangjinhua
@Date: 2018/10/24 14:16
"""
import re

#personal/models 模型提取规则

#github paddle/models 模型提取规则
re_conf_paddle_models = {
    'CRNN_CTC': {
        'performance': [
            {
                'keyword': 'train_acc',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'train_acc'
            }],
        'speedup_ratio':
            {
                'keyword': 'average fps',
                'result': 'split(": ")[1].split(",")[0]',
                'method': 'sum'
            }
    },
    'seq2seq+attention': {
        'performance': [
            {
                'keyword': 'train_acc',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'train_acc'
            }],
        'speedup_ratio':
            {
                'keyword': 'average fps',
                'result': 'split(": ")[1].split(",")[0]',
                'method': 'sum'
            }
    },
    'transformer': {
        'performance': [
            {
                'keyword': 'BLEU = ',
                'result': 'split()[2][:-1]',
                'step': 'index',
                'indicant': 'BLEU'
            }],
        'speedup_ratio':
            {
                'keyword': 'step/s',
                'result': 'split()[-2]',
                'method': 'sum'
            }
    },
    'SE-ResNeXt50': {
        'performance': [
            {
                'keyword': 'test_acc1',
                'result': 'split(", ")[5].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc1'
            },
            {
                'keyword': 'test_acc5',
                'result': 'split(", ")[6].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc5'
            }
        ],
        'speedup_ratio':
            {
                'keyword': ' time ',
                'result': 'split("time ")[1].split(" ")[0]',
                'method': 'mean'
            }
    },
    'Inception-V4': {
        'performance': [
            {
                'keyword': 'test_acc1',
                'result': 'split(", ")[5].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc1'
            },
            {
                'keyword': 'test_acc5',
                'result': 'split(", ")[6].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc5'
            }
        ],
        'speedup_ratio':
            {
                'keyword': ' time ',
                'result': 'split("time ")[1].split(" ")[0]',
                'method': 'mean'
            }
    },
    'ResNet50': {
        'performance': [
            {
                'keyword': 'test_acc1',
                'result': 'split(", ")[5].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc1'
            },
            {
                'keyword': 'test_acc5',
                'result': 'split(", ")[6].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc5'
            }
        ],
        'speedup_ratio':
            {
                'keyword': ' time ',
                'result': 'split("time ")[1].split(" ")[0]',
                'method': 'mean'
            }
    },
    'MobileNet': {
        'performance': [
            {
                'keyword': 'test_acc1',
                'result': 'split(", ")[5].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc1'
            },
            {
                'keyword': 'test_acc5',
                'result': 'split(", ")[6].split(" ")[1]',
                'step': 'split(", ")[0].split(" ")[2]',
                'indicant': 'test_acc5'
            }
        ],
        'speedup_ratio':
            {
                'keyword': ' time ',
                'result': 'split("time ")[1].split(" ")[0]',
                'method': 'mean'
            }
    },
    'ssd': {
        'performance': [
            {
                'keyword': 'Best test map',
                'result': 'split()[-1]',
                'step': 'index',
                'indicant': 'test_map'
            }
        ],
        'speedup_ratio':
            {
                'keyword': ' time ',
                'result': 'split("time ")[1]',
                'method': 'mean'
            }
    },
    'text_classification_bow': {
        'performance': [
            {
                'keyword': 'avg_acc',
                'result': 'split(",")[1].split(": ")[1]',
                'step': 'split(",")[0].split(": ")[1]',
                'indicant': 'avg_acc'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'pass_time_cost',
                'result': 'split(",")[3].split(": ")[1]',
                'method': 'mean'
            }
    },
    'text_classification_cnn': {
        'performance': [
            {
                'keyword': 'avg_acc',
                'result': 'split(",")[1].split(": ")[1]',
                'step': 'split(",")[0].split(": ")[1]',
                'indicant': 'avg_acc'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'pass_time_cost',
                'result': 'split(",")[3].split(": ")[1]',
                'method': 'mean'
            }
    },
    'PyramidBox': {
        'performance': [
            {
                'keyword': 'batch 0',
                'result': 'split(", ")[2].split(" ")[2]',
                'step': 'split(", ")[0].split(" ")[1]',
                'indicant': 'face loss'
            },
            {
                'keyword': 'batch 0',
                'result': 'split(", ")[3].split(" ")[2]',
                'step': 'split(", ")[0].split(" ")[1]',
                'indicant': 'head loss'
            }
        ],
         'speedup_ratio':
            {
                'keyword': 'time ',
                'result': 'split("time ")[1]',
                'method': 'mean'
            }
    },

    "DeepLab_V3+": {
        'performance': [
            {
                'keyword': ', mIoU:',
                'result': 'split(", ")[1].split(": ")[1][0:6]',
                #'step': 'split(", ")[0].split(" ")[1]',
                'step': 'index',
                'indicant': 'mIoU'
            }],
        'speedup_ratio':
            {
                'keyword': 'step_time_cost',
                'result': 'split("step_time_cost: ")[1]',
                'method': 'mean'
            }

    },
    'cudnn_lstm': {
        'performance': [
            {
                'keyword': 'train ppl',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'train_ppl'
            },
            {
                'keyword': 'valid ppl',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'valid_ppl'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'lstm_language_model_duration',
                'result': 'split()[2]',
                'method': 'mean'
            }
    },
    'StaticRNN': {
        'performance': [
            {
                'keyword': 'train ppl',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'train_ppl'
            },
            {
                'keyword': 'valid ppl',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'valid_ppl'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'lstm_language_model_duration',
                'result': 'split()[2]',
                'method': 'mean'
            }
    },
    'PaddingRNN': {
        'performance': [
            {
                'keyword': 'train ppl',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'train_ppl'
            },
            {
                'keyword': 'valid ppl',
                'result': 'split()[2]',
                'step': 'index',
                'indicant': 'valid_ppl'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'lstm_language_model_duration',
                'result': 'split()[2]',
                'method': 'mean'
            }
    },
    'CycleGAN': {
        'speedup_ratio':
            {
                'keyword': 'Batch_time_cost',
                'result': 'split("; ")[6].split(": ")[1]',
                'method': 'mean'
            }
    },
    'DCGAN': {
        'speedup_ratio':
            {
                'keyword': 'Batch_time_cost',
                'result': 'split("=")[1]',
                'method': 'mean'
            }
    },
    'DAM': {
        'performance': [
            {
                'keyword': 'ave loss',
                'result': 'split("[")[2].split("]")[0]',
                'step': 'index',
                'indicant': 'ave_loss'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'pass_time_cost',
                'result': 'split()[-2]',
                'method': 'mean'
            }
    },
    'BiDAF': {
        'performance': [
            {
                'keyword': 'Rouge-L',
                'result': 'split("Rouge-L")[1].split(": ")[1].split(",")[0]',
                'step': 'index',
                'indicant': 'Rouge-L'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'epoch_time_cost',
                'result': 'split(", ")[1].split(": ")[1]',
                'method': 'mean'
            }
    },
    'Faster-RCNN': {
        'performance': [
            {
                'keyword': re.compile(r"Average Precision.*area=medium.*"),
                'result': 'split("=")[4][1:]',
                'step': 'index',
                'indicant': 'map'
            }
        ],
        'speedup_ratio':
            {
                'keyword': ' time: ',
                'result': 'split()[-1]',
                'method': 'mean'
            }
    },
    'TSN': {
        'performance': [
            {
                'keyword': 'test_acc1',
                'result': 'split(", ")[2].split(": ")[1]',
                'step': 'split(", ")[0].split(": ")[1]',
                'indicant': 'test_acc1'
            },
            {
                'keyword': 'test_acc5',
                'result': 'split(", ")[3].split(": ")[1]',
                'step': 'split(", ")[0].split(": ")[1]',
                'indicant': 'test_acc5'
            }
        ],
        'speedup_ratio':
            {
                'keyword': '\ttime: ',
                'result': 'split()[-2]',
                'method': 'mean'
            }
    }
        #todo add other models
}
re_conf_tf_models = {
    'ResNet50': {
            'performance': [
                {
                    'keyword': "'accuracy'",
                    'result': 'split()[11][:-1]',
                    'step': 'index',
                    'indicant': 'test_acc1'
                },
                {
                    'keyword': "'accuracy_top_5'",
                    'result': 'split()[11][:-1]',
                    'step': 'index',
                    'indicant': 'test_acc5'
                }
            ],
            'speedup_ratio':
                {
                    'keyword': 'global_step/sec: ',
                    'result': 'split("global_step/sec: ")[1]',
                    'method': 'mean',
                    'else': 'reciprocal'
                }
        },
    'MobileNet': {
        'performance': [
            {
                'keyword': 'eval/Accuracy',
                'result': 'split("[")[1].split("]")[0]',
                'step': 'index',
                'indicant': 'acc'
            }
        ],
        'speedup_ratio':
                {
                    'keyword': 'global_step/sec: ',
                    'result': 'split("global_step/sec: ")[1]',
                    'method': 'mean',
                    'else': 'reciprocal'
                }
    },
    'Inception-V4': {
        'performance': [
            {
                'keyword': 'eval/Accuracy',
                'result': 'split("[")[1].split("]")[0]',
                'step': 'index',
                'indicant': 'acc'
            }
        ],
        'speedup_ratio':
                {
                    'keyword': 'global_step/sec: ',
                    'result': 'split("global_step/sec: ")[1]',
                    'method': 'mean',
                    'else': 'reciprocal'
                }
    },
    'StaticRNN': {
        'performance': [
            {
                'keyword': 'Train Perplexity',
                'result': 'split()[-1]',
                'step': 'index',
                'indicant': 'train_ppl'
            },
            {
                'keyword': 'Valid Perplexity',
                'result': 'split()[-1]',
                'step': 'index',
                'indicant': 'valid_ppl'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'speed:',
                'result': 'split()[-2]',
                'method': 'mean'
            }
    },
    'cudnn_lstm': {
        'performance': [
            {
                'keyword': 'Train Perplexity',
                'result': 'split()[-1]',
                'step': 'index',
                'indicant': 'train_ppl'
            },
            {
                'keyword': 'Valid Perplexity',
                'result': 'split()[-1]',
                'step': 'index',
                'indicant': 'valid_ppl'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'speed:',
                'result': 'split()[-2]',
                'method': 'mean'
            }
    },
    'DeepLab_V3+': {
            'performance': [
                {
                    'keyword': "miou",
                    'result': 'split("[")[1].split("]")[0]',
                    'step': 'index',
                    'indicant': 'miou'
                }
            ],
            'speedup_ratio':
                {
                    'keyword': 'sec/step',
                    'result': 'split()[-2][1:]',
                    'method': 'mean'
                }
        },
    'DCGAN': {
        'speedup_ratio':
            {
                'keyword': 'Epoch:',
                'result': 'split(":")[2].split()[0][:-1]',
                'method': 'mean'
            }
    },
    'transformer': {
        'performance': [
            {
                'keyword': 'BLEU = ',
                'result': 'split()[2][:-1]',
                'step': 'index',
                'indicant': 'BLEU'
            }],
        'speedup_ratio':
            {
                'keyword': 'global_step/sec',
                'result': 'split()[-1]',
                'method': 'sum'
            }
    },
    'CycleGAN': {
        'speedup_ratio':
            {
                'keyword': 'batch_cost',
                'result': 'split(":")[1]',
                'method': 'mean'
            }
    }

}
re_conf_pytorch_models = {
    'TSN': {
        'performance': [
            {
                'keyword': 'Testing Results:',
                'result': 'split()[3]',
                'step': 'index',
                'indicant': 'test_acc1'
            },
            {
                'keyword': 'Testing Results:',
                'result': 'split()[5]',
                'step': 'index',
                'indicant': 'test_acc5'
            }
        ],
        'speedup_ratio':
            {
                'keyword': 'Epoch: [0]',
                'result': 'split()[6][1:-1]',
                'method': 'mean'
            }
    }
}
re_conf_theano_models = {}
re_conf_caffe_models = {}

frame2re = {
    "paddlepaddle": re_conf_paddle_models,
    "tensorflow": re_conf_tf_models,
    "pytorch": re_conf_pytorch_models,
    "theano": re_conf_theano_models,
    "caffe": re_conf_caffe_models
}
