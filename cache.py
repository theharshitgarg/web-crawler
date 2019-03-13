class Cache():
    def __init__(self):
        self.data = {
            "images": [],
            "hyper_links": [],
        }

    def append_links(self, links):
        self.data["hyper_links"].append(links)

    def append_images(self, links):
        self.data["images"].append(links)
