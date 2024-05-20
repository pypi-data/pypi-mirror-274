import random
from typing import Union

import torch
import torch.nn as nn
from torch.autograd import Variable

from .LagrangePolynomial import *
from .utils import *


class Function(nn.Module):
    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        basis,
        weight_magnitude: float = 1.0,
        periodicity: float = None,
        **kwargs,
    ):
        super().__init__()
        self.poly = basis
        self.n = n
        self.periodicity = periodicity
        self.w = torch.nn.Parameter(
            data=torch.empty(out_features, in_features, n), requires_grad=True
        )
        self.w.data.uniform_(
            -weight_magnitude / in_features, weight_magnitude / in_features
        )

        self.result = torch.nn.Parameter(
            data=torch.empty(out_features), requires_grad=True
        )

    def forward(self, x: torch.Tensor):
        periodicity = self.periodicity
        if periodicity is not None:
            x = make_periodic(x, periodicity)

        result = self.poly.interpolate(x, self.w)

        return result


class Polynomial(Function):
    def __init__(
        self, n: int, in_features: int, out_features: int, length: float = 2.0, **kwargs
    ):
        return super().__init__(
            n, in_features, out_features, LagrangePolyFlat(n, length=length), **kwargs
        )


class PolynomialProd(Function):
    def __init__(
        self, n: int, in_features: int, out_features: int, length: float = 2.0, **kwargs
    ):
        return super().__init__(
            n,
            in_features,
            out_features,
            LagrangePolyFlatProd(n, length=length),
            **kwargs,
        )


class FourierSeries(Function):
    def __init__(
        self, n: int, in_features: int, out_features: int, length: float = 2.0, **kwargs
    ):
        return super().__init__(
            n, in_features, out_features, FourierSeriesFlat(n, length=length)
        )


class Piecewise(nn.Module):
    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        segments: int,
        length: int = 2.0,
        weight_magnitude: float = 1.0,
        poly=None,
        periodicity: float = None,
        device: str = "cpu",
        **kwargs,
    ):
        super().__init__()
        self._poly = poly(n)
        self._n = n
        self._segments = segments
        self.in_features = in_features
        self.out_features = out_features
        self.periodicity = periodicity
        self.device = device
        self.w = torch.nn.Parameter(
            data=torch.empty(
                out_features, in_features, ((n - 1) * segments + 1), device=device
            ),
            requires_grad=True,
        )
        self.w.data.uniform_(
            -weight_magnitude / in_features, weight_magnitude / in_features
        )
        self.wrange = None
        self._length = length
        self._half = 0.5 * length

    def which_segment(self, x: torch.Tensor) -> Tensor:
        """
        Return the segment(s) the x are in.  This is being added for
        use with h-refinement
        Args :
            - x the input values
        Returns :
            - tensor of segment indices
        """

        periodicity = self.periodicity
        if periodicity is not None:
            x = make_periodic(x, periodicity)

        # get the segment index
        id_min = (((x + self._half) / self._length) * self._segments).long()
        device = id_min.device
        id_min = torch.where(
            id_min <= self._segments - 1,
            id_min,
            torch.tensor(self._segments - 1, device=device),
        )
        id_min = torch.where(id_min >= 0, id_min, torch.tensor(0, device=device))

        return id_min

    def x_local(self, x_global: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
        # compute x_local from x_global
        x_min = self._eta(index)
        x_max = self._eta(index + 1)

        # rescale to -1 to +1
        x_local = self._length * ((x_global - x_min) / (x_max - x_min)) - self._half
        return x_local

    def x_global(self, x_local: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
        # compute x_global from x_local
        x_min = self._eta(index)
        x_max = self._eta(index + 1)

        x_global = ((x_local + self._half) / self._length) * (x_max - x_min) + x_min
        return x_global

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        periodicity = self.periodicity
        if periodicity is not None:
            x = make_periodic(x, periodicity)

        # get the segment index
        id_min = (((x + self._half) / self._length) * self._segments).long()
        device = id_min.device
        id_min = torch.where(
            id_min <= self._segments - 1,
            id_min,
            torch.tensor(self._segments - 1, device=device),
        )
        id_min = torch.where(id_min >= 0, id_min, torch.tensor(0, device=device))
        id_max = id_min + 1

        # determine which weights are active
        wid_min = (id_min * (self._n - 1)).long()
        wid_max = (id_max * (self._n - 1)).long() + 1

        # Fill in the ranges
        wid_min_flat = wid_min.reshape(-1)
        wid_max_flat = wid_max.reshape(-1)
        wrange = wid_min_flat.unsqueeze(-1) + torch.arange(self._n, device=device).view(
            -1
        )

        windex = (
            torch.div(
                torch.arange(wrange.shape[0] * wrange.shape[1], device=device),
                self._n,
                rounding_mode="floor",
            )
            % self.in_features
        )
        wrange = wrange.flatten()

        w = self.w[:, windex, wrange]

        w = w.view(self.out_features, -1, self.in_features, self._n)
        w = w.permute(1, 2, 0, 3)

        # get the range of x in this segment
        x_min = self._eta(id_min)
        x_max = self._eta(id_max)

        # rescale to -1 to +1
        x_in = self._length * ((x - x_min) / (x_max - x_min)) - self._half

        result = self._poly.interpolate(x_in, w)
        return result

    def _eta(self, index: int):
        """
        Arg:
            - index is the segment index
        """
        eta = index / float(self._segments)
        return eta * 2 - 1

    def interpolate(
        self,
        layer_out: "Piecewise",
    ) -> None:
        interpolate_polynomial_layer(self, layer_out)

    def refine(
        self,
        layer_out: "Piecewise",
    ) -> None:
        refine_polynomial_layer(layer_in=self, layer_out=layer_out)


class PiecewisePolynomial(Piecewise):
    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        segments: int,
        length=2.0,
        weight_magnitude=1.0,
        periodicity: float = None,
        device: str = "cpu",
        **kwargs,
    ):
        super().__init__(
            n,
            in_features,
            out_features,
            segments,
            length,
            weight_magnitude,
            poly=LagrangePoly,
            periodicity=periodicity,
            device=device,
        )


class PiecewisePolynomialProd(Piecewise):
    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        segments: int,
        length=2.0,
        weight_magnitude=1.0,
        periodicity: float = None,
        device: str = "cpu",
        **kwargs,
    ):
        super().__init__(
            n,
            in_features,
            out_features,
            segments,
            length,
            weight_magnitude,
            poly=LagrangePolyProd,
            periodicity=periodicity,
            device=device,
        )


class PiecewiseDiscontinuous(nn.Module):
    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        segments: int,
        length=2.0,
        weight_magnitude=1.0,
        poly=None,
        periodicity: float = None,
        device: str = "cpu",
        **kwargs,
    ):
        super().__init__()
        self._n = n
        self.device = device
        self._poly = poly(self._n)
        self._segments = segments
        self.in_features = in_features
        self.out_features = out_features
        self.periodicity = periodicity
        self.w = torch.nn.Parameter(
            data=torch.empty(out_features, in_features, n * segments, device=device),
            requires_grad=True,
        )
        self.w.data.uniform_(-1 / in_features, 1 / in_features)

        self._length = length
        self._half = 0.5 * length

    @property
    def n(self) -> int:
        """
        The polynomial order
        """
        return self._n

    def which_segment(self, x: torch.Tensor) -> Tensor:
        """
        Return the segment(s) the x are in.  This is being added for
        use with h-refinement
        Args :
            - x the input values
        Returns :
            - tensor of segment indices
        """

        periodicity = self.periodicity
        if periodicity is not None:
            x = make_periodic(x, periodicity)

        # get the segment index
        id_min = (((x + self._half) / self._length) * self._segments).long()
        device = id_min.device
        id_min = torch.where(
            id_min <= self._segments - 1,
            id_min,
            torch.tensor(self._segments - 1, device=device),
        )
        id_min = torch.where(id_min >= 0, id_min, torch.tensor(0, device=device))
        return id_min

    def forward(self, x: torch.Tensor):
        periodicity = self.periodicity
        if periodicity is not None:
            x = make_periodic(x, periodicity)

        # determine which segment it is in
        id_min = (((x + self._half) / self._length) * self._segments).long()
        device = id_min.device
        id_min = torch.where(
            id_min <= self._segments - 1,
            id_min,
            torch.tensor(self._segments - 1, device=device),
        )
        id_min = torch.where(id_min >= 0, id_min, torch.tensor(0, device=device))
        id_max = id_min + 1

        # determine which weights are active
        wid_min = (id_min * self._n).long()
        wid_max = (id_max * self._n).long()

        # Fill in the ranges
        wid_min_flat = wid_min.flatten()
        wid_max_flat = wid_max.flatten()

        # get the range of x in this segment
        x_min = self._eta(id_min)
        x_max = self._eta(id_max)

        # rescale to -1 to +1
        x_in = self._length * ((x - x_min) / (x_max - x_min)) - self._half
        w_list = []

        wrange = wid_min_flat.unsqueeze(-1) + torch.arange(self._n, device=device).view(
            -1
        )

        # should be size batches*inputs*n
        windex = (
            torch.div(
                torch.arange(wrange.shape[0] * wrange.shape[1], device=device),
                self._n,
                rounding_mode="floor",
            )
        ) % self.in_features
        wrange = wrange.flatten()

        w = self.w[:, windex, wrange]

        w = w.view(self.out_features, -1, self.in_features, self._n)
        w = w.permute(1, 2, 0, 3)

        result = self._poly.interpolate(x_in, w)
        return result

    def x_local(self, x_global: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
        # compute x_local from x_global
        x_min = self._eta(index)
        x_max = self._eta(index + 1)

        # rescale to -1 to +1
        x_local = self._length * ((x_global - x_min) / (x_max - x_min)) - self._half
        return x_local

    def x_global(self, x_local: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
        # compute x_global from x_local
        x_min = self._eta(index)
        x_max = self._eta(index + 1)

        x_global = ((x_local + self._half) / self._length) * (x_max - x_min) + x_min
        return x_global

    def _eta(self, index: int):
        eta = index / float(self._segments)
        return eta * 2 - 1

    def interpolate(self, layer_out: "PiecewiseDiscontinuous"):
        interpolate_polynomial_layer(layer_in=self, layer_out=layer_out)

    def refine(self, layer_out: "PiecewiseDiscontinuous"):
        refine_discontinuous_polynomial_layer(layer_in=self, layer_out=layer_out)


class PiecewiseDiscontinuousPolynomial(PiecewiseDiscontinuous):
    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        segments: int,
        length=2.0,
        weight_magnitude=1.0,
        periodicity: float = None,
        device: str = "cpu",
        **kwargs,
    ):
        super().__init__(
            n,
            in_features,
            out_features,
            segments,
            length,
            weight_magnitude,
            poly=LagrangePoly,
            periodicity=periodicity,
            device=device,
        )


class PiecewiseDiscontinuousPolynomialProd(PiecewiseDiscontinuous):
    def __init__(
        self,
        n: int,
        in_features: int,
        out_features: int,
        segments: int,
        length=2.0,
        weight_magnitude=1.0,
        periodicity: float = None,
        device: str = "cpu",
        **kwargs,
    ):
        super().__init__(
            n,
            in_features,
            out_features,
            segments,
            length,
            weight_magnitude,
            poly=LagrangePolyProd,
            periodicity=periodicity,
        )


def interpolate_polynomial_layer(
    layer_in: Union[PiecewisePolynomial, PiecewiseDiscontinuousPolynomial],
    layer_out: Union[PiecewisePolynomial, PiecewiseDiscontinuousPolynomial],
) -> None:
    """
    Use layer_in to compute the weights in layer_out when layer_in and layer_out
    have the same number of segments but different polynomial orders.  This technique
    is called "p refinement" as it allows us to refine the polynomial order
    Args :
        - layer_in : The layer we will interpolate data from
        - layer_out : The layer whose new weights we compute
    """

    # TODO don't access "private" add a property instead
    poly_in = layer_in._poly
    segments_in = layer_in._segments
    w_in = layer_in.w

    poly_out = layer_out._poly
    segments_out = layer_out._segments
    w_out = layer_out.w

    if segments_in != segments_out:
        raise ValueError(
            f"Number of input and output segments must be the same, got {segments_in} and {segments_out}"
        )

    x_in = poly_in.basis.X.reshape(-1, 1)
    x_out = poly_out.basis.X.reshape(-1, 1)

    n_in = poly_in.basis.n
    n_out = poly_out.basis.n

    if isinstance(layer_in, PiecewisePolynomial):
        offset = -1
        end = 1
    elif isinstance(layer_in, PiecewiseDiscontinuousPolynomial):
        offset = 0
        end = 0

    # Compute the weights on polynomial b from a
    with torch.no_grad():  # No grad so we can assign leaf variable in place
        for inputs in range(w_in.shape[0]):
            for outputs in range(w_in.shape[1]):
                for i in range(segments_in):
                    w = w_in[
                        inputs,
                        outputs,
                        i * (n_in + offset) : (i + 1) * (n_in + offset) + end,
                    ].reshape(1, 1, 1, -1)
                    w_b = poly_in.interpolate(x_out, w)
                    w_out[
                        inputs,
                        outputs,
                        i * (n_out + offset) : (i + 1) * (n_out + offset) + end,
                    ] = w_b.flatten()


def refine_discontinuous_polynomial_layer(
    layer_in: PiecewiseDiscontinuousPolynomial,
    layer_out: PiecewiseDiscontinuousPolynomial,
):
    """
    TODO: If the segments in and segments out are not multiples of each other accuracy
    can be very wrong.  I need to investigate this further whether its a bug or if that's
    in fact how the math works out.

    Given an input layer with N segments, use that to initialize another layer (output layer)
    with M segments.  It's assumed that the polynomial order of both segments are identical.
    This technique would be "h refinement"
    Args :
        layer_in : The layer to interpolate from
        layer_out : The layer whose weights are changed
    """

    device = layer_in.device

    poly_in = layer_in._poly
    segments_in = layer_in._segments
    w_in = layer_in.w

    poly_out = layer_out._poly
    segments_out = layer_out._segments
    w_out = layer_out.w

    x_in = poly_in.basis.X.reshape(-1, 1).to(device)
    x_out = poly_out.basis.X.reshape(-1, 1).to(device)

    n_in = poly_in.basis.n
    n_out = poly_out.basis.n

    # Compute the weights on polynomial b from a
    with torch.no_grad():  # No grad so we can assign leaf variable in place
        for inputs in range(w_in.shape[0]):
            for outputs in range(w_in.shape[1]):
                # TODO: I could probably do this as a single matrix operation,
                # but this was easier for me to debug.  Also, it's not performance
                # critical.

                # loop through the out segments
                for j in range(segments_out):
                    # compute x in the global space
                    x_global = layer_out.x_global(x_out, j)

                    # figure out which segments these correspond to in the input
                    # TODO: This is a problem in discontinuous at the boundaries
                    # since x is contained by 2 segments
                    index_in = layer_in.which_segment(x_global)

                    print("index_in", index_in)
                    raise ValueError(
                        "Since boundaries are doubled up at discontinuities there is ambiguity and this does not work.  This function needs to be fixed."
                    )
                    # compute the local x value in the input so we can interpolate
                    x_local_in = layer_in.x_local(x_global, index_in)

                    # Since the segments may not be aligned, modify the weights one by one
                    for index, i in enumerate(index_in):
                        x = torch.tensor([[x_local_in[index, 0]]], device=device)
                        w = (
                            w_in[inputs, outputs, i * n_in : (i + 1) * n_in]
                            .reshape(1, 1, 1, -1)
                            .to(device)
                        )
                        w_b = poly_in.interpolate(x, w)
                        w_out[inputs, outputs, j * (n_out) + index] = w_b.flatten()


def refine_polynomial_layer(
    layer_in: PiecewisePolynomial, layer_out: PiecewisePolynomial
) -> None:
    """
    TODO: If the segments in and segments out are not multiples of each other accuracy
    can be very wrong.  I need to investigate this further whether its a bug or if that's
    in fact how the math works out.

    Given an input layer with N segments, use that to initialize another layer (output layer)
    with M segments.  It's assumed that the polynomial order of both segments are identical.
    This technique would be "h refinement"
    Args :
        layer_in : The layer to interpolate from
        layer_out : The layer whose weights are changed
    """

    device = layer_in.device

    poly_in = layer_in._poly
    segments_in = layer_in._segments
    w_in = layer_in.w

    poly_out = layer_out._poly
    segments_out = layer_out._segments
    w_out = layer_out.w

    x_in = poly_in.basis.X.reshape(-1, 1).to(device)
    x_out = poly_out.basis.X.reshape(-1, 1).to(device)

    n_in = poly_in.basis.n
    n_out = poly_out.basis.n

    # Compute the weights on polynomial b from a
    with torch.no_grad():  # No grad so we can assign leaf variable in place
        for inputs in range(w_in.shape[0]):
            for outputs in range(w_in.shape[1]):
                # TODO: I could probably do this as a single matrix operation,
                # but this was easier for me to debug.  Also, it's not performance
                # critical.

                # loop through the out segments
                for j in range(segments_out):
                    # compute x in the global space
                    x_global = layer_out.x_global(x_out, j)

                    # figure out which segments these correspond to in the input
                    index_in = layer_in.which_segment(x_global)

                    # compute the local x value in the input so we can interpolate
                    x_local_in = layer_in.x_local(x_global, index_in)

                    # Since the segments may not be aligned, modify the weights one by one
                    for index, i in enumerate(index_in):
                        x = torch.tensor([[x_local_in[index, 0]]], device=device)
                        w = (
                            w_in[
                                inputs,
                                outputs,
                                i * (n_in - 1) : (i + 1) * (n_in - 1) + 1,
                            ]
                            .reshape(1, 1, 1, -1)
                            .to(device)
                        )
                        w_b = poly_in.interpolate(x, w)
                        w_out[inputs, outputs, j * (n_out - 1) + index] = w_b.flatten()


def smooth_discontinuous_layer(layer: PiecewiseDiscontinuous, factor: float):
    """
    Bring the discontinuous nodes closer together by the given
    factor.
    Args :
        - layer: A layer of type piecewise discontinuous
        - factor: 0.5 brings the high value down by 25% and the lower value
        up by 25%.  With enough application the discontinuous node then
        approximates a continuous one.
    """
    n = layer.n

    # every nth interior node is discontinuous
    with torch.no_grad():
        left = layer.w[:, :, (n - 1) : -1 : n]
        right = layer.w[:, :, n:-1:n]
        diff = left - right
        layer.w[:, :, (n - 1) : -1 : n] = left - 0.5 * factor * diff
        layer.w[:, :, n:-1:n] = right + 0.5 * factor * diff


def initialize_polynomial_layer(
    layer_in: Union[PiecewisePolynomial, PiecewiseDiscontinuous],
    max_slope: float = 1.0,
    max_offset: float = 0.0,
) -> None:
    """
    Initialize the layer so that the initial value is a line accross the region.  Without
    this, high order polynomials start out arbitrarily wiggly which can take time to flatten
    out.

    Args :
        layer_in : The layer to initialize
        max_slope : Maximum slope of the input
        max_offset : Maximum mean value or b in ax+b
    """

    if not isinstance(layer_in, (PiecewisePolynomial, PiecewiseDiscontinuous)):
        return

    poly_in = layer_in._poly
    segments_in = layer_in._segments
    w_in = layer_in.w

    x_in = poly_in.basis.X.reshape(-1, 1)
    n_in = poly_in.basis.n

    if isinstance(layer_in, PiecewisePolynomial):
        nodes_per_segment = n_in - 1
        upper_limit = 1
    elif isinstance(layer_in, PiecewiseDiscontinuous):
        nodes_per_segment = n_in
        upper_limit = 0

    with torch.no_grad():  # No grad so we can assign leaf variable in place
        for inputs in range(w_in.shape[0]):
            for outputs in range(w_in.shape[1]):
                a = max_slope * (random.random() * 2 - 1.0)
                b = max_offset * (random.random() * 2 - 1.0)

                for j in range(segments_in):
                    # compute x in the global space
                    x_global = layer_in.x_global(x_in, j)

                    y_global = a * x_global + b

                    w_in[
                        inputs,
                        outputs,
                        j * nodes_per_segment : (j + 1) * nodes_per_segment
                        + upper_limit,
                    ] = y_global.flatten()
