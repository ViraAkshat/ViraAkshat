import task2
import utils
from matplotlib import pyplot as plt
import numpy as np

tcases = utils.load('testcases.pkl')
for tcase in tcases:
    img_patches, shape, reconstructed = tcases[tcase]
    cleaned_img = task2.reconstruct_from_noisy_patches(img_patches, shape)
    #if tcase == 3 :
        #print(img_patches)
        #print(shape)
        #print(reconstructed.shape)
        #key = [(197, 207, 214, 222), (167, 207, 197, 222), (153, 207, 167, 222), (137, 207, 153, 222)]
        #for i in key:
        #        utils.make_fig(img_patches[i], cmap='gray', title='Yours')

    try:
        if np.allclose(cleaned_img, reconstructed):
            print('testcase# {} passed'.format(tcase))
            utils.make_fig(reconstructed, cmap='gray', title='Correct')
            utils.make_fig(cleaned_img, cmap='gray', title='Yours')
            plt.show()
        else:
            print('testcase# {} failed'.format(tcase))
            utils.make_fig(reconstructed, cmap='gray', title='Correct')
            utils.make_fig(cleaned_img, cmap='gray', title='Yours')
            plt.show()
    except Exception as e:
        print('testcase# {} failed'.format(tcase))