// Two teaching figures: generated biological art, editable labels and charts.
// Requires @oai/artifact-tool. Usage: node build_rna_concepts.mjs <build-directory>
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../../..');
const OUT=path.resolve(process.argv[2]||path.join(ROOT,'.rna-figure-build'));
const ART=path.join(ROOT,'assets/06-rna-seq/illustrations');
await fs.mkdir(OUT,{recursive:true});
const W=1200,H=1260,FONT='Hiragino Sans GB',GREEN='#186254',INK='#283E39',MUTED='#5E726D';
const ppt=Presentation.create({slideSize:{width:W,height:H}});
function label(slide,text,x,y,w,h=44,size=28,color=INK,bold=false,align='left',fill='none'){
 const shape=slide.shapes.add({geometry:'textbox',name:text,position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}});
 shape.text=text;shape.text.style={typeface:FONT,fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',autoFit:'none',insets:{left:0,right:0,top:0,bottom:0}};
 return shape;
}
function line(slide,x1,y1,x2,y2,color=GREEN,width=2){
 return slide.shapes.add({geometry:'line',position:{left:Math.min(x1,x2),top:Math.min(y1,y2),width:Math.abs(x2-x1),height:Math.abs(y2-y1),verticalFlip:(x2-x1)*(y2-y1)<0},fill:'none',line:{fill:color,width}});
}
function arrow(slide,x1,y1,x2,y2){
 const dot=(x,y)=>slide.shapes.add({geometry:'rect',name:'Arrow anchor',position:{left:x-0.5,top:y-0.5,width:1,height:1},fill:'none',line:{fill:'none',width:0}});
 const a=dot(x1,y1),b=dot(x2,y2);
 const c=slide.shapes.connect(a,b,{kind:'straight',line:{fill:GREEN,width:2.6},tail:{type:'triangle',width:'med',length:'med'}});c.bringToFront();return c;
}
async function picture(slide,file,x,y,w,h,crop){
 return slide.images.add({blob:await fs.readFile(path.join(ART,file)),contentType:'image/png',alt:file,fit:'contain',position:{left:x,top:y,width:w,height:h},...(crop?{crop}:{})});
}
// Figure 5.1: the illustration supplies biological form; labels carry meaning.
const s1=ppt.slides.add();s1.background.fill='#FFFFFF';
label(s1,'RNA 的主要类型与分工',55,12,1090,56,36,GREEN,true,'center');
await picture(s1,'rna-roles-art.png',15,69,1170,1170);
label(s1,'细胞核',126,154,190,42,32,GREEN,true);
label(s1,'细胞质',884,141,190,42,32,GREEN,true);
label(s1,'DNA',310,208,180,42,30,GREEN,true,'center');
arrow(s1,350,334,350,366);label(s1,'转录',374,330,110,37,27,GREEN,true);
label(s1,'前体 mRNA',165,424,210,40,28,GREEN,true);
arrow(s1,491,416,491,452);label(s1,'剪接',510,415,100,40,27,GREEN,true);
label(s1,'剪接体',73,488,180,38,26,GREEN,true);
label(s1,'含 snRNA',73,524,180,36,25,INK);
line(s1,223,526,278,501,GREEN,1.8);
label(s1,'成熟 mRNA',294,645,240,40,28,GREEN,true);
arrow(s1,561,675,697,675);label(s1,'输出',604,700,115,37,26,GREEN,true);
label(s1,'蛋白质',852,232,200,42,30,GREEN,true);
label(s1,'tRNA',1040,462,130,40,29,GREEN,true);
line(s1,1034,488,968,509,GREEN,1.8);
label(s1,'翻译',736,420,120,40,28,GREEN,true);
label(s1,'核糖体（含 rRNA）',738,804,400,42,28,GREEN,true,'center');
line(s1,907,796,907,752,GREEN,1.8);
// Exact labels beneath the three separate regulatory-RNA vignettes.
label(s1,'miRNA / siRNA',45,1110,355,42,28,GREEN,true,'center');
label(s1,'识别靶 RNA，影响稳定性或翻译',28,1155,392,40,23,INK,false,'center');
label(s1,'lncRNA',437,1110,355,42,29,GREEN,true,'center');
label(s1,'长链，作用与位置多样',437,1155,355,40,23,INK,false,'center');
label(s1,'circRNA',820,1110,345,42,29,GREEN,true,'center');
label(s1,'首尾相连的环状 RNA',820,1155,345,40,23,INK,false,'center');
label(s1,'代表性形态与作用场景；具体 RNA 的功能需分别判断。',45,1212,1110,35,22,MUTED,false,'center');
s1.speakerNotes.textFrame.setText('图 5.1。生物形象由内置 image_gen 生成，标签与关系独立排版。插画为示意，不代表精确分子尺度或每一种 RNA 的全部功能。mRNA 作为蛋白编码模板；snRNA 参与剪接；rRNA 为核糖体组成与催化核心，tRNA 参与氨基酸递送；其他 RNA 不构成同一条必经线性路径。参考：https://www.genome.gov/about-genomics/educational-resources/fact-sheets/ribonucleic-acid-fact-sheet ; https://openstax.org/books/microbiology/pages/10-3-structure-and-function-of-rna 。');

const s2=ppt.slides.add();s2.background.fill='#FFFFFF';
label(s2,'相同基因组，不同的 RNA 丰度',45,18,1110,58,36,GREEN,true,'center');
label(s2,'同一个体的三类细胞，保留同一组示意基因 A–D',60,91,1080,44,28,INK,false,'center');
const subjects=[
 {title:'神经细胞',labelCenter:214,x:28,values:[3,5,1,1]},
 {title:'肌肉细胞',labelCenter:695,x:414,values:[3,1,5,1]},
 {title:'上皮细胞',labelCenter:1050,x:800,values:[3,1,1,5]}
];
await picture(s2,'cell-types-art.png',20,173,1160,387);
for(const d of subjects){
 label(s2,d.title,d.labelCenter-150,561,300,50,32,GREEN,true,'center');
 arrow(s2,d.labelCenter,624,d.x+186,664);
}
label(s2,'比较同一种 RNA 在三类细胞中的相对丰度',55,683,1090,46,28,GREEN,true,'center');
// Native PowerPoint charts; all share 0–5.5 so bar lengths remain comparable.
for(const d of subjects){
 const c=s2.charts.add('bar',{
  position:{left:d.x+14,top:752,width:344,height:355},
  categories:['RNA D','RNA C','RNA B','RNA A'],
  series:[{name:d.title,values:d.values.slice().reverse(),fill:GREEN,line:{fill:'none',width:0}}],
  hasLegend:false,barOptions:{direction:'bar',grouping:'clustered',gapWidth:145},
  xAxis:{visible:true,tickLabelPosition:'nextTo',line:{fill:'none',width:0},majorGridlines:null,textStyle:{typeface:FONT,fontSize:25,fill:INK}},
  yAxis:{visible:true,min:0,max:5.5,majorUnit:1,tickLabelPosition:'none',line:{fill:'#B1C3BE',width:1},majorGridlines:null,textStyle:{typeface:FONT,fontSize:24,fill:INK}},
  dataLabels:{showValue:true,position:'outEnd',textStyle:{typeface:FONT,fontSize:24,fill:GREEN}},
  chartFill:'none',chartLine:{fill:'none',width:0},plotAreaFill:'none',plotAreaLine:{fill:'none',width:0}
 });
 c.legend.textStyle.typeface=FONT;
}
label(s2,'共有的 RNA 仍然存在，变化的是各类 RNA 的丰度组合。',55,1137,1090,45,28,GREEN,true,'center');
label(s2,'A–D 为示意标签；条形长度和数字不代表实测值。',55,1202,1090,38,23,MUTED,false,'center');
s2.speakerNotes.textFrame.setText('图 5.2。细胞形态由内置 image_gen 生成，三组丰度图为原生可编辑 PowerPoint 图表。示意矩阵按神经、肌肉、上皮分别为 [3,5,1,1]、[3,1,5,1]、[3,1,1,5]。每个类别在三组都非零，RNA A 同为 3；A–D 不对应真实基因、数值不是测量值。细胞大小不按比例，肌肉图为单核梭形形态的示意。参考：https://www.genome.gov/about-genomics/educational-resources/fact-sheets/ribonucleic-acid-fact-sheet 。');
await (await PresentationFile.exportPptx(ppt)).save(path.join(OUT,'candidate.pptx'));
for(let i=0;i<2;i++){
 const slide=ppt.slides.items[i];
 const preview=await ppt.export({slide,format:'png',scale:2});
 await fs.writeFile(path.join(OUT,`rna-concepts-${i+1}.png`),new Uint8Array(await preview.arrayBuffer()));
 const layout=await slide.export({format:'layout'});await fs.writeFile(path.join(OUT,`slide-${i+1}.layout.json`),await layout.text());
}
await fs.writeFile(path.join(OUT,'design.json'),JSON.stringify({slideSize:{width:W,height:H},font:FONT,figures:['5.1','5.2'],abundance:subjects.map(d=>({cell:d.title,values:d.values})),nativeCharts:3},null,2));
console.log(`Wrote two-slide candidate and PNGs to ${OUT}`);
