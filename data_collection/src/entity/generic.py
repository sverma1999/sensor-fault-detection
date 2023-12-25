import pandas as pd
import json


class Generic:
    def __init__(self, record: dict):
        # This loop will create the attributes of the class dynamically from the dictionary "record"
        for k, v in record.items():
            setattr(self, k, v)

    # This method is used to convert the dictionary to object
    @staticmethod
    def dict_to_object(data: dict, ctx):
        print(data, ctx)
        return Generic(record=data)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_object(cls, file_path):
        """
        This function generates JSON records as an object from the csv file
        Args:
            file_path (_str_): File path of the csv file

        Yields:
            generic: Generic object
        """
        # First we will read the csv file in chunks of 10 rows
        chunk_df = pd.read_csv(file_path, chunksize=10)
        n_row = 0

        # Now we will iterate over the chunks of 10 rows and then iterate over the rows of the chunk
        for df in chunk_df:
            # Iterates over each row within the current chunk, where data represents a single row of data as an array.
            for data in df.values:
                # Constructs a Generic object by converting the row data into a dictionary where
                # the keys are the column names and the values are the corresponding row values.
                generic = Generic(dict(zip(df.columns, list(map(str, data)))))
                # cars.append(car)
                # print(n_row)
                n_row += 1
                # Allowing the caller of this function to receive and process the Generic objects one at a time.
                yield generic

    @classmethod
    def export_schema_to_create_confluent_schema(cls, file_path):
        columns = next(pd.read_csv(file_path, chunksize=10)).columns

        schema = dict()
        schema.update(
            {
                "type": "record",
                "namespace": "com.mycorp.mynamespace",
                "name": "sampleRecord",
                "doc": "Sample schema to help you get started.",
            }
        )

        fields = []
        for column in columns:
            fields.append(
                {"name": f"{column}", "type": "string", "doc": "The string type."}
            )

        schema.update({"fields": fields})

        json.dump(schema, open("schema.json", "w"))
        schema = json.dumps(schema)

        print(schema)
        return schema

    @classmethod
    def get_schema_to_produce_consume_data(cls, file_path):
        """
        This function is used to generate schema for data to be produced and consumed by kafka
        Args:
            file_path (_str_): File path of the csv file

        Returns:
            _str_: schema of the data to be produced and consumed by kafka
        """
        # We can read the 10 rows of the csv file to get the column names, we dont need
        # to read the whole file to get the column names.
        columns = next(pd.read_csv(file_path, chunksize=10)).columns

        # initialize the schema dictionary
        schema = dict()
        # update the schema dictionary with the required fields. These feilds are defined by
        # confluent schema registry
        schema.update(
            {
                "$id": "http://example.com/myURI.schema.json",
                "$schema": "http://json-schema.org/draft-07/schema#",
                "additionalProperties": False,
                "description": "Sample schema to help you get started.",
                "properties": dict(),
                "title": "SampleRecord",
                "type": "object",
            }
        )
        for column in columns:
            schema["properties"].update(
                {f"{column}": {"description": f"generic {column} ", "type": "string"}}
            )

        schema = json.dumps(schema)

        print(schema)
        return schema

    def __str__(self):
        return f"{self.__dict__}"


def instance_to_dict(instance: Generic, ctx):
    return instance.to_dict()
