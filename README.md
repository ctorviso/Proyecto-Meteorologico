### Pre-requisitos:
- [Conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html)

### Setup:
```sh
conda env create -f environment.yml
conda activate proyecto_meteorologico
```

### Ejecución (UNIX):
```sh
./run.sh
```

### Ejecución (Windows):
```sh
run.bat
```

### Notebooks:

```sh
conda install ipykernel
python -m ipykernel install --user --name=proyecto_meteorologico
```

Obtain API key from https://opendata.aemet.es/centrodedescargas/

Create .env file in root directory and add:
```AEMET_API_KEY=your_api key```
