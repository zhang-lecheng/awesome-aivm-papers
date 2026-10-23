# Awesome AIVM Papers

面向人工智能与虚拟代谢研究的论文、教程和学习入口。持续完善，欢迎通过 Issue 或 Pull Request 补充资料。

**[浏览学术看板](https://zhang-lecheng.github.io/awesome-aivm-papers/)** · [阅读方法](METHODOLOGY.md) · [贡献文献](CONTRIBUTING.md)

已收录 **21 篇**文献。入门库长期维护；近期论文每周日 09:00（Asia/Shanghai）由 DeepSeek Harness 更新，模型为 `westlake/deepseek-flash`。

本项目覆盖代谢网络重建、酶约束模型、酶动力学预测、组学与通量、机制与机器学习融合，以及单细胞代谢。

## 建议阅读顺序

1. **理解约束与通量**：从 FBA 的守恒条件、反应边界和目标函数开始，再用 COBRApy 动手。 入口：FBA、COBRApy、COBRA Toolbox 3.0。
2. **读懂一个代谢网络**：比较酵母、人类和自动重建模型；学习基因、反应与代谢物如何对应。 入口：Yeast9、Human1、Recon3D、CarveMe、MEMOTE。
3. **加入酶容量与动力学**：理解酶丰度和 kcat 如何约束通量，再研究 AI 参数预测与系统优化。 入口：GECKO、DLKcat、UniKP、EnzymeTuning。
4. **连接数据与机制**：比较组学到通量的监督学习，以及神经网络和约束优化共同预测表型。 入口：组学到通量的监督学习、神经网络与机制模型融合。
5. **走向细胞状态与实验**：比较单细胞代谢推断与实测证据，研究推断出的差异能否指导干预。 入口：scFEA、Compass、METAFlux、SCOOTI。

## 本周更新

首期正在准备。下面的经典论文可直接作为学习入口。

## 前瞻与综述

- **代谢通路重建框架** — [Artificial intelligence revolutionizes cellular metabolic pathway reconstruction](https://doi.org/10.1016/j.tibs.2026.01.003)。Trends in biochemical sciences, 2026。
  文章讨论如何把逆合成规划与生物约束结合，重建有生物可行性的代谢通路；同时连接单个通路和系统层面的建模，以及大语言模型参与理解、设计、评价和优化的可能方式。
  - 为什么读：从通路设计与系统约束两端理解 AI 如何参与代谢研究。
  - 阅读时注意：这是概念框架；具体路线的有效性仍需要依赖相应的模型与实验结果。

- **AI Virtual Cell** — [How to build the virtual cell with artificial intelligence: Priorities and opportunities](https://doi.org/10.1016/j.cell.2024.11.015)。Cell, 2024。
  这篇前瞻提出用多尺度、多模态神经网络表示并模拟分子、细胞与组织，讨论构建虚拟细胞所需的数据、评价与协作。它提供整体研究愿景，适合先理解代谢模型在虚拟细胞中的位置。
  - 为什么读：先理解虚拟细胞要支持哪些科学问题，再决定代谢模块该预测什么。
  - 阅读时注意：文章提出研究议程，没有给出一个已经完成全部能力的虚拟细胞系统。

## FBA 与约束建模

- **COBRA Toolbox 3.0** — [Creation and analysis of biochemical constraint-based models using the COBRA Toolbox v.3.0](https://doi.org/10.1038/s41596-018-0098-2)。Nature protocols, 2019。
  这篇协议系统介绍如何建立和分析生化约束模型，覆盖模型重建、分析与多种应用。它适合与 FBA 入门配合使用，帮助读者把一个数学优化问题扩展为规范的代谢模型工作流程。
  - 为什么读：查阅约束建模的标准操作、分析方法与可复现流程。
  - 阅读时注意：教程包含多种方法，实际研究需要按数据和目标选择，而非全部套用。

- **COBRApy** — [COBRApy: COnstraints-Based Reconstruction and Analysis for Python](https://doi.org/10.1186/1752-0509-7-74)。BMC systems biology, 2013。
  COBRApy 提供 Python 接口建立、修改和分析约束代谢模型，是运行 FBA、基因删除和模型分析的常用工具。读完 FBA 基础后，可以用它把化学计量矩阵、培养基和基因反应关系转化成可执行实验。
  - 为什么读：作为动手入口，复现最简单的生长预测和单基因删除实验。
  - 阅读时注意：软件工具提供求解能力；模型的生物学正确性仍取决于网络和约束。

- **FBA** — [What is flux balance analysis?](https://doi.org/10.1038/nbt.1614)。Nature biotechnology, 2010。
  通量平衡分析的入门文章，介绍如何用化学计量矩阵、稳态质量守恒、反应上下界及目标函数刻画可行通量。它是理解基因组尺度代谢模型、酶约束模型与后续机器学习融合方法的理论起点。
  - 为什么读：掌握 Sv=0、可行解空间和目标函数，后面的 GEM 工作才容易读懂。
  - 阅读时注意：FBA 依赖稳态、网络边界和目标函数；一个最优解不能自动代表细胞的真实通量。

## GEM 与模型重建

- **Yeast9** — [Yeast9: a consensus genome-scale metabolic model for S. cerevisiae curated by the community](https://doi.org/10.1038/s44320-024-00060-7)。Molecular systems biology, 2024。
  社区持续维护的酿酒酵母基因组尺度代谢模型。作者将单细胞转录组、蛋白组和大量突变株表达数据接入模型，研究渗透压和氮源适应，并比较模型通量表示与表达表示在功能预测中的表现。
  - 为什么读：适合学习真实 GEM 如何维护、如何整合组学，以及如何设计遗传扰动分析。
  - 阅读时注意：由表达约束得到的通量属于模型推断，需要与实测通量或独立表型核对。

- **Human1** — [An atlas of human metabolism](https://doi.org/10.1126/scisignal.aaz1482)。Science signaling, 2020。
  Human1 将既有的人类代谢重建整合成统一模型，为组学数据分析和组织、疾病相关代谢研究提供共同起点。它适合与酵母模型并读，理解人类细胞的代谢网络、基因注释与条件化分析如何衔接。
  - 为什么读：从微生物过渡到人类细胞时，使用一个有持续维护基础的参考模型。
  - 阅读时注意：通用人类网络需要按组织、细胞状态和培养条件设置，不能直接视为特定细胞的模型。

- **Virtual Metabolic Human** — [The Virtual Metabolic Human database: integrating human and gut microbiome metabolism with nutrition and disease](https://doi.org/10.1093/nar/gky992)。Nucleic acids research, 2019。
  Virtual Metabolic Human 将人类和肠道微生物代谢与营养、疾病信息整合到数据库中。它提供跨宿主、微生物和饮食的反应与代谢物索引，可以作为搭建代谢研究数据入口和检查标识符的参考。
  - 为什么读：查代谢物、反应和生物背景，了解宿主与微生物代谢的组织方式。
  - 阅读时注意：数据库中的关联和模型条目需要按具体研究情境核实，不能替代条件化测量。

- **Recon3D** — [Recon3D enables a three-dimensional view of gene variation in human metabolism](https://doi.org/10.1038/nbt.4072)。Nature biotechnology, 2018。
  Recon3D 将人类代谢网络和蛋白三维结构等信息联系起来，支持分析基因变异对代谢功能的可能影响。它提供从基因、酶结构到系统代谢表型的跨尺度组织方式，是理解机制约束如何扩充的重要资源。
  - 为什么读：了解人类 GEM 如何连接蛋白结构与遗传变异。
  - 阅读时注意：把结构信息映射到网络，并不自动确定每个变异的细胞内动力学效应。

- **CarveMe** — [Fast automated reconstruction of genome-scale metabolic models for microbial species and communities](https://doi.org/10.1093/nar/gky537)。Nucleic acids research, 2018。
  CarveMe 自动从通用模型出发，为微生物物种和群落重建基因组尺度代谢网络。它让重建成为可重复的计算流程，适合研究大规模自动建模、网络缺口和群落代谢交换。
  - 为什么读：理解自动重建与人工审校之间的分工，建立微生物模型作为方法实验平台。
  - 阅读时注意：自动重建和补洞依赖先验与培养条件，关键反应和预测表型仍需审查。

## 酶约束与动力学

- **EnzymeTuning** — [EnzymeTuning improves enzyme-constrained metabolic modeling and proteome abundance prediction through deep learning](https://doi.org/10.1038/s41467-026-73744-3)。Nature communications, 2026。
  EnzymeTuning 用生成对抗网络全局优化酶约束代谢模型中的 kcat，并结合蛋白降解常数推断蛋白合成率。作者在多种酵母与大肠杆菌中评价代谢模型和蛋白组丰度预测，分析不同营养限制下的酶资源分配。
  - 为什么读：比较独立预测 kcat 与为系统模型联合优化参数这两种研究路线。
  - 阅读时注意：优化后的参数服务于模型拟合；是否对应独立测得的细胞内酶动力学，需要额外核实。

- **UniKP** — [UniKP: a unified framework for the prediction of enzyme kinetic parameters](https://doi.org/10.1038/s41467-023-44113-1)。Nature communications, 2023。
  UniKP 将蛋白质和底物表示用于预测多类酶动力学参数。它可以与 DLKcat 对照阅读，比较数据整理、序列与化学表示、参数预测任务以及对酶工程和系统建模的用途。
  - 为什么读：横向比较 kcat、Km 等参数的学习问题，建立简单且可检查的基线。
  - 阅读时注意：相近序列和相同底物如何分到训练与测试，会显著影响对泛化能力的解释。

- **DLKcat** — [Deep learning-based kcat prediction enables improved enzyme-constrained model reconstruction](https://doi.org/10.1038/s41929-022-00798-z)。Nature Catalysis, 2022。
  DLKcat 从酶蛋白序列和底物结构预测催化周转数 kcat，并把预测参数接入酶约束模型的构建。它连接了酶级别的监督学习与系统级代谢表型预测，展示参数预测如何改变下游模型的用途。
  - 为什么读：从序列和底物出发，追踪 AI 预测误差如何传到整个代谢网络。
  - 阅读时注意：训练中的体外动力学值稀疏且有噪声；预测值不能直接等同于细胞内的实际周转数。

- **GECKO** — [Improving the phenotype predictions of a yeast genome-scale metabolic model by incorporating enzymatic constraints](https://doi.org/10.15252/msb.20167411)。Molecular systems biology, 2017。
  GECKO 把酶加入代谢反应约束，使每条通量受酶丰度和催化周转数的乘积限制。论文在酵母中比较不同碳源、胁迫和通路过表达，并展示如何把定量蛋白组接入模型，缩小可行通量范围。
  - 为什么读：理解 GEM 如何变成酶约束 GEM，以及蛋白组和动力学参数各自提供什么信息。
  - 阅读时注意：对酶丰度、动力学参数和酶容量的设置，会影响最后得到的通量范围。

## 机器学习与机制融合

- **组学到通量的监督学习** — [Predicting metabolic fluxes from omics data via machine learning: Moving from knowledge-driven towards data-driven approaches](https://doi.org/10.1016/j.csbj.2023.10.002)。Computational and structural biotechnology journal, 2023。
  论文用大肠杆菌转录组、蛋白组和通量数据训练监督学习模型，比较内部与外部通量预测和简约 FBA 的表现。它提供一个直接切入点：先比较数据驱动映射与经典约束优化，再讨论两者如何结合。
  - 为什么读：建立组学到通量的简单基线，弄清训练标签和目标条件。
  - 阅读时注意：数据规模、条件划分和可用输入决定外推能力；目前没有核实 ML2Flux 是正式方法名。

- **神经网络与机制模型融合** — [A neural-mechanistic hybrid approach improving the predictive power of genome-scale metabolic models](https://doi.org/10.1038/s41467-023-40380-0)。Nature communications, 2023。
  作者让神经网络与约束代谢模型共同预测微生物表型，在不同培养基和基因敲除条件下评估大肠杆菌及恶臭假单胞菌。该路线尝试用数据学习补充不充分的机制输入，同时保留反应网络的机制约束。
  - 为什么读：学习神经网络究竟补了哪个未知量，以及机制约束如何进入训练和预测。
  - 阅读时注意：模型仍需要训练表型；跨物种或超出培养条件的泛化，必须分别验证。

## 单细胞与空间代谢

- **SCOOTI** — [Inferring metabolic objectives and trade-offs in single cells during embryogenesis](https://doi.org/10.1016/j.cels.2024.12.005)。Cell systems, 2025。
  SCOOTI 结合组学、代谢建模和机器学习，推断单细胞所优先满足的代谢目标及其取舍。作者在胚胎发育、细胞周期和静息状态中分析目标变化，并用 CRISPR 筛选中的必需基因等结果验证推断。
  - 为什么读：从固定最大化生物量，转向研究不同细胞实际优先满足什么代谢需求。
  - 阅读时注意：推断目标依赖模型和候选目标集合，独立功能测量仍决定其生物学解释。

- **METAFlux** — [Characterizing cancer metabolism from bulk and single-cell RNA-seq data using METAFlux](https://doi.org/10.1038/s41467-023-40457-w)。Nature communications, 2023。
  METAFlux 使用整体和单细胞 RNA 数据刻画肿瘤代谢，把基因表达与约束代谢建模连接起来。它与 scFEA、Compass 提供互补入口，适合比较网络定义、细胞间差异和下游验证如何影响结论。
  - 为什么读：用同一生物学问题比较不同 RNA 到代谢推断方法。
  - 阅读时注意：转录水平到反应活性的映射含有假设，不能仅凭几种方法结果一致就确定真实通量。

- **scFEA** — [A graph neural network model to estimate cell-wise metabolic flux using single-cell RNA-seq data](https://doi.org/10.1101/gr.271205.120)。Genome research, 2021。
  scFEA 把代谢网络表示为因子图，用图神经网络和通量平衡约束从单细胞 RNA 推断细胞级代谢通量。作者还生成配对代谢组与 RNA 数据，比较氧气和遗传扰动下的预测变化及代谢物变化。
  - 为什么读：理解从 RNA 推断代谢状态的完整假设链，以及细胞异质性如何进入模型。
  - 阅读时注意：验证中的代谢物丰度变化与通量直接测量不同，RNA 推断结果需要保留这一差别。

- **Compass** — [Metabolic modeling of single Th17 cells reveals regulators of autoimmunity](https://doi.org/10.1016/j.cell.2021.05.045)。Cell, 2021。
  Compass 结合单细胞 RNA 和代谢网络分析 Th17 细胞的代谢状态，提出与致病潜力有关的多胺代谢假设。作者通过代谢实验、化学与遗传扰动及体内研究检验候选，展示计算代谢分析如何引导生物学实验。
  - 为什么读：观察从转录组推断、候选通路选择到功能实验的具体研究过程。
  - 阅读时注意：计算得分描述网络支持的代谢状态，不能直接当作每个细胞实测的绝对通量。

## 实验数据与模型验证

- **MEMOTE** — [MEMOTE for standardized genome-scale metabolic model testing](https://doi.org/10.1038/s41587-020-0446-y)。Nature biotechnology, 2020。
  MEMOTE 为基因组尺度代谢模型建立标准化测试，检查注释、化学计量一致性等模型质量问题。它把模型重建后的技术验证变成可以重复执行和比较的流程，适合所有新模型或自动重建项目作为基础检查。
  - 为什么读：在比较预测性能前，先检查模型本身是否满足基本结构与一致性要求。
  - 阅读时注意：结构和注释测试通过，不等同于生长、扰动或通量预测已得到实验验证。

## 历期周报


## 数据与维护

- `data/papers.json`：文献库及中文导读。
- `data/weeks/`：每期候选、检索来源和编辑选择的快照。
- `scripts/radar.py`：采集、校验、重建与推送。
- `prompts/weekly.zh-CN.md`：DeepSeek Harness 每周任务指令。

参考文献的标题、期刊和日期优先核对 DOI 注册信息与 Europe PMC。每篇记录核查日期及证据层级。欢迎提交更正。
