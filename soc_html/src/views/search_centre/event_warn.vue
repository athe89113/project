<style lang="less" scoped>
    .ys-error-color > a:hover, .ys-error-color > a:active {
        color: #e96157 !important;
    }
</style>
<template>
    <div class="clearfix">
        <div class="ys-box fLeft" style="width: 420px">
            <div class="clearfix">
                <div class="fLeft" style="width: 202px">
                    <div class="ys-box-title">告警类型</div>
                    <div class="ys-box-con warn_type" style="padding: 0px;">
                        <table class="ys-table ys-success-color">
                            <thead>
                            <tr>
                                <th>类型</th>
                                <th>告警次数</th>
                                <th>攻击IP数</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="list in warnType">
                                <td>
                                    <div :title="list.group_name"
                                         style="max-width: 100px;overflow: hidden;text-overflow:ellipsis;white-space: nowrap;">
                                        <a :class="{'ys-error-color':group_name == list.group_name && load}"
                                           @click="checkType(list.group_name)">{{list.group_name}}</a>
                                    </div>
                                </td>
                                <td>{{list.count_}}</td>
                                <td>{{list.src_count}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="fRight" style="width: 202px">
                    <div class="ys-box-title">告警监测</div>
                    <div class="ys-box-con warn_test" style="padding: 0px;">
                        <table class="ys-table">
                            <thead>
                            <tr>
                                <th>规则名称</th>
                                <th>告警次数</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="list in warnTest">
                                <td><a :class="{'ys-error-color':rule_name == list.rule_name && load}"
                                       @click="checkRule(list)">{{list.rule_name}}</a></td>
                                <td>{{list.count_}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="ys-box-title m-t-15">告警源</div>
                    <div class="ys-box-con warn_source" style="padding: 0px;">
                        <table class="ys-table">
                            <thead>
                            <tr>
                                <th>源IP</th>
                                <th>告警次数</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="list in warnSource">
                                <td><a :class="{'ys-error-color':src_ip == list.src_ip}"
                                       @click="checkSource(list)">{{list.src_ip}}</a></td>
                                <td>{{list.count_}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="m-t-15">
                <div class="ys-box-title">告警趋势</div>
                <div class="ys-box-con">
                    <line-chart
                            :id="'warn-line'"
                            :height="'240px'"
                            :name="lineData.name"
                            :x="lineData.x"
                            :series="lineData.series">
                    </line-chart>
                </div>
            </div>
        </div>
        <div class="" style="margin-left: 435px">
            <div class="ys-box-title">
                <span>告警列表</span>
            </div>
            <div class="ys-box-con ys-wrap">
                <div class="textR">
                    <span class="m-r-5">风险级别</span>
                    <ys-select
                            :option="eventLevelList"
                            :selected.sync="tableFliter.alarm_level"
                            :width="130">
                    </ys-select>
                    <div class="ys-search d-i-b m-l-5">
                        <input type="text" placeholder="输入关键词查询"
                               v-model="searchValue"
                               @keyup.enter="tableRe"
                               class="ys-input" style="width:130px;"/>
                        <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
                    </div>
                    <button class="ys-btn m-r-5 m-l-5" @click="tableRe()">查询</button>
                    <button class="ys-btn ys-btn-blue" @click="closeWarn('all')">关闭告警</button>
                </div>
                <table class="ys-table m-t-10">
                    <thead>
                    <tr>
                        <th>
                            <checkbox :show.sync="allSelected"></checkbox>
                        </th>
                        <th>源IP</th>
                        <th>源端口</th>
                        <th>告警时间</th>
                        <th>目标IP</th>
                        <th>目标端口</th>
                        <th>告警类型</th>
                        <th>风险级别</th>
                        <th>告警安全设备IP</th>
                        <th>操作</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-bind:class="[$index%2==1 ? 'even' : 'odd' ]" v-for="list in tableList">
                        <td>
                            <checkbox :show.sync="list.selected"></checkbox>
                        </td>
                        <td>{{list.src_ip}}</td>
                        <td>{{list.src_port}}</td>
                        <td>{{list.alarm_time}}</td>
                        <td>{{list.dst_ip}}</td>
                        <td>{{list.dst_port}}</td>
                        <td>
                            <div :title="list.group_name"
                                 style="max-width: 80px;overflow: hidden;text-overflow:ellipsis;white-space: nowrap;">
                                <span>{{list.group_name}}</span>
                            </div>
                        </td>
                        <td>{{level[list.alarm_level]}}</td>
                        <td>{{list.event_host}}</td>
                        <td>
                            <a v-if="list.status == 1" @click="closeWarn('one',list.id)">关闭</a>
                            <span v-else class="ys-white-color">已关闭</span>
                            <a class="m-l-5" @click="view(list)">日志</a>
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
               :header="'原始日志'"
               :left="'auto'"
               :width="'800px'">
            <table class="ys-table">
                <thead>
                <tr>
                    <th>事件接受时间</th>
                    <th>设备IP</th>
                    <th>原始日志</th>
                </tr>
                </thead>
                <tbody>
                <tr v-bind:class="[$index%2==1 ? 'even' : 'odd' ]" v-for="list in tableListAside">
                    <td>{{list.stastic_time}}</td>
                    <td>{{list.event_host}}</td>
                    <td>{{list.event_detail}}</td>
                </tr>
                </tbody>
            </table>
            <table-data :url='tableUrlAside'
                        :data.sync="tableListAside"
                        :filter.sync="tableFliterAside"
                        v-ref:aside></table-data>
        </aside>
    </div>
</template>
<script>
    import Api from 'src/lib/api'

    export default {
        name: 'event_warn',
        props: {},
        data() {
            return {
                tableUrl: '/api/op_store/alarm_list/dts',
                tableList: [],
                tableFliter: {
                    group_name: {id: ''},
                    rule_name: {id: ''},
                    src_ip: {id: ''},
                    alarm_level: {id: ''},
                },
                searchValue: '',
                lineData: {
                    name: ['告警趋势'],
                    x: '',
                    series: '',
                },
                level: {
                    '1': '严重',
                    '2': '重大',
                    '3': '次要',
                    '4': '警告',
                },
                eventLevelList: [{
                    id: 1, name: '严重'
                }, {
                    id: 2, name: '重大'
                }, {
                    id: 3, name: '次要'
                }, {
                    id: 4, name: '警告'
                }],
                group_name: '',
                rule_name: '',
                src_ip: '',
                warnType: [],    //告警类型
                warnTest: [],    //告警检测
                warnSource: [],  //告警源
                configStatus: false,
                tableUrlAside: '/api/op_store/alarm_log/dts',
                tableListAside: [],
                tableFliterAside: {
                    id: {id: ''},
                },
                load: false,
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
            tableRe() {
                this.tableFliter.group_name['id'] = this.group_name;
                this.tableFliter.rule_name['id'] = this.rule_name;
                this.tableFliter.src_ip['id'] = this.src_ip;
                this.$refs.table.Re()
            },
            scroll() {
                $('.warn_type').slimScroll({
                    height: '360px',
                    position: 'right',
                    size: "5px",
                    color: 'black',
                    opcity: 0.5
                })
                $('.warn_test').slimScroll({
                    height: '153px',
                    position: 'right',
                    size: "5px",
                    color: 'black',
                    opcity: 0.5
                })
                $('.warn_source').slimScroll({
                    height: '152px',
                    position: 'right',
                    size: "5px",
                    color: 'black',
                    opcity: 0.5
                })
            },
            get_alarm_type() {
                return new Promise((resolve) => {
                    this.$http.post('/api/op_store/alarm_type', {}).then(function (response) {
                        if (response.data.status == 200) {
                            this.warnType = response.data.data;
                            this.group_name = response.data.data.length ? response.data.data[0]['group_name'] : ''
                            resolve()
                        } else {
                            this.$root.errorMsg = response.data.msg;
                            this.$root.alertError = true
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    });
                })
            },
            get_alarm_monitor() {
                return new Promise((resolve) => {
                    this.$http.post('/api/op_store/alarm_monitor', {
                        group_name: this.group_name,
                    }).then(function (response) {
                        if (response.data.status == 200) {
                            response.data.data.map((value) => {
                                value.group_name = this.group_name;
                            })
                            this.warnTest = response.data.data;
                            this.rule_name = response.data.data.length ? response.data.data[0]['rule_name'] : ''
                            resolve()
                        } else {
                            this.$root.errorMsg = response.data.msg;
                            this.$root.alertError = true
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    });
                })
            },
            get_alarm_source() {
                return new Promise((resolve) => {
                    this.$http.post('/api/op_store/alarm_source', {
                        group_name: this.group_name,
                        rule_name: this.rule_name,
                    }).then(function (response) {
                        if (response.data.status == 200) {
                            response.data.data.map((value) => {
                                value.group_name = this.group_name;
                                value.rule_name = this.rule_name;
                            })
                            this.warnSource = response.data.data;
                            this.src_ip = response.data.data.length ? response.data.data[0]['src_ip'] : ''
                            resolve()
                        } else {
                            this.$root.errorMsg = response.data.msg;
                            this.$root.alertError = true
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    });
                })
            },
            get_alarm_trend() {
                return new Promise((resolve) => {
                    this.$http.post('/api/op_store/alarm_trend', {
                        group_name: this.group_name,
                        rule_name: this.rule_name,
                        src_ip: this.src_ip,
                    }).then(function (response) {
                        if (response.data.status == 200) {
                            let x = [], y = [];
                            response.data.data.map((value) => {
                                x.push(value.days)
                                y.push(value.count_)
                            });
                            this.lineData.x = [].concat(x);
                            this.lineData.series = [{
                                data: y
                            }];
                            resolve()
                        } else {
                            this.$root.errorMsg = response.data.msg;
                            this.$root.alertError = true
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    });
                })
            },
            init() {
                Promise.all([this.get_alarm_type()]).then((result) => {
                    Promise.all([this.get_alarm_monitor()]).then((result) => {
                        Promise.all([this.get_alarm_source()]).then((result) => {
                            this.group_name = '';
                            this.rule_name = '';
                            this.src_ip = '';
                            this.load = true;
                            this.$http.post('/api/op_store/alarm_trend', {}).then(function (response) {
                                if (response.data.status == 200) {
                                    let x = [], y = [];
                                    response.data.data.map((value) => {
                                        x.push(value.days)
                                        y.push(value.count_)
                                    });
                                    this.lineData.x = [].concat(x);
                                    this.lineData.series = [{
                                        data: y
                                    }];
                                } else {
                                    this.$root.errorMsg = response.data.msg;
                                    this.$root.alertError = true
                                }
                            }, function (response) {
                                Api.user.requestFalse(response, this);
                            });
                        })
                    })
                })
            },
            checkType(type) {
                this.group_name = type;
                this.load = false;
                Promise.all([this.get_alarm_monitor()]).then((result) => {
                    Promise.all([this.get_alarm_source()]).then((result) => {
                        this.rule_name = '';
                        this.src_ip = '';
                        this.load = true;
                        this.get_alarm_trend();
                        this.tableRe();
                    })
                })
            },
            checkRule(list) {
                this.group_name = list.group_name;
                this.rule_name = list.rule_name;
                Promise.all([this.get_alarm_source()]).then((result) => {
                    this.src_ip = '';
                    this.get_alarm_trend();
                    this.tableRe();
                })
            },
            checkSource(list) {
                this.group_name = list.group_name;
                this.rule_name = list.rule_name;
                this.src_ip = list.src_ip;
                this.get_alarm_trend();
                this.tableRe();
            },
            view(list) {
                this.configStatus = true;
                this.tableFliterAside.id.id = list.id;
                this.$refs.aside.Re()
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
            closeWarn(type, id) {
                let str = type == 'one' ? String(id) : this.getCheckIds().length ? this.getCheckIds().join(',') : '';
                if (!str) {
                    this.$root.errorMsg = '请最少选择一条数据';
                    this.$root.alertError = true
                    return false;
                }
                this.$http.post('/api/op_store/alarm_log/stop', {
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
            }
        },
        components: {}
    };
</script>