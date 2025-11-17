
#!/usr/bin/env python3
"""repeated_measures_anova.py

Reproducible script to run repeated-measures ANOVA and post-hoc tests on NASA-TLX.
Saves results to specified output directory.
"""
import argparse
from pathlib import Path
import pandas as pd
import numpy as np
from statsmodels.stats.anova import AnovaRM
from scipy import stats
from statsmodels.stats.multitest import multipletests

def run_anova(csv_path, out_dir):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path)
    if not {'participantId','task_id','tlx'}.issubset(df.columns):
        raise ValueError("CSV must contain columns: participantId, task_id, tlx")
    task_map = {"task_1_form": "T1_form", "task_2_product": "T2_product", "task_3_travel": "T3_travel"}
    df['task_short'] = df['task_id'].map(task_map).fillna(df['task_id'])
    wide = df.pivot(index='participantId', columns='task_short', values='tlx').reset_index()
    wide.to_csv(out_dir / "tlx_wide_table.csv", index=False)
    aov_df = df[['participantId','task_short','tlx']].dropna()
    aov = AnovaRM(aov_df, depvar='tlx', subject='participantId', within=['task_short']).fit()
    with open(out_dir / "repeated_measures_anova_summary.txt", "w") as f:
        f.write(aov.summary().as_text())
    pairs = [("T1_form","T2_product"), ("T1_form","T3_travel"), ("T2_product","T3_travel")]
    tt_records = []; pvals = []
    for a,b in pairs:
        if a not in wide.columns or b not in wide.columns:
            tt_records.append({"pair": f"{a} vs {b}", "n": 0, "t": None, "p_uncorrected": None, "mean_diff": None, "dz": None})
            pvals.append(1.0); continue
        x = wide[a].dropna(); y = wide[b].dropna(); common_idx = x.index.intersection(y.index)
        x = x.loc[common_idx]; y = y.loc[common_idx]
        t, p = stats.ttest_rel(x, y)
        diff = x - y
        dz = (diff.mean()) / (diff.std(ddof=1)) if (diff.std(ddof=1) != 0) else np.nan
        tt_records.append({"pair": f"{a} vs {b}", "n": len(common_idx), "t": float(t), "p_uncorrected": float(p), "mean_diff": float(diff.mean()), "dz": float(dz)})
        pvals.append(p)
    rej, pvals_corrected, _, _ = multipletests(pvals, alpha=0.05, method='holm')
    for i, rec in enumerate(tt_records):
        rec["p_holm"] = float(pvals_corrected[i]); rec["reject_holm"] = bool(rej[i])
    tt_df = pd.DataFrame(tt_records); tt_df.to_csv(out_dir / "posthoc_paired_ttests_holm.csv", index=False)
    aov_table = aov.anova_table
    F_val = aov_table['F Value'][0]; p_val = aov_table['Pr > F'][0]
    df1 = aov_table['Num DF'][0]; df2 = aov_table['Den DF'][0]
    interpretation = f"Interpretation Summary:\nRepeated-measures ANOVA on NASA-TLX across tasks produced F({int(df1)},{int(df2)}) = {F_val:.3f}, p = {p_val:.4g}.\nPairwise comparisons (paired t-tests) with Holm correction:\n{tt_df.to_string(index=False)}\n\nConclusion: Hypothesis T1 < T2 < T3 is {'supported' if (tt_df.loc[tt_df['pair']=='T1_form vs T2_product','p_holm'].values[0] < 0.05 and tt_df.loc[tt_df['pair']=='T1_form vs T3_travel','p_holm'].values[0] < 0.05 and tt_df.loc[tt_df['pair']=='T2_product vs T3_travel','p_holm'].values[0] < 0.05) else 'not fully supported'}."
    with open(out_dir / "interpretation_summary_detailed.txt", "w") as f:
        f.write(interpretation)
    return out_dir

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, default='./data/processed/modeling_dataset_ultrarealistic.csv')
    parser.add_argument('--out-dir', type=str, default='./analysis/results')
    args = parser.parse_args()
    run_anova(args.csv, args.out_dir)
