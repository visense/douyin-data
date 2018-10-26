#!/usr/bin/python
# -*- coding: UTF-8 -*-

from douyin import *

# 生产-消费 流程 的消费者 _receiver
async def download_videos(_receiver, downloader):
  while True:
    async for video in _receiver:
      # video = await _receiver.receive() # may get repeated tail
      if video is None:
        return # 结束下载
      url = video['video_url']
      if downloader.is_file_downloaded(video['name']) or url is None:
        logging.info(f"{video['name']} is already downloaded or expired!")
        continue
      
      logging.debug(f"downloading {url} ... ")
      content = await downloader.download_file(url)
      if content is not None:
        await downloader.save_file(video['name'], content)
        logging.info(f"download {video['name']} from {url} succ")
      else:
        logging.error(f"download {video['name']} from {url} FAIL!")


# 生产-消费 流程 的生产者 _sender
async def generate_videos(_sender, func_dict, user, action, repeat_func):
    '''根据用户选择调用指定函数'''
    async for video in func_dict[action](user, repeat_func=repeat_func):
        await _sender.send(video)
    await _sender.send(None)


# 爬取单个用户的视频
async def crawler_user_video(user, func_dict, action, save_dir, concurrency):
  '''下载指定用户指定的'''
  logging.info(f"start download {user}'s favorite video to {save_dir} with {concurrency} concurrency ...")
  downloader = AsyncDownloader(os.path.join(save_dir, user, action))

  async with trio.open_nursery() as nursery:
    _sender, _receiver = trio.open_memory_channel(concurrency) # 并行数量
    nursery.start_soon(generate_videos, _sender, func_dict, user, action, downloader.is_file_downloaded)
    nursery.start_soon(download_videos, _receiver, downloader)

  logging.info(f"video for user with user_id={user} downloads finished!")

# 主函数
async def main(user, action, follow, save_dir, concurrency):
    dy = DouyinTool()
    func_dict = {
        "favorite" : dy.get_favorite_list,
        "post" : dy.get_post_list,
    }

    if action not in func_dict.keys():
        logging.critical(f"action={action} is not supported!")
        exit(-1)
    if not user.isdigit():
        logging.critical(f"user={user} is illegal!")
        exit(-1)

    if follow:
        user_ids = set()
        logging.info(f"Crawler {user}'s follow list...")
        async for people in dy.get_follow_list(user):
            user_ids.add(people['user_id'])
        logging.info(f"there are {len(user_ids)} followed users need for crawler, let's begin!")
        for _user in user_ids:
            await crawler_user_video(_user, func_dict, action, save_dir, concurrency)
    else:
        await crawler_user_video(user, func_dict, action, save_dir, concurrency)

    logging.info("all videos are downloaded! congratulations!!!")

save_dir = 'C:/Users/my/Documents/GitHub/douyin-hack/download'
concurrency = 20
user = '66615900141'
action = 'favorite'
follow = 'follow'
trio.run(main, user, action, follow, save_dir, concurrency)