import biondi, os , glob, pickle
import pandas as pd
import numpy as np
from tensorflow.keras import Input, Model, models, layers, metrics
from jarvis.train.box import BoundingBox
from tensorflow import keras
import matplotlib.pyplot as plt

###Load training, validation, and test datasets###
#specify dataset directory
dataset_dir = ...
with open(dataset_dir + 'LV retinanet dataset including lv- training dataset 06152023.pickle','rb') as handle:
    x = pickle.load(handle)
with open(dataset_dir + 'LV retinanet dataset including lv- validation dataset 06152023.pickle','rb') as handle:
    v = pickle.load(handle)
with open(dataset_dir + 'LV retinanet dataset including lv- test dataset 06152023.pickle','rb') as handle:
    t = pickle.load(handle)

###Create data generaters which will be passed to the keras models for Retinanet training and validation###
xgen = biondi.dataset.TrainingGenerator(data=x, batch_size=16, retinanet=True, contrast=True)
vgen = biondi.dataset.TrainingGenerator(data=v, batch_size=16, retinanet=True, validation=True)

###Define various parameters and generate inputs for the generation of the RetinaNet model###
bb_c3_16 = BoundingBox(
    image_shape=(256,256),
    classes=1,
    c=[3],
    anchor_shapes=[16],
    anchor_scales=[1],
    anchor_ratios=[1],
    iou_upper=0.5,
    iou_lower=0.2)

inputs = bb_c3_16.get_inputs({'dat':Input(name='dat', shape=(None, 256, 256, 3)),
                              'cls-c3': Input(name='cls-c3_y', shape=(None, 32, 32, 1)),
                              'reg-c3': Input(name='reg-c3_y', shape=(None, 32, 32, 4)),},
                              Input)
###Create the RetinaNet model###
rn_model = biondi.models.retinanet_resnet50_3d(inputs, K=1, A=1, feature_maps=('c3'), lr=2e-4, filter_ratio=1)


###Start training RetinaNet model###
#create checkpoint object to save the model after each epoch.
chckpnt_dir = ...
checkpoint = keras.callbacks.ModelCheckpoint(filepath=chckpnt_dir + 'LV_with_lv-_retinanet_c3_smallbox_1fr_epoch-{epoch:02d}_val_loss-{val_loss:.4f}_val_ppv-{val_cls-c3_ppv:.4f}_val_sens-{val_cls-c3_sens:.4f}')

#train model. Depending on system resources the number of workers and the max_queue_size can be adjusted.
rn_hist = rn_model.fit(x=xgen, epochs=50, validation_data=vgen, workers=16, max_queue_size=100, verbose=1, callbacks=[checkpoint],)

###Visualize model training and performance across epochs###
#create list of model checkpoint saves
chckpnts = sorted(glob.glob(chckpnt_dir + 'LV_with_lv-_retinanet_c3_smallbox_1fr_epoch*'))

#extract validation loss, positive predictive value, and sensitivity from model checkpoint filenames.
modelstats_loss_ppv_sens = np.array([[i[-37:-31],i[-22:-16],i[-6:]] for i in chckpnts])
plt.ylim((0,0.8))
plt.xlim(8,41)
plt.plot(modelstats_loss_ppv_sens[:,0].astype(float), label='val_loss')
plt.plot(modelstats_loss_ppv_sens[:,1].astype(float), label='val_ppv')
plt.plot(modelstats_loss_ppv_sens[:,2].astype(float), label='val_sens')
plt.legend()
plt.show()

#calculate and visual the intersection over union (IOU) of model generated boxes and ground truth#
#measure median, 25% quartile, and 75% quartile across checkpoints.
chckpnt_ios = []
anchors_true, _ = bb_c3_16.convert_box_to_anc(v)
for i in chckpnts:
    print(os.path.basename(i))
    model = models.load_model(i)
    ious = {
        'med': [],
        'p25': [],
        'p75': []}

    rn_preds = model.predict(vgen, workers=16, max_queue_size=100)
    anchors_pred, _ = bb_c3_16.convert_box_to_anc(rn_preds, iou_nms=0.3)

    curr = []
    for pred, true in zip(anchors_pred, anchors_true):
        for p in pred:
            iou = bb_c3_16.calculate_ious(box=p, anchors=true)
            if iou.size > 0:
                curr.append(np.max(iou))
            else:
                curr.append(0)

    if len(curr) == 0:
        curr = [0]

    ious['med'].append(np.median(curr))
    ious['p25'].append(np.percentile(curr, 25))
    ious['p75'].append(np.percentile(curr, 75))

    ious = {k: np.array(v) for k, v in ious.items()}
    df = pd.DataFrame(index=np.arange(ious['med'].size))
    df['iou_median'] = ious['med']
    df['iou_p-25th'] = ious['p25']
    df['iou_p-75th'] = ious['p75']

    # --- Print accuracy
    print(df['iou_median'].median())
    print(df['iou_p-25th'].median())
    print(df['iou_p-75th'].median())
    chckpnt_ios.append(df)

#plot IOUs
plt.plot([i.to_numpy()[0][0] for i in chckpnt_ios], label='med')
plt.plot([i.to_numpy()[0][1] for i in chckpnt_ios], label='p25')
plt.plot([i.to_numpy()[0][2] for i in chckpnt_ios], label='p75')
plt.legend()
plt.xlim(8,41)
plt.show()

###RetinaNet performance statistics from test dataset###
# model checkpoint 'LV_with_lv-_retinanet_c3_smallbox_1fr_epoch-21_val_loss-0.0056_val_ppv-0.4283_val_sens-0.7352' was used
test_model = models.load_model(chckpnt_dir + 'LV_with_lv-_retinanet_c3_smallbox_1fr_epoch-21_val_loss-0.0056_val_ppv-0.4283_val_sens-0.7352')
tgen = biondi.dataset.TrainingGenerator(data=t, batch_size=16, retinanet=True, validation=True)

ious = {
    'med': [],
    'p25': [],
    'p75': []}

enqueuer = keras.utils.OrderedEnqueuer(tgen)
enqueuer.start(workers=12, max_queue_size=128)
datas = enqueuer.get()
progbar = keras.utils.Progbar(tgen.__len__())
for i in range(tgen.__len__()):
    rn_preds = test_model.predict_on_batch(next(datas))
    progbar.add(1)
    anchors_pred, _ = bb_c3_16.convert_box_to_anc(rn_preds, iou_nms=0.3)
    gtruth = {j: t[j][i * 16:(i + 1) * 16] for j in t.keys()}
    anchors_true, _ = bb_c3_16.convert_box_to_anc(gtruth)

    curr = []
    for pred, true in zip(anchors_pred, anchors_true):
        for p in pred:
            iou = bb_c3_16.calculate_ious(box=p, anchors=true)
            if iou.size > 0:
                curr.append(np.max(iou))
            else:
                curr.append(0)

    if len(curr) == 0:
        curr = [0]

    ious['med'].append(np.median(curr))
    ious['p25'].append(np.percentile(curr, 25))
    ious['p75'].append(np.percentile(curr, 75))
dfiou = pd.DataFrame(index=np.arange(ious['med'].size))
dfiou['iou_median'] = ious['med']
dfiou['iou_p-25th'] = ious['p25']
dfiou['iou_p-75th'] = ious['p75']

print(dfiou['iou_median'].median())
print(dfiou['iou_p-25th'].median())
print(dfiou['iou_p-75th'].median())

ious = {k: np.array(v) for k, v in ious.items()}
enqueuer.stop()
