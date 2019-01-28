<template>
    <div class="ys-con pos-r">
        <div class="ys-box-con">
            <p>用户可查询、查看已定制的报表模版，及报告生成周期，为用户提供相关管理操作。</p>
        </div>

        <ul class="ys-nav m-t-10">
            <li v-for="list in typeData" @click="clickType(list.id)">
                <a :class="curIndex == list.id ? 'on' : ''">
                    <span class="ys-nav-cor"></span>
                    <span class="text">{{list.name}}</span>
                </a>
            </li>
            <div class="clearfix"></div>
        </ul>
        <div class="ys-box-con ys-wrap">
            <div class="tool-box">
                <div class="fLeft d-i-b">
                    <button v-if="curIndex == 1" class="ys-btn" @click="createTemp()"><i
                            class="ys-icon icon-add-circle"></i>定制新模板
                    </button>
                    <span class="verticalM m-l-10">已有报告模板<span
                            class="ys-success-color m-l-5 m-r-5">{{tableTotal}}</span>个</span>
                </div>
                <div class="ys-search d-i-b m-l-10 fRight">
                    <input type="text" placeholder="输入关键词查询"
                           v-model="searchValue"
                           @blur="tableRe()"
                           @keyup.enter="tableRe()"
                           class="ys-input" style="width:180px;"/>
                    <button class="ys-search-btn" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
                </div>
            </div>
            <table class="ys-table m-t-10" v-if="curIndex == 1">
                <thead>
                <tr>
                    <th>模板名称</th>
                    <th>图表数</th>
                    <th>生成周期</th>
                    <th>操作</th>
                </tr>
                </thead>
                <tbody v-for="list in tableList">
                <tr v-bind:class="[curEditId == list.id ? 'on' : '' ]">
                    <td>{{list.name}}</td>
                    <td>{{list.count}}</td>
                    <td>{{list.schedule_time}}</td>
                    <td class="operate">
                        <tooltip :content="'周期'" :delay="0">
                            <a @click="showEditCycle(list)"><i class="ys-icon icon-clock"></i></a>
                        </tooltip>
                        <tooltip :content="'历史'" :delay="0">
                            <a @click="showHistory(list)"><i class="ys-icon icon-eye"></i></a>
                        </tooltip>
                        <tooltip :content="'立即生成'" :delay="0">
                            <a @click="makeReport(list)"><i class="ys-icon icon-play"></i></a>
                        </tooltip>
                        <tooltip :content="'编辑'" :delay="1000">
                            <a @click="showEdit(list)"><i class="ys-icon icon-edit"></i></a>
                        </tooltip>
                        <ys-poptip confirm
                                   title="您确认删除此模板吗？"
                                   :placement="'left'"
                                   @on-ok="delTempalte(list)"
                                   @on-cancel="">
                            <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
                        </ys-poptip>
                    </td>
                </tr>
                </tbody>
            </table>
            <table class="ys-table m-t-10" v-if="curIndex == 2 || curIndex == 3">
                <thead>
                <tr>
                    <th>模板名称</th>
                    <th>生成周期</th>
                    <th>操作</th>
                </tr>
                </thead>
                <tbody v-for="list in tableList">
                <tr v-bind:class="[curEditId == list.id ? 'on' : '' ]">
                    <td :class="[(list.id == 11 || list.id == 12)?'ys-success-color':'']">{{list.name}}</td>
                    <td>{{list.schedule_time}}</td>
                    <td class="operate">
                        <tooltip :content="'周期'" :delay="0">
                            <a @click="showEditCycle(list)"><i class="ys-icon icon-clock"></i></a>
                        </tooltip>
                        <tooltip :content="'历史'" :delay="0">
                            <a @click="showHistory(list)"><i class="ys-icon icon-eye"></i></a>
                        </tooltip>
                        <ys-poptip v-if="list.id == 11 || list.id == 12" :placement="'left'"
                                   :confirm="true" @on-ok="makeReport(list,'day')" :title="'请选择时间范围（默认最近一个月）'">
                            <div slot="content">
                                <div class="m-t-10">
                                    <span class="ys-info-color m-r-5 verticalM">起始时间：</span>
                                    <calendar :type="'date'"
                                              :value.sync="start_day"
                                              :place="'right'"
                                              :text="'选择起始时间'"></calendar>
                                </div>
                                <div class="m-t-10">
                                    <span class="ys-info-color m-r-5 verticalM">终止时间：</span>
                                    <calendar :type="'date'"
                                              :place="'right'"
                                              :value.sync="end_day"
                                              :text="'选择终止时间'"></calendar>
                                </div>
                            </div>
                            <a><i class="ys-icon icon-play"></i></a>
                        </ys-poptip>
                        <tooltip v-else :content="'立即生成'" :delay="0">
                            <a @click="makeReport(list)"><i class="ys-icon icon-play"></i></a>
                        </tooltip>
                    </td>
                </tr>
                </tbody>
            </table>
            <table-data :url='tableUrl'
                        :whole.sync="tableTotal"
                        :data.sync="tableList"
                        :filter.sync="tableFilter"
                        :search.sync="searchValue"
                        v-ref:table></table-data>
        </div>
        <aside :show.sync="showConfigStatus"
               :header="configHead"
               :width="'800px'"
               :left="'auto'">
            <div>
                <div class="ys-box-con ys-info-color">在这里您可以查看该模版生成的历史报表记录</div>
                <table class="ys-table m-t-10">
                    <thead>
                    <tr>
                        <th>名称</th>
                        <th>生成时间</th>
                        <th style="width:180px;" class="textC">操作</th>
                    </tr>
                    </thead>
                    <tbody v-for="list in hisTableList">
                    <tr>
                        <td>{{list.name}}</td>
                        <td>{{list.create_time}}</td>
                        <td class="textC">
                            <tooltip :content="'.doc下载'" :delay="0">
                                <!--<a @click="downReportFile(list)"><i class="ys-icon icon-cloud-download"></i></a>-->
                                <!--<a @click="downReportFile(list)"><i class="ys-icon icon-cloud-download"></i></a>-->
                                <a :href="'/api/ssa/report/download/docx/'+ list.id" class="ys-success-color"
                                   download="report"><i class="ys-icon icon-cloud-download"></i></a>
                            </tooltip>
                            <tooltip :content="'.pdf下载'" class="m-l-10" :delay="0">
                                <a :href="'/api/ssa/report/download/pdf/'+ list.id" download="report"><i
                                        class="ys-icon icon-cloud-download"></i></a>
                            </tooltip>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <table-data :url="hisTableUrl"
                            :data.sync="hisTableList"
                            :filter.sync="hisTableFilter"
                            :search.sync="hisSearchValue"
                            v-ref:histable>
                </table-data>
            </div>
            <div class="aside-foot m-t-20">
                <button class="ys-btn ys-btn-white" @click="showConfigStatus=false">取消返回</button>
            </div>
        </aside>
        <aside :show.sync="showCycleStatus"
               :header="cycleHead"
               :width="'800px'"
               :left="'auto'">
            <div>
                <div class="ys-box-con ys-info-color">报告模版：默认月度总和统计报告</div>
                <div class="ys-box-con m-t-10">
                    <table class="ys-form-table">
                        <tr>
                            <td>扫描方式：</td>
                            <td>
                                <ys-select
                                        :option="scheduleTypeList"
                                        :selected.sync="curScheduleType"
                                        :width="140"></ys-select>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2" v-if="curScheduleType.id==1">您选择了<span class="ys-success-color">立即生成</span>
                            </td>
                            <td colspan="2" v-if="curScheduleType.id==2">您选择了<span class="ys-success-color">生成一次</span>，生成时间为：
                            </td>
                            <td colspan="2" v-if="curScheduleType.id==3">您选择了<span class="ys-success-color">周期生成</span>，生成时间为：
                            </td>
                        </tr>
                        <tr v-if="curScheduleType.id==2">
                            <td colspan="2">
                                <calendar :type="'date'" :text="'选择日期'" :value.sync="schedule_start_date"></calendar>
                                <calendar :type="'time'" :text="'选择时间'" :value.sync="schedule_time"
                                          class="m-l-10"></calendar>
                            </td>
                        </tr>
                        <tr v-if="curScheduleType.id==3">
                            <td colspan="2">
                                <ys-select :option="periodList" :selected.sync="curPeriod"></ys-select>
                                <span class="m-l-5 m-r-5">的</span>
                                <ys-select v-if="curPeriod.id==4" :option="weekList" :selected.sync="curWeek"
                                           :width="100"></ys-select>
                                <ys-select v-if="curPeriod.id==5" :option="monthList" :selected.sync="curMonth"
                                           :width="100"></ys-select>
                                <span v-if="curPeriod.id==5" class="m-l-5 m-r-5">号</span>
                                <span v-if="curPeriod.id==6">
                <ys-select :option="quarterList" :selected.sync="curQuarter" :width="100"></ys-select>
                <ys-select :option="monthList" :selected.sync="curMonth" :width="100"></ys-select>
                <span class="m-l-5 m-r-5">号</span>
              </span>
                                <span v-if="curPeriod.id==7">
                <ys-select :option="yearList" :selected.sync="curYear" :width="100"></ys-select>
                <ys-select :option="monthList" :selected.sync="curMonth" :width="100"></ys-select>
                <span class="m-l-5 m-r-5">号</span>
              </span>
                                <calendar :type="'time'" :text="'选择时间'" :value.sync="schedule_time"
                                          class="m-l-5"></calendar>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            <div class="aside-foot m-t-20">
                <button class="ys-btn m-r-10" @click="saveCycle()">保存周期</button>
                <button class="ys-btn ys-btn-white" @click="showCycleStatus=false">取消返回</button>
            </div>
        </aside>
    </div>
</template>
<style scoped>

</style>
<script>
    import Api from 'src/lib/api'

    let moment = require('moment')
    export default {
        name: "template-mgt",
        data() {
            return {
                tableUrl: "/api/ssa/report/template/dts",
                searchValue: "",
                tableList: "",
                tableFilter: {
                    template_type: {'id': 2},
                },
                tableTotal: 0,
                showConfigStatus: false,
                configHead: "",
                hisTableUrl: '',
                hisTableList: [],
                hisSearchValue: "",
                hisTableFilter: {},
                showCycleStatus: false,
                cycleHead: "",
                scheduleTypeList: [
                    {id: 1, name: "立即生成"},
                    {id: 2, name: "生成一次"},
                    {id: 3, name: "周期生成"},
                ],
                curScheduleType: {id: 1, name: "立即生成"},
                periodList: [
                    {id: 3, name: "每天"},
                    {id: 4, name: "每周"},
                    {id: 5, name: "每月"},
                    {id: 6, name: "每季度"},
                    {id: 7, name: "每年"},
                ],
                curDay: 1,
                curPeriod: {id: 3, name: "每天"},
                // 选择日期
                startDateSel: {},
                // 选择时间
                startTimeSel: {},
                curWeek: {id: "1", name: "星期一"},
                weekList: [
                    {id: "1", name: "星期一"},
                    {id: "2", name: "星期二"},
                    {id: "3", name: "星期三"},
                    {id: "4", name: "星期四"},
                    {id: "5", name: "星期五"},
                    {id: "6", name: "星期六"},
                    {id: "7", name: "星期天"},
                ],
                curMonth: {id: "1", name: "1"},
                monthList: [
                    {id: "1", name: "1"},
                    {id: "2", name: "2"},
                    {id: "3", name: "3"},
                    {id: "4", name: "4"},
                    {id: "5", name: "5"},
                    {id: "6", name: "6"},
                    {id: "7", name: "7"},
                    {id: "8", name: "8"},
                    {id: "9", name: "9"},
                    {id: "10", name: "10"},
                    {id: "11", name: "11"},
                    {id: "12", name: "12"},
                    {id: "13", name: "13"},
                    {id: "14", name: "14"},
                    {id: "15", name: "15"},
                    {id: "16", name: "16"},
                    {id: "17", name: "17"},
                    {id: "18", name: "18"},
                    {id: "19", name: "19"},
                    {id: "20", name: "20"},
                    {id: "21", name: "21"},
                    {id: "22", name: "22"},
                    {id: "23", name: "23"},
                    {id: "24", name: "24"},
                    {id: "25", name: "25"},
                    {id: "26", name: "26"},
                    {id: "27", name: "27"},
                    {id: "28", name: "28"},
                    {id: "29", name: "29"},
                    {id: "30", name: "30"}
                ],
                quarterList: [
                    {id: 1, name: "第一个月"},
                    {id: 2, name: "第二个月"},
                    {id: 3, name: "第三个月"}
                ],
                curQuarter: {id: 1, name: "第一个月"},
                yearList: [
                    {id: 1, name: "01月"},
                    {id: 2, name: "02月"},
                    {id: 3, name: "03月"},
                    {id: 4, name: "04月"},
                    {id: 5, name: "05月"},
                    {id: 6, name: "06月"},
                    {id: 7, name: "07月"},
                    {id: 8, name: "08月"},
                    {id: 9, name: "09月"},
                    {id: 10, name: "10月"},
                    {id: 11, name: "11月"},
                    {id: 12, name: "12月"}
                ],
                curYear: {id: 1, name: "01月"},
                schedule_start_date: "",
                schedule_time: "",
                editId: 0,
                typeData: [{
                    id: 2, name: '终端安全检查模版'
                }, {
                    id: 3, name: '安全审计模版'
                }, {
                    id: 1, name: '定制模版'
                },],
                curIndex: 2,
                start_day: '',
                end_day: '',
            }
        },
        compiled(){
            if (this.$route.query.tag == 3) {
                this.curIndex = 1;
                this.tableFilter.template_type.id = 1;
            }
        },
        ready() {
            this.end_day = moment().format('YYYY-MM-DD');
            this.start_day = moment().add(-30, 'days').format('YYYY-MM-DD')
        },
        methods: {
            clickType(id) {
                this.curIndex = id;
                this.tableFilter.template_type.id = id;
                this.end_day = moment().format('YYYY-MM-DD');
                this.start_day = moment().add(-30, 'days').format('YYYY-MM-DD')
                this.tableRe();
            },
            createTemp() {
                this.$router.go({name: "create-data-report-template"})
            },
            showHistory(list) {
                this.showConfigStatus = true;
                this.configHead = "查看模板生成的历史报表";
                this.reLog(list);
            },
            reLog(list) {
                this.hisTableFilter.template_id = {id: list.id, name: list.id};
                this.hisTableUrl = "/api/ssa/report/result/dts";
                this.hisTableRe(this.hisTableUrl)
            },
            hisTableRe(url) {
                this.$refs.histable.Re(url)
            },
            tableRe() {
                this.$refs.table.Re()
            },
            showEdit(list) {
                this.$router.go({
                    name: "create-data-report-template",
                    params: {
                        id: list.id
                    }
                })
            },
            delTempalte(list) {
                this.$root.loadStatus = true;
                this.$http.delete('/api/ssa/report/template/' + list.id).then(function (response) {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.tableRe();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            makeReport(list, day) {
                this.$root.loadStatus = true;
                let data = {};
                if (day === 'day') {
                    data['end_day'] = this.end_day;
                    data['start_day'] = this.start_day;
                }
                this.$http.post('/api/ssa/report/task/' + list.id + '/run',data).then(function (response) {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.tableRe();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            delReport(list) {
                this.$http.delete('/api/ssa/report/result/' + list.id).then(function (response) {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.tableRe();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            downReportFile(list) {
                window.open('/api/ssa/report/download/' + list.id)
            },
            showEditCycle(list) {
                this.editId = list.id;
                this.showCycleStatus = true;
                this.cycleHead = "设置生成周期";
                this.$http.get('/api/ssa/report/template/' + this.editId,).then(function (response) {
                    this.$root.loadStatus = false;
                    let data = response.data.data;

                    if (data.schedule_type == 1) {
                        this.curScheduleType = {id: 1, name: "立即生成"};
                    } else if (data.schedule_type == 2) {
                        this.curScheduleType = {id: 2, name: "生成一次"};
                        this.schedule_start_date = data.schedule_start_date;
                        this.schedule_time = data.schedule_time;
                    } else if (data.schedule_type == 3) {
                        this.curScheduleType = {id: 3, name: "周期生成"};
                        this.curPeriod = {id: 3, name: "每天"};
                        this.schedule_time = data.schedule_time;
                    } else if (data.schedule_type == 4) {
                        this.curScheduleType = {id: 3, name: "周期生成"};
                        this.curPeriod = {id: 4, name: "每周"};
                        for (let x in this.weekList) {
                            if (this.weekList[x].id == data.schedule_days) {
                                this.curWeek = this.weekList[x];
                            }
                        }
                        this.schedule_time = data.schedule_time;
                    } else if (data.schedule_type == 5) {
                        this.curScheduleType = {id: 3, name: "周期生成"};
                        this.curPeriod = {id: 5, name: "每月"};
                        for (let x in this.monthList) {
                            if (this.monthList[x].id == data.schedule_days) {
                                this.curMonth = this.monthList[x];
                            }
                        }
                        this.schedule_time = data.schedule_time;
                    } else if (data.schedule_type == 6) {
                        this.curScheduleType = {id: 3, name: "周期生成"};
                        this.curPeriod = {id: 6, name: "每季度"};
                        for (let x in this.monthList) {
                            if (this.monthList[x].id == data.schedule_days) {
                                this.curMonth = this.monthList[x];
                            }
                        }
                        for (let x in this.quarterList) {
                            if (this.quarterList[x].id == data.schedule_months) {
                                this.curQuarter = this.quarterList[x];
                            }
                        }
                        this.schedule_time = data.schedule_time;
                    } else if (data.schedule_type == 7) {
                        this.curScheduleType = {id: 3, name: "周期生成"};
                        this.curPeriod = {id: 7, name: "每年"};
                        for (let x in this.monthList) {
                            if (this.monthList[x].id == data.schedule_days) {
                                this.curMonth = this.monthList[x];
                            }
                        }
                        for (let x in this.yearList) {
                            if (this.yearList[x].id == data.schedule_months) {
                                this.curYear = this.yearList[x];
                            }
                        }
                        this.schedule_time = data.schedule_time;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            saveCycle() {
                let data = {};
                if (this.curScheduleType.id == 1) {
                    data.schedule_type = 1
                } else if (this.curScheduleType.id == 2) {
                    data.schedule_type = 2
                } else if (this.curScheduleType.id == 3) {
                    if (this.curPeriod.id == 3) {
                        data.schedule_type = 3
                    } else if (this.curPeriod.id == 4) {
                        data.schedule_type = 4
                        data.schedule_days = this.curWeek.id
                    } else if (this.curPeriod.id == 5) {
                        data.schedule_type = 5
                        data.schedule_days = this.curMonth.id
                    } else if (this.curPeriod.id == 6) {
                        data.schedule_type = 6
                        data.schedule_months = this.curQuarter.id
                        data.schedule_days = this.curMonth.id
                    } else if (this.curPeriod.id == 7) {
                        data.schedule_type = 7
                        data.schedule_months = this.curYear.id
                        data.schedule_days = this.curMonth.id
                    }
                }
                if (data.schedule_type != 1) {
                    data.schedule_time = this.schedule_time
                    data.schedule_start_date = this.schedule_start_date
                } else {
                    data.schedule_time = this.getCurDateTime()[1];
                    data.schedule_start_date = this.getCurDateTime()[0];
                }
                this.$http.put('/api/ssa/report/template/' + this.editId, data).then(function (response) {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.showCycleStatus = false;
                        this.tableRe();
                    } else {
                        this.$root.alertError = true
                    }
                    this.$root.errorMsg = response.data.msg
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getCurDateTime() {
                let time = new Date();//获取系统当前时间
                let year = time.getFullYear();
                let month = time.getMonth() + 1;
                let date = time.getDate();//系统时间月份中的日
                let day = time.getDay();//系统时间中的星期值

                let hour = time.getHours();
                let minutes = time.getMinutes();
                let seconds = time.getSeconds();
                if (month < 10) {
                    month = "0" + month;
                }
                if (date < 10) {
                    date = "0" + date;
                }
                if (hour < 10) {
                    hour = "0" + hour;
                }
                if (minutes < 10) {
                    minutes = "0" + minutes;
                }
                if (seconds < 10) {
                    seconds = "0" + seconds;
                }
                let dateStr = year + "-" + month + "-" + date;
                let timeStr = hour + ":" + minutes + ":" + seconds;
                let dateTime = [dateStr, timeStr];
                return dateTime;
            },
        },
        watch:{
            'end_day': function () {
                if (new Date(this.start_day).getTime() > new Date(this.end_day).getTime()) {
                    let time = this.end_day;
                    this.end_day = this.start_day;
                    this.start_day = time;
                }
            },
            'start_day': function () {
                if (new Date(this.start_day).getTime() > new Date(this.end_day).getTime()) {
                    let time = this.end_day;
                    this.end_day = this.start_day;
                    this.start_day = time;
                }
            },
        }
    }
</script>