# Awesome AIVM Papers

**English** | [简体中文](README.zh-CN.md)

A curated collection of papers, tutorials, and learning resources for AI and virtual metabolism. This collection is a work in progress; readers are welcome to suggest resources through Issues or Pull Requests.

**[Explore the research dashboard](https://zhang-lecheng.github.io/awesome-aivm-papers/)** · [Selection methodology (Chinese)](METHODOLOGY.md) · [Contribution guide (Chinese)](CONTRIBUTING.md)

The library currently contains **25 papers**. Foundational resources are maintained over time; recent literature is updated every **Sunday at 09:00, Asia/Shanghai**, by DeepSeek Harness using `westlake/deepseek-flash`.

Topics include metabolic network reconstruction, enzyme-constrained models, enzyme kinetic prediction, omics-to-flux inference, neural-mechanistic integration, and single-cell metabolism. AIVM is used here as an organizing theme; individual papers may use different terminology.

## Suggested reading path

1. **Understand constraints and fluxes.** Start with FBA mass balance, reaction bounds, and objective functions; then try COBRApy. Start with: FBA, COBRApy, COBRA Toolbox 3.0.
2. **Read a metabolic network.** Compare yeast, human, and automatically reconstructed models; learn how genes, reactions, and metabolites connect. Start with: Yeast9, Human1, Recon3D, CarveMe, MEMOTE.
3. **Add enzyme capacity and kinetics.** Learn how enzyme abundance and kcat constrain flux, then study AI parameter prediction and systems-level optimization. Start with: GECKO, DLKcat, UniKP, EnzymeTuning.
4. **Connect data and mechanisms.** Compare supervised omics-to-flux learning with approaches that combine neural networks and constraint-based optimization. Start with: Omics-to-flux supervised learning; neural-mechanistic hybrid models.
5. **Study cell states and experiments.** Compare single-cell metabolic inference with measured evidence and ask whether inferred differences can guide interventions. Start with: scFEA, Compass, METAFlux, SCOOTI.

## This week

Latest issue: [2026-10-23](weekly/2026-10-23.md) (Chinese).

This issue highlights GPU-based metabolic optimization and a virtual-cell framework for fungal biomanufacturing. Semi-supervised enzyme kinetic prediction and the integration of deuterium metabolic imaging with metabolic models are also worth following; both remain on the watchlist because only their abstracts were checked. For a first reading, start with FBA, GECKO, and DLKcat, then assess what the newer approaches add.

## Perspectives and reviews

- **Metabolic pathway reconstruction framework** — [Artificial intelligence revolutionizes cellular metabolic pathway reconstruction](https://doi.org/10.1016/j.tibs.2026.01.003). Trends in biochemical sciences, 2026.
  The article discusses combining retrosynthetic planning with biological constraints to reconstruct biologically feasible metabolic pathways. It connects pathway-level and systems-level modeling and considers how large language models might contribute to understanding, designing, evaluating, and optimizing metabolic networks.
  - Why read: Understand AI for metabolism from both pathway design and systems constraints.
  - Reading note: This is a conceptual framework. The effectiveness of individual approaches depends on their corresponding modeling and experimental results.

- **AI Virtual Cell** — [How to build the virtual cell with artificial intelligence: Priorities and opportunities](https://doi.org/10.1016/j.cell.2024.11.015). Cell, 2024.
  This Perspective proposes multiscale, multimodal neural networks for representing and simulating molecules, cells, and tissues. It discusses the data, evaluation, and collaboration needed to build virtual cells, providing a useful starting point for understanding where metabolic modeling fits into the broader vision.
  - Why read: Identify the scientific questions a virtual cell should support before deciding what its metabolic component should predict.
  - Reading note: The article sets out a research agenda; it does not present a completed system with all of the proposed capabilities.

- **AI-enabled fungal biomanufacturing** — [AI-enabled fungal biomanufacturing: from genome mining to the artificial intelligence virtual cell](https://europepmc.org/article/PMC/PMC13647374). Mycology, 2026.
  This review surveys AI for filamentous fungal biomanufacturing, spanning genome mining, enzymes and pathways, genome editing, metabolic modeling, and fermentation control. It presents omics, mechanistic models, and machine learning within a unified multiscale virtual-cell framework, emphasizing compartmentalized metabolism, secretion, and morphology-dependent production alongside data quality, cross-scale integration, interpretability, and experimental validation.
  - Why read: Connect GEMs and machine learning to a concrete manufacturing context. The discussion of compartments and secretion helps assess whether a proposed virtual-cell framework addresses fungal biology beyond a collection of separate tasks.
  - Reading note: The review provides no new quantitative benchmark, error-propagation analysis, or validation experiments for the proposed cross-scale integration. Its discussion of fungal GEMs cites existing models and dynamic FBA examples, leaving the added benefit over current hybrid models unresolved.

## FBA and constraint-based modeling

- **COBRA Toolbox 3.0** — [Creation and analysis of biochemical constraint-based models using the COBRA Toolbox v.3.0](https://doi.org/10.1038/s41596-018-0098-2). Nature protocols, 2019.
  This protocol describes the construction and analysis of biochemical constraint-based models, including reconstruction, analysis, and applications. It complements introductory FBA material by expanding a mathematical optimization problem into a structured metabolic modeling workflow.
  - Why read: Consult standard procedures, analytical methods, and reproducible workflows for constraint-based modeling.
  - Reading note: The protocol includes many methods. A study should select those appropriate to its data and objective rather than apply them all.

- **COBRApy** — [COBRApy: COnstraints-Based Reconstruction and Analysis for Python](https://doi.org/10.1186/1752-0509-7-74). BMC systems biology, 2013.
  COBRApy provides Python interfaces for building, modifying, and analyzing constraint-based metabolic models. After learning FBA, readers can use it to turn stoichiometry, media definitions, and gene-reaction relationships into executable analyses such as growth prediction and gene deletion.
  - Why read: Start with hands-on reproduction of simple growth predictions and single-gene deletions.
  - Reading note: The software provides analysis and solver access; biological correctness still depends on the network and its constraints.

- **FBA** — [What is flux balance analysis?](https://doi.org/10.1038/nbt.1614). Nature biotechnology, 2010.
  An introduction to flux balance analysis, covering stoichiometric matrices, steady-state mass balance, reaction bounds, and objective functions. It provides the theoretical starting point for genome-scale metabolic models, enzyme-constrained models, and later approaches that combine constraints with machine learning.
  - Why read: Learn Sv = 0, feasible flux spaces, and objective functions before moving on to GEM research.
  - Reading note: FBA depends on steady-state assumptions, network boundaries, and the objective function. An optimal solution is not automatically the actual cellular flux state.

- **gpuGEM** — [gpuGEM: GPU-based linear optimisation of genome-scale metabolic models](https://arxiv.org/abs/2610.24106v1). arXiv, 2026.
  The open-source gpuGEM library formulates FBA and coupled constraints as linear programs for the NVIDIA cuOpt PDLP solver, using size-dependent precision, tolerances, and presolve settings. Across ten models with 95 to 1.18 million variables, the authors compare objective values, primal feasibility, and bound satisfaction with HiGHS and Gurobi and report 1.1- to 94-fold speedups. In eight models the objective reaction is fixed by its bounds, so agreement there is only a consistency check. A candidate-gene prioritization workflow falls from 41 to 21 seconds.
  - Why read: Gene-deletion scans, flux variability analysis, personalized models, and cohort studies require repeated solves. The study examines solver choice, feasibility, and numerical stability and offers an open implementation relevant to GPU-based GEM workflows.
  - Reading note: The accessible HTML conversion is truncated in Results, so some acceleration, residual-tolerance, and iteration details were verified only at abstract level. Speedups come from a single RTX A4500 workstation. Biological consequences of feasibility decisions across models with different degeneracy were not evaluated; practical gains require reproduction.

## Genome-scale metabolic models and reconstruction

- **Yeast9** — [Yeast9: a consensus genome-scale metabolic model for S. cerevisiae curated by the community](https://doi.org/10.1038/s44320-024-00060-7). Molecular systems biology, 2024.
  A community-maintained genome-scale metabolic model of Saccharomyces cerevisiae. The authors integrate single-cell transcriptomics, proteomics, and mutant expression data to study osmotic and nitrogen-source adaptation, and compare model-derived flux representations with expression representations for functional prediction.
  - Why read: Learn how a working GEM is maintained, how omics data are integrated, and how genetic perturbation analyses are designed.
  - Reading note: Fluxes obtained by constraining a model with expression data are model inferences and should be checked against measured fluxes or independent phenotypes.

- **Human1** — [An atlas of human metabolism](https://doi.org/10.1126/scisignal.aaz1482). Science signaling, 2020.
  Human1 integrates previous human metabolic reconstructions into a unified model for omics analysis and tissue- and disease-related metabolism research. Reading it alongside yeast models helps explain how human metabolic networks, gene annotations, and condition-specific analyses fit together.
  - Why read: Use a maintained reference model when moving from microorganisms to human cells.
  - Reading note: A generic human network must be adapted to tissue, cell state, and culture conditions; it is not automatically a model of a particular cell.

- **Virtual Metabolic Human** — [The Virtual Metabolic Human database: integrating human and gut microbiome metabolism with nutrition and disease](https://doi.org/10.1093/nar/gky992). Nucleic acids research, 2019.
  The Virtual Metabolic Human database integrates human and gut microbial metabolism with nutrition and disease information. It indexes reactions and metabolites across host, microbes, and diet and is a useful reference for organizing metabolic research resources and checking identifiers.
  - Why read: Look up metabolites, reactions, and biological context and explore the organization of host and microbial metabolism.
  - Reading note: Database associations and model entries need interpretation in the specific study context and do not replace condition-specific measurements.

- **Recon3D** — [Recon3D enables a three-dimensional view of gene variation in human metabolism](https://doi.org/10.1038/nbt.4072). Nature biotechnology, 2018.
  Recon3D links the human metabolic network with information including protein three-dimensional structures to analyze potential metabolic consequences of genetic variation. It illustrates a multiscale organization from genes and enzyme structures to systems-level phenotypes.
  - Why read: Understand how human GEMs can connect protein structure and genetic variation.
  - Reading note: Mapping structural information onto a network does not determine the intracellular kinetic effect of every variant.

- **CarveMe** — [Fast automated reconstruction of genome-scale metabolic models for microbial species and communities](https://doi.org/10.1093/nar/gky537). Nucleic acids research, 2018.
  CarveMe automatically reconstructs genome-scale metabolic models for microbial species and communities from a universal model. It makes reconstruction a repeatable computational process and provides a platform for studying large-scale modeling, network gaps, and community metabolic exchange.
  - Why read: Understand the roles of automated reconstruction and manual curation, and build microbial models for methodological experiments.
  - Reading note: Automated reconstruction and gap filling depend on prior knowledge and culture conditions. Key reactions and predicted phenotypes still require review.

## Enzyme constraints and kinetic parameters

- **EnzymeTuning** — [EnzymeTuning improves enzyme-constrained metabolic modeling and proteome abundance prediction through deep learning](https://doi.org/10.1038/s41467-026-73744-3). Nature communications, 2026.
  EnzymeTuning uses a generative adversarial network to optimize kcat values globally within enzyme-constrained metabolic models and incorporates protein degradation constants to infer protein synthesis rates. The authors evaluate metabolic and proteome-abundance predictions across yeast species and E. coli and examine enzyme allocation under nutrient limitation.
  - Why read: Compare predicting kcat independently with jointly optimizing parameters for a systems model.
  - Reading note: Optimized parameters serve model fitting. Whether they correspond to independently measured intracellular enzyme kinetics requires additional verification.

- **UniKP** — [UniKP: a unified framework for the prediction of enzyme kinetic parameters](https://doi.org/10.1038/s41467-023-44113-1). Nature communications, 2023.
  UniKP uses protein and substrate representations to predict multiple enzyme kinetic parameters. It can be read alongside DLKcat to compare data curation, sequence and chemical representations, prediction tasks, and applications to enzyme engineering and systems modeling.
  - Why read: Compare the learning problems for kcat, Km, and related parameters and establish simple, inspectable baselines.
  - Reading note: How similar sequences and identical substrates are assigned to training and test sets strongly affects the interpretation of generalization.

- **DLKcat** — [Deep learning-based kcat prediction enables improved enzyme-constrained model reconstruction](https://doi.org/10.1038/s41929-022-00798-z). Nature Catalysis, 2022.
  DLKcat predicts enzyme turnover numbers, kcat, from protein sequences and substrate structures and uses those predictions to construct enzyme-constrained models. It connects enzyme-level supervised learning with systems-level phenotype prediction, showing how parameter prediction can affect downstream metabolic modeling.
  - Why read: Trace how errors in sequence- and substrate-based parameter prediction propagate through a metabolic network.
  - Reading note: The in vitro kinetic training data are sparse and noisy. Predicted values should not be equated directly with actual intracellular turnover numbers.

- **GECKO** — [Improving the phenotype predictions of a yeast genome-scale metabolic model by incorporating enzymatic constraints](https://doi.org/10.15252/msb.20167411). Molecular systems biology, 2017.
  GECKO adds enzyme constraints to metabolic reactions, bounding flux by enzyme abundance multiplied by its turnover number. The yeast study examines carbon sources, stress, and pathway overexpression, and shows how quantitative proteomics can narrow the feasible flux space.
  - Why read: Understand how a GEM becomes an enzyme-constrained GEM and what information protein abundance and kinetic parameters each contribute.
  - Reading note: The resulting flux ranges depend on how enzyme abundance, kinetic parameters, and enzyme capacities are specified.

- **Semi-supervised kcat prediction** — [Going beyond labels: Semi-supervised learning for enzyme kinetic parameter prediction](https://doi.org/10.64898/2026.10.15.759462). 预印本, 2026.
  This preprint proposes regularized semi-supervised kcat prediction using enzyme-substrate pairs that lack kcat but have other kinetic records. Rather than assign pseudo-labels, it trains with labeled and unlabeled examples together. On CataPro data clustered at 40% sequence identity, neural consistency and graph Laplacian regularization reportedly benefit from unlabeled records; gains require sufficient labeled data and saturate after several thousand unlabeled records. This description is based on the abstract.
  - Why read: Explore incomplete kinetic records as additional information for sparse kcat prediction and consider the role of feature-space density, rather than only proximity, when constructing training sets and benchmarks.
  - Reading note: Only the abstract was checked. Detailed splits, explicit sequence-cluster or enzyme-family holdouts, and gains on independent external datasets remain unverified. There is no verified downstream enzyme-constrained-model evaluation, so effects on flux prediction cannot yet be assessed.

## Machine learning and mechanistic models

- **Supervised learning from omics to flux** — [Predicting metabolic fluxes from omics data via machine learning: Moving from knowledge-driven towards data-driven approaches](https://doi.org/10.1016/j.csbj.2023.10.002). Computational and structural biotechnology journal, 2023.
  The study trains supervised models on Escherichia coli transcriptomics, proteomics, and flux data and compares internal and external flux predictions with parsimonious FBA. It offers a direct entry point for comparing data-driven mappings with classical constraint-based optimization before considering their integration.
  - Why read: Establish simple omics-to-flux baselines and identify the training labels and target conditions.
  - Reading note: Dataset size, condition splits, and available inputs determine extrapolation ability. ML2Flux has not been verified as the formal method name.

- **Neural-mechanistic hybrid models** — [A neural-mechanistic hybrid approach improving the predictive power of genome-scale metabolic models](https://doi.org/10.1038/s41467-023-40380-0). Nature communications, 2023.
  The authors combine neural networks with constraint-based metabolic models to predict microbial phenotypes, evaluating E. coli and Pseudomonas putida under different media and gene-knockout conditions. The approach learns to compensate for incomplete mechanistic inputs while retaining metabolic network constraints.
  - Why read: Identify exactly which unknown quantity the neural network supplies and how mechanistic constraints enter training and prediction.
  - Reading note: Training phenotypes are still required. Generalization across species or beyond the studied culture conditions must be evaluated separately.

- **Deuterium imaging and GEM integration** — [Uncertainty-aware integration of deuterium metabolic imaging with genome-scale metabolic modeling reveals diet-associated feasible-space remodeling in mouse skeletal muscle](https://arxiv.org/abs/2610.15175v1). arXiv, 2026.
  This preprint proposes an uncertainty-aware workflow that integrates dynamic deuterium metabolic imaging into GEMs through soft flux constraints. Dynamic spectra follow labeled glucose administration in three muscle types in control and high-fat-diet mice, with a hierarchical four-state kinetic model for labeling. Because glucose labeling is more reliable than lactate and glutamate/glutamine signals, only two anchors are used: glucose handling mapped to hexokinase flux, and glucose-derived oxidative entry mapped to pyruvate dehydrogenase flux. This description is based on the abstract.
  - Why read: Consider how noisy in vivo tracer signals can constrain GEMs through intervals rather than point estimates, and how unreliable signals are excluded. This helps distinguish feasible flux ranges from directly measured fluxes when interpreting flux variability analysis.
  - Reading note: Only the abstract was checked. The robustness of the inferred intervals, resampling strategy, and independent tracer validation remain unverified. The magnitude and reliability of subsystem and high-fat-diet effects therefore remain uncertain.

## Single-cell and spatial metabolism

- **SCOOTI** — [Inferring metabolic objectives and trade-offs in single cells during embryogenesis](https://doi.org/10.1016/j.cels.2024.12.005). Cell systems, 2025.
  SCOOTI combines omics, metabolic modeling, and machine learning to infer metabolic objectives and trade-offs in single cells. The authors analyze embryonic development, cell-cycle phases, and quiescence and validate inferences using evidence including essential genes from CRISPR screens.
  - Why read: Move beyond a fixed biomass-maximization objective to ask which metabolic needs different cells prioritize.
  - Reading note: Inferred objectives depend on the model and candidate objective set. Independent functional measurements remain important for their biological interpretation.

- **METAFlux** — [Characterizing cancer metabolism from bulk and single-cell RNA-seq data using METAFlux](https://doi.org/10.1038/s41467-023-40457-w). Nature communications, 2023.
  METAFlux links gene expression with constraint-based modeling to characterize cancer metabolism from bulk and single-cell RNA data. Alongside scFEA and Compass, it provides an entry point for comparing network definitions, cellular differences, and downstream validation.
  - Why read: Compare different RNA-to-metabolism inference methods on the same biological question.
  - Reading note: Mapping transcription to reaction activity involves assumptions. Agreement between methods alone does not establish the actual flux state.

- **scFEA** — [A graph neural network model to estimate cell-wise metabolic flux using single-cell RNA-seq data](https://doi.org/10.1101/gr.271205.120). Genome research, 2021.
  scFEA represents a metabolic network as a factor graph and uses graph neural networks and flux-balance constraints to infer cell-wise metabolic flux from single-cell RNA data. The authors also generate matched metabolomics and RNA data to compare predicted changes with metabolite changes under oxygen and genetic perturbations.
  - Why read: Follow the assumptions linking RNA to metabolic state and examine how cell-to-cell heterogeneity enters the model.
  - Reading note: Metabolite abundance changes used for validation differ from direct flux measurements. That distinction remains necessary when interpreting RNA-inferred flux.

- **Compass** — [Metabolic modeling of single Th17 cells reveals regulators of autoimmunity](https://doi.org/10.1016/j.cell.2021.05.045). Cell, 2021.
  Compass combines single-cell RNA with metabolic network analysis to characterize Th17 metabolic states and propose polyamine-metabolism hypotheses related to pathogenic potential. Metabolic assays, chemical and genetic perturbations, and in vivo studies test the candidates, illustrating how computational analysis can guide experiments.
  - Why read: Follow the concrete sequence from transcriptomic inference through pathway selection to functional experiments.
  - Reading note: Computational scores describe network-supported metabolic states and should not be treated as directly measured absolute fluxes in individual cells.

## Experimental data and model validation

- **MEMOTE** — [MEMOTE for standardized genome-scale metabolic model testing](https://doi.org/10.1038/s41587-020-0446-y). Nature biotechnology, 2020.
  MEMOTE introduces standardized tests for genome-scale metabolic models, including annotation and stoichiometric consistency checks. It turns technical validation after reconstruction into a repeatable, comparable workflow and provides useful foundational checks for new or automatically reconstructed models.
  - Why read: Check structural and consistency requirements before comparing predictive performance.
  - Reading note: Passing structural and annotation tests does not establish experimental validity for growth, perturbation, or flux predictions.

## Weekly archive

- [2026-10-23](weekly/2026-10-23.md) (Chinese)

## Data and maintenance

- `data/papers.json`: paper records and bilingual reading annotations.
- `data/weeks/`: weekly snapshots, retrieval sources, and editorial selections.
- `scripts/radar.py`: collection, validation, rebuilding, and publishing.
- `prompts/weekly.zh-CN.md`: instructions for the weekly DeepSeek Harness task.

The build generates both `README.md` (English, the default GitHub landing page) and `README.zh-CN.md` (Simplified Chinese). Use the language links at the top to switch. Weekly reports and the dashboard remain in Chinese.

Titles, venues, and dates are checked against DOI registration metadata and Europe PMC where available. Records retain their verification date and evidence level. Corrections and additional references are welcome.
