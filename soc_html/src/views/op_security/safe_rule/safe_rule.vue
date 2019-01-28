<style lang="less" scoped>
    .con-left {
        left: 0px;
        top: 0px;
        bottom: 0px;
        width: 218px;
        position: absolute;
        background: rgba(0, 0, 0, 0.15)
    }

    .con-right {
        margin-left: 233px;
    }

    .check {
        background: #4a92ff;
        & > a {
            color: #fff !important;
        }
    }
</style>
<template>
    <div class="ys-box">
        <div class="pos-r">
            <div class="con-left">
                <div class="ys-box-title">
                    <tooltip :content="'新增'" :delay="1000">
                        <a class="m-r-10" @click="addRule"><i class="ys-icon icon-add-circle"></i></a>
                    </tooltip>
                    <tooltip :content="'编辑'" :delay="1000">
                        <a class="m-r-10" @click="editRule"><i class="ys-icon icon-edit"></i></a>
                    </tooltip>
                    <ys-poptip confirm
                               :title=`您确认删除${ruleTitle}？`
                               :placement="'right'"
                               @on-ok="delRule"
                               @on-cancel="">
                        <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
                    </ys-poptip>
                </div>
                <ul class="con p-t-10">
                    <li class="p-l-10" style="overflow: hidden;text-overflow:ellipsis;white-space: nowrap;" :class="{check:ruleStatus == '1'&& list.id == ruleId}"
                        v-for="list in ruleList" :key="list.id">
                        <div class="ys-search d-i-b"
                             v-if="(ruleStatus == '3' && list.id == ruleId) || (ruleStatus == '2' && list.type == '0')">
                            <input type="text" v-model="list.value" placeholder="输入安全规则"
                                   @keyup.enter="saveRule(list.value)"
                                   class="ys-input" style="width:200px;"/>
                            <button class="ys-search-btn" style="right: 22px;width: 20px" @click="saveRule(list.value)">
                                <i
                                        class="ys-icon icon-check-circle"></i>
                            </button>
                            <button class="ys-search-btn" style="width: 20px" @click="cancelRule(list.value)"><i
                                    class="ys-icon icon-clear-circle"></i>
                            </button>
                        </div>
                        <a :title="list.value" class="tool-box p-l-10" v-else @click="checkRule(list.id,list.value)">{{list.value}}</a>
                    </li>
                </ul>
            </div>
            <div class="con-right ys-box-con ys-wrap">
                <div>
                    <div class="ys-search d-i-b">
                        <input type="text" placeholder="输入规则名称查询"
                               v-model="searchValue"
                               @keyup.enter="tableRe"
                               class="ys-input" style="width:180px;"/>
                        <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
                    </div>
                    <div class="fRight">
                        <button class="ys-btn ys-btn-blue m-r-5" @click="add"><i class="ys-icon icon-add-circle"></i>添加
                        </button>
                        <button class="ys-btn ys-btn-red m-r-5" @click="del('all')"><i class="ys-icon icon-trash"></i>删除
                        </button>
                        <button class="ys-btn ys-btn-op m-r-5" @click="start('all')"><i class="ys-icon icon-play"></i>启用
                        </button>
                        <button class="ys-btn ys-btn-op-white" @click="pause('all')"><i class="ys-icon icon-pause"></i>停用
                        </button>
                    </div>
                </div>
                <table class="ys-table m-t-10">
                    <thead>
                    <tr>
                        <th>
                            <checkbox :show.sync="allSelected"></checkbox>
                        </th>
                        <th>名称</th>
                        <th>描述</th>
                        <th>状态</th>
                        <th>创建时间</th>
                        <th>扫描间隔/范围</th>
                        <th>立即执行</th>
                        <th>操作</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-bind:class="[$index%2==1 ? 'even' : 'odd' ]" v-for="list in tableList">
                        <td>
                            <checkbox :show.sync="list.selected"></checkbox>
                        </td>
                        <td>{{list.rule_name}}</td>
                        <td>{{list.description}}</td>
                        <td v-if="list.status==-1" class="ys-error-color">停用</td>
                        <td v-else class="ys-success-color">启用</td>
                        <td>{{list.create_time}}</td>
                        <td>
                            <div v-if="list.time_type == 1">{{list.interval}}(分钟)</div>
                            <div v-if="list.time_type == 2">{{list.time_start}}~{{list.time_end}}</div>
                        </td>
                        <td>
                            <span v-if="list.status==-1 || list.time_type == 1" class="ys-white-color disabled">立即执行</span>
                            <a v-else @click="run(list.id)">立即执行</a>
                        </td>
                        <td>
                            <tooltip :content="'编辑'" :delay="1000">
                                <a @click="showEdit(list)" class="m-r-10"><i class="ys-icon icon-edit"></i></a>
                            </tooltip>
                            <ys-poptip confirm
                                       title="您确认删除此条规则？"
                                       :placement="'left'"
                                       @on-ok="del('one',list.id)"
                                       @on-cancel="">
                                <a class="ys-error-color m-r-10"><i class="ys-icon icon-trash"></i></a>
                            </ys-poptip>
                            <tooltip :content="'启用'" :delay="1000">
                                <a class="ys-success-color m-r-10" @click="start('one',list.id)"><i
                                        class="ys-icon icon-play"></i></a>
                            </tooltip>
                            <tooltip :content="'停用'" :delay="1000">
                                <a class="ys-error-color" @click="pause('one',list.id)"><i
                                        class="ys-icon icon-pause"></i></a>
                            </tooltip>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table-data :url='tableUrl'
                            :data.sync="tableList"
                            :filter.sync="tableFliter"
                            :search.sync="searchValue"
                            v-ref:table></table-data>
            </div>
        </div>
        <aside :show.sync="configStatus"
               :header="configHead"
               :left="'auto'"
               :width="'800px'">
            <safe-rule-add v-if="configStatus" :id="id" :group-id="ruleId" @cancel="cancel"></safe-rule-add>
        </aside>
    </div>
</template>
<script>
    import tableData from 'src/components/table-data.vue'
    import aside from 'src/components/Aside.vue'
    import safeRuleAdd from './safe-rule-add.vue'
    import Api from 'src/lib/api'

    export default {
        name: 'safe_rule',
        props: {},
        data() {
            return {
                tableUrl: '/api/op_store/alarm_rule/dts',
                tableList: [],
                tableFliter: {
                    group_id: {id: '-1'},
                },
                searchValue: '',
                configStatus: false,
                configHead: '添加规则',
                id: '',
                ruleStatus: 0, //1、选中；2、新增 3、编辑
                ruleId: '',
                ruleTitle: '',
                ruleList: [],
            };
        },
        computed: {
            allSelected: {
                get: function () {
                    if (this.tableList.length == 0) {
                        return false
                    }
                    return this.tableList.reduce(function (prev, curr) {
                        return prev && curr.selected;
                    }, true);
                },
                set: function (newValue) {
                    this.tableList.forEach(function (list) {
                        list.selected = newValue;
                    });
                }
            }
        },
        ready() {
            this.init();
            this.scroll();
        },
        methods: {
            scroll() {
                $(".con").slimScroll({
                    height: '620',
                    position: 'right',
                    size: "5px",
                    color: '#4a92ff',
                    opacity: 0.8,
                })
            },
            init() {
                this.$http.post('/api/op_store/group_rule/dts', {}).then(function (response) {
                    if (response.data.status == 200) {
                        let arr = [];
                        response.data.data.map((value) => {
                            arr.unshift({
                                id: value.id,
                                value: value.group_name,
                                type: '1'
                            })
                        })
                        this.ruleList = [].concat(arr);
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },//获取列表
            tableRe() {
                if (!this.isChoice()) return;
                this.tableFliter.group_id.id = this.ruleId
                this.$refs.table.Re()
            },
            addRule() {
                let rule = JSON.stringify(this.ruleList);
                if (rule.indexOf('"id":"-1"') != -1) return false
                this.ruleStatus = 2;
                this.ruleList.unshift({
                    id: '-1',
                    value: '',
                    type: '0',
                })
            },
            saveAdd(value) {
                this.$http.post('/api/op_store/group_rule', {
                    group_name: value,
                }).then(function (response) {
                    this.$root.errorMsg = response.data.msg;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true
                        this.ruleStatus = 1;
                        // this.clearSet()
                        this.init();
                    } else {
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },
            cancelRule() {
                this.ruleStatus = 1;
                // this.clearSet();
                this.init();
            },
            editRule() {
                this.ruleStatus = 3;
            },//编辑树
            saveEdit(value) {
                this.$http.put(`/api/op_store/group_rule/${this.ruleId}`, {
                    group_name: value,
                }).then(function (response) {
                    this.$root.errorMsg = response.data.msg;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true
                        this.ruleStatus = 1;
                        // this.clearSet()
                        this.init();
                    } else {
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },//编辑保存
            delRule() {
                this.$http.delete(`/api/op_store/group_rule/${this.ruleId}`, {}).then(function (response) {
                    this.$root.errorMsg = response.data.msg;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true
                        this.clearSet();
                        this.init();
                        this.tableFliter.group_id.id = '-1';
                        this.$refs.table.Re()
                    } else {
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },//删除规则
            checkRule(id, value) {
                this.ruleStatus = 1;
                this.ruleId = id;
                this.ruleTitle = value;
                this._del_new();
                this.tableFliter.group_id.id = this.ruleId
                this.$refs.table.Re();
            },//选中规则
            _del_new() {
                if (this.ruleList[0].id == -1) this.ruleList.splice(0, 1);
            },//选中其他节点、删除第一个新增框
            saveRule(value) {
                if (!value) {
                    this.$root.alertError = true
                    this.$root.errorMsg = '规则名称不能为空';
                    return false;
                }
                if (this.ruleStatus == 3) {
                    this.saveEdit(value);
                } else if (this.ruleStatus == 2) {
                    this.saveAdd(value);
                }
            },
            showEdit(list) {
                this.configStatus = true;
                this.configHead = `修改${list.rule_name}规则`;
                this.id = list.id
            },
            add() {
                if (!this.isChoice()) return;
                this.configStatus = true;
                this.configHead = '添加规则';
                this.id = '';
            },
            del(type, id) {
                if (!this.isChoice()) return;
                let str = type == 'one' ? String(id) : this.getCheckIds().length ? this.getCheckIds().join(',') : '';
                if (!str) {
                    this.$root.errorMsg = '请最少选择一条数据';
                    this.$root.alertError = true
                    return false;
                }
                this.$http.delete('/api/op_store/alarm_rule', {
                    ids: str
                }).then(function (response) {
                    this.$root.errorMsg = response.data.msg;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true
                        this.tableRe();
                    } else {
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },
            start(type, id) {
                if (!this.isChoice()) return;
                let str = type == 'one' ? String(id) : this.getCheckIds().length ? this.getCheckIds().join(',') : '';
                if (!str) {
                    this.$root.errorMsg = '请最少选择一条数据';
                    this.$root.alertError = true
                    return false;
                }
                this.$http.post('/api/op_store/alarm_rule/start', {
                    ids: str
                }).then(function (response) {
                    this.$root.errorMsg = response.data.msg;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true
                        this.tableRe();
                    } else {
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },//开启
            run(id) {
                this.$http.post('/api/op_store/alarm_rule/run', {
                    id: String(id)
                }).then(function (response) {
                    this.$root.errorMsg = response.data.msg;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true
                        this.tableRe();
                    } else {
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },//立即执行
            pause(type, id) {
                if (!this.isChoice()) return;
                let str = type == 'one' ? String(id) : this.getCheckIds().length ? this.getCheckIds().join(',') : '';
                if (!str) {
                    this.$root.errorMsg = '请最少选择一条数据';
                    this.$root.alertError = true
                    return false;
                }
                this.$http.post('/api/op_store/alarm_rule/stop', {
                    ids: str
                }).then(function (response) {
                    this.$root.errorMsg = response.data.msg;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true
                        this.tableRe();
                    } else {
                        this.$root.alertError = true
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },//暂停
            isChoice() {
                if (!this.ruleId) {
                    this.$root.errorMsg = '请先选择左侧规则';
                    this.$root.alertError = true
                    return false;
                } else {
                    return true;
                }
            },
            clearSet() {
                this.ruleId = '';
                this.ruleStatus = 0;
                this.ruleTitle = ''
            },
            getCheckIds() {
                let arr = [];
                this.tableList.map((value) => {
                    if (value.selected) {
                        arr.push(value.id)
                    }
                })
                return arr;
            },
            cancel() {
                this.configStatus = false;
                this.tableRe();
            }
        },
        components: {
            tableData,
            aside,
            safeRuleAdd
        }
    };
</script>