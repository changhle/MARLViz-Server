import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_packed_sequence

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class EncoderMSE(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderMSE, self).__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size)

    def forward(self, packed_input, init_hidden):
        output, hidden = self.gru(packed_input, init_hidden)
        return output, hidden


class DecoderMSE(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DecoderMSE, self).__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, packed_input, init_hidden):
        gru_output, hidden = self.gru(packed_input, init_hidden)
        # print(gru_output)
        unpacked, unpacked_len = pad_packed_sequence(gru_output, batch_first=True)
        # print(unpacked.shape)
        # print(unpacked_len.shape)
        # print(unpacked[15])
        output = self.out(unpacked)
        # print(output.shape)
        return output, hidden


class EncoderSoftmax(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(EncoderSoftmax, self).__init__()
        # input_size: 34
        # hidden_size: HyperParam.
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size)

    def forward(self, packed_input, init_hidden):
        output, hidden = self.gru(packed_input, init_hidden)
        return output, hidden


class DecoderSoftmax(nn.Module):
    def __init__(self, input_size, hidden_size, t_output_size, s_output_size):
        super(DecoderSoftmax, self).__init__()
        # input_size: 34
        # hidden_size: HyperParam.
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size)

        self.t_out = nn.Linear(hidden_size, t_output_size)
        self.so_out = nn.Linear(hidden_size, s_output_size)
        self.sd_out = nn.Linear(hidden_size, s_output_size)

    def forward(self, packed_input, init_hidden):
        gru_output, hidden = self.gru(packed_input, init_hidden)
        # print(gru_output)
        unpacked, unpacked_len = pad_packed_sequence(gru_output, batch_first=True)
        # unpacked: (batch_size, seq_length, hidden_size)

        print(unpacked.shape)
        # print(unpacked_len.shape)
        # print(unpacked[15])
        # output = self.out(unpacked)
        # print(output.shape)
        # return output, hidden


def show_plot(points):
    # plt.figure()
    fig, ax = plt.subplots()
    # 주기적인 간격에 이 locator가 tick을 설정
    loc = ticker.MultipleLocator(base=0.2)
    ax.yaxis.set_major_locator(loc)
    plt.plot(points)
