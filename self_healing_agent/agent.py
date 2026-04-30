from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

from .utils import clean_code_block, ensure_dir, run_python_file, timestamp


@dataclass
class AgentResult:
    success: bool
    rounds: int
    final_code_path: Path
    log_path: Path


class SelfHealingCodingAgent:
    """
    A lightweight coding agent that can:
    1. Generate Python code from a natural language task
    2. Execute the generated code locally
    3. Capture runtime errors
    4. Ask the LLM to repair the code
    5. Repeat until success or max rounds reached
    """

    def __init__(
        self,
        model: str | None = None,
        workspace: str = "workspace",
        max_rounds: int = 3,
        timeout: int = 15,
    ) -> None:
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Set it in .env or environment variables."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.workspace = ensure_dir(workspace)
        self.max_rounds = max_rounds
        self.timeout = timeout

    def _ask_llm(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一个严谨的高级 Python 工程师。"
                        "你的输出必须是完整、可运行的 Python 代码。"
                        "不要输出解释，不要输出 Markdown。"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""

    def _generate_code(self, task: str) -> str:
        prompt = f"""
请根据下面的需求生成一个完整 Python 程序。

需求：
{task}

代码要求：
1. 可以直接运行
2. 包含必要的异常处理
3. 输出结果清晰
4. 尽量减少不必要的第三方依赖
5. 只返回 Python 代码，不要解释
"""
        return clean_code_block(self._ask_llm(prompt))

    def _repair_code(self, task: str, code: str, error: str) -> str:
        prompt = f"""
下面的 Python 代码运行失败，请根据错误信息修复它。

原始需求：
{task}

当前代码：
{code}

错误信息：
{error}

修复要求：
1. 返回修复后的完整 Python 代码
2. 保留原始需求的功能
3. 不要解释
4. 不要 Markdown 代码块
"""
        return clean_code_block(self._ask_llm(prompt))

    def run(self, task: str) -> AgentResult:
        run_id = timestamp()
        code_path = self.workspace / f"generated_{run_id}.py"
        log_path = self.workspace / f"log_{run_id}.txt"

        code = self._generate_code(task)

        with open(log_path, "w", encoding="utf-8") as log:
            log.write(f"TASK:\n{task}\n\n")

            for round_id in range(1, self.max_rounds + 1):
                code_path.write_text(code, encoding="utf-8")

                log.write(f"========== ROUND {round_id} ==========" + "\n")
                log.write(f"CODE PATH: {code_path}\n\n")

                print(f"\n🚀 Round {round_id}: running {code_path}")

                try:
                    returncode, stdout, stderr = run_python_file(
                        code_path, timeout=self.timeout
                    )
                except Exception as exc:
                    returncode, stdout, stderr = 1, "", str(exc)

                log.write("STDOUT:\n")
                log.write(stdout or "<empty>\n")
                log.write("\nSTDERR:\n")
                log.write(stderr or "<empty>\n")
                log.write("\n\n")

                if returncode == 0:
                    print("✅ Code executed successfully.")
                    if stdout:
                        print(stdout)
                    return AgentResult(
                        success=True,
                        rounds=round_id,
                        final_code_path=code_path,
                        log_path=log_path,
                    )

                print("❌ Code failed. Asking model to repair...")
                code = self._repair_code(task, code, stderr)

        print("⚠️ Agent failed after max repair rounds.")
        return AgentResult(
            success=False,
            rounds=self.max_rounds,
            final_code_path=code_path,
            log_path=log_path,
        )
