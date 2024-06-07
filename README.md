# CONCERTO

Concerto is a memote repository for a community-level genome-scale metabolic model 
[Memote test results for the models](https://pnnl-compbio.github.io/CONCERTO/)


## Overview

This repository contains the continuous validation environment for a community-level genome-scale metabolic model (GEM) using Memote. Memote is a software tool that provides a suite of tests to ensure the quality and consistency of metabolic models. By integrating Memote into a continuous integration (CI) workflow, we can automatically validate updates to the GEM, ensuring that model modifications improve or maintain the model's integrity.

## Features

- **Automated Testing**: Utilize Memote for automated testing of metabolic model properties such as stoichiometric consistency, gene-protein-reaction (GPR) associations, and reaction SBO terms.
- **Continuous Integration**: Integrate with CI platforms like GitHub Actions or Travis CI to run Memote tests on every commit, ensuring model quality over time.
- **Version Control**: Track changes to the GEM using Git, allowing for revertible updates and collaborative development.
- **Memote Report**: Generate and store Memote history reports to visualize the model's quality over time and identify areas for improvement.
- **Documentation**: Detailed instructions for setting up the environment, running tests, and interpreting Memote reports.

## Quick Start

1. **Clone the Repository**
   ```
   git clone https://github.com/pnnl-predictive-phenomics/concerto.git
   cd concerto
   ```

2. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run Memote Tests Locally**
   ```
   memote run --filename "model.xml" --pytest-args "-v"
   ```

4. **Set Up Continuous Integration**
   - Configure your CI tool of choice by following the provided CI configuration guide.

5. **Interpret Results**
   - Review the output of Memote tests and reports for insights into model quality and validation status.

## Contributing

We welcome contributions to improve the model's quality and extend its capabilities. Please read `CONTRIBUTING.md` for guidelines on how to contribute.

## License

This project is licensed under the [Apache 2.0] license. See the `LICENSE` file for details.

## Contact

For support or to report issues, please file an issue on the GitHub issue tracker or contact the repository maintainers at [jeremy.zucker@pnnl.gov].

---

