# @generated from torch/_C/return_types.pyi

from torch import Tensor, Generator, strided, memory_format, contiguous_format, strided
from typing import List, Tuple, Optional, Union, Any, ContextManager, Callable, overload, Iterator, NamedTuple, Sequence, TypeVar
from typing_extensions import Literal
from torch._six import inf

from torch.types import _int, _float, _bool, Number, _dtype, _device, _qscheme, _size, _layout

_fake_quantize_per_tensor_affine_cachemask_tensor_qparams = NamedTuple("_fake_quantize_per_tensor_affine_cachemask_tensor_qparams", [("output", Tensor), ("mask", Tensor)])
_fused_moving_avg_obs_fq_helper = NamedTuple("_fused_moving_avg_obs_fq_helper", [("output", Tensor), ("mask", Tensor)])
_linalg_det = NamedTuple("_linalg_det", [("result", Tensor), ("LU", Tensor), ("pivots", Tensor)])
_linalg_eigh = NamedTuple("_linalg_eigh", [("eigenvalues", Tensor), ("eigenvectors", Tensor)])
_linalg_slogdet = NamedTuple("_linalg_slogdet", [("sign", Tensor), ("logabsdet", Tensor), ("LU", Tensor), ("pivots", Tensor)])
_linalg_solve_ex = NamedTuple("_linalg_solve_ex", [("result", Tensor), ("LU", Tensor), ("pivots", Tensor), ("info", Tensor)])
_linalg_svd = NamedTuple("_linalg_svd", [("U", Tensor), ("S", Tensor), ("Vh", Tensor)])
_lu_with_info = NamedTuple("_lu_with_info", [("LU", Tensor), ("pivots", Tensor), ("info", Tensor)])
_unpack_dual = NamedTuple("_unpack_dual", [("primal", Tensor), ("tangent", Tensor)])
aminmax = NamedTuple("aminmax", [("min", Tensor), ("max", Tensor)])
cummax = NamedTuple("cummax", [("values", Tensor), ("indices", Tensor)])
cummin = NamedTuple("cummin", [("values", Tensor), ("indices", Tensor)])
frexp = NamedTuple("frexp", [("mantissa", Tensor), ("exponent", Tensor)])
geqrf = NamedTuple("geqrf", [("a", Tensor), ("tau", Tensor)])
histogram = NamedTuple("histogram", [("hist", Tensor), ("bin_edges", Tensor)])
histogramdd = NamedTuple("histogramdd", [("hist", Tensor), ("bin_edges", List[Tensor])])
kthvalue = NamedTuple("kthvalue", [("values", Tensor), ("indices", Tensor)])
lu_unpack = NamedTuple("lu_unpack", [("P", Tensor), ("L", Tensor), ("U", Tensor)])
max = NamedTuple("max", [("values", Tensor), ("indices", Tensor)])
median = NamedTuple("median", [("values", Tensor), ("indices", Tensor)])
min = NamedTuple("min", [("values", Tensor), ("indices", Tensor)])
mode = NamedTuple("mode", [("values", Tensor), ("indices", Tensor)])
nanmedian = NamedTuple("nanmedian", [("values", Tensor), ("indices", Tensor)])
qr = NamedTuple("qr", [("Q", Tensor), ("R", Tensor)])
slogdet = NamedTuple("slogdet", [("sign", Tensor), ("logabsdet", Tensor)])
sort = NamedTuple("sort", [("values", Tensor), ("indices", Tensor)])
svd = NamedTuple("svd", [("U", Tensor), ("S", Tensor), ("V", Tensor)])
symeig = NamedTuple("symeig", [("eigenvalues", Tensor), ("eigenvectors", Tensor)])
topk = NamedTuple("topk", [("values", Tensor), ("indices", Tensor)])
triangular_solve = NamedTuple("triangular_solve", [("solution", Tensor), ("cloned_coefficient", Tensor)])
