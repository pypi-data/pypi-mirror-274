import os

import matplotlib.pyplot as plt
import skimage.io

import biondi
import openslide
import numpy as np
import re
import tensorflow.keras as keras
from tensorflow.keras import layers, models, losses, Model, Input
import sqlite3
import pickle
import tensorflow as tf
import pandas as pd
import h5py
import scipy
from sklearn.neighbors import KDTree
import json, PIL

def tile_sample_hdf5_generator_v3_aqp1ae2_hoechst(wsi_filename, aqp1ae2=False, im_size=1024, sample_size=100, name=None,
                                                  half_res=False, save_path=None, sample_num=None):
    if name:
        if name == 'HE':
            wsi_name = re.search('(^.*?) ', os.path.basename(wsi_filename)).group(1) + '_H&E'
            if half_res:
                wsi_name = wsi_name + '_20x'
        else:
            wsi_name = name
    else:
        wsi_name = re.search('(^.*?) ', os.path.basename(wsi_filename)).group(1)
    filename = wsi_name + '_tile_sample_'
    if save_path:
        sp = save_path
    else:
        sp = ''
    previous_metadata = glob.glob(sp + filename + '*.hdf5')
    max_previous = max([int(re.search('sample_(.{1,2}?).hdf5', i).group(1)) for i in previous_metadata] + [0])
    full_filename = sp + filename + str(sample_num or max_previous + 1) + '.hdf5'
    wsi = openslide.open_slide(wsi_filename)
    dim = wsi.dimensions
    grid_height = dim[1] // im_size
    grid_width = dim[0] // im_size
    im_num = grid_height * grid_width
    if max_previous == 0:
        p = np.random.permutation(im_num)
    else:
        f_old = h5py.File(sp + filename + '1.hdf5', 'r')
        p = f_old['full_randomized_tile_indices']
    tile_stack = []
    for index in p[:sample_size * (sample_num or max_previous + 1)]:
        # determine row in WSI
        i = index // grid_width
        # determine column in WSI
        j = index % grid_width
        a = wsi.read_region((j * im_size, i * im_size), 0, (im_size, im_size))
        if aqp1ae2:
            tile_stack.append(np.concatenate([np.array(a)[:, :, :-2], np.zeros((im_size, im_size, 1),dtype='uint8')], axis=-1))
        else:
            tile_stack.append(np.concatenate([np.zeros((im_size, im_size, 1), dtype='uint8'), np.array(a)[:, :, 1:-1]], axis=-1))
    tile_stack = np.stack(tile_stack, axis=0)
    if half_res:
        model = biondi.dataset.half_tile_resolution(im_size)
        tile_stack = model.predict(tile_stack)
    f = h5py.File(full_filename, 'w')
    dset1 = f.create_dataset('images', data=tile_stack.astype('uint8'))
    dset2 = f.create_dataset('rows-columns', data=np.array([grid_height, grid_width]))
    dset3 = f.create_dataset('tile_index', data=p[:sample_size * (sample_num or max_previous + 1)])
    dset4 = f.create_dataset('full_randomized_tile_indices', data=p)
    print('Saved as:', full_filename)











def wsi_mosaic_start_stop_slices_cpecs(counter, grid_size, imsize, im_separation):
    r = counter // grid_size
    c = counter % grid_size
    r_start = (imsize+im_separation) * r
    r_stop = (imsize+im_separation) * r + imsize
    c_start = (imsize+im_separation) * c
    c_stop = (imsize+im_separation) * c + imsize
    return r_start, r_stop, c_start, c_stop


def classification_QC(case_name, wsi, coords, predictions, code_name=None, grid_size=10, im_size=128, im_separation=5, marker_length=20, marker_thickness=2, save_dir='', return_im=False):
    # Merge coords and predictions into 1 array so that it is easier to keep track.
    coords_and_preds = np.concatenate([coords, np.expand_dims(predictions, axis=-1)], axis=1)
    # Calculates the prevalence of the case. Will be used to determine how many positive and negative cells to sample.
    positive_class_count = np.sum(coords_and_preds[:,2])
    negative_class_count = np.sum(coords_and_preds[:,2]==0)
    prevalence  = positive_class_count/(positive_class_count+negative_class_count)
    # Calculates the exact number of positive and negative cells to samples based on prevalence and size of the grid.
    positive_cells = int(np.round(grid_size**2 * prevalence))
    # Adjusts the # of positive cells so that at least 1 positive and 1 negative cells are include in the sampling.
    if positive_cells == 0:
        positive_cells = 1
    elif positive_cells == grid_size**2:
        positive_cells = grid_size**2 -1
    negative_cells = grid_size**2 - positive_cells
    # Randomly samples the desired amount of positive and negative cells from the coordinates
    random_positive_indices = np.random.permutation(positive_class_count)[:positive_cells]
    positive_coords = coords_and_preds[coords_and_preds[:,2]==1][random_positive_indices]
    random_negative_indices = np.random.permutation(negative_class_count)[:negative_cells]
    negative_coords = coords_and_preds[coords_and_preds[:,2]==0][random_negative_indices]
    # Merge positive and negative coords and shuffle
    combined_random_coords_and_preds = np.concatenate([positive_coords, negative_coords], axis=0)
    p = np.random.permutation(len(combined_random_coords_and_preds)) # indicies for shuffling
    combined_random_coords_and_preds = combined_random_coords_and_preds[p]

    # Get CPEC images from wsi file
    cells = biondi.dataset.wsi_cell_extraction_from_coords_v3(wsi, im_size=im_size,
                                                              coords=combined_random_coords_and_preds[:,:2], verbose=0)

    # Generate empty(white) array for the image grid
    grid_length = (im_size + im_separation)*grid_size # length in pixels of each side of the image grid
    grid = np.full((grid_length, grid_length, 3,), 255,dtype=np.uint8)

    # Generate cross-shaped marker boolean mask to add a white cross to the cell of interest in each CPEC image
    # This will be done by making a mask that will leave.............
    cross_mask = np.full((marker_length, marker_length), False, dtype=bool)
    # Adding horizontal bar
    cross_mask[(marker_length//2)-(marker_thickness//2):(marker_length//2)+(marker_thickness//2),:] = True
    # Adding vertical bar
    cross_mask[:,(marker_length//2)-(marker_thickness//2):(marker_length//2)+(marker_thickness//2)] = True
    # Padding with False values to achieve same final dimensions as a CPEC image
    cross_mask = np.pad(cross_mask, (im_size-marker_length)//2, mode='constant', constant_values=False)

    # Start loop for adding CPEC images to the grid
    for i in range(len(cells)):
        # Get slices for where to add image
        r_start, r_stop, c_start, c_stop = wsi_mosaic_start_stop_slices_cpecs(i, grid_size=grid_size, imsize= im_size,
                                                                              im_separation=im_separation)
        # Add number label to top-left corner of CPEC image
        numbered_cell = Image.fromarray(cells[i])
        ImageDraw.Draw(numbered_cell).text((0+1,0), str(i+1), (255,255,0))
        grid[r_start:r_stop, c_start:c_stop, :] = np.array(numbered_cell) # Add image into grid
        grid[r_start:r_stop, c_start:c_stop, :][cross_mask] = 255 # Use cross_mask to add white cross to the image
    metadata = {'case': case_name,
                'code_name': code_name,
                'coords': combined_random_coords_and_preds[:,:2],
                'predictions': combined_random_coords_and_preds[:,2]}
    if code_name:
        with open(save_dir + f'Case-{code_name} classification quality control samples of cells metadata.pickle','wb') as handle:
            pickle.dump(metadata, handle)
        skimage.io.imsave(save_dir+f'Case-{code_name} classification quality control samples of cells image grid.tif', grid)

    else:
        with open(save_dir+f'{case_name} classification quality control samples of cells metadata.pickle','wb') as handle:
            pickle.dump(metadata, handle)
        skimage.io.imsave(save_dir+f'{case_name} classification quality control samples of cells image grid.tif', grid)
    if return_im:
        return grid


def batch_BB_binary_masks_from_geoJSON(file_list, show_mask=True):
    masks = []
    for i in file_list:
        # load geoJSON file
        with open(i) as f:
            jdata = json.load(f)
        print(os.path.basename(i))
        # create empty image to draw segmentations.
        img = PIL.Image.new('L', (690, 690), 0)
        # iterate through geometry objects that are Biondi bodies and draw them on the empty image
        for j in jdata['features']:
            cls_name = j['properties']['classification']['name']
            if cls_name == 'Biondi body' or cls_name == 'biondi bodies' or cls_name == 'Bondi Bodies':
                # Segmentations with holes in them have multiple arrays of "Polygons" rather than just 1.
                # The first polygon is the most outer surface of the segmentation, and all subsequent polygons are the
                # empty regions/holes. The below code should work for polygons with or without holes.
                if j['geometry']['type'] == 'Polygon':
                    for l, m in enumerate(j['geometry']['coordinates']):
                        if l == 0:
                            PIL.ImageDraw.Draw(img).polygon([tuple(k) for k in m], outline=1, fill=1)
                        else:
                            PIL.ImageDraw.Draw(img).polygon([tuple(k) for k in m], outline=1, fill=0)
                # Segmentations with that have multiple separate objects in them are multipolygons and are an array of
                # individual "Polygons". The individual polygons are formatted similarly to normal polygons and may have
                # multiple arrays if holes are present.
                elif j['geometry']['type'] == 'MultiPolygon':
                    for n in j['geometry']['coordinates']:
                        for l, m in enumerate(n):
                            if l == 0:
                                PIL.ImageDraw.Draw(img).polygon([tuple(k) for k in m], outline=1, fill=1)
                            else:
                                PIL.ImageDraw.Draw(img).polygon([tuple(k) for k in m], outline=1, fill=0)
        masks.append(np.array(img))
        if show_mask:
            plt.figure(figsize=(25,25))
            plt.imshow(img)
            plt.show()
    masks = np.array(masks)
    return masks













class OncocyteTrainingGenerator(keras.utils.Sequence):
    def __init__(self,
                 data1,
                 data2,
                 batch_size,
                 labels=None,
                 normalize=True,
                 per_channel=False,
                 validation=False,
                 flip=False,
                 rotation=False,
                 contrast=False,
                 c_factor=0.9,
                 r_factor=0.4,
                 prediction=False, ):
        self.batch_size = batch_size
        self.normalize = normalize
        self.per_channel = per_channel
        self.validation = validation
        self.prediction = prediction
        self.flip = flip
        if self.flip:
            # will likely need to update this code when moving to a newer version of TF/Keras
            self.flipper = keras.layers.experimental.preprocessing.RandomFlip()
        self.rotation = rotation
        self.r_factor = r_factor
        if self.rotation:
            # will likely need to update this code when moving to a newer version of TF/Keras
            self.rotator = keras.layers.experimental.preprocessing.RandomRotation(self.r_factor)
        self.contrast = contrast
        self.c_factor = c_factor
        if self.contrast:
            # will likely need to update this code when moving to a newer version of TF/Keras
            self.contraster = keras.layers.experimental.preprocessing.RandomContrast(self.c_factor)
        if type(data1) is str:
            if '.pickle' in data1:
                with open(data1, 'rb') as handle:
                    self.data1 = pickle.load(handle)
            elif '.npy' in data1:
                self.data1 = np.load(data1)
                if self.data1.ndim != 4:
                    self.data1 = np.squeeze(self.data1)
                    if self.data1.ndim != 4:
                        raise ValueError(f"Data ndim is {self.data1.ndim}. Data needs to have either 4 or 5 dimensions.")
            else:
                raise ValueError('Warning: Filetype is not recognized. Only ".pickle" and ".npy" filetypes are supported.')
        else:
            if self.retinanet:
                self.data1 = data1
            else:
                if data1.ndim == 5:
                    self.data1 = np.squeeze(data1)
                else:
                    self.data1 = data1
        if type(data2) is str:
            if '.pickle' in data2:
                with open(data2, 'rb') as handle:
                    self.data2 = pickle.load(handle)
            elif '.npy' in data2:
                self.data2 = np.load(data2)
                if self.data2.ndim != 4:
                    self.data2 = np.squeeze(self.data2)
                    if self.data2.ndim != 4:
                        raise ValueError(f"Data ndim is {self.data2.ndim}. Data needs to have either 4 or 5 dimensions.")
            else:
                raise ValueError('Warning: Filetype is not recognized. Only ".pickle" and ".npy" filetypes are supported.')
        else:
            if self.retinanet:
                self.data2 = data2
            else:
                if data2.ndim == 5:
                    self.data2 = np.squeeze(data2)
                else:
                    self.data2 = data2
        if self.retinanet:
            self.sample_number1 = len(self.data1['dat'])
            self.keys = self.data1.keys()
            self.data1['dat'] = np.squeeze(self.data1['dat'])
        else:
            self.sample_number1 = len(self.data1)
            self.sample_number2 = len(self.data2)
            if labels is not None:
                if type(labels) is str:
                    self.labels = np.load(labels)
                else:
                    self.labels = labels
            else:
                print('Warning: Must provide labels!')
                return
        if self.two_channel:
            self.c_idx_start = 1
        else:
            self.c_idx_start = 0
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(self.sample_number1 / self.batch_size))

    def __getitem__(self, index):
        batch_idx = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        x1_batch = self.data1[batch_idx, ..., self.c_idx_start:]
        p = np.random.choice(self.sample_number2, size=self.batch_size)
        x2_batch = self.data2[p, ..., self.c_idx_start:]
        p2 = np.random.permutation(self.batch_size*2)
        x_batch = np.concatenate([x1_batch,x2_batch], axis=0)[p2]
        y_batch = np.concatenate([np.ones(shape=(self.batch_size,)), np.zeros(shape=(self.batch_size,))])[p2]
        if self.flip and not self.validation:
            x_batch = self.flipper(x_batch).numpy()
        if self.rotation and not self.validation:
            x_batch = self.rotator(x_batch).numpy()
        if self.contrast and not self.validation:
            x_batch = self.contraster(x_batch).numpy()

        if self.normalize:
            x_batch = biondi.dataset.per_sample_tile_normalization(x_batch, per_channel=self.per_channel)
        x_batch = np.expand_dims(x_batch, axis=1)
        if self.prediction:
            return x_batch
        else:
            return x_batch, y_batch

    def on_epoch_end(self):
        if self.validation:
            self.indexes = np.arange(self.sample_number1)
        else:
            # not necessary since keras shuffles the index it gives __getitem__()
            # self.indexes = np.random.permutation(self.sample_number)
            self.indexes = np.arange(self.sample_number1)


def custom_unet2(inputs, filter_ratio=1, logits_num=2, num_layers=6, class_num=1, _3d=False):
    # --- Define kwargs dictionary
    if _3d:
        kwargs = {
            'kernel_size': (3, 3, 3),
            'padding': 'same'}
    else:
        kwargs = {
            'kernel_size': (1, 3, 3),
            'padding': 'same'}

    # --- Define lambda functions
    conv = lambda x, filters, strides: layers.Conv3D(filters=filters,
                                                     strides=strides,
                                                     **kwargs)(x)
    norm = lambda x: layers.BatchNormalization()(x)
    relu = lambda x: layers.LeakyReLU()(x)
    tran = lambda x, filters, strides: layers.Conv3DTranspose(filters=filters,
                                                              strides=strides,
                                                              **kwargs)(x)

    # --- Define stride-1, stride-2 blocks
    conv1 = lambda filters, x: relu(norm(conv(x, filters, strides=1)))
    conv2 = lambda filters, x: relu(norm(conv(x, filters, strides=(1, 2, 2))))
    tran2 = lambda filters, x: relu(norm(tran(x, filters, strides=(1, 2, 2))))

    # --- Define simple layers
    c_layer = lambda filters, x: conv1(filters, conv2(filters, x))
    e_layer = lambda filters1, filters2, x: tran2(filters1, conv1(filters2, x))

    contracting_layers = []
    for i in range(num_layers):  # 0,1,2,3,4,5
        if i == 0:
            contracting_layers.append(conv1(int(4*filter_ratio), inputs))
        else:
            contracting_layers.append(c_layer(int(8*filter_ratio)*i, contracting_layers[i-1]))
    expanding_layers = []
    for j in reversed(range(num_layers-1)):  # 4,3,2,1,0
        if j == num_layers-2:
            expanding_layers.append(tran2(int(8*filter_ratio)*j, contracting_layers[j+1]))
        else:
            expanding_layers.append(e_layer(int(8*filter_ratio)*j if j != 0 else int(4*filter_ratio),
                                            int(8*filter_ratio)*(j+1),
                                            expanding_layers[-1] + contracting_layers[j+1]))
    last_layer = conv1(int(4*filter_ratio),
                       conv1(int(4*filter_ratio), expanding_layers[-1] + contracting_layers[0]))

    # --- Create logits
    logits = {}
    for k in range(class_num):
        logits[f'zones{k}'] = layers.Conv3D(filters=logits_num, name=f'zones{k}', **kwargs)(last_layer)

    # --- Create model
    if class_num > 1:
        model = Model(inputs=inputs, outputs=logits)
    else:
        model = Model(inputs=inputs, outputs=logits)
    return model

def cpec_masks(hdf5, cell, nucleus):
    tiles = []
    cell_pts = pd.read_csv(cell).to_numpy()[:, 1:6]
    nucleus_pts = pd.read_csv(nucleus).to_numpy()[:, 1:6]
    #hyalinized_pts = pd.read_csv(hyalinized).to_numpy()[:, 1:6]
    #mineralized_pts = pd.read_csv(mineralized).to_numpy()[:, 1:6]
    real_tile_indices = pd.read_csv(cell).to_numpy()[:, 5]
    unique_tile_indices = np.unique(real_tile_indices)
    with h5py.File(hdf5, 'r') as handle:
        coords = handle['coords'][:]
        wsi_path = str(handle['wsi_path'][...].astype(str))
    unique_coords = coords[unique_tile_indices]
    images = biondi.dataset.wsi_cell_extraction_from_coords_v3(wsi_path, 128, unique_coords, verbose=0)
    tile_num = len(unique_tile_indices)
    counter = 0
    # model = biondi.dataset.half_tile_resolution(4096)
    for i in range(tile_num):
        tile_pts = [
            cell_pts[cell_pts[:, -1] == unique_tile_indices[i]],
            nucleus_pts[nucleus_pts[:, -1] == unique_tile_indices[i]],
        ]
        cell_mask = biondi.dataset.generate_mask_quarterres_v2(tile_pts[0], cellmask=True)
        nucleus_mask = biondi.dataset.generate_mask_quarterres_v2(tile_pts[1], cellmask=True)
        tiles.append(np.concatenate([images[i],
                                     np.stack([cell_mask, nucleus_mask], axis=-1)],
                                    axis=2))
        counter += 1
        print(counter, 'out of', tile_num)
    return np.stack(tiles)


def kolmogorov_smirnov_statistic_for_wsi_montecarlo_simulations(obs_pa, simulated_pa,
                                                                observed_only=False, test_observed=False,
                                                                workers=16, max_queue_size=128, verbose=1):
    # Todo: add option to provide variable instead of filename
    KSG = KSgenerator(obs_pa, simulated_pa)
    enqueuer = keras.utils.OrderedEnqueuer(KSG)
    enqueuer.start(workers=workers, max_queue_size=max_queue_size)
    if test_observed:
        obs_dvalue, obs_pvalue = scipy.stats.ks_2samp(KSG.observed, KSG.obs_and_sims)
        print('Observed data D-value:', obs_dvalue, 'Observed data P-value:', obs_pvalue)
        if observed_only:
            return obs_dvalue, obs_pvalue

    sim_dpvalues = []
    datas = enqueuer.get()
    progbar = keras.utils.Progbar(KSG.__len__(), verbose=verbose)
    for i in range(KSG.__len__()):
        sim_dpvalues.append(next(datas))
        progbar.add(1)
    enqueuer.stop()
    if test_observed:
        return obs_dvalue, obs_pvalue, sim_dpvalues
    else:
        return sim_dpvalues


class KSgenerator(keras.utils.Sequence):
    def __init__(self, obs_pa, simulated_pa):
        if type(obs_pa) is str:
            self.observed = np.load(obs_pa)
        else:
            self.observed = obs_pa
        if type(simulated_pa) is str:
            self.simulations = np.load(simulated_pa)
        else:
            self.simulations = simulated_pa
        self.obs_and_sims = np.concatenate([np.expand_dims(self.observed, axis=0), self.simulations]).flatten()
        self.indexes = np.arange(len(self.simulations))

    def __len__(self):
        return int(len(self.simulations))

    def __getitem__(self, index):
        d, p = scipy.stats.ks_2samp(self.simulations[index], self.obs_and_sims)
        return d, p


def local_density_simulations(affected, total, iterations, radius=310.559, workers=16, max_queue_size=128, verbose=1):
    MCG = MCgenerator(affected=affected, total=total, iterations=iterations, radius=radius)
    enqueuer = keras.utils.OrderedEnqueuer(MCG)
    enqueuer.start(workers=workers, max_queue_size=max_queue_size)

    simulated_densities = []
    datas = enqueuer.get()
    progbar = keras.utils.Progbar(MCG.__len__(), verbose=verbose)
    for i in range(MCG.__len__()):
        simulated_densities.append(next(datas))
        progbar.add(1)
    enqueuer.stop()
    simulated_densities = np.stack(simulated_densities, axis=0)
    return simulated_densities


class MCgenerator(keras.utils.Sequence):
    def __init__(self, affected, total, iterations, radius):
        self.total = total
        self.affected = affected
        self.iterations = iterations
        self.radius = radius
        self.positive_count = len(affected)
        self.total_count = len(total)

    def __len__(self):
        return int(self.iterations)

    def __getitem__(self, index):
        p = np.random.permutation(self.total_count)
        sim_affected = self.total[p[:self.positive_count]]
        affected_tree = KDTree(sim_affected)
        total_tree = KDTree(self.total)
        nearby_affected = affected_tree.query_radius(self.total, r=self.radius, count_only=True)
        nearby_total = total_tree.query_radius(self.total, r=self.radius, count_only=True)
        density = nearby_affected / nearby_total
        return density


def percent_affected(total_cpec_coords, affected_cpec_coords, density=False, radius=310.559):
    """
    Returns a list of percent affected values (within a given radius) for
    use in applying a heatmap to a scatterplot.

    Keyword arguments:
    total_cpec_coords -- a 2D array of all CPEC coordinates
    affected_cpec_coords -- a 2D array of affected CPEC coordinates
    radius -- radius to calculate percent of affected CPEC (default 310.559)
    """
    ac = KDTree(affected_cpec_coords)
    tc = KDTree(total_cpec_coords)

    total = tc.query_radius(total_cpec_coords, r=radius, count_only=True)
    affected = ac.query_radius(total_cpec_coords, r=radius, count_only=True)
    percentage_affected = affected / total
    for i in range(len(percentage_affected)):
        if percentage_affected[i] > 1:
            percentage_affected[i] = 1
    if density:
        return percentage_affected, total
    else:
        return percentage_affected


    ####################################
    ###image tiler for image blurring###
    ####################################
    class ImageTiler(keras.utils.Sequence):
        def __init__(self, image, tile_size, stride=1, kernel_size=311, batch_size=1):
            self.image = image
            self.image_shape = np.squeeze(self.image).shape
            self.tile_size = tile_size
            self.stride = stride
            self.kernel_size = kernel_size
            self.padded_tile_size = self.tile_size + (self.kernel_size-1)*2
            self.batch_size = batch_size
            self.tile_count = (self.image_shape[0] // self.tile_size) * (self.image_shape[1] // self.tile_size)
            self.idx_number = int(np.ceil(self.tile_count / self.batch_size))
            self.column_num = self.dim[0] // self.im_size

        def __len__(self):
            return self.idx_number


        def __getitem__(self, idx):
            batch = []
            rstatusb = []
            cstatusb = []
            rrawb = []
            crawb = []
            r = idx // self.image_shape[1]
            c = idx % self.image_shape[1]
            r_raw = (r*self.tile_size)
            c_raw = (c*self.tile_size)
            r_start = r_raw-(self.kernel_size-1)
            r_stop = r_raw+self.tile_size+(self.kernel_size-1)
            c_start = c_raw-(self.kernel_size-1)
            c_stop = c_raw+self.tile_size+(self.kernel_size-1)
            if r_start<0:
                r_start=0
                rstatus = True
            else:
                rstatus = False
            if c_start<0:
                c_start=0
                cstatus = True
            else:
                cstatus = False
            return self.image[r_start:r_stop, c_start:c_stop], rstatus, cstatus, r_raw, c_raw

def get_burred(tiler_obj, model, padding=310, tile_size=1024, return_merged=True):
    max_iter = tiler_obj.idx_number
    trimmed_tiles = []
    r_raws = []
    c_raws = []
    enqueuer = keras.utils.OrderedEnqueuer(tiler_obj)
    enqueuer.start(workers=12, max_queue_size=128)
    datas = enqueuer.get()
    progbar = keras.utils.Progbar(tiler_obj.__len__(), verbose=1)
    for i in range(max_iter):
        data = next(datas)
        blurred_tile = model.predict(np.expand_dims(data[0], axis=(0, -1)))
        if data[1] == True:
            r_trim = 0
        else:
            r_trim = 310
        if data[2] == True:
            c_trim = 0
        else:
            c_trim = 310
        r_raws.append(data[3])
        c_raws.append(data[4])
        trimmed_tiles.append(np.squeeze(blurred_tile)[r_trim:r_trim+tile_size, c_trim:c_trim+1024])
        progbar.add(1)
    if return_merged:
        merged = np.zeros(shape = tiler_obj.image_shape)
        for i,j,k in zip(trimmed_tiles, r_raws, c_raws):
            merged[j:j+tile_size,k:k+tile_size] = i
        return merged
    else:
        return trimmed_tiles