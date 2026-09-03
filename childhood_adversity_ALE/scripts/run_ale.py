import json, os, sys, warnings, numpy as np
warnings.filterwarnings("ignore")
import logging; logging.getLogger("nimare").setLevel(logging.ERROR)
from nimare.io import convert_sleuth_to_dataset
from nimare.meta.cbma import ALE
from nimare.correct import FWECorrector

VOX_MM3 = 8.0
NITER = 2000

def run(name, sleuth, voxel_thresh):
    ds = convert_sleuth_to_dataset(sleuth)
    est = ALE()
    res = est.fit(ds)
    corr = FWECorrector(method="montecarlo", voxel_thresh=voxel_thresh,
                        n_iters=NITER, n_cores=int(os.environ.get("NC","4")))
    cres = corr.transform(res)
    nd = cres.estimator.null_distributions_
    key_v = [k for k in nd if "values_level-voxel" in k][0]
    key_c = [k for k in nd if "values_desc-size_level-cluster" in k][0]
    ale_thr = float(np.percentile(nd[key_v], 95))
    clus_vox = float(np.percentile(nd[key_c], 95))
    stat = cres.get_map("stat").get_fdata()
    logp = cres.get_map("logp_desc-size_level-cluster_corr-FWE_method-montecarlo").get_fdata()
    z = cres.get_map("z").get_fdata()
    n_surv = int((logp > -np.log10(0.05)).sum())
    out = dict(model=name, k=len(ds.ids), foci=int(ds.coordinates.shape[0]),
               N=int(ds.metadata.sample_sizes.apply(lambda x: x[0]).sum()),
               voxel_thresh=voxel_thresh, n_iters=NITER,
               ale_threshold_voxelFWE=round(ale_thr, 6),
               min_cluster_voxels=int(round(clus_vox)),
               min_cluster_mm3=int(round(clus_vox * VOX_MM3)),
               peak_ale=round(float(np.nanmax(stat)), 6),
               peak_z=round(float(np.nanmax(z)), 4),
               voxels_surviving_clusterFWE=n_surv,
               voxels_surviving_voxelFWE=int((stat > ale_thr).sum()))
    cres.save_maps(output_dir="ale_out", prefix=name)
    return out

if __name__ == "__main__":
    jobs = json.loads(sys.argv[1])
    results = []
    path = "ale_results.json"
    if os.path.exists(path):
        results = json.load(open(path))
    for name, sleuth, vt in jobs:
        r = run(name, sleuth, vt)
        results = [x for x in results if x["model"] != name] + [r]
        json.dump(results, open(path, "w"), indent=1)
        print(name, "done:", r["k"], "exp,", r["foci"], "foci, min cluster",
              r["min_cluster_mm3"], "mm3, ALE thr", r["ale_threshold_voxelFWE"],
              ", surviving voxels", r["voxels_surviving_clusterFWE"])
