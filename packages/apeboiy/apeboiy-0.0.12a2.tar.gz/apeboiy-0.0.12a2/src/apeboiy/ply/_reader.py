import os
import struct

import numpy as np


class Reader:
    """
    Class to read PLY files. The class can read in ASCII 1.0 and little-endian binary 1.0 files.

    usage:
    reader = PLYReader("file.ply")
    reader.read() # read the file

    # get the vertices
    vertices = reader.vertices
    """
    def __init__(self, filename):

        # check if file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found.")
        self.__name = filename
        self.__header = "ply\n"
        self.__vertex_count = 0
        self.__format = None
        self.__vertices = {
            "Position": np.zeros((0, 3), dtype=np.float64),  # (x, y, z
            "Color": np.zeros((0, 3), dtype=np.uint8),  # (r, g, b)
        }

    @property
    def vertices(self):
        return self.__vertices

    @property
    def vertex_count(self):
        return self.__vertex_count

    @property
    def format(self):
        return self.__format

    @property
    def name(self):
        return self.__name

    def info(self):
        print("File: ", self.__name)
        print(self.__header)

    def _parse_header(self, f):
        header = []
        while True:
            line = f.readline()
            if isinstance(line, bytes):
                line = line.decode("ascii").strip()
            else:
                line = line.strip()

            header.append(line)

            if line == "end_header":
                break
            if line.startswith("element vertex"):
                self.__vertex_count = int(line.split()[-1])
            if line.startswith("format"):
                self.__format = line.split()[1]

        self.__header = "\n".join(header)

    def _read_vertices_binary(self, f):
        vertex_format = "dddBBB"
        vertex_size = struct.calcsize(vertex_format)
        self.__vertices["Position"] = np.zeros(
            (self.__vertex_count, 3), dtype=np.float64
        )
        self.__vertices["Color"] = np.zeros((self.__vertex_count, 3), dtype=np.uint8)
        for i in range(self.__vertex_count):
            data = f.read(vertex_size)
            x, y, z, r, g, b = struct.unpack(vertex_format, data)
            self.__vertices["Position"][i] = [x, y, z]
            self.__vertices["Color"][i] = [r, g, b]

    def _read_vertices_ascii(self, f):
        self.__vertices["Position"] = np.zeros(
            (self.__vertex_count, 3), dtype=np.float64
        )
        self.__vertices["Color"] = np.zeros((self.__vertex_count, 3), dtype=np.uint8)
        errors = []

        for i in range(self.__vertex_count):
            line = f.readline()
            try:
                x, y, z, r, g, b = map(float, line.split())
                self.__vertices["Position"][i] = [x, y, z]
                self.__vertices["Color"][i] = [r, g, b]
            except Exception as e:
                errors.append((i, line, e))
        if errors:
            err_count = len(errors)
            if os.path.exists("error.log"):
                os.remove("error.log")
            with open("error.log", "w") as f:
                for i, line, e in errors:
                    f.write(f"Error in line {i}: {line}\n")
                    f.write(f"Message: {e}\n\n")
            print(
                f"Found {err_count} Errors while reading file. Check error.log for more information."
            )

    def read(self):
        with open(self.__name, "rb") as f:
            self._parse_header(f)
            if "ascii" in self.__format:
                self._read_vertices_ascii(f)
            else:
                self._read_vertices_binary(f)
