import time
import numpy as np
import torch
from multidim_indexing import torch_view as view
from pytorch_seed import seed

d = "cuda" if torch.cuda.is_available() else "cpu"


def test_query_performance():
    seed(0)
    data_size = 100
    query_size = 20000

    data = torch.randn(data_size, data_size, data_size, device=d)
    data_view = view.TorchMultidimView(data, value_ranges=[(0, 1), (0, 5), (0, 10)])

    times = []
    res = None
    for iter in range(10):
        query = torch.randn((query_size, 3), device=d)
        start = time.time()
        this_res = data_view[query]
        if res is None:
            res = this_res
        else:
            res += this_res
        end = time.time()
        times.append(end - start)

    print(f"Average query time: {np.mean(times)}")
    print(f"All query times: {times}")


if __name__ == "__main__":
    test_query_performance()
