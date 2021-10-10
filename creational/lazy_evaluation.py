class Record:
    def __init__(self, row_id):
        self.row_id = row_id


class Table:
    lookup_table = {}

    @classmethod
    def get_record(cls, row_id: int) -> Record:
        """
        if row_id not in cls.lookup_table,
        instantiate Record object on the fly.
        """
        if row_id not in cls.lookup_table.keys():
            # There must be more args.
            cls.lookup_table[row_id] = Record(row_id)
        return cls.lookup_table[row_id]


if __name__ == '__main__':
    Table.get_record(1)
