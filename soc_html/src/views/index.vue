<template>
    <div>
        <!-- Top Bar Start -->
        <topbar v-ref:top @change="change(topic)"></topbar>
        <!-- Top Bar End -->

        <!-- Left Sidebar Start -->
        <side-menu v-ref:side></side-menu>
        <!-- Left Sidebar End -->

        <!-- ============================================================== -->
        <!-- Start right Content here -->
        <!-- ============================================================== -->
        <content></content>
        <!-- ============================================================== -->
        <!-- End Right content here -->
        <!-- ============================================================== -->
    </div>
</template>
<style scoped>
    .lock-screen-con {
        left: 0px;
        position: fixed;
        right: 0;
        top: 0px;
        z-index: 99999;
        color: #f2f2f2;
        width: 100%;
        height: 100%;
        background: url(../assets/images/lock-screen.png);
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
    }

    .lock-screen-box {
        width: 150px;
        height: 130px;
        position: absolute;
        top: 50%;
        left: 50%;
        margin-left: -75px;
        margin-top: -65px;
    }

    .user-avatar img {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 2px solid #4a92ff;
    }

    .lock-screen-icon {
        position: absolute;
        top: 7px;
        left: 7px;
    }
</style>
<script>
    import Api from 'src/lib/api'
    import Topbar from './topbar'
    import SideMenu from './sidemenu'
    import Content from './content'
    import {changeMenu} from 'src/lib/actions'
    import {getFromLogin} from 'src/lib/getter'
    import {changeUser} from 'src/lib/actions'
    import {changeVersion} from 'src/lib/actions'

    export default {
        vuex: {
            getters: {
                fromLogin: getFromLogin,
            },
            actions: {
                changeMenu,
                changeUser,
                changeVersion,
            }
        },
        data: function () {
            return {
                ysMenuData: [
                    {
                        name: "服务支持",
                        link: "company",
                        topic: "service_support",
                        children: [
                            {
                                name: "服务支持",
                                icon: "ys-icon icon-menu-support",
                                topic: "support",
                                children: [
                                    {name: "公司管理", link: "company", menu: "company-mgt", topic: "company-mgt"},
                                    {name: "用户管理", link: "user-mgt", menu: "user-mgt", topic: "user-mgt"},
                                    {name: "消息管理", link: "message-all", menu: "message-mgt", topic: "message-mgt"},
                                    {
                                        name: "工单管理",
                                        link: "workorder-apply",
                                        menu: "workorder-mgt",
                                        topic: "workorder-mgt"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        name: "系统管理",
                        link: "",
                        topic: "system",
                        children: [
                            {
                                name: "全局设置",
                                icon: "ys-icon icon-menu-info-overview",
                                topic: "global",
                                children: [
                                    {name: '基本信息', link: 'base-info', menu: 'base-info', topic: "base-info"},
                                    {name: '菜单管理', link: 'menu-mgt', menu: 'menu-mgt', topic: "menu-mgt"},
                                ]
                            },
                            {
                                name: "管理设置",
                                icon: "ys-icon icon-menu-user",
                                topic: "manage",
                                children: [
                                    {name: "管理员管理", link: "admin-mgt", menu: "admin-mgt", topic: "admin-mgt"},
                                    {
                                        name: "权限管理",
                                        link: "permissions-mgt",
                                        menu: "permissions-mgt",
                                        topic: "permissions-mgt"
                                    },
                                ]
                            },
                            {
                                name: '系统设置',
                                icon: 'ys-icon icon-menu-system',
                                topic: 'system',
                                children: [
                                    {name: '访问设置', link: 'visit', menu: 'visit', topic: "access"},
                                    {name: '财务设置', link: 'finance', menu: 'finance', topic: "finance"},
                                    {name: '邮件设置', link: 'email-smtp', menu: 'email', topic: "email"},
                                    {
                                        name: '短信设置',
                                        link: 'message-setting',
                                        menu: 'message-setting',
                                        topic: "message-setting"
                                    },
                                    {name: '接口设置', link: 'api-setting', menu: 'api-setting', topic: "api-setting"},
                                ]
                            },
                            {
                                name: '安全设置',
                                icon: 'ys-icon icon-menu-lock',
                                topic: 'security',
                                children: [
                                    {
                                        name: '系统安全',
                                        link: 'two-validation',
                                        menu: 'system-safe',
                                        topic: "system-security"
                                    },
                                ]
                            },
                            {
                                name: '集中管理',
                                icon: 'ys-icon icon-menu-jizhong',
                                topic: 'node',
                                children: [
                                    {name: '级联控制', link: 'node-control', menu: 'node-control', topic: "node-control"},
                                    {name: '级联状态', link: 'node-state-topo', menu: 'node-state', topic: "node-state"},
                                    {
                                        name: '系统资源',
                                        link: 'system-resource',
                                        menu: 'system-resource',
                                        topic: "system-resource"
                                    },
                                    {
                                        name: '系统健康',
                                        link: 'system-health',
                                        menu: 'system-health',
                                        topic: "system-health"
                                    },
                                ]
                            },
                            {
                                name: "安全响应",
                                icon: "ys-icon icon-menu-domain",
                                topic: "system-action",
                                children: [
                                    {
                                        name: "响应配置",
                                        link: "system-action-alert",
                                        menu: "system-action-alert",
                                        topic: "system-action-alert"
                                    }
                                ]
                            },
                            {
                                name: '系统升级',
                                icon: 'ys-icon icon-menu-upgrade',
                                topic: 'upgrade',
                                children: [
                                    {name: '升级管理', link: 'upgrade-mgt', menu: 'upgrade-mgt', topic: "system-upgrade"},
                                ]
                            },
                            {
                                name: '日志审计',
                                icon: 'ys-icon icon-menu-log',
                                topic: 'log',
                                children: [
                                    {name: '机房登陆', link: 'admin-login', menu: 'admin-login', topic: "admin-login"},
                                    {
                                        name: '机房操作',
                                        link: 'admin-operation',
                                        menu: 'admin-operation',
                                        topic: "admin-operation"
                                    },
                                    {name: '用户登陆', link: 'user-login', menu: 'user-login', topic: "user-login"},
                                    {
                                        name: '用户操作',
                                        link: 'user-operation',
                                        menu: 'user-operation',
                                        topic: "user-operation"
                                    },
                                    {name: '数据备份', link: 'backup-mgt', menu: 'backup-mgt', topic: "backup-mgt"},
                                ]
                            },
                        ]
                    },
                    {
                        name: "安全运维",
                        link: "",
                        topic: "op",
                        children: [
                            {
                                name: "知识库",
                                icon: "ys-icon icon-menu-user-tree",
                                topic: "op-knowledge",
                                children: [
                                    {
                                        name: '知识库管理',
                                        link: 'knowledge-mgt',
                                        menu: 'knowledge-mgt',
                                        topic: "op-knowledge-mgt"
                                    },
                                ]
                            },
                            {
                                name: "漏洞库",
                                icon: "ys-icon icon-menu-system-warn",
                                topic: "op-hole",
                                children: [
                                    {name: '漏洞管理', link: 'hole-mgt', menu: 'hole-mgt', topic: "op-hole-mgt"},
                                ]
                            },
                            {
                                name: "预案库",
                                icon: "ys-icon icon-menu-topo",
                                topic: "op-plan",
                                children: [
                                    {name: '预案管理', link: 'plan-mgt', menu: 'plan-mgt', topic: "op-plan-mgt"},
                                ]
                            },
                            {
                                name: "SM词库",
                                icon: "ys-icon icon-menu-keyword",
                                topic: "op-sm",
                                children: [
                                    {name: 'SM词管理', link: 'sm-mgt', menu: 'sm-mgt', topic: "op-sm-mgt"},
                                ]
                            },
                            {
                                name: "安全规则",
                                icon: "ys-icon icon-menu-setting",
                                topic: "op-sr",
                                children: [
                                    {name: '安全规则管理', link: 'sr-mgt', menu: 'sr-mgt', topic: "op-sr-mgt"},
                                ]
                            },
                            {
                                name: "工作日",
                                icon: "ys-icon icon-menu-domain",
                                topic: "op-wd",
                                children: [
                                    {name: '工作日管理', link: 'wd-mgt', menu: 'wd-mgt', topic: "op-wd-mgt"},
                                ]
                            }
                        ]
                    },
                    {
                        name: "态势感知",
                        link: "",
                        topic: "ssa",
                        children: [
                            {
                                name: "全局态势",
                                icon: "ys-icon icon-menu-home",
                                topic: "ssa-global-config",
                                children: [
                                    {
                                        name: '全局态势数据',
                                        link: 'new-global',
                                        menu: 'ssa-global',
                                        topic: "ssa-global"
                                    },
                                ]
                            },
                            {
                                name: "资源态势",
                                icon: "ys-icon icon-menu-data-source",
                                topic: "ssa-source-config",
                                children: [
                                    {
                                        name: '资源态势数据',
                                        link: 'ssa-source',
                                        menu: 'ssa-source',
                                        topic: "ssa-source"
                                    },
                                ]
                            },
                            {
                                name: "业务态势",
                                icon: "ys-icon icon-menu-data-source",
                                topic: "ssa-business-config",
                                children: [
                                    {
                                        name: '业务态势数据',
                                        link: 'ssa-business',
                                        menu: 'ssa-business',
                                        topic: "ssa-business"
                                    },
                                ]
                            },
                            {
                                name: "安全态势",
                                icon: "ys-icon icon-menu-defense",
                                topic: "ssa-security-config",
                                children: [
                                    {
                                        name: '安全态势数据',
                                        link: 'ssa-security',
                                        menu: 'ssa-security',
                                        topic: "ssa-security"
                                    },
                                ]
                            },
                            {
                                name: "专家分析",
                                icon: "ys-icon icon-menu-expert",
                                topic: "ssa-experts-analysis",
                                children: [
                                    {
                                        name: '规则管理',
                                        link: 'ssa-experts-analysis-rule-manage',
                                        menu: 'ssa-experts-analysis-rule-manage',
                                        topic: "ssa-experts-analysis-rule-manage"
                                    },
                                ]
                            },
                            {
                                name: "态势预警管理",
                                icon: "ys-icon icon-menu-bell",
                                topic: "ssa-warning",
                                children: [
                                    {
                                        name: '预警管理',
                                        link: 'ssa-warning-mgt',
                                        menu: 'ssa-warning-mgt',
                                        topic: "ssa-warning-mgt"
                                    },
                                ]
                            },
                            {
                                name: "定制图表",
                                icon: "ys-icon icon-menu-handmade",
                                topic: "ssa-chart",
                                children: [
                                    {
                                        name: '创建图表',
                                        link: 'ssa-new-chart',
                                        menu: 'ssa-new-chart',
                                        topic: "ssa-new-chart"
                                    },
                                    {
                                        name: '图表管理',
                                        link: 'ssa-chart-manage',
                                        menu: 'ssa-chart-manage',
                                        topic: "ssa-chart-manage"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        name: "深度扫描",
                        link: "",
                        topic: "scan",
                        children: [
                            {
                                name: "扫描搜索",
                                icon: "ys-icon icon-menu-ip",
                                topic: "scan-ip",
                                children: [
                                    {
                                        name: '扫描搜索筛选',
                                        link: 'scan-search',
                                        menu: 'scan-search',
                                        topic: "scan-ip-mgt"
                                    },
                                ]
                            },
                            {
                                name: "扫描任务",
                                icon: "ys-icon icon-menu-info-overview",
                                topic: "scan-task",
                                children: [
                                    {
                                        name: '扫描任务数据',
                                        link: 'scan-task',
                                        menu: 'scan-task',
                                        topic: "scan-task-mgt"
                                    },
                                ]
                            },
                            {
                                name: "扫描配置",
                                icon: "ys-icon icon-menu-system",
                                topic: "scan-conf",
                                children: [
                                    {
                                        name: '扫描引擎',
                                        link: 'scan-conf',
                                        menu: 'scan-conf',
                                        topic: "scan-conf-mgt"
                                    },
                                ]
                            },
                        ]
                    },
                    {
                        name: "数据管理",
                        link: "",
                        topic: "dama",
                        children: [
                            {
                                name: '数据管理',
                                icon: 'ys-icon icon-menu-dashboard',
                                topic: 'dama-config',
                                children: [
                                    {name: '数据管理', link: 'dama-mgt', menu: 'dama-mgt', topic: 'dama-mgt'},
                                    //  { name: '数据预览', link: 'dama-preview',menu:"dama-preview",topic:'dama-preview'}
                                ]
                            }
                        ]
                    },
                    {
                        name: "数据报告",
                        link: "",
                        topic: "data-report",
                        children: [
                            {
                                name: "数据报告",
                                icon: "ys-icon icon-menu-file",
                                topic: "data-report-config",
                                children: [
                                    {
                                        name: '创建报告模板',
                                        link: 'create-data-report-template',
                                        menu: 'create-report-template',
                                        topic: "create-report-template"
                                    },
                                    {
                                        name: '模板管理',
                                        link: 'data-report-template-mgt',
                                        menu: 'template-mgt',
                                        topic: "data-report"
                                    },
                                    {name: '报告管理', link: 'data-report-mgt', menu: 'report-mgt', topic: "report-mgt"},
                                ]
                            }
                        ]
                    },
                    {
                        name: "事件检测",
                        link: "",
                        topic: "event-detect",
                        children: [
                            {
                                name: "安全事件",
                                icon: "ys-icon icon-menu-search",
                                topic: "security-event",
                                children: [
                                    {
                                        name: '事件搜索',
                                        link: 'analysis-event-search',
                                        menu: 'analysis-event-search',
                                        topic: "analysis-event-search"
                                    },
                                    {name: '日志搜索', link: 'event-search', menu: 'event-search', topic: "event-search"},
                                    {name: '告警事件', link: 'event-warn', menu: 'event-warn', topic: "event-warn"},
                                ]
                            }
                        ]
                    },
                    {
                        name: "事件时间线",
                        link: "",
                        topic: "event-detect",
                        children: [
                            {
                                name: "事件时间线",
                                icon: "ys-icon icon-menu-topo",
                                topic: "security-event-time",
                                children: [
                                    {
                                        name: '事件时间线',
                                        link: 'event-timeline',
                                        menu: 'event-timeline',
                                        topic: "event-timeline"
                                    }
                                ]
                            }
                        ]
                    },
                ],
                landingUrl: "",
                userInfo: {}
            }
        },
        ready() {
            this.getMenuData();
            this.getUserInfo();
            this.getVersionData();
        },
        components: {
            Topbar,
            SideMenu,
            Content
        },
        methods: {
            getVersionData() {
                this.$http.get('/api/system/version').then(function (response) {
                    this.changeVersion(response.data)
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getUserInfo() {
                this.$http.get('/api/profile').then(function (response) {
                    this.userInfo = response.data.data;
                    this.changeUser(response.data.data)
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            change() {
                this.$refs.side.topic = this.$refs.top.topic
            },
            getMenuData() {
                this.$http.get('/api/system/menus').then(function (response) {
                    if (response.data.status == 200) {
                        let memoryData = response.data.data.default;
                        let ysData = this.ysMenuData;
                        for (let x in ysData) {
                            for (let y in memoryData) {
                                if (ysData[x].topic == memoryData[y].topic) {
                                    if (memoryData[y].topic == 'home') {
                                        this.landingUrl = 'home'
                                    }
                                    for (let menu1 in ysData[x].children) {
                                        for (let menu2 in memoryData[y].children) {
                                            if (ysData[x].children[menu1].topic == memoryData[y].children[menu2].topic) {
                                                memoryData[y].children[menu2].icon = ysData[x].children[menu1].icon
                                                for (let list1 in ysData[x].children[menu1].children) {
                                                    for (let list2 in memoryData[y].children[menu2].children) {
                                                        if (ysData[x].children[menu1].children[list1].topic == memoryData[y].children[menu2].children[list2].topic) {
                                                            memoryData[y].children[menu2].children[list2].link = ysData[x].children[menu1].children[list1].link
                                                            memoryData[y].children[menu2].children[list2].menu = ysData[x].children[menu1].children[list1].menu
                                                            if (memoryData[y].children[menu2].children[list2].is_landing == 1) {
                                                                this.landingUrl = ysData[x].children[menu1].children[list1].link;
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        this.changeMenu(memoryData);
                        this.$root.loadStatus = true;
                        let self = this;
                        setTimeout(function () {
                            self.$root.loadStatus = false;
                        }, 2000)
                        if (this.fromLogin) {
                            this.$router.go({name: this.landingUrl})
                        }
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
        }
    }

</script>
