class Storage:
    def __init__(self):
        self._data = {}

    def save(self, namespace, key, value):
        if namespace not in self._data:
            self._data[namespace] = {}
        self._data[namespace][key] = value

    def find(self, namespace, key):
        return self._data[namespace][key]

    def find_all(self, namespace):
        return list(self._data.get(namespace, {}).values())
