import requests
import xml.etree.ElementTree as ET
import pandas as pd


def get_homology_data(ensembl_id, species_list, taxon_filter):
    server = "https://rest.ensembl.org"
    #      "/homology/id/human/ENSG00000157764?format=condensed;type=orthologues"
    ext = f"/homology/id/human/{ensembl_id}?format=condensed;type=orthologues"
    
    response = requests.get(server + ext, headers={"Content-Type": "application/json"})
    if not response.ok:
        response.raise_for_status()
        return None
    
    data = response.json()
    homologies = data["data"][0].get("homologies", [])
    #print(homologies)
    homology_records = []
    for homology in homologies:
        species = homology["species"]
        if species in species_list or taxon_filter in homology["taxonomy_level"]:
            homology_records.append({
                "Species": species,
                "Homology type": homology["type"],
                "Protein ID": homology["protein_id"],
                "Taxonomy level": homology["taxonomy_level"],
                "Gene ID": homology["id"]
            })
    
    return homology_records



def get_Worm_symbol(gene_id):
  if gene_id == "":
    return " "
  # Base URL for WormBase API
  base_url = "https://wormbase.org/rest/widget/gene"

  # Construct the URL with the gene ID
  url = f"{base_url}/{gene_id}/overview"

  # Send the request
  response = requests.get(url)

  # Check if the request was successful
  if response.ok:
      data = response.json()
      # Extract the gene symbol from the JSON response
      gene_symbol = data['fields']['name']['data']['label']
      return gene_symbol
  else:
      return "NA"

def get_symbol_species(gene_id, species):
  if gene_id == "":
    return " "
  if species is None:
    return "No species"
  # Base URL for Ensembl API
  base_url = "https://rest.ensembl.org"
  # Endpoint for gene lookup by Ensembl ID, e.g., ENSMUSG00000056121
  url = f"{base_url}/lookup/id/{gene_id}?species={species}"

  # Send the request
  response = requests.get(url, headers={"Content-Type": "application/json"})

  # Check if the request was successful
  if response.ok:
      data = response.json()
      # Extract gene symbol
      gene_symbol = data.get("display_name", "Symbol not found")
      return gene_symbol
  else:
      return "Failed to retrieve data."
