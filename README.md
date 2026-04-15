# Beyond Approve-or-Deny — Auditing LLMs for Non-binary Treatment Discrimination in Lending

![Project banner / placeholder](assets/banner.png)

This project goal is to audit large language models (LLMs) to measure and mitigate non-binary treatment discrimination. This audit of of extreme importance as different LLMs in recent times have been stressed tested in making decisions in different critical domains. However, the use of the LLMs in lending has mostly framed it as a simple binary decision making process of either granting a loan or not.This way of stress testing might obscures the limitations that LLMs might have in terms of the decisions they make for lending. 

The repo contains the code for data processsing, serializations, and experimental setup.

## Repository layout
- README.md — this file
- data/ — raw and processed datasets (do not include sensitive data)
- notebooks/ — analysis and reproducible experiments
- src/ — core code: data processing, model wrappers, evaluation

Quick start
1. Create virtual environment and install
    - python -m venv .venv
    - source .venv/bin/activate
    - pip install -r requirements.txt
2. Prepare data
    - Place raw datasets into ./data
3. Run an experiment (example)
4. Evaluate results

## Contact & citation
- Author: INCLUDE LATER
- For questions, open an issue or contact via email in project metadata.
- If you use this work, please cite the project paper and include a link to this repo.


## License
This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
