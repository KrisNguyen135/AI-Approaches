import skimage
import numpy as np
import random
import matplotlib.pyplot as plt


class Game:
    def __init__(self, img_path, n_segments=3):
        self.img = skimage.io.imread(img_path)
        self.img = skimage.color.rgb2gray(self.img)

        self.n_segments = n_segments
        self.pieces = self.generate_puzzle()

    def generate_puzzle(self):
        # Resize to a square
        size = min(self.img.shape) // self.n_segments * self.n_segments
        self.img = skimage.transform.resize(self.img, (size, size),
                                            anti_aliasing=True)

        # Cut up the pieces
        segment_size = size // self.n_segments
        pieces = np.array([self.img[
                               segment_size * i: segment_size * (i + 1),
                               segment_size * j: segment_size * (j + 1)
                           ] for i in range(self.n_segments)
                           for j in range(self.n_segments)
                           ])

        # Shuffle and rotate the pieces
        np.random.shuffle(pieces)
        pieces = np.array([
            skimage.transform.rotate(piece, 90*random.randint(0, 3))
            for piece in pieces
        ])

        return pieces

    def visualize_solution(self, solution, output=None):
        indices, orientations = solution

        print(indices)
        print(orientations)

        f, ax = plt.subplots(self.n_segments, self.n_segments,
                             figsize=(5, 5),
                             gridspec_kw={'wspace': 0, 'hspace': 0})

        for row in range(self.n_segments):
            for col in range(self.n_segments):
                ax[row, col].imshow(
                    skimage.transform.rotate(
                        self.pieces[indices[row, col]],
                        -90 * orientations[indices[row, col]]
                    ),
                    cmap='gray'
                )
                ax[row, col].set_xticklabels([])
                ax[row, col].set_yticklabels([])

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()

        if output is not None:
            f.savefig(output)
