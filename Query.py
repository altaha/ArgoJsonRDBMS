import time
import logging
__author__ = 'Gary'


logging.basicConfig(level=logging.INFO, format='%(asctime)s -> %(message)s')
log = logging.getLogger(__name__)

class Query(object):
    def __init__(self, tag):
        self.tag = tag
        self.arguments = []

    def prepare(self):
        pass

    def execute(self, object_count=None):
        self.prepare()
        start = time.time()
        results = self.db_command()
        count = 0
        if results:
            for item in results:
                count += 1
        end = time.time()
        log.info(self.tag + " took " + "%.2f" % (end - start) + " seconds. Returned " + str(count) + " records.")
        try:
            results.close()
        except:
            pass
        else:
            print("Managed to close connection.")
        return "%.2f" % (end - start)

    def db_command(self):
        raise NotImplementedError("You need to implement this!")
