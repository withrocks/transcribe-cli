import tempfile
import subprocess


class FileService(object):
    def edit_temp_file(self, initial_text):
        """Edits a temp file in a subprocess"""
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tfile:
            tfile.write(initial_text)
            tfile.flush()
            subprocess.call(["vim", '+set backupcopy=yes', tfile.name])
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


