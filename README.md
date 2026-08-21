# Search Engine Bias Analysis

Statistical analysis of search engine bias using Google and Bing search results.

This project was developed as the final project for the **Web Information Retrieval** course during my B.Sc. studies in Computer Engineering.

The implementation is inspired by the methodology proposed in the paper:

> **Are Search Engines Biased? Detecting and Reducing Bias using Meta Search Engines**  
> Patrick Maillé, Gwen Maudet, Mathieu Simon, Bruno Tuffin  
> Electronic Commerce Research and Applications (2022)

Unlike the original work, this repository provides an independent implementation developed from scratch in Python for educational and research purposes.

---

# Project Overview

Search engines play a major role in determining which information users access first. Since ranking algorithms are proprietary and largely opaque, detecting potential ranking bias is an important research problem.

This project compares search results returned by **Google** and **Bing**, performs statistical analyses on their rankings, stores historical observations in a local database, and visualizes the obtained results.

The goal is not to prove that a search engine is biased, but to provide a reproducible framework for investigating differences between ranking behaviors.

---

## Research Timeline

This project was initiated during my Bachelor’s studies in Computer Engineering at Islamic Azad University, Bushehr Branch.

- **May 22, 2024:** Initial reading and critical review of the research paper  
  *“Are Search Engines Biased? Detecting and Reducing Bias using Meta Search Engines” (Maillé et al., 2022)*

- Following this study, I independently implemented a Python-based system to reproduce and extend the methodology in an educational and experimental setting.

- The implementation was developed as part of the Web Information Retrieval course final project.

  
---


# Workflow

```
          User Query

               │

               ▼

  Google API          Bing

      │               │

      └──────┬────────┘

             ▼

      Ranking Comparison

             ▼

    Statistical Analysis

        χ² + Dixon Q

             ▼

      SQLite Database

             ▼

      Visualization
```

---

# Features

- Compare Google and Bing search results
- Detect overlapping search results
- Chi-Square statistical analysis
- Dixon Q outlier detection
- SQLite database for storing search history
- Interactive graphical interface using Tkinter
- Statistical visualization using Matplotlib and Seaborn
- Historical search analysis
- Distribution analysis of search results

---

# Statistical Methods

Two statistical approaches are implemented.

## Chi-Square Test

The Chi-Square test evaluates whether observed ranking differences between search engines are statistically significant.

## Dixon Q Test

The Dixon Q test is used to identify potential outliers that may indicate unusual ranking behavior.

These statistical methods provide quantitative evidence for investigating search engine ranking differences.

---

# Technologies

- Python
- SQLite
- Requests
- BeautifulSoup
- NumPy
- SciPy
- Matplotlib
- Seaborn
- Tkinter

---

# Repository Structure

```
Search-Engine-Bias-Analysis/

├── src/
│   └── Search_Engine_Bias.py
│
├── figures/
│   ├── comparison.png
│   └── gui.png
│
├── database/
│   └── sample_database.png
│
├── docs/
│   ├── Presentation_FA.pdf
│   └── Related_Paper.pdf
│
├── data/
│   └── README.md
│
├── examples/
│   └──  search_history.db
│
├── requirements.txt
├── LICENSE
├── CITATION.cff
└── README.md
```

---

# Example Analysis

The application allows users to

- submit a search query,
- retrieve search results from Google and Bing,
- compare retrieved URLs,
- perform statistical tests,
- store observations,
- visualize ranking distributions,
- inspect historical search records.

---

# Screenshots

The `figures/` directory contains sample outputs including

- GUI interface
- Search comparison
- Statistical plots
- Distribution histograms

---

# Database

Search history is stored locally using SQLite.

Each record contains

- Search query
- Google results
- Bing results
- Statistical outcome
- Bias indicator
- Timestamp

---

# Educational Purpose

This repository was developed for educational and research purposes.

It demonstrates

- Information Retrieval
- Statistical Data Analysis
- Scientific Programming
- Data Visualization
- GUI Development
- Database Programming
- Web Scraping

---

# Reference

Patrick Maillé, Gwen Maudet, Mathieu Simon, Bruno Tuffin.

**Are Search Engines Biased? Detecting and Reducing Bias using Meta Search Engines**

Electronic Commerce Research and Applications, 2022.

DOI:
https://doi.org/10.1016/j.elerap.2022.101132

---

# Disclaimer

Google search results require a valid Google Custom Search API key.

For security reasons, API credentials are **not included** in this repository.

Users should create their own API credentials before running the project.

---

# Author

**Hannah Fathi**

Research Interests

- Computer Vision
- Remote Sensing
- Medical AI
- Machine Learning
- Information Retrieval
- Large Language Models

---
