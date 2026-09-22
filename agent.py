import json
import os
import time
from typing import Any, cast

from dotenv import load_dotenv
import litellm

from session import Session
from permissions import PermissionManager
import tools as tool_impl

AUTO_APPROVE_THRESHOLD = 0.85


class Agent:
    def __init__(self, session: Session):
        model, self.api_key = self._get_env_vars()
        self.session = session
        self.permission_manager = PermissionManager()
        self.session.model = model
        self.session.context_window = self._get_context_window(model)

    def _get_env_vars(self) -> tuple[str, str]:
        load_dotenv()

        model = os.environ["LITELLM_MODEL"] or ""
        api_key = os.environ["LITELLM_API_KEY"] or ""

        return model, api_key

    def _get_context_window(self, model: str) -> int | None:
        try:
            get_max_tokens = getattr(litellm, "get_max_tokens", None)
            if callable(get_max_tokens):
                max_tokens = get_max_tokens(model)
                if isinstance(max_tokens, int) and max_tokens > 0:
                    return max_tokens

            get_model_info = getattr(litellm, "get_model_info", None)
            if callable(get_model_info):
                info = get_model_info(model)
                if isinstance(info, dict):
                    for key in ("max_input_tokens", "max_tokens", "max_output_tokens"):
                        value = info.get(key)
                        if isinstance(value, int) and value > 0:
                            return value
        except Exception:
            pass

        return None

    def _accumulate_used_tokens(self, response: litellm.ModelResponse) -> None:
        self.session.used_tokens += response["usage"]["total_tokens"]

    def run(self, user_prompt: str, messages: list[Any]) -> tuple[str, list[Any]]:
        messages_copy = messages.copy()
        messages_copy.append({"role": "user", "content": user_prompt})

        while True:
            response = litellm.completion(
                model=self.session.model,
                api_key=self.api_key,
                messages=messages_copy,
                stream=False,
                tools=tool_impl.tools,
            )

            response = cast(litellm.ModelResponse, response)

            self._accumulate_used_tokens(response)

            message_obj = response.choices[0].message
            message_dict: dict[str, Any] = {
                "role": "assistant",
                "content": message_obj.content or "",
            }
            if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
                message_dict["tool_calls"] = message_obj.tool_calls

            messages_copy.append(message_dict)

            if not message_obj.tool_calls:
                return message_obj.content or "", messages_copy

            for tool_call in message_obj.tool_calls:
                self._execute_tool(tool_call, messages_copy)

    def _run_tool(self, handler: Any, args: dict[str, Any]) -> tuple[str, float]:
        started = time.perf_counter()
        try:
            raw_result = handler(**args)
            result = (
                raw_result if isinstance(raw_result, str) else json.dumps(raw_result)
            )
        except TypeError as e:
            result = f"Execution Error: Invalid tool arguments - {str(e)}"
        except Exception as e:
            result = f"Execution Error: {str(e)}"

        return result, time.perf_counter() - started

    def _should_auto_approve(
        self, tool_name: str, args: dict[str, Any], reason: str
    ) -> bool:
        from jev import assess_operation

        try:
            probability, risk_class = assess_operation(
                tool_name, args, reason, self.session.permission_mode
            )
        except Exception as e:
            self.session.ui.display_error(f"Auto-approve check failed: {e}")
            return False

        if probability < AUTO_APPROVE_THRESHOLD:
            self.session.ui.display_info_message(
                f"Auto-approve declined ({probability:.2f} safe, {risk_class})"
            )
            return False

        self.session.ui.display_info_message(
            f"Auto-approved ({probability:.2f} safe, {risk_class})"
        )
        return True

    def _execute_tool(self, tool_call: Any, messages_copy: list[Any]) -> None:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        handler = getattr(tool_impl, function_name, None)

        decision = self.permission_manager.check(
            tool_name=function_name,
            args=args,
            mode=self.session.permission_mode,
        )

        duration: float | None = None

        if decision.action == "deny":
            result: str = f"Permission denied: {decision.reason}"
        elif decision.action == "ask":
            if not callable(handler):
                result = "Error: Tool not found"
            elif self.session.auto_approve and self._should_auto_approve(
                function_name, args, decision.reason
            ):
                result, duration = self._run_tool(handler, args)
            else:
                self.session.ui.stop_processing()
                choice = self.session.ui.confirm_tool_execution(
                    tool_name=function_name,
                    args=args,
                    reason=decision.reason,
                    mode=self.session.permission_mode,
                )
                self.session.ui.display_processing()

                if choice == "auto":
                    self.session.auto_approve = True
                    self.session.ui.display_info_message(
                        "Auto-approve enabled for this session"
                    )
                    choice = "yes"

                if choice == "yes":
                    result, duration = self._run_tool(handler, args)
                else:
                    result = "Permission denied: User rejected approval request"
        elif not callable(handler):
            result = "Error: Tool not found"
        else:
            result, duration = self._run_tool(handler, args)

        self.session.ui.display_tool_execution(function_name, result, duration)

        messages_copy.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result,
            }
        )
