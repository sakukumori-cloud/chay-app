import base64
import os
import streamlit as st
from openai import OpenAI

# ページの設定
st.set_page_config(page_title="チャット先生（個別指導版）", page_icon="🤖")
st.title("🤖 チャット先生（個別指導アシスタント）")

# APIキーの入力
api_key = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))

if not api_key:
    st.warning("StreamlitのSecretsにOpenAIのAPIキー（OPENAI_API_KEY）を設定してください。")
    st.stop()

client = OpenAI(api_key=api_key)
model_name = "gpt-4o"

# 生徒目線の対話型プロンプト
system_prompt = """
あなたは日本の個別指導塾の、生徒から大人気の優しく親しみやすいベテラン講師です。
生徒から送られてきた問題の画像やテキストに対して、以下のルールで指導してください：
1. いきなり答えのすべてを教えず、生徒が自分で気づけるようにヒントを優しく出してください。
2. 解説は専門用語や参考書のような堅い表現を避け、中学生や高校生にも直感的にわかるよう、身近な例えを用いてかみ砕いて説明してください。
3. 最後に「ここまでで、どのあたりが分かったかな？」など、生徒に問いかけて会話をキャッチボールしてください。
"""

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 過去のメッセージの表示（描画はすべてここが一元管理する）
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "text":
                        st.markdown(item["text"])
                    elif item.get("type") == "image_url":
                        img_data = item.get("image_url")
                        url = img_data.get("url") if isinstance(img_data, dict) else img_data
                        if url:
                            st.image(url, caption="アップロードされた問題", width=300)
            else:
                st.markdown(content)

# ユーザーからの入力を受け取る
uploaded_file = st.file_uploader("問題の写真をアップロード（JPEG / PNG）", type=["jpg", "jpeg", "png"])
prompt = st.chat_input("先生に質問を入力（例：問3の(1)が分かりません）")

if prompt or uploaded_file:
    user_content = []
    
    # テキストの処理
    if prompt:
        user_content.append({"type": "text", "text": prompt})
    else:
        user_content.append({"type": "text", "text": "この問題を解説してください。"})
        
    # 画像の処理
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{base64_image}"
        user_content.append({"type": "image_url", "image_url": {"url": image_url}})
        
    # 履歴にユーザーの入力を追加（※ここでは画面に直接描画せず、セッションへの追加のみに絞ることで二重を防ぐ）
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    # 画面を即座に再描画してユーザーの入力を一番下に綺麗に反映させる
    st.rerun()

# ユーザーの最新入力に対してAIの返答を生成するロジック
# （直前のメッセージがユーザーのもの、かつアシスタントの返答がまだの場合に実行）
if len(st.session_state.messages) > 1 and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("先生が考えています...（わかりやすく噛み砕いています）"):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages,
                    max_tokens=1500
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")import base64
import os
import streamlit as st
from openai import OpenAI

# ページの設定
st.set_page_config(page_title="チャット先生（個別指導版）", page_icon="🤖")
st.title("🤖 チャット先生（個別指導アシスタント）")

# APIキーの入力
api_key = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))

if not api_key:
    st.warning("StreamlitのSecretsにOpenAIのAPIキー（OPENAI_API_KEY）を設定してください。")
    st.stop()

client = OpenAI(api_key=api_key)
model_name = "gpt-4o"

# 生徒目線の対話型プロンプト
system_prompt = """
あなたは日本の個別指導塾の、生徒から大人気の優しく親しみやすいベテラン講師です。
生徒から送られてきた問題の画像やテキストに対して、以下のルールで指導してください：
1. いきなり答えのすべてを教えず、生徒が自分で気づけるようにヒントを優しく出してください。
2. 解説は専門用語や参考書のような堅い表現を避け、中学生や高校生にも直感的にわかるよう、身近な例えを用いてかみ砕いて説明してください。
3. 最後に「ここまでで、どのあたりが分かったかな？」など、生徒に問いかけて会話をキャッチボールしてください。
"""

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 過去のメッセージの表示（描画はすべてここが一元管理する）
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "text":
                        st.markdown(item["text"])
                    elif item.get("type") == "image_url":
                        img_data = item.get("image_url")
                        url = img_data.get("url") if isinstance(img_data, dict) else img_data
                        if url:
                            st.image(url, caption="アップロードされた問題", width=300)
            else:
                st.markdown(content)

# ユーザーからの入力を受け取る
uploaded_file = st.file_uploader("問題の写真をアップロード（JPEG / PNG）", type=["jpg", "jpeg", "png"])
prompt = st.chat_input("先生に質問を入力（例：問3の(1)が分かりません）")

if prompt or uploaded_file:
    user_content = []
    
    # テキストの処理
    if prompt:
        user_content.append({"type": "text", "text": prompt})
    else:
        user_content.append({"type": "text", "text": "この問題を解説してください。"})
        
    # 画像の処理
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{base64_image}"
        user_content.append({"type": "image_url", "image_url": {"url": image_url}})
        
    # 履歴にユーザーの入力を追加（※ここでは画面に直接描画せず、セッションへの追加のみに絞ることで二重を防ぐ）
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    # 画面を即座に再描画してユーザーの入力を一番下に綺麗に反映させる
    st.rerun()

# ユーザーの最新入力に対してAIの返答を生成するロジック
# （直前のメッセージがユーザーのもの、かつアシスタントの返答がまだの場合に実行）
if len(st.session_state.messages) > 1 and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("先生が考えています...（わかりやすく噛み砕いています）"):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages,
                    max_tokens=1500
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")import base64
import os
import streamlit as st
from openai import OpenAI

# ページの設定
st.set_page_config(page_title="チャット先生（個別指導版）", page_icon="🤖")
st.title("🤖 チャット先生（個別指導アシスタント）")

# APIキーの入力
default_api_key = os.environ.get("OPENAI_API_KEY", "")
# Secretsから正しくAPIキーを読み込む
api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.warning("サイドバーにOpenAIのAPIキーを入力してください。(sk-...から始まるキー)")
    st.stop()

client = OpenAI(api_key=api_key)
model_name = "gpt-4o"

# 生徒目線の対話型プロンプト
system_prompt = """
あなたは日本の個別指導塾の、生徒から大人気の優しく親しみやすいベテラン講師です。
生徒から送られてきた問題の画像やテキストに対して、以下のルールで指導してください：
1. いきなり答えのすべてを教えず、生徒が自分で気づけるようにヒントを優しく出してください。
2. 解説は専門用語や参考書のような堅い表現を避け、中学生や高校生にも直感的にわかるよう、身近な例えを用いてかみ砕いて説明してください。
3. 最後に「ここまでで、どのあたりが分かったかな？」など、生徒に問いかけて会話をキャッチボールしてください。
"""

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 過去のメッセージの表示
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "text":
                        st.markdown(item["text"])
                    elif item.get("type") == "image_url":
                        st.image(item["image_url"]["url"], caption="アップロードされた問題", width=300)
            else:
                st.markdown(content)

# ユーザーからの入力を受け取る
uploaded_file = st.file_uploader("問題の写真をアップロード（JPEG / PNG）", type=["jpg", "jpeg", "png"])
prompt = st.chat_input("先生に質問を入力（例：問3の(1)が分かりません）")

if prompt or uploaded_file:
    user_content = []
    display_text = prompt if prompt else "この問題を解説してください。"
    
    if prompt:
        user_content.append({"type": "text", "text": prompt})
    else:
        user_content.append({"type": "text", "text": "この問題の画像を解説してください。"})
        
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{base64_image}"
        user_content.append({"type": "image_url", "image_url": {"url": image_url}})
        
    with st.chat_message("user"):
        if uploaded_file:
            st.image(bytes_data, caption="アップロードされた問題", width=300)
        st.markdown(display_text)
        
    st.session_state.messages.append({"role": "user", "content": user_content})
    
    with st.chat_message("assistant"):
        with st.spinner("先生が考えています...（わかりやすく噛み砕いています）"):
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages,
                    max_tokens=1500
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
