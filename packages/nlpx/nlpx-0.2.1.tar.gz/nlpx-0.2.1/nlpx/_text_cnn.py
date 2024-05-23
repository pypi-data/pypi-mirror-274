import torch
from typing import Collection
from torch import nn
from torch.nn import functional as F


class TextCNN(nn.Module):

    def __init__(self, word_dim: int, cnn_out_channels: int, cnn_kernel_sizes: Collection[int], num_classes: int,
                 drop_out=None):
        """ TextCNN model
        Parameters
        ----------
        word_dim:
        cnn_out_channels:
        cnn_kernel_sizes:
        num_classes:
        drop_out:

        Examples
        --------
        >>> import torch
        >>> from nlpx.models import TextCNN
        >>> X = torch.randn(batch_size, 10, word_dim)
        >>> targets = torch.randint(0, num_classes, (batch_size,))
        >>> model = TextCNN(word_dim, cnn_out_channels=64, cnn_kernel_sizes=(2, 3, 4), num_classes=num_classes)
        >>> output = model(X)
        >>> loss, output = model(X, targets)
        """
        super().__init__()
        self.convs = nn.ModuleList([
            nn.Sequential(
                nn.Conv1d(in_channels=word_dim, out_channels=cnn_out_channels, kernel_size=kernel_size, bias=False),
                nn.ReLU(inplace=True),  # inplace为True，将会改变输入的数据 ，否则不会改变原输入，只会产生新的输出
                nn.AdaptiveMaxPool1d(1)
            ) for kernel_size in cnn_kernel_sizes
        ])
        self.fc = nn.Linear(in_features=cnn_out_channels * len(cnn_kernel_sizes), out_features=num_classes)
        self.dropout = nn.Dropout(drop_out) if drop_out else None

    def forward(self, inputs, labels=None):
        """
        :param inputs: [(batch, sentence, word_dim)]
        :param labels: [long]
        """
        input_embeddings = inputs.transpose(2, 1)
        out = torch.cat([conv(input_embeddings) for conv in self.convs], dim=1)
        out = out.transpose(2, 1)

        if self.dropout:
            out = self.dropout(out)

        out = self.fc(out)
        logits = out.squeeze(1)

        if labels is None:
            return logits
        else:
            loss = F.cross_entropy(logits, labels)
            return loss, logits
