from dataclasses_serialization.json import JSONSerializer


class Serializer:
    @staticmethod
    def serialize(question_response):
        return JSONSerializer.serialize(question_response)
