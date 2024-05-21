# zeval/zeval/utils/model_caller.py
import litellm
from litellm import completion
from unionllm import UnionLLM
import time

class ModelCaller:
    def __init__(self, config):
        self.config = config

    def call(self, **params):
        # 更新或合并额外参数，避免重复
        effective_params = {**params}
        start_time = time.time() # 开始计时

        try:
            self.client = UnionLLM(**params)
            response = self.client.completion(**effective_params)
        except:
            try:
                # 去掉不需要的参数provider
                effective_params.pop('provider', None)
                response = litellm.completion(**effective_params)
            except Exception as e:
                return False, str(e)
          
        end_time = time.time() # 结束计时
        elapsed_time = end_time - start_time # 计算经过的时间
        return response, elapsed_time
            
    def parse_response(self, response):
        try:
            # 从模型响应中获得最终陈述
            choices = response.choices
            final_statement = choices[0].message.content 
            return final_statement
        except Exception as e:
            return False