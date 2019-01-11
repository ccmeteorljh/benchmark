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
                    'keyword': 'val ppl',
                    'result': 'split(", ")[3].split(": ")[1]',
                    'step': 'split(", ")[0].split(": ")[1]',
                    'indicant': 'test_ppl'
                }],
            'speedup_ratio':
                {
                    'keyword': 'examples/sed',
                    'result': 'split(", ")[2].split(" ")[0]',
                    'method': 'mean'
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
                    'keyword': 'test map [',
                    'result': 'split(",")[1].split("[")[1].split("]")[0]',
                    'step': 'split(",")[0].split(" ")[1]',
                    'indicant': 'test_map'
                }
            ],
            'speedup_ratio':
                {
                    'keyword': 'time ',
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
                    'result': 'split("pass_time_cost ")[1]',
                    'method': 'mean'
                }
        },
        'BiDAF': {
            'performance': [
                {
                    'keyword': 'Average loss from batch',
                    'result': 'split("Average loss from batch")[1].split("is ")[1]',
                    'step': 'index',
                    'indicant': 'ave_loss'
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
                    'keyword': 'area=medium',
                    'result': 'split("=")[4][1:]',
                    'step': 'index',
                    'indicant': 'map'
                }
            ],
            'speedup_ratio':
                {
                    'keyword': ' time ',
                    'result': 'split(", ")[3].split(" ")[1]',
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
                    'result': 'split(": ")[6]',
                    'method': 'mean'
                }
        }
        #todo add other models
}
re_conf_tf_models = {}

frame2re = {
    "paddlepaddle": re_conf_paddle_models,
    "tensorflow": re_conf_tf_models
}
