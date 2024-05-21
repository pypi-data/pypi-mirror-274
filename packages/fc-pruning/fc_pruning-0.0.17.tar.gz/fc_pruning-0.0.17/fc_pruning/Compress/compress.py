from FeatureCloud.app.engine.app import AppState
from typing import TypedDict, Union, List, Type
import torch
import torch_pruning as tp
import pickle

import fc_pruning.Compress.utils as pf


class PruningType(TypedDict):
    model: torch.nn.Module
    reference_model: torch.nn.Module
    imp: Type[tp.pruner.importance.Importance]
    ignored_layers: Union[List[torch.nn.Module], None]
    pruning_ratio: float


class PruneBase(AppState):

    def configure_pruning(self, pruning_ratio : float = 0.5, model: torch.nn.Module = None, reference_model: torch.nn.Module = None,
                         imp: Type[tp.pruner.importance.Importance] = tp.importance.MagnitudeImportance(p=2), ex_input : torch.Tensor = None,
                         ignored_layers: Union[List[torch.nn.Module], None] = None ):

        '''
        Configures the pruning settings for your model.
        Parameters
        ----------
        model : nn.Module
            Your PyTorch model.
        reference_model : nn.Module
            Could be same model as your original model and has to have identical structure to initial model.
        imp : tp.importance
            Importance method for pruning.
        ex_input : torch.Tensor
            Example input tensor.
        ignored_layers : Union[List[nn.Module], None], optional
            List of layers to be ignored during pruning, mostly last layer.
        pruning_ratio : float
            Pruning ratio, should be between 0 and 1. Default value is 0.5.

        '''

        if self.load('default_pruning') is None:
            self.store('default_pruning', PruningType())

        default_pruning = self.load('default_pruning')

        updated_pruning = default_pruning.copy()

        updated_pruning['model'] = model
        updated_pruning['reference_model'] = reference_model
        updated_pruning['pruning_ratio'] = pruning_ratio
        updated_pruning['imp'] = imp
        updated_pruning['ex_input'] = ex_input
        updated_pruning['ignored_layers'] = ignored_layers


        self.store('default_pruning', updated_pruning)


    def prune(self, data):
        '''
        Prunes the model and returns pruned weights and binary mask.


        Parameters
        ----------
        data : torch.nn.Module
              The model to be pruned.

        Returns
        -------
        data_with_mask : list
            List of data with masks for pruning.
        '''

        default_pruning = self.load('default_pruning')

        example_input = default_pruning['ex_input']
        ignored_layers = default_pruning['ignored_layers']
        pruning_ratio = default_pruning['pruning_ratio']
        model = data
        reference_model = default_pruning['reference_model']
        imp = default_pruning['imp']

        self.store('default_pruning', default_pruning)
        self.store('reference_model', reference_model)



        self.log('start pruning...')

        # exclude last_layer from pruning
        last_layer = pf.get_last_layer(model)


        if ignored_layers is None:
            ignored_layers = []
        if last_layer not in ignored_layers:
            ignored_layers.append(last_layer)



        self.log(f'Size of model before pruning: {pf.print_size_of_model(model)} MB')

        binary_mask = []
        _, mask_client_list = pf.soft_prune(model, imp, example_input,
                                        pruning_ratio, ignored_layers)
        binary_mask.append(mask_client_list)
        model = pf.hard_prune(model, imp, example_input,pruning_ratio, ignored_layers)

        self.log(f'Size of model after pruning: {pf.print_size_of_model(model)} MB')

        data_with_mask = pf.get_weights(model) + [binary_mask]

        return model, data_with_mask

class PruneAppState(PruneBase):
    def gather_data(self, use_pruning=True, **kwargs):
        '''
        Gathers data for federated learning, including pruning if enabled.

        Parameters
        ----------
        use_pruning : bool, optional
            Flag to indicate whether to use pruning. Default is True.
        Returns
        -------
        data : list
            List of data to be sent to the coordinator.
        '''
        data_with_mask_list = super().gather_data(**kwargs)

        if use_pruning:
            reference_model = self.load('reference_model')

            #extract data and binary_mask
            data = []
            binary_mask = []
            for data_with_mask in data_with_mask_list:
                data.append(data_with_mask[:-1])
                binary_mask.append(data_with_mask[-1])

            # reconstruct data after pruning
            reconstructed_clients = []
            for i in range(len(data_with_mask_list)):

                reconstructed_model = pf.reconstruct_model(binary_mask[i][0], data[i], reference_model)
                reconstructed_clients.append(pf.get_weights(reconstructed_model))
            data = reconstructed_clients
        else:
            data = data_with_mask_list
        return data

    def send_data_to_coordinator(self, data, use_pruning= True, **kwargs):
        '''
            Sends data to the coordinator, including pruning if enabled.

            Parameters
            ----------
            data : list
                List of data to be sent to the coordinator.
            use_pruning : bool, optional
                Flag to indicate whether to use pruning. Default is True. Enabled if no finetuning is desired.

            Returns
            -------
            data_with_mask : list
                List of data with masks for pruning.
            '''
        if use_pruning:
            _, data_with_mask = self.prune(data)
            super().send_data_to_coordinator(data_with_mask,**kwargs)
        else:
            super().send_data_to_coordinator(data, **kwargs)
            data_with_mask = data
        return data_with_mask