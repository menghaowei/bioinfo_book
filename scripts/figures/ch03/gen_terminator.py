#!/usr/bin/env python3
"""Representative early Solexa/Illumina reversible terminator; RDKit required.

Connectivity: US7541444B2, compound (18), image C00024 (C5-Alexa488 dCTP).
The fluorophore beyond its amide carbonyl is deliberately abbreviated as Dye.
dCTP stereochemistry cross-checked with PubChem CID 65091.
This is not a specification of current commercial Illumina reagents.
Run: python3 scripts/figures/ch03/gen_terminator.py
"""
import json
import sys
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/figures/ch04'))
from common import Svg, COLOR_PRIMARY as GREEN, COLOR_WARN as AMBER, COLOR_FILL as PALE

# Atom maps identify the sites that must remain connected correctly. Mapping
# labels are cleared before depiction, and are not chemical isotope numbers.
SMILES=('[CH2:2]1[C@@H:3]([C@H:4]([O:40][C@H:1]1'
        '[N:10]2[CH:16]=[C:15](C#CCNC(=O)CC[S:70][S:71]CCNC(=O)[*:90])'
        '[C:14](=[N:13][C:12]2=O)N)[CH2:5][O:50][P:51](=O)(O)OP(=O)(O)OP(=O)(O)O)'
        '[O:30][CH2:31][N:32]=[N+:33]=[N-:34]')


def main():
    mol=Chem.MolFromSmiles(SMILES)
    assert mol is not None
    ids={a.GetAtomMapNum():a.GetIdx() for a in mol.GetAtoms() if a.GetAtomMapNum()}
    assert mol.GetBondBetweenAtoms(ids[1],ids[10]) is not None # C1′–N1
    assert mol.GetBondBetweenAtoms(ids[3],ids[30]) is not None # C3′–O
    assert mol.GetBondBetweenAtoms(ids[70],ids[71]) is not None # disulfide
    assert mol.GetAtomWithIdx(ids[2]).GetTotalNumHs()==2 # 2′-deoxy
    for a in mol.GetAtoms(): a.SetAtomMapNum(0)
    mol.GetAtomWithIdx(ids[90]).SetProp('atomLabel','Dye')
    Chem.AssignStereochemistry(mol,cleanIt=True,force=True)
    rdDepictor.Compute2DCoords(mol)
    # Open the phosphate chain so terminal OH labels cannot collide.
    from rdkit.Geometry import Point3D
    conf=mol.GetConformer(); origin=conf.GetAtomPosition(ids[5])
    def put(i,x,y):conf.SetAtomPosition(i,Point3D(origin.x+x,origin.y+y,0))
    put(ids[50],-1.2,-0.75)
    p=ids[51]; previous=ids[50]
    for j in range(3):
        x=-2.5-j*3;put(p,x,-1.5)
        next_p=None
        terminals=[b.GetOtherAtomIdx(p) for b in mol.GetAtomWithIdx(p).GetBonds()
                   if b.GetBondType()==Chem.BondType.SINGLE and b.GetOtherAtomIdx(p)!=previous
                   and mol.GetAtomWithIdx(b.GetOtherAtomIdx(p)).GetDegree()==1]
        for bond in mol.GetAtomWithIdx(p).GetBonds():
            oxygen=bond.GetOtherAtomIdx(p)
            if oxygen==previous:continue
            if bond.GetBondType()==Chem.BondType.DOUBLE:put(oxygen,x,-3)
            elif mol.GetAtomWithIdx(oxygen).GetDegree()==1:
                put(oxygen,x if oxygen==terminals[0] else x-1.5,0 if oxygen==terminals[0] else -1.5)
            else:
                put(oxygen,x-1.5,-1.5)
                next_p=next(a.GetIdx() for a in mol.GetAtomWithIdx(oxygen).GetNeighbors() if a.GetIdx()!=p)
                next_previous=oxygen
        if next_p is not None:p,previous=next_p,next_previous
    drawer=rdMolDraw2D.MolDraw2DSVG(744,400)
    opt=drawer.drawOptions();opt.useBWAtomPalette();opt.clearBackground=False
    opt.padding=0.06;opt.bondLineWidth=1.8;opt.minFontSize=15;opt.maxFontSize=22
    opt.addStereoAnnotation=False
    amber=(0.99,0.88,0.72); green=(0.82,0.93,0.89)
    highlighted=[ids[k] for k in [30,31,32,33,34,70,71,90]]
    colors={i:(amber if i in [ids[k] for k in [30,31,32,33,34]] else green) for i in highlighted}
    rdMolDraw2D.PrepareAndDrawMolecule(drawer,mol,highlightAtoms=highlighted,highlightAtomColors=colors)
    coords={str(k):[drawer.GetDrawCoords(v).x,drawer.GetDrawCoords(v).y] for k,v in ids.items()}
    drawer.FinishDrawing()
    molecular=drawer.GetDrawingText(); molecular=molecular[molecular.index('<svg'):]
    molecular=molecular.replace('<svg ','<svg x="18" y="66" ',1)
    s=Svg(780,820,'可逆终止子核苷酸的关键结构与测序循环',
          '早期专利中的 C5 染料连接 dCTP 示例。糖环 3′ 位以 O–CH2–N3 封闭；碱基经含二硫键的连接子连接染料；Dye 缩写代表未展开的染料部分。掺入后成像，再恢复 3′-OH 并移除染料。')
    def text(x,y,t,size=18,color='#333333',bold=False,anchor='start'):
        s.text(x,y,t,size=size,mono=False,fill=color,weight='bold' if bold else 'normal',anchor=anchor)
    text(24,30,'A  代表性 dCTP 的关键结构',23,GREEN,True)
    text(24,57,'依据早期专利实例；Dye 为染料部分的简写，图示不展开其内部结构。',16)
    s.add(molecular)
    # Labels at the exact mapped atoms, with leaders kept short and outside bonds.
    for key,txt,dx,dy in [(1,"1′",12,12),(2,"2′",-11,-12),(3,"3′",-18,19),(4,"4′",17,20),(5,"5′",15,3)]:
        x,y=coords[str(key)];text(x+18+dx,y+66+dy,txt,15,GREEN)
    s.line(24,481,756,481,stroke=GREEN,sw=1.1)
    text(26,510,'5′-三磷酸',18,GREEN,True)
    text(26,537,'掺入时释放焦磷酸',16)
    text(282,510,'3′-O–CH₂–N₃',18,AMBER,True)
    text(282,537,'封闭 3′-OH，暂停延伸',16)
    text(535,510,'连接子中的 S–S',18,GREEN,True)
    text(535,537,'可切除碱基上的染料',16)
    text(24,584,'B  一轮测序中，链末端怎样变化',23,GREEN,True)
    labels=['① 掺入一个核苷酸','② 成像，识别碱基','③ 脱保护，继续延伸']
    for i,(x,title) in enumerate(zip([24,282,540],labels)):
        s.rect(x,604,216,137,fill=PALE,stroke=GREEN,rx=10)
        text(x+108,634,title,18,GREEN,True,'middle')
        s.line(x+18,670,x+61,670,stroke=GREEN,sw=2.7)
        s.rect(x+62,651,42,38,fill='white',stroke=GREEN,sw=1.8,rx=3)
        text(x+83,677,'C',22,GREEN,True,'middle')
        if i<2:
            text(x+121,669,'Dye',17,GREEN,True)
            s.line(x+104,663,x+116,663,stroke=GREEN,sw=1.5)
            text(x+108,718,'3′-O–CH₂–N₃',17,AMBER,False,'middle')
        else:
            s.line(x+104,663,x+116,663,stroke=GREEN,sw=1.8)
            text(x+135,686,'残基',15)
            text(x+108,718,'3′-OH 恢复',18,GREEN,True,'middle')
        if i<2:s.arrow(x+222,674,x+250,674,stroke=GREEN,sw=2)
    text(390,775,'掺入链的是单磷酸残基；脱保护后，碱基上仍可能留下连接子的残基。',17,anchor='middle')
    text(390,804,'A 为化学关键结构，B 为过程示意；不代表所有代际平台的试剂配方。',16,anchor='middle')
    out=ROOT/'assets/03-sequencing-and-data-formats/010-nucleotide-reversible-terminator.svg'
    out.write_text(s.render())
    print(json.dumps({'file':str(out),'stereocenters':Chem.FindMolChiralCenters(mol,includeUnassigned=True),'atom_coordinates':coords},ensure_ascii=False))


if __name__=='__main__':main()
