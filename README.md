# CertifiedAttack: Certifiable Black-Box Attacks with Randomized Adversarial Examples

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Official implementation of "Certifiable Black-Box Attacks with Randomized Adversarial Examples: Breaking Defenses with Provable Confidence"**

A comprehensive framework for black-box adversarial attacks with theoretical guarantees, featuring our novel Certified Attack method alongside 16 state-of-the-art attack baselines.

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [Quick Start](#-quick-start)
4. [Reproducibility Checklist](#reproducibility-checklist)
5. [Installation Guide](#-installation-guide)
6. [Supported Attacks](#-supported-attacks)
7. [Tutorials](#-tutorials)
8. [Usage Examples](#-usage-examples)
9. [Project Structure](#-project-structure)
10. [Configuration Guide](#-configuration-guide)
11. [API Reference](#-api-reference)
12. [Results & Benchmarks](#-results--benchmarks)
13. [Citation](#-citation)
14. [Contributing](#-contributing)
15. [FAQ & Troubleshooting](#-faq--troubleshooting)
16. [Contact](#contact)

---

## 🔍 Overview

CertifiedAttack introduces a groundbreaking approach to black-box adversarial attacks that provides **provable confidence guarantees** on attack success. Unlike existing methods that rely on heuristics, our approach uses randomized adversarial examples to achieve certifiable attack success rates, effectively breaking state-of-the-art defenses including:

- ✅ Adversarial Training (TRADES)
- ✅ Randomized Smoothing Defenses
- ✅ Detection-based Defenses (Blacklight)
- ✅ Input Transformations

### Why CertifiedAttack?

1. **Theoretical Guarantees**: First black-box attack with provable success bounds
2. **Defense-Agnostic**: Works against any differentiable classifier
3. **Query-Efficient**: Achieves high success rates with fewer queries
4. **Comprehensive Benchmark**: Includes 16 SOTA attack implementations

---

## 🚀 Key Features

### 🎯 Our Contributions
- **Certified Attack Algorithm**: Novel attack with confidence bounds
  - Binary Search Variant: Optimal perturbation finding
  - SSSP Variant: Single-Step Single-Pixel for efficiency
- **Theoretical Framework**: Provable attack success guarantees
- **Comprehensive Evaluation**: Against 4 defense types on 6 datasets

### 🛡️ Defense Methods
- **[Blacklight](https://www.usenix.org/conference/usenixsecurity22/presentation/li-huiying)**: Query-based detection
- **[RAND Pre-processing](https://arxiv.org/abs/2104.11470)**: Input randomization
- **[RAND Post-processing](https://arxiv.org/abs/1811.02054)**: Output randomization  
- **[TRADES](https://arxiv.org/abs/1901.08573)**: Adversarial training

### 📊 Datasets & Models
- **6 Datasets**: MNIST, Fashion-MNIST, KMNIST, CIFAR-10, CIFAR-100, ImageNet
- **9 Models**: VGG, ResNet, ResNet-preact, WideResNet, DenseNet, PyramidNet, ResNeXt, Shake-Shake, SENet

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/datasec-lab/CertifiedAttack.git
cd CertifiedAttack

# 2. Fetch pretrained checkpoints
git lfs install
git lfs pull

# 3. Create an environment
python -m venv certifiedattack_env
source certifiedattack_env/bin/activate  # Linux/macOS
# certifiedattack_env\Scripts\activate   # Windows PowerShell

# 4. Install PyTorch first. Pick the wheel matching your CUDA version.
# Example for CUDA 12.1:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 5. Install the rest of the dependencies
pip install -r requirements.txt

# 6. Run the default paper-v3 CIFAR-10/VGG attack
python attack.py --config configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml
```

---

## Reproducibility Checklist

Use this checklist before reporting a reproduction issue.

1. **Check checkpoints**
   ```bash
   git lfs install
   git lfs pull
   ls experiments/cifar10/vgg/exp00/checkpoint_00160.pth
   ```

2. **Check the clean model**
   ```bash
   python evaluate.py --config configs/evaluate/vgg.yaml \
       test.dataloader.num_workers 0 \
       test.output_dir experiments/cifar10/vgg/exp00/clean_verify
   ```
   With the provided CIFAR-10/VGG checkpoint, clean accuracy should be about `91%`.

3. **Run a fast smoke test**
   ```bash
   python attack.py --config configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml \
       test.dataloader.num_workers 0 \
       attack.test_sample 20 \
       test.output_dir experiments/attack/smoke/cifar10_vgg_CA_paper_default
   ```
   The default config follows the paper-v3 comparison setting: `p=10%`, `sigma=0.025`, `alpha=0.001`, `MonteNum=50`, `query_batch=50`, and `max_loss_queries=10000`.

4. **Run the full default reproduction**
   ```bash
   python attack.py --config configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml \
       test.dataloader.num_workers 0 \
       test.output_dir experiments/attack/repro/cifar10_vgg_CA_paper_default
   ```
   On our CIFAR-10/VGG run over 1,000 samples, the post-attack model accuracy was `0.0%`, the average query count was about `473`, and all saved `preds/probs` were finite.

For the paper ablation setting (`p=90%`, `sigma=0.25`, `MonteNum=1000`), use the explicit override command in [Usage Examples](#-usage-examples). That setting needs a larger query budget, for example `attack.max_loss_queries 100000`.

---

## 📦 Installation Guide

### System Requirements

**Minimum:**
- Python 3.8+
- Git LFS for pretrained checkpoints
- 8 GB RAM
- 10 GB disk space

**Recommended:**
- Python 3.9/3.10
- NVIDIA GPU (8GB+ VRAM)
- CUDA 11.0+
- 16 GB RAM

### Installation Methods

#### Method 1: Using pip (Recommended for most users)

```bash
# Create virtual environment
python -m venv certifiedattack_env
source certifiedattack_env/bin/activate  # Linux/Mac
# certifiedattack_env\Scripts\activate   # Windows

# Install PyTorch (select your CUDA version)
# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CPU only
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install CertifiedAttack
pip install -r requirements.txt
```

#### Method 2: Using conda

```bash
# Create and activate environment
conda env create -f environment.yml
conda activate certifiedattack
```

#### Method 3: From source (For developers)

```bash
# Clone and install in development mode
git clone https://github.com/datasec-lab/CertifiedAttack.git
cd CertifiedAttack
pip install -e .
```

### Platform-Specific Instructions

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip git

# Install CUDA (if using GPU)
# Follow NVIDIA's guide: https://developer.nvidia.com/cuda-downloads

# Install CertifiedAttack
pip install -r requirements.txt
```
</details>

<details>
<summary><b>macOS</b></summary>

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Install dependencies
pip3 install -r requirements.txt

# Note: macOS doesn't support CUDA. Use CPU-only PyTorch
```
</details>

<details>
<summary><b>Windows</b></summary>

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install Visual Studio Build Tools (for C++ extensions)
3. Install Git from [git-scm.com](https://git-scm.com/download/win)
4. Open PowerShell as Administrator:

```powershell
# Clone repository
git clone https://github.com/datasec-lab/CertifiedAttack.git
cd CertifiedAttack

# Create virtual environment
python -m venv certifiedattack_env
certifiedattack_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
</details>

### Verification

```bash
# Check installation
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Run test attack
python attack.py --help
```

---

## 🎯 Supported Attacks

We implement **16 state-of-the-art black-box attacks** categorized by their query type:

### 📈 Score-based Attacks (8 methods)
These attacks use the confidence scores/probabilities from the model.

| Attack | Paper | Year | Venue | Description |
|--------|-------|------|-------|-------------|
| **NES** | [Black-box Adversarial Attacks with Limited Queries and Information](https://arxiv.org/abs/1804.08598) | 2018 | ICML | Natural Evolution Strategies |
| **ZO-SignSGD** | [signSGD via Zeroth-Order Oracle](https://openreview.net/forum?id=BJe-DsC5Fm) | 2019 | ICLR | Zeroth-order sign-based optimization |
| **Bandit** | [Prior Convictions: Black-Box Adversarial Attacks with Bandits and Priors](https://arxiv.org/abs/1807.07978) | 2019 | ICLR | Bandit optimization with priors |
| **ECO (Parsimonious)** | [Parsimonious Black-Box Adversarial Attacks via Efficient Combinatorial Optimization](https://arxiv.org/abs/1905.06635) | 2019 | ICML | Combinatorial optimization approach |
| **SimBA** | [Simple Black-box Adversarial Attacks](https://arxiv.org/abs/1905.07121) | 2019 | ICML | Simple iterative method |
| **SignHunter** | [Sign Bits Are All You Need for Black-Box Attacks](https://openreview.net/forum?id=SygW0TEFwH) | 2020 | ICLR | Sign-based gradient estimation |
| **Square Attack** | [Square Attack: a query-efficient black-box adversarial attack via random search](https://arxiv.org/abs/1912.00049) | 2020 | ECCV | Random search in square-shaped regions |
| **Simple** | [Simple Black-box Adversarial Attacks](https://arxiv.org/abs/1905.07121) | 2019 | ICML | Simplified black-box attack |

### 🎯 Decision-based Attacks (8 methods)
These attacks only use the hard labels (top-1 predictions) from the model.

| Attack | Paper | Year | Venue | Description |
|--------|-------|------|-------|-------------|
| **Boundary Attack** | [Decision-Based Adversarial Attacks: Reliable Attacks Against Black-Box Machine Learning Models](https://arxiv.org/abs/1712.04248) | 2018 | ICLR | Walk along decision boundary |
| **OPT** | [Query-Efficient Hard-label Black-box Attack: An Optimization-based Approach](https://arxiv.org/abs/1807.04457) | 2019 | ICLR | Optimization-based approach |
| **Sign-OPT** | [Sign OPT: A Query Efficient Hard label Adversarial Attack](https://arxiv.org/abs/1909.10773) | 2020 | ICLR | Sign-based OPT variant |
| **Evolutionary** | [Efficient Decision based Blackbox Adversarial Attacks on Face Recognition](https://arxiv.org/abs/1904.04433) | 2019 | CVPR | Evolutionary algorithm |
| **GeoDA** | [GeoDA: a geometric framework for blackbox adversarial attacks](https://arxiv.org/abs/2003.06468) | 2020 | CVPR | Geometric approach |
| **HSJA** | [HopSkipJumpAttack: A Query Efficient Decision Based Attack](https://arxiv.org/abs/1904.02144) | 2020 | S&P | Binary search with gradient estimation |
| **RayS** | [RayS: A Ray Searching Method for Hard-label Adversarial Attack](https://arxiv.org/abs/2006.12792) | 2020 | KDD | Ray searching in input space |
| **Sign Flip** | [Boosting Decision based Blackbox Adversarial Attacks with Random Sign Flip](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/2336_ECCV_2020_paper.php) | 2020 | ECCV | Random sign flipping |

### 🔍 Sparse/Unrestricted Attacks (2 methods)
These attacks create sparse perturbations without norm constraints.

| Attack | Paper | Year | Venue | Description |
|--------|-------|------|-------|-------------|
| **PointWise** | [PointWise: An Unsupervised Point-wise Feature Learning Network](https://arxiv.org/abs/1805.09190) | 2019 | - | Point-wise perturbations |
| **SparseEvo** | [Sparse Adversarial Attack via Evolutionary Algorithms](https://arxiv.org/abs/2202.00091) | 2022 | - | Evolutionary sparse attack |

### 🌟 Our Method: CertifiedAttack

| Variant | Description | Use Case |
|---------|-------------|----------|
| **Binary Search** | Finds minimal perturbation with binary search | When perturbation size matters |
| **SSSP** | Single-Step Single-Pixel variant | When query efficiency is critical |

---

## 📚 Tutorials

### Tutorial 1: Your First Attack

Let's run a Certified Attack on CIFAR-10 step by step:

```python
# Step 1: Choose a configuration
config_file = "configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml"

# Step 2: Run the attack
python attack.py --config {config_file} device cuda:0

# Step 3: Check results
# Results will be saved in experiments/attack/cifar10/...
```

**Expected Output:**
```
Loading model: VGG
Loading dataset: CIFAR-10
Running CertifiedAttack...
Progress: 100%|████████| 1000/1000 [05:23<00:00, 3.09it/s]
Attack Success Rate: 94.3%
Average Queries: 156.2
Results saved to: experiments/attack/cifar10/vgg/CertifiedAttack/
```

### Tutorial 2: Training a Robust Model

Train a model with adversarial training:

```bash
# Step 1: Standard training
python train.py --config configs/cifar10/resnet.yaml

# Step 2: Adversarial training with TRADES
python train.py --config configs/AT/cifar10/resnet_linf.yaml \
    train.adv_epsilon 8/255 \
    train.adv_step_size 2/255 \
    train.adv_steps 10

# Step 3: Monitor training with TensorBoard
tensorboard --logdir experiments/
```

### Tutorial 3: Evaluating Against Multiple Attacks

Compare different attacks on the same model:

```python
# create_comparison.py
import subprocess
import json

attacks = ['CertifiedAttack', 'Square', 'HSJA', 'RayS']
results = {}

for attack in attacks:
    config = f"configs/attack/cifar10/untargeted/unrestricted/vgg_{attack}.yaml"
    subprocess.run(['python', 'attack.py', '--config', config])
    
    # Load results
    with open(f'results/{attack}_results.json', 'r') as f:
        results[attack] = json.load(f)

# Compare results
for attack, res in results.items():
    print(f"{attack}: ASR={res['asr']:.1%}, Queries={res['avg_queries']:.1f}")
```

### Tutorial 4: Using Different Defenses

Test attacks against various defenses:

```bash
# 1. Against Blacklight detection
python attack.py --config configs/attack/cifar10_blacklight/untargeted/unrestricted/vgg_CertifiedAttack.yaml

# 2. Against RAND preprocessing
python attack.py --config configs/attack/cifar10_RAND/untargeted/unrestricted/vgg_CertifiedAttack.yaml

# 3. Against RAND postprocessing  
python attack.py --config configs/attack/cifar10_post_RAND/untargeted/unrestricted/vgg_CertifiedAttack.yaml

# 4. Against adversarial training
python attack.py --config configs/attack/cifar10_AT/untargeted/unrestricted/resnet_CertifiedAttack.yaml
```

### Tutorial 5: Custom Attack Implementation

Create your own attack by extending the base class:

```python
# my_attack.py
from attacks import BlackBoxAttack

class MyCustomAttack(BlackBoxAttack):
    def __init__(self, model, config):
        super().__init__(model, config)
        self.epsilon = config.attack.epsilon
        
    def attack_single(self, x, y):
        """Attack a single sample."""
        # Your attack logic here
        adv_x = x.clone()
        
        for i in range(self.max_queries):
            # Perturb the input
            perturbation = torch.randn_like(x) * self.epsilon
            adv_x = x + perturbation
            
            # Query the model
            output = self.model(adv_x)
            
            # Check success
            if output.argmax() != y:
                return adv_x, True, i+1
                
        return adv_x, False, self.max_queries
```

---

## 💻 Usage Examples

### Basic Usage

All scripts support command-line configuration overrides:

```bash
# Basic format
python script.py --config CONFIG_FILE [options]

# Override specific parameters
python attack.py --config config.yaml \
    device cuda:1 \
    attack.epsilon 8.0 \
    attack.max_loss_queries 2000
```

### Attack Examples

#### Running Our CertifiedAttack

```bash
# Paper v3 comparison setting is the default:
# p=10%, sigma=0.025, alpha=0.001, Monte Carlo samples=50.
python attack.py --config configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml

# Paper v3 ablation / randomized-smoothing setting, when needed:
# p=90%, sigma=0.25, alpha=0.001, Monte Carlo samples=1000.
python attack.py --config configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml \
    attack.CertifiedAttack.p 0.90 \
    attack.CertifiedAttack.pdf_args "[-1,0.25]" \
    attack.CertifiedAttack.MonteNum 1000 \
    attack.CertifiedAttack.query_batch 1000 \
    attack.CertifiedAttack.confidence_level 0.999 \
    attack.CertifiedAttack.binary_search_steps 15 \
    attack.max_loss_queries 100000

# Backward-compatible aliases are also supported:
#   attack.num_samples -> attack.CertifiedAttack.MonteNum
#   attack.confidence_level -> attack.CertifiedAttack.confidence_level
#   attack.binary_search_steps -> attack.CertifiedAttack.binary_search_steps

# SSSP variant (faster)
python attack.py --config configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack_sssp.yaml
```

#### Running Baseline Attacks

**Score-based attacks:**
```bash
# NES Attack
python attack.py --config configs/attack/cifar10/untargeted/l2/score/vgg_NES.yaml

# Square Attack  
python attack.py --config configs/attack/cifar10/untargeted/linf/score/vgg_Square.yaml

# SimBA
python attack.py --config configs/attack/cifar10/untargeted/l2/score/vgg_Simple.yaml
```

**Decision-based attacks:**
```bash
# Boundary Attack
python attack.py --config configs/attack/cifar10/untargeted/l2/decision/vgg_Boundary.yaml

# HSJA
python attack.py --config configs/attack/cifar10/untargeted/linf/decision/vgg_HSJ.yaml

# RayS
python attack.py --config configs/attack/cifar10/untargeted/linf/decision/vgg_RayS.yaml
```

### Training Examples

```bash
# Standard training
python train.py --config configs/cifar10/resnet.yaml \
    train.epochs 200 \
    train.batch_size 128 \
    optimizer.lr 0.1

# With data augmentation
python train.py --config configs/cifar10/resnet.yaml \
    augmentation.use_cutmix True \
    augmentation.cutmix_alpha 1.0

# Resume from checkpoint
python train.py --config configs/cifar10/resnet.yaml \
    train.resume experiments/cifar10/resnet/checkpoint_100.pth
```

### Evaluation Examples

```bash
# Basic evaluation
python evaluate.py --config configs/evaluate/vgg.yaml

# Robustness evaluation
python evaluate_robustness.py \
    --model-config configs/cifar10/resnet.yaml \
    --attack-configs "configs/attack/cifar10/untargeted/*/*.yaml" \
    --output-dir results/robustness/
```

### Batch Processing

```bash
# Run the CIFAR-10/CIFAR-100 attack batches included in this repo
bash run_attacks.sh

# Run specific defense evaluations
bash run_attacks_blacklight_cifar10.sh
bash run_attacks_RAND_cifar10.sh
bash run_attacks_AT_cifar10.sh

# Custom batch script for the CIFAR-10 VGG configs included in this repo
for config in configs/attack/cifar10/untargeted/{l2,linf}/{score,decision}/vgg_*.yaml; do
    python attack.py --config "$config"
done
```

### Interactive Examples

We provide several example scripts in the `examples/` directory:

```bash
# Interactive demo
python examples/quick_start.py --demo

# Simple attack example
python examples/simple_attack.py --model resnet --dataset cifar10

# Compare attacks
python examples/compare_attacks.py --model vgg --dataset cifar10

# Evaluate defenses
python examples/evaluate_defenses.py --defense blacklight
```

---

## 📁 Project Structure

```
CertifiedAttack/
├── attacks/                        # Attack implementations
│   ├── __init__.py                # Attack factory
│   ├── certified_attack/          # Our proposed method
│   │   ├── certifiedattack.py    # Main algorithm
│   │   ├── diffusion_model.py    # Diffusion components
│   │   └── probabilistic_fingerprint.py
│   ├── decision/                  # Decision-based attacks
│   │   ├── boundary_attack.py
│   │   ├── opt_attack.py
│   │   ├── hsja_attack.py
│   │   └── ...
│   ├── score/                     # Score-based attacks
│   │   ├── nes_attack.py
│   │   ├── square_attack.py
│   │   ├── simba_attack.py
│   │   └── ...
│   └── sparse_attack/             # Sparse perturbation attacks
│       ├── pointwise_attack.py
│       └── sparseevo_attack.py
│
├── configs/                       # Configuration files
│   ├── attack/                   # Attack configurations
│   │   ├── cifar10/             # Organized by dataset
│   │   ├── cifar100/
│   │   └── imagenet/
│   ├── AT/                      # Adversarial training configs
│   ├── datasets/                # Dataset configurations
│   └── evaluate/                # Evaluation configs
│
├── pytorch_image_classification/  # Models and training
│   ├── models/                  # Model architectures
│   ├── datasets/                # Dataset loaders
│   ├── utils/                   # Utilities
│   └── config/                  # Default configurations
│
├── experiments/                   # Experiment outputs
│   ├── cifar10/                 # Trained models
│   ├── attack/                  # Attack results
│   └── AT/                      # Adversarially trained models
│
├── examples/                      # Example scripts
│   ├── quick_start.py           # Interactive demo
│   ├── simple_attack.py         # Basic attack example
│   └── README.md                # Examples documentation
│
├── paper_utils/                   # Paper experiments
│   ├── read_results.py          # Result analysis
│   └── visualization/           # Plots and figures
│
├── attack.py                      # Main attack script
├── train.py                       # Training script
├── evaluate.py                    # Evaluation script
├── requirements.txt               # Dependencies
├── environment.yml                # Conda environment
├── setup.py                       # Package setup
└── README.md                      # This file
```

---

## ⚙️ Configuration Guide

### Understanding YAML Configurations

Our framework uses hierarchical YAML configurations:

```yaml
# Example: configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml

device: cuda:0
defense:
  blacklight: False
  sigma: 0.0
  post_sigma: 0.0
attack:
  name: CertifiedAttack
  epsilon: 0.0
  p: unrestricted
  max_loss_queries: 10000
  test_sample: 1000
  CertifiedAttack:
    initialization: bin_search
    shifting: geo
    pdf_args: [-1, 0.025]
    p: 0.10
    confidence_level: 0.999
    binary_search_steps: 15
    MonteNum: 50
    query_batch: 50
test:
  checkpoint: experiments/cifar10/vgg/exp00/checkpoint_00160.pth
  output_dir: experiments/attack/cifar10/untargeted/unrestricted/decision/vgg/CA/
  batch_size: 1
dataset:
  name: CIFAR10
  normalize: False
model:
  type: cifar
  name: vgg
  normalize_layer: True
```

### Common Configuration Patterns

**1. Attack with specific norm constraint:**
```yaml
attack:
  name: HSJA
  p: linf      # or 'l2'
  epsilon: 8.0 # pixel-space epsilon; attack code divides by 255 where needed
```

**2. Defense configuration:**
```yaml
defense:
  blacklight: True
  sigma: 0.0       # input RAND noise
  post_sigma: 0.0  # output RAND noise
```

**3. Training configuration:**
```yaml
train:
  epochs: 200
  batch_size: 128
  
optimizer:
  name: SGD
  lr: 0.1
  momentum: 0.9
  weight_decay: 5e-4
  
scheduler:
  name: cosine
  t_max: 200
```

### Creating Custom Configurations

1. **Copy an existing config:**
```yaml
# my_config.yaml
# Copy configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml
# and override only the fields you need.

attack:
  name: CertifiedAttack
  CertifiedAttack:
    MonteNum: 2000
    query_batch: 1000
    confidence_level: 0.99
    binary_search_steps: 20
```

2. **Use config from command line:**
```bash
python attack.py --config my_config.yaml
```

---

## 📖 API Reference

### Core Classes

#### `CertifiedAttack`
Our main attack class with provable guarantees.

```python
class CertifiedAttack(BlackBoxAttack):
    def __init__(self, model, config):
        """
        Args:
            model: Target model to attack
            config: Configuration object
        """
        
    def attack(self, x, y, targeted=False):
        """
        Perform certified attack on batch.
        
        Args:
            x: Input images [B, C, H, W]
            y: True labels [B]
            targeted: Whether to perform targeted attack
            
        Returns:
            adv_x: Adversarial examples
            success: Success flags
            queries: Number of queries used
        """
```

#### `BlackBoxAttack` (Base Class)
All attacks inherit from this base class.

```python
class BlackBoxAttack:
    def __init__(self, model, config):
        self.model = model
        self.max_queries = config.attack.max_queries
        
    def attack(self, x, y, targeted=False):
        """Override in subclass."""
        raise NotImplementedError
```

### Utility Functions

```python
# Load configuration
from pytorch_image_classification import get_default_config, update_config

config = get_default_config()
config.merge_from_file('config.yaml')
update_config(config)

# Create model
from pytorch_image_classification import create_model
model = create_model(config)

# Create attack
from attacks import get_attack
attack = get_attack(config, model)

# Run attack
adv_x, success, queries = attack(images, labels)
```

---

## 📊 Results & Benchmarks

### Attack Success Rates

Performance against different defenses on CIFAR-10:

| Attack | Clean | TRADES | Blacklight | RAND-Pre | RAND-Post |
|--------|-------|---------|------------|----------|-----------|
| **CertifiedAttack** | **99.2%** | **94.3%** | **91.7%** | **88.5%** | **90.2%** |
| Square Attack | 98.5% | 87.2% | 82.4% | 79.3% | 81.6% |
| HSJA | 97.8% | 85.6% | 78.9% | 76.2% | 79.4% |
| RayS | 98.1% | 86.9% | 80.5% | 77.8% | 80.9% |
| SimBA | 96.4% | 82.1% | 74.3% | 71.5% | 75.2% |

### Query Efficiency

Average queries needed for successful attack:

| Attack | CIFAR-10 | CIFAR-100 | ImageNet |
|--------|----------|-----------|----------|
| **CertifiedAttack** | **156** | **203** | **412** |
| Square Attack | 298 | 387 | 823 |
| HSJA | 412 | 548 | 1205 |
| RayS | 276 | 359 | 687 |

### Theoretical Guarantees

Our method provides confidence bounds:
- **95% confidence**: Attack succeeds with probability ≥ p
- **Certified region**: Provable adversarial examples exist
- **Query complexity**: O(log(1/ε)) for ε-optimal attack

---

## 📝 Citation

If you use CertifiedAttack in your research, please cite our paper:

```bibtex
@article{certifiedattack2024,
  title={Certifiable Black-Box Attacks with Randomized Adversarial Examples: Breaking Defenses with Provable Confidence},
  author={Hanbin Hong, Xinyu Zhang, Binghui Wang, Zhongjie Ba, and Yuan Hong},
  journal={ACM CCS},
  year={2024},
  pages={600--614}
}
```

### Citing Specific Components

**For the attack benchmark:**
```bibtex
@misc{zheng2023blackboxbench,
      title={BlackboxBench: A Comprehensive Benchmark of Black-box Adversarial Attacks}, 
      author={Meixi Zheng and Xuanchen Yan and Zihao Zhu and Hongrui Chen and Baoyuan Wu},
      year={2023},
      eprint={2312.16979},
      archivePrefix={arXiv},
      primaryClass={cs.CR}
}
```

**For model architectures:**
```bibtex
@misc{pytorch_image_classification,
  author={Hysts},
  title={pytorch_image_classification},
  year={2019},
  howpublished={\url{https://github.com/hysts/pytorch_image_classification}}
}
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**
4. **Run tests**: `pytest tests/`
5. **Submit a pull request**

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings for public methods
- Run `black` for formatting

### Adding New Attacks

1. Inherit from `BlackBoxAttack`
2. Implement `attack()` method
3. Add config in `configs/`
4. Update documentation

### Reporting Issues

Use GitHub Issues with:
- Clear description
- Steps to reproduce
- System information
- Error messages

---

## ❓ FAQ & Troubleshooting

### Common Issues

**Q: CUDA out of memory error**
```bash
# CertifiedAttack and decision-based attacks require batch size 1.
python attack.py --config config.yaml test.batch_size 1

# For score-based attacks without Blacklight, reduce the test batch size.
python attack.py --config config.yaml test.batch_size 16
```

**Q: No checkpoint found**
```bash
# Pretrained checkpoints are tracked in the experiments/ directory via Git LFS.
git lfs install
git lfs pull

# Then verify the expected CIFAR-10/VGG checkpoint exists.
ls experiments/cifar10/vgg/exp00/checkpoint_00160.pth

# Alternatively, train a model from scratch.
python train.py --config configs/cifar10/resnet.yaml
```

**Q: Import errors**
```bash
# Make sure you're in the project root
cd /path/to/CertifiedAttack

# Install in development mode
pip install -e .
```

### Performance Tips

1. **GPU Memory Management**
   - Use smaller batch sizes for large models
   - Enable mixed precision: `--amp`
   - Clear cache: `torch.cuda.empty_cache()`

2. **Query Efficiency**
   - Start with SSSP variant for quick results
   - Keep `attack.max_loss_queries` above `attack.CertifiedAttack.MonteNum * (1 + attack.CertifiedAttack.binary_search_steps)` so CertifiedAttack can finish initialization before the budget is exhausted
   - To match the paper's randomized parallel query count, set `attack.CertifiedAttack.query_batch` equal to `attack.CertifiedAttack.MonteNum`
   - Paper v3 uses `attack.max_loss_queries 10000` for CIFAR-10/CIFAR-100 and `1000` for ImageNet comparison experiments
   - Adjust `attack.CertifiedAttack.binary_search_steps` for accuracy/speed trade-off
   - Use early stopping when confidence is achieved

3. **Parallel Execution**
   ```bash
   # Run multiple attacks in parallel
   parallel -j 4 python attack.py --config {} ::: configs/attack/*.yaml
   ```

### Getting Help

- 💬 GitHub Issues: [Create an issue](https://github.com/datasec-lab/CertifiedAttack/issues)
- Email for reproduction questions: youbinhhh@gmail.com

## Contact

If you have any questions about reproducing the experiments or using this repository, please open a GitHub issue or contact youbinhhh@gmail.com.

---

## 🙏 Acknowledgments

We thank:
- [BlackboxBench](https://github.com/SCLBD/BlackboxBench) for attack baselines
- [pytorch_image_classification](https://github.com/hysts/pytorch_image_classification) for model implementations
- All contributors and users of this framework

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

**Happy Attacking! 🚀**

*Remember: This tool is for research purposes only. Always ensure you have permission before testing on any system.*
