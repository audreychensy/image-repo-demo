## id -> path
## e.g. aaaa0001 -> 0000/0000/aaaa/00000000aaaa0001
def generateImagePath(id):
    assert(len(id) <= 16)
    ## format id to have leading zeros and is 16 digits long
    padded_id = str(id).zfill(16)[:-4]
    ## split id string to 3 blocks where each block denotes a directory level
    dirs = [padded_id[i:i+4] for i in range(0, len(padded_id), 4)]
    path = '/'.join(dirs) + '/' + id
    return path

print(generateImagePath("aaaa0001"))

