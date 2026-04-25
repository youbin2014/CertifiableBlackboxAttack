import torch

from .defaults import get_default_config


def update_config(config):
    if config.attack.num_samples is not None:
        config.attack.CertifiedAttack.MonteNum = config.attack.num_samples
    if config.attack.confidence_level is not None:
        config.attack.CertifiedAttack.confidence_level = config.attack.confidence_level
    if config.attack.binary_search_steps is not None:
        config.attack.CertifiedAttack.binary_search_steps = config.attack.binary_search_steps

    if config.dataset.name in ['CIFAR10', 'CIFAR100']:
        dataset_dir = f'~/.torch/datasets/{config.dataset.name}'
        config.dataset.dataset_dir = dataset_dir
        config.dataset.image_size = 32
        config.dataset.n_channels = 3
        config.dataset.n_classes = int(config.dataset.name[5:])
    elif config.dataset.name in ['MNIST', 'FashionMNIST', 'KMNIST']:
        dataset_dir = '~/.torch/datasets'
        config.dataset.dataset_dir = dataset_dir
        config.dataset.image_size = 28
        config.dataset.n_channels = 1
        config.dataset.n_classes = 10

    if not torch.cuda.is_available():
        config.device = 'cpu'

    return config
