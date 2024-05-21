import os

HOME_DIR = os.path.expanduser("~")
RUN_DIR = "/run/user/%d/" % os.getuid()

# project_dir
project_dir = os.path.dirname(os.path.abspath(__file__))

# most used software path
trinity_path = "Trinity"

hisat2_path = "hisat2"
hisat2_build_path = "hisat2-build"

busco_path = "busco"
busco_download_dir = "/lustre/home/xuyuxing/Database/busco/busco_downloads"

stringtie_path = "stringtie"
gtf_to_alignment_gff3_perl_script = "gtf_to_alignment_gff3.pl"

fasttree_path = "FastTree"
raxml_path = "raxmlHPC-PTHREADS-SSE3"
clustalo_path = "clustalo"
clustalw_path = "clustalw2"
trimal_path = "trimal"
treebest_path = "treebest"
ascp_path = "/lustre/home/xuyuxing/.aspera/connect/bin/ascp"
wget_path = "wget"
mcl_path = ""
RNAfold_path = "RNAfold"
blast_path = ""
gce_dir_path = "/lustre/home/xuyuxing/Program/GCE/gce-1.0.0/"
samtools_path = "samtools"
fasta_path = "fasta36"
ssearch_path = "ssearch36"
treeshrink_path = "run_treeshrink.py"
cd_hit_dir_path = "/lustre/home/xuyuxing/Program/cd-hit/cd-hit-v4.8.1-2019-0228"
pfam_db_file = '/lustre/home/xuyuxing/Database/Interpro/interproscan-5.39-77.0/data/pfam/32.0/pfam_a.hmm'
esearch_path = "esearch"
efetch_path = "efetch"
badirate_path = "/lustre/home/xuyuxing/Program/badirate/badirate-master/BadiRate.pl"
cutadapt_path = "cutadapt"
trf_path = 'trf'
diamond_path = 'diamond'

# sqlite

sqlite_temp_store_directory = os.path.join(HOME_DIR, '.toolbiox_tmp/sqlite_tmp_folder')
if not os.path.exists(os.path.join(HOME_DIR, '.toolbiox_tmp')):
    os.makedirs(os.path.join(HOME_DIR, '.toolbiox_tmp'))
if not os.path.exists(sqlite_temp_store_directory):
    os.makedirs(sqlite_temp_store_directory)

# gene_painter
gene_painter_path = 'ruby /lustre/home/xuyuxing/Program/genepainter/gene_painter/gene_painter.rb'

# dlcpar_search
dlcpar_search_path = "dlcpar_search"

# ncbi taxon database
taxon_nr_db="/lustre/home/xuyuxing/Database/NCBI/nr/2020/nr.taxon.dmnd"
taxon_dump="/lustre/home/xuyuxing/Database/NCBI/nr/2020/taxdmp"

# Easy PlantTribes
hmmsearch_path="hmmsearch"
hmmbuild_path="hmmbuild"
hmmpress_path="hmmpress"
cap3_path="cap3"
transdecoder_path="TransDecoder.LongOrfs"
gt_path="gt"
plant_tribes_scaffold_dir="/lustre/home/xuyuxing/Program/PlantTribes/PlantTribes_scaffolds"
plant_tribes_default_scaffold="26Gv2.0"
assembly_post_processor='AssemblyPostProcessor'
assembly_post_processor_xyx='AssemblyPostProcessor.xyx'
gene_family_classifier='GeneFamilyClassifier'