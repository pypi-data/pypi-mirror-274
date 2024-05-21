class Accession:
    def __init__(self,
                 uniq_id,
                 lat=None,
                 lon=None,
                 alt=None,
                 sources=[],
                 IDs={},
                 passport={},
                 phenotypic={},
                 dataset={},
                 properties={},
                 **kwargs):

        self.uniq_id = str(uniq_id)

        # load the coordinate
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.update_coordinate()

        # load IDs
        self.IDs = IDs if IDs else {}
        for k, v in kwargs.items():
            if k.endswith("_id"):
                if k in self.IDs:
                    if isinstance(self.IDs[k], list):
                        self.IDs[k].append(v)
                    else:
                        self.IDs[k] = v
                else:
                    self.IDs[k] = v

            if k.endswith("_id_list"):
                k = k.replace("_id_list", "_id")
                if k in self.IDs:
                    self.IDs[k].append(v)
                else:
                    self.IDs[k] = v

        # load passport
        self.passport = passport if passport else {}

        # load phenotypic
        self.phenotypic = phenotypic if phenotypic else {}

        # load dataset
        self.dataset = dataset if dataset else {}

        # load properties
        self.properties = properties if properties else {}
        for k, v in kwargs.items():
            if not k.endswith("_id") and not k.endswith("_id_list"):
                self.properties[k] = v

        # load sources
        self.sources = sources

    def __str__(self):
        return """
----------------
Accession: %s
Coordinate: Lat: %s, Lon: %s, Alt: %s
Sources: %s
----------------
""" % (
            self.uniq_id,
            self.lat if self.lat else "None",
            self.lon if self.lon else "None",
            self.alt if self.alt else "None",
            self.sources
        )

    def __repr__(self):
        return self.__str__()

    def update(self, value, level1, level2=None):
        """
        Update the value of the accession
        level1: the level of the value, it can be "coordinate", "IDs", "passport", "phenotypic", "dataset", "properties"
        level2: the key of the value, if the level1 is "coordinate", it can be "lat", "lon", "alt"
        """

        if level1 == "coordinate":
            if level2 == "lat":
                self.lat = value
            elif level2 == "lon":
                self.lon = value
            elif level2 == "alt":
                self.alt = value
            else:
                print("Error: the level2 is not valid")
            self.update_coordinate()
        elif level1 == "IDs":
            if level2 in self.IDs:
                if isinstance(value, list):
                    self.IDs[level2] += value
                    self.IDs[level2] = list(set(self.IDs[level2]))
                else:
                    self.IDs[level2] = value
            else:
                self.IDs[level2] = value
        elif level1 == "passport":
            if level2 in self.passport:
                if isinstance(value, list):
                    self.passport[level2] += value
                    self.passport[level2] = list(set(self.passport[level2]))
                else:
                    self.passport[level2] = value
            else:
                self.passport[level2] = value
        elif level1 == "phenotypic":
            if level2 in self.phenotypic:
                if isinstance(value, list):
                    self.phenotypic[level2] += value
                    self.phenotypic[level2] = list(
                        set(self.phenotypic[level2]))
                else:
                    self.phenotypic[level2] = value
            else:
                self.phenotypic[level2] = value
        elif level1 == "dataset":
            if level2 in self.dataset:
                if isinstance(value, list):
                    self.dataset[level2] += value
                    self.dataset[level2] = list(set(self.dataset[level2]))
                else:
                    self.dataset[level2] = value
            else:
                self.dataset[level2] = value
        elif level1 == "properties":
            if level2 in self.properties:
                if isinstance(value, list):
                    self.properties[level2] += value
                    self.properties[level2] = list(
                        set(self.properties[level2]))
                else:
                    self.properties[level2] = value
            else:
                self.properties[level2] = value
        elif level1 == "sources":
            self.sources += value
            self.sources = list(set(self.sources))
        else:
            print("Error: the level1 is not valid")

    def update_coordinate(self):
        self.lat = float(self.lat) if self.lat is not None else None
        self.lon = float(self.lon) if self.lon is not None else None
        self.alt = float(self.alt) if self.alt is not None else None

        if self.lat is None and self.lon is None and self.alt is None:
            self.coordinate = None
        else:
            self.coordinate = (self.lat, self.lon, self.alt)


class AccessionSet:
    def __init__(self, name, date, default_ID_items={}, default_passport_items={}, default_phenotypic_items={}, default_dataset_items={}, default_properties_items={}):
        """
        items is a dict to store the default items for the accession
        example:
        items_dict = {
            'unique_id': str,
            'country': str,
            'reseq': bool,
            'dataset': list,
        }
        """

        self.name = name
        self.date = date
        self.default_ID_items = default_ID_items
        self.default_passport_items = default_passport_items
        self.default_phenotypic_items = default_phenotypic_items
        self.default_dataset_items = default_dataset_items
        self.default_properties_items = default_properties_items
        self.accession_dict = {}

    def add(self, accession):
        accession = self.acc_formatter(accession)
        self.accession_dict[accession.uniq_id] = accession

    def get(self, uniq_id):
        return self.accession_dict[uniq_id]

    def acc_formatter(self, accession):
        IDs = {}
        for k in self.default_ID_items:
            if self.default_ID_items[k] is str:
                IDs[k] = str(accession.IDs[k]) if k in accession.IDs else None
            elif self.default_ID_items[k] is list:
                if k in accession.IDs:
                    if isinstance(accession.IDs[k], list):
                        IDs[k] = accession.IDs[k]
                    else:
                        IDs[k] = [accession.IDs[k]]
                else:
                    IDs[k] = []
            elif self.default_ID_items[k] is bool:
                IDs[k] = bool(accession.IDs[k]) if k in accession.IDs else None
            elif self.default_ID_items[k] is int:
                IDs[k] = int(accession.IDs[k]) if k in accession.IDs else None
            elif self.default_ID_items[k] is float:
                IDs[k] = float(accession.IDs[k]
                               ) if k in accession.IDs else None
            else:
                print("Error: the type of the ID item is not valid")

        passport = {}
        for k in self.default_passport_items:
            if self.default_passport_items[k] is str:
                passport[k] = str(accession.passport[k]
                                  ) if k in accession.passport else None
            elif self.default_passport_items[k] is list:
                if k in accession.passport:
                    if isinstance(accession.passport[k], list):
                        passport[k] = accession.passport[k]
                    else:
                        passport[k] = [accession.passport[k]]
                else:
                    passport[k] = []
            elif self.default_passport_items[k] is bool:
                passport[k] = bool(accession.passport[k]
                                   ) if k in accession.passport else None
            elif self.default_passport_items[k] is int:
                passport[k] = int(accession.passport[k]
                                  ) if k in accession.passport else None
            elif self.default_passport_items[k] is float:
                passport[k] = float(accession.passport[k]
                                    ) if k in accession.passport else None
            else:
                print("Error: the type of the passport item is not valid")

        phenotypic = {}
        for k in self.default_phenotypic_items:
            if self.default_phenotypic_items[k] is str:
                phenotypic[k] = str(accession.phenotypic[k]
                                    ) if k in accession.phenotypic else None
            elif self.default_phenotypic_items[k] is list:
                if k in accession.phenotypic:
                    if isinstance(accession.phenotypic[k], list):
                        phenotypic[k] = accession.phenotypic[k]
                    else:
                        phenotypic[k] = [accession.phenotypic[k]]
                else:
                    phenotypic[k] = []
            elif self.default_phenotypic_items[k] is bool:
                phenotypic[k] = bool(accession.phenotypic[k]
                                     ) if k in accession.phenotypic else None
            elif self.default_phenotypic_items[k] is int:
                phenotypic[k] = int(accession.phenotypic[k]
                                    ) if k in accession.phenotypic else None
            elif self.default_phenotypic_items[k] is float:
                phenotypic[k] = float(
                    accession.phenotypic[k]) if k in accession.phenotypic else None
            else:
                print("Error: the type of the phenotypic item is not valid")

        dataset = {}
        for k in self.default_dataset_items:
            if self.default_dataset_items[k] is str:
                dataset[k] = str(accession.dataset[k]
                                 ) if k in accession.dataset else None
            elif self.default_dataset_items[k] is list:
                if k in accession.dataset:
                    if isinstance(accession.dataset[k], list):
                        dataset[k] = accession.dataset[k]
                    else:
                        dataset[k] = [accession.dataset[k]]
                else:
                    dataset[k] = []
            elif self.default_dataset_items[k] is bool:
                dataset[k] = bool(accession.dataset[k]
                                  ) if k in accession.dataset else None
            elif self.default_dataset_items[k] is int:
                dataset[k] = int(accession.dataset[k]
                                 ) if k in accession.dataset else None
            elif self.default_dataset_items[k] is float:
                dataset[k] = float(accession.dataset[k]
                                   ) if k in accession.dataset else None
            else:
                print("Error: the type of the dataset item is not valid")

        properties = {}
        for k in self.default_properties_items:
            if self.default_properties_items[k] is str:
                properties[k] = str(accession.properties[k]
                                    ) if k in accession.properties else None
            elif self.default_properties_items[k] is list:
                if k in accession.properties:
                    if isinstance(accession.properties[k], list):
                        properties[k] = accession.properties[k]
                    else:
                        properties[k] = [accession.properties[k]]
                else:
                    properties[k] = []
            elif self.default_properties_items[k] is bool:
                properties[k] = bool(accession.properties[k]
                                     ) if k in accession.properties else None
            elif self.default_properties_items[k] is int:
                properties[k] = int(accession.properties[k]
                                    ) if k in accession.properties else None
            elif self.default_properties_items[k] is float:
                properties[k] = float(
                    accession.properties[k]) if k in accession.properties else None
            else:
                print("Error: the type of the properties item is not valid")

        return Accession(
            accession.uniq_id,
            lat=accession.lat,
            lon=accession.lon,
            alt=accession.alt,
            sources=accession.sources,
            IDs=IDs,
            passport=passport,
            phenotypic=phenotypic,
            dataset=dataset,
            properties=properties
        )

    def build_index(self):
        IDs2uniq_id = {}
        for id_type in self.default_ID_items:
            IDs2uniq_id[id_type] = {}
            for uniq_id in self.accession_dict:
                if self.default_ID_items[id_type] is list:
                    for id_tmp in self.accession_dict[uniq_id].IDs[id_type]:
                        if id_tmp in IDs2uniq_id[id_type]:
                            print("Warning: %s is duplicated" % id_tmp)
                        IDs2uniq_id[id_type][id_tmp] = uniq_id
                else:
                    id_tmp = self.accession_dict[uniq_id].IDs[id_type]
                    if id_tmp in IDs2uniq_id[id_type]:
                        print("Warning: %s is duplicated" % id_tmp)
                    IDs2uniq_id[id_type][id_tmp] = uniq_id

        self.index = IDs2uniq_id

    def search(self, q_id, id_type=None):
        if q_id is None:
            return None

        id_type_list = [id_type] if id_type else list(
            self.default_ID_items.keys())
        uniq_id = None

        for id_type in id_type_list:
            if q_id in self.index[id_type]:
                uniq_id = self.index[id_type][q_id]
                break

        return uniq_id

    def search_by_id_list(self, id_list):
        uniq_id_dict = {q_id: self.search(q_id)
                        for q_id in id_list if self.search(q_id)}
        return uniq_id_dict

    def __str__(self):
        return """
----------------
Accession Set: %s
Date: %s
Accession Number: %d
Georeferenced Accession Number: %d
----------------
""" % (
            self.name,
            self.date,
            len(self.accession_dict),
            len([i for i in self.accession_dict if self.accession_dict[i].coordinate])
        )


if __name__ == "__main__":
    # test the sample class
    acc1 = Accession('xyx1', lat=1.0, lon=2.0, alt=3.0,
                     lib_id='lib1', pi_id='pi1')
    print(vars(acc1))

    acc2 = Accession('xyx2', lat=1.0, lon=2.0, lib_id='lib2', pi_id_list=[
        'pi2', 'pi3'], is_id_list=['is2', 'is3'])
    print(vars(acc2))

    acc3 = Accession('xyx3', is_id='is3', lib_id='lib3', pi_id='pi3')
    print(vars(acc3))

    AS = AccessionSet('test', '2020-01-01',
                      default_ID_items={'lib_id': str, 'pi_id': list, 'is_id': list})
    AS.add(acc1)
    AS.add(acc2)
    AS.add(acc3)

    AS.build_index()

    for i in AS.accession_dict:
        print(vars(AS.accession_dict[i]))

    uniq_id = AS.search('lib1', 'lib_id')
    acc = AS.accession_dict[uniq_id]

    print(vars(acc))
