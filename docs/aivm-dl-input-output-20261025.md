# AIVM代表论文：输入、输出与数据规模

核对日期：2026-10-25。范围是本项目中的虚拟代谢相关任务；列代表工作，不作完整文献清单。实测记录、条件、单细胞与模型生成标签分别统计。

| 论文 | 输入 | 输出 | 数据来源与规模 |
|---|---|---|---|
| DLKcat，Nature Catalysis 2022 | 酶氨基酸序列、底物结构 | 单个酶—底物对的kcat | BRENDA与SABIO-RK整理的16,838条记录，7,822条独特蛋白序列、2,672种底物。343个物种是后续应用范围，不是343个监督训练样本。 |
| UniKP，Nature Communications 2023 | 蛋白与底物的预训练表示；环境扩展另加入pH/温度 | kcat、Km、kcat/Km | kcat复用16,838条；Km 11,722条；kcat/Km 910条。最终回归器是Extra Trees，不是端到端深度网络。 |
| AMN，Nature Communications 2023 | 培养基成分、基因敲除和代谢网络 | 生长率，以及满足网络约束的通量分布 | 自采大肠杆菌110种培养基；ASAP数据145种敲除×120种培养基，共17,400条生长记录；另有FBA模拟训练集。生长数据并非实测全通量标签。 |
| EnzymeTuning，Nature Communications 2026 | 已有酶约束模型、初始kcat分布，实测生长/交换率/蛋白丰度用于评分校准；cGAN学习并生成参数组合 | 优化后的kcat参数组，下游模型预测蛋白丰度和表型 | 主酿酒酵母资料23种稳态培养条件，其中9碳限制、14氮限制；另有其他物种、C/N梯度及独立验证蛋白组。生成参数组不计为新增独立实测培养。 |
| scFEA，Genome Research 2021 | 单细胞RNA表达、代谢网络 | 每细胞169个代谢模块的推断通量和代谢不平衡 | 自采胰腺癌细胞实验质控后161个细胞：缺氧40 KD+48对照，常氧27 KD+46对照，共4种条件；另用公开数据和1000模拟细胞。没有161个细胞的配对实测通量标签，代谢组验证为群体测量。 |
| mFLIP，BMC Bioinformatics 2026 | 代谢物丰度谱 | 98条通路的通量上下界，共196维 | 合并150项公开代谢组研究。摘要/方法称超过22,000个样本，结果节称183,000样本，口径不一致尚未解释。标签由Recon3D/fastFVA计算生成，并非实测通量；同时比较深度模型和树模型。 |

## 解释

这些代表工作既有真实酶测量监督学习，也有少量培养实验结合机制约束、单细胞表达约束推断，以及学习现有通量求解器的代理模型。必须分别看实测条件数、独立干预数和监督标签来源。

EnzymeTuning的23个培养条件是主酵母资料，不能当整篇全部物种/验证数据的总样本数。scFEA的161个细胞来自四种处理，不能当161种独立干预。mFLIP的两个总量暂不合并解释。

本次不改变研究队列。

## 原始来源

- DLKcat：doi:10.1038/s41929-022-00798-z，原论文正文与图1；本机原论文保存在/data/research/aivm-literature-search/papers/dlkcat/。
- UniKP：doi:10.1038/s41467-023-44113-1，正文与原论文PDF，数据集与模型构建章节。
- AMN：doi:10.1038/s41467-023-40380-0，图3/4、AMNs can be trained on experimental datasets、Data availability。
- EnzymeTuning：doi:10.1038/s41467-026-73744-3，Methods: Dataset resources及Construction of EnzymeTuning。
- scFEA：doi:10.1101/gr.271205.120，PMC8494226，scRNA-seq data processing、network reconstruction、synthetic validation。
- mFLIP：doi:10.1186/s12859-026-06500-5，摘要、Dataset、Evaluation of flux interval prediction models。该文摘要/方法的22,000样本与结果节183,000样本并列保留。
