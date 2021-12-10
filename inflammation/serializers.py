from inflammation import models
import json
from abc import ABC, abstractmethod


class Serializer(ABC):
    @classmethod
    @abstractmethod
    def serialize(cls, instances):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def save(cls, instances, path):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def deserialize(cls, data):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load(cls, path):
        raise NotImplementedError


class PatientSerializer(Serializer):
    model = models.Patient

    @classmethod
    def serialize(cls, instances):
        return [{
            'name': instance.name,
            'observations': ObservationSerializer.serialize(instance.observations),
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        instances = []

        for item in data:
            item['observations'] = ObservationSerializer.deserialize(
                item.pop('observations'))
            instances.append(cls.model(**item))

        return instances

    @classmethod
    def save(cls, instances, path):
        raise NotImplementedError

    @classmethod
    def load(cls, path):
        raise NotImplementedError


class PatientJSONSerializer(PatientSerializer):
    @classmethod
    def save(cls, instances, path):
        with open(path, 'w') as jsonfile:
            json.dump(cls.serialize(instances), jsonfile)

    @classmethod
    def load(cls, path):
        with open(path) as jsonfile:
            data = json.load(jsonfile)

        return cls.deserialize(data)


class ObservationSerializer(Serializer):
    model = models.Observation

    @classmethod
    def serialize(cls, instances):
        return [{
            'day': instance.day,
            'value': instance.value,
        } for instance in instances]

    @classmethod
    def deserialize(cls, data):
        return [cls.model(**d) for d in data]
