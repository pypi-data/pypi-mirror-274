import scanpy as sc
import decoupler as dc

import pandas as pd
import seaborn as sns
import re
from anndata import AnnData
from functools import cache

import hdf5plugin
import infercnvpy as cnv
import anndata
import matplotlib.pyplot as plt
import wget

import warnings
from functools import cache
warnings.filterwarnings('ignore')

class scrun():
    def __init__(self, names, path):
        print('Scrublets detection and removal...')
        sam = []
        for i in names:
            sam.append(int(names[0]))
        
        samr = []
        k = 0
        for i in names:
            sam[k] = sc.read_10x_h5(path+i+ '.h5', genome='GRCh38')
            samr.append(sam[k])
            k += 1
        
        for i in samr:
            adata = i
            adata.var_names_make_unique()
            sc.external.pp.scrublet(adata)
            adata = adata[adata.obs['predicted_doublet'] == False]
        
        print('Quality control...')
    
        for i in samr:
            adata = i
            adata.var['mt'] = adata.var_names.str.startswith(('mt-', 'MT-'))
            adata.var['ribo'] = adata.var_names.str.startswith(('Rps', 'Rpl', 'RPS', 'RPL'))
            adata.var["hb"] = adata.var_names.str.contains(("^HB[^(P)]"))
            sc.pp.calculate_qc_metrics(adata, qc_vars=['mt', 'ribo'], inplace=True, percent_top='', log1p =False)
            plt.gcf().canvas.draw()
            sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt', 'pct_counts_ribo'],
                     jitter=0.4, multi_panel=True,
                     #save = 'pre_QC.png'
                     )
            plt.gcf().canvas.draw()
            mit = int(input("Select the maximum percentage of mitochondrial genes:"))
            rib = int(input("Select the maximum percentage of ribosomal genes:"))
        
            adata = adata[(adata.obs.pct_counts_mt < mit) & (adata.obs.pct_counts_ribo < rib), :]
            sc.pp.filter_cells(adata, min_genes=6)
            sc.pp.filter_genes(adata, min_cells=5)
            plt.gcf().canvas.draw()
            sc.pl.scatter(adata, x='total_counts', y='n_genes_by_counts',
                          #save = 'pre.sactterQC2.png'
                          )
            plt.gcf().canvas.draw()
            ng = int(input("Select the maximum number genes by counts:"))
        
            adata = adata[adata.obs.n_genes_by_counts < ng, :]
            if 'n_genes_by_counts' in adata.obs.columns:
                adata.obs['n_genes'] = adata.obs['n_genes_by_counts']
        print('Performing PCA and leiden clustering...')
        
        for i in samr:
            adata = i
            sc.pp.normalize_total(adata, target_sum=1e4)
            sc.pp.log1p(adata)
            adata.raw = adata
        
            sc.tl.pca(adata, svd_solver='arpack')
        
            sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
            sc.tl.umap(adata)
            sc.tl.leiden(adata)
          
        markers = dc.get_resource('PanglaoDB')
        
        markers  = markers[markers['cell_type'].isin(
              [ 'Adipocytes', 'Adrenergic neurons', 'Airway epithelial cells','Airway smooth muscle cells', 'Alpha cells', 'Alveolar macrophages','B cells', 'B cells memory', 'B cells naive',
               'Basal cells', 'Basophils',  'Beta cells', 'Chondrocytes', 'Dendritic cells', 'Distal tubule cells', 'Ductal cells', 'Embryonic stem cells',
               'Endothelial cells', 'Endothelial cells (aorta)', 'Eosinophils', 'Epithelial cells', 'Fibroblasts', 'Gamma delta T cells',
            'Hemangioblasts', 'Hematopoietic stem cells','Hepatic stellate cells', 'Hepatoblasts', 'Luminal epithelial cells', 'Macrophages', 'Mast cells', 'Megakaryocytes',
               'Melanocytes',  'Microfold cells', 'Monocytes', 'Myeloid-derived suppressor cells', 'Myoblasts', 'Myocytes',
            'Myoepithelial cells', 'Myofibroblasts', 'Natural killer T cells','Neutrophils', 'NK cells', 'Nuocytes', 'Olfactory epithelial cells', 'Plasma cells',
               'Plasmacytoid dendritic cells', 'Platelets','Pluripotent stem cells', 'Podocytes',  'Red pulp macrophages', 'Reticulocytes',
               'Sebocytes',  'Smooth muscle cells',  'Stromal cells',  'T cytotoxic cells',
               'T follicular helper cells', 'T helper cells', 'T memory cells',
               'T regulatory cells', 'Thymocytes', 'Transient cells', 'Vascular smooth muscle cells'
               ])
               ]
        immune =[ 'Alveolar macrophages', 'B cells', 'B cells memory',
                   'B cells naive', 'Basal cells', 'Basophils',
                'Dendritic cells', 'Embryonic stem cells', 'Endothelial cells',
                'Eosinophils','Fibroblasts', 'Gamma delta T cells',
               'Macrophages', 'Monocytes', 'Myeloid-derived suppressor cells',
               'Myocytes',  'Natural killer T cells', 'Neutrophils', 'NK cells', 'Nuocytes',
                'Plasma cells','Plasmacytoid dendritic cells', 'Platelets',
                'Red pulp macrophages', 'Reticulocytes',  'T cytotoxic cells',
               'T follicular helper cells', 'T helper cells', 'T memory cells',
               'T regulatory cells', 'Thymocytes', 'Transient cells',
               ]
        # Filter by canonical_marker and human
        markers = markers[markers['human'].isin(['True'])]
        #&(markers['canonical_marker']=='True')
          
        # Remove duplicated entries
        markers = markers[~markers.duplicated(['cell_type', 'genesymbol'])]
        print('Cell types annotation...')
        
        for i in samr:
            adata = i
            dc.run_ora(mat=adata, net=markers, source='cell_type', target='genesymbol', min_n=2, verbose=True)
            acts = dc.get_acts(adata, obsm_key='ora_estimate')
            mean_enr = dc.summarize_acts(acts, groupby='leiden', min_std=1)
        
            annotation_dict = dc.assign_groups(mean_enr)
        
            adata.obs['cell_type'] = [annotation_dict[clust] for clust in adata.obs['leiden']]
        
            adata.var['start'] = 0
            adata.var['end'] = 0
            adata.var['chromosome'] = '0'
          
        filename = wget.download('https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_44/gencode.v44.annotation.gff3.gz')
        gencode = pd.read_table(filename, comment="#",
                                  sep = "\t",
                                  names = ['seqname', 'source', 'feature', 'start' , 'end', 'score', 'strand', 'frame', 'attribute']
                                  )
          
        #/content/drive/MyDrive/gencode.v44.annotation.gff3.gz
        gencode_genes = gencode[(gencode.feature == "gene")][['seqname', 'start', 'end', 'attribute']].copy().reset_index().drop('index', axis=1) # Extract genes
          
        def gene_info(x):
            # Extract gene names
            g_name = list(filter(lambda x: 'gene_name' in x,  x.split(";")))[0].split("=")[1]
            g_type = list(filter(lambda x: 'gene_type' in x,  x.split(";")))[0].split("=")[1]
            #g_status = list(filter(lambda x: 'gene_status' in x,  x.split(";")))[0].split("=")[1]
            # g_leve = int(list(filter(lambda x: 'level' in x,  x.split(";")))[0].split("=")[1])
            return (g_name, g_type)
          
        gencode_genes["gene_name"], gencode_genes["gene_type"] = zip(*gencode_genes.attribute.apply(lambda x: gene_info(x)))
          
        @cache
        def lis(l):
            ll = []
            for i in l:
              if i in gencode_genes.gene_name.tolist():
                ll.append(i)
            return ll
          
        @cache
        def chro(list):
            c = []
            for j in list:
              c.append(gencode_genes[gencode_genes['gene_name'] == j].seqname.tolist()[0])
            return c
          
        @cache
        def sta(list):
            c = [gencode_genes[gencode_genes['gene_name'] == j].start.tolist()[0] for j in list]
            return c
          
        @cache
        def en(list):
            c = []
            for j in list:
              c.append(gencode_genes[gencode_genes['gene_name'] == j].end.tolist()[0])
            return c
          
        print('Annotation of gene locations...')
        
        for i in samr:
            adata = i
        
            l = tuple(adata.var.index.tolist())
            l1 = lis(l)
        
            adata.var['chromosome'].loc[l1] = chro(tuple(l1))
            adata.var['start'].loc[l1] = sta(tuple(l1))
            adata.var['end'].loc[l1] = en(tuple(l1))
          
        print('Infercnv calculations...')
          
        
        for i in samr:
            adata = i
            reference_cat = []
            
            for j in adata.obs['cell_type'].unique():
                if j in immune:
                    reference_cat.append(j)
        
            cnv.tl.infercnv(
            adata,
            reference_key="cell_type",
            reference_cat=reference_cat,
            window_size=250,
            )
        
            cnv.tl.pca(adata)
            cnv.pp.neighbors(adata)
            cnv.tl.leiden(adata)
        
            cnv.tl.umap(adata)
            cnv.tl.cnv_score(adata)
          
        k = 0
        for i in samr:
            adata = i
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 11))
            ax4.axis("off")
            fig.suptitle(names[k], fontsize=22)
            cnv.pl.umap(
                adata,
                color="cnv_leiden",
                legend_loc="on data",
                legend_fontoutline=2,
                ax=ax1,
               show=False,
            #save = 'firi_R_'+str(i)'cnvscore.png'
            )
            cnv.pl.umap(adata, color="cnv_score", ax=ax2, show=False)
            cnv.pl.umap(adata, color="cell_type", ax=ax3)
        
            fig.savefig(path+names[k]+'cnv.png', dpi=300,  facecolor ='w')
        
            k = k+1
            
        k = 0
          
        for i in samr:
            adata = i
            reference_cat = []
            for j in adata.obs['cell_type'].unique():
                if j in immune:
                    reference_cat.append(j)
        
            cnv.tl.infercnv(
            adata,
            reference_key="cell_type",
            reference_cat=reference_cat,
            window_size=250,
            )
        
            cnv.tl.infercnv(
            adata,
            reference_key="cell_type",
            reference_cat=reference_cat,
            window_size=250,
            )
        
            print(names[k])
        
            cnv.pl.chromosome_heatmap(adata, dendrogram=True,
                                save = (names[k]+'.png')
                                 )
        
        
        
            k = k+1
        k = 0
          
        for i in samr:
            tc = str(input('Set the tumor clusters for '+str(names[k])+', please:'))
            tcc = tc.split(',')
            adata = i
            adata.obs["cnv_status"] = "normal"
            adata.obs.loc[
                adata.obs["cnv_leiden"].isin(tcc), "cnv_status"
                ] = "tumor"
            k += 1
          
        k = 0 
        for i in samr:
            i.obs['sample'] = names[k]
            k += 1
          
        print('Concatenate the data..')
          
        adata = sc.concat(samr, join="outer")
          
        adata.obs['celltype'] = 0
        adata.obs['cell_type'].astype("category")
        for i in adata.obs.index:
            if adata.obs[adata.obs.index == i].cnv_status.tolist()[0] == 'tumor':
                adata.obs['celltype'].loc[i] = 'Tumor'
            else:
                adata.obs['celltype'].loc[i] = adata.obs['cell_type'].loc[i]
                
        save_name = str(input("Enter the name to save the data: "))
        adata.write_h5ad(
            path+save_name,
            compression=hdf5plugin.FILTERS["zstd"]
              )