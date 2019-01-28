<template>
    <div class="ys-con pos-r">
        <div class="search-result-box off">
            <div>
                <p><a @click="returnEvent()"><i class="ys-icon icon-arrow-left"></i>返回事件搜索</a></p>
                <div class="ys-box-con timeline-info-box m-t-10">
                    <div class="timeline-info-con clearfix">
                        <div class="fLeft textC m-r-20">
                            <div class="avatar m-b-10">
                                <img src="../../assets/images/ip-net.png" style="width:60px;height:60px;"
                                     class="verticalM"/>
                            </div>
                            <p class=""><span class="ys-primary-color">违规终端 / 被攻击终端</span></p>
                        </div>
                        <div class="detail">
                            <p class="p-t-20">
                                <span class="font18 m-r-20 d-i-b" style="width:68px;">{{IP}}</span>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="ys-box-con m-t-10">
                    <p>综合条件查询<a class="m-l-10" @click="filterStatus=!filterStatus"><span
                            v-if="filterStatus">收起</span><span v-else>展开</span><i class="ys-icon icon-downlist-up m-l-5"
                                                                                  v-bind:class="[filterStatus ? '' : 'arrow-rotate' ]"></i></a>
                    </p>
                    <div class="filter-wrap">
                        <div v-if="filterStatus"><!--v-bind:class="[filterStatus ? 'on' : 'off' ]"-->
                            <div class="filter-box m-t-15 m-b-15">
                                <div>
                                    <div v-for="list in conditionList" style="height:30px;line-height:30px;">
                                        <span v-for="single in list">
                                          <span class="ys-success-color m-r-5 m-l-5 font14 verticalM"
                                                v-show="single.logic==1">且</span>
                                          <span class="ys-success-color m-r-5 m-l-5 font14 verticalM"
                                                v-show="single.logic==2 && $index==0">且</span>
                                          <span class="ys-success-color m-r-5 m-l-5 font12 verticalM"
                                                v-show="single.logic==2 && $index!=0">或</span>
                                          <span class="verticalM">[ {{single.field.name}} ]</span>
                                          <span class="verticalM m-l-5 m-r-5">{{single.expression.name}}</span>
                                          <span class="verticalM"
                                                v-if="single.field.id=='level'">[ {{single.value | levelFil}} ]</span>
                                          <span class="verticalM" v-else>[ {{single.value}} ]</span>
                                          <span class="verticalM ys-error-color text-cursor"
                                                @click="deleteCondition(single,list)"><i
                                                  class="ys-icon icon-trash m-l-5"></i></span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <radio :list="logicList" :value.sync="addCondition.logic"></radio>
                                <span class="ys-info-color m-l-20 verticalM">字段：</span>
                                <ys-select :option="fieldList" :selected.sync="addCondition.field"></ys-select>
                                <span class="ys-info-color m-l-20 verticalM">条件：</span>
                                <ys-select :option="expressionData"
                                           :selected.sync="addCondition.expression"></ys-select>
                                <span class="ys-info-color m-l-20 verticalM">值：</span>
                                <ys-select :option="levelData" :selected.sync="levelLevle"
                                           v-if="addCondition.field.id=='level'"></ys-select>
                                <input class="ys-input" v-model="addCondition.value" v-else/>
                                <button class="ys-btn ys-btn-s ys-btn-blue m-l-20" @click="addSetting()">添加条件</button>
                            </div>
                            <p class="m-t-10">
                                <button class="ys-btn" @click="goSearch()"><i class="ys-icon icon-search"></i>查询
                                </button>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="ys-box-con m-t-5 event-timeline-chart-box">
                    <div id="event-timeline-chart" style="width:100%;height:200px;"></div>
                </div>
            </div>
            <div class="m-t-10">
                <div v-if="timelineData.length==0" class="ys-box-con">
                    <no-data :height="'400px'"></no-data>
                </div>
                <div v-if="timelineData.length>0" class="timeline-module m-b-10">
                    <div class="time-box" style="visibility: hidden">
                        <div class="inner" style="height: 30px;">
                            <p class="ys-info-color textC m-t-15"></p>
                        </div>
                    </div>
                    <div class="time-clock" style="visibility: hidden">
                        <div class="inner"><i class="ys-icon icon-clock font14 ys-error-color"></i></div>
                    </div>
                    <div class="displayCell p-l-20">
                        <div class="timeline-module-info-con">
                            <div class="thead p-0"
                                 style="background: rgba(0, 0, 0, 0.35);height: 40px;line-height: 40px;">
                                <span>攻击源</span>
                            </div>
                            <div class="item">
                                <div class="item-list">
                                    <div class="displayCell">
                                        <div style="width: 163px;background: rgba(0, 0, 0, 0.35)" class="textC">
                                            <p style="height: 40px;line-height: 40px;">事件类型</p>
                                        </div>
                                    </div>
                                    <div class="item-list-detail">
                                        <div style="background: rgba(0, 0, 0, 0.35)" class="textC">
                                            <p class=" keyword timeline_str" style="height: 40px;line-height: 40px;">
                                                事件详情</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="timelineData.length>0" id="timeline-wrap">
                    <div class="timeline-module level1"
                         v-for="list in timelineData"
                         v-bind:class="[itemColor(list.threat_level),curTimelineId==$index ? 'on' : '']"
                         @mouseover="curTimelineId=$index" @mouseout="curTimelineId=-1">
                        <div class="time-box">
                            <div class="inner">
                                <p class="ys-info-color textC m-t-15">{{list.time | formatterTime}}</p>
                            </div>
                        </div>
                        <div class="time-clock">
                            <div class="inner"><i class="ys-icon icon-clock font14 ys-error-color"></i></div>
                        </div>
                        <div class="timeline-module-info">
                            <div class="timeline-module-info-con">
                                <div class="title">
                                    <i class="ys-icon m-r-5 icon-user"></i>
                                    <span>{{list.dst_ip || '未知'}}</span>
                                </div>
                                <div class="item">
                                    <div class="item-list">
                                        <div class="item-list-label">
                                            <div class="inner clearfix">
                                                <div class="d-i-b">
                                                    <span class="ys-info-color">{{list.event_name}}</span>
                                                    <!--<p style="color:#596f9b;">{{list.time | formatterTime}}-->
                                                    <!--&lt;!&ndash;{{item.start_time}}-{{item.end_time}}&ndash;&gt;</p>-->
                                                </div>
                                                <!--<div class="fRight ys-primary-color text-cursor"-->
                                                     <!--style="padding-top:12px;"-->
                                                     <!--v-if="list.threat_level>1"><i-->
                                                        <!--class="ys-icon icon-import m-r-5 font14"></i>转处置-->
                                                <!--</div>-->
                                                <!--<div class="fRight ys-error-color text-cursor m-r-10"-->
                                                     <!--style="padding-top:12px;"-->
                                                     <!--v-if="list.threat_level>1"><i-->
                                                        <!--class="ys-icon icon-menu-bell m-r-5 font14"></i>预警-->
                                                <!--</div>-->
                                            </div>
                                        </div>
                                        <div class="item-list-detail">
                                            <div class="top">
                                                <p class="ys-info-color keyword timeline_str" style="max-width: 560px;"
                                                   :title="list.timeline_str | formatterTime">{{list.timeline_str}}</p>
                                                <!-- &lt;!&ndash;!-- @click="getCurInfo(item)"--><!--{{item.count}}条-->
                                                <div class="keyword-num text-cursor"
                                                     v-bind:class="itemColor(list.threat_level)"
                                                     @click="list.show = !list.show"><span
                                                        class="fRight text-cursor" style="margin-right: 18px"><i
                                                        class="ys-icon icon-downlist-up"
                                                        v-bind:class="[list.show ? '' : 'item-arrow-rotate']"></i></span>
                                                </div>
                                            </div>
                                            <div class="bottom p-b-15" v-bind:class="[list.show ? '' : 'off']">
                                                <ul>
                                                    <li v-for="info in list.detialInfo">
                                                        <span class="ys-error-color font14 m-r-5">·</span>
                                                        <span class="m-r-10" style="color:#596f9b;">{{info}}</span>
                                                        <!--<span class="m-r-10" style="color:#596f9b;">{{info.time}}</span>
                                                        <span class="m-r-10" style="color:#596f9b;">{{info.message}}</span>-->
                                                    </li>
                                                </ul>
                                                <!--<p class="m-t-5"><a @click="goMoreLog(item)"><i
                                                        class="ys-icon icon-eye m-r-5"></i>更多日志</a></p>-->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="textC">
                    <loading-normal :show="moreTimelineStatus"></loading-normal>
                </div>
                <div class="textC ys-info-color" v-if="bottomStatus && timelineData.length>0"><i
                        class="ys-icon icon-warn-outline m-r-5"></i>已滚动到最底部
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
    .level1.on .time-box .inner {
        background: rgba(0, 189, 133, 0.3);
        border: 1px solid rgba(0, 189, 133, 0.5);
    }

    .timeline_str {
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
    }

    .level1 .time-clock {
        background: rgba(0, 189, 133, 0.15);
    }

    .level1 .time-clock .inner i {
        color: #00bd85 !important;
    }

    .level1 .timeline-module-info-con > div.title i {
        color: #00bd85 !important;
    }

    .level2.on .time-box .inner {
        background: rgba(218, 187, 97, 0.3);
        border: 1px solid rgba(218, 187, 97, 0.5);
    }

    .level2 .time-clock {
        background: rgba(218, 187, 97, 0.15);
    }

    .level2 .time-clock .inner i {
        color: #dabb61 !important;
    }

    .level2 .timeline-module-info-con > div.title i {
        color: #dabb61 !important;
    }

    .level3.on .time-box .inner {
        background: rgba(231, 125, 78, 0.3);
        border: 1px solid rgba(231, 125, 78, 0.5);
    }

    .level3 .time-clock {
        background: rgba(231, 125, 78, 0.3);
    }

    .level3 .time-clock .inner i {
        color: #e77d4e !important;
    }

    .level3 .timeline-module-info-con > div.title i {
        color: #e77d4e !important;
    }

    .level4.on .time-box .inner {
        background: rgba(223, 97, 87, 0.3);
        border: 1px solid rgba(223, 97, 87, 0.5);
    }

    .level4 .time-clock {
        background: rgba(223, 97, 87, 0.3);
    }

    .level4 .time-clock .inner i {
        color: #e96157 !important;
    }

    .level4 .timeline-module-info-con > div.title i {
        color: #e96157 !important;
    }

    .level5.on .time-box .inner {
        background: rgba(148, 55, 55, 0.3);
        border: 1px solid rgba(148, 55, 55, 0.5);
    }

    .level5 .time-clock {
        background: rgba(148, 55, 55, 0.3);
    }

    .level5 .time-clock .inner i {
        color: #943737 !important;
    }

    .level5 .timeline-module-info-con > div.title i {
        color: #943737 !important;
    }

    .item-arrow-rotate {
        transform: rotate(180deg);
    }

    .search-result {
        transition-property: all;
        transition-duration: 0.5s;
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .search-result.off {
        height: 0px !important;
        min-height: 0px !important;
        padding: 0px;
        overflow: hidden;
    }

    .search-result-box {
        transition-property: all;
        transition-duration: 0.5s;
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .search-result-box.off {
        overflow: hidden;
    }

    .item-list-detail .top .keyword {
        line-height: 66px;
        padding-left: 25px;
        margin-right: 120px;
    }

    .item-list-detail .top .keyword-num {
        position: absolute;
        top: 0;
        right: 15px;
        width: 50px;
        height: 24px;
        line-height: 24px;
        border-radius: 20px;
        margin-top: 23px;
        padding-left: 15px;
        text-align: center;
    }

    .keyword-num.level1 {
        background: #00bd85;
    }

    .keyword-num.level2 {
        background: #dabb61;
    }

    .keyword-num.level3 {
        background: #e77d4e;
    }

    .keyword-num.level4 {
        background: #e96157;
    }

    .keyword-num.level5 {
        background: #943737;
    }

    .item-list-detail .top {
        height: 66px;
        background: rgba(0, 0, 0, 0.15);
        position: relative;
    }

    .item-list-detail .bottom {
        height: auto;
        background: rgba(0, 0, 0, 0.25);
        box-shadow: inset 0px 3px 10px rgba(0, 0, 0, 0.2);

        overflow-y: hidden;
        max-height: 5000px; /* approximate max height */
        transition-property: all;
        transition-duration: 0.5s;
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .item-list-detail .bottom.off {
        max-height: 0;
        padding: 0px !important;
    }

    .item-list-detail .bottom ul {
        margin-left: 25px;
        margin-top: 20px;
    }

    .item-list-detail .bottom ul li {
        line-height: 26px;
    }

    .item-list-detail .bottom p {
        margin-left: 25px;
    }

    .item-list {
        margin-bottom: 3px;
        width: 100%;
        display: table;
    }

    .item-list:last-child {
        margin-bottom: 0px;
    }

    .item-list-label {
        display: table-cell;
        padding-right: 3px;
        vertical-align: top;
        background: rgba(0, 0, 0, 0.15);
        line-height: 66px;
        text-align: center;
    }

    .item-list-label .inner {
        width: 160px;
        text-align: center;
        /*padding: 15px;*/
    }

    .item-list-detail {
        display: table-cell;
        vertical-align: top;
        width: 100%;
        padding-left: 3px;
    }

    .timeline-module-info {
        display: table-cell;
        vertical-align: top;
        padding-left: 20px;
        padding-bottom: 18px;
        width: 100%;
    }

    .timeline-module-info-con {
        display: table;
        table-layout: fixed;
        width: 100%;
    }

    .timeline-module-info-con .thead {
        display: table-cell;
        width: 160px;
        background: rgba(0, 0, 0, 0.15);
        padding: 13px 0px;
        text-align: center;
        position: relative;
        vertical-align: top;
    }

    .timeline-module-info-con .title {
        display: table-cell;
        width: 160px;
        background: rgba(0, 0, 0, 0.15);
        line-height: 66px;
        text-align: center;
        position: relative;
        vertical-align: top;
    }

    .timeline-module-info-con .title::before {
        position: absolute;
        top: 18px;
        left: -20px;
        content: "";
        border: 10px solid transparent;
        border-right: 10px solid rgba(0, 0, 0, 0.15);
        width: 0;
        height: 0px;
    }

    .timeline-module-info-con .item {
        display: table-cell;
        padding-left: 3px;
    }

    .timeline-info-box {
        position: relative;
    }

    .timeline-tag {
        position: absolute;
        top: 0px;
        left: 0px;
    }

    .search-input-box {
        width: 370px;
        margin-top: 38px;
        text-align: center;
        display: inline-block;
    }

    .search-input-box input {
        height: 35px;
        width: 350px;
        font-size: 16px;
    }

    .search-input-box div i {
        position: absolute;
        right: 15px;
        top: 8px;
        font-size: 20px;
    }

    .search-input-box p {
        width: 370px;
        margin-top: 10px;
        display: inline-block;
    }

    .timeline-split {
        width: 100%;
        height: 1px;
        background: rgba(255, 255, 255, 0.08);
        margin-top: 55px;
    }

    .time-line-table tbody tr {
        height: 54px;
    }

    .timeline-info-con {
        padding-left: 32px;
        padding-top: 3px;
    }

    .timeline-info-con .avatar {
        display: inline-block;
        border-radius: 50%;
        background: rgba(74, 146, 255, .3);
    }

    .timeline-info-con .detail {
        float: left;
        display: inline-block;
    }

    .grade {
        float: right;
        margin-right: 12px;
    }

    .grade-value {
        font-size: 40px;
        font-weight: 900;
    }

    .event-timeline-chart-box {
        position: relative;
    }

    /*.event-timeline-chart-box::before {*/
    /*position: absolute;*/
    /*bottom: -28px;*/
    /*left: 107px;*/
    /*content: "";*/
    /*border: 10px solid transparent;*/
    /*border-top: 18px solid rgba(0, 0, 0, 0.15);*/
    /*width: 0;*/
    /*height: 0px;*/
    /*}*/

    .timeline-module {
        display: table;
    }

    .time-box {
        display: table-cell;
        padding-right: 10px;
        vertical-align: top;
    }

    .time-box .inner {
        width: 100px;
        height: 78px;
        border-radius: 3px;
        border: 1px solid rgba(0, 0, 0, 0);
        background: rgba(0, 0, 0, 0);
    }

    .time-clock {
        display: table-cell;
        background: rgba(181, 83, 81, 0.15);
    }

    .time-clock .inner {
        width: 10px;
        height: 100%;
        background: rgba(181, 83, 81, 0.15);
        position: relative
    }

    .time-clock i {
        position: absolute;
        top: 20px;
        left: -2px;
    }

    .filter-wrap > div {
        max-height: 5000px;
        transition-property: all;
        transition-duration: 0.5s;
        transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
    }

    .filter-wrap > div.off {
        max-height: 0;
        padding: 0px;
        overflow: hidden;
    }

    .arrow-rotate {
        transform: rotate(180deg);
    }
</style>
<script>
    let echarts = require('echarts/lib/echarts');
    require('../../assets/js/jquery.slimscroll.js');
    import Api from '../../lib/api'

    export default {
        name: "event-timeline",
        props: {
            ip: {
                default: ''
            },
            passTag: {
                default: ''
            },
            passTime: {
                default: ''
            },
            show: {
                default: false
            }
        },
        data() {
            return {
                searchWord: "",
                userInfo: {
                    recordsTotal: ''
                },
                firstDay: "",
                lastDay: "",
                serachResultList: [],
                curScore: 0,
                timelineData: [],
                actionList: [
                    {id: "", name: "全部操作"},
                    {id: "0", name: "网络访问"},
                    {id: "1", name: "操作记录"},
                    {id: "2", name: "安全预警"},
                    {id: "3", name: "认证总数"},
                    {id: "4", name: "系统状态"},
                    {id: "5", name: "恶意代码"},
                    {id: "6", name: "设备故障"},
                    {id: "7", name: "信息刺探"},
                    {id: "8", name: "攻击入侵"},
                    {id: "9", name: "其他"},
                    {id: "10", name: "信息危害"},
                    {id: "11", name: "信息监控"},
                ],
                curAction: {id: "", name: "全部操作"},
                levelList: [
                    {id: "0", name: "全部等级"},
                    {id: "1", name: "正常"},
                    {id: "2", name: "低危"},
                    {id: "3", name: "中危"},
                    {id: "4", name: "高危"},
                    {id: "5", name: "严重"}
                ],
                curLevel: {id: "0", name: "全部等级"},
                levelLevle: {},
                curPage: -1,
                moreTimelineStatus: false,
                curTimelineId: -1,
                timelineTotal: 0,
                bottomStatus: false,
                curPoliceCode: this.$route.params.police_code,
                curPoliceIdCode: this.$route.params.police_id_code,
                IP: '',
                Name: '',
                Port: '',
                curDate: "",
                stopLoadStatus: false,
                curIpList: "",
                tag: '',
                time: '',
                fieldList: [],
                logicList: [
                    {id: 1, text: "且"},
                    {id: 2, text: "或"},
                ],
                curLogic: 1,
                filterStatus: false,
                expressionData: [
                    {id: "1", name: "等于"},
                    {id: "2", name: "不等于"},
                    {id: "3", name: "小于"},
                    {id: "4", name: "大于"},
                    {id: "5", name: "包含"},
                    {id: "6", name: "不包含"}
                ],
                addCondition: {
                    logic: 1,
                    field: {},
                    expression: {id: "1", name: "等于"},
                    value: ""
                },
                conditionList: [],
                showTime: ''
            }
        },
        ready() {
        },
        filters: {
            levelFil: function (id) {
                for (let x in this.levelData) {
                    if (id == this.levelData[x].id) {
                        return this.levelData[x].name
                    }
                }
            },
            formatterTime: function (val) {
                return val.substring(0, 4) + '-' + val.substring(4, 6) + '-' + val.substring(6, 8) + ' ' + val.substring(8, 10) + ':' + val.substring(10, 12) + ':' + val.substring(12, 14);
            }
        },
        methods: {
            itemColor(level) {
                switch (level) {
                    case 1:
                        return "level1";
                        break;
                    case 2:
                        return "level2";
                        break;
                    case 3:
                        return "level3";
                        break;
                    case 4:
                        return "level4";
                        break;
                    case 5:
                        return "level5";
                        break;
                    default:
                        return "level1";
                }
            },
            goSearch() {
                this.showTimeline();
                this.tableRe();
            },
            showTimeline() {
                let self = this;
                self.curAction = {id: "", name: "全部操作"};
                self.curLevel = {id: "0", name: "全部等级"};
                $(window).scroll(function () {
                    var $currentWindow = $(window);
                    var windowHeight = $currentWindow.height();
                    var scrollTop = $currentWindow.scrollTop();
                    var docHeight = $(document).height() - 500;
                    if ((scrollTop) >= docHeight - windowHeight) {
                        if (self.moreTimelineStatus == false) {
                            self.moreTimelineStatus = true;
                            self.loadMoreTimeline()
                        }
                    }
                });
                this.$root.loadStatus = false;
                this.getScoreData();
                this.loadMoreTimeline();
            },
            getScoreData() {
                let data = {
                    ip: this.IP,
                    tag: this.tag,
                    event_time: this.time,
                    query_string: ''
                };
                let arr = [];
                for (let parent in this.conditionList) {
                    let arr1 = [];
                    for (let child in this.conditionList[parent]) {
                        arr1.push({
                            field: this.conditionList[parent][child].field.id,
                            expression: this.transExpression(this.conditionList[parent][child].expression.id),
                            value: this.conditionList[parent][child].value
                        })
                    }
                    arr.push(arr1)
                }
                data.query = arr;
                this.$http.post('/api/ssa/event/ip_score_line', data).then((response) => {
                    if (response.data.status == 200) {
                        let data = response.data.data;
                        let x = [];
                        let y = [];
                        for (let key in data) {
                            let resTime = data[key].data_time;
                            let time = resTime.split('-')[0] + '-' + resTime.split('-')[1] + '-' + resTime.split('-')[2] + ' ' + resTime.split('-')[3] + ':00:00';
                            x.push(time);
                            y.push(data[key].total);
                        }
                        this.setChart(x, y)
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg;
                    }
                }).catch((response) => {
                    Api.user.requestFalse(response, this);
                })
            },
            tableRe() {
                this.timelineTotal = 0;
                this.curPage = -1;
                this.stopLoadStatus = false;
                this.bottomStatus = false;
                this.loadMoreTimeline();
            },
            loadMoreTimeline() {
                if (this.stopLoadStatus) {
                    this.moreTimelineStatus = false;
                    this.bottomStatus = true;
                    return false
                }
                let start = 0;
                if (this.curPage == -1) {
                    start = 0;
                    this.curPage += 1;
                } else {
                    this.curPage += 1;
                    start = this.curPage * 10;
                    if (this.timelineData.length == this.timelineTotal && this.timelineData.length != 0) {
                        this.moreTimelineStatus = false;
                        this.bottomStatus = true;
                        return false;
                    }
                    if (this.timelineData.length == 0) {
                        this.moreTimelineStatus = false;
                        return false;
                    }
                }
                let min = 0;
                let max = 0;
                if (this.curLevel.id == 0) {
                    min = 0;
                    max = 5;
                } else {
                    min = this.curLevel.id;
                    max = this.curLevel.id;
                }
                let data = {
                    length: 10,
                    ip: this.IP,
                    tag: this.tag,
                    event_time: this.time,
                    query_string: '',
                    start: start
                };
                let arr = [];
                for (let parent in this.conditionList) {
                    let arr1 = [];
                    for (let child in this.conditionList[parent]) {
                        arr1.push({
                            field: this.conditionList[parent][child].field.id,
                            expression: this.transExpression(this.conditionList[parent][child].expression.id),
                            value: this.conditionList[parent][child].value
                        })
                    }
                    arr.push(arr1)
                }
                data.query = arr;
                this.$http.post('/api/ssa/event/event_timeline_info', data).then((response) => {
                    let data = response.data.data;
                    if (data.length == 0) {
                        this.stopLoadStatus = true;
                    }
                    this.timelineTotal = response.data.recordsFiltered;
                    this.userInfo.recordsTotal = response.data.recordsTotal;
                    for (let i in data) {
                        data[i].show = false;
                        let detialInfo = [];
                        let timeline_str = '';
                        let count = 0;
                        for (let j in data[i].tran_data) {
                            let str = j + ': ' + data[i].tran_data[j];
                            if (data[i].tran_data[j] && count < 4) {
                                timeline_str += str + ', ';
                                count += 1;
                            }
                            detialInfo.push(str);
                        }
                        data[i].detialInfo = detialInfo;
                        data[i].timeline_str = timeline_str;
                    }
                    for (let x in data) {
                        this.timelineData.push(data[x]);
                    }
                    this.moreTimelineStatus = false;
                }).catch((response) => {
                    Api.user.requestFalse(response, this);
                })
            },
            setChart(xData, yData) {
                let self = this;
                let eventTimelineChart = echarts.init(document.getElementById("event-timeline-chart"));
                let option = {
                    grid: {
                        top: '10',
                        bottom: '50',
                        left: 30,
                        right: 30,
                        containLabel: true
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            lineStyle: {
                                color: "#e96157",
                                opacity: 0.25
                            },
                        },
                        formatter: function (params) {
                            let str = "<div class='font12 m-r-10' style='height:60px;padding-right:10px;padding-left:10px;'>";
                            str += "<p style='margin-top:10px;'><span class='ys-info-color'>时间：</span>" + params[0].name + "<p>";
                            str += "<p style='margin-top:10px;'><span class='ys-info-color'>数量：</span>" + params[0].value + "<p>";
                            str + "</div>"
                            return str
                        },
                        backgroundColor: 'rgba(22,26,47,.5)',
                        borderColor: 'rgba(231,125,78,.5)',
                        borderWidth: 1
                    },
                    dataZoom: [
                        {
                            type: 'slider',
                            realtime: true,
                            start: 0,
                            end: 4000,
                            borderColor: "rgba(0,0,0,0)",
                            backgroundColor: "rgba(0,0,0,0)",
                            fillerColor: "rgba(233,97,87,0.15)",
                            handleIcon: "path://M12,0c0.6,0,1,0.4,1,1v22c0,0.6-0.4,1-1,1s-1-0.4-1-1V1C11,0.4,11.4,0,12,0z",
                            handleStyle: {
                                color: "#e96157",
                                borderColor: "rgba(0,0,0,0)"
                            },
                            dataBackground: {
                                lineStyle: {
                                    color: "#46578e",
                                    opacity: 1
                                },
                                areaStyle: {
                                    color: "rgba(0,0,0,0.3)",
                                    opacity: 1
                                }
                            },
                            textStyle: {
                                color: "#f2f2f2",
                            }
                        }
                    ],
                    xAxis: {
                        type: 'category',
                        data: xData,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        axisLabel: {textStyle: {color: "#dfdfe7"}}
                    },
                    yAxis: {
                        type: 'value',
                        minInterval: 1,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        splitNumber: 5,
                        axisLabel: {
                            textStyle: {color: "#dfdfe7"},
                        },//y轴坐标的字颜色
                        splitLine: {
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        }
                    },
                    series: [{
                        data: yData,
                        type: 'line',
                        smooth: true,
                        lineStyle: {
                            normal: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                        offset: 0, color: '#943737' // 0% 处的颜色
                                    }, {
                                        offset: 0.25, color: '#e96157' // 0% 处的颜色
                                    }, {
                                        offset: 0.50, color: '#e77d4e' // 0% 处的颜色
                                    }, {
                                        offset: 0.75, color: '#dabb61' // 0% 处的颜色
                                    }, {
                                        offset: 1, color: '#00bd85' // 100% 处的颜色
                                    }],
                                    globalCoord: false // 缺省为 false
                                },
                                width: 3,
                                shadowBlur: 6,
                                shadowColor: "rgba(0,0,0,0.25)",
                                shadowOffsetX: 10,
                                shadowOffsetY: 10
                            }
                        },
                        symbol: "circle",
                        itemStyle: {
                            normal: {
                                color: "rgba(0,0,0,0)",
                                borderColor: "rgba(0,0,0,0)",
                            },
                            emphasis: {
                                color: "#4b404c",
                                borderColor: "#e96157",
                                borderWidth: 3,
                            }
                        }
                    }]
                };
                eventTimelineChart.setOption(option);
                window.addEventListener('resize', function () {
                    eventTimelineChart.resize()
                });
                eventTimelineChart.on('click', function (params) {
                    self.curDate = params.name;
                    self.curAction = {id: "", name: "全部操作"};
                    self.curLevel = {id: "0", name: "全部等级"};
                    self.tableRe();
                });
            },
            getFieldData() {
                this.$http.post('/api/ssa/event/analysis_select_search/list', {tag: this.tag}).then(function (response) {
                    this.fieldList = [];
                    for (let key in response.data.items) {
                        let item = response.data.items[key].name;
                        if (item.indexOf('时间') > -1 || item.indexOf('事件类型') > -1) {
                            continue;
                        } else {
                            this.fieldList.push(response.data.items[key]);
                        }
                    }
                    //this.fieldList =[].concat(response.data.items);
                    this.addCondition.field = this.fieldList[0];
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
            },
            addSetting() {
                if (!this.addCondition.value && this.addCondition.field.id != "level") {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '筛选值不能为空';
                    return false;
                }
                if (this.addCondition.field.id == "level" && !this.levelLevle.id) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '筛选值不能为空';
                    return false;
                }
                if (this.addCondition.field.id == "level") {
                    this.addCondition.value = this.levelLevle.id;
                }
                if (this.addCondition.logic == 2) {
                    let length = this.conditionList.length;
                    this.conditionList[length - 1].push({
                        logic: this.addCondition.logic,
                        field: this.addCondition.field,
                        expression: this.addCondition.expression,
                        value: this.addCondition.value
                    })
                } else {
                    if (this.conditionList.length == 0) {
                        this.conditionList.push([{
                            logic: 3,
                            field: this.addCondition.field,
                            expression: this.addCondition.expression,
                            value: this.addCondition.value
                        }])
                    } else {
                        this.conditionList.push([{
                            logic: this.addCondition.logic,
                            field: this.addCondition.field,
                            expression: this.addCondition.expression,
                            value: this.addCondition.value
                        }])
                    }
                }
                this.addCondition = {
                    logic: 1,
                    field: this.fieldList[0],
                    expression: {id: "1", name: "等于"},
                    value: ""
                }
            },
            deleteCondition(single, list) {
                for (let a = 0; a < this.conditionList.length; a++) {
                    if (this.conditionList[a].length) {
                        for (let b = 0; b < this.conditionList[a].length; b++) {
                            if (this.conditionList[a][b] == single) {
                                this.conditionList[a]
                                this.conditionList[a].splice(b, 1);
                                if (this.conditionList[a].length == 0) {
                                    this.conditionList.splice(a, 1);
                                }
                                break;
                            }
                        }
                    }
                }
            },
            getFieldMapData() {
                this.$http.get('/api/ssa/event/analysis_field_map', {tag: this.tag}).then(function (response) {
                    this.fieldMapData = response.data.data;
                    if (this.fieldMapData.level) {
                        this.levelData = this.fieldMapData.level.items;
                        this.levelLevle = this.levelData[0];
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            transExpression(id) {
                switch (id) {
                    case '1':
                        return "="
                        break;
                    case '2':
                        return "!="
                        break;
                    case '3':
                        return "<"
                        break;
                    case '4':
                        return ">"
                        break;
                    case '5':
                        return "in"
                        break;
                    case '6':
                        return "not in"
                        break;
                }
            },
            returnEvent() {
                this.show = false;
                //this.$router.go({name: 'analysis-event-search'})
            }
        },
        watch: {
            'curAction': function (val, oldVal) {
                if (val.id == oldVal.id) {
                    return false
                } else {
                    this.tableRe();
                }
            },
            'curLevel': function (val, oldVal) {
                if (val.id == oldVal.id) {
                    return false
                } else {
                    this.tableRe();
                }
            },
            'show': function () {
                if (this.show) {
                    this.IP = this.ip;
                    this.tag = this.passTag;
                    this.time = this.passTime;
                    this.timelineData = [];
                    this.goSearch();
                    this.getFieldData();
                    this.getFieldMapData();
                }
            },
            //'addCondition.field'
            'addCondition': {
                handler(newValue, oldValue) {
                    console.log(newValue)
                },
                deep: true
            }
        }
    }
</script>
