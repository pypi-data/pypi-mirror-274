## Scprel - Single-Cell Data Preprocessing in Python

### Import scprel as:

    import scprel

This package allows to perform basic preprocessing steps for single-cell analysis of multiple samples. It includes scrublets detection, quality control, normalization with `target_sum=1e4`, leiden clustering, annotation of cell types with [PanglaoDB](https://panglaodb.se/) database and infercnv calculations. It integrates some of the [`Scanpy`](https://scanpy.readthedocs.io/en/stable/), [`Decoupler`](https://decoupler-py.readthedocs.io/en/latest/), [`Infercnvpy`](https://infercnvpy.readthedocs.io/en/latest/infercnv.html) and [`Anndata`](https://anndata.readthedocs.io/en/latest/concatenation.html) functions. It is designed to facilitate workflow when analyzing multiple samples. Each sample is analyzed and annotated separately and then all samples are concatenated.

### Example of usage:

    scprel.scrun(names = ['sample1', 'sample2'], path = '/content/drive/MyDrive/MyDirectory/')

* `names` - *list of sample names in your directory (.h5 format);* 
* `path` - *path to the directory with samples*

The result of this function is the [`anndata.AnnData`](https://anndata.readthedocs.io/en/stable/generated/anndata.AnnData.html#anndata.AnnData) object, compressed with [`hdf5plugin`](https://pypi.org/project/hdf5plugin/), with concatenated samples, filtered by 'mt' and 'ribo' genes, with annotated gene locations and annotated tumor cells based on cnv score. All immune cells in the sample are considered reference cells for infercnv calculations.

![The obs table for resulting adata file](https://raw.githubusercontent.com/ronnaug/1/Genomic_data_analysis/Example_table.png)

*The resulting file will be saved in your default home directory and is ready for batch correction and further analysis.*