# coding=utf-8
from __future__ import unicode_literals
import os
from soc_system.tools.gpg_tool import GPGTool


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soc.settings')
    import django
    django.setup()


"""
分中心与子中心同时更新 先更新分中心 再更新子中心

      系统更新

       前端
        |
        |
        v
       中心
        |
        |
        v
      分中心1                 分中心2
        |
        |
        v
      子中心1         子中心2         子中心3
        |
        |
        v
      SocAgent
        |
        |
        v
      服务组件


    接口参数：
        binfile: 更新包 (local path)
        type:    类型（系统/Nids/扫描）
        target:  更新目标 [
                    {'sub_id': 1, uuid: xxx， task_id: 1}
                    {'sub_id': None,  uuid: xxx, task_id: 2}
                ]
        src:     更新指令来源 用于状态回传 (当前中心 uuid)

    返回结果

        cache upgrade_task_1
                status: 0 未运行 1 运行中 2 正常结束 3: 异常结束
                msg: 提示信息，随着状态和进度的变化会 变动
                progress: 进度百分比

    更新接口--逻辑示意
        接收更新包 验证包合法性（加密/签名/版本/类型）

        判断更新目标是否是自身或者自身的功能组件

        是
            开始更新
                src 是否为自身
                    是
                        记录状态
                    否
                        上传状态到上级中心
        否
            有下级中心
                寻找合适的下级中心下发
            无
                返回错误


    更新云松系统逻辑

        步骤 中心数 + 5

        解包
        复制配置
        替换代码
        重启
        重启之后上传 当前版本

    更新组件逻辑
        步骤 中心数 + 3
        解包
        通过SocAgent传输deb包
        通过SocAgent执行升级命令

    接收更新状态接口

        参数
            src
            tark_id
            msg
            status
            progress

        逻辑
            src 为自身，存储状态
            src 不为自身，向父节点传递

"""


class GPG(GPGTool):

    def __init__(self):
        from common import SetUpCls

        super(GPG, self).__init__(
            passphrase=SetUpCls.passphrase,
            send_id=SetUpCls.send_id,
            recv_id=SetUpCls.recv_id,
            cls=SetUpCls.cls,
            clss=SetUpCls.clss)


if __name__ == '__main__':
    g = GPG()
    # g.version('/tmp/yunsong_v2.25.2.tar.gz')
    # g.encrypt_sign('/tmp/soc.tar.gz', '/tmp/soc.tar.gz.bin')
    # s, r = g.decrypt('/tmp/soc.tar.gz.bin', '/tmp/soc_decrypt.tar.gz')
    print(g.info('/tmp/soc_decrypt.tar.gz'))
    # g.info('/tmp/yunsong_decrypt.tar.gz')
    # g.encrypt_sign('/tmp/nids.tar.gz', '/tmp/nids.tar.gz.bin')
    # s, r = g.decrypt('/tmp/nids.tar.gz.bin', '/tmp/nids_decrypt.tar.gz')
    # print(g.info('/tmp/nids_decrypt.tar.gz'))

