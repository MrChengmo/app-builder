<div align="center">

# AppBuilder-SDK

[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)
![Supported Python versions](https://img.shields.io/badge/python-3.8+-orange.svg)
![Supported OSs](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)

AppBuilder SDKは、開発者向けにAIネイティブアプリケーションのワンストップ開発ツールを提供します。これには、基本的なクラウドリソース、AI機能エンジン、Qianfan大規模モデル、および関連する機能コンポーネントが含まれ、AIネイティブアプリケーションの開発効率を向上させます。

</div>
<div align="center">
<h1>AppBuilder-SDK WeChatコミュニケーション グループ</h1>
<img src='docs/image/wechat_group.png' alt='wechat' width='200' >

</div>

## ニュース
* **[クラウドでRAG、Agent、GBIなどのアプリケーションを迅速に作成](https://console.bce.baidu.com/ai_apaas/app)**
* **[公式コンポーネントリスト](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz#%E5%BC%80%E5%8F%91%E7%BB%84%E4%BB%B6)**
* **2023.12.19 v0.1.0バージョンリリース**: [リリースノート](https://github.com/baidubce/app-builder/releases/tag/0.1.0)
  * 初期バージョンリリース、基本的なクラウドコンポーネントはBESをサポート、AI機能エンジンの音声、視覚クラスの10機能、大規模モデル関連のRAG、テキスト生成機能19。
* **2024.01.03 v0.2.0バージョンリリース** [リリースノート](https://github.com/baidubce/app-builder/releases/tag/0.2.0)
  * コアアップグレードポイントGBI関連コンポーネントの追加、v0.1.0のレガシー問題の修正
* **2024.01.26 v0.3.0バージョンリリース** [リリースノート](https://github.com/baidubce/app-builder/releases/tag/0.3.0)
  * 新規コンポーネント：Baidu検索ragコンポーネント（RAGwithBaiduSearch）を追加しました。[Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/rag_with_baidusearch.ipynb)
  * モデルリストの取得：Qianfan大規模モデルプラットフォームのモデル名と連携し、現在のアカウントのモデル名を動的に取得し、コンポーネントで使用できます[モデルリストの取得](https://github.com/baidubce/app-builder/blob/master/README.md#%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8)
  * 公式イメージを介してインスタンスコードを開発および実行できます[二次開発](https://github.com/baidubce/app-builder/blob/master/README.md#%E4%BA%8C%E6%AC%A1%E5%BC%80%E5%8F%91)
* **2024.02.27 v0.4.0バージョンリリース** [リリースノート](https://github.com/baidubce/app-builder/releases/tag/0.4.0)
  * AppBuilder Console SDKリリース[ナレッジベースCookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/console_dataset.ipynb)、[RAGコールCookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/console_rag.ipynb)
  * 大規模モデルコンポーネントの追加：Excel2Figure（Excel情報に基づいてグラフを描画）
  * AI機能エンジンコンポーネントの追加と更新：植物認識、動物認識、テーブルテキスト認識V2、手書きテキスト認識、QRコード認識、IDカード混合認識、ドキュメント補正認識、画像コンテンツ理解、ストリーミングTTS
  * AgentRuntime：[Cookbook](https://github.com/baidubce/app-builder/blob/master/cookbooks/agent_runtime.ipynb)を追加
* **2024.03.13 v0.4.1バージョンリリース** [リリースノート](https://github.com/baidubce/app-builder/releases/tag/0.4.1)
  * 次の機能のFunctionCall呼び出しをサポート：動植物認識、テーブルテキスト認識、バーコードおよびQRコード認識、IDカード混合認識、手書きテキスト認識、text2image、excel2figure
* **2024.03.20 v0.5.0バージョンリリース** [リリースノート](https://github.com/baidubce/app-builder/releases/tag/0.5.0)
  * AgentBuilder ConsoleSDKリリース[AgentコールCookBook](https://github.com/baidubce/app-builder/blob/0.5.0/cookbooks/agent_builder.ipynb)
  * AI機能エンジンコンポーネントの追加：ベクトル検索-VDB
  * 次の機能のFunctionCall呼び出しをサポートし、[CookBook](https://github.com/baidubce/app-builder/blob/master/cookbooks/general_ocr.ipynb)を追加：テキスト翻訳-汎用版、一般物体およびシーン認識-高度版、一般テキスト認識-高精度版、短音声認識-エクストリーム版
* **2024.03.21 v0.5.1バージョンリリース** [リリースノート](https://github.com/baidubce/app-builder/releases/tag/0.5.1)
  * バグ修正：Python 3.8以下の環境でAgentBuilder ConsoleSDKが使用できない問題を修正しました。同時に、次期バージョン0.6.0では、Python 3.8以下の環境のサポートは提供されなくなります。Pythonをバージョン3.9にアップグレードしてください
## チュートリアルとドキュメント

* **前提条件**
  * [認証](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6)
  * [コンポーネント権限の有効化](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#2%E3%80%81%E5%BC%80%E9%80%9A%E7%BB%84%E4%BB%B6%E6%9C%8D%E5%8A%A1)
* **APIドキュメント**
  * [APIドキュメント](https://cloud.baidu.com/doc/AppBuilder/s/Glqb6dfiz)


## クイックインストール

次のコマンドを実行して、Python用の最新バージョンのAppBuilder-SDKを迅速にインストールします（Python >= 3.8が必要）。

```shell
pip install --upgrade appbuilder-sdk
```
ローカルでappbuilder-sdkパッケージを実行できない場合は、公式イメージを使用してインストールおよび実行することもできます。詳細については、**二次開発**セクションを参照してください。

## クイックスタート

AppBuilder SDKを使用する前に、まず認証パラメータを申請して設定してください。詳細については、[認証](https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6)を参照してください。

``` python
# 環境でTOKENを設定します。次の例は省略されています
os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
```

## モデルリスト

AppBuilderは、Qianfanモデルのリストを取得する機能を提供します。特定のコンポーネントを実行する前に、現在のアカウントで利用可能なモデルのリストを取得できます。コードは次のとおりです。
``` python
import appbuilder
import os

os.environ["APPBUILDER_TOKEN"] = "bce-YOURTOKEN"
models = appbuilder.get_model_list(api_type_filter=["chat"], is_available=True)
print(", ".join(models))
```

独自のトークンを入力して、モデルリストの出力を次のように取得します。
``` shell
ERNIE-Bot 4.0, ERNIE-Bot-8K, ERNIE-Bot, ERNIE-Bot-turbo, EB-turbo-AppBuilder-specific version, Qianfan-Chinese-Llama-2-7B, Yi-34B-Chat, Llama-2-7B-Chat, Llama-2-13B-Chat, Llama-2-70B-Chat, ChatGLM2-6B-32K, ChatLaw, BLOOMZ-7B, Qianfan-BLOOMZ-7B-compressed, AquilaChat-7B
```

ユーザーがモデルを使いやすくするために、モデルの短い名前をいくつか示します
| Qianfanモデル名 | AppBuilder-SDKの短い名前 |
|----------------------------|------------------|
| ERNIE-Bot 4.0 | eb-4 |
| ERNIE-Bot-8K | eb-8k |
| ERNIE-Bot | eb |
| ERNIE-Bot-turbo | eb-turbo |
| EB-turbo-AppBuilder-specific version | ernie_speed_appbuilder |
| ERNIE Speed-AppBuilder | ernie_speed_appbuilder |


### 代表的な例

AppBuilderには、Promptテンプレートに基づくテキスト生成、検索拡張生成、外部ツールを使用したテキスト生成など、大規模モデルに基づくAIネイティブアプリケーションを構築するためのさまざまなパラダイムが含まれています。

#### プレイグラウンド
```python
import appbuilder

# プレイグラウンドコンポーネント
template_str = "あなたは{role}を演じています、私の質問に答えてください。\n\n質問：{question}。\n\n回答："
playground = appbuilder.Playground(prompt_template=template_str, model="ERNIE Speed-AppBuilder")

# 入力を定義し、プレイグラウンドコンポーネントを呼び出します
input = appbuilder.Message({"role": "Javaエンジニア", "question": "Java言語のメモリリサイクルメカニズムとは何ですか？"})
print(playground(input, stream=False, temperature=1e-10))

```

#### テキスト補完
```python
import appbuilder

# 類似質問生成コンポーネント
similar_q = appbuilder.SimilarQuestion(model="ERNIE Speed-AppBuilder")

# 入力を定義し、類似質問生成を呼び出します
input = appbuilder.Message("アイスクリームが食べたいのですが、どこで美味しいアイスクリームが食べられますか？")
print(similar_q(input))

```

#### チャットRAG
```python
import appbuilder
import os

# ここでのAPPBUILDER_TOKENはQPSが制限された試用アカウントです。独自のアプリケーションをテストするときは、独自のアカウントトークンに置き換えてください。
os.environ["APPBUILDER_TOKEN"] = ""

# ここにオンラインRAGアプリケーションIDを入力します。これは[AppBuilder Web側-マイアプリケーションインターフェイス]で表示できます
# Webリンク https://console.bce.baidu.com/ai_apaas/app
app_id = ""
rag_app = appbuilder.console.RAG(app_id)
query = "中国の首都はどこですか？"
answer = rag_app.run(appbuilder.Message(query)) # 新しい会話
print(answer.content)
```

## アプリケーションのサービス化

AppBuilder-SDKは、コンポーネントのサービス化機能を提供します。エージェントを定義することで、開発者はChainlit、Flaskなどのサービス化されたデモやAPIを迅速に開始して、迅速なエクスペリエンス環境を提供できます。

サービスをデプロイする必要がある環境では、開発者はまずChainlitライブラリを手動でインストールする必要があります

```shell
pip install chainlit
```
次に、AppBuilderのエージェントサービス化機能を使用して、サービスを迅速にデプロイします

```python
import appbuilder

# プレイグラウンドコンポーネント
playground = appbuilder.Playground(
    prompt_template="{query}",
    model="ERNIE Speed-AppBuilder"
)

# AgentRuntimeを使用してプレイグラウンドコンポーネントをサービス化します
agent = appbuilder.AgentRuntime(component=playground)

# chainlitデモを開始すると、ブラウザでエクスペリエンスダイアログページが自動的に開きます
agent.chainlit_demo(port=8091)
```

## 二次開発
現在、開発者向けにMessageやComponentなどのオープンなデータ構造を提供しており、開発者が既存の大規模モデルアプリケーションを統合するのに便利です。この部分はまだ構築中です。
二次開発では、公式の開発イメージを使用して、さまざまな依存ライブラリを迅速にインストールできます。
``` shell
docker pull registry.baidubce.com/appbuilder/appbuilder-sdk-devel:0.1.0
```

### メッセージ
- 大規模モデルアプリケーションを構築するための統一されたデータ構造で、Pydanticに基づいて構築され、さまざまなコンポーネント間を流れます。Message基本クラスのデフォルトフィールドはcontentで、型はAnyです。
```python
from appbuilder import Message
input_dict = Message({"query": "豚の角煮の作り方"})
input_list = Message(["text1", "text2", "text3"])
input_str = Message("豚の角煮の作り方")
```

### コンポーネント
- すべての機能ユニットの標準構造で、Message構造を入力および出力として使用します。内部実行ロジックはローカルで実行することも、クラウドサービスを呼び出すこともできます。以下は、公式コンポーネントの実装例です。
```python
class SimilarQuestionMeta(ComponentArguments):
    """ SimilarQuestionMeta
    """
    message: Message = Field(...,
                             variable_name="query",
                             description="入力メッセージ、モデルへの入力として使用され、通常は質問です。")


class SimilarQuestion(CompletionBaseComponent):
    """ 入力された質問に基づいて、その質問に関連する類似の質問をマイニングします。カスタマーサービス、質疑応答などのシナリオで広く使用されています。
    Examples:

        .. code-block:: python
            import os
            import appbuilder

            os.environ["APPBUILDER_TOKEN"] = "..."

            qa_mining = appbuilder.SimilarQuestion(model="ERNIE Speed-AppBuilder")

            msg = "アイスクリームが食べたいのですが、どこで美味しいアイスクリームが食べられますか？"
            msg = appbuilder.Message(msg)
            answer = qa_mining(msg)

            print("Answer: \n{}".format(answer.content))
    """
    name = "similar_question"
    version = "v1"
    meta = SimilarQuestionMeta

    def __init__(self, model=None):
        """SimilarQuestionMetaタスクを初期化します。

        Args:
            model (str|None): モデル名、使用するQianfanモデルを指定するために使用されます。

        Returns:
            None

        """
        super().__init__(SimilarQuestionMeta, model=model)

    def run(self, message, stream=False, temperature=1e-10):
        """
        モデルに実行する入力（メッセージ）を与え、実行パラメータを指定し、結果を返します。

        Args:
            message (obj:`Message`): 入力メッセージ、モデルの主要な入力コンテンツとして使用されます。これは必須パラメータです。
            stream (bool, optional): 応答をストリーミング形式で返すかどうかを指定します。デフォルトはFalseです。
            temperature (float, optional): モデル構成の温度パラメータで、モデルの生成確率を調整するために使用されます。値の範囲は0.0〜1.0で、値が低いほど生成が確定的になり、値が高いほど生成が多様になります。デフォルト値は1e-10です。

        Returns:
            obj:`Message`: モデル実行後の出力メッセージ。
        """
        return super().run(message=message, stream=stream, temperature=temperature)
```

## ライセンス

AppBuilder-SDKは、Apache-2.0オープンソースライセンスに従います。
