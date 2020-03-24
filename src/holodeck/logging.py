import sys
import time
import traceback

_calls = []
_call_log_filename = "client_call_log.csv"


def log_call(fun, uuid):
    # noinspection PyProtectedMember
    def log_call_inner(*args, **kwargs):
        stack = sys._getframe().f_back
        fun_name = fun.__name__
        time_now = time.time()

        _calls.append((str(time_now), uuid, fun_name, stack))
        return fun(*args, **kwargs)

    return log_call_inner


def export_call_log():
    global _calls
    # if not os.path.exists(_call_log_filename):
    #     os.path.touc
    with open(_call_log_filename, "a") as call_log_file:
        for call in _calls:
            stack_line = "\\n".join(
                [
                    line.replace("\n", "\\n")
                    for line in traceback.format_stack(call[3])
                ]
            )
            call_line = ",".join([*call[:3], stack_line])
            call_log_file.write(f"{call_line}\n")

    _calls = []
    print(f"Exported call log to {_call_log_filename}")
