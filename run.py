from self_healing_agent import SelfHealingCodingAgent


def main() -> None:
    print("Self-Healing Coding Agent")
    print("输入一个编程任务，Agent 会自动生成、运行并修复代码。")
    print("示例：写一个读取 CSV 文件并计算每列平均值的 Python 脚本")
    print("-" * 60)

    task = input("请输入任务：\n> ").strip()
    if not task:
        print("任务不能为空。")
        return

    agent = SelfHealingCodingAgent(max_rounds=3)
    result = agent.run(task)

    print("\n运行结果：")
    print(f"成功：{result.success}")
    print(f"迭代轮数：{result.rounds}")
    print(f"最终代码：{result.final_code_path}")
    print(f"运行日志：{result.log_path}")


if __name__ == "__main__":
    main()
