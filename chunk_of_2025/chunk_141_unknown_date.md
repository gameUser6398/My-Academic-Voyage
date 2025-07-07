

文献支持
微调蛋白质语言模型可促进对不同任务的预测 |自然通讯 (nature.com)

9月22日

wandb记录日志
Optimize_Hugging_Face_models_with_Weights_&_Biases.ipynb - Colab (google.com)

Hugging Face Transformers | Weights & Biases Documentation (wandb.ai)

使用 Trainer API 微调模型 - Hugging Face NLP Course

9月23日

vscode的launch.json调试代码真不容易啊，它的好处在哪里

{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Train Protein Model",
            "type": "python",
            "request": "launch",

            "program": "${workspaceFolder}/train.py",  // 确保这里指向你的主训练脚本
            "console": "integratedTerminal",

            "justMyCode": false,  // 确保调试第三方库代码
            "env": {
                "PYTHONOPTIMIZE": "0"
            }
        }
    ]
}

今天主要精力在调试代码，对Transformer的Train、TrainArgument更熟悉了。真实感慨他

们能把这么多参数封装的这么好。

在Transformer超参数方面，不要尝试用hydra，因为会导致Object of type ListConfig is

not JSON serializable #567
来自 <https://github.com/huggingface/peft/issues/567>

过度依赖coplit，去技术网站上Stack Overflow 、csdn、github上搜索可能结果更好

