import sys
import numpy as np

class SPEFile():
    """extract image from princeton instrument .SPE file"""

    def __init__(self, fname):
        """fname: file name of the SPE file"""
        self._fid = open(fname, 'rb')
        self._xdim = np.int64(self._read(42, 1, np.int16)[0])
        self._ydim = np.int64(self._read(656, 1, np.int16)[0])
        self._readImg()
        self._fid.close()

    def getSize(self):
        """get the x and y dimension of the image"""
        return (self._xdim, self._ydim)

    def _readImg(self):
        img = self._read(4100, self._xdim * self._ydim, np.uint16)
        img = img.reshape((self._ydim, self._xdim))
        self._img = img[700:200:-1]

    def _read(self, pos, size, ntype):
        """read from a specific posion in file"""
        self._fid.seek(pos)
        return np.fromfile(self._fid, ntype, size)

    def getImage(self):
        return self._img

if __name__ == '__main__':
    spe = SPEFile(sys.argv[-1])
    print(spe.getSize())
