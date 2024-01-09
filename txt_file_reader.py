class TxtFileReader:
    def read(file_name) -> list[str]:
        with open(file_name) as file:
            return [line.strip('\n') for line in file.readlines()]
