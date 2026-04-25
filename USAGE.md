# Usage Guide

This guide provides comprehensive examples and tutorials for using CertifiedAttack.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Attack Examples](#attack-examples)
  - [Certified Attack](#certified-attack)
  - [Black-box Attacks](#black-box-attacks)
  - [Attacks with Defenses](#attacks-with-defenses)
- [Training Models](#training-models)
  - [Standard Training](#standard-training)
  - [Adversarial Training](#adversarial-training)
- [Evaluation](#evaluation)
- [Configuration System](#configuration-system)
- [Advanced Usage](#advanced-usage)
- [Batch Processing](#batch-processing)
- [Custom Experiments](#custom-experiments)

## Basic Usage

### Command Line Interface

All main scripts support command-line arguments:

```bash
# General format
python script.py --config CONFIG_FILE [options]

# Override config options
python attack.py --config config.yaml device cuda:1 attack.epsilon 0.05
```

### Quick Start Examples

```bash
# 1. Run Certified Attack on CIFAR-10
python attack.py --config "./configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml"

# 2. Train a model
python train.py --config "./configs/cifar10/resnet.yaml"

# 3. Evaluate a model
python evaluate.py --config "./configs/evaluate/vgg.yaml"
```

## Attack Examples

### Certified Attack

Our proposed certified attack method with different variants:

#### Binary Search Variant
```bash
# Paper v3 comparison setting is the default:
# p=10%, sigma=0.025, alpha=0.001, Monte Carlo samples=50.
python attack.py --config "./configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml" \
    device cuda:0

# Paper v3 ablation / randomized-smoothing setting, when needed:
# p=90%, sigma=0.25, alpha=0.001, Monte Carlo samples=1000.
python attack.py --config "./configs/attack/cifar10/untargeted/unrestricted/vgg_CertifiedAttack.yaml" \
    device cuda:0 \
    attack.CertifiedAttack.p 0.90 \
    attack.CertifiedAttack.pdf_args "[-1,0.25]" \
    attack.CertifiedAttack.MonteNum 1000 \
    attack.CertifiedAttack.query_batch 1000 \
    attack.CertifiedAttack.confidence_level 0.999 \
    attack.CertifiedAttack.binary_search_steps 15 \
    attack.max_loss_queries 100000

# CIFAR-100 with ResNet
python attack.py --config "./configs/attack/cifar100/untargeted/unrestricted/resnet_CertifiedAttack.yaml" \
    device cuda:0 \
    attack.CertifiedAttack.binary_search_steps 15
```

#### SSSP (Single-Step Single-Pixel) Variant
```bash
# SSSP variant on ImageNet
python attack.py --config "./configs/attack/imagenet_RAND/untargeted/unrestricted/resnet_CertifiedAttack_sssp.yaml" \
    device cuda:0
```

### Black-box Attacks

#### Score-based Attacks
```bash
# NES Attack
python attack.py --config "./configs/attack/cifar10/untargeted/l2/score/vgg_NES.yaml"

# Square Attack
python attack.py --config "./configs/attack/cifar10/untargeted/linf/score/vgg_Square.yaml"

# SimBA Attack
python attack.py --config "./configs/attack/cifar10/untargeted/l2/score/vgg_Simple.yaml"
```

#### Decision-based Attacks
```bash
# Boundary Attack
python attack.py --config "./configs/attack/cifar10/untargeted/l2/decision/vgg_Boundary.yaml"

# HSJA Attack
python attack.py --config "./configs/attack/cifar10/untargeted/linf/decision/vgg_HSJ.yaml"

# GeoDA Attack
python attack.py --config "./configs/attack/cifar10/untargeted/l2/decision/vgg_GeoDA.yaml"
```

#### Sparse Attacks
```bash
# PointWise Attack
python attack.py --config "./configs/attack/cifar10/untargeted/unrestricted/vgg_PointWise.yaml"

# SparseEvo Attack
python attack.py --config "./configs/attack/cifar10/untargeted/unrestricted/vgg_SparseEvo.yaml"
```

### Attacks with Defenses

#### Against Blacklight Defense
```bash
# CIFAR-10
python attack.py --config "./configs/attack/cifar10_blacklight/untargeted/unrestricted/vgg_CertifiedAttack.yaml"

# CIFAR-100
python attack.py --config "./configs/attack/cifar100_blacklight/untargeted/unrestricted/resnet_CertifiedAttack.yaml"
```

#### Against Randomized Defenses
```bash
# Pre-processing defense (RAND)
python attack.py --config "./configs/attack/cifar10_RAND/untargeted/unrestricted/resnet_CertifiedAttack.yaml"

# Post-processing defense
python attack.py --config "./configs/attack/cifar10_post_RAND/untargeted/unrestricted/wrn_CertifiedAttack.yaml"
```

#### Against Adversarial Training
```bash
# L2 adversarial training
python attack.py --config "./configs/attack/cifar10_AT/untargeted/unrestricted/resnet_CertifiedAttack_l2.yaml"

# L-infinity adversarial training
python attack.py --config "./configs/attack/cifar10_AT/untargeted/unrestricted/resnet_CertifiedAttack.yaml"
```

## Training Models

### Standard Training

#### Basic Training
```bash
# Train ResNet on CIFAR-10
python train.py --config "./configs/cifar10/resnet.yaml" \
    train.output_dir "./experiments/my_resnet" \
    train.epochs 200 \
    train.batch_size 128
```

#### Different Architectures
```bash
# VGG
python train.py --config "./configs/cifar10/vgg.yaml"

# Wide ResNet
python train.py --config "./configs/cifar10/wrn.yaml"

# ResNeXt
python train.py --config "./configs/cifar10/resnext.yaml"

# DenseNet
python train.py --config "./configs/cifar10/densenet.yaml"
```

#### With Data Augmentation
```bash
# CutMix
python train.py --config "./configs/cifar10/resnet.yaml" \
    augmentation.use_cutmix True \
    augmentation.cutmix_alpha 1.0

# MixUp
python train.py --config "./configs/cifar10/resnet.yaml" \
    augmentation.use_mixup True \
    augmentation.mixup_alpha 0.2
```

### Adversarial Training

#### TRADES Training
```bash
# L-infinity adversarial training
python train.py --config "./configs/AT/cifar10/resnet_linf.yaml" \
    train.adv_epsilon 8/255 \
    train.adv_step_size 2/255 \
    train.adv_steps 10

# L2 adversarial training
python train.py --config "./configs/AT/cifar10/resnet_l2.yaml" \
    train.adv_epsilon 0.5 \
    train.adv_beta 6.0
```

#### Custom Adversarial Training
```bash
# Custom epsilon schedule
python train.py --config "./configs/AT/cifar100/resnet_linf.yaml" \
    train.adv_epsilon_schedule "linear" \
    train.adv_epsilon_start 0 \
    train.adv_epsilon_end 8/255
```

## Evaluation

### Model Evaluation
```bash
# Basic evaluation
python evaluate.py --config "./configs/evaluate/vgg.yaml" \
    model.checkpoint "./experiments/cifar10/vgg/exp00/checkpoint_00160.pth"

# Evaluation with different metrics
python evaluate.py --config "./configs/evaluate/vgg.yaml" \
    evaluate.metrics ["accuracy", "robustness", "confidence"]
```

### Robustness Evaluation
```bash
# Evaluate against multiple attacks
python evaluate_robustness.py \
    --model-config "./configs/cifar10/resnet.yaml" \
    --attack-configs "./configs/attack/cifar10/untargeted/*/*.yaml" \
    --output-dir "./results/robustness_evaluation"
```

## Configuration System

### Understanding Config Files

Configuration files use YAML format with hierarchical structure:

```yaml
# Example config structure
dataset:
  name: CIFAR10
  data_dir: ./data
  
model:
  name: resnet
  depth: 18
  
attack:
  name: CertifiedAttack
  epsilon: 0.0
  max_loss_queries: 10000
  CertifiedAttack:
    p: 0.10
    pdf_args: [-1, 0.025]
    MonteNum: 50
    query_batch: 50
    confidence_level: 0.999
    binary_search_steps: 15
  
device: cuda:0
```

### Config Override System

Override any config parameter from command line:

```bash
# Override single parameter
python attack.py --config base.yaml attack.epsilon 0.05

# Override multiple parameters
python attack.py --config base.yaml \
    attack.epsilon 0.05 \
    attack.max_loss_queries 2000 \
    device cuda:1
```

### Creating Custom Configs

1. **Extend existing config**:
```yaml
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

2. **Use the custom config**:
```bash
python attack.py --config my_config.yaml
```

## Advanced Usage

### Multi-GPU Training
```bash
# Data parallel training
python train.py --config "./configs/cifar10/resnet.yaml" \
    train.distributed True \
    train.world_size 4
```

### Mixed Precision Training
```bash
# Enable automatic mixed precision
python train.py --config "./configs/cifar10/resnet.yaml" \
    train.use_amp True \
    train.amp_opt_level "O1"
```

### Custom Learning Rate Schedules
```bash
# Cosine annealing
python train.py --config "./configs/cifar10/resnet.yaml" \
    scheduler.name "cosine" \
    scheduler.t_max 200

# Multi-step LR
python train.py --config "./configs/cifar10/resnet.yaml" \
    scheduler.name "multistep" \
    scheduler.milestones [100, 150] \
    scheduler.gamma 0.1
```

### Checkpoint Management
```bash
# Resume from checkpoint
python train.py --config "./configs/cifar10/resnet.yaml" \
    train.resume "./experiments/cifar10/resnet/exp00/checkpoint_00100.pth"

# Save checkpoints at specific intervals
python train.py --config "./configs/cifar10/resnet.yaml" \
    train.checkpoint_interval 10
```

## Batch Processing

### Running Multiple Attacks
```bash
# Use provided scripts
bash run_attacks.sh

# Or create custom batch script
for config in configs/attack/cifar10/untargeted/{l2,linf}/{score,decision}/vgg_*.yaml; do
    python attack.py --config "$config"
done
```

### Parallel Execution
```bash
# Run attacks in parallel
parallel -j 4 python attack.py --config {} ::: configs/attack/cifar10/untargeted/*/*.yaml
```

## Custom Experiments

### Creating New Attack Configurations

1. **Create config file**:
```yaml
# configs/attack/custom/my_attack.yaml
dataset:
  name: CIFAR10
  
model:
  name: resnet
  checkpoint: ./experiments/cifar10/resnet/checkpoint.pth
  
attack:
  name: CertifiedAttack
  epsilon: 0.05
  CertifiedAttack:
    MonteNum: 1500
    query_batch: 1000
    binary_search_steps: 20
    confidence_level: 0.95
test:
  output_dir: ./results/custom_attack
```

2. **Run the experiment**:
```bash
python attack.py --config ./configs/attack/custom/my_attack.yaml
```

### Analyzing Results

```python
# Load and analyze results
import numpy as np
import matplotlib.pyplot as plt

# Load attack results
results = np.load('results/attack_results.npz')
success_rates = results['success_rates']
query_counts = results['query_counts']

# Plot success rate vs queries
plt.figure(figsize=(10, 6))
plt.plot(query_counts, success_rates)
plt.xlabel('Number of Queries')
plt.ylabel('Attack Success Rate')
plt.title('Attack Performance')
plt.grid(True)
plt.savefig('attack_performance.png')
```

### Custom Metrics and Logging

```bash
# Evaluation writes predictions, probabilities, labels, loss, and accuracy
# to test.output_dir/predictions.npz.
python evaluate.py --config "./configs/evaluate/vgg.yaml" \
    test.output_dir "./experiments/cifar10/vgg/exp00/clean"
```

## Tips and Best Practices

1. **Start with small experiments**: Test with reduced dataset size or iterations
   ```bash
   python attack.py --config config.yaml \
       attack.test_sample 100 \
       attack.max_loss_queries 10000
   ```

2. **Monitor GPU memory**: Adjust batch size if OOM. CertifiedAttack and decision-based attacks require `test.batch_size 1`; score-based attacks can use larger batches when Blacklight is disabled.
   ```bash
   python attack.py --config config.yaml \
       test.batch_size 1
   ```

3. **Use tensorboard for monitoring**:
   ```bash
   # Start tensorboard
   tensorboard --logdir ./experiments/
   ```

4. **Save outputs to a custom directory**:
   ```bash
   python attack.py --config config.yaml \
       test.output_dir ./results/custom_attack
   ```

5. **Quick smoke test**:
   ```bash
   python attack.py --config config.yaml \
       attack.test_sample 10 \
       attack.max_loss_queries 100
   ```

## Getting Help

- Check configuration defaults in `pytorch_image_classification/config/defaults.py`
- See example configs in `configs/` directory
- Review source code documentation
- Open an issue on GitHub for specific problems
