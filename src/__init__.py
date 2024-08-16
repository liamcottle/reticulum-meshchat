import sys

# NOTE: this class is required to be able to use print/log commands and have them flush to stdout and stderr immediately
# without wrapper stdout and stderr, when using `childProcess.stdout.on('data', ...)` in NodeJS script, we never get
# any events fired until the process exits. However, force flushing the streams does fire the callbacks in NodeJS.


# this class forces stream writes to be flushed immediately
class ImmediateFlushingStreamWrapper:

    def __init__(self, stream):
        self.stream = stream

    # force write to flush immediately
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    # force writelines to flush immediately
    def writelines(self, lines):
        self.stream.writelines(lines)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


# wrap stdout and stderr with our custom wrapper
sys.stdout = ImmediateFlushingStreamWrapper(sys.stdout)
sys.stderr = ImmediateFlushingStreamWrapper(sys.stderr)
