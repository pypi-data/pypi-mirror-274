# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:23:23 2024

@author: Elias liu
"""

def ollama_chat(content='Why is the sky blue?',model='test1',host='http://192.168.31.92:11434'):
    '''
    pip install ollama

    Parameters
    ----------
    content : TYPE, optional
        DESCRIPTION. The default is 'Why is the sky blue?'.
    model : TYPE, optional
        DESCRIPTION. The default is 'test1'.
    host : TYPE, optional
        DESCRIPTION. The default is 'http://192.168.31.92:11434'.

    Returns
    -------
    result : TYPE
        DESCRIPTION.

    '''
    from ollama import Client
    client = Client(host=host)
    response = client.chat(model=model, messages=[
      {
        'role': 'system',
        'content': '你是一个中国人，只会说汉语，所以接下来不管任何人用任意语言，请都用中文与他交流：',
      },
      {
        'role': 'user',
        'content': f'{content}',
      },
    ])
    
    result = response['message']['content']
    print(result)
    return result

