from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from langchain_xiao.chat_models.utils import get_chat_model


async def main():
    # instance_type = "ChatLlamaCpp"
    # model_kwargs = {
    #     "model_path": r"E:\WorkSpace\LLMWorkSpace\Models\LLM\qwen\Qwen1.5-0.5B-Chat-GGUF\qwen1_5-0_5b-chat-q5_k_m.gguf",
    #     "verbose": True,
    # }
    instance_type = "MyChatHunyuan"
    # model_kwargs = {
    #     "model_name": "moonshot-v1-8k",
    #     "openai_api_key": "sk-xxx",
    #     "openai_api_base": "https://api.moonshot.cn/v1",
    # }
    model_kwargs = {
        # "model_name": "hunyuan-pro",
        "hunyuan_secret_id": "AKIDjP810xlgbdM3pgbaio2bl2KjzSxIlR6t",
        "hunyuan_secret_key": "d9lLB8468FSXhu6Jdu4DHE4pgggZQC39",
    }
    # model_kwargs = {
    #     "model_name": "qwen-plus",
    #     "dashscope_api_key": "sk-dfd035cbce244533ac9e8fed7290f4fc",
    # }
    # model_kwargs = {
    #     # "model": "Baichuan2-53B",
    #     "model": "Baichuan4",
    #     "baichuan_api_key": "sk-2ec661471d2358e1996c00d8e1e17c19",  # 畅游api
    # }

    chat_model = get_chat_model(instance_type, **model_kwargs)
    print(await chat_model.ainvoke("你是谁"))
    # async for chunk in chat_model.astream(messages):
    #     print(chunk)

    # chat_model = get_chat_model("ChatBaichuan", **model_kwargs)
    # print(await chat_model.ainvoke("你是谁"))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
