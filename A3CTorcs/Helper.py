import tensorflow as tf
import numpy as np
import scipy.signal
import moviepy.editor as mpy
# from skimage.color import rgb2grey
from matplotlib import pyplot as plt
# Copies one set of variables to another.
# Used to set worker network parameters to those of global network.
def update_target_graph(from_scope, to_scope):
    from_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, from_scope)
    to_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, to_scope)

    op_holder = []
    for from_var, to_var in zip(from_vars, to_vars):
        op_holder.append(to_var.assign(from_var))
    return op_holder


# Processes Doom screen image to produce cropped and resized image.
def process_frame(frame):
    #s = frame[10:-10, 30:-30]
    #s = scipy.misc.imresize(s, [64, 64])  #TODO CHANGED For resizing.
    s = np.reshape(frame, [np.prod(frame.shape)]) / 255.0
    return s


# Discounting function used to calculate discounted returns.
def reScale(img):
    return scipy.misc.imresize(img, [84, 84])


def discount(x, gamma):
    return scipy.signal.lfilter([1], [1, -gamma], x[::-1], axis=0)[::-1]


# Used to initialize weights for policy and value output layers
def normalized_columns_initializer(std=1.0):
    def _initializer(shape, dtype=None, partition_info=None):
        out =np.random.randn(*shape).astype(np.float32)
        out *= std / np.sqrt(np.square(out).sum(axis=0, keepdims=True))
        return tf.constant(out)

    return _initializer


# This code allows gifs to be saved of the training episode for use in the Control Center.
def make_gif(images, fname, duration=2, true_image=False, salience=False, salIMGS=None):
    def make_frame(t):
        try:
            x = images[int(len(images) / duration * t)]
        except:
            x = images[-1]

        if true_image:
            return x.astype(np.uint8)
        else:
            return ((x + 1) / 2 * 255).astype(np.uint8)

    def make_mask(t):
        try:
            x = salIMGS[int(len(salIMGS) / duration * t)]
        except:
            x = salIMGS[-1]
        return x

    clip = mpy.VideoClip(make_frame, duration=duration)
    if salience == True:
        mask = mpy.VideoClip(make_mask, ismask=True, duration=duration)
        clipB = clip.set_mask(mask)
        clipB = clip.set_opacity(0)
        mask = mask.set_opacity(0.1)
        mask.write_gif(fname, fps=len(images) / duration, verbose=False)
        # clipB.write_gif(fname, fps = len(images) / duration,verbose=False)
    else:
        clip.write_gif(fname, fps=len(images) / duration, verbose=False)


# def rgb2grey(img):
#     img=np.array([2,64])
#     avgGray=(np.dot(img[...,:3],[0.333,0.333,0.333]))
#     img = np.ndarray((64, 64, 3))
#     for i in range(3):
#         img[:, :, i] = 255 - vision[:, i].reshape((64, 64))
#     lum=(np.dot(img[...,:3],[0.299,0.717,0.114]))
#     lum = np.reshape(lum, [np.prod(lum.shape)])
#     #return avgGray
#     return lum

def rgb2grey(vision):

    img_grey = np.ndarray([64, 64])
    vision=torcsImage(vision)
    for i in range(3):
        img_grey += vision[:, :, i]
    img_grey = img_grey / 3

    img_grey = np.round(img_grey, 0)
    np.clip(img_grey, 0, 255, out=img_grey)
    img_grey = img_grey.astype('uint8')

    return img_grey    # # [x, y, z]
    # vision=vision.reshape(160,120,3)
    # lum = np.dot((vision[:,:,:3]),[0.299, 0.717, 0.114])
    # return lum
def torcsImage(vision):
    img = np.ndarray((64, 64, 3))
    for i in range(3):
        img[:, :, i] =vision[:, i].reshape((64, 64))
    img=img[::-1]
    '''plt.imshow(img)
    plt.draw();
    plt.pause(0.01)'''
    return img

def normalize(value, min, max):
    return (value - min) / (max - min)

def denormalize(value, min, max):
    return (value * (max - min)) + min