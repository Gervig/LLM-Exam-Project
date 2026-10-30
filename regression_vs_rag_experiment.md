# Linear Regression vs. Local LLM + RAG

*Comparison exercise for the exam project "LLM for Developers".*

> **How to use this file.** Everything marked **[PASTE: ...]** or **[X]** is for your own results. The setup facts and the observations come from our runs, but check each one against your final notebook output before you keep it. The synopsis is limited to 5 pages, so condense this text before you submit it. Delete these blockquote hints when you are done.

---

## 1. Question

Can a local LLM that receives retrieved examples (RAG) predict the same number as a linear regression model trained on the full dataset? And what does the comparison show about when each approach is the right tool?

The exam does not expect the LLM to win. The aim is to compare two different approaches to the same numerical task and to explain the differences from **measured** results.

## 2. Task and data

| | |
|---|---|
| Task | Predict the sale price of an apartment from its size |
| Input | `size_m2`, the size in square metres |
| Target | `price_kdkk`, the sale price in thousand DKK |
| Data | 45 synthetic rows: `price = 42 · size + 350 + noise`, noise normally distributed with standard deviation 120, sizes drawn between 30 and 150 m² (the 45 rows span 37 to 148 m²), random seed 42 |
| Split | 40 training/reference rows and 5 held-out test cases (`train_test_split`, `random_state=42`) |
| Test inputs | 37, 72, 78, 106 and 107 m² |

**Why synthetic data.** It is reproducible, contains no personal data, and the relationship is linear by construction. The last point also favours the regression model, which is a limitation of the experiment (see section 7).

**One detail worth noting.** The smallest test case (37 m²) is just below the smallest training example (38 m²), so it is a small extrapolation.

**No leakage.** The test prices are kept in a separate variable (`y_test`) and are only read in the comparison step. Neither approach sees them.

> **[PASTE: optional scatter plot of the training data]**

## 3. Approach A: linear regression

- Model: scikit-learn `LinearRegression`, fitted on the 40 training rows only.
- Learned line: `price = 42.70 · size + 296.52` (the line that generated the data is `42 · size + 350`).
- Predictions for the 5 test cases: 1876, 3371, 3627, 4822 and 4865 thousand DKK.

## 4. Approach B: local LLM + RAG

### 4.1 Setup

| Component | Choice |
|---|---|
| Chat model | `qwen3:4b` via Ollama (thinking switched off, temperature 0) |
| Embedding model | `nomic-embed-text` via Ollama (768-dimensional vectors) |
| Retrieval | Cosine similarity over all chunks, top 5 (`TOP_K = 5`), implemented by hand with numpy |
| Hardware | **[X: laptop, RAM, CPU/GPU]** |

### 4.2 The RAG collection

The collection has **41 chunks**: one short background note and one sentence per **training** row, for example:

```
An apartment of 84 m2 sold for 3798 thousand DKK.
```

Each training row is its own chunk, so a row is never split in half (which would happen with chunking by character count). **No test row is in the collection.** The collection is saved in `rag_data/rag_collection.txt` so it can be inspected.

### 4.3 How a prediction is made

```
question ("Predict the price of an apartment of 78 m2")
   -> embedding model -> 768 numbers
   -> cosine similarity against all 41 chunk vectors
   -> the 5 most similar chunks
   -> pasted into the prompt as "Context:" followed by the question
   -> qwen3:4b -> reply -> price extracted from the reply
```

The model itself is unchanged and is not trained on the data. The only difference between "with RAG" and "without RAG" is the text it receives.

### 4.4 Prompt (4T's)

```
Traits: You are a careful data analyst who estimates numbers from the examples you are given.
Task: Predict the sale price of an apartment from its size, using the example sales in the context.
Tone: Precise and matter-of-fact. No explanations.
Target: A script that reads your answer. Reply with ONLY one number: the price in thousand DKK, no unit and no text.
```

The user message is `Context:` followed by the 5 retrieved chunks, then `Predict the sale price (in thousand DKK) of an apartment of {size} m2.`

### 4.5 Reading the answer

The model often ignored "reply with ONLY one number" and wrote a short derivation first, so the price has to be extracted from the text. The rules used:

- A short reply with exactly one number is the answer.
- Otherwise, a marked answer (`Answer: ...`, `**Answer**: ...` or `\boxed{...}`).
- Anything else counts as unreadable. The question is asked again (up to 3 attempts, retries at a small temperature), and if all attempts fail the result is NaN.

> **[Check]** Make sure this matches the notebook version you actually ran.

### 4.6 Rules from the exam

- The RAG collection only holds training rows and background text.
- The LLM never calls the regression model and never executes code. Everything it computes, it computes in its own text.
- Results are reported as measured, including failures.

### 4.7 Optional baseline: LLM without RAG

The same question without any context. This is an extra baseline, not an exam requirement. It shows what the model brings on its own.

> **[PASTE: one or two sentences on how this baseline was run, and if anything was adjusted.]**

## 5. Results

Absolute error is `|prediction - actual|`, and MAE is the mean absolute error over the test cases. Units are thousand DKK.

> **[PASTE: results table from Step 5 of the notebook.]** The skeleton below already has the actual values and the regression results. Fill in the LLM columns, or replace the whole table with the notebook's output.

| Size (m²) | Actual | Regression | Abs. error (regression) | LLM + RAG | Abs. error (LLM + RAG) |
|---:|---:|---:|---:|---:|---:|
| 37 | 1800 | 1876 | 76 | [X] | [X] |
| 72 | 3332 | 3371 | 39 | [X] | [X] |
| 78 | 3634 | 3627 | 7 | [X] | [X] |
| 106 | 4822 | 4822 | 0 | [X] | [X] |
| 107 | 4925 | 4865 | 60 | [X] | [X] |
| **MAE** | | | **36.4** | | **[X]** |

> **[PASTE (optional): the same table with the "LLM without RAG" columns.]**

### 5.1 Figure

> **[PASTE: figure showing the regression line, the training data, the actual test values and both sets of predictions.]**
>
> *To save it from the notebook, add `plt.savefig("figures/regression_vs_rag.png", dpi=200)` just before `plt.show()` in the plotting cell (and create the folder with `Path("figures").mkdir(exist_ok=True)`). Then keep the line below.*

![Regression line, test cases and LLM predictions](figures/regression_vs_rag.png)

### 5.2 What was retrieved

The exam asks you to document what the LLM retrieved. Example from our run, for the 37 m² question:

| Rank | Similarity | Retrieved chunk |
|---:|---:|---|
| 1 | 0.899 | An apartment of 84 m2 sold for 3798 thousand DKK. |
| 2 | 0.898 | An apartment of 57 m2 sold for 2688 thousand DKK. |
| 3 | 0.896 | An apartment of 84 m2 sold for 3840 thousand DKK. |
| 4 | 0.893 | An apartment of 63 m2 sold for 2956 thousand DKK. |
| 5 | 0.892 | An apartment of 137 m2 sold for 6283 thousand DKK. |

> **[PASTE: the retrieval output for the other test cases (the "What was retrieved?" cell), at least for one more case.]**

## 6. Findings

> **[X] = fill in from your final table.**

### 6.1 Accuracy

The linear regression model reached an MAE of **36.4** thousand DKK. The LLM + RAG reached **[X]**, which is **[X]** times [higher / lower]. The largest LLM error was **[X]** at **[X]** m², and the smallest was **[X]** at **[X]** m².

> **[PASTE: one sentence on the no-RAG baseline, if you included it, and what RAG changed.]**

### 6.2 Observations from the runs

1. **Retrieval does not find the numerically closest rows.** For the 37 m² question, the closest training examples (38 to 41 m²) were not retrieved. The model received 57 to 137 m² examples instead. All similarity scores were between about 0.89 and 0.90, so the embedding model barely distinguishes the rows. Embeddings capture what a text is about, not how close two numbers are.

2. **The model imitates statistics in words.** Without being given any code, it interpolated between the two nearest examples (72 m²: between 63 m² and 74 m²), averaged the price per square metre (106 m² and 37 m²), and once wrote out a regression formula with a slope and intercept in its answer. This stays inside the exam rules, because it did not call the regression model or run code, but it is a language-based approximation of arithmetic, not a fitted model.

3. **Formatting instructions are not reliable.** Asked for "only one number", the model wrote derivations. A first parser that took the first number in the reply returned 37, 72, 43.64 and 1 (an apartment size, a slope and a list marker). A fallback that took the last number turned an off-topic reply into the prediction 130. Reading and validating the answer is part of the experiment, because a wrong parser looks exactly like a wrong model.

4. **One reply was about something completely different.** For 107 m² the model answered a question about a JSON file for a game character, the same way in two runs. It disappeared after unloading the model with `ollama stop qwen3:4b`, which points to stale model state in Ollama and not to the prompt or the data.

5. **Even at temperature 0, results are not fully repeatable.** The identical question for 37 m² returned 1708 in one run and 1754 in another.

### 6.3 Why the approaches differ

| | Linear regression | Local LLM + RAG |
|---|---|---|
| What happens to the data | Fitted: the line is the least-squares solution over all 40 training rows | Not trained on. At most 5 rows are shown in the prompt |
| Output | Deterministic and exact to the model | Text from which a number is extracted, can vary between runs |
| Explanation | Two numbers: slope 42.70 and intercept 296.52 | A written derivation that may or may not be correct |
| Speed and cost | Milliseconds | Seconds to minutes per question on a laptop |
| Sensitivity | Uses every row equally | Depends on which rows retrieval happens to select |

The regression model has the right form for this data: the data is linear by construction, and the model uses all 40 rows. The LLM sees a handful of rows chosen by a text-similarity measure and has to reason from them.

### 6.4 Was RAG useful?

> **[PASTE: your answer, based on the no-RAG comparison.]** Points to cover: what the model without RAG knew about the price level, and what the retrieved examples gave it that its own knowledge did not.

### 6.5 When is a trained model preferable?

- Numerical, tabular data with a clear relationship, as here.
- When you need the same answer every time, quickly and cheaply.
- When the result must be explainable and checkable (coefficients, error measures).
- When many predictions are needed.

LLM + RAG is the better fit when the information is text, when there is no labelled dataset or training pipeline, and when a natural-language explanation is part of the product.

## 7. Limitations and possible improvements

**Limitations**

- Only 5 test cases from one split and one random seed, so a single case can change the conclusion.
- Synthetic, exactly linear data favours the regression model.
- A small model (4B parameters) running on a laptop CPU.
- Embedding-based retrieval is poor at numerical closeness (see 6.2).
- Unreadable or off-topic replies, answer parsing, and results that vary between runs.
- **[X: anything else you encountered]**

**Possible improvements**

- More test cases and several seeds, with the MAE averaged over them.
- Test `TOP_K = len(chunks)` (all rows in the prompt) to see whether retrieval is the bottleneck.
- Retrieve by numerical closeness (the nearest sizes) instead of, or together with, embeddings.
- A larger local model, if the hardware allows it.

## 8. Conclusion

> **[X: 3 to 4 sentences.]** Suggested skeleton: which approach was more accurate and by how much, the main reason (what each approach has access to and how it uses it), whether RAG helped, and when you would choose each approach.

---

## Appendix A. Reproducing the experiment

```
ollama pull qwen3:4b
ollama pull nomic-embed-text
uv sync
# open linear_regression_vs_rag.ipynb and run the cells from top to bottom
```

- Files: the notebook, `rag_data/rag_collection.txt` (the full RAG collection), `figures/` (plots).
- Versions: **[PASTE: output of `ollama --version` and `ollama list`]**
- If the model gives off-topic replies, unload it with `ollama stop qwen3:4b` and run the cell again.

## Appendix B. Raw replies (optional)

> **[PASTE: the raw model reply for one or two test cases, to show the derivations the model wrote.]**

---

## Before you submit (delete this section)

- [ ] Re-run the notebook from top to bottom and save it with its outputs.
- [ ] Paste the results table, the MAE, the figure and the retrieval output, and replace every **[X]** and **[PASTE]**.
- [ ] Decide what to do with the "without RAG" baseline. If the notebook still asks that model about `size * 10`, remove it or describe it openly in section 4.7. It changes the question the model is asked, and the factor was chosen after seeing the test prices.
- [ ] Check that sections 4.4 and 4.5 match the notebook version you actually ran.
- [ ] Check every number in section 6.2 against your own output.
- [ ] Delete the hint blockquotes and this checklist.
