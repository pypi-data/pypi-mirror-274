import unittest
import os
import appbuilder
# from ...api.conf.load_config import LoadConfig
from appbuilder.core.assistant.type import thread_type
path = os.path.dirname(os.path.abspath(__file__)) + "/files"
os.environ["APPBUILDER_TOKEN"] = "bce-v3/ALTAK-zX2OwTWGE9JxXSKxcBYQp/7dd073d9129c01c617ef76d8b7220a74835eb2f4"
check_tool = {
    "name": "get_cur_whether",
    "description": "这是一个获得指定地点天气的工具",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "省，市名，例如：河北省"
            },
            "unit": {
                "type": "string",
                "enum": [
                    "摄氏度",
                    "华氏度"
                ]
            }
        },
        "required": [
            "location"
        ]
    }
}


def get_cur_whether(location, unit):
    """
    获取当前某个位置的温度，返回一个字符串，包含该位置的当前温度和单位。
    """
    return "{} 的当前温度是30 {}".format(location, unit)


class TestRunsStepsList(unittest.TestCase):
    """
    测试创建消息
    """
    def setUp(self):
        """
        初始化测试环境，设置必要的环境变量和配置文件。
        """
        pass
        
        # LoadConfig()

    @classmethod
    def setUpClass(cls):
        """
        创建 assistant thread messages 并运行
        """
        # LoadConfig()
        assistant_create = appbuilder.assistant.assistants.create(
            name="Abc-_123",
            description="test",
            model="ERNIE-4.0-8K",
            tools=[
                {'type': 'function', 'function': check_tool}
            ]
        )
        thread_create = appbuilder.assistant.threads.create()
        appbuilder.assistant.threads.messages.create(
            thread_id=thread_create.id,
            role="user",
            content="今天北京的天气怎么样"
        )
        run_result = appbuilder.assistant.threads.runs.stream_run(
            thread_id=thread_create.id,
            assistant_id=assistant_create.id,
        )

        run_id = ""
        for run_step in run_result:
            # print("\nRun result: {}\n".format(run_step))
            if run_step.status == 'queued':
                run_obj = run_step.details.run_object
                run_id = run_obj.id
            elif run_step.status == 'requires_action':
                detail = run_step.details
                tool_call = detail.tool_calls[0]
                func_res = get_cur_whether(**eval(tool_call.function.arguments))
                appbuilder.assistant.threads.runs.submit_tool_outputs(
                    run_id=run_id,
                    thread_id=thread_create.id,
                    tool_outputs=[
                        {"tool_call_id": tool_call.id,
                         "output": func_res, }
                    ]
                )
        cls.thread_id = thread_create.id
        cls.assistant_id = assistant_create.id
        cls.run_id = run_id

    @classmethod
    def tearDownClass(cls):
        """
        删除线程 assistant
        """
        appbuilder.assistant.threads.delete(cls.thread_id)
        appbuilder.assistant.assistants.delete(cls.assistant_id)

    def test_runs_steps_list_must_params_right(self):
        """
        grade: p0
        description: must params right
        """
        runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
            thread_id=self.thread_id,
            run_id=self.run_id
        )
        data = runs_steps_list.data
        for i in range(len(data)-1):
            self.assertGreaterEqual(data[i].created_at, data[i+1].created_at)
        self.assertEqual(data[0].thread_id, self.thread_id)
        self.assertEqual(data[0].run_id, self.run_id)

    def test_runs_steps_list_thread_id_del(self):
        """
        grade: p2
        description: thread_id del
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                run_id=self.run_id
            )
        except Exception as e:
            self.assertIn("missing 1 required positional argument: 'thread_id'", str(e))
        else:
            raise Exception("测试失败，thread_id del 查询run的step记录成功\n", print(runs_steps_list))

    def test_runs_steps_list_thread_id_None(self):
        """
        grade: p2
        description: thread_id None
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                thread_id="",
                run_id=self.run_id
            )
        except Exception as e:
            self.assertIn("String should have at least 1 character", str(e))
        else:
            raise Exception("测试失败，thread_id None 查询run的step记录成功\n", print(runs_steps_list))

    def test_runs_steps_list_thread_id_int_type(self):
        """
        grade: p2
        description: thread_id int type
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                thread_id=12345,
                run_id=self.run_id
            )
        except Exception as e:
            self.assertIn("Input should be a valid string", str(e))
        else:
            raise Exception("测试失败，thread_id int type 查询run的step记录成功\n", print(runs_steps_list))

    def test_runs_steps_list_thread_id_err_id(self):
        """
        grade: p2
        description: thread_id err thread_id
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                thread_id=self.thread_id.replace("thread", "err"),
                run_id=self.run_id
            )
        except Exception as e:
            self.assertIn("threadId不存在", str(e))
        else:
            raise Exception("测试失败，thread_id err thread_id 查询run的step记录成功\n", print(runs_steps_list))

    def test_runs_steps_list_run_id_del(self):
        """
        grade: p2
        description: run_id del
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                thread_id=self.thread_id
            )
        except Exception as e:
            self.assertIn("missing 1 required positional argument: 'run_id'", str(e))
        else:
            raise Exception("测试失败，run_id del 查询run的step记录成功\n", print(runs_steps_list))

    def test_runs_steps_list_run_id_None(self):
        """
        grade: p2
        description: run_id None
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                thread_id=self.thread_id,
                run_id=""
            )
        except Exception as e:
            self.assertIn("String should have at least 1 character", str(e))
        else:
            raise Exception("测试失败，run_id None 查询run的step记录成功\n", print(runs_steps_list))

    def test_runs_steps_list_run_id_int_type(self):
        """
        grade: p2
        description: run_id int type
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                thread_id=self.thread_id,
                run_id=123456
            )
        except Exception as e:
            self.assertIn("Input should be a valid string", str(e))
        else:
            raise Exception("测试失败，thread_id int type 查询run的step记录成功\n", print(runs_steps_list))

    def test_runs_steps_list_run_id_err_id(self):
        """
        grade: p2
        description: run_id err thread_id
        """
        try:
            runs_steps_list = appbuilder.assistant.threads.runs.steps.list(
                thread_id=self.thread_id,
                run_id=self.run_id.replace("run", "err")
            )
        except Exception as e:
            self.assertIn("当前run不存在", str(e))
        else:
            raise Exception("测试失败，run_id err thread_id 查询run的step记录成功\n", print(runs_steps_list))


if __name__ == '__main__':
    unittest.main(verbosity=2)
