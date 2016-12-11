import tempfile
import subprocess
import os
import yaml


class FileService(object):
    METAPATH_KEY = "_metapath"

    def edit_temp_file(self, initial_text):
        """Edits a temp file in a subprocess"""
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tfile:
            tfile.write(initial_text)
            tfile.flush()
            print("Starting vim process")
            subprocess.call(["vim", '+set backupcopy=yes', tfile.name])
            print("vim process ended")
            tfile.seek(0)
            ret_bytes = tfile.read().rstrip()
            import codecs
            ret = codecs.decode(ret_bytes, "UTF-8")
            return ret

    def read_line(self, path, line_no):
        current_line = 0
        with open(path, "r") as fs:
            for line in fs:
                current_line += 1
                if current_line == line_no:
                    return line.strip()
        return None

    def get_metapath(self, path):
        metafile_ext = ".yaml"
        directory, fname = os.path.split(path)
        fname_no_ext, ext = os.path.splitext(fname)
        if ext == metafile_ext:
            raise FileServiceException("Can't get a metafile for files using the {} extension"
                                       .format(metafile_ext))
        return os.path.join(directory, fname_no_ext + metafile_ext)

    def get_metafile(self, path):
        """Returns the metafile for this file, or a new one"""
        metapath = self.get_metapath(path)
        try:
            with open(metapath) as fs:
                metafile = yaml.load(fs)
        except FileNotFoundError:
            metafile = {"path": path, "lines": dict()}

        # Add a path to the object, which should not be serialized
        metafile[self.METAPATH_KEY] = metapath
        return metafile

    def save_metafile(self, metafile):
        metapath = metafile[self.METAPATH_KEY]
        with open(metapath, "w") as fs:
            # HACK:
            del metafile[self.METAPATH_KEY]
            yaml.dump(metafile, fs, default_flow_style=False)
            metafile[self.METAPATH_KEY] = metapath



class FileServiceException(Exception):
    """Generic exception involving the file service"""
    pass
