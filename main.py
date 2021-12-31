import re
import os

from googleapiclient.discovery import build

from video import Video

api_key = os.environ['YOUTUBE_API_KEY']

youtube = build('youtube', 'v3', developerKey=api_key)

# For video duration formatting
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')


def create_vid(v_id: str):
    video_response = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=v_id
    ).execute()

    items = video_response.get("items")[0]

    # get the snippet, statistics & content details from the video response
    snippet = items["snippet"]
    statistics = items["statistics"]
    content_details = items["contentDetails"]

    # get infos from the snippet
    title: str = snippet["title"]
    publish_year: str = snippet["publishedAt"][0:4]

    # get stats infos
    comment_count: str = statistics["commentCount"]
    like_count: str = statistics["likeCount"]
    view_count: str = statistics["viewCount"]

    # get duration from content details
    duration: str = content_details["duration"]

    hours = hours_pattern.search(duration)
    minutes = minutes_pattern.search(duration)
    seconds = seconds_pattern.search(duration)

    hours = int(hours.groups()[0]) if hours else 0
    minutes = int(minutes.groups()[0]) if minutes else 0
    seconds = int(seconds.groups()[0]) if seconds else 0

    duration_str = f"{hours}:{minutes}:{seconds}"
    video = Video(title, publish_year, duration_str, comment_count, view_count, like_count)
    return video


def main():
    nextPageToken = None
    videos_2021: list[Video] = []

    while True:

        pli_request = youtube.playlistItems().list(
            part=['contentDetails, snippet'],
            playlistId='UU8butISFwT-Wl7EV0hUK0BQ',
            maxResults=50,
            pageToken=nextPageToken,
        )

        pli_response = pli_request.execute()

        for item in pli_response['items']:
            videoID: str = item['contentDetails']['videoId']
            video = create_vid(videoID)
            if video.yearEnd():
                mostCommented = get_max_vid(videos_2021, 'commentCount')
                mostLiked = get_max_vid(videos_2021, 'likeCount')
                mostViewed = get_max_vid(videos_2021, 'viewCount')

                print(f'Freecodecamp released {len(videos_2021)} videos in 2021')
                print(f"Most commented: {mostCommented.title}, Comment Count: {mostCommented.commentCount}")
                print(f"Most liked: {mostLiked.title}, Like Count: {mostLiked.likeCount}")
                print(f"Most viewed: {mostViewed.title}, View Count: {mostViewed.viewCount}")
                return
            else:
                videos_2021.append(video)

        nextPageToken = pli_response.get('nextPageToken')
        if not nextPageToken:
            break


def get_max_vid(vid_list: list[Video], attr: str):
    vid: Video = vid_list[0]
    highest: int = 0
    for item in vid_list:
        if int(getattr(item, attr)) > highest:
            highest = int(getattr(item, attr))
            vid = item
    return vid


main()
