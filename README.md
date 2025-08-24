![badge-labs](https://user-images.githubusercontent.com/327285/230928932-7c75f8ed-e57b-41db-9fb7-a292a13a1e58.svg)

<img align="right" width="40%" src="https://www.finos.org/hubfs/FINOS/finos-logo/FINOS_Icon_Wordmark_Name_RGB_horizontal.png">


# 🚀 Quick Start Guide

Follow these steps to set up and run the project.

---

## 1. Set Up the Conda Environment

Make sure you have [Conda](https://docs.conda.io/en/latest/) installed.

```bash
conda create -n myproject python=3.10 -y
conda activate myproject
```

## 2. Install Python Dependencies

Install required packages using pip:
```bash
pip install -r requirements.txt
```

## 3. Configure API Settings

Edit the api.yaml file to set your API credentials:
```
azure:
  api_key: [YOUR_API]
  api_base: [YOUR_API_BASE]
  api_version: [YOUR_API_VERSION]
  deployment_name: [YOUR_DEPLOYMENT_NAME]

brightdata:
  api_key: [YOUR_API]
  zone: [YOUR_ZONE]

```

## 4. Run the Experiment

Use the following command to run the main experiment script:
```bash
bash scripts/run_experiment.bash
```


# EMIR-specific RAG

Welcome to the EMIR-specific RAG repository. This project builds on the existing work done by AI4FINANCE to address key challenges in maintaining and expanding the DRR system. The initiative leverages AI to reduce maintenance costs and improve scalability across different jurisdictions and regulations.


## Overview

The DRR system, which generates reports based on existing regulations (e.g., EMIR), currently faces high maintenance costs and scalability challenges. This repository aims to address these issues by developing AI-based tools:
1. **AI-based Validator**: Checks the lineage consistency of the DRR system to reduce maintenance costs.
2. **AI-based Rule Generator/Copilot**: Generates new rules to expand the DRR system to other jurisdictions and regulations, such as Japan and Australia.

## Key Contributors

- **Ian**: Expert in the Common Domain Model (CDM) and ex-director of Market Infrastructure and Technology at ISDA.
- **Yanglet**: Fine-tuning FinGPT models
- **Charlie**: benchmarking model performance on analyzing EMIR regulatory data
- **Jaswanth Duddu**: Train FinGPT on CDM Documentation and benchmarking model performance
- **Matthew Tavares**: fetching and curation of EMIR regulatory data


## Roadmap

### Short Term Goals

1. **Review and Test EMIR Interpretation**
    - Extract "plain English" regulatory requirements.
2. **Train FinGPT on CDM Documentation**
    - Enable FinGPT to learn the "CDM language."
3. **Train FinGPT on Regulation-to-Rule Pairs**
    - Teach FinGPT to match regulatory requirements with the reporting rules.
4. **Fine-tune FinGPT**
    - Review existing DRR code and regulatory references to ensure correctness.

### Long Term Goals

1. **Deliver a Working Prototype**

### Estimated Time of Arrival

We will follow the following timeline  
1. Benchmarking existing models and identifying weaknesses: June 30, 2024 
2. Curation of EMIR regulatory data: July 20, 2024
3. Fine-tuning a FinGPT model using LoRA or RAG: July 31, 2024
4. Deliver a Working Prototype: August 20, 2024



## Contributing Guidelines

1. Fork it (<https://github.com/finos/EMIR-specific RAG/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Read our [contribution guidelines](.github/CONTRIBUTING.md) and [Community Code of Conduct](https://www.finos.org/code-of-conduct)
4. Commit your changes (`git commit -am 'Add some fooBar'`)
5. Push to the branch (`git push origin feature/fooBar`)
6. Create a new Pull Request

## Contact

For more information, feel free to reach out to the project maintainers:
- Ian: ian@southcardinal.ie 
- Maurizio (Mao): maoo@finos.org 

We look forward to your contributions and collaboration to make regulatory reporting more efficient and scalable.

## License

Copyright 2024 Fintech Open Source Foundation

Distributed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

SPDX-License-Identifier: [Apache-2.0](https://spdx.org/licenses/Apache-2.0)
