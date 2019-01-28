<template>
    <div class="global-full">
        <div class="global-top-border">
            <div class="global-title">
                <p class="font22 textC head">态势感知平台</p>
                <!--<p class="info textC"><span>全局态势</span></p>-->
            </div>
            <div class="global-logo"></div>
            <div class="global-time">
                <span><i class="ys-icon icon-clock ys-success-color m-r-5"></i><span
                        class="d-i-b p-r-5">{{curDate}}</span><span class="d-i-b p-r-5">{{curWeek}}</span><span
                        class="d-i-b p-r-5">{{curTime}}</span></span>
                <button class="m-l-15" @click="refreshGlobal()">刷新</button>
                <button class="m-l-15" @click="closeFullPage()">关闭</button>
            </div>
        </div>
        <div class="global-border">
            <div class="global-top p-l-10 p-r-10">
                <div class="global-top-left fLeft module-style p-l-15 p-r-15">
                    <div class="safetyScore font-title p-t-20 p-b-10">安全评分</div>
                    <div class="global-bottom-line"></div>
                    <div class="safe-grade-box">
                        <div class="safe-grade-box-bg"></div>
                        <div class="safe-grade-box-point" id="safe-grade-box-point">
                            <div class="light"></div>
                        </div>
                        <div class="title ys-info-color">安全评分</div>
                        <div class="value font36" style="font-family: digi">{{securityGrade}}</div>
                    </div>
                    <div class="p-b-10 m-t-40">
                        <span class="font-title fLeft displayIB m-t-5">事件总量</span>
                        <span class="fRight displayIB m-t-8 ys-error-color">{{securityUp}}</span>
                        <i class="ys-icon icon-downlist-up fRight displayIB m-t-8 ys-error-color"></i>
                        <span class="fRight m-r-5 specialNum displayIB">{{securityTotal}}</span>
                        <div class="clearfix"></div>
                    </div>
                    <div class="global-bottom-line"></div>
                    <div class="amountOfEvents">
                        <div class="amountOfEvents-item fLeft m-t-30">
                            <cirque-chart :id="0" :value="30" :name="'fanghuo'"></cirque-chart>
                        </div>
                        <div class="amountOfEvents-item fLeft m-t-30">
                            <cirque-chart :id="1" :value="40" :name="'fanghuo00'"></cirque-chart>
                        </div>
                        <div class="amountOfEvents-item fLeft m-t-30">
                            <cirque-chart :id=2 :value="50" :name="'11fanghuo'"></cirque-chart>
                        </div>
                        <div class="amountOfEvents-item fLeft m-t-30">
                            <cirque-chart :id="3" :value="60" :name="'fanghuo333'"></cirque-chart>
                        </div>
                        <div class="clear"></div>
                    </div>
                </div>
                <div class="global-top-center fLeft p-l-10 p-r-10">
                    <div class="global-top-center-content module-style p-r-15 p-l-15">
                        <div class="font-title p-t-20 p-b-10">操作访问链路</div>
                        <div class="global-bottom-line"></div>
                        <div id="oprateLine" style="width: 100%; height: 100%; padding-bottom: 30px;">
                            <transfer :width="oprateLineWidth" :id="'opratefull'" :height="oprateLineHeight"
                                      :data="AccessLink"
                                      style="margin: 0px auto;"
                            ></transfer>
                        </div>
                    </div>
                </div>
                <div class="global-top-right fLeft module-style p-l-15 p-r-15">
                    <div class="p-t-20 p-b-10">
                        <span class="font-title">风险资产</span>
                        <span class="font-title font14 m-l-5">TOP 5</span>
                    </div>
                    <div class="global-bottom-line"></div>
                    <div class="m-t-10 m-b-10 global-risk-asset-border">
                        <div id="global-risk-asset" style="width: 100%;height: 290px;"></div>
                    </div>
                    <div class="font-title m-b-10">评分体系</div>
                    <div class="global-bottom-line"></div>
                    <div class="composite-state-box">
                        <div id="composite-state"></div>
                    </div>
                </div>
                <div class="clear"></div>
            </div>
            <div class="global-bottom p-l-10 p-r-10 m-t-10">
                <div class="col-md-4 module-style p-l-15 p-r-15 global-bottom-item">
                    <div class="font-title p-t-10 p-b-10">最新事件</div>
                    <div class="global-bottom-line"></div>
                    <div class="table-item-header">
                        <div class="col-md-2">名称</div>
                        <div class="col-md-3">程序</div>
                        <div class="col-md-3">产生地址</div>
                        <div class="col-md-4">时间</div>
                        <div class="clear"></div>
                    </div>
                    <div class="table-body-border">
                        <div class="table-body" @mouseover="dynamicRolling('', true)" @mouseout="startScroll">
                            <div class="table-item-body" v-for="list in newEvent" :class="$index?'m-t-5':''">
                                <div class="col-md-2 overHidden tdItem" :title="list.type">{{list.type}}</div>
                                <div class="col-md-3 overHidden tdItem" :title="list.event">{{list.event}}</div>
                                <div class="col-md-3 overHidden tdItem" :title="list.addr">{{list.addr}}</div>
                                <div class="col-md-4 overHidden tdItem" :title="list.time">{{list.time}}</div>
                                <div class="clear"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 global-bottom-item">
                    <div class="bottom-center-content module-style">
                        <div class="p-l-15 p-r-15">
                            <div class="font-title p-t-10 p-b-10">事件趋势</div>
                            <div class="global-bottom-line"></div>
                            <div id="whole-net-ssa-trend" style="width:100%;height:220px;"></div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 module-style p-l-15 p-r-15 global-bottom-item">
                    <div class="font-title p-t-10 p-b-10">设备状态</div>
                    <div class="global-bottom-line" id="device-status-full">
                        <table class="ys-table">
                            <thead>
                            <tr>
                                <!-- <th></th> -->

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
                                <td style="text-align: left;">{{list.type}}</td>
                                <td>{{list.num}}</td>
                                <td class="ys-success-color">{{list.normal}}</td>
                                <td class="ys-warn-color">{{list.off}}</td>
                                <td class="ys-error-color">{{list.abnormal}}</td>
                            </tr>
                            <!--
                            <tr class="detail" v-bind:class="[curDetailId == list.type ? 'open' : '' ]"
                                v-for="obj in list.detail">
                                <td class="ys-success-color textC"></td>
                                <td style="text-align: left"><span
                                        class="displayIB textC verticalM m-l-10 m-r-5 ys-success-color font26">·</span>
                                    <span>{{obj.ip}}</span>
                                </td>
                                <td class="textC">{{obj.num}}</td>
                                <td class="ys-success-color textC">{{obj.normal}}</td>
                                <td class="ys-warn-color textC">{{obj.off}}</td>
                                <td class="ys-error-color textC">{{obj.abnormal}}</td>
                            </tr>
                            -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped>
    .global-top-border{
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 10;
    }
    .global-top {
        width: 100%;
        height: 670px;
    }

    .global-border {
        width: 100%;
        position: absolute;
        left: 0;
        bottom: 10px;
    }

    .global-top .global-top-left, .global-top .global-top-right, .global-top .global-top-center, .global-top-center-content {
        height: 100%;
    }

    .global-top-left, .global-top-right {
        width: 19%;
    }

    .global-top-center {
        width: 62%;
    }

    .module-style {
        background: rgba(74, 146, 255, 0.12);
        box-shadow: 0px 0px 10px 0px rgba(74, 146, 255, 1);
        border: 1px solid rgba(74, 146, 255, 1);
    }

    .global-bottom .global-bottom-item {
        height: 261px;
    }

    .bottom-center-content {
        height: 100%;
    }

    .font-title {
        font-size: 16px;
        /*font-family: PingFangSC-Medium;*/
        color: rgba(230, 237, 254, 1);
    }

    .global-bottom-line {
        width: 100%;
        height: 1px;
        background: rgba(74, 146, 255, 0.65);
    }
    #device-status-full{
        background: transparent;
    }
    .p-r-15 {
        padding-right: 15px;
    }

    .m-t-8 {
        margin-top: 8px;
    }

    .specialNum {
        font-size: 24px;
        font-family: digi;
        color: rgba(242, 242, 242, 1);
    }

    .table-item-header div {
        font-size: 12px;
        color: rgba(74, 146, 255, 1);
        text-align: center;
        height: 34px;
        line-height: 34px;
    }

    .table-item-body {
        width: 100%;
        height: 30px;
        background: rgba(74, 146, 255, 0.1);
        border: 1px solid rgba(74, 146, 255, 0.3);
    }

    .table-body-border {
        width: 100%;
        height: 175px;
        overflow: hidden;
        position: relative;
    }
    .table-item-body:hover{
        background: rgba(74, 146, 255, 0.2);
        border: 1px solid rgba(74, 146, 255, 0.3);
    }
    .table-body {
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        /*overflow-x: hidden;
        overflow-y: scroll;*/
    }

    .table-item-body div {
        font-size: 12px;
        color: rgba(230, 237, 254, 1);
        line-height: 30px;
        text-align: center;
    }

    .amountOfEvents-item {
        width: 50%;
        height: 120px;
        text-align: center;
    }
	.tdItem {
		 white-space: nowrap;
		 text-overflow:ellipsis;
		 overflow:hidden;
	}
    .global-risk-asset-border {

    }

    .amountOfEvents-item-text {
        font-size: 12px;
        font-family: PingFangSC-Medium;
        color: rgba(230, 237, 254, 1);
    }

    /*.global-bottom-table{
    display: table;
    width:100%;
  }
  .global-bottom-cell{
    display: table-cell;
  }
  .global-auto-box{
    width:100%;
    height:280px;
    position:relative;
  }
  .global-auto-box-left{
    float: left;
    width:224px;
    height:280px;
    background: url("../../../assets/images/ssa/global-box-bg-left.png");
  }
  .global-auto-box-middle{
    margin-left: 224px;
    margin-right: 14px;
    height:280px;
    background: url("../../../assets/images/ssa/global-box-bg-middle.png") repeat-x;
  }
  .global-auto-box-right{
    float: right;
    width:14px;
    height:280px;
    background: url("../../../assets/images/ssa/global-box-bg-right.png");
  }
  .global-auto-box-inner{
    position: absolute;
    top:0px;
    left:0px;
    width:100%;
  }*/
  .global-auto-box-inner .title{
    height:38px;
    line-height:38px;
    padding-left:23px;
    border-bottom:1px solid rgba(60,150,255,0.65);
    margin-left:10px;
    margin-right:10px;
  }
  .global-auto-box-inner .content{
    padding:15px;
  }
    /*仪表盘*/
    .safe-grade-box {
        width: 100%;
        position: relative;
        margin-top: 25px;
    }

    .safe-grade-box .title {
        width: 100%;
        text-align: center;
        position: absolute;
        top: 72px;
    }

    .safe-grade-box .value {
        width: 100%;
        text-align: center;
        position: absolute;
        top: 105px;
    }

    .safe-grade-box-bg {
        background: url("../../../assets/images/ssa/gauge-bg.png");
        background-size: 220px;
        width: 220px;
        height: 172px;
        margin: 0 auto;
    }

    .safe-grade-box-point {
        height: 146px;
        width: 146px;
        border-radius: 50%;
        position: absolute;
        top: 44px;
        left: 95px;
        transform: rotate(-90deg);
    }

    .safe-grade-box-point .light {
        height: 4px;
        width: 4px;
        position: absolute;
        background: #fff;
        border-radius: 50%;
        top: 26px;
        left: 35px;
        box-shadow: 0 0 15px 5px rgba(0, 192, 255, 0.75);
    }

    @keyframes rond {
        0% {
            transform: rotate(-90deg);
        }
        100% {
            transform: rotate(180deg);
        }
    }

    @-webkit-keyframes rond {
        0% {
            -webkit-transform: rotate(-90deg);
        }
        100% {
            -webkit-transform: rotate(180deg);
        }
    }

    .global-full {
        width: 100%;
        height: 100%;
        background-image: url('../../../assets/images/ssa/global-bg.jpg');
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
        position: relative;
    }

    .global-title {
        height: 100px;
        width: 100%;
        background-image: url('../../../assets/images/ssa/title-bg.png');
        background-position: top center;
        background-size: 100% 104%;
        background-repeat: no-repeat;
    }

    .global-title .head {
        padding-top: 17px;
        text-shadow: 0 0 15px #fff;
    }

    .global-title .info {
        margin-top: -30px;
    }

    .global-title .info span {
        display: inline-block;
        width: 258px;
        height: 128px;
        line-height: 128px;
        color: #79eeff;
        background-image: url('../../../assets/images/ssa/top-title-bg.png');
    }

    .global-logo {
        position: absolute;
        width: 195px;
        height: 85px;
        left: 0px;
        top: 0px;
        background: url("../../../assets/images/ssa/logo-bg.png");
    }

    .global-map-title {
        width: 441px;
        height: 63px;
        line-height: 63px;
        background: url("../../../assets/images/ssa/map-title-bg.png") no-repeat;
        background-size: 441px;
        position: absolute;
        top: 145px;
        left: 50%;
        margin-left: -220px;
    }

    .global-time {
        position: absolute;
        right: 13px;
        top: 10px;
    }

    .global-time button {
        border: none;
        width: 80px;
        height: 34px;
        text-align: center;
        line-height: 34px;
        background: url("../../../assets/images/ssa/close-btn-bg.png");
    }

    .global-left {
        position: absolute;
        left: 5px;
        bottom: 300px;
    }

    .global-box .content {
        padding: 15px;
        position: relative;
    }

    .global-box .content .chart {
        margin: 0 auto;
    }

    .global-box.global-box-1 {
        background: url("../../../assets/images/ssa/box-bg-1.png");
        width: 334px;
        height: 280px;
    }

    .global-box .title {
        height: 38px;
        line-height: 38px;
        padding-left: 33px;
    }

    /*评分体系KDA*/
    .composite-state-box {
        width: 100%;
        height: 270px;
        position: relative;
    }

    #composite-state-bg {
        position: absolute;
        top: 50px;
        left: 69px;
        background: url("../../../assets/images/ssa/pie-chart-bg-2.png");
        background-size: 202px;
        width: 202px;
        height: 198px;
    }

    #composite-state {
        position: absolute;
        top: 30px;
        left: 0px;
        width: 100%;
        height: 230px;
    }

    #composite-state-tag {
        position: absolute;
        top: 3px;
        left: 12px;
        background: url("../../../assets/images/ssa/grade-tag.png") no-repeat;
        background-size: 99px;
        width: 99px;
        height: 67px;
        font-size: 14px;
        padding-top: 9px;
        padding-left: 21px;
    }

    /*攻击次数*/
    .attck-time-box {
        position: relative;
    }

    .attck-time-bg {
        width: 170px;
        height: 170px;
        margin: 10px auto;
        background: url("../../../assets/images/ssa/pie-chart-bg.png") no-repeat;
        background-size: 170px;
    }

    .attck-time-rate {
        width: 300px;
        height: 300px;
        margin: 0 auto;
        position: absolute;
        top: -21px;
        left: 17px;
    }

    /*攻击资源*/
    .attck-source-box {
        position: relative;
    }

    .attck-source-chart {
        width: 260px;
        height: 180px;
        margin-left: 20px;
    }

    /*蠕虫感染总数*/
    .worm-infect-box {
        position: relative;
    }

    .worm-infect-bg {
        width: 170px;
        height: 170px;
        margin: 10px auto;
        background: url("../../../assets/images/ssa/pie-chart-bg.png") no-repeat;
        background-size: 170px;
    }

    .worm-infect-chart {
        width: 220px;
        height: 220px;
        margin: 0 auto;
        position: absolute;
        top: 20px;
        left: 54px;
    }

    .global-map {
        position: absolute;
        left: 320px;
        right: 350px;
        bottom: 270px;
        top: 80px;
    }

    /*.global-bottom{
    position: absolute;
    left:5px;
    bottom:0px;
    width:100%;
  }*/
    .global-right {
        position: absolute;
        right: 0px;
        bottom: 300px;
    }

    .global-trend-box {
        width: 332px;
        height: 210px;
        background: url("../../../assets/images/ssa/global-trend-box-bg.png") no-repeat;
        background-size: 332px;
        float: right;
        margin-bottom: 10px;
    }

    .attack-detail-wrap {
        width: 529px;
    }

    .attack-detail-con {
        height: 142px;
        display: inline-block;
        position: relative;
        float: right;
    }

    .attack-detail-con.host {
        width: 401px;
        background: url("../../../assets/images/ssa/platform-bg-1.png") no-repeat;
        background-size: 401px;
    }

    .attack-detail-con.app {
        width: 465px;
        background: url("../../../assets/images/ssa/platform-bg-2.png") no-repeat;
        background-size: 465px;
        margin-top: 10px;
    }

    .attack-detail-con.net {
        width: 529px;
        background: url("../../../assets/images/ssa/platform-bg-3.png") no-repeat;
        background-size: 529px;
        margin-top: 10px;
    }

    .attack-detail-con .tag {
        position: absolute;
        top: 15px;
        left: -40px;
        background: url("../../../assets/images/ssa/grade-tag.png") no-repeat;
        background-size: 99px;
        width: 99px;
        height: 67px;
        font-size: 14px;
        padding-top: 9px;
        text-align: center;
    }

    .attack-detail-module {
        width: 130px;
        display: inline-block;
        float: left;
    }

    .attack-detail-module .head {
        padding-top: 20px;
        text-align: center;
        padding-left: 50px;
    }

    .attack-detail-module .icon {
        padding-top: 4px;
        text-align: center;
        padding-left: 25px;
        height: 64px;
        line-height: 64px;
    }

    .attack-detail-module .num {
        text-align: center;
    }

    .attack-detail-module .num span {
        font-size: 24px;
        margin-right: 3px;
    }

    .hole-rate-box {
        width: 96px;
        height: 96px;
    }

    .global-hole-tab-box {
        width: 424px;
        height: 210px;
        background: url("../../../assets/images/ssa/global-hole-tab-a.png") no-repeat;
        background-size: 424px;
    }

    .global-hole-tab-box .title {
        height: 38px;
        line-height: 38px;
        padding-left: 33px;
    }

    .global-hole-tab-box .content {
        padding: 15px 40px;
    }

    .hole-rate-box {
        width: 96px;
        height: 96px;
        background: url("../../../assets/images/ssa/hole-rate-bg.png") no-repeat;
        background-size: 96px;
    }

    .danger-hole-box {
        width: 96px;
        height: 96px;
        background: url("../../../assets/images/ssa/hole-num-bg.png") no-repeat;
        background-size: 96px;
    }

    .danger-hole-box .text {
        height: 96px;
        line-height: 98px;
        text-align: center;
        font-family: digi;
        font-size: 24px;
    }

    .danger-hole-asset-box {
        background: url("../../../assets/images/ssa/hole-asset-bg.png") no-repeat;
        background-size: 96px;
    }

    .big-hole-top5-box ul {
        margin-top: -5px;
    }

    .big-hole-top5-box ul li {
        padding-bottom: 4px;
    }

    .big-hole-top5-box ul li .top-title {
        padding-left: 0px;
        font-size: 14px;
        font-weight: bold;
        font-style: italic;
        text-shadow: 0 1px #e96157, 1px 0 #e96157, -1px 0 #e96157, 0 -1px #e96157;
    }

    .attack-info-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0px 2px;
    }

    .attack-info-table tr th {
        background: rgba(74, 146, 255, 0.2);
        padding-top: 8px;
        padding-bottom: 8px;
        text-align: center;
        color: #93a6d8;
    }

    .attack-info-table tr th:first-child, .attack-info-table tr td:first-child {
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
    }

    .attack-info-table tr th:last-child, .attack-info-table tr td:last-child {
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }

    .attack-info-table tr td {
        background: rgba(74, 146, 255, 0.1);
        padding-top: 10px;
        padding-bottom: 10px;
        text-align: center;
        collapse: 1;
    }
</style>
<script>
    import Api from 'src/lib/api'
    import transfer from './transfer.vue'

    let echarts = require('echarts/lib/echarts');
    export default {
        name: "global-full-page",
        props: {
            show: {
                default: false
            }
        },
        data() {
            return {
                curDate: "",
                curWeek: "",
                curTime: "",
                realMapData: [],
                securityGrade: 0,
                securityTotal: 0,
                securityUp: 0,
                attackInfoRealData: [],
                AssetStatus: [],
                AccessLink: {},
                curDetailId: '-1',
                oprateLineWidth: '500px',
                oprateLineHeight: '460px',
                AssetRiskData: [],
                newEvent:[{
                    type: 'a',
                    event: 'b',
                    addr: 'c',
                    time: 'd'
                },{
                    type: '1',
                    event: '2',
                    addr: '1',
                    time: '1'
                },{
                    type: '2',
                    event: '2',
                    addr: '2',
                    time: '2'
                },{
                    type: '3',
                    event: '3',
                    addr: '3',
                    time: '3'
                },{
                    type: 'a',
                    event: 'b',
                    addr: 'c',
                    time: 'd'
                },{
                    type: 'a',
                    event: 'b',
                    addr: 'c',
                    time: 'd'
                },{
                    type: 'a',
                    event: 'b',
                    addr: 'c',
                    time: 'd'
                },{
                    type: 'a',
                    event: 'b',
                    addr: 'c',
                    time: 'd'
                },{
                    type: 'a',
                    event: 'b',
                    addr: 'c',
                    time: 'd'
                },{
                    type: 'a',
                    event: 'b',
                    addr: 'c',
                    time: 'd'
                }],
                scrollTimer: '',
                index: 0,
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
            },
            range(val) {
                if (val >= 1000) {
                    return "999+"
                } else {
                    return val
                }
            }
        },
        ready: function () {
            $('#device-status-full').slimScroll({
                height: '215',
                position: 'right',
                size: "5px",
                color: '#000',
                wheelStep: 5
            });
            this.$nextTick(() => {
                this.oprateLineWidth = $('#oprateLine').width() + 'px';
                this.oprateLineHeight = $('#oprateLine').height() + 'px';
                window.addEventListener('resize', () => {
                    this.oprateLineWidth = $('#oprateLine').width() + 'px';
                    this.oprateLineHeight = $('#oprateLine').height() + 'px';
                })
            });
            let self = this ;
            this.scrollTimer = setInterval(function () {
                self.dynamicRolling(self.index, false)
            }, 3000);
        },
        components: {
            transfer
        },
        methods: {
            //动态滚动
            dynamicRolling (index, stop) {
                if(stop){
                    window.clearInterval(this.scrollTimer);
                    return false;
                }else{
                    this.index = index + 1 ;
                }
                $('.table-body').animate({
                    top: -(35 * index)+'px'
                }, 500);
                if(index === this.newEvent.length-1){
                    this.index = 0 ;
                }
            },
            startScroll () {
                let self = this ;
                this.scrollTimer = setInterval(function () {
                    self.dynamicRolling(self.index, false)
                }, 3000);
            },
            //当前时间
            setRealTime() {
                let self = this;

                function run() {
                    var time = new Date();//获取系统当前时间
                    var year = time.getFullYear();
                    var month = time.getMonth() + 1;
                    var date = time.getDate();//系统时间月份中的日
                    var day = time.getDay();//系统时间中的星期值
                    var weeks = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
                    var week = weeks[day];//显示为星期几
                    var hour = time.getHours();
                    var minutes = time.getMinutes();
                    var seconds = time.getSeconds();
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
                    self.curDate = year + "年" + month + "月" + date + "日";
                    self.curWeek = week;
                    self.curTime = hour + ":" + minutes + ":" + seconds;
                }

                setInterval(function () {
                    run()
                }, 1000)
            },
            //链路
            getAccessLink() {
                this.$http.post('/api/ssa/new_global/access_link').then(function (response) {
                    if (response.data.status == 200) {
                        this.AccessLink = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //获取设备状态
            getAssetStatus() {
                this.$http.post('/api/ssa/new_global/asset_status').then(function (response) {
                    if (response.data.status == 200) {
                        this.AssetStatus = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //攻击信息数据 - 废弃
            getAttackInfoData() {
                let self = this;
                if (window.WebSocket != undefined) {
                    let host = '10.10.10.33';
                    //let host=window.location.host;
                    var connection = new WebSocket('ws://' + host + '/api/ssa/websocket/security/attack_map');
                    //console.log(connection.readyState);
                    //握手协议成功以后，readyState就从0变为1，并触发open事件
                    connection.onopen = function wsOpen(event) {
                        connection.send('向客户端发送消息');
                    };
                    connection.onmessage = function wsMessage(event) {
                        let data = JSON.parse(event.data);
                        if (self.attackInfoRealData.length > 4) {
                            self.attackInfoRealData.shift()
                        }
                        self.attackInfoRealData.push(data);
                    };//监听
                    connection.onclose = function wsClose() {
                        console.log("Closed");
                    };//关闭WebSocket连接，会触发close事件。
                    connection.onerror = wsError;//出现错误
                    function wsError(event) {
                        console.log("Error: " + event.data);
                    }
                }
            },
            //分数
            getSecurityGrade() {
                this.$http.post('/api/ssa/new_global/score').then(function (response) {
                    if (response.data.status == 200) {
                        this.securityGrade = response.data.data.score;
                        this.securityTotal = response.data.data.total;
                        this.securityUp = response.data.data.up;
                        let deg = 2.43 * this.securityGrade - 90;
//                        $("#safe-grade-box-point").css({"transform": "rotate(" + deg + "deg)"})
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //评分体系
            getDangerGrade() {
                this.$http.post('/api/ssa/new_global/event_type_score').then(function (response) {
                    if (response.data.status == 200) {
                        let chartData = response.data.data;
                        let compositeStateChart = echarts.init(document.getElementById('composite-state'));
                        let lineStyle = {
                            normal: {
                                width: 1,
                                opacity: 0.5
                            }
                        };

                        let option = {
                            tooltip: {
                                trigger: 'item',
                                backgroundColor: 'rgba(74, 146, 255, 0.2)',
                                border: '1px solid rgba(74, 146, 255, 0.3)'
                            },
                            radar: {
                                indicator: [
                                    {name: '防火墙事件', max: 1000},
                                    {name: '隔离事件', max: 1000},
                                    {name: 'SM扫描事件', max: 1000},
                                    {name: '摆渡机事件', max: 1000},
                                    {name: '终端事件', max: 1000},
                                ],
	                            radius: '65%',
                                shape: 'circle',
                                splitNumber: 3,
                                name: {
                                    textStyle: {
                                        color: 'rgba(230,237,254,1)'
                                    }
                                },
                                splitLine: {
                                    lineStyle: {
                                        color: 'rgba(89,111,155,1)'
                                    }
                                },
                                splitArea: {
                                    show: true,
                                    areaStyle: {
                                        color: 'rgba(74,146,255,0)'
                                    }
                                },
                                axisLine: {
                                    show: false,
                                    lineStyle: {
                                        color: 'rgba(238, 197, 102, 0.5)'
                                    }
                                },
                            },
                            series: [
                                {
                                    name: '评分体系',
                                    type: 'radar',
                                    lineStyle: lineStyle,
                                    symbol: 'circle',
                                    symbolSize: 5,
                                    data: [[chartData.firewall, chartData.gl, chartData.sm, chartData.zd,chartData.bd]],
                                    itemStyle: {
                                        normal: {
                                            color: 'rgb(0, 187, 133)'
                                        }
                                    },
                                    areaStyle: {
                                        normal: {
                                            opacity: 0.25,
                                            color: 'rgba(0, 187, 133, 0.4)',
                                        }
                                    },
                                }
                            ]
                        };
                        compositeStateChart.setOption(option);
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //获取新事件
            getNewEvent(){
                this.$http.post('/api/ssa/new_global/new_event').then(function (response) {
                    if (response.data.status == 200) {
                        this.newEvent = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            // 事件趋势
            getWholeNetTrend() {
                this.$http.post('/api/ssa/new_global/event_trend').then(function (response) {
                    if (response.data.status == 200) {
                        let trendData = response.data.data;
                        let trendChart = echarts.init(document.getElementById('whole-net-ssa-trend'));
                        let trendOption = {
					        tooltip: {
					            trigger: 'axis',
                                backgroundColor: 'rgba(74, 146, 255, 0.2)',
                                border: '1px solid rgba(74, 146, 255, 0.3)',
                                formatter: '{a} <br /> {b}: {c}'
					        },
                            xAxis: {
                                type: 'category',
                                data: trendData.x,
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
                                splitLine: {
                                    show: true,
                                    interval: 0,
                                    lineStyle: {
                                        color: "#46578e",
                                        opacity: "0.75"
                                    }
                                },
                                axisLabel: {textStyle: {color: "#93a6d8"}}
                            },
                            grid: {
                                top: '15',
                                bottom: '20',
                                left: 5,
                                right: 5,
                                containLabel: true
                            },
                            yAxis: {
                                type: 'value',
                                axisLabel: {
                                    show: false,
                                },
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
                                splitLine: {
                                    show: false
                                }
                            },
                            series: [{
					            name: '事件趋势',
                                data: trendData.y,
                                type: 'line',
                                smooth: true,
                                lineStyle: {
                                    color: {
                                        type: 'linear',
                                        x: 0,
                                        y: 0,
                                        x2: 0,
                                        y2: 1,
                                        colorStops: [{
                                            offset: 0, color: '#dabb61' // 0% 处的颜色
                                        }, {
                                            offset: 1, color: '#e96157' // 100% 处的颜色
                                        }],
                                        globalCoord: false // 缺省为 false
                                    }
                                }
                            }]
                        };
                        trendChart.setOption(trendOption);
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            // 风险资产TOP5
            getAssetRisk() {
                this.$http.post('/api/ssa/new_global/asset_risk_top').then(function (response) {
                    if (response.data.status == 200) {
                        this.AssetRiskData = response.data.data;
                        for (let key in this.AssetRiskData){
                            Object.assign(this.AssetRiskData[key], {symbolSize: Number(key)*10 + 15})
                        }
                        this.showRiskAsset();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            // 风险资产TOP5 echart 生成
            showRiskAsset() {
                let self = this;
                let riskAssetChart = echarts.init(document.getElementById('global-risk-asset'));
                let option = {
                    roam: false, //鼠标缩放及平移
                    focusNodeAdjacency: false, //是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点
                    tooltip: {
                        show: true,
                        trigger: 'item',
                        formatter: '{b} <br />风险：{c}',
                        backgroundColor: 'rgba(74, 146, 255, 0.2)',
                        border: '1px solid rgba(74, 146, 255, 0.3)'
                    },
                    series: [{
                        name: '',
                        type: 'pie',
                        startAngle: 0,
                        hoverAnimation: false,
                        radius: ['80%', '80%'],
                        center: ['50%', '50%'],
                        data: self.AssetRiskData,
                        itemStyle: {
                            normal: {
                                label: {
                                    show: false
                                }
                            },
                            emphasis: {
                                color: 'rgba(154,188,238,1)'
                            }
                        }
                    }, {
                        type: 'graph',
                        tooltip: {},
                        ribbonType: false,
                        layout: 'circular',
                        hoverAnimation: false,
                        width: '80%',
                        height: '80%',
                        circular: {
                            rotateLabel: true
                        },
                        symbolSize: 1,
                        data: this.roundDatas(300),
                        itemStyle: {
                            normal: {
                                label: {
                                    show: false
                                },
                                color: 'rgba(255, 255, 255, 0.3)',
                            },
                            emphasis: {
                                label: {
                                    show: false,
                                }
                            }
                        },
                    }, {
                        type: 'graph',
                        tooltip: {},
                        ribbonType: true,
                        layout: 'circular',
                        width: '80%',
                        height: '80%',
                        color: ['rgba(0, 187, 133, 0.2)'],
                        circular: {
                            rotateLabel: true
                        },
                        symbolSize: 30,
                        edgeSymbol: ['circle'],
                        edgeSymbolSize: [8, 10],
                        edgeLabel: {
                            normal: {
                                textStyle: {
                                    fontSize: 13,
                                    fontWeight: 'bold',
                                    fontFamily: '宋体'
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderColor: 'rgb(0, 187, 133)',
                                borderWidth: 2,
                                label: {
                                    rotate: true,
                                    show: false,
                                    textStyle: {
                                        color: 'rgba(154,188,238,1)',
                                    },
                                    formatter: '{b}\n风险：{c}',
                                },
                            },
                            emphasis: {
                                label: {
                                    show: false
                                }
                            }
                        },
                        data: self.AssetRiskData,
                    }]
                };
                riskAssetChart.setOption(option);
            },

            refreshGlobal() {
                this.setRealTime()
                this.getAccessLink(); //链路
                this.getAssetStatus(); //设备状态
                this.getSecurityGrade()
                this.getDangerGrade()
                this.getAssetRisk();
                this.getNewEvent();
                this.getWholeNetTrend()
            },
            closeFullPage() {
                this.show = false
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
            //展开详情
            showDetail(id) {
                if (this.curDetailId == id) {
                    this.curDetailId = "-1"
                } else {
                    this.curDetailId = id;
                }
            },
        },
        watch: {
            'show': function () {
                if (this.show) {
                    this.getAccessLink(); //链路
                    this.getAssetStatus(); //设备状态
                    this.setRealTime()
                    this.getSecurityGrade()
                    this.getDangerGrade()
                    this.getWholeNetTrend()
                    this.getNewEvent()
                    this.getAssetRisk()
                }
            }
        },
        destroyed: function () {
            window.clearInterval(this.scrollTimer);
        }
    }
</script>
