import requests, zipfile, os, json, random, time, datetime
import urllib3
urllib3.disable_warnings()

# 获取token信息
def prove_token(token):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-type": "application/json",
        "Referer": "https://api.novelai.net/",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
    }
    headers['Authorization'] = 'Bearer ' + token

    for i in range(2):
        try:
            response = requests.get('https://api.goutou.cc/user/data', headers=headers, verify=False)
            data = response.json()

            if 'statusCode' in data:
                return False, 'Token无效'
            

            end_date = datetime.datetime.fromtimestamp(int(data['subscription']['expiresAt'])).strftime('%Y-%m-%d %H:%M')
            value = data['subscription']['trainingStepsLeft']['fixedTrainingStepsLeft']
            

            return end_date, value
        except Exception as e:
            pass

    return False, '请求失败'

# 提交任务
def poster(data,apikey,downpath='back/imgs'):
    
    url = "https://dai.iisbo.com/ai/generate-image"
    headers = {
        "Authorization": "Bearer " + apikey,
        "Content-type": "application/json",
        "Referer": "https://novelai.net/",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36",
    }

    response = requests.post(url, json=data, headers=headers)

    # 判断是否生成成功
    try:
        # 如果是json数据，则生成失败，返回错误信息
        class res:
            def __init__(self, status, data):
                self.status = status
                self.data = data
        response = res(response.status_code, response.json())
        return response
    except:
        # 否则为图片信息
        pass

    # 下载zip到本地 以时间戳加随机数字作为文件名
    filename = str(time.time()) + str(random.randint(1000,9999))

    with open(f'{downpath}/{filename}.zip', 'wb') as f:
        f.write(response.content)
        
    # 解压zip文件
    with zipfile.ZipFile(f'{downpath}/{filename}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{downpath}/{filename}')

    # 删除zip文件
    os.remove(f'{downpath}/{filename}.zip')

    # 复制图片到{downpath}文件夹
    os.rename(f'{downpath}/{filename}/image_0.png', f'{downpath}/{filename}.png')
    
    # 删除文件夹
    os.rmdir(f'{downpath}/{filename}')
    
    # 返回图片路径
    ipath = f'{downpath}/{filename}.png'
    class res:
        def __init__(self, status, data):
            self.status = status
            self.data = data
    response = res('success',ipath)
    return response

# 文生图
def txt2img(apikey,downpath,prompt='',nprompt='',size='512x512',steps=28,seed=-1):
    if int(seed) == -1:
        seed = random.randint(0,21474836)
    data = {
        "input":prompt,
        "model":"nai-diffusion-3",
        "action":"generate",
        "parameters":{
            "params_version":1,
            "width":int(size.split('x')[0]),
            "height":int(size.split('x')[1]),
            "scale":5,
            "sampler":"k_euler",
            "steps": int(steps),
            "seed": int(seed),
            "n_samples":1,
            "ucPreset":0,
            "qualityToggle":True,
            "sm":False,
            "sm_dyn":False,
            "dynamic_thresholding":False,
            "controlnet_strength":1,
            "legacy":False,
            "add_original_image":False,
            "uncond_scale":1,
            "cfg_rescale":0,
            "noise_schedule":"native",
            "legacy_v3_extend":False,
            "negative_prompt":nprompt,
            "noise":0,
        }
    }
    return poster(data,apikey,downpath)
# 图生图
def img2img(apikey,downpath,image,prompt='',strength=0.7,nprompt='',size='512x512',steps=28,seed=-1):
    if int(seed) == -1:
        seed = random.randint(0,21474836)
    data = {
        "input":prompt,
        "model": "nai-diffusion-3",
        "action": "img2img",
        "parameters": {
            "image": image,
            "params_version": 1,
             "width":int(size.split('x')[0]),
            "height":int(size.split('x')[1]),
            "scale":5,
            "sampler":"k_euler",
            "steps": int(steps),
            "seed": int(seed),
            "n_samples": 1,
            "strength": strength,
            "noise": 0,
            "ucPreset": 0,
            "qualityToggle": True,
            "sm": False,
            "sm_dyn": False,
            "dynamic_thresholding": False,
            "controlnet_strength": 1,
            "legacy": False,
            "add_original_image": True,
            "uncond_scale": 1,
            "cfg_rescale": 0,
            "noise_schedule": "native",
            "legacy_v3_extend": False,
            "negative_prompt": nprompt,
            "reference_image_multiple": [],
            "reference_information_extracted_multiple": [],
            "reference_strength_multiple": []
        }
    }
    return poster(data,apikey,downpath)