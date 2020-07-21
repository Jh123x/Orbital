# from ai_invader.model.CNN2D import Conv2DImproved
import numpy as np
import pygad.cnn as cnn
from scipy.signal import convolve2d
class Conv2DImproved(cnn.Conv2D):
    def __init__(self,num_filters, kernel_size, previous_layer, activation_function=None):
        super(Conv2DImproved,self).__init__(num_filters,kernel_size,previous_layer,activation_function)

    def conv_(self, input2D, conv_filter):
        result = np.zeros(shape=(input2D.shape[0]-self.kernel_size+1, input2D.shape[1]-self.kernel_size+1, conv_filter.shape[0]))
        input2D = np.squeeze(input2D)
        for filter_idx in range(conv_filter.shape[0]):
            # for each filter in the stack of filters
            filt = np.squeeze(conv_filter[filter_idx], 2)
            # squeeze last axis of filter off for scipy
            #print(filt.shape)
            #print(input2D.shape)
            conv = convolve2d(input2D,filt,boundary='symm', mode='valid')
            result[:,:,filter_idx]= conv

        final_result = result[np.uint16(self.filter_bank_size[1] / 2.0):result.shape[0] - np.uint16(
                                self.filter_bank_size[1] / 2.0),
                                np.uint16(self.filter_bank_size[1] / 2.0):result.shape[1] - np.uint16(
                                self.filter_bank_size[1] / 2.0), :]

        # result = np.zeros(shape=(input2D.shape[0], input2D.shape[1], conv_filter.shape[0]))
        # # Looping through the image to apply the convolution operation.
        # img_row = np.uint16(np.arange(self.filter_bank_size[1] / 2.0,
        #                                    input2D.shape[0] - self.filter_bank_size[1] / 2.0 + 1))
        # img_col = np.uint16(np.arange(self.filter_bank_size[1] / 2.0,
        #                                        input2D.shape[1] - self.filter_bank_size[1] / 2.0 + 1))
        #
        # for r in img_row:
        #     for c in img_col:
        #         """
        #         Getting the current region to get multiplied with the filter.
        #         How to loop through the image and get the region based on
        #         the image and filer sizes is the most tricky part of convolution.
        #         """
        #         if len(input2D.shape) == 2:
        #             curr_region = input2D[
        #                           r - np.uint16(np.floor(self.filter_bank_size[1] / 2.0)):r + np.uint16(
        #                               np.ceil(self.filter_bank_size[1] / 2.0)),
        #                           c - np.uint16(np.floor(self.filter_bank_size[1] / 2.0)):c + np.uint16(
        #                               np.ceil(self.filter_bank_size[1] / 2.0))]
        #         else:
        #             curr_region = input2D[
        #                           r - np.uint16(np.floor(self.filter_bank_size[1] / 2.0)):r + np.uint16(
        #                               np.ceil(self.filter_bank_size[1] / 2.0)),
        #                           c - np.uint16(np.floor(self.filter_bank_size[1] / 2.0)):c + np.uint16(
        #                               np.ceil(self.filter_bank_size[1] / 2.0)), :]
        #         # Element-wise multipliplication between the current region and the filter.
        #
        #         for filter_idx in range(conv_filter.shape[0]):
        #             curr_result = curr_region * conv_filter[filter_idx]
        #             conv_sum = np.sum(curr_result)  # Summing the result of multiplication.
        #
        #             if self.activation is None:
        #                 result[r, c, filter_idx] = conv_sum  # Saving the SOP in the convolution layer feature map.
        #             else:
        #                 result[r, c, filter_idx] = self.activation(
        #                     conv_sum)  # Saving the activation function result in the convolution layer feature map.
        #
        # # Clipping the outliers of the result matrix.
        # final_result = result[np.uint16(self.filter_bank_size[1] / 2.0):result.shape[0] - np.uint16(
        #     self.filter_bank_size[1] / 2.0),
        #                np.uint16(self.filter_bank_size[1] / 2.0):result.shape[1] - np.uint16(
        #                    self.filter_bank_size[1] / 2.0), :]
        # return final_result


        
        # result[r, c, filter_idx]
        # (n_f, n_c_f,f, _) = filt.shape
        # n_c,in_dim,_ = img.shape
        # out_dim = int((in_dim-f)/s)+1
        # assert n_c == n_c_f
        # out = np.zeros((out_dim,out_dim,n_f))
        # for curr_f in range(n_f):
        #     curr_y = out_y = 0
        #     while curr_y + f <= in_dim:
        #         curr_x = out_x = 0
        #         while curr_x + f <= in_dim:
        #             out[out_y,out_x,curr_f] = np.sum(filt[curr_f]*img[:,curr_y:curr_y+f,curr_x+f]) + self.filter_bank_size[1][curr_f]
        #             curr_x+=s
        #             out_x+= 1
        #         curr_y+= 1
        #         out_y += 1
        # final_result = result[np.uint16(self.filter_bank_size[1] / 2.0):result.shape[0] - np.uint16(
        #     self.filter_bank_size[1] / 2.0),
        #                np.uint16(self.filter_bank_size[1] / 2.0):result.shape[1] - np.uint16(
        #                    self.filter_bank_size[1] / 2.0), :]
        # return out


