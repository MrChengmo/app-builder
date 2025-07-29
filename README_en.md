<div align="center">

# AppBuilder-SDK

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.8+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)

The AppBuilder SDK provides developers with a one-stop development tool for AI-native applications, including basic cloud resources, an AI capability engine, the Qianfan large model, and related capability components, to improve the development efficiency of AI-native applications.

</div>
<div align="center">
<h1>AppBuilder-SDK WeChat Communication Group</h1>
<img src='docs/image/wechat_group.png' alt='wechat' width='200' >

</div>

## News
* **[Quickly create RAG, Agent, GBI and other applications in the cloud](https://console.bce.baidu.com/ai_apaas/app)**
* **[Official Component List](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz#%E5%BC%80%E5%8F%91%E7%BB%84%E4%BB%B6)**
* **2023.12.19 v0.1.0 version released**: [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.1.0)
  * Initial version release, basic cloud components support including BES; AI capability engine speech, vision class 10 capabilities, large model related RAG, text generation capabilities 19.
* **2024.01.03 v0.2.0 version released** [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.2.0)
  * Core upgrade point GBI related components added, v0.1.0 legacy issues fixed
* **2024.01.26 v0.3.0 version released** [Release Notes](https://github.com/baidubce/app-builder/releases/tag/0.3.0)
  * New component: Added Baidu search rag component (RAGwithBaiduSearch). [Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/rag_with_baidusearch.ipynb)
  * Model list acquisition: Opened up with the Qianfan large model platform model name, can dynamically obtain the current account model name, and use it in the component [Get model list](https://github.com/baidubce/app-builder/blob/master/README.md#%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8)
  * You can develop and run instance code through the official image [Secondary Development](https://github.com/baidubce/app-builder/blob/master/README.md#%E4%BA%8C%E6%AC%A1%E5%BC%80%E5%8F%91)
* **2024.02.27 v0.4.0 version released** [Release Note](https://github.com/baidubce/app-builder/releases/tag/0.4.0)
  * AppBuilder Console SDK released [Knowledge Base Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/console_dataset.ipynb), [RAG Call Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/console_rag.ipynb)
  * Large model component added: Excel2Figure (draw charts based on Excel information)
  * AI capability engine components added & updated: plant recognition, animal recognition, table text recognition V2, handwritten text recognition, QR code recognition, ID card mixed recognition, document correction recognition, image content understanding, streaming TTS
  * AgentRuntime: Added [Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/agent_runtime.ipynb)
* **2024.03.13 v0.4.1 version released** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.4.1)
  * Support FunctionCall calls for the following functions: animal and plant recognition, table text recognition, barcode and QR code recognition, ID card mixed recognition, handwritten text recognition, text2image, excel2figure
* **2024.03.20 v0.5.0 version released** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.5.0)
  * AgentBuilder ConsoleSDK released [Agent Call CookBook](https://github.com/baidubce/app-builder/blob/0.5.0/cookbooks/agent_builder.ipynb)
  * AI capability engine component added: Vector Search-VDB
  * Support FunctionCall calls for the following functions and add [CookBook](https://github.com/baidubce/app-builder/blob/master/cookbooks/general_ocr.ipynb): Text Translation-General Edition, General Object and Scene Recognition-Advanced Edition, General Text Recognition-High-precision Edition, Short Speech Recognition-Extreme Edition
* **2024.03.21 v0.5.1 version released** [ReleaseNote](https://github.com/baidubce/app-builder/releases/tag/0.5.1)
  * Bug fix: Fixed the problem that AgentBuilder ConsoleSDK could not be used in Python 3.8 and below environments. At the same time, in the upcoming version 0.6.0, support for Python 3.8 and below environments will no longer be provided. Please upgrade Python to version 3.9
## Tutorials and Documentation

* **Prerequisites**
  * [Authentication](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6)
  * [Enable component permissions](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#2%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1)
* **API Documentation**
  * [API Docs](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz)


## Quick Installation

Execute the following command to quickly install the latest version of the AppBuilder-SDK for Python (requires Python >= 3.8).

```shell
pip install --upgrade appbuilder-sdk
```
If you cannot run the appbuilder-sdk package locally, you can also use our official image to install and run it. For details, please refer to the **Secondary Development** section.

## Quick Start

Before using the AppBuilder SDK, please apply for and set the authentication parameters first. For details, please refer to [Authentication](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6).

``` python
# Set the TOKEN in the environment, the following example is omitted
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

## Model List

AppBuilder provides a function to get the list of Qianfan models. Before running a specific component, you can get the list of models available under the current account. The code is as follows:
``` python
import appbuilder
import os

os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
models = appbuilder.get_model_list(api_type_filter=["chat"], is_available=True)
print(", ".join(models))
```

Fill in your own Token to get the model list output as follows:
``` shell
ERNIE-Bot 4.0, ERNIE-Bot-8K, ERNIE-Bot, ERNIE-Bot-turbo, EB-turbo-AppBuilder-specific version, Qianfan-Chinese-Llama-2-7B, Yi-34B-Chat, Llama-2-7B-Chat, Llama-2-13B-Chat, Llama-2-70B-Chat, ChatGLM2-6B-32K, ChatLaw, BLOOMZ-7B, Qianfan-BLOOMZ-7B-compressed, AquilaChat-7B
```

To make it easier for users to use the models, here are some short names for the models
| Qianfan Model Name | AppBuilder-SDK Short Name |
|----------------------------|------------------|
| ERNIE-Bot 4.0 | eb-4 |
| ERNIE-Bot-8K | eb-8k |
| ERNIE-Bot | eb |
| ERNIE-Bot-turbo | eb-turbo |
| EB-turbo-AppBuilder-specific version | ernie_speed_appbuilder |
| ERNIE Speed-AppBuilder | ernie_speed_appbuilder |


### Typical Examples

AppBuilder includes various paradigms for building AI-native applications based on large models, including text generation based on Prompt templates, retrieval-augmented generation, and text generation using external tools.

#### Playground
```python
import appbuilder

# Playground component
template_str = "You are playing the role of {role}, please answer my question.\n\nQuestion: {question}.\n\nAnswer:"
playground = appbuilder.Playground(prompt_template=template_str, model="ERNIE Speed-AppBuilder")

# Define input and call the playground component
input = appbuilder.Message({"role": "Java engineer", "question": "What is the memory recycling mechanism of the Java language?"})
print(playground(input, stream=False, temperature=1e-10))

```

#### Text Completion
```python
import appbuilder

# Similar question generation component
similar_q = appbuilder.SimilarQuestion(model="ERNIE Speed-AppBuilder")

# Define input and call similar question generation
input = appbuilder.Message("I want to eat ice cream, where can I find delicious ice cream?")
print(similar_q(input))

```

#### Chat RAG
```python
import appbuilder
import os

# The APPBUILDER_TOKEN here is a trial account with limited QPS. Please replace it with your own account Token when testing your own application.
os.environ["APPBUILDER_TOKEN"] = ""

# Fill in the online RAG application ID here, which can be viewed on the [AppBuilder web-side-my application interface]
# Web link https://console.bce.baidu.com/ai_apaas/app
app_id = ""
rag_app = appbuilder.console.RAG(app_id)
query = "Where is the capital of China?"
answer = rag_app.run(appbuilder.Message(query)) # New conversation
print(answer.content)
```

## Application Servitization

The AppBuilder-SDK provides servitization capabilities for components. By defining an Agent, developers can quickly start Chainlit, Flask and other servitized demos or APIs to provide a fast experience environment.

In the environment where services need to be deployed, developers need to manually install the Chainlit library first

```shell
pip install chainlit
```
Then, use the Agent servitization function of AppBuilder to quickly deploy the service

```python
import appbuilder

# Playground component
playground = appbuilder.Playground(
    prompt_template="{query}",
    model="ERNIE Speed-AppBuilder"
)

# Use AgentRuntime to servitize the playground component
agent = appbuilder.AgentRuntime(component=playground)

# Start the chainlit demo, which will automatically open the experience dialog page in the browser
agent.chainlit_demo(port=8091)
```

## Secondary Development
Currently, it provides open data structures for developers, including Message and Component, to facilitate developers to integrate their existing large model applications. This part is still under construction.
Secondary development can use the official development image to facilitate the rapid installation of various dependent libraries.
``` shell
docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.1.0
```

### Message
- A unified data structure for building large model applications, built on Pydantic, and flowing between different Components. The default field of the Message base class is content, and the type is Any.
```python
from appbuilder import Message
input_dict = Message({"query": "How to make braised pork"})
input_list = Message(["text1", "text2", "text3"])
input_str = Message("How to make braised pork")
```

### Component
- The standard structure of all capability units, with the Message structure as input and output. The internal execution logic can be executed locally or call cloud services. The following is an implementation example of an official component.
```python
class SimilarQuestionMeta(ComponentArguments):
    """ SimilarQuestionMeta
    """
    message: Message = Field(...,
                             variable_name="query",
                             description="Input message, used as input for the model, usually a question.")


class SimilarQuestion(CompletionBaseComponent):
    """ Based on the input question, mine similar questions related to the question. Widely used in customer service, question and answer and other scenarios.
    Examples:

        .. code-block:: python
            import os
            import appbuilder

            os.environ["APPBUILDER_TOKEN"] = "..."

            qa_mining = appbuilder.SimilarQuestion(model="ERNIE Speed-AppBuilder")

            msg = "I want to eat ice cream, where can I find delicious ice cream?"
            msg = appbuilder.Message(msg)
            answer = qa_mining(msg)

            print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    def __init__(self, model=None):
        """Initializes the SimilarQuestionMeta task.

        Args:
            model (str|None): Model name, used to specify the Qianfan model to be used.

        Returns:
            None

        """
        super().__init__(SimilarQuestionMeta, model=model)

    def run(self, message, stream=False, temperature=1e-10):
        """
        Given the input (message) to the model to run, specify the running parameters, and return the result.

        Args:
            message (obj:`Message`): Input message, used as the main input content of the model. This is a required parameter.
            stream (bool, optional): Specifies whether to return the response in a streaming format. Defaults to False.
            temperature (float, optional): The temperature parameter of the model configuration, used to adjust the generation probability of the model. The value range is 0.0 to 1.0, where a lower value makes the generation more deterministic, and a higher value makes the generation more diverse. The default value is 1e-10.

        Returns:
            obj:`Message`: The output message after the model runs.
        """
        return super().run(message=message, stream=stream, temperature=temperature)
```

## License

The AppBuilder-SDK follows the Apache-2.0 open source license.
