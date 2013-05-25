This script searches phylopic.org for taxon silhouettes and downloads them.

To use from the command line:

    ./phylopic.py "Homo sapiens" "Pan troglodytes" "Mus musculus"

To use from Python:

    import phylopic
    phylopic.download_pics('Homo sapiens', 'Pan troglodytes', 'Mus musculus')