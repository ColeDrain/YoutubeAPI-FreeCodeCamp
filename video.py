class Video:
    def __init__(self, title, publishYear, duration, commentCount, viewCount, likeCount):
        self.title = title
        self.publishYear = publishYear
        self.duration = duration
        self.commentCount = commentCount
        self.viewCount = viewCount
        self.likeCount = likeCount

    def yearEnd(self):
        return self.publishYear != '2021'
