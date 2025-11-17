#!/usr/bin/env python3
"""
behavioral_pattern_discovery.py

Compute correlations between engineered behavioral features and NASA-TLX,
produce per-task correlations, save CSV tables, produce heatmap and boxplots
for top features, write APA-style interpretations, and zip figures for download.

Usage:
    python behavioral_pattern_discovery.py --csv /path/to/modeling_dataset_ultrarealistic.csv --out /path/to/output_dir

Outputs (default saved under ./analysis/behavioral_patterns/):
 - feature_correlation_matrix_pearson.csv
 - correlations_overall_pearson.csv
 - correlations_overall_spearman.csv
 - correlations_by_task_pearson.csv
 - top_features_summary.csv
 - correlation_matrix_heatmap.png
 - boxplot_<feature>.png (for top features)
 - figures_package.zip
 - interpretation_apa.txt
"""

import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import zipfile, os, json

sns.set(style="whitegrid")

def run(csv_path, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    df = pd.read_csv(csv_path)
    required = {'participantId','task_id','tlx'}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required}")

    # Identify feature columns
    meta_cols = {'participantId','task_id','tlx','High_Load','shap_cluster'}
    feature_cols = [c for c in df.columns if c not in meta_cols]
    # Ensure numeric
    for c in feature_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    # Overall correlations (Pearson & Spearman) vs TLX
    pearson_results = []
    spearman_results = []
    for c in feature_cols:
        valid = df[['tlx', c]].dropna()
        if len(valid) < 3:
            pearson_results.append((c, np.nan, np.nan))
            spearman_results.append((c, np.nan, np.nan))
            continue
        r, p = stats.pearsonr(valid['tlx'], valid[c])
        rho, p2 = stats.spearmanr(valid['tlx'], valid[c])
        pearson_results.append((c, r, p))
        spearman_results.append((c, rho, p2))

    pearson_df = pd.DataFrame(pearson_results, columns=['feature','pearson_r','pearson_p']).sort_values('pearson_r', key=abs, ascending=False)
    spearman_df = pd.DataFrame(spearman_results, columns=['feature','spearman_rho','spearman_p']).sort_values('spearman_rho', key=abs, ascending=False)

    pearson_df.to_csv(out_dir / "correlations_overall_pearson.csv", index=False)
    spearman_df.to_csv(out_dir / "correlations_overall_spearman.csv", index=False)

    # Correlation matrix (features + tlx)
    corr_matrix = df[['tlx'] + feature_cols].corr(method='pearson')
    corr_matrix.to_csv(out_dir / "feature_correlation_matrix_pearson.csv")

    # Per-task correlations
    per_task_records = []
    for task in df['task_id'].unique():
        sub = df[df['task_id']==task]
        for c in feature_cols:
            valid = sub[['tlx', c]].dropna()
            if len(valid) < 3:
                r = np.nan; p = np.nan
            else:
                r, p = stats.pearsonr(valid['tlx'], valid[c])
            per_task_records.append({'task_id': task, 'feature': c, 'pearson_r': r, 'pearson_p': p, 'n': len(valid)})
    per_task_df = pd.DataFrame(per_task_records)
    per_task_df.to_csv(out_dir / "correlations_by_task_pearson.csv", index=False)

    # Top features by absolute Pearson r
    pearson_df['abs_r'] = pearson_df['pearson_r'].abs()
    top_features = pearson_df.sort_values('abs_r', ascending=False).head(8)['feature'].tolist()

    # Save top features summary with per-task r
    summary_records = []
    for feat in top_features:
        overall = pearson_df[pearson_df['feature']==feat].iloc[0]
        per_t = per_task_df[per_task_df['feature']==feat].set_index('task_id')['pearson_r'].to_dict()
        rec = {'feature': feat, 'pearson_r_overall': overall['pearson_r'], 'pearson_p_overall': overall['pearson_p']}
        for k,v in per_t.items():
            rec[f"r_{k}"] = v
        summary_records.append(rec)
    summary_df = pd.DataFrame(summary_records)
    summary_df.to_csv(out_dir / "top_features_summary.csv", index=False)

    # Heatmap plot
    plt.figure(figsize=(12,10))
    sns.heatmap(corr_matrix, cmap='coolwarm', center=0)
    plt.title('Pearson correlation matrix: TLX and behavioral features')
    plt.tight_layout()
    heatmap_path = fig_dir / "correlation_matrix_heatmap.png"
    plt.savefig(heatmap_path, dpi=200, bbox_inches='tight')
    plt.close()

    # Boxplots for top features across tasks
    boxplot_paths = []
    tasks_order = sorted(df['task_id'].unique())
    for feat in top_features:
        plt.figure(figsize=(8,6))
        sns.boxplot(x='task_id', y=feat, data=df, order=tasks_order, showfliers=False)
        sns.swarmplot(x='task_id', y=feat, data=df, order=tasks_order, color='k', alpha=0.6)
        plt.title(f'Distribution of {feat} by task')
        plt.xlabel('Task'); plt.ylabel(feat)
        path = fig_dir / f"boxplot_{feat}.png"
        plt.savefig(path, dpi=200, bbox_inches='tight')
        plt.close()
        boxplot_paths.append(str(path.name))

    # APA-style interpretation text
    lines = []
    lines.append("Behavioral Pattern Discovery — APA-style interpretation\\n")
    lines.append("Overall strongest correlations with NASA-TLX (Pearson r):\\n")
    for i, row in pearson_df.head(8).iterrows():
        feat = row['feature']; r = row['pearson_r']; p = row['pearson_p']
        direction = 'positively' if r > 0 else 'negatively'
        lines.append(f\"- {feat}: {direction} correlated with TLX (r = {r:.2f}, p = {p:.3g})\\n\")
    lines.append("\\nPer-task observations:\\n")
    for feat in top_features:
        per = per_task_df[per_task_df['feature']==feat].set_index('task_id')['pearson_r'].to_dict()
        lines.append(f\"- {feat}: per-task r -> {json.dumps(per)}\\n\")
    lines.append('\\nNotes: dataset is synthetic; validate with real-users for publication.\\n')
    (out_dir / "interpretation_apa.txt").write_text('\\n'.join(lines))

    # Zip figures
    zip_path = out_dir / "figures_package.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(fig_dir)):
            zf.write(fig_dir / f, arcname=f)

    # Return key outputs
    return {
        "out_dir": str(out_dir),
        "corr_matrix_csv": str(out_dir / "feature_correlation_matrix_pearson.csv"),
        "pearson_csv": str(out_dir / "correlations_overall_pearson.csv"),
        "spearman_csv": str(out_dir / "correlations_overall_spearman.csv"),
        "per_task_csv": str(out_dir / "correlations_by_task_pearson.csv"),
        "top_summary_csv": str(out_dir / "top_features_summary.csv"),
        "heatmap_png": str(heatmap_path),
        "boxplots": boxplot_paths,
        "figures_zip": str(zip_path),
        "interpretation": str(out_dir / "interpretation_apa.txt")
    }

def main():
    parser = argparse.ArgumentParser(description='Behavioral Pattern Discovery analysis')
    parser.add_argument('--csv', type=str, default='/mnt/data/modeling_dataset_ultrarealistic.csv', help='Path to modeling CSV')
    parser.add_argument('--out', type=str, default='/mnt/data/analysis/behavioral_patterns', help='Output folder')
    args = parser.parse_args()
    res = run(args.csv, args.out)
    print('Saved outputs:')
    for k,v in res.items():
        print(f' - {k}: {v}')

if __name__ == '__main__':
    import argparse
    main()
