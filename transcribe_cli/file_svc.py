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

    def seek_line(self, fs, line_no):
        current_line = 0
        for line in fs:
            current_line += 1
            if current_line == line_no:
                break
        return current_line

    def _seek_line_force(self, path, line_no, content):
        # Reads the file up until the line number, writing new lines if necessary:
        with open(path, "r+") as fs:
            found = self.seek_line(fs, line_no)
            assert found <= line_no
            print(found, line_no)
            if found == line_no:
                pass
            elif found < line_no:
                for line in range(line_no - found - 1):
                    fs.write("\n")
                # Finally, print the new line
                fs.write("{}\n".format(content))

    def write_line(self, path, line_no, line):
        # Ensure that there are no newlines (ignoring other control chars for now):
        line_in = line.replace("\n", "<br/>")
        self._seek_line_force(path, line_no, line_in)

