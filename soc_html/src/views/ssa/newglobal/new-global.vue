<template>
    <div>
        <div class="global-wrap">
            <div class="global-head ys-box-con">
                <div class="global-title">
                    <p class="font14 textC">态势感知平台</p>
                    <span class="right"><button class="ys-btn" @click="showFullScreen()">全屏</button></span>
                </div>
                <div class="global-title m-t-5">
                    <p class="ys-info-color textC">全局态势</p>
                </div>
            </div>
            <div class="m-t-10 pos-r clearfix">
                <div class="col-md-8 p-0">
                    <div class="global-module-box">
                        <div class="global-module-title ys-white-color">风险状态</div>
                        <div class="global-module-con">
                            <div style="width:100%;margin:0 auto;" class="clearfix">
                                <bubble
                                        :id="'ssa-global-risk-status'"
                                        :height="'279px'"
                                        :data="riskStatusData"
                                ></bubble>
                            </div>
                        </div>
                    </div>
                    <div class="global-module-box m-t-5" style="position: relative">
                        <div class="global-module-title ys-white-color">事件统计</div>
                        <div class="tool-box p-t-10 p-r-10" style="position: absolute;right: 0px;top: 0px">
                            <span class="ys-info-color verticalM displayIB">事件总数:</span>
                            <span class=" m-r-5 specialNum displayIB verticalM"
                                  v-html="changeWanUnit_total(securityGrade.total)"></span>
                            <i class="ys-icon icon-downlist-up displayIB verticalM ys-error-color"></i>
                            <span class=" displayIB ys-error-color verticalM">{{securityGrade.up}}</span>
                            <div class="clearfix"></div>
                        </div>
                        <div class="global-module-con">
                            <div style="width:100%;margin:0 auto;" class="clearfix">
                                <div class="col-md-7 p-0 m-t-10">
                                    <div class="col-md-4 textC">
                                        <div class="p-t-40 p-b-20 m-l-5 m-r-5">
                                            <div style="height: 90px">
                                                <img src="../../../assets/images/ssac/global-rq.png" alt="">
                                            </div>
                                            <p class="textC font28 ys-primary-color">
                                                {{changeWanUnit(eventStatic.rq)}}</p>
                                            <p class="textC m-t-10 font14 ys-info-color">攻击</p>
                                        </div>
                                    </div>
                                    <div class="col-md-4 textC">
                                        <div class="p-t-40 p-b-20 m-l-5 m-r-5">
                                            <div class="" style="height: 90px;padding-top: 7px;">
                                                <img src="../../../assets/images/ssac/global-bd.png" alt="">
                                            </div>
                                            <p class="textC font28 ys-primary-color">
                                                {{changeWanUnit(eventStatic.bd)}}</p>
                                            <p class="textC m-t-10 font14 ys-info-color">病毒</p>
                                        </div>
                                    </div>
                                    <div class="col-md-4 textC">
                                        <div class="p-t-40 p-b-20 m-r-5 m-l-5">
                                            <div style="height: 90px;padding-top: 5px;">
                                                <img src="../../../assets/images/ssac/global-wg.png" alt="">
                                            </div>
                                            <p class="font28 ys-primary-color">
                                                {{changeWanUnit(eventStatic.wg)}}</p>
                                            <p class="font14 m-t-10 ys-info-color">违规</p>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-5 p-0">
                                    <pie-chart
                                            :id="'ssa-global-event-pie'"
                                            :height="'240px'"
                                            :name="'事件来源'"
                                            :unit="'wan'"
                                            :y.sync="eventStaticPie"
                                            :color="1"></pie-chart>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="global-module-box m-t-5">
                        <div class="global-module-title ys-white-color">事件趋势</div>
                        <div class="global-module-con">
                            <div style="width:100% ;margin: 0 auto;">
                                <line-chart
                                        :id="'ssa-global-machine-22'"
                                        :height="'240px'"
                                        :name="assetDetail.name"
                                        :x="assetDetail.x"
                                        :unit="'wan'"
                                        :color="assetDetail.color"
                                        :series="assetDetail.series"></line-chart>
                            </div>
                        </div>
                    </div>
                    <div class="m-t-5 clearfix">
                        <div class="col-md-6 p-0">
                            <div class="ys-box">
                                <div class="ys-box-title">违规类型统计</div>
                                <div class="ys-box-con">
                                    <ring-chart :id="'ssa-global-safe-type'" :height="'240px'"
                                                :data="safeErrorType"></ring-chart>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 p-0 p-l-5">
                           <div class="ys-box">
                                <div class="ys-box-title">病毒类型统计</div>
                                <div class="ys-box-con">
                                    <ring-chart :id="'ssa-global-bd-type'" :height="'240px'"
                                                :data="bdErrorType"></ring-chart>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="m-t-5 clearfix">
                        <div class="col-md-6 p-0">
                             <div class="ys-box">
                                <div class="ys-box-title">违规单位统计TOP5</div>
                                <div class="ys-box-con">
                                    <feng-bar-chart :id="'website-response'"
                                                    :height="'240px'"
                                                    :tipname="'违规数'"
                                                    :unit="'wan'"
                                                    :x="captionRisk.y"
                                                    :y="captionRisk.x">
                                    </feng-bar-chart>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 p-0 p-l-5">
                            <div class="ys-box">
                                <div class="ys-box-title">病毒统计TOP5</div>
                                <div class="ys-box-con">
                                    <feng-bar-chart :id="'ssa-global-attack-source'"
                                                    :height="'240px'"
                                                    :name="'部门'"
                                                    :color="'#00bd85'"
                                                    :x="bd_unit_count.y"
                                                    :y="bd_unit_count.x"
                                                    :unit="'wan'"></feng-bar-chart>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="global-module-box m-t-5">
                        <div class="global-module-title ys-white-color">网络流量</div>
                        <div class="global-module-con">
                            <div style="width:100%;margin:0 auto;" class="clearfix">
                                <line-chart
                                        :id="'ssa-global-online'"
                                        :height="'253px'"
                                        :name="lineData.name"
                                        :x="lineData.x"
                                        :unit="'band'"
                                        :color="lineData.color"
                                        :series="lineData.series"></line-chart>
                            </div>
                        </div>
                    </div>
                    <div class="global-module-box m-t-5">
                        <div class="ys-box-title">设备状态</div>
                        <div class="global-module-con">
                            <no-data :height="'250px'" v-show="AssetStatus.length==0"></no-data>
                            <div style="width:100%;margin:0 auto;" v-show="AssetStatus.length>0" class="clearfix">
                                <div id="decive-status" style="height: 250px;">
                                    <table class="ys-table">
                                        <thead>
                                        <tr>
                                            <!--<th></th>-->
                                            <th style="text-align: left">类型</th>
                                            <th>数量</th>
                                            <th><span class="ys-success-color"><i
                                                    class="ys-icon m-r-3 font14 icon-check-circle"></i>正常</span></th>
                                            <th><span class="ys-warn-color"><i
                                                    class="ys-icon m-r-3 font14 icon-clear-circle"></i>采集断开</span></th>
                                            <th><span class="ys-error-color"><i
                                                    class="ys-icon m-r-3 icon-warn-circle"></i>异常事件</span></th>
                                        </tr>
                                        </thead>
                                        <tbody v-for="list in AssetStatus" class="textC">
                                        <tr>
                                            <!--
                                            <td class="detail">
                                                    <span @click="showDetail(list.type)"><i class="ys-icon"
                                                                                            v-bind:class="[curDetailId == list.type ? 'icon-downlist-up' : 'icon-downlist' ]"></i></span>
                                            </td>
                                            -->
                                            <td style="text-align: left;width: 150px;">{{list.type}}</td>
                                            <td>{{list.num}}</td>
                                            <td class="ys-success-color">{{list.normal}}</td>
                                            <td class="ys-warn-color">{{list.off}}</td>
                                            <td class="ys-error-color">{{list.abnormal}}</td>
                                        </tr>
                                        <!--
                                        <tr class="detail" v-bind:class="[curDetailId == list.type ? 'open' : '' ]"
                                            v-for="(index,obj) in list.detail">
                                            <td class="ys-success-color"></td>
                                            <td style="text-align: left"><span
                                                    class="displayIB verticalM m-l-10 m-r-5 ys-success-color font26">·</span>
                                                <span>{{obj.ip}}</span>
                                            </td>
                                            <td>{{obj.num}}</td>
                                            <td class="ys-success-color">{{obj.normal}}</td>
                                            <td class="ys-warn-color">{{obj.off}}</td>
                                            <td class="ys-error-color">{{obj.abnormal}}</td>
                                        </tr>
                                        -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 p-0 p-l-5">
                    <div class="ys-box-title">安全评分</div>
                    <div class="ys-box-con">
                        <div class="security-grade-box" style="margin-top: 56px;margin-bottom: 57px;">
                            <div class="grade">{{changeWanUnit(securityGrade.score)}}</div>
                        </div>
                    </div>
                    <div class="ys-box m-t-5">
                        <div class="ys-box-title">设备风险指数比例</div>
                        <div class="ys-box-con">
                            <danger-grade :id="'ssa-global-danger-grade-state'"
                                          :height="'227px'"
                                          :name="'比例'"
                                          :data="dangerGradeSeries"
                                          :value="dangerGradeValue"
                                          :unit="'wan'">

                            </danger-grade>
                        </div>
                    </div>
                    <div class="ys-box m-t-5">
                        <div class="ys-box-title">风险资产TOP5</div>
                        <div class="ys-box-con">
                            <risk-bubble
                                    :id="'ssa-global-risk-rate'"
                                    :height="'227px'"
                                    :data="AssetRiskData"
                                    :tipname="'风险资产数'"
                                    :unit="'wan'">

                            </risk-bubble>
                        </div>
                    </div>
                    <div class="ys-box m-t-5">
                        <div class="ys-box-title">攻击类型统计</div>
                        <div class="ys-box-con">
                            <ring-chart :id="'ssa-global-attack-type'" :height="'240px'"
                                                :data="attackErrorType"></ring-chart>
                        </div>
                    </div>
                    <div class="ys-box m-t-5">
                        <div class="ys-box-title">攻击源统计TOP5</div>
                        <div class="ys-box-con">
                            <feng-bar-chart :id="'ssa-global-caption'"
                                            :height="'240px'"
                                            :name="'攻击源'"
                                            :color="'#4a92ff'"
                                            :x="attack_srcip_count.y"
                                            :y="attack_srcip_count.x"
                                            :unit="'wan'"></feng-bar-chart>
                        </div>
                    </div>
                    <div class="ys-box m-t-5">
                        <div class="ys-box-title">风险事件TOP5</div>
                        <div class="ys-box-con" style="height:270px;">
                            <table class="ys-chart-table over-table m-t-20">
                                <tr v-for="list in eventRiskTop">
                                    <td class="ys-error-color textL"><i class="ys-icon icon-menu-home m-r-5"></i><span>{{list.name}}</span>
                                    </td>
                                    <td>{{changeWanUnit(list.count)}}</td>
                                </tr>
                            </table>
                            <no-data :height="'195px'" v-if="eventRiskTop.length==0"></no-data>
                        </div>
                    </div>
                    <div class="ys-box m-t-5">
                        <div class="ys-box-title">被攻击终端统计TOP5</div>
                        <div class="ys-box-con">
                            <ling-bar-chart :id="'ssa-global-chack'"
                                            :height="'240px'"
                                            :name="'终端'"
                                            :color="'#e96157'"
                                            :x="attack_dstip_count.x"
                                            :y="attack_dstip_count.y"
                                            :unit="'wan'"></ling-bar-chart>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="global-full-page" v-show="globalFullStatus">
            <global-full-page :show.sync="globalFullStatus"></global-full-page>
        </div>
    </div>
</template>
<style scoped>

    .specialNum {
        font-size: 24px;
        font-family: digi;
        color: rgba(242, 242, 242, 1);
    }

    .ys-table tr.detail td {
        text-align: center;
    }

    .over-table {
        table-layout: fixed;
    }

    .over-table td {
        width: 100%;
        word-break: keep-all; /* 不换行 */
        white-space: nowrap; /* 不换行 */
        overflow: hidden; /* 内容超出宽度时隐藏超出部分的内容 */
        text-overflow: ellipsis; /* 当对象内文本溢出时显示省略标记(...) ；需与overflow:hidden;一起使用。*/
    }

    .global-title {
        width: 100%;
        position: relative;
    }

    .global-title .right {
        position: absolute;
        top: 9px;
        right: 10px;
    }

    .global-module-box {
        background: rgba(0, 0, 0, 0.15);
        border-top: 1px solid rgba(74, 146, 255, 0.25);
    }

    .global-module-title {
        height: 36px;
        line-height: 36px;
        position: relative;
        padding-left: 15px;
        font-size: 14px;
    }

    .global-module-title:before {
        content: '';
        position: absolute;
        left: 0px;
        width: 154px;
        height: 36px;
        background: url("../../../assets/images/ssa/global-box-title-corner.png") no-repeat;
        background-size: 154px;
        z-index: 0;
    }

    .security-grade-box {
        width: 166px;
        height: 153px;
        margin: 0px auto;
        background: url("../../../assets/images/ssa/security-grade-bg-1.png") no-repeat;
        background-size: 166px;
    }

    .security-grade-box .title {
        text-align: center;
        padding-top: 50px;
    }

    .security-grade-box .grade {
        text-align: center;
        font-size: 40px;
        padding-top: 60px;
    }

    .global-module-con {
        padding: 10px;
    }

    .global-module-con .title-mark {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #4a92ff;
        margin-right: 5px;
    }

    .title-mark.blue {
        background: #4a92ff;
    }

    .title-mark.green {
        background: #00bd85;
    }

    .title-mark.red {
        background: #d75c56;
    }

    .title-mark.yellow {
        background: #cbae5f;
    }

    .module-list-box {
        margin-top: 30px;
    }

    .module-list {
        display: inline-block;
    }

    .module-list li {
        float: left;
        margin-right: 14px;
        position: relative;
        width: 4px;
        height: 77px;
    }

    .module-list li:last-child {
        margin-right: 0px;
    }

    .module-list-single {
        width: 4px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        height: 77px;
        background: #4a92ff;
        position: absolute;
        bottom: 0px;
    }

    .module-list-single.blue {
        background: #4a92ff;
    }

    .module-list-single.green {
        background: #00bd85;
    }

    .module-list-single.red {
        background: #d75c56;
    }

    .module-list-single.yellow {
        background: #cbae5f;
    }

    .global-module-con .col-md-3, .global-module-con .col-md-4 {
        padding: 0px !important;
    }
</style>
<script>
    let screenfull = require('screenfull/dist/screenfull');
    import globalFullPage from './global-full-second'
    import Api from 'src/lib/api'
    import bubble from './bubble.vue'
    import double from './pie-double.vue'
    import ringChart from './ring-chart.vue'
    import riskBubble from './risk-bubble.vue'
    import dangerGrade from './danger-grade.vue'

    let echarts = require('echarts/lib/echarts');
    export default {
        name: "",
        data() {
            return {
                globalFullStatus: false,
                lineData: {
                    name: ["事件数量"],
                    x: '',
                    color: ['#8375d0', "#e96157", "#e77d4e", "#4a8aee", '#0c67ff', '#4a92ff', '#8375d0', '#5dc962', '#008974', '#b06cae'],
                    series: [
                        {data: []},
                    ]
                },
                securityGrade: {
                    total: 0,
                    score: 0,
                    up: 0
                },
                eventRiskTop: [],
                AssetRiskData: '',
                AssetStatus: [],
                curDetailId: '-1',
                eventStaticPie: '',
                // 风险状态
                riskStatusData: '',
                //事件统计
                eventStatic: {
                    wg: 0,
                    rq: 0,
                    bd: 0
                },
                //设备风险指数比例
                dangerGradeValue: '',
                dangerGradeSeries: '',
                //设备事件状况
                assetDetail: {
                    name: ["事件趋势"],
                    x: '',
                    color: ['#8375d0', "#e96157", "#e77d4e", "#4a8aee", '#0c67ff', '#4a92ff', '#8375d0', '#5dc962', '#008974', '#b06cae'],
                    series: [
                        {data: []},
                    ]
                },
                //违规类型统计
                safeErrorType: '',
                //病毒类型统计
                bdErrorType: '',
                //攻击类型统计
                attackErrorType: '',
                 //违规单位top
                captionRisk: {
                    x: '',
                    y: ''
                },
                //病毒单位统计top
                bd_unit_count: {
                    x: '',
                    y: ''
                },
                //攻击源统计top
                attack_srcip_count: {
                    x: '',
                    y: ''
                },
                //被攻击终端top
                attack_dstip_count: {
                    x: '',
                    y: ''
                }
            }
        },
        filters: {
            changeBand(val) {
                if (val < 1024) {
                    return val
                } else if (val >= 1024 && val < 1024 * 1024) {
                    val = (val / 1024).toFixed(1);
                    return val
                } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024)).toFixed(1);
                    return val
                } else if (val >= 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024 * 1024)).toFixed(1);
                    return val
                }
            },
            changeUnit(val) {
                if (val < 1024) {
                    return "b"
                } else if (val >= 1024 && val < 1024 * 1024) {
                    return "Kb"
                } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
                    return "Mb"
                } else if (val >= 1024 * 1024 * 1024) {
                    return "Gb"
                }
            }
        },
        ready: function () {
            let self = this;
            if (screenfull.enabled) {
                screenfull.on('change', function () {
                    if (!screenfull.isFullscreen) {
                        self.globalFullStatus = false;
                    }
                });
            }

            this.getRiskStatus(); //风险状态
            this.getEventStatic(); //事件统计
            this.getAssetDetail(); //设备事件状况
            this.getInternetFlow();//网络流量
            this.getAssetStatus(); //设备状态
            this.getOverallScore();//安全评分
            this.getEventRiskTop();// 风险事件TOP5
            this.getAssetRisk();// 风险资产TOP5
            this.getEventTypeScore();//设备风险指数比例
            this.getSafeEvent(); //安全事件统计
            this.getTop5Static(); // top5统计
            $('#decive-status').slimScroll({
                height: '250',
                position: 'right',
                size: "5px",
                color: '#000',
                wheelStep: 5
            });
        },
        methods: {
            showFullScreen() {
                this.globalFullStatus = true;
                let width = window.screen.width;
                let height = window.screen.height;
                $("#global-full-page").css({"width": width + "px", "height": height + "px"});
                const target = $('#global-full-page')[0];
                if (screenfull.enabled) {
                    screenfull.request(target)
                }
            },
            //获取风险状态
            getRiskStatus() {
                this.$http.post('/api/ssa/new_global/risk_state').then(function (response) {
                    if (response.data.status == 200) {
                        this.riskStatusData = response.data.data;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //事件统计
            getEventStatic() {
                this.$http.post('/api/ssa/new_global/event_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.eventStatic.wg = response.data.data.event_type.norule;
                        this.eventStatic.rq = response.data.data.event_type.attack;
                        this.eventStatic.bd = response.data.data.event_type.viruses;
                        this.eventStaticPie = response.data.data.event_source;
//                        this.threeTypeChart();
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //事件统计 左侧违规、 入侵 、病毒
            threeTypeChart() {
                let self = this;
                let threeTypeChart = echarts.init(document.getElementById('ssa-global-event-number'));
                let myRate1 = 1000;
                let statusOption = {
                    title: [
                        {
                            x: "15%",
                            bottom: 20,
                            text: '违规',
                            textStyle: {
                                fontWeight: 'normal',
                                fontSize: 14,
                                color: "#93a6d8"
                            },
                        }, {
                            x: "45%",
                            bottom: 20,
                            text: '攻击',
                            textStyle: {
                                fontWeight: 'normal',
                                fontSize: 14,
                                color: "#93a6d8"
                            },
                        }, {
                            x: "75%",
                            bottom: 20,
                            text: '病毒',
                            textStyle: {
                                fontWeight: 'normal',
                                fontSize: 14,
                                color: "#93a6d8"
                            },
                        }],
                    tooltip: {
                        show: true,
                        formatter: function (params) {
                            return params.seriesName + '：' + self.changeWanUnit(params.value);
                        },
                    },
                    series: [
                        {
                            type: 'gauge',
                            center: ['50%', '55%'], // 默认全局居中
                            radius: '50%',
                            splitNumber: 10, //刻度数量
                            min: 0,
                            max: 1000,
                            startAngle: 200,
                            endAngle: -20,
                            clockwise: true,
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    width: 1,
                                    shadowBlur: 0,
                                    color: [
                                        [1, '#4a92ff']
                                    ]
                                }
                            },
                            axisTick: {
                                show: true,
                                lineStyle: {
                                    color: '#4a92ff',
                                    width: 1
                                },
                                length: -10,
                                splitNumber: 10
                            },
                            splitLine: {
                                show: true,
                                length: -15,
                                lineStyle: {
                                    color: '#4a92ff',
                                }
                            },
                            axisLabel: {
                                distance: -15,
                                textStyle: {
                                    color: "#4a92ff",
                                    fontSize: "10",
                                }
                            },
                            pointer: { //仪表盘指针
                                show: 0,
                                width: 4,
                            },
                            detail: {
                                show: false,
                            },
                            data: [{
                                name: "",
                                value: myRate1
                            }]
                        }, {
                            name: '入侵',
                            type: 'gauge',
                            startAngle: 200,
                            endAngle: -20,
                            radius: '45%',
                            center: ['50%', '55%'], // 默认全局居中
                            min: 0,
                            max: 1000,

                            axisLine: {
                                show: false,
                                lineStyle: {
                                    width: 10,
                                    shadowBlur: 6,
                                    color: [
                                        [0.33, '#00bd85'],
                                        [0.66, '#dabb61'],
                                        [1, '#e96157']
                                    ]
                                }
                            },
                            axisTick: {
                                show: false,

                            },
                            splitLine: {
                                show: false,
                                length: 20,

                            },

                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: true,
                                width: 4,
                            },
                            detail: {
                                show: true,
                                offsetCenter: [0, '80%'],
                                formatter: function (value) {
                                    return self.changeWanUnit(value);
                                },
                                textStyle: {
                                    fontSize: 16
                                }
                            },
                            itemStyle: {
                                normal: {
                                    color: "#4a92ff",
                                }
                            },
                            data: [{
                                value: self.eventStatic.rq
                            }]
                        }, {
                            type: 'gauge',
                            center: ['20%', '55%'], // 默认全局居中
                            radius: '35%',
                            splitNumber: 10, //刻度数量
                            min: 0,
                            max: 1000,
                            endAngle: 45,
                            clockwise: true,
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    width: 1,
                                    shadowBlur: 0,
                                    color: [
                                        [1, '#4a92ff']
                                    ]
                                }
                            },
                            axisTick: {
                                show: true,
                                lineStyle: {
                                    color: '#4a92ff',
                                    width: 1
                                },
                                length: -10,
                                splitNumber: 10
                            },
                            splitLine: {
                                show: true,
                                length: -15,
                                lineStyle: {
                                    color: '#4a92ff',
                                }
                            },
                            axisLabel: {
                                distance: -15,
                                textStyle: {
                                    color: "#4a92ff",
                                    fontSize: "10",
                                }
                            },
                            pointer: { //仪表盘指针
                                show: 0,
                                width: 4,
                            },
                            detail: {
                                show: false
                            },
                            data: [{
                                name: "",
                                value: myRate1
                            }]
                        }, {
                            name: '违规',
                            type: 'gauge',
                            endAngle: 45,
                            radius: '30%',
                            center: ['20%', '55%'], // 默认全局居中

                            min: 0,
                            max: 1000,

                            axisLine: {
                                show: false,
                                lineStyle: {
                                    width: 10,
                                    shadowBlur: 6,
                                    color: [
                                        [0.33, '#00bd85'],
                                        [0.66, '#dabb61'],
                                        [1, '#e96157']
                                    ]
                                }
                            },
                            axisTick: {
                                show: false,

                            },
                            splitLine: {
                                show: false,
                                length: 20,

                            },

                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: true,
                                width: 4,
                            },
                            detail: {
                                show: true,
                                offsetCenter: [0, '100%'],
                                textStyle: {
                                    fontSize: 16
                                },
                                formatter: function (value) {
                                    return self.changeWanUnit(value);
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: "#4a92ff",

                                }
                            },
                            data: [{
                                value: self.eventStatic.wg
                            }]
                        }, {
                            type: 'gauge',
                            center: ['80%', '55%'], // 默认全局居中
                            radius: '35%',
                            splitNumber: 10, //刻度数量
                            min: 0,
                            max: 1000,
                            startAngle: 140,
                            endAngle: -45,
                            clockwise: true,
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    width: 1,
                                    shadowBlur: 0,
                                    color: [
                                        [1, '#4a92ff']
                                    ]
                                }
                            },
                            axisTick: {
                                show: true,
                                lineStyle: {
                                    color: '#4a92ff',
                                    width: 1
                                },
                                length: -10,
                                splitNumber: 10
                            },
                            splitLine: {
                                show: true,
                                length: -15,
                                lineStyle: {
                                    color: '#4a92ff',
                                }
                            },
                            axisLabel: {
                                distance: -15,
                                textStyle: {
                                    color: "#4a92ff",
                                    fontSize: "10",
                                }
                            },
                            pointer: { //仪表盘指针
                                show: 0,
                                width: 4,
                            },
                            detail: {
                                show: false
                            },
                            data: [{
                                name: "",
                                value: myRate1
                            }]
                        }, {
                            name: '病毒',
                            type: 'gauge',
                            startAngle: 140,
                            endAngle: -45,
                            radius: '30%',
                            center: ['80%', '55%'], // 默认全局居中
                            min: 0,
                            max: 1000,

                            axisLine: {
                                show: false,
                                lineStyle: {
                                    width: 10,
                                    shadowBlur: 6,
                                    color: [
                                        [0.33, '#00bd85'],
                                        [0.66, '#dabb61'],
                                        [1, '#e96157']
                                    ]
                                }
                            },
                            axisTick: {
                                show: false,

                            },
                            splitLine: {
                                show: false,
                                length: 20,

                            },
                            axisLabel: {
                                show: false
                            },
                            pointer: {
                                show: true,
                                width: 4,
                            },
                            detail: {
                                show: true,
                                offsetCenter: [0, '100%'],
                                textStyle: {
                                    fontSize: 16
                                },
                                formatter: function (value) {
                                    return self.changeWanUnit(value);
                                },
                            },
                            itemStyle: {
                                normal: {
                                    color: "#4a92ff",

                                }
                            },
                            data: [{
                                value: self.eventStatic.bd
                            }]
                        }]
                };
                threeTypeChart.setOption(statusOption);
                window.addEventListener('resize', threeTypeChart.resize())
            },
            //事件趋势
            getAssetDetail() {
                this.$http.post('/api/ssa/new_global/assets_event_trend').then(function (response) {
                    if (response.data.status == 200) {
                        this.assetDetail.name = response.data.data.labes;
                        this.assetDetail.series = response.data.data.data;
                        this.assetDetail.x = response.data.data.days;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //网络流量
            getInternetFlow() {
                this.$http.post('/api/ssa/new_global/network_flow').then(function (response) {
                    if (response.data.status == 200) {
                        this.lineData.name = response.data.data.labes;
                        this.lineData.series = response.data.data.data;
                        this.lineData.x = response.data.data.days;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //获取设备状态
            getAssetStatus() {
                this.$http.post('/api/ssa/new_global/asset_status').then(function (response) {
                    if (response.data.status == 200) {
                        this.AssetStatus = response.data.data;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            // 安全评分
            getOverallScore() {
                this.$http.post('/api/ssa/new_global/score').then(function (response) {
                    if (response.data.status == 200) {
                        this.securityGrade.total = response.data.data.total;
                        this.securityGrade.score = response.data.data.score;
                        this.securityGrade.up = response.data.data.up;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            // 风险事件TOP5
            getEventRiskTop() {
                this.$http.post('/api/ssa/new_global/event_risk_top').then(function (response) {
                    if (response.data.status == 200) {
                        this.eventRiskTop = response.data.data;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            // 风险资产TOP5
            getAssetRisk() {
                this.$http.post('/api/ssa/new_global/asset_risk_top').then(function (response) {
                    if (response.data.status == 200) {
                        this.AssetRiskData = response.data.data.reverse();
                        for (let key in this.AssetRiskData) {
                            Object.assign(this.AssetRiskData[key], {symbolSize: Number(key) * 10 + 15})
                        }
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            roundDatas(num) {
                var datas = [];
                for (var i = 0; i < num; i++) {
                    datas.push({
                        name: 'circle' + i
                    });
                }
                return datas;
            },
            //设备风险指数比例
            getEventTypeScore() {
                this.$http.post('/api/ssa/new_global/event_type_score').then(function (response) {
                    if (response.data.status == 200) {
                        let chartData = response.data.data, total = 0, value = [], series = [], name = [];
                        for (let i = 0; i < chartData.length; i++) {
                            value.push(chartData[i].value);
                            series.push({
                                name: chartData[i].name,
                                max: 100
                            });
                        }
                        this.dangerGradeValue = [].concat(value);
                        this.dangerGradeSeries = [].concat(series);
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //统计集合
            getTop5Static() {
                //病毒类型统计
                this.$http.post('/api/ssa/new_global/virus_type_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.bdErrorType = response.data.data;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
                //病毒单位统计top5
                this.$http.post('/api/ssa/new_global/virus_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.bd_unit_count.x = response.data.data.series;
                        this.bd_unit_count.y = response.data.data.lables;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
                //攻击类型统计
                this.$http.post('/api/ssa/new_global/attack_type_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.attackErrorType = response.data.data;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
                //攻击源统计top5
                this.$http.post('/api/ssa/new_global/attack_srcip_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.attack_srcip_count.x = response.data.data.series;
                        this.attack_srcip_count.y = response.data.data.lables;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
                //被攻击终端统计top5
                this.$http.post('/api/ssa/new_global/attack_dstip_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.attack_dstip_count.x = response.data.data.series.reverse();
                        this.attack_dstip_count.y = response.data.data.lables;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //安全事件
            getSafeEvent() {
                //违规类型统计
                this.$http.post('/api/ssa/new_global/foul_type_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.safeErrorType = response.data.data;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
                //违规单位统计top5
                this.$http.post('/api/ssa/new_global/foul_org_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.captionRisk.x = response.data.data.series;
                        this.captionRisk.y = response.data.data.lables;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            showDetail(id) {
                if (this.curDetailId == id) {
                    this.curDetailId = "-1"
                } else {
                    this.curDetailId = id;
                }
            },
            changeWanUnit(val) {
                if (val < 10000) {
                    return val
                } else if (val >= 10000 && val < 10000 * 10000) {
                    val = (val / 10000).toFixed(1);
                    return val + "万"
                } else {
                    val = (val / (10000 * 10000)).toFixed(1);
                    return val + "亿"
                }
            },
            changeWanUnit_total(val) {
                if (val < 10000) {
                    return val
                } else if (val >= 10000 && val < 10000 * 10000) {
                    val = (val / 10000).toFixed(1);
                    return val + "<span style='font-size: 20px' class='d-i-b m-l-3'>万</span>"
                } else {
                    val = (val / (10000 * 10000)).toFixed(1);
                    return val + "<span style='font-size: 20px' class='d-i-b m-l-3'>亿</span>"
                }
            }
        },
        watch: {
            'globalFullStatus': function () {
                if (this.globalFullStatus == false) {
                    screenfull.exit();
                }
            }
        },
        components: {
            globalFullPage,
            bubble,
            double,
            ringChart,
            riskBubble,
            dangerGrade
        }
    }
</script>
