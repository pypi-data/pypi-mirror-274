import numpy as np
import xarray as xr
import arviz as az
from matplotlib import pyplot as plt

from pymob.utils.plot_helpers import plot_hist, plot_loghist

def cluster_chains(posterior, deviation="std"):
    assert isinstance(posterior, (xr.DataArray, xr.Dataset))
    chain_means = posterior.mean(dim="draw")
    if deviation == "std":
        chain_dev = posterior.std(dim="draw")
    elif "frac:" in deviation:
        _, frac = deviation.split(":")
        chain_dev = chain_means * float(frac)
    else:
        raise ValueError("Deviation method not implemented.")    

    global cluster_id
    cluster_id = 1
    cluster = [cluster_id] * len(posterior.chain)
    unclustered_chains = posterior.chain.values

    def recurse_clusters(unclustered_chains):
        global cluster_id
        compare = unclustered_chains[0]
        new_cluster = []
        for i in unclustered_chains[1:]:
            a = chain_means.sel(chain=compare) + chain_dev.sel(chain=compare) > chain_means.sel(chain=i)
            b = chain_means.sel(chain=compare) - chain_dev.sel(chain=compare) < chain_means.sel(chain=i)
            isin_dev = (a * b).all()

            if isinstance(isin_dev, xr.Dataset):
                isin_dev = isin_dev.to_array().all()

            if not isin_dev:
                cluster[i] = cluster_id + 1
                new_cluster.append(i)

        cluster_id += 1
        if len(new_cluster) == 0:
            return

        recurse_clusters(new_cluster)
    
    recurse_clusters(unclustered_chains)

    return cluster


def rename_extra_dims(df, extra_dim_suffix="_dim_0", new_dim="new_dim", new_coords=None):
    # TODO: COuld be used for numypro backend for fixing posterior indexes
    df_ = df.copy()
    data_vars = list(df_.data_vars.keys())

    # swap dimension names for all dims that have the suffix 
    new_dims = {}
    for dv in data_vars:
        old_dim = f"{dv}{extra_dim_suffix}"
        if df_.dims[old_dim] == 1:
            df_[dv] = df_[dv].squeeze(old_dim)
        else:
            new_dims.update({old_dim: new_dim})

    df_ = df_.swap_dims(new_dims)

    # assign coords to new dimension
    df_ = df_.assign_coords({new_dim: new_coords})
    
    # drop renamed coords
    df_ = df_.drop([f"{dv}{extra_dim_suffix}" for dv in data_vars])

    return df_



# plot loghist
def plot_posterior_samples(posterior, col_dim=None, log=True, hist_kwargs={}):
    if log:
        hist = plot_loghist
    else:
        hist = plot_hist

    parameters = list(posterior.data_vars.keys())
    samples = posterior.stack(sample=("chain", "draw"))

    fig = plt.figure(figsize=(5, len(parameters)*2))
    fig.subplots_adjust(right=.95, top=.95, hspace=.25)

    gs = fig.add_gridspec(len(parameters), 1)

    for i, key in enumerate(parameters):
        postpar = samples[key]
        if col_dim in postpar.dims:
            col_coords = postpar[col_dim]
            gs_par = gs[i, 0].subgridspec(1, len(col_coords))
            axes = gs_par.subplots()

            for ax, coord in zip(axes, col_coords):
                hist(
                    x=postpar.sel({col_dim: coord}), 
                    name=f"${key}$ {str(coord.values)}",
                    ax=ax,
                    **hist_kwargs
                )

        else:
            gs_par = gs[i, 0].subgridspec(1, 1)
            ax = gs_par.subplots()

            hist(
                x=postpar, 
                name=f"${key}$",
                ax=ax,
                **hist_kwargs
            )


    return fig


def bic(idata: az.InferenceData):
    """calculate the BIC for az.InferenceData. The function will average over
    all samples from the markov chain
    """
    log_likelihood = idata.log_likelihood.mean(("chain", "draw")).sum().to_array().sum()
    k = idata.posterior.mean(("chain", "draw")).count().to_array().sum()

    vars = [i.split("_")[0] for i in list(idata.log_likelihood.data_vars.keys())]
    n = 0
    for v in vars:
        if v in idata.observed_data:
            n += (~idata.observed_data[v].isnull()).sum()
        elif v + "_obs" in idata.observed_data:
            n += (~idata.observed_data[v + "_obs"].isnull()).sum()
        else:
            raise IndexError(f"Variable {v} or {v+'_obs'} not in idata")

    # n = (~idata.observed_data[vars].isnull()).sum().to_array().sum()

    bic = float(k * np.log(n) - 2 * log_likelihood)
    msg = str(
        "Bayesian Information Criterion (BIC)"
        "\n===================================="
        f"\nParameters: {int(k)}"
        f"\nData points: {int(n)}"
        f"\nLog-likelihood: {float(log_likelihood)}"
        f"\nBIC: {bic}"
    )

    return msg, bic


def add_cluster_coordinates(idata, deviation="std"):
    cluster = cluster_chains(idata.posterior, deviation=deviation)
    idata = idata.assign_coords(cluster=("chain", cluster))
    return idata