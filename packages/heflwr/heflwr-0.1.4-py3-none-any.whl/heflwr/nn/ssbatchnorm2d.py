from typing import Tuple, List, Union, Optional
from typing_extensions import Self
from fractions import Fraction

import torch
import torch.nn as nn
import torch.nn.functional as F


# For example, (0, 0.5) represents extracting the first 50%.
Interval = Tuple[str, str]
# For example, [(0, 0.2), (0.5, 0.8)] also represents extracting 50%, but at different positions.
Intervals = List[Tuple[str, str]]
Layer_Range = Union[Interval, Intervals]


class SSBatchNorm2d(nn.BatchNorm2d):
    def __init__(
            self,
            num_features: int,
            eps: float = 1e-5,
            momentum: float = 0.1,
            affine: bool = True,
            track_running_stats: bool = True,
            device=None,
            dtype=None,
            channels_ranges: Layer_Range = ('0', '1'),
    ) -> None:

        # if in_channels_ranges/out_channels_ranges belong to Interval, then convert into Intervals.
        if isinstance(channels_ranges[0], str):
            channels_ranges = [channels_ranges]

        # Convert string interval into fraction interval.
        channels_ranges = [tuple(map(self.parse_fraction_strings, range_str)) for range_str in channels_ranges]

        factory_kwargs = {'device': device, 'dtype': dtype}

        super().__init__(
            num_features=sum(int(num_features * (end - start)) for start, end in channels_ranges),
            eps=eps,
            momentum=momentum,
            affine=affine,
            track_running_stats=track_running_stats,
            **factory_kwargs
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        self._check_input_dim(input)

        # exponential_average_factor is set to self.momentum
        # (when it is available) only so that it gets updated
        # in ONNX graph when this node is exported to ONNX.
        if self.momentum is None:
            exponential_average_factor = 0.0
        else:
            exponential_average_factor = self.momentum

        if self.training and self.track_running_stats:
            # TODO: if statement only here to tell the jit to skip emitting this when it is None
            if self.num_batches_tracked is not None:  # type: ignore[has-type]
                self.num_batches_tracked.add_(1)  # type: ignore[has-type]
                if self.momentum is None:  # use cumulative moving average
                    exponential_average_factor = 1.0 / float(self.num_batches_tracked)
                else:  # use exponential moving average
                    exponential_average_factor = self.momentum

        r"""
        Decide whether the mini-batch stats should be used for normalization rather than the buffers.
        Mini-batch stats are used in training mode, and in eval mode when buffers are None.
        """
        if self.training:
            bn_training = True
        else:
            bn_training = (self.running_mean is None) and (self.running_var is None)

        r"""
        Buffers are only updated if they are to be tracked and we are in training mode. Thus they only need to be
        passed when the update should occur (i.e. in training mode when they are tracked), or when buffer stats are
        used for normalization (i.e. in eval mode when buffers are not None).
        """
        return F.batch_norm(
            x,
            # If buffers are not to be tracked, ensure that they won't be updated
            self.running_mean
            if not self.training or self.track_running_stats
            else None,
            self.running_var if not self.training or self.track_running_stats else None,
            self.weight,
            self.bias,
            bn_training,
            exponential_average_factor,
            self.eps,
        )