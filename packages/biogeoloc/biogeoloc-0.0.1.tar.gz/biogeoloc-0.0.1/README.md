# biogeoloc
A python object package for storing and managing geographic information about biological samples

## Installation
```
pip install biogeoloc
```

## Example
1. `Accession`

`Accession` objects are used to store information about a biological sample. This information includes the sample's geographic location, the date it was collected, and any other relevant information.

There are three main information types that can be stored in an `Accession` object:

- `Coordinates`: The geographic location of the sample
- `IDs`: You can store different types of IDs for the sample
- `passport`: Information about the sample, such as the date it was collected, the collector, and any other relevant information
- `phenotypic`: Information about the sample's phenotype
- `dataset`: Information about the dataset the sample belongs to
- `properties`: Any other relevant information about the sample

```python
from biogeoloc import Accession

acc = Accession('u0001', genesys_id='23412', pi_id=['PI628326', 'PI326387'], lib_id='333', latitude=12.345, longitude=23.456, dataset={'reseq': True})
```

2. `AccessionSet`

`AccessionSet` objects are used to store multiple `Accession` objects. This is useful when you have a collection of samples that you want to manage together.

```python
from biogeoloc import AccessionSet

acc1 = Accession('xyx1', lat=1.0, lon=2.0, alt=3.0, lib_id='lib1', pi_id='pi1')
acc2 = Accession('xyx2', lat=1.0, lon=2.0, lib_id='lib2', pi_id_list=['pi2', 'pi3'], is_id_list=['is2', 'is3'])
acc3 = Accession('xyx3', is_id='is3', lib_id='lib3', pi_id='pi3')

AS = AccessionSet('test', '2020-01-01',
                    default_ID_items={'lib_id': str, 'pi_id': list, 'is_id': list})
AS.add(acc1)
AS.add(acc2)
AS.add(acc3)

AS.build_index()

uniq_id = AS.search('lib1', 'lib_id')
acc = AS.get(uniq_id)

print(vars(acc))
```

3. `GeneSys`

`GeneSys` objects are used to parse and store information from the Genesys database. This is useful when you want to access information about a sample from the Genesys database.

Go to [GeneSys Website](https://www.genesys-pgr.org/) to download the accessions data in a zip file. Extract the zip file and use the `GeneSys` object to parse the data.

```python
from biogeoloc import GeneSys

download_genesys_dir = '/path/to/downloaded/genesys/data'
sorghumGS = GeneSys()
sorghumGS.load(download_genesys_dir)
sorghumGS.build_index()

q_id = 'PI207841'
u_id = sorghumGS.search(q_id)
acc = sorghumGS.get(u_id)
```


