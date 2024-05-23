import w
import os
#  whisper-faster
# whisper_result = w.whisper_faster(file_path='test.mp4', model='tiny', srt=True)


# whisper-faster-local
# whisper_result = w.whisper_faster(file_path='test.mp4',
#                                     model='tiny',
#                                     srt=True)
# openai_whisper
# result = w.whisper_openai('test.mp4', 'sk-xxx')

# translate
# translate_result = w.translate(result=whisper_result,
#                                  api_key='sk-9f8e218e61664eabafdb2bbb8fb0cf79',
#                                  model='deepseek-chat',
#                                  srt=True)

# merge
# w.merge('test.mp4', 'translated_output.srt', subtitle_model='软字幕')

# blog
answer = w.blog('test.mp4', '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', 'http://47.236.123.254:8099/v1', whisper_model="faster")
print(answer)
