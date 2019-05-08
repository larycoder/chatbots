# Chatbots
This is part of AI project try to deplay [tensor2tensor](https://github.com/tensorflow/tensor2tensor) on insert punctuations for text. To build simple environment for deploy t2t model on reality, the telegram chatbot was design as the easiest solution.

I following [this](https://chatbotslife.com/your-first-chatbot-using-telegram-and-python-part-1-796894016ba8) reference as a guider for first time working with telegram chatBot

## Philosophy of design
Simplest code as mush as possible and portable.

## Quick start 
You can easy build simple program (**chatBot**) to take and send text with Telegram server through [Telgegram API](https://core.telegram.org/) and python. Then you can build model t2t to handle text retrieve by Bot.

All of bot build tutorial I was mention [in here](https://github.com/larycoder/chatbots/blob/master/README.md)

## Update translator for faster translate by keeping model onlive during time bot run
If you already build your simple translate bot depend on my previous guilder. You will be easily relize that time for bot respond translate mess is supper slow

**Reason** is

that t2t using estimator as model decoder, which indeep will reload data, model, grap, ..etc each time you call t2t_decoder. For some mastery reason, they who build-in estimator never create some more covinient version which try to keep model loading one time and run for each times decode. 

**How can I solve this problem ?**

I look a bit on decoder code of t2t, exspecially on interactive mode which can keep model loading one times and waiting for user typing. Then I try to cheat interactive code with very useful function of python **yield**. It work but using terrible machenism. After that, I try to wrap whose machenism on class then I can call instant which will more scabability and extensibility. Funtualy, I found a interesting guy who working for google has same idea as me and successfully builded up 1 wrapper. And I said "Woalla, I can depending on this guy idea for wrapping my mechanism to class". For long hours, I finished it.

Now, I will not describe detail about my code (too **complicate** and lazy for me) then I will show you how to **apply** it: 

First, class name is model_decoder in [this file](https://github.com/larycoder/chatbots/blob/decode_Server/decode_server.py), in here, you must modify prefix paramet (right on the head of file) before using it for sure.

Then you can call instant out on any program you want. Whenever you create instant of model_decoder, model of translator will be loaded and keep for living, then there are 2 function for working with this living model:

**getMessage(string)**: send message to model and it will return translated string for you

**closeModel()**: will kill living model right after you dont want to using it anymore

**OK** that all, what do you want to do with it is depend on you. But for me, I wrap it into my chatbot, you can clone it down then run.

For the process to run it, you may want to read again my [previous version](https://github.com/larycoder/chatbots/blob/master/README.md) but dont need to modify any file, just need to push data for decoder as mention an token of chatBot on right file then run.

This is only a part of more huge project and final purpose of project is can insert punctuation to text. So we try to modify translator model of t2t to reach our target. If you have some interesting in it, feel free to see more in [here](https://github.com/linhhonblade/try-tensor2tensor/tree/master/custom_data)...





### update at 2019-05-9
