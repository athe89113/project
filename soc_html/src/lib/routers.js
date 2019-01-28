//公共功能
import Index from '../views/index.vue'
import Login from '../views/login.vue'
import SSOLogin from '../views/sso-login.vue'
// 着陆页
import Home from '../views/home.vue'
import UI from '../views/ui.vue'
import Example from '../views/example.vue'

//支持管理
import UserMgt from "../views/service_support/user/user-mgt.vue"
import UserAdd from "../views/service_support/user/user-add.vue"
import UserEdit from "../views/service_support/user/user-edit.vue"
import WorkorderMgt from "../views/service_support/workorder-mgt.vue"
import WorkorderAdd from "../views/service_support/workorder/workorder-add.vue"
import WorkorderDeal from "../views/service_support/workorder/deal-mgt.vue"
import WorkorderDealInfo from "../views/service_support/workorder/deal-info-mgt.vue"
import WorkorderApply from "../views/service_support/workorder/apply-mgt.vue"
import Message from "../views/service_support/message-mgt.vue"
import MessageAll from "../views/service_support/message/all.vue"
import MessageAssets from "../views/service_support/message/assets.vue"
import MessageSecurity from "../views/service_support/message/security.vue"
import MessageMoitor from "../views/service_support/message/monitor.vue"
import MessageOther from "../views/service_support/message/other.vue"
import Company from "../views/service_support/company/company-mgt.vue"
import CompanyAdd from "../views/service_support/company/company-add.vue"
import CompanyEdit from "../views/service_support/company/company-edit.vue"
import CompanyUser from "../views/service_support/company/company-user.vue"
import CompanyUserAdd from "../views/service_support/company/company-user-add.vue"

//商务购买模块
import ShopCart from "../views/business/shop-cart.vue"
import OrderMgt from "../views/business/order-mgt.vue"
import InvoiceApply from "../views/business/invoice-apply.vue"

//系统设置模块
import BaseInfo from "../views/system/base-info/base-info.vue"
import MenuMgt from "../views/system/global_setting/menu-mgt.vue"
import AdminMgt from "../views/system/manage_setting/admin-mgt.vue"
import PermissionsMgt from "../views/system/manage_setting/permissions-mgt.vue"
import NodeControl from "../views/system/centralized-mgt/node-control.vue"
import NodeState from "../views/system/centralized-mgt/node-state.vue"
import NodeStateParent from "../views/system/centralized-mgt/node-state-parent.vue"
import NodeStateChildren from "../views/system/centralized-mgt/node-state-children.vue"
import NodeStateTopo from "../views/system/centralized-mgt/node-state-topo.vue"
import Finance from '../views/system/finance-setting/finance.vue'
import Email from '../views/system/email/email.vue'
import EmailCloud from '../views/system/email/email-cloud.vue'
import EmailSmtp from '../views/system/email/email-smtp.vue'
import MessageSetting from '../views/system/message/message-setting.vue'
import ApiSetting from '../views/system/api/api-setting.vue'
import SystemResource from '../views/system/resource/index.vue'
import SystemHealth from '../views/system/health/index.vue'
import UpgradeMgt from '../views/system/upgrade/upgrade-mgt.vue'
import BackupMgt from '../views/system/soclog/backup-mgt.vue'
import AdminLogin from '../views/system/soclog/admin/login.vue'
import AdminOperation from '../views/system/soclog/admin/operation.vue'
import UserLogin from '../views/system/soclog/user/login.vue'
import UserOperation from '../views/system/soclog/user/operation.vue'
import Visit from '../views/system/visit/visit.vue'
import SystemSafe from '../views/system/safe/SystemSafe.vue'
import BlackList from '../views/system/safe/black-list.vue'
import WhiteList from '../views/system/safe/white-list.vue'
import TwoValidation from '../views/system/safe/two-validation.vue'
import SystemActionAlert from "../views/system/action/index.vue"

//安全运维
import CreateOpKnowledge from "../views/op_security/knowledge-data/knowledge-add.vue"
import OpKnowledgeMgt from "../views/op_security/knowledge-data/knowledge-mgt.vue"
import OpKnowledgeDetail from "../views/op_security/knowledge-data/knowledge-detail.vue"
import OpKnowledgeEdit from "../views/op_security/knowledge-data/knowledge-edit.vue"
import CreateOpHole from "../views/op_security/hole_data/hole-add.vue"
import OpHoleMgt from "../views/op_security/hole_data/hole-mgt.vue"
import OpHoleDetail from "../views/op_security/hole_data/hole-detail.vue"
import OpHoleScore from "../views/op_security/hole_data/hole-score.vue"
import OpPlanMgt from "../views/op_security/plan_data/plan-mgt.vue"
import OpPlanAdd from "../views/op_security/plan_data/plan-add.vue"
import OpPlanDetail from "../views/op_security/plan_data/plan-detail.vue"
import OpPlanEdit from "../views/op_security/plan_data/plan-edit.vue"
import OpSmMgt from "../views/op_security/sm/sm-mgt.vue"
import OpWdMgt from "../views/op_security/work_day/wd_mgt.vue"
import OpSafeRule from "../views/op_security/safe_rule/safe_rule.vue"

// 系统管理
import Upgrade from "../views/upgrade.vue"
//态势感知
import SsaGlobal from "../views/ssa/global/ssa-global"
import NewGlobal from "../views/ssa/newglobal/new-global"
import SsaSource from "../views/ssa/source/ssa-source"
import SsaBusiness from "../views/ssa/business/ssa-business"
import SsaSecurity from "../views/ssa/security/ssa-security"
import SsaRuleManage from "../views/ssa/experts_analysis/rule_manage"
import SsaWarningMgt from "../views/ssa/warning/warning_mgt"
import SsaNewChart from '../views/ssa/chart/SsaNewChart';
import SsaChartManage from '../views/ssa/chart/SsaChartManage';
//数据管理
import DamaDataMgt from "../views/data_manage/data_mgt"
import DamaDataPreview from "../views/data_manage/data_preview"

//数据报告
import CreateDataReportTemplate from "../views/data_report/create_template"
import DataReportTemplateMgt from "../views/data_report/template_mgt"
import DataReportMgt from "../views/data_report/report_mgt"

//事件检测
import SecurityEventSearch from "../views/search_centre/event_search"
import SecurityEventTimeLine from "../views/search_centre/event-timeline"
import SecurityAnalysisEventSearch from "../views/search_centre/analysis_event_search"
import SecurityEventWarn from "../views/search_centre/event_warn"

//探测扫描
import scnSearch from "../views/scn/search.vue"
import scnTaskResult from "../views/scn/task_result.vue"
import scnTask from "../views/scn/task.vue"
import scnScan from "../views/scn/conf.vue"

export default function (router) {
    router.map({
        '/dp': {
            name: 'index',
            component: Index,
            subRoutes: {
                '/home': {
                    name: 'home',
                    component: Home,
                    auth: true,
                    topic: "home"
                },// 安全运维
                '/op': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        'create-knowledge': {
                            name: 'create-knowledge',
                            component: CreateOpKnowledge,
                            auth: true,
                            topic: 'op',
                            menu: 'knowledge-mgt'
                        },
                        'knowledge-detail/:id': {
                            name: 'knowledge-detail',
                            component: OpKnowledgeDetail,
                            auth: true,
                            topic: 'op',
                            menu: 'knowledge-mgt'
                        },
                        'knowledge-edit/:id': {
                            name: 'knowledge-edit',
                            component: OpKnowledgeEdit,
                            auth: true,
                            topic: 'op',
                            menu: 'knowledge-mgt'
                        },
                        'knowledge-mgt': {
                            name: 'knowledge-mgt',
                            component: OpKnowledgeMgt,
                            auth: true,
                            topic: 'op',
                            menu: 'knowledge-mgt',
                        },
                        'create-hole': {
                            name: 'create-hole',
                            component: CreateOpHole,
                            auth: true,
                            topic: 'op',
                            menu: 'hole-mgt'
                        },
                        'hole-mgt': {
                            name: 'hole-mgt',
                            component: OpHoleMgt,
                            auth: true,
                            topic: 'op',
                            menu: 'hole-mgt',
                        },
                        'hole-detail/:id': {
                            name: 'hole-detail',
                            component: OpHoleDetail,
                            auth: true,
                            topic: 'op',
                            menu: 'hole-mgt'
                        },
                        'hole-score/:id': {
                            name: 'hole-score',
                            component: OpHoleScore,
                            auth: true,
                            topic: 'op',
                            menu: 'hole-detail/:id'
                        },
                        'plan-mgt': {
                            name: 'plan-mgt',
                            component: OpPlanMgt,
                            auth: true,
                            topic: 'op',
                            menu: 'plan-mgt',
                        },
                        'plan-add': {
                            name: 'plan-add',
                            component: OpPlanAdd,
                            auth: true,
                            topic: 'op',
                            menu: 'plan-mgt'
                        },
                        'plan-edit/:id': {
                            name: 'plan-edit',
                            component: OpPlanEdit,
                            auth: true,
                            topic: 'op',
                            menu: 'plan-mgt'
                        },
                        'plan-detail/:id': {
                            name: 'plan-detail',
                            component: OpPlanDetail,
                            auth: true,
                            topic: 'op',
                            menu: 'plan-mgt'
                        },
                        'sm-mgt': {
                            name: 'sm-mgt',
                            component: OpSmMgt,
                            auth: true,
                            topic: 'op',
                            menu: 'sm-mgt',
                        },
                        'wd-mgt': {
                            name: 'wd-mgt',
                            component: OpWdMgt,
                            auth: true,
                            topic: 'op',
                            menu: 'wd-mgt',
                        },
                        'sr-mgt': {
                            name: 'sr-mgt',
                            component: OpSafeRule,
                            auth: true,
                            topic: 'op',
                            menu: 'sr-mgt',
                        }
                    }
                },
                '/scan': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        'search': {
                            name: 'scan-search',
                            component: scnSearch,
                            auth: true,
                            topic: 'scan',
                            menu: 'scan-search'
                        },
                        'task': {
                            name: 'scan-task',
                            component: scnTask,
                            auth: true,
                            topic: 'scan',
                            menu: 'scan-task'
                        },
                        'task-result': {
                            name: 'scan-task-result',
                            component: scnTaskResult,
                            auth: true,
                            topic: 'scan',
                            menu: 'scan-task'
                        },
                        'conf': {
                            name: 'scan-conf',
                            component: scnScan,
                            auth: true,
                            topic: 'scan',
                            menu: 'scan-conf'
                        },
                    }
                },
                '/ssa': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        'global': {
                            name: 'ssa-global',
                            component: SsaGlobal,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-global'
                        },
                        'new-global': {
                            name: 'new-global',
                            component: NewGlobal,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-global'
                        },
                        'source': {
                            name: 'ssa-source',
                            component: SsaSource,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-source'
                        },
                        'business': {
                            name: 'ssa-business',
                            component: SsaBusiness,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-business'
                        },
                        'security': {
                            name: 'ssa-security',
                            component: SsaSecurity,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-security'
                        },
                        'experts-analysis-rule-manage': {
                            name: 'ssa-experts-analysis-rule-manage',
                            component: SsaRuleManage,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-experts-analysis-rule-manage'
                        },
                        'warning': {
                            name: 'ssa-warning-mgt',
                            component: SsaWarningMgt,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-warning-mgt'
                        },
                        'new-chart': { //创建图表
                            name: 'ssa-new-chart',
                            component: SsaNewChart,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-new-chart'
                        },
                        'chart-manage': { // 图表管理
                            name: 'ssa-chart-manage',
                            component: SsaChartManage,
                            auth: true,
                            topic: 'ssa',
                            menu: 'ssa-chart-manage'
                        }
                    }
                },
                '/dama-config': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        'dama-mgt': {
                            name: 'dama-mgt',
                            component: DamaDataMgt,
                            auth: true,
                            topic: 'dama',
                            menu: 'dama-mgt'
                        },
                        // 'dama-preview': {
                        //   name: 'dama-preview',
                        //   component: DamaDataPreview,
                        //   auth: true,
                        //   topic: 'dama',
                        //   menu: 'dama-preview'
                        // },
                    }
                },
                '/data-report': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        '/create-data-report-template/:id': {
                            name: 'create-data-report-template',
                            component: CreateDataReportTemplate,
                            auth: true,
                            topic: 'data-report',
                            menu: 'create-report-template'
                        },
                        '/data-report-template-mgt': {
                            name: 'data-report-template-mgt',
                            component: DataReportTemplateMgt,
                            auth: true,
                            topic: 'data-report',
                            menu: 'template-mgt'
                        },
                        '/data-report-mgt': {
                            name: 'data-report-mgt',
                            component: DataReportMgt,
                            auth: true,
                            topic: 'data-report',
                            menu: 'report-mgt'
                        },
                    },
                },
                '/event-detect': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        '/analysis-event-search': {
                            name: 'analysis-event-search',
                            component: SecurityAnalysisEventSearch,
                            auth: true,
                            topic: 'event-detect',
                            menu: 'analysis-event-search'
                        },
                        '/event-search': {
                            name: 'event-search',
                            component: SecurityEventSearch,
                            auth: true,
                            topic: 'event-detect',
                            menu: 'event-search'
                        },
                        '/event-timeline': {
                            name: 'event-timeline',
                            component: SecurityEventTimeLine,
                            auth: true,
                            topic: 'event-detect',
                            menu: 'analysis-event-search'
                        },
                        '/event-warn': {
                            name: 'event-warn',
                            component: SecurityEventWarn,
                            auth: true,
                            topic: 'event-detect',
                            menu: 'event-warn'
                        },
                    },
                },
                '/example': {
                    name: 'example',
                    component: Example,
                    auth: true
                },//服务支持
                '/support': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        // 公司
                        'company': {
                            name: 'company',
                            component: Company,
                            auth: true,
                            topic: 'service_support',
                            menu: 'company-mgt'
                        },
                        'company-add': {
                            name: 'company-add',
                            component: CompanyAdd,
                            auth: true,
                            topic: 'service_support',
                            menu: 'company-mgt'
                        },
                        'company/:company_id': {
                            name: 'company-edit',
                            component: CompanyEdit,
                            auth: true,
                            topic: 'service_support',
                            menu: 'company-mgt'
                        },
                        'company-user/:company_id': {
                            name: 'company-user',
                            component: CompanyUser,
                            auth: true,
                            topic: 'service_support',
                            menu: 'company-mgt'
                        },
                        'company-user-add/:company_id': {
                            name: 'company-user-add',
                            component: CompanyUserAdd,
                            auth: true,
                            topic: 'service_support',
                            menu: 'company-mgt'
                        },// 用户
                        '/user-mgt': {
                            name: 'user-mgt',
                            component: UserMgt,
                            auth: true,
                            topic: 'service_support',
                            menu: 'user-mgt'
                        },
                        '/user-add': {
                            name: 'user-add',
                            component: UserAdd,
                            auth: true,
                            topic: 'service_support',
                            menu: 'user-mgt'
                        },
                        '/user/:user_id': {
                            name: 'user-edit',
                            component: UserEdit,
                            auth: true,
                            topic: 'service_support',
                            menu: 'user-mgt'
                        },
                        '/workorder-mgt': {
                            name: 'workorder-mgt',
                            component: WorkorderMgt,
                            subRoutes: {
                                '/': {
                                    name: 'workorder-deal',
                                    component: WorkorderDeal,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'workorder-mgt'
                                },
                                '/deal': {
                                    name: 'workorder-deal',
                                    component: WorkorderDeal,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'workorder-mgt'
                                },
                                '/apply/:type': {
                                    name: 'workorder-apply',
                                    component: WorkorderApply,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'workorder-mgt'
                                },
                            }
                        },
                        '/message': {
                            name: 'message',
                            component: Message,
                            subRoutes: {
                                '/': {
                                    name: 'message-all',
                                    component: MessageAll,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'message-mgt'
                                },
                                '/all': {
                                    name: 'message-all',
                                    component: MessageAll,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'message-mgt'
                                },
                                '/assets': {
                                    name: 'message-assets',
                                    component: MessageAssets,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'message-mgt'
                                },
                                '/security': {
                                    name: 'message-security',
                                    component: MessageSecurity,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'message-mgt'
                                },
                                '/monitor': {
                                    name: 'message-monitor',
                                    component: MessageMoitor,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'message-mgt'
                                },
                                '/other': {
                                    name: 'message-other',
                                    component: MessageOther,
                                    auth: true,
                                    topic: 'service_support',
                                    menu: 'message-mgt'
                                }
                            }
                        },
                        '/workorder-add': {
                            name: 'workorder-add',
                            component: WorkorderAdd,
                            auth: true,
                            topic: 'service_support',
                            menu: 'workorder-mgt'
                        },
                        '/workorder-mgt/deal-info/:order_id/:target': {
                            name: 'workorder-deal-info',
                            component: WorkorderDealInfo,
                            auth: true,
                            topic: 'service_support',
                            menu: 'workorder-mgt'
                        },
                    }
                },
                //系统管理
                '/system': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        // 全局设置
                        'health': {
                            name: 'system-health',
                            component: SystemHealth,
                            auth: true,
                            topic: 'system',
                            menu: 'system-health'
                        },
                        'action-alert': {
                            name: 'system-action-alert',
                            component: SystemActionAlert,
                            auth: true,
                            topic: 'system',
                            menu: 'system-action-alert'
                        },
                        'resource': {
                            name: 'system-resource',
                            component: SystemResource,
                            auth: true,
                            topic: 'system',
                            menu: 'system-resource'
                        },
                        'base-info': {
                            name: 'base-info',
                            component: BaseInfo,
                            auth: true,
                            topic: 'system',
                            menu: 'base-info'
                        },
                        'finance': {
                            name: 'finance',
                            component: Finance,
                            auth: true,
                            topic: 'system',
                            menu: 'finance'
                        },
                        'email': {
                            name: 'email',
                            component: Email,
                            subRoutes: {
                                '/': {
                                    name: 'email-smpt',
                                    component: EmailSmtp,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'email'
                                },
                                '/smtp': {
                                    name: 'email-smtp',
                                    component: EmailSmtp,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'email'
                                },
                                '/cloud': {
                                    name: 'email-cloud',
                                    component: EmailCloud,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'email'
                                },
                            }
                        },
                        'system-safe': {
                            name: 'system-safe',
                            component: SystemSafe,
                            subRoutes: {
                                '/': {
                                    name: 'two-validation',
                                    component: TwoValidation,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'system-safe'
                                },
                                '/black': {
                                    name: 'black-list',
                                    component: BlackList,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'system-safe'
                                },
                                '/white': {
                                    name: 'white-list',
                                    component: WhiteList,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'system-safe'
                                },
                                '/validation': {
                                    name: 'two-validation',
                                    component: TwoValidation,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'system-safe'
                                },
                            }
                        },
                        'user-login': {
                            name: 'user-login',
                            component: UserLogin,
                            auth: true,
                            topic: 'system',
                            menu: 'user-login'
                        },
                        'user-operation': {
                            name: 'user-operation',
                            component: UserOperation,
                            auth: true,
                            topic: 'system',
                            menu: 'user-operation'
                        },
                        'admin-operation': {
                            name: 'admin-operation',
                            component: AdminOperation,
                            auth: true,
                            topic: 'system',
                            menu: 'admin-operation'
                        },
                        'visit': {
                            name: 'visit',
                            component: Visit,
                            auth: true,
                            topic: 'system',
                            menu: 'visit'
                        },
                        'admin-login': {
                            name: 'admin-login',
                            component: AdminLogin,
                            auth: true,
                            topic: 'system',
                            menu: 'admin-login'
                        },
                        'api-setting': {
                            name: 'api-setting',
                            component: ApiSetting,
                            auth: true,
                            topic: 'system',
                            menu: 'api-setting'
                        },
                        'message-setting': {
                            name: 'message-setting',
                            component: MessageSetting,
                            auth: true,
                            topic: 'system',
                            menu: 'message-setting'
                        },
                        'menu-mgt': {
                            name: 'menu-mgt',
                            component: MenuMgt,
                            auth: true,
                            topic: 'system',
                            menu: 'menu-mgt'
                        },
                        'admin-mgt': {
                            name: 'admin-mgt',
                            component: AdminMgt,
                            auth: true,
                            topic: 'system',
                            menu: 'admin-mgt'
                        },
                        'permissions-mgt': {
                            name: 'permissions-mgt',
                            component: PermissionsMgt,
                            auth: true,
                            topic: 'system',
                            menu: 'permissions-mgt'
                        },
                        'node-control': {
                            name: 'node-control',
                            component: NodeControl,
                            auth: true,
                            topic: 'system',
                            menu: 'node-control'
                        },
                        'node-state': {
                            name: 'node-state',
                            component: NodeState,
                            subRoutes: {
                                '/': {
                                    name: 'node-state-parent',
                                    component: NodeStateParent,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'node-state'
                                },
                                '/parent': {
                                    name: 'node-state-parent',
                                    component: NodeStateParent,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'node-state'
                                },
                                '/children': {
                                    name: 'node-state-children',
                                    component: NodeStateChildren,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'node-state'
                                },
                                '/topo': {
                                    name: 'node-state-topo',
                                    component: NodeStateTopo,
                                    auth: true,
                                    topic: 'system',
                                    menu: 'node-state'
                                },
                            },
                        },
                        'backup-mgt': {
                            name: 'backup-mgt',
                            component: BackupMgt,
                            auth: true,
                            topic: 'system',
                            menu: 'backup-mgt'
                        },
                        'upgrade-mgt': {
                            name: 'upgrade-mgt',
                            component: UpgradeMgt,
                            auth: true,
                            topic: 'system',
                            menu: 'upgrade-mgt'
                        },
                    }
                },
                //服务购买
                '/business': {
                    component: {template: '<router-view></router-view>'},
                    subRoutes: {
                        //订单中心
                        'shop-cart': {
                            name: 'shop-cart',
                            component: ShopCart,
                            auth: true,
                            topic: 'business',
                            menu: 'shop-cart'
                        },
                        'order-mgt': {
                            name: 'order-mgt',
                            component: OrderMgt,
                            auth: true,
                            topic: 'business',
                            menu: 'order-mgt'
                        },//发票管理
                        '/invoice-apply': {
                            name: 'invoice-apply',
                            component: InvoiceApply,
                            auth: true,
                            topic: 'business',
                            menu: 'invoice-apply'
                        },
                    }
                },
                '/upgrade': {
                    name: 'upgrade',
                    component: Upgrade,
                    auth: true
                },
                '/ui': {
                    name: 'ui',
                    component: UI,
                    auth: true
                },
            }
        },
        '/login': {name: 'login', component: Login},
        '/sso/login/:base_str': {name: 'sso-login', component: SSOLogin},
    });
    router.redirect({
        '/': '/dp/ssa/new-global',//'*': '/soc/home'
    })
};
