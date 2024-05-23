# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:23:23 2024

@author: Elias liu
"""

def ollama_chat(system_prompt = '',user_prompt='Why is the sky blue?',model='test1',host='http://192.168.31.92:11434',chinese=0):
    '''
    
    pip install ollama

    Parameters
    ----------
    system_prompt : TYPE, optional
        系统提示词. The default is ''.
    user_prompt : TYPE, optional
        用户提示词. The default is 'Why is the sky blue?'.
    model : TYPE, optional
        模型. The default is 'test1'.
    host : TYPE, optional
        服务ip. The default is 'http://192.168.31.92:11434'.
    chinese : TYPE, optional
        当chinese=1时，{
          'role': 'system',
          'content': f'你是一个中国人，只会说汉语，所以接下来不管任何人用任意语言，请都用中文与他交流。{system_prompt}',
        },. The default is 0.

    Returns
    -------
    result : TYPE
        DESCRIPTION.

    '''
    from ollama import Client
    client = Client(host=host)
    
    if chinese == 1:
        if system_prompt == None:
            system_prompt = ''
        response = client.chat(model=model, messages=[
          {
            'role': 'system',
            'content': f'你是一个中国人，只会说汉语，所以接下来不管任何人用任意语言，请都用中文与他交流。{system_prompt}',
          },
          {
            'role': 'user',
            'content': f'{user_prompt}',
          },
        ])
    
    else:
    
        if system_prompt == '' or system_prompt == None:
            response = client.chat(model=model, messages=[
              {
                'role': 'user',
                'content': f'{user_prompt}',
              },
            ])
            
            
        else:
            response = client.chat(model=model, messages=[
              {
                'role': 'system',
                'content': f'{system_prompt}',
              },
              {
                'role': 'user',
                'content': f'{user_prompt}',
              },
            ])
        

    
    
    result = response['message']['content']
    print(result)
    return result

