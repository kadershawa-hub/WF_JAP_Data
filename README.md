# Dataset Repository

## 📊 Datasets

This repository contains the structured datasets generated for the Website Fingerprinting on JAP research. Due to their large size, the actual CSV files are hosted on Google Drive. The files available here are metadata and download scripts.

### Dataset Information

1. **Original_Features.csv** (2.1 GB)
   - **Description**: This dataset contains features derived from **raw, unfiltered** network traffic captures. It includes all packets from each browsing session.
   - **Columns**: 80 columns
   - **Download**: [Google Drive Link](https://drive.google.com/file/d/1AyQqt8Rnm86Fctrgh0OJ54DhyZ2607Fz/view?usp=sharing)

2. **Filtered_Features.csv** (1.47 GB)
   - **Description**: This dataset contains features derived from traffic traces after **filtering out pure TCP ACK packets**. As demonstrated in our paper, removing this "OS chatter" reveals more stable and repeatable website fingerprints, leading to higher classification accuracy.
   - **Columns**: 80 columns
   - **Download**: [Google Drive Link](https://drive.google.com/file/d/14WrI5_RcbzCJ8terqemjoLs8Wnsjhf43/view?usp=sharing)

### 📄 Data Format & Column Description

Both CSV files share the same structure. Each row represents a single, unique visit to a website.

| Column Name | Description | Data Type / Format |
| :--- | :--- | :--- |
| `website` | **Label**: The name of the website visited (e.g., `adobe.com`). This is the target variable for classification. | String |
| `packet_sizes` | Raw packet sizes (in bytes) extracted from the PCAP using `dpkt`. | String representation of a list, e.g., `"[1064, 66, 1064, ...]"` |
| `packet_directions` | Raw packet directions (+1 for outgoing, -1 for incoming). | String representation of a list, e.g., `"[1, -1, -1, ...]"` |
| `packet_times` | Raw packet timestamps (in seconds) relative to the start of the capture. | String representation of a list, e.g., `"[0.0, 0.1935, 0.2119, ...]"` |
| `signed_packet_sizes` | **Input for Deep Learning models**: A sequence created by multiplying each packet's size by its direction, combining size and direction into one feature. | String representation of a list, e.g., `"[1064, -66, -1064, ...]"` |
| `[Column_3]` ... `[Column_76]` | **74 Statistical Features**: Aggregate statistics (e.g., total packets, mean packet size, burst features) used as input for Traditional Machine Learning models. The full list and descriptions are available in the paper's Appendix (Table~\ref{tab:statistical_features}). | Integer / Float |

> **Note for Users:** When loading the data in Python, you will need to parse the list-like strings (e.g., using `ast.literal_eval()` or `json.loads()`) to convert them back into actual list objects for processing.

## 🚀 Quick Start

### Prerequisites
```bash
pip install gdown pandas
```

### Download Data
Run the `download_datasets.py` script to get the full datasets.

```bash
python download_datasets.py
```

## 📝 Metadata

More detailed metadata can be found in `dataset_metadata.json`.

## 🔖 Citation
Please cite this dataset as: [Your citation here]

## 📄 License
Specify license (e.g., CC-BY 4.0)

## ✉️ Contact
kader.shawa@su.edu.ye
