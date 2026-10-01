# Day 4 Task — Will It Fit, and May I Use It?

## 1. Scenario and memory budget

My scenario is to run a local AI coding assistant on my Windows laptop for personal academic use. The assistant would help me understand Python code, debug small programs, and summarise short documents. It is intended for one student, not for public access or commercial deployment.

The system reports approximately **23.69 GB of physical system RAM**. My Day 4 estimator also detects a usable memory budget of **5.4 GB** for its model-fit calculation. The script uses dedicated GPU VRAM for the fit budget when it detects a supported dedicated GPU; otherwise, it uses a percentage of system RAM. Therefore, the 5.4 GB figure used in the current output is the estimator's selected budget, not the total system RAM. The hardware-detection output should be saved in the screenshots folder so that the detected memory type can be checked.

The estimates below are planning estimates. They do not guarantee that a model will run with exactly the same memory use on every system.

## 2. Concepts used in the decision

### 2.1 Model weights

Model weights are the values learned during training. The amount of memory needed for weights mainly depends on the number of parameters and the numerical format or quantization used to store them. In the estimator, weight memory is approximated by multiplying the parameter count in billions by the bytes-per-parameter value for the selected format.

For example, the 1.5B configuration using Q4_K_M has an estimated weight size of 1.5 × 0.57 = 0.855 GB. The script displays this as approximately 0.86 GB before KV-cache and runtime overhead are added. Larger models need more memory, so model size is one of the first things to check before downloading a model.

If weight memory is ignored, a model may be selected even though it cannot be loaded within the intended memory budget. This estimate is approximate because model files can also contain metadata and tensors that do not exactly follow the average bytes-per-parameter assumption.

### 2.2 Quantization

Quantization stores model weights using a lower-precision representation to reduce memory use. The estimator uses the following approximate bytes-per-parameter values:

| Format | Estimated bytes per parameter |
|---|---:|
| FP16 | 2.00 |
| Q8_0 | 1.00 |
| Q6_K | 0.81 |
| Q5_K_M | 0.68 |
| Q4_K_M | 0.57 |
| Q3_K_M | 0.43 |

These are effective estimation values in this script, not guaranteed fixed values for every model. For the same 8B model at an 8K context, the estimated total changes from 19.01 GB with FP16 to 10.21 GB with Q8_0, 7.39 GB with Q5_K_M, 6.42 GB with Q4_K_M, and 5.19 GB with Q3_K_M.

The lower-precision formats reduce the estimated memory requirement. However, lower precision can also affect answer quality, depending on the model and task. The estimate alone does not measure quality; the model should be tested on the intended coding and summarisation tasks.

### 2.3 KV cache and context length

The KV cache stores attention-related information for tokens processed during a conversation. It allows a model to use the previous context without recalculating everything from the beginning. In general, a larger context length requires more KV-cache memory.

The script estimates KV-cache memory using this simplified formula:

`KV cache (GB) = parameter count in billions × context length in thousands × 0.02`

It then adds the estimated weights and KV cache and applies a 10% overhead factor:

`Total estimate (GB) = (weights + KV cache) × 1.10`

This is a rough model. Actual KV-cache memory depends on factors such as architecture, attention design, cache precision, and inference runtime. A longer context does not change the model's weight size in this estimator, but it increases the estimated KV cache. This matters for a coding assistant or agent that keeps a long conversation or accumulates tool results.

### 2.4 Model cards

A model card is the documentation published for a model. It can describe the model's publisher, intended uses, limitations, parameter count, context length, supported features, and licence. Before selecting a model, I need to read the official model card and check the corresponding Ollama library entry for the specific model/build I plan to use.

A model name alone is not enough to confirm its licence or technical limits. Model-card details and the date they were checked should be recorded in the comparison table in Section 5.

### 2.5 Open-weight versus open-source licensing

An open-weight model makes its trained weights available, but that does not automatically mean that it is open-source software or that every use is unrestricted. The exact licence and any additional terms determine whether the model can be used commercially, redistributed, or used under other conditions.

For this personal student scenario, I still need to record the exact licence for each candidate model rather than assuming that every downloadable model has the same permissions. If the project later becomes a public or commercial application, licence conditions would become an even more important selection factor.

### 2.6 Tool-calling support

Tool calling allows a model to request actions from external functions, such as a calculator or a code tool, rather than only returning text. If the coding assistant later becomes an agent that runs tools, I should verify tool-calling support in the model card and in the specific runner/build. Tool-calling support should not be assumed just because a model can generate code.

## 3. Memory estimate table

The estimator applies a 10% overhead factor after adding the estimated weights and KV cache. The current script reports a selected usable budget of **5.4 GB**.

| Model configuration | Parameters (B) | Precision | Context (K) | Weights (GB) | KV cache (GB) | Total estimate (GB) | Fits within 5.4 GB budget? |
|---|---:|---|---:|---:|---:|---:|---|
| Qwen small (estimator label) | 1.5 | Q4_K_M | 8 | 0.86 | 0.24 | 1.20 | Fits comfortably |
| Granite / Qwen mid (estimator label) | 8.0 | Q4_K_M | 8 | 4.56 | 1.28 | 6.42 | Does not fit |
| Mid model, FP16 (estimator label) | 8.0 | FP16 | 8 | 16.00 | 1.28 | 19.01 | Does not fit |
| Large local model (estimator label) | 30.0 | Q4_K_M | 8 | 17.10 | 4.80 | 24.09 | Does not fit |
| Server-class model (estimator label) | 70.0 | Q4_K_M | 8 | 39.90 | 11.20 | 56.21 | Does not fit |

The names in this table are labels used by the estimator, not verified exact downloadable model versions. A model's actual GGUF/Ollama file size can differ from this formula-based estimate.

For the 1.5B Q4_K_M configuration, the estimated total is about 1.20 GB, which is below 70% of the 5.4 GB budget and is therefore marked “fits comfortably” by the script. The 8B Q4_K_M configuration is estimated at 6.42 GB and exceeds the selected budget. The 30B and 70B configurations are much larger than the budget and are not suitable for this estimator's selected memory target.

## 4. Context-length and quantization observations

### 4.1 Same 8B model, different context lengths

The quantization is kept fixed at Q4_K_M while the context length changes.

| Context length | Weights (GB) | KV cache (GB) | Total estimate (GB) | Fits within 5.4 GB? |
|---:|---:|---:|---:|---|
| 4K | 4.56 | 0.64 | 5.72 | No |
| 8K | 4.56 | 1.28 | 6.42 | No |
| 32K | 4.56 | 5.12 | 10.65 | No |
| 128K | 4.56 | 20.48 | 27.54 | No |

The estimated weight memory remains constant because the parameter count and quantization remain the same. The KV cache increases with context length, so the total estimate also increases. Under the current assumptions and a 5.4 GB budget, even the 4K configuration exceeds the budget.

### 4.2 Same 8B model, different quantizations

The context length is kept fixed at 8K while the quantization changes.

| Quantization | Weights (GB) | KV cache (GB) | Total estimate (GB) | Fits within 5.4 GB? |
|---|---:|---:|---:|---|
| Q3_K_M | 3.44 | 1.28 | 5.19 | Fits, but tight |
| Q4_K_M | 4.56 | 1.28 | 6.42 | No |
| Q5_K_M | 5.44 | 1.28 | 7.39 | No |
| Q8_0 | 8.00 | 1.28 | 10.21 | No |
| FP16 | 16.00 | 1.28 | 19.01 | No |

The KV cache remains constant because the parameter count and context length are unchanged. The estimated weight memory changes with the quantization format. In this table, Q3_K_M is the only listed 8B configuration that falls within the 5.4 GB budget, although it is classified as a tight fit by the estimator. It may involve a greater quality trade-off than higher-precision options, so quality should be checked with real tasks.

The largest context among the tested Q4_K_M settings that stays within the selected budget is **none**: even the 4K setting is estimated at 5.72 GB. A smaller model or a lower-memory configuration would be needed for this budget under the current estimator.

## 5. Comparison of three open models: model cards, licences, and Ollama builds

**This section must be completed after checking the official model cards and the Ollama library pages.** The current estimator output does not contain enough evidence to fill in exact model versions, licence names, context windows, commercial-use terms, tool-calling support, or Ollama download sizes. Those details should not be guessed.

Choose three candidates from different model families and fill the table from their official model cards and Ollama pages. Record the date you checked each source.

| Basis for comparison | Model 1 | Model 2 | Model 3 |
|---|---|---|---|
| Full model name and version | To verify | To verify | To verify |
| Publisher | To verify | To verify | To verify |
| Total / active parameters; MoE? | To verify | To verify | To verify |
| Context window | To verify | To verify | To verify |
| Exact licence name | To verify | To verify | To verify |
| Commercial use allowed? | Check licence | Check licence | Check licence |
| Additional conditions | Check licence | Check licence | Check licence |
| Tool calling stated on model card? | To verify | To verify | To verify |
| GGUF / Ollama build available? | Check Ollama library | Check Ollama library | Check Ollama library |
| Download size at Q4 | To verify | To verify | To verify |
| Estimated total for chosen configuration | Calculate | Calculate | Calculate |
| Fits the selected scenario budget? | Calculate | Calculate | Calculate |
| Date model card checked | Add date | Add date | Add date |
| Official model card URL | Add URL | Add URL | Add URL |
| Ollama library URL | Add URL | Add URL | Add URL |

The memory estimate and the actual downloadable build size are related but are not identical measurements. The comparison should use the exact model/version and quantized build that would be used in the scenario. The licence decision should be based on the exact licence and conditions, not simply on whether the weights are available to download.

## 6. Estimate versus actual runtime memory

The task requires at least one model to be installed and checked with Ollama. The estimator's current output alone does not provide the actual installed model size or the runtime memory reported by `ollama ps`, so those values must be collected from the machine before this section can be finalised.

Run the following commands after installing a small model for the test:

```powershell
ollama list
ollama run <model-name>
```

Keep the model running in one terminal, and in a second terminal run:

```powershell
ollama ps
```

Replace `<model-name>` with the exact model tag shown by `ollama list`. Save screenshots of both commands and record the output below.

| Measurement | Observed value |
|---|---|
| Exact model tag | Add from `ollama list` |
| `ollama list` size | Add observed size |
| `ollama ps` size / processor allocation | Add observed output |
| Processor allocation (CPU / GPU / split) | Add observed output |
| Estimator's weights estimate | Calculate for exact model configuration |
| Estimator's total estimate | Calculate using context and quantization |
| Was the estimate close? | Explain after comparing |
| Explanation of any difference | Consider context, quantization, architecture, runtime overhead, and offloading |

The estimate should be treated as a planning tool rather than a prediction to the megabyte. Differences can occur because the formula uses average bytes per parameter and a simplified KV-cache assumption, while a real runtime also depends on model architecture, the chosen build, context settings, and where the model is loaded. The processor allocation reported by Ollama helps show whether inference is using the GPU, CPU, or a split between them.

## 7. Suitability analysis

Based only on the current estimator output, the **1.5B Q4_K_M configuration** is the most practical starting point for the selected 5.4 GB budget: the estimated total is approximately 1.20 GB and the script classifies it as a comfortable fit. This is a preliminary memory-based choice, not yet a final model recommendation, because the exact model card, licence, Ollama build, and actual runtime result have not been recorded in this analysis.

The 8B Q4_K_M configuration is estimated at 6.42 GB for an 8K context and exceeds the selected budget. The 8B Q3_K_M configuration is estimated at 5.19 GB and is marked as a tight fit, but its answer quality should be tested before it is preferred over a smaller model. The 30B and 70B configurations exceed the budget by a large margin in the current estimate.

The final recommendation should be made after completing the three-model comparison and the estimate-versus-reality test. The runner-up should also be named at that point, with a reason based on memory, quality, context length, tool-calling support, and licence. More usable memory could make a larger model or higher quantization practical. A need for a longer context could change the choice because KV-cache memory increases with context length. A public or commercial release would make licence conditions a key requirement.

## 8. Conclusion

Model size matters most when the machine has a strict memory limit: a model that exceeds the available budget may not load as intended or may require CPU offloading. Quantization matters when a model is close to the memory limit because it can reduce weight memory, although lower precision may affect quality. Context length matters when the application needs long documents, long conversations, or an agent that accumulates tool results, because the KV cache grows as context increases. Licence terms matter whenever the model is redistributed, integrated into a public application, or used commercially; a model that fits in memory is not automatically permitted for every use.

For this personal student coding-assistant scenario, the estimator suggests beginning with a small Q4_K_M configuration and validating it with a real runtime test. The final choice should combine memory measurements, task quality, context requirements, tool-calling support if needed, and the exact licence terms. The current formula is useful for narrowing the options before downloading, but actual runtime measurements and verified model-card information are necessary before the final recommendation is complete.

## 9. Evidence and submission checklist

Save the following evidence in the repository's `screenshots/` folder:

- System hardware detection and memory-estimator output.
- The context-length experiment.
- The quantization experiment.
- Official model-card pages for the three selected models.
- The corresponding Ollama library pages.
- `ollama list` output.
- `ollama ps` output while a model is running.

The repository should include the estimator code, any script used for the experiments, this `analysis.md`, the screenshots folder, and a README. Before submission, replace every “To verify” or “Add observed output” entry in Sections 5 and 6 with checked information. The analysis should then describe the actual model versions, licence terms, runtime result, and final recommendation without relying on assumptions.
