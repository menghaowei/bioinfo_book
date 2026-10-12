#!/usr/bin/env python3
"""Export Figure 10.1 from the current chapter's exact Snakefile.

Uses empty input placeholders for DAG construction only: no analysis job runs.
Requires Snakemake (verified with 9.27.0); Graphviz renders rnaseq-dag.dot to SVG.
"""
import argparse
import re
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'assets/10-snakemake-and-reproducibility'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--snakemake',default='snakemake')
    args=parser.parse_args()
    text=(ROOT/'manuscript/10-snakemake-and-reproducibility.md').read_text()
    blocks={m.group(1):m.group(2) for m in re.finditer(r'```\{[^\n]*data-code-title="(rnaseq/[^\"]+)"[^\n]*\}\n(.*?)\n```',text,re.S)}
    with tempfile.TemporaryDirectory(prefix='bioinfo-dag-') as tmp:
        work=Path(tmp)
        for name in ['Snakefile','config.yaml','samples.tsv']:(work/name).write_text(blocks['rnaseq/'+name])
        samples=[s.split('\t')[0] for s in blocks['rnaseq/samples.tsv'].splitlines()[1:] if s.strip()]
        for sample in samples:
            for read in [1,2]:
                f=work/f'raw/{sample}_{read}.fastq.gz';f.parent.mkdir(exist_ok=True);f.touch()
        annotation=re.search(r'^annotation:\s*"?([^"\n]+)',blocks['rnaseq/config.yaml'],re.M).group(1)
        f=work/annotation;f.parent.mkdir(parents=True,exist_ok=True);f.touch()
        process=subprocess.run([args.snakemake,'--dag','--cores','1','--runtime-source-cache-path',str(work/'source-cache')],cwd=work,text=True,capture_output=True)
        if process.returncode:
            raise RuntimeError(process.stderr)
        raw=process.stdout[process.stdout.index('digraph'):].rstrip()+'\n'
    nodes={int(i):label for i,label in re.findall(r'(\d+)\[label\s*=\s*"([^"]+)"',raw)}
    edges=[(int(a),int(b)) for a,b in re.findall(r'\b(\d+)\s*->\s*(\d+)',raw)]
    assert len(nodes)==19 and len(edges)==35,(len(nodes),len(edges))
    group={}
    for i,label in nodes.items():
        if 'sample: ' in label:group[i]=label.split('sample: ')[1]
    for a,b in edges:
        if a in group and nodes[b].split('\\n')[0] in ['hisat2_align','samtools_index']:group[b]=group[a]
    for a,b in edges:
        if a in group and nodes[b].split('\\n')[0]=='samtools_index':group[b]=group[a]
    dot=['digraph snakemake_dag {',
         'graph [rankdir=TB, bgcolor="transparent", ranksep=0.50, nodesep=0.20, margin=0.08, compound=true];',
         'node [shape=box, style="rounded,filled", fillcolor="#e8f4f1", color="#186254", fontcolor="#333333", fontname="Arial", fontsize=15, margin="0.13,0.13", penwidth=1.4];',
         'edge [color="#6b7280", penwidth=1.1, arrowsize=0.6];']
    for sample in samples:
        ids=[i for i in nodes if group.get(i)==sample]
        dot.append(f'subgraph cluster_{sample} {{ label="{sample}"; fontname="Arial"; fontsize=17; color="#9ca3af"; style=rounded;')
        for i in ids:dot.append(f'{i} [label="{nodes[i].split(chr(92)+"n")[0]}"];')
        fq=next(i for i in ids if nodes[i].startswith('fastqc_raw'))
        cut=next(i for i in ids if nodes[i].startswith('cutadapt'))
        # Invisible layout constraints are not dependency edges.
        dot.append(f'{fq} -> {cut} [style=invis, weight=20];')
        dot.append('}')
    for i in nodes:
        if i not in group:dot.append(f'{i} [label="{nodes[i]}", fillcolor="#fdf3e3", color="#b45309"];')
    fc=next(i for i in nodes if nodes[i]=='feature_counts')
    for i in nodes:
        if nodes[i]=='samtools_index':dot.append(f'{i} -> {fc} [style=invis, weight=20];')
    for a,b in edges:dot.append(f'{a} -> {b};')
    dot.append('}')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'rnaseq-dag.dot').write_text('\n'.join(dot)+'\n')
    (OUT/'rnaseq-dag-raw.dot').write_text(raw)
    print(f'{len(nodes)} jobs; {len(edges)} dependency edges; {len(samples)} sample clusters')

if __name__=='__main__':main()
