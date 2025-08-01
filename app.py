import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# 環境変数を読み込み
load_dotenv()

def get_llm_response(input_text, expert_type):
    """
    入力テキストと専門家の種類を受け取り、LLMからの回答を返す関数
    
    Args:
        input_text (str): ユーザーからの入力テキスト
        expert_type (str): 選択された専門家の種類
    
    Returns:
        str: LLMからの回答
    """
    # 専門家の種類に応じてシステムメッセージを設定
    system_messages = {
        "プログラミング専門家": "あなたは経験豊富なプログラミング専門家です。プログラミングに関する質問に対して、具体的で実践的なアドバイスを提供してください。コード例も含めて回答してください。",
        "データサイエンス専門家": "あなたは熟練したデータサイエンティストです。データ分析、機械学習、統計に関する質問に対して、専門的で分かりやすい解説を提供してください。",
        "ビジネス戦略専門家": "あなたは経験豊富なビジネス戦略コンサルタントです。ビジネスに関する質問に対して、戦略的な視点から実用的なアドバイスを提供してください。",
        "教育専門家": "あなたは教育分野の専門家です。学習方法や教育に関する質問に対して、効果的で具体的なアドバイスを提供してください。"
    }
    
    # ChatOpenAIインスタンスを作成
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # メッセージを構成
    messages = [
        SystemMessage(content=system_messages[expert_type]),
        HumanMessage(content=input_text)
    ]
    
    # LLMに問い合わせ
    response = llm.invoke(messages)
    return response.content

def main():
    """メイン関数"""
    
    # ページ設定
    st.set_page_config(
        page_title="AI専門家相談アプリ",
        page_icon="🤖",
        layout="wide"
    )
    
    # タイトル
    st.title("🤖 AI専門家相談アプリ")
    
    # アプリの概要説明
    st.markdown("""
    ## アプリの概要
    このアプリは、様々な分野の専門家として振る舞うAIに質問できるWebアプリです。
    
    ## 使い方
    1. **専門家を選択**: 相談したい分野の専門家をラジオボタンで選択してください
    2. **質問を入力**: テキストエリアに質問や相談内容を入力してください
    3. **送信**: 「回答を取得」ボタンをクリックして、AI専門家からの回答を取得してください
    
    ---
    """)
    
    # サイドバーで専門家選択
    with st.sidebar:
        st.header("🎯 専門家選択")
        expert_type = st.radio(
            "相談したい専門家を選択してください：",
            [
                "プログラミング専門家",
                "データサイエンス専門家", 
                "ビジネス戦略専門家",
                "教育専門家"
            ]
        )
        
        # 選択された専門家の説明
        expert_descriptions = {
            "プログラミング専門家": "プログラミング言語、開発手法、技術的な問題解決についてアドバイスします。",
            "データサイエンス専門家": "データ分析、機械学習、統計学について専門的な知識を提供します。",
            "ビジネス戦略専門家": "事業戦略、マーケティング、経営に関する戦略的アドバイスを提供します。",
            "教育専門家": "効果的な学習方法、教育手法について専門的なアドバイスを提供します。"
        }
        
        st.info(f"**{expert_type}**\n\n{expert_descriptions[expert_type]}")
    
    # メインエリア
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("💬 質問入力")
        
        # 入力フォーム
        user_input = st.text_area(
            "質問や相談内容を入力してください：",
            height=200,
            placeholder="例：Pythonでファイルを読み込む方法を教えてください"
        )
        
        # 送信ボタン
        submit_button = st.button("🚀 回答を取得", type="primary")
    
    with col2:
        st.header("🎯 AI専門家からの回答")
        
        # 回答表示エリア
        if submit_button:
            if user_input.strip():
                with st.spinner("AI専門家が回答を生成中..."):
                    try:
                        # LLMからの回答を取得
                        response = get_llm_response(user_input, expert_type)
                        
                        # 回答を表示
                        st.success("回答が生成されました！")
                        st.markdown(f"**選択した専門家**: {expert_type}")
                        st.markdown("**回答内容**:")
                        st.write(response)
                        
                    except Exception as e:
                        st.error(f"エラーが発生しました: {str(e)}")
                        st.info("OpenAI APIキーが正しく設定されているか確認してください。")
            else:
                st.warning("質問を入力してください。")
        else:
            st.info("上記のフォームに質問を入力して「回答を取得」ボタンをクリックしてください。")
    
    # フッター
    st.markdown("---")
    st.markdown("💡 **ヒント**: より具体的な質問をすることで、より詳細で役立つ回答を得ることができます。")

if __name__ == "__main__":
    main()
