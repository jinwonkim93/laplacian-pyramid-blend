import cv2
import numpy as np

class LaplacianPyramidBlender:
    def laplacian_pyramid_blending_with_mask(self, src, target, mask, num_levels = 9):
        # assume mask is float32 [0,1]

        # generate Gaussian pyramid for src,target and mask
        Gsrc = src.copy()
        Gtarget = target.copy()
        Gmask = mask.copy()
        gpA = [Gsrc]
        gpB = [Gtarget]
        gpM = [Gmask]
        for i in range(num_levels):
            Gsrc = cv2.pyrDown(Gsrc)
            Gtarget = cv2.pyrDown(Gtarget)
            Gmask = cv2.pyrDown(Gmask)
            gpA.append(np.float32(Gsrc))
            gpB.append(np.float32(Gtarget))
            gpM.append(np.float32(Gmask))

        # generate Laplacian Pyramids for src,target and masks
        lpA  = [gpA[num_levels-1]] # the bottom of the Lap-pyr holds the last (smallest) Gauss level
        lpB  = [gpB[num_levels-1]]
        gpMr = [gpM[num_levels-1]]
        for i in range(num_levels-1,0,-1):
            # Laplacian: subtarct upscaled version of lower level from current level
            # to get the high frequencies
            a_row, a_col, _ = gpA[i-1].shape
            b_row, b_col, _ = gpB[i-1].shape
            LA = np.subtract(gpA[i-1], cv2.pyrUp(gpA[i], dstsize=(a_col, a_row)))
            LB = np.subtract(gpB[i-1], cv2.pyrUp(gpB[i], dstsize=(b_col, b_row)))
            lpA.append(LA)
            lpB.append(LB)
            gpMr.append(gpM[i-1]) # also reverse the masks

        # Now blend images according to mask in each level
        LS = []
        for idx, (la,lb,Gmask) in enumerate(zip(lpA,lpB,gpMr)):
            lo = lb * (1.0 - Gmask)
            if idx <= 2:
                lo += lb * Gmask
            else:
                lo +=  la * Gmask
            LS.append(lo)

        # now reconstruct
        ls_ = LS[0]
        for i in range(1,num_levels):
            row, col, _ = LS[i].shape
            ls_ = cv2.pyrUp(ls_, dstsize=(col, row))
            ls_ = cv2.add(ls_, LS[i], dtype = cv2.CV_32F)

        return ls_
    
    def __call__(self, 
                 src_image: np.ndarray,
                 target_image: np.ndarray,
                 mask_image: np.ndarray,
                 ):
        
        #normalize image to 0, 1
        mask_image = np.clip(mask_image, 0, 1)
        num_levels = int(np.log2(src_image.shape[0]))

        composite_image = self.laplacian_pyramid_blending_with_mask(src_image, target_image, mask_image, num_levels)
        composite_image = np.clip(composite_image, 0 , 255)
        return composite_image
