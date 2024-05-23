import jax
import random

import numpy as np
import jax.numpy as jnp

class SamplerBase:
    """Other classes will be used this helper class."""

    def __init__(self, dtype):
        """Base class for sampling mesh data for training.

        Initializes instance variables for storing sampled data and solutions.
        """
        self.time_domain_sampled = None
        self.spatial_domain_sampled = None
        self.solution_sampled = None
        self.solution_names = None
        dtype = 'float32'
        self.np_dtype = np.dtype(dtype)
        self.rng = jax.random.PRNGKey(0)

    def concatenate_solutions(self, flatten_mesh):
        """Concatenate dictionary of sampled solution data.

        :param flatten_mesh: Flattened mesh data.
        :return: Flattened mesh data with concatenated solutions.
        """
        flatten_mesh = list(flatten_mesh)
        concatenated_solutions = [
            flatten_mesh[2][solution_name] for solution_name in self.solution_names
        ]
        flatten_mesh[2] = np.concatenate(concatenated_solutions, axis=-1)

        return flatten_mesh

    def sample_mesh(self, num_sample, flatten_mesh):
        """Sample the mesh data for training.

        :param num_sample: Number of samples to generate.
        :param flatten_mesh: Flattened mesh data.
        :return: Sampled spatial, time, and solution data.
        """

        flatten_mesh = self.concatenate_solutions(flatten_mesh)

        if num_sample is None:
            return self.convert_to_tensor(flatten_mesh)
        else:
            idx = np.random.choice(range(flatten_mesh[0].shape[0]), num_sample, replace=False)
            return self.convert_to_tensor(
                (flatten_mesh[0][idx, :], flatten_mesh[1][idx, :], flatten_mesh[2][idx, :])
            )

    def convert_to_tensor(self, arrays):
        """Convert NumPy arrays to TensorFlow tensors.

        :param arrays: List of NumPy arrays to convert.
        :return: List of converted TensorFlow tensors.
        """

        return [jnp.array(array.astype(self.np_dtype)) for array in arrays]

    def loss_fn(self, inputs, loss, **functions):
        """Compute the loss function based on given inputs and functions.

        :param inputs: Input data for computing the loss.
        :param loss: Loss variable.
        :param functions: Additional functions required for loss computation.
        """

        pass

    def requires_grad(self, x, t, enable_grad=True):
        """Set the requires_grad attribute for tensors in the input list.

        :param x: List of tensors to modify requires_grad attribute.
        :param t: Tensor to modify requires_grad attribute.
        :param enable_grad: Boolean indicating whether to enable requires_grad or not.
        :return: Modified list of tensors and tensor.
        """
        if t is not None:
            t = t.requires_grad_(enable_grad)
        x = [x_.requires_grad_(enable_grad) for x_ in x]

        return x, t

    @property
    def mean(self):
        """Calculate the mean of the concatenated input data along each column.

        :return: A numpy array containing the mean values along each column.
        """

        x, t, _ = self[:]
        inputs = np.concatenate((*x, t), 1).astype(np.float32)

        return inputs.mean(0, keepdims=True)

    @property
    def std(self):
        """Calculate the standard deviation of the concatenated input data along each column.

        :return: A numpy array containing the standard deviation values along each column.
        """

        x, t, _ = self[:]
        inputs = np.concatenate((*x, t), 1).astype(np.float32)

        return inputs.std(0, keepdims=True)

    
    def shuffle(self):
        # Get random permutation indices
        random_indices = jax.random.permutation(self.rng, jnp.arange(len(self.spatial_domain_sampled[0])))
        
        # Shuffle spatial_domain_sampled
        self.spatial_domain_sampled = [jnp.take(spatial_domain, random_indices, axis=0) 
                                       for spatial_domain in self.spatial_domain_sampled]
        
        # Shuffle time_domain_sampled if it's not None
        if self.time_domain_sampled is not None:
            self.time_domain_sampled = jnp.take(self.time_domain_sampled, random_indices, axis=0)
        
        # Shuffle solution_sampled if it's not None
        if self.solution_sampled is not None:
            self.solution_sampled = [jnp.take(solution, random_indices, axis=0) 
                                     for solution in self.solution_sampled]


        
    def __len__(self):
        """Get the number of sampled data points.

        :return: The number of sampled data points.
        """

        return len(self.spatial_domain_sampled[0])

    def __getitem__(self, idx):
        """Get a specific sampled data point using indexing. In some cases, we may not have
        `time_domain` and `solution_domain`. For example, in periodic boundary condition, there is
        not `solution_domain`.

        :param idx: Index of the desired data point.
        :return: Tuple containing spatial, time, and solution data for the indexed point.
        """

        spatial_domain = [spatial_domain[idx] for spatial_domain in self.spatial_domain_sampled]

        time_domain = None
        if self.time_domain_sampled is not None:
            time_domain = self.time_domain_sampled[idx]

        solution_domain = None
        if self.solution_sampled is not None:
            solution_domain = {
                solution_name: self.solution_sampled[i][idx]
                for i, solution_name in enumerate(self.solution_names)
            }

        return (spatial_domain, time_domain, solution_domain)
