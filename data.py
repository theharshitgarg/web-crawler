class Data():
    def __init__(self):
        self.images = []
        self.hyperlinks = {}
        self.paragraphs = []
        self.pdfs = []

    def append_images(self, images):
        self.images = self.images + images

        return images

    def append_links(self, depth, links):

        if depth > 0:
            links = list(set(links).difference(
                set(self.hyperlinks[depth - 1])))

        try:
            links = list(set(links).difference(set(self.hyperlinks[depth])))
            self.hyperlinks[depth] = self.hyperlinks[depth] + links
        except BaseException:
            self.hyperlinks[depth] = links

        return links
