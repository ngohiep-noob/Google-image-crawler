import faiss


def create_index(shape, metrics):
    if metrics == "L2":
        index = faiss.IndexFlatL2(shape)
    elif metrics == "IP":
        index = faiss.IndexFlatIP(shape)
    else:
        raise ValueError("metrics must be either L2 or IP")
    return index


def write_index(index, index_path):
    faiss.write_index(index, index_path)


def read_index(index_path):
    index = faiss.read_index(index_path)
    return index
