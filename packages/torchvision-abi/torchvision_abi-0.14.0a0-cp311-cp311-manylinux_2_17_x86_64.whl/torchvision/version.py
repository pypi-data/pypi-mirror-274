__version__ = '0.14.0a0+ebeef87'
git_version = 'ebeef87c053cb6583a71184d11b7c52eea5e3f76'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
