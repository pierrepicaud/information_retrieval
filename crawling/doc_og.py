from collections import Counter


class HtmlDocumentTextData:

    def __init__(self, url):
        self.doc = HtmlDocument(url)
        self.doc.get()
        self.doc.parse()

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def get_sentence(self):
        # TODO extract plain text, images and links from the document
        soup = BeautifulSoup(self.doc.content, 'html.parser')
        result = []
        body = soup.find('body')
        if body is not None:
            sentences = body.findAll(text=True)
            sentences = filter(self.tag_visible, sentences)
            for t in sentences:
                result.extend(t.split('.'))
        result = [t.strip() for t in result]
        result = filter(''.__ne__, result)
        return result

    def get_word_stats(self):
        # TODO return Counter object of the document, containing mapping {`word` -> count_in_doc}
        sentences = self.get_sentence()
        words = []
        for sentence in sentences:
            words.extend(sentence.split(' '))
        words = [word.strip().lower() for word in words]
        words = filter(''.__ne__, words)
        return Counter(words)
