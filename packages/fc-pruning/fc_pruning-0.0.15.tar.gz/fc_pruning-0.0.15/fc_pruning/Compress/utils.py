import torch_pruning as tp
import torch
import torch.nn as nn
import copy
import os
import sys


def print_test():
    print(' It works ')


def get_weights(model):
    return [param.data for param in model.parameters()]


def get_last_layer(model):
    last_layer = None
    for layer in model.modules():
        if isinstance(layer, nn.Linear):
            last_layer = layer
    return last_layer


def create_channel_mask_old(pruned_model):
    mask_indices = []
    mask_values = []

    # Flatten the parameters of the pruned model
    flattened_params = [tensor.flatten() for tensor in pruned_model.parameters()]
    pruned_model_flat = torch.cat(flattened_params, dim=0)

    for idx, val in enumerate(pruned_model_flat):
        if val != 0:
            # If the value is not zero, save the index and value
            mask_indices.append(idx)
            mask_values.append(val.item())  # Save the actual value instead of 1

    # Construct the sparse tensor
    mask_indices = torch.tensor([mask_indices], dtype=torch.long)
    mask_values = torch.tensor(mask_values, dtype=torch.float32)
    mask_sparse = torch.sparse_coo_tensor(mask_indices, mask_values, size=(pruned_model_flat.numel(),))

    return mask_sparse


def create_channel_mask(pruned_model):

    # Flatten the parameters of the pruned model
    flattened_params = [tensor.flatten() for tensor in pruned_model.parameters()]
    pruned_model_flat = torch.cat(flattened_params, dim=0)

    mask_indices = (idx for idx, val in enumerate(pruned_model_flat) if val != 0)

    print(f" {sys.getsizeof(mask_indices)} bytes")

    return mask_indices

def soft_prune(model, imp, example_inputs, pruning_ratio=None, ignored_layers=None):
    pmodel = copy.deepcopy(model)

    #print('error')

    pruner = tp.pruner.MetaPruner(
        pmodel,
        example_inputs,
        #iterative_steps=1,
        importance=imp,
        pruning_ratio=pruning_ratio,
        ignored_layers=ignored_layers
    )

    print('Applying soft pruning step')
    for group in pruner.step(interactive=True):
        # print(group)
        for dep, idxs in group:
            target_layer = dep.target.module
            pruning_fn = dep.handler
            if pruning_fn in [tp.prune_conv_in_channels, tp.prune_linear_in_channels]:
                target_layer.weight.data[:, idxs] *= 0
            elif pruning_fn in [tp.prune_conv_out_channels, tp.prune_linear_out_channels]:
                target_layer.weight.data[idxs] *= 0
                if target_layer.bias is not None:
                    target_layer.bias.data[idxs] *= 0
            elif pruning_fn in [tp.prune_batchnorm_out_channels]:
                target_layer.weight.data[idxs] *= 0
                target_layer.bias.data[idxs] *= 0

    mask_client_list = create_channel_mask(pmodel)

    return pmodel, mask_client_list


def hard_prune(model, imp, example_inputs, pruning_ratio=None, ignored_layers=None):
    pmodel = copy.deepcopy(model)

    pruner = tp.pruner.MetaPruner(
        pmodel,
        example_inputs,
        importance=imp,
        #iterative_steps=1,
        pruning_ratio=pruning_ratio,
        ignored_layers=ignored_layers,
    )

    print('Applying hard pruning step')

    if isinstance(imp, tp.importance.TaylorImportance):
        # Taylor expansion requires gradients for importance estimation
        loss = pmodel(example_inputs).sum()  # a dummy loss for TaylorImportance
        loss.backward()  # before pruner.step()
        print(loss)
    pruner.step()

    return pmodel

def reconstruct_model(mask, pruned_model_params, reference_model):

    if reference_model is not None:
        flattened_params_ref = [tensor.flatten() for tensor in get_weights(reference_model)]
        reference_model_flat = torch.cat(flattened_params_ref, dim=0)

    flattened_params = [tensor.flatten() for tensor in pruned_model_params]
    pruned_model_flat = torch.cat(flattened_params, dim=0)

    mask_indices_list = list(mask)


    mask_dict = {idx: val.item() for idx, val in zip(mask_indices_list, pruned_model_flat)}

    nr_param = len(reference_model_flat)


    # Reconstruct by setting all zero
    reconstructed_model_flat = torch.zeros_like(reference_model_flat)

    # Fill in the values from the dictionary
    for idx, val in mask_dict.items():
        reconstructed_model_flat[idx] = val

    # If a reference model is provided, fill in the remaining values and else keep zero
    if reference_model is not None:
        for i in range(nr_param):
            if reconstructed_model_flat[i] == 0:
                reconstructed_model_flat[i] = reference_model_flat[i]


    desired_shape = [param_tensor.shape for param_tensor in get_weights(reference_model)]

    # Initialize a new model instance
    reconstructed_model = copy.deepcopy(reference_model)

    # Assign the reconstructed parameters to the new model
    start = 0
    for param, shape in zip(reconstructed_model.parameters(), desired_shape):
        end = start + shape.numel()
        param.data = reconstructed_model_flat[start:end].reshape(shape)
        start = end

    return reconstructed_model



def print_size_of_model(model):
    torch.save(model.state_dict(), "temp.p")
    size = os.path.getsize("temp.p") / 1e6  # size in MB
    os.remove('temp.p')
    return size