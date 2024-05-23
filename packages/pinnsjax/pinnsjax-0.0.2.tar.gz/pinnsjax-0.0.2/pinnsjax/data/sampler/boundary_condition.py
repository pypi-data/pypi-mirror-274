import numpy as np
import jax.numpy as jnp
import jax
from pinnsjax import utils

from .sampler_base import SamplerBase


class DirichletBoundaryCondition(SamplerBase):
    """Initialize Dirichlet boundary condition."""

    def __init__(
        self,
        mesh,
        solution,
        num_sample: int = None,
        idx_t: int = None,
        boundary_fun=None,
        discrete: bool = False,
        dtype: str = 'float32'
    ):
        """Initialize a mesh sampler for collecting training data in upper and lower boundaries for
        Dirichlet boundary condition.

        :param mesh: Instance of the mesh used for sampling.
        :param solution: Names of the solution outputs.
        :param num_sample: Number of samples to generate.
        :param idx_t: Index of the time step for discrete mode.
        :param boundary_fun: A function can apply on boundary data.
        :param discrete: It is a boolean that is true when problem is discrete.
        """

        super().__init__(dtype)

        self.solution_names = solution
        self.discrete = discrete

        spatial_upper_bound, time_upper_bound, solution_upper_bound = mesh.on_upper_boundary(
            self.solution_names
        )
        spatial_lower_bound, time_lower_bound, solution_lower_bound = mesh.on_lower_boundary(
            self.solution_names
        )

        spatial_bound = np.vstack([spatial_upper_bound, spatial_lower_bound])
        time_bound = np.vstack([time_upper_bound, time_lower_bound])

        solution_bound = {}
        for solution_name in self.solution_names:
            solution_bound[solution_name] = np.vstack(
                [solution_upper_bound[solution_name], solution_lower_bound[solution_name]]
            )

        if boundary_fun:
            solution_bound = boundary_fun(time_bound)

        self.idx_t = idx_t

        (
            self.spatial_domain_sampled,
            self.time_domain_sampled,
            self.solution_sampled,
        ) = self.sample_mesh(num_sample, (spatial_bound, time_bound, solution_bound))

        self.spatial_domain_sampled = jnp.split(self.spatial_domain_sampled,
                                                indices_or_sections=self.spatial_domain_sampled.shape[1],
                                                axis=1)

        self.solution_sampled = jnp.split(self.solution_sampled, 
                                          indices_or_sections=self.solution_sampled.shape[1], 
                                          axis=1)

    def sample_mesh(self, num_sample, flatten_mesh):
        """Sample the mesh data for training. If idx_t is defined, only points on that time will be
        selected. If num_sample is not defined the whole points will be selected.

        :param num_sample: Number of samples to generate.
        :param flatten_mesh: Flattened mesh data.
        :return: Sampled spatial, time, and solution data.
        """

        flatten_mesh = self.concatenate_solutions(flatten_mesh)

        if self.discrete:
            t_points = len(flatten_mesh[0]) // 2
            flatten_mesh = [
                np.vstack(
                    (
                        flatten_mesh_[self.idx_t : self.idx_t + 1, :],
                        flatten_mesh_[self.idx_t + t_points : self.idx_t + t_points + 1, :],
                    )
                )
                for flatten_mesh_ in flatten_mesh
            ]

        if num_sample is None:
            return self.convert_to_tensor(flatten_mesh)
        else:
            idx = np.random.choice(range(flatten_mesh[0].shape[0]), num_sample, replace=False)
            return self.convert_to_tensor(
                (flatten_mesh[0][idx, :], flatten_mesh[1][idx, :], flatten_mesh[2][idx, :])
            )


    def loss_fn(self, params, inputs, loss, functions):
        """Compute the loss function based on inputs and functions.

        :param inputs: Input data for computing the loss.
        :param loss: Loss variable.
        :param functions: Additional functions required for loss computation.
        :return: Loss variable and outputs dict from the forward pass.
        """

        x, t, u = inputs

        # In discrete mode, we do not use time.
        if self.discrete:
            t = None

        outputs = functions["forward"](params, x, t)

        loss = functions["loss_fn"](loss, outputs, u, keys=self.solution_names)

        return loss, outputs


class PeriodicBoundaryCondition(SamplerBase):
    """Initialize Periodic boundary condition."""

    def __init__(
        self,
        mesh,
        solution,
        idx_t: int = None,
        num_sample: int = None,
        derivative_order: int = 0,
        discrete: bool = False,
        dtype: str = 'float32'
    ):
        super().__init__(dtype)
        """Initialize a mesh sampler for collecting training data in upper and lower boundaries for
        periodic boundary condition.

        :param mesh: Instance of the mesh used for sampling.
        :param solution: Names of the solution outputs.
        :param num_sample: Number of samples to generate.
        :param idx_t: Index of the time step for discrete mode.
        :param boundary_fun: A function can apply on boundary data.
        :param discrete: It is a boolean that is true when problem is discrete.
        """

        self.derivative_order = derivative_order
        self.idx_t = idx_t
        self.solution_names = solution

        spatial_upper_bound, time_upper_bound, _ = mesh.on_upper_boundary(self.solution_names)
        spatial_lower_bound, time_lower_bound, _ = mesh.on_lower_boundary(self.solution_names)

        self.discrete = discrete

        (self.spatial_domain_sampled, self.time_domain_sampled) = self.sample_mesh(
            num_sample,
            (spatial_upper_bound, time_upper_bound, spatial_lower_bound, time_lower_bound),
        )

        self.mid = len(self.time_domain_sampled) // 2
        self.spatial_domain_sampled = jnp.split(self.spatial_domain_sampled,
                                                indices_or_sections=self.spatial_domain_sampled.shape[1],
                                                axis=1)


    def sample_mesh(self, num_sample, flatten_mesh):
        """Sample the mesh data for training.

        :param num_sample: Number of samples to generate.
        :param flatten_mesh: Flattened mesh data.
        :return: Sampled spatial, time, and solution data.
        """

        if self.discrete:
            flatten_mesh = [
                flatten_mesh_[self.idx_t : self.idx_t + 1, :] for flatten_mesh_ in flatten_mesh
            ]

        if num_sample is None:
            return self.convert_to_tensor(
                (
                    np.vstack((flatten_mesh[0], flatten_mesh[2])),
                    np.vstack((flatten_mesh[1], flatten_mesh[3])),
                )
            )
        else:
            idx = np.random.choice(range(flatten_mesh[0].shape[0]), num_sample, replace=False)
            return self.convert_to_tensor(
                (
                    np.vstack((flatten_mesh[0][idx, :], flatten_mesh[2][idx, :])),
                    np.vstack((flatten_mesh[1][idx, :], flatten_mesh[3][idx, :])),
                )
            )

    def loss_fn(self, params, inputs, loss, functions):
        """Compute the loss function based on inputs and functions.

        :param inputs: Input data for computing the loss.
        :param loss: Loss variable.
        :param functions: Additional functions required for loss computation.
        :return: Loss variable and outputs dict from the forward pass.
        """

        x, t, _ = inputs

        # In discrete mode, we do not use time.
        if self.discrete:
            t = None

        outputs = functions["forward"](params, x, t)
        
        if self.derivative_order > 0:
            for solution_name in self.solution_names:
                if self.discrete:
                    outputs[f"{solution_name}-tmp"] = jax.vmap(utils.fwd_gradient(functions['functional_net'],
                                                        argnums=1,
                                                        order=1),
                                     in_axes = functions['functional_net'].in_axes_discrete)(params, *x, None, solution_name)
                else:
                    outputs[f"{solution_name}-tmp"] = jax.vmap(utils.gradient(functions['functional_net'],
                                                               argnums=1,
                                                               order=1),
                                              in_axes = functions['functional_net'].in_axes_gard)(params, *x, t, solution_name)
                    
                loss = functions["loss_fn"](loss, outputs, keys=[f"{solution_name}-tmp"], mid=self.mid)
        loss = functions["loss_fn"](loss, outputs, keys=self.solution_names, mid=self.mid)
                
        return loss, outputs
