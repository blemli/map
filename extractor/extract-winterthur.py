#!/usr/bin/env python3
import os
import requests
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine output path based on environment
# Use /data in container, local directory otherwise
if os.path.exists('/data') and os.access('/data', os.W_OK):
    DATA_DIR = '/data'
else:
    DATA_DIR = BASE_DIR
    logger.info(f"'/data' directory not found or not writable, using local directory: {DATA_DIR}")

OSM_URL = "https://download.geofabrik.de/europe/switzerland-latest.osm.pbf"
RELATION_URL = "https://api.openstreetmap.org/api/0.6/relation/1691239/full"
OUTPUT_PATH = os.path.join(DATA_DIR, "winterthur.osm.pbf")

def download_relation():
    """Download the Winterthur relation"""
    logger.info("Downloading Winterthur relation from OpenStreetMap API")
    response = requests.get(RELATION_URL)
    response.raise_for_status()
    
    relation_path = os.path.join(BASE_DIR, "winterthur.osm")
    with open(relation_path, "wb") as f:
        f.write(response.content)
    
    logger.info(f"Downloaded Winterthur relation to {relation_path}")
    return relation_path

def download_and_extract(relation_path):
    """Download Switzerland OSM data and extract Winterthur"""
    pbf_path = os.path.join(BASE_DIR, "switzerland.osm.pbf")
    
    # Download Switzerland OSM data
    logger.info(f"Downloading Switzerland OSM data from {OSM_URL}")
    response = requests.get(OSM_URL, stream=True)
    response.raise_for_status()
    
    with open(pbf_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    logger.info(f"Downloaded Switzerland OSM data to {pbf_path}")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Extract Winterthur using osmium
    logger.info(f"Extracting Winterthur data using osmium to {OUTPUT_PATH}...")
    
    subprocess.run([
        "osmium", "extract", "--overwrite",
        "-p", relation_path,
        pbf_path, "-o", OUTPUT_PATH
    ], check=True)
    
    logger.info(f"Extracted Winterthur data to {OUTPUT_PATH}")
    
    # Clean up temporary files
    os.remove(pbf_path)
    logger.info(f"Cleaned up temporary file {pbf_path}")

def main():
    try:
        logger.info(f"Starting extraction at {datetime.now()}")
        logger.info(f"Output will be saved to: {OUTPUT_PATH}")
        relation_path = download_relation()
        download_and_extract(relation_path)
        logger.info(f"Extraction completed successfully at {datetime.now()}")
    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        raise

if __name__ == "__main__":
    main()