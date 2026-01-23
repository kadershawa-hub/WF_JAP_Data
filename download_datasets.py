#!/usr/bin/env python3
"""
Dataset Download Script
Author: [Abdulqader Shawa]
Date: [23/01/2026]

This script downloads the large datasets from Google Drive.
The full datasets are too large for GitHub (>1GB each).
"""

import os
import json
import subprocess
import sys
import time

def install_gdown():
    """Install gdown if not available."""
    try:
        import gdown
    except ImportError:
        print("Installing gdown...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
        import gdown
    return gdown

def download_with_gdown(file_id, output_path, retries=3):
    """Download a file using gdown with retry logic."""
    gdown = install_gdown()
    
    for attempt in range(retries):
        try:
            print(f"Downloading to {output_path}...")
            gdown.download(
                f"https://drive.google.com/uc?id={file_id}",
                output_path,
                quiet=False
            )
            
            # Check if file was downloaded
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                file_size = os.path.getsize(output_path) / (1024**3)
                print(f"✓ Download complete: {output_path} ({file_size:.2f} GB)")
                return True
            else:
                raise Exception("Downloaded file is empty or doesn't exist")
                
        except Exception as e:
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print(f"✗ Failed after {retries} attempts: {e}")
                return False
    return False

def main():
    """Main download function."""
    print("=" * 60)
    print("Dataset Download Script")
    print("=" * 60)
    
    # Read metadata
    if not os.path.exists('dataset_metadata.json'):
        print("Error: dataset_metadata.json not found!")
        print("Make sure you're in the repository root directory.")
        return
    
    with open('dataset_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    print(f"Found {len(metadata['datasets'])} datasets:")
    for i, dataset in enumerate(metadata['datasets'], 1):
        print(f"  {i}. {dataset['name']} ({dataset['size_gb']} GB)")
    
    print("\n" + "=" * 60)
    
    # Ask which datasets to download
    print("Which datasets would you like to download?")
    print("1. Download all datasets")
    print("2. Download specific datasets")
    print("3. Exit")
    
    choice = input("Enter choice (1-3): ").strip()
    
    datasets_to_download = []
    
    if choice == "1":
        datasets_to_download = metadata['datasets']
        print("Downloading all datasets...")
    elif choice == "2":
        print("\nAvailable datasets:")
        for i, dataset in enumerate(metadata['datasets'], 1):
            print(f"  {i}. {dataset['name']}")
        
        selections = input("Enter dataset numbers (comma-separated, e.g., '1,2'): ").strip()
        indices = [int(idx.strip()) - 1 for idx in selections.split(',')]
        datasets_to_download = [metadata['datasets'][i] for i in indices if i < len(metadata['datasets'])]
    else:
        print("Exiting.")
        return
    
    # Download selected datasets
    print("\nStarting downloads...")
    print("-" * 60)
    
    successful_downloads = []
    
    for dataset in datasets_to_download:
        print(f"\nDataset: {dataset['name']}")
        print(f"Size: {dataset['size_gb']} GB")
        print(f"Description: {dataset['description']}")
        
        output_path = f"data/{dataset['name']}"
        
        # Check if file already exists
        if os.path.exists(output_path):
            overwrite = input(f"File {output_path} already exists. Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("Skipping...")
                continue
        
        # Download the file
        success = download_with_gdown(dataset['file_id'], output_path)
        
        if success:
            successful_downloads.append(dataset['name'])
    
    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    
    if successful_downloads:
        print("✓ Successfully downloaded:")
        for name in successful_downloads:
            print(f"  - {name}")
        
        print("\nFiles are located in the 'data/' directory.")
        print("\nFor citation and usage terms, see dataset_metadata.json")
    else:
        print("No files were downloaded.")
    
    print("\nAlternative download methods:")
    print("1. Manual download from Google Drive links in metadata.json")
    print("2. Use wget: wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=FILE_ID'")

if __name__ == "__main__":
    main()
