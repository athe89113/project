<style scoped>
	@font-face {
		font-family: AliHYAiHei-Beta;
		src: url('../../../assets/fonts/AliHYAiHei-Beta.ttf');
		font-weight: 200;
		font-style: normal;
	}
	#rem-border {
		width: 100%;
		height: 100%;
		font-size: 0.12rem !important;
	}
	.global-full{
		width: 100%;
		height: 100%;
		background-image: url('../../../assets/images/ssa/global_bg11.jpg');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		position: relative;
	}
	.global{
		width: 100%;
		height: 100%;
		position: absolute;
		top: 0;
		left: 0;
		z-index: 10;
	}
	.header{
		position: relative;
		top: 0;
		left: 0;
		width: 100%;
	}
	.header .logo{
		width: 0.3rem;
		height: 0.3rem;
		text-align: center;
		color: #fff;
	}
	.header img{
		width: 0.35rem;
	}
	.title-count{
		font-size: 0.36rem;
		font-family: digi;
		color:rgba(248,157,68,1);
	}
	.global-count-border{
		border-bottom: 1px solid rgba(248,157,68,1);
		margin-top: 0.08rem;
	}
	.global-time {
        position: absolute;
        right: 0.13rem;
        top: 0.12rem;
		z-index: 10;
    }
    .global-time button {
        border: none;
        width: 0.8rem;
        height: 0.34rem;
        text-align: center;
        line-height: 0.34rem;
        background: url("../../../assets/images/ssa/close-btn-bg.png");
	    background-size: 100% 100%;
	    background-repeat: no-repeat;
    }
	.global-time-time{
		color: rgba(74,146,255,1);
	}
	.WP30{
		width: 30%;
	}
	.WP40{
		width: 40%;
	}
	.headerCenter img{
		margin-top: 0.05rem;
	}
	.contentLeft, .contentRight{
		width: 18%;
	}
	.contentCenter{
		width: 64%;
		z-index: 11;
	}
	.global-title{
		font-size: 0.12rem;
		height: 0.28rem;
		line-height: 0.28rem;
		border-top:1px solid rgba(255,255,255,0.3);
		border-bottom:1px solid rgba(255,255,255,0.3);
	}
	.misdeeds-type-bg,.thing-count-bg{
		width: 100%;
		height: 3.3rem;
		position: absolute;
		top: 0;
		left: 0;
		z-index: 0;
		background-image: url('../../../assets/images/ssa/pieCenter.png');
		background-repeat: no-repeat;
	}
	.misdeeds-type-bg{
		background-position: 55px 65px;
		background-size: 90px 90px;
	}
	.thing-count-bg{
		background-position: 40px 70px;
		background-size: 80px 80px;
	}
	.positionRl{
		position: relative;
	}
	.table-item-header div {
        font-size: 0.12rem;
        color: rgba(74, 146, 255, 1);
        text-align: center;
        height: 0.34rem;
        line-height: 0.34rem;
    }
    .table-item-body {
        width: 100%;
        height: 0.3rem;
        background: rgba(74, 146, 255, 0.1);
        border: 1px solid rgba(74, 146, 255, 0.3);
    }
    .table-body-border {
        width: 100%;
        height: 1.75rem;
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
        font-size: 0.12rem;
        color: rgba(230, 237, 254, 1);
        line-height: 0.3rem;
        text-align: center;
    }
	.tdItem {
		 white-space: nowrap;
		 text-overflow:ellipsis;
		 overflow:hidden;
	}
	#device-status-full{
        background: transparent;
    }
    .ys-table tr.detail td {
        text-align: center;
    }
	.content{
		width: 100%;
		height: 100%;
		position: relative;
		bottom: -0.2rem;
		left: 0;
	}
	.WP50{
		width: 50%;
	}
	.contentCenterLeft, .contentCenterCenter, .contentCenterRight{
		height: 4.85rem;
	}
	.contentCenterLeft{
		background-image: url('../../../assets/images/ssa/new-global-left-part.png');
		background-size: 137% 110%;
		background-repeat: no-repeat;
		background-position: -0.79rem -0.49rem;
	}
	.contentCenterRight{
		background-image: url('../../../assets/images/ssa/new-global-right-part.png');
		background-size: 135% 110%;
		background-repeat: no-repeat;
		background-position: -0.9rem -0.5rem;
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
        margin-top: 10px;
    }
	.diverge-top-line{
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 133px;
		background-image: url('../../../assets/images/ssa/diverge-line.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		z-index: 3;
	}
	.global-top-left-split{
		position: absolute;
		top: 0;
		left: 0;
		width: 30%;
		height: 60px;
		background-image: url('../../../assets/images/ssa/global-top-left-split.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		z-index: 4;
	}
	.global-top-right-split{
		position: absolute;
		top: 0;
		right: 0;
		width: 30%;
		height: 60px;
		background-image: url('../../../assets/images/ssa/global-top-right-split.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		z-index: 4;
	}
	.content-top{
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		z-index: 11;
	}
	.content-footer{
		position: absolute;
		bottom: 60px;
		left: 0;
		width: 100%;
		z-index: 1;
	}
	.content-middle{
		position: absolute;
		height: 60px;
		bottom: 540px;
		left: 0;
		width: 100%;
		z-index: 2;
	}
	.contentCenterCenter{
		position: relative;
	}
	.earth-bottom, .earth-border, .earth-search{
		width: 100%;
		height: 100%;
		border-radius: 50%;
		position: absolute;
		top: 0;
		left: 0;
		text-align: center;
	}
	.earth-bottom{
		z-index: 1;
	}
	.earth-bottom img{
		margin-top: 54px;
	}
	.earth-search img{
		margin-top: 13px;
	}
	.earth-search{
		z-index: 3;
	}
	.earth-border{
		z-index: 2;
	}
	.earth-border img{
		width: 345px !important;
		height: 345px !important;
		margin-top: 41px;
	}
	#global-safe-result{
		position: absolute;
		top: 0;
		left: 0;
		z-index: 5;
	}
	.contentCenterCenterTitle{
		position: absolute;
		bottom: 0;
		left: 0;
		width: 100%;
	}
	.headerRight{
		height: 60px;
		position: relative;
	}
	.rotate-global{
        animation: mymove 3s linear infinite normal;
    }
    @keyframes mymove {
        from {transform: rotateZ(0deg)}
        to {transform:rotateZ(360deg)}
    }
</style>
<template>
	<div id="rem-border" style="font-size: 100px;">
		<div class="global-full">
		<div class="global">
			<div class="header">
				<div class="WP30 headerLeft p-t-5 p-l-10 p-b-10 fLeft">
					<img class="fLeft logo m-t-8" src="../../../assets/images/ssa/global-full-logo.png" alt="">
					<div class="fLeft m-l-10 m-t-8">
						<div class="font14">安全态势分析</div>
						<div class="font12 m-t-5">Security situation analysis</div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="WP40 headerCenter fLeft center m-t-10">
					<div class="fLeft p-l-10 p-r-10 col-md-4" style="text-align: center">
						<div style="display: inline-block">
							<img class="fLeft" src="../../../assets/images/ssa/global_warm.png" alt="">
							<div class="fLeft m-l-10 p-r-5 global-count-border">
								<span class="font12">违规</span>
								<span class="title-count m-l-10">{{eventStatic.wg | formatterBigCoiunt}}</span>
							</div>
							<div class="clearfix"></div>
						</div>
					</div>
					<div class="fLeft p-l-10 p-r-10 col-md-4" style="text-align: center">
						<div style="display: inline-block">
							<img class="fLeft" src="../../../assets/images/ssa/global_bad.png" alt="">
							<div class="fLeft m-l-10 p-r-5 global-count-border">
								<span class="font12">入侵</span>
								<span class="title-count m-l-10">{{eventStatic.rq | formatterBigCoiunt}}</span>
							</div>
							<div class="clearfix"></div>
						</div>
					</div>
					<div class="fLeft p-l-10 p-r-10 col-md-4" style="text-align: center">
						<div style="display: inline-block">
							<img class="fLeft" src="../../../assets/images/ssa/du.png" alt="">
							<div class="fLeft m-l-10 p-r-5 global-count-border">
								<span class="font12">病毒</span>
								<span class="title-count m-l-10">{{eventStatic.bd | formatterBigCoiunt}}</span>
							</div>
							<div class="clearfix"></div>
						</div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="WP30 headerRight fRight">
					<div class="fRight global-time">
						<span class="global-time-time"><span
		                        class="d-i-b p-r-5">{{curDate}}</span><span class="d-i-b p-r-5">{{curWeek}}</span><span
		                        class="d-i-b p-r-5">{{curTime}}</span></span>
		                <button class="m-l-15" @click="refreshGlobal()">刷新</button>
		                <button class="m-l-15" @click="closeFullPage()">关闭</button>
					</div>
				</div>
				<div class="clearfix"></div>
			</div>
			<div class="content">
				<div class="content-top">
					<div class="contentLeft fLeft p-l-10">
							<div class="global-title">
									<div class="fLeft">风险资产</div>
									<div class="fRight">TOP5</div>
									<div class="clearfix"></div>
								</div>
							<div>
								<global-full-bar :id="'ssa-global-full-risk'"
										                :height="'150px'"
										                :start-color="'rgba(49,100,255,1)'"
										                :end-color="'rgba(0,186,255,1)'"
										                :x="eventRiskTop.x"
										                :need="false"
										                :y="eventRiskTop.y"></global-full-bar>
							</div>
							<div class="global-title">
									<div class="fLeft">部门风险统计</div>
									<div class="fRight">TOP5</div>
									<div class="clearfix"></div>
								</div>
							<div class="m-t-5">
								<global-full-bar :id="'ssa-global-full-unit-count'"
										                 :height="'150px'"
										                :start-color="'rgba(49,100,255,1)'"
										                :end-color="'rgba(0,186,255,1)'"
										                :x="orgRiskCount.x"
										                :need="false"
										                :y="orgRiskCount.y"></global-full-bar>
								</div>
						</div>
					<div class="contentCenter fLeft p-l-10 p-r-10">
						<div class="fLeft contentCenterLeft WP30">
							<div class="security-grade-box" style="margin-top: 100px;margin-bottom: 30px;">
								<div class="title ys-info-color ">安全评分</div>
								<div class="grade">{{securityGrade.score | formatterBigCoiunt}}</div>
							</div>
							<div class="font18" style="text-align: center">安全评分</div>
						</div>
						<div class="fLeft contentCenterCenter WP40">
							<div class="m-t-5" id="global-safe-result" style="width: 100%; height: 463px;"></div>
							<div class="earth-bottom">
								<img src="../../../assets/images/ssa/earthPie.png" alt="">
							</div>
							<div class="earth-border">
								<img src="../../../assets/images/ssa/pieBorder.png" alt="">
							</div>
							<div class="earth-search">
								<img class="rotate-global" src="../../../assets/images/ssa/pieSearch.png" alt="">
							</div>
							<div class="font18 contentCenterCenterTitle" style="text-align: center">安全检测结果统计</div>
						</div>
						<div class="fLeft contentCenterRight WP30">
							<div id="global-rating-system" style="height: 220px;width: 100%; margin-top: 80px;"></div>
							<div class="font18" style="text-align: center">评分体系</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="contentRight fRight p-r-10">
						<div class="global-title">
							<div class="fLeft">违规类型</div>
							<div class="clearfix"></div>
						</div>
						<div>
							<div class="m-t-5 positionRl" style="height: 220px;">
								<global-full-pie :id="'ssa-global-full-misdeeds-type'"
								                :height="'220px'"
									            :x="'right'"
									            :y="'center'"
									            :position="['100', '50%']"
									            :name="'违规类型'"
								                :data="outLineType"></global-full-pie>
								<div class="misdeeds-type-bg"></div>
							</div>
						</div>
						<div class="global-title">
							<div class="fLeft">攻击源统计</div>
							<div class="fRight">TOP5</div>
							<div class="clearfix"></div>
						</div>
						<global-full-bar :id="'ssa-global-full-fight-count'"
								                :height="'150px'"
								                :start-color="'rgba(237,114,44,1)'"
								                :end-color="'rgba(231,180,52,1)'"
								                :x="attackSrcipCount.x"
								                :y="attackSrcipCount.y"></global-full-bar>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="content-middle">
					<img class="fLeft" style="width: 30%" src="../../../assets/images/ssa/global-bottom-left-split.png" alt="">
					<img class="fRight" style="width: 30%" src="../../../assets/images/ssa/global-bottom-right-split.png" alt="">
				</div>
				<div class="content-footer">
					<div class="contentLeft fLeft p-l-10">
						<div class="global-title" style="margin-top: 70px;">
							<div class="fLeft">违规单位</div>
							<div class="fRight">TOP5</div>
							<div class="clearfix"></div>
						</div>
						<div style="height: 220px;">
							<global-full-bar :id="'ssa-global-full-misdeeds-unit'"
							                :height="'160px'"
							                :start-color="'rgba(49,100,255,1)'"
							                :end-color="'rgba(0,186,255,1)'"
							                :x="terminal_foul_org.x"
							                :y="terminal_foul_org.y"></global-full-bar>
						</div>
						<div class="global-title">
							<div class="fLeft">终端操作违规</div>
							<div class="fRight">TOP5</div>
							<div class="clearfix"></div>
						</div>
						<div class="m-t-5">
							<global-full-bar :id="'ssa-global-full-terminal-bad'"
							                :height="'150px'"
							                :start-color="'rgba(49,100,255,1)'"
							                :end-color="'rgba(0,186,255,1)'"
							                :x="foulOperation.x"
							                :y="foulOperation.y"></global-full-bar>
						</div>
					</div>
					<div class="contentCenter fLeft p-r-10 p-l-10">
						<div class="global-title" style="margin-top: 70px;">
							<div class="fLeft">网络流量</div>
							<div class="clearfix"></div>
						</div>
						<div class="m-t-5" style="height: 180px;width: 100%" id="global-net-flow"></div>
						<div class="WP50 fLeft p-r-5">
							<div class="global-title">
								<div class="fLeft">最新事件</div>
								<div class="clearfix"></div>
							</div>
							<div class="table-item-header">
		                        <div class="col-md-12">
			                        <div class="col-md-2">名称</div>
			                        <div class="col-md-3">程序</div>
			                        <div class="col-md-3">产生地址</div>
			                        <div class="col-md-4">时间</div>
			                        <div class="clearfix"></div>
		                        </div>
		                    </div>
		                    <div class="table-body-border">
		                        <div class="table-body" @mouseover="dynamicRolling('', true)" @mouseout="startScroll">
		                            <div class="table-item-body" v-for="list in newEvent" :class="$index?'m-t-5':''">
		                                <div class="col-md-2 overHidden tdItem" :title="list.type">{{list.name}}</div>
		                                <div class="col-md-3 overHidden tdItem" :title="list.event">{{list.app}}</div>
		                                <div class="col-md-3 overHidden tdItem" :title="list.addr">{{list.ip}}</div>
		                                <div class="col-md-4 overHidden tdItem" :title="list.time">{{list.time}}</div>
		                                <div class="clear"></div>
		                            </div>
		                        </div>
		                    </div>
						</div>
						<div class="WP50 fLeft p-l-5">
							<div class="global-title">
								<div class="fLeft">设备状态</div>
								<div class="clearfix"></div>
							</div>
		                    <div id="device-status-full">
		                        <table class="ys-table">
		                            <thead>
		                            <tr style="background:rgba(0,0,0,0.15) !important; border:1px solid rgba(74,146,255,0.5) !important">
		                                <th></th>
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
		                            <tr style="background:rgba(255,255,255,0.15) !important;">
		                                <td class="detail">
		                                                <span @click="showDetail(list.type)"><i class="ys-icon"
		                                                                                     v-bind:class="[curDetailId == list.type ? 'icon-downlist-up' : 'icon-downlist' ]"></i></span>
		                                </td>
		                                <td style="text-align: left;width: 120px;">{{list.type}}</td>
		                                <td>{{list.num}}</td>
		                                <td class="ys-success-color">{{list.normal}}</td>
		                                <td class="ys-warn-color">{{list.off}}</td>
		                                <td class="ys-error-color">{{list.abnormal}}</td>
		                            </tr>
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
		                            </tbody>
		                        </table>
							</div>
							<div class="clearfix"></div>
						</div>
				</div>
					<div class="contentRight fRight p-r-10">
						<div id="global-full-risk-status" style="height: 300px; width: 100%"></div>
						<div class="global-title">
							<div class="fLeft">事件统计</div>
							<div class="clearfix"></div>
						</div>
						<div>
							<div class="m-t-5 positionRl" style="height: 220px;">
								<global-full-pie :id="'ssa-global-full-thing-count'"
								                :height="'220px'"
									            :x="'right'"
									            :y="'middle'"
									            :name="'事件统计'"
									            :position="['80', '50%']"
								                :data="eventCount"></global-full-pie>
								<div class="thing-count-bg"></div>
							</div>
						</div>
					</div>
					<div class="clearfix"></div>
			</div>
		</div>
			<!--<div class="diverge-top-line"></div>-->
			<div class="global-top-left-split"></div>
			<div class="global-top-right-split"></div>
		</div>
	</div>
	</div>
</template>
<script>
    import Api from 'src/lib/api';
    let echarts = require('echarts/lib/echarts');
    import globalFullBar from './global-full-bar.vue';
    import globalFullPie from './global-full-pie.vue';
    export default {
        name: "global-full-page",
        props: {
            show: {
                default: false
            }
        },
        data() {
            return {
	            curDate: '',
	            curWeek: '',
	            curTime: '',
	            activeColor: 'linear-gradient(90deg,rgba(237,114,44,1),rgba(231,180,52,1))',
                captionRisk: {
                    x: [],
                    y: [],
	                color: {
                        type: 'bar',
                        colorStops: [{
                            offset: 0,
                            color: 'rgba(11,42,84,.3)' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#ffa800' // 100% 处的颜色
                        }],
                        globalCoord: false
	                }
                },
	            newEvent:[],
	            scrollTimer: '',
	            index: 0,
	            AssetStatus: [],
                curDetailId: '-1',
	            safeStaticChart: '',
	            trendChart: '',
	            dangerGradeStateChart: '',
	            riskStatusChart: '',
	            plantCap: [],
	            eventCount: [],
	            hours: [],
	            days: [],
	            AssetsDetail: [],
	            netFlowData: {
	                x: [],
		            data: []
	            },
	            outLineType: [],
	            terminal_foul_org: {
	                x: [],
		            y: []
	            },
	            foulOperation: {
	                x: [],
		            y: []
	            },
	            attackSrcipCount: {
	                x: [],
		            y: []
	            },
	            orgRiskCount: {
	                x: [],
		            y: []
	            },
	            attackDstipCount: {
	                x: [],
		            y: []
	            },
	            terminalLevel: [],
	            safeResultData: [],
	            eventStatic: {
	                wg: 0,
		            bd: 0,
		            rq: 0
	            },
                securityGrade: {
                    total: 0,
                    score: 0,
                    up: 0
                },
	            eventRiskTop: {
	                x: [],
		            y: []
	            },
	            event_type_score: '',
	            eventType: {
	                total: 0,
		            series: [],
		            value: []
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
            },
            range(val) {
                if (val >= 1000) {
                    return "999+"
                } else {
                    return val
                }
            },
	        formatterBigCoiunt (val) {
                if(val > 99999999){
                    return (val/100000000).toFixed(1) + ' 亿' ;
                }else if(val > 9999){
                    return (val/10000).toFixed(1) + ' 万' ;
                }else{
                    return val ;
                }
	        }
        },
        ready: function () {
            this.captionRisk.x = [270000, 302, 20003, 130, 2700];
            this.captionRisk.y = ["aa.com", "bb.com", "cc", "dd", "ee"];
	        $('#device-status-full').slimScroll({
		        height: '200',
		        width: '100%',
		        position: 'right',
		        size: "5px",
		        color: '#000',
		        wheelStep: 5
	        });
	        this.remConfig();
        },
        components: {
            globalFullBar,
	        globalFullPie
        },
        methods: {
            //rem配置
	        remConfig () {
		        (function (doc, win) {
			        var docEl = doc.documentElement,
			        //console.log(window);
			        //var docEl = document.getElementById('rem-border'),
			        resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
				        recalc = function () {
			                var clientWidth = docEl.clientWidth;
			                if (!clientWidth) return;
			                if(clientWidth>=1920){
			                    docEl.style.fontSize = '100px';
			                }else{
			                    docEl.style.fontSize = 100 * (clientWidth / 1920) + 'px';
			                }
			            };
			        if (!doc.addEventListener) return;
			        win.addEventListener(resizeEvt, recalc, false);
			        doc.addEventListener('DOMContentLoaded', recalc, false);
			    })(document, window);
	        },
            //动态滚动
            dynamicRolling (index, stop) {
                if(this.newEvent.length < 6){
                    return false;
                }
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
                if(this.newEvent.length < 6){
                    return false;
                }
                let self = this ;
                this.scrollTimer = setInterval(function () {
                    self.dynamicRolling(self.index, false)
                }, 3000);
            },
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
	        refreshGlobal () {
		        this.setRealTime();
		        this.getNetFlowData();
		        this.getRatingSystemData();
		        //this.getAssetDetailData();
		        this.getAssetStatusData();
		        this.getAssetStatus();
		        this.getThingCountData();
		        this.getOutLineTypeData();
		        this.getFoulOrgData();
		        this.getFoulOperationData();
		        this.getOrgRiskCountData();
		        this.getAttackScripCountData();
		        this.getAttackDstipCountData();
		        this.getEventStatic();
		        this.getOverallScore();
		        this.getEventRiskTop();
		        this.getNewEvent();
	        },
	        closeFullPage () {
                this.show = false;
	        },
	        //安全结果统计
	        getSafeResultData () {
		        this.$http.post('/api/ssa/new_global/terminal_level').then(function (response) {
                    if (response.data.status == 200) {
                        this.safeResultData = response.data.data ;
				        this.safeStaticChart = echarts.init(document.getElementById('global-safe-result'));
				        this.initChart('global-safe-result', this.safeResult, this.safeStaticChart);
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        //格式化事件综述
	        formatterEventCount (val) {
                let str=val.toString();
				let re=/(?=(?!(\b))(\d{3})+$)/g;
				str=str.replace(re,".");
				return str
	        },
	        // 安全检测结果统计
	        safeResult () {
				let self = this;
				let data = [
				    {
					    name: '危急',
						value: self.safeResultData.super
					},
				    {
					    name: '高危',
						value: self.safeResultData.high
					},
					{
					    name: '中危',
						value: self.safeResultData.mid
					},
					{
					    name: '低危',
						value: self.safeResultData.low
					},
				];
                let staticOption = {
                    title: {
                        text: '事件总数',
	                    x: 'center',
			            y: '38%',
			            textStyle: {
			                fontWeight: 'normal',
			                fontSize: 20,
			                color: "#fff",
			            },
			            subtext: self.formatterEventCount(self.securityGrade.total),
	                    subtextStyle: {
                            color: '#fff',
		                    fontFamily: 'digi',
		                    fontSize: 44
	                    }
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b}: {c} ({d}%)",
				        backgroundColor: 'rgba(74, 146, 255, 0.2)',
				        border: '1px solid rgba(74, 146, 255, 0.3)',
                    },
                    color: ['#ff686b','#fcbf5d','#229aff','#a3f29d','#00b1f2','#fff225','#ff93c3','#23e8c7','#fca04e','#4cccff','#b8f049','#c593ff','#0be6c1','#fbd65b','#73e3ff','#ff937c','#6aeaa4','#388bff','#fce75d','#ffbab3','#ff5662','#4fe995','#d9bfff','#ffc43d','#6b8dfe','#fc5bb4','#26d8ef','#8ca1ff','#b5e2e2','#ffa69e','#d0b0ff'],
                    legend: {
                        left: 'center',
                        top: 'bottom',
                        textStyle: {
                            color: 'rgba(154,188,238,1)'
                        },
                        itemWidth: 10,
                        itemHeight: 10
                    },
                    series: [
                        {
                            name: '安全结果统计',
                            type:'pie',
                            radius: ['80%', '90%'],
                            center: ['50%', '45%'],
                            avoidLabelOverlap: false,
                            label: {
                                normal: {
                                    show: false,
                                    position: 'center'
                                },
                                emphasis: {
                                    show: false,
                                    textStyle: {
                                        fontSize: '30',
                                        fontWeight: 'bold'
                                    }
                                }
                            },
                            labelLine: {
                                normal: {
                                    show: false
                                }
                            },
                            data: data
                        }
                    ]
                };
                self.safeStaticChart.setOption(staticOption);
	        },
	         //网络流量
	        getNetFlowData () {
		        this.$http.post('/api/ssa/new_global/network_flow').then(function (response) {
                    if (response.data.status == 200) {
                        this.netFlowData.x = response.data.data.days;
                        this.netFlowData.data = response.data.data.data;
				        this.trendChart = echarts.init(document.getElementById('global-net-flow'));
				        this.initChart('global-net-flow', this.netFlow, this.trendChart);
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        //网络流量
	        netFlow () {
                let self = this ;
                let series = [];
		        let color = ['#ff686b','#fcbf5d','#229aff','#a3f29d','#00b1f2','#fff225','#ff93c3','#23e8c7','#fca04e','#4cccff','#b8f049','#c593ff','#0be6c1','#fbd65b','#73e3ff','#ff937c','#6aeaa4','#388bff','#fce75d','#ffbab3','#ff5662','#4fe995','#d9bfff','#ffc43d','#6b8dfe','#fc5bb4','#26d8ef','#8ca1ff','#b5e2e2','#ffa69e','#d0b0ff'];
                for(let key in self.netFlowData.data){
                    let obj = {
				        name: self.netFlowData.data[key].name,
				        data: self.netFlowData.data[key].data,
				        type: 'line',
				        smooth: true,
	                    areaStyle: {
				            color: color[key],
				            opacity: 0.2
	                    }
			        };
			        series.push(obj)
                }
		        let trendOption = {
                    color: ['#ff686b','#fcbf5d','#229aff','#a3f29d','#00b1f2','#fff225','#ff93c3','#23e8c7','#fca04e','#4cccff','#b8f049','#c593ff','#0be6c1','#fbd65b','#73e3ff','#ff937c','#6aeaa4','#388bff','#fce75d','#ffbab3','#ff5662','#4fe995','#d9bfff','#ffc43d','#6b8dfe','#fc5bb4','#26d8ef','#8ca1ff','#b5e2e2','#ffa69e','#d0b0ff'],
			        tooltip: {
				        trigger: 'axis',
				        backgroundColor: 'rgba(74, 146, 255, 0.2)',
				        border: '1px solid rgba(74, 146, 255, 0.3)',
				        formatter: function (params) {
				            let str = '' ;
				            for(let key in params){
					            str += params[key].seriesName +': '+ self.changeBand(params[key].data) +' '+self.changeUnit(params[key].data)+ '<br />' ;
				            }
				            return str;
				        }
			        },
			        xAxis: {
				        type: 'category',
				        data: self.netFlowData.x,
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
			        series: series
		        };
		        self.trendChart.setOption(trendOption);
	        },
	        //评分体系数据获取
	        getRatingSystemData () {
                this.$http.post('/api/ssa/new_global/event_type_score').then(function (response) {
                    if (response.data.status == 200) {
                        this.event_type_score = response.data.data;
                        let chartData = response.data.data, total = 0, value = [], series = [], name = [];
                        for (let i = 0; i < chartData.length; i++) {
                            total += parseInt(chartData[i]['value']);
                        }
                        for (let i = 0; i < chartData.length; i++) {
                            value.push(chartData[i].value / total);
                            series.push({
                                name: chartData[i].name,
                                max: 1
                            });
                        }
                        let dangerGradeStateChart = echarts.init(document.getElementById('global-rating-system'));
                        let dangerGradeStateOption = {
                            tooltip: {
                                trigger: 'item',
				                backgroundColor: 'rgba(74, 146, 255, 0.2)',
				                border: '1px solid rgba(74, 146, 255, 0.3)',
                                formatter: function (params) {
                                    let str = params.seriesName + '<br />';
                                    for (let key in series) {
                                        str += series[key].name + ': ' + (Number(params.value[key]) * 100).toFixed(1) + '%<br/>';
                                    }
                                    return str;
                                }
                            },
                            radar: {
                                shape: 'polygon',
                                name: {
                                    textStyle: {
                                        color: '#93a6d8',
                                    }
                                },
                                radius: '66%',
                                nameGap: 10,
	                            center: ['50%', '50%'],
                                indicator: series,
                                splitArea: {
                                    show: true,
                                    areaStyle: {
                                        color: "rgba(74, 146, 255, 0.05)",
                                    },
                                },
                                splitLine: {
                                    lineStyle: {
                                        color: "rgba(74, 146, 255, 0.2)"
                                    }
                                },
                                axisLine: {
                                    show: true,
                                    lineStyle: {
                                        color: "rgba(74, 146, 255, 0.2)"
                                    }
                                },
                            },
                            series: [{
                                name: '评分体系',
                                type: 'radar',
                                areaStyle: {
                                    color: "rgba(233,97,87,0.2)"
                                },
                                lineStyle: {
                                    color: "rgba(233,97,87,1)",
                                },
                                data: [
                                    {
                                        value: value
                                    },
                                    {
                                        name: series
                                    }
                                ]
                            }]
                        };
                        dangerGradeStateChart.setOption(dangerGradeStateOption);
                        window.addEventListener('resize', dangerGradeStateChart.resize());
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })

	        },
	        //设备事件状况数据获取
	        getAssetDetailData () {
		        this.$http.post('/api/ssa/new_global/assets_event_trend').then(function (response) {
                    if (response.data.status == 200) {
                        this.hours = response.data.data.days;
                        this.days = response.data.data.labes;
                        this.AssetsDetail = response.data.data.data;
		                this.assetDetailChart = echarts.init(document.getElementById('global-full-machine-detail'));
		                 this.initChart('global-full-machine-detail', this.assetDetail, this.assetDetailChart);
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        //设备事件状况图
            assetDetail () {
                let self = this ;
                let colors = ['#3164FF', '#4FA5EB', '#E96157'];
                self.AssetsDetail = self.AssetsDetail.map(function (item) {
                    return {
                        value: [item[1], item[0], item[2]],
                        itemStyle: {
                            normal: {
                                color: colors[Math.floor(Math.random() * 3)]
                            }
                        },
                    };
                });

                let assetOption = {
                    tooltip: {
                        position: 'top',
	                    formatter: function (params) {
                            return params.seriesName +'<br />'+ params.name+': '+params.data.value[2]
	                    }
                    },
                    grid: {
                        left: 5,
                        bottom: 5,
                        right: 5,
                        top: 5,
                        containLabel: true
                    },
                    xAxis: {
                        type: 'category',
                        data: self.hours,
                        boundaryGap: false,
                        splitLine: {
                            show: true,
                            lineStyle: {
                                color: 'rgba(0,0,0,0.1)',
                            }
                        },
                        axisLine: {
                            show: false
                        },
                        axisLabel: {
                            color: '#ddd'
                        }
                    },
                    yAxis: {
                        type: 'category',
                        data: self.days,
                        axisLine: {
                            show: false
                        },
                        axisLabel: {
                            color: '#9abcee'
                        }
                    },
                    series: [{
                        name: '设备情况',
                        type: 'scatter',
                        symbolSize: function (val) {
                            if(val[2] > 10000){
                                return 25;
                            }else if(val[2] > 1000){
                                return 15;
                            }else if(val[2] > 100){
                                return 10;
                            }else{
                                return 5
                            }
                        },
                        data: self.AssetsDetail,
                        animationDelay: function (idx) {
                            return idx * 5;
                        }
                    }]
                };
                self.assetDetailChart.setOption(assetOption);
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
            //展开详情
            showDetail(id) {
                if (this.curDetailId == id) {
                    this.curDetailId = "-1"
                } else {
                    this.curDetailId = id;
                }
            },
	        //获取风险状态数据获取
	        getAssetStatusData () {
                this.$http.post('/api/ssa/new_global/risk_state', '').then(function (res) {
					if(res.data.status == 200){
					    this.plantCap = res.data.data;
				        this.riskStatusChart = echarts.init(document.getElementById('global-full-risk-status'));
				        this.initChart('global-full-risk-status', this.assetStatusChart, this.riskStatusChart);
					}
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
	        },
	        //规整风险状态数据
	        formatterAssetsValue (index) {
                let count = 80 - Number(index)*2;
                if(count > 10){
                    return count ;
                }else{
                    return 10 ;
                }
	        },
            //获取风险状态chart
            assetStatusChart() {
                let self = this, colors = ['#F05D5F', '#4A92FF', '#53ADF8'];
                let datalist = [[56, 48], [35, 80], [20, 43], [83, 30], [36, 20], [64, 10], [75, 75], [93, 72], [0, 12], [50, 6], [100, 20], [10, 20], [20, 0], [0, 60], [20, 80], [50, 100]];
                let datas = [];
                for (var i = 0; i < self.plantCap.length; i++) {
                    var item = self.plantCap[i];
                    var itemToStyle = datalist[i];
                    datas.push({
                        name: item.name + '\n\n' + item.value,
                        value: itemToStyle,
                        symbolSize: self.formatterAssetsValue(i),
                        label: {
                            normal: {
                                textStyle: {
                                    fontSize: 11
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: colors[i<5?0:i>10?2:1],
                                opacity: (Math.random() * 5 + 5) / 10
                            }
                        },
                    })
                }
                let statusOption = {
                    grid: {
                        show: false,
                    },
                    xAxis: [{
                        gridIndex: 0,
                        type: 'value',
                        show: false,
                        min: 0,
                        max: 100,
                        nameLocation: 'middle',
                        nameGap: 5
                    }],
                    yAxis: [{
                        gridIndex: 0,
                        min: 0,
                        show: false,
                        max: 100,
                        nameLocation: 'middle',
                        nameGap: 30
                    }],
                    series: [{
                        type: 'scatter',
                        symbol: 'circle',
                        symbolSize: 100,
                        label: {
                            normal: {
                                show: true,
                                formatter: '{b}',
                                color: '#fff',
                                textStyle: {
                                    fontSize: '20'
                                }
                            },
                        },
                        itemStyle: {
                            normal: {
                                color: '#00acea'
                            }
                        },
                        data: datas
                    }]
                };
                self.riskStatusChart.setOption(statusOption);
            },
	        //初始化
            initChart(id, setChart, chart) {
                let self = this;
                let repeat = setInterval(function () {
                    if (document.getElementById(id)) {
                        setChart();
                        window.addEventListener('resize', function () {
                            self.handleResize(chart);
                        });
                        clearInterval(repeat)
                    }
                }, 300)
                let resizeRepeat = setInterval(function () {
                    if (document.getElementById(id)) {
                        var EleResize = {
                            _handleResize: function (e) {
                                var ele = e.target || e.srcElement;
                                var trigger = ele.__resizeTrigger__;
                                if (trigger) {
                                    var handlers = trigger.__z_resizeListeners;
                                    if (handlers) {
                                        var size = handlers.length;
                                        for (var i = 0; i < size; i++) {
                                            var h = handlers[i];
                                            var handler = h.handler;
                                            var context = h.context;
                                            handler.apply(context, [e]);
                                        }
                                    }
                                }
                            },
                            _removeHandler: function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    var size = handlers.length;
                                    for (var i = 0; i < size; i++) {
                                        var h = handlers[i];
                                        if (h.handler === handler && h.context === context) {
                                            handlers.splice(i, 1);
                                            return;
                                        }
                                    }
                                }
                            },
                            _createResizeTrigger: function (ele) {
                                var obj = document.createElement('object');
                                obj.setAttribute('style',
                                    'display: block; position: absolute; top: 0; left: 0; height: 100%; width: 100%; overflow: hidden;opacity: 0; pointer-events: none; z-index: -1;');
                                obj.onload = EleResize._handleObjectLoad;
                                obj.type = 'text/html';
                                ele.appendChild(obj);
                                obj.data = 'about:blank';
                                return obj;
                            },
                            _handleObjectLoad: function (evt) {
                                this.contentDocument.defaultView.__resizeTrigger__ = this.__resizeElement__;
                                this.contentDocument.defaultView.addEventListener('resize', EleResize._handleResize);
                            }
                        };
                        if (document.attachEvent) {//ie9-10
                            EleResize.on = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (!handlers) {
                                    handlers = [];
                                    ele.__z_resizeListeners = handlers;
                                    ele.__resizeTrigger__ = ele;
                                    ele.attachEvent('onresize', EleResize._handleResize);
                                }
                                handlers.push({
                                    handler: handler,
                                    context: context
                                });
                            };
                            EleResize.off = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    EleResize._removeHandler(ele, handler, context);
                                    if (handlers.length === 0) {
                                        ele.detachEvent('onresize', EleResize._handleResize);
                                        delete  ele.__z_resizeListeners;
                                    }
                                }
                            }
                        } else {
                            EleResize.on = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (!handlers) {
                                    handlers = [];
                                    ele.__z_resizeListeners = handlers;

                                    if (getComputedStyle(ele, null).position === 'static') {
                                        ele.style.position = 'relative';
                                    }
                                    var obj = EleResize._createResizeTrigger(ele);
                                    ele.__resizeTrigger__ = obj;
                                    obj.__resizeElement__ = ele;
                                }
                                handlers.push({
                                    handler: handler,
                                    context: context
                                });
                            };
                            EleResize.off = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    EleResize._removeHandler(ele, handler, context);
                                    if (handlers.length === 0) {
                                        var trigger = ele.__resizeTrigger__;
                                        if (trigger) {
                                            trigger.contentDocument.defaultView.removeEventListener('resize', EleResize._handleResize);
                                            ele.removeChild(trigger);
                                            delete ele.__resizeTrigger__;
                                        }
                                        delete  ele.__z_resizeListeners;
                                    }
                                }
                            }
                        }
                        var resizeDiv = document.getElementById(id);
                        EleResize.on(resizeDiv, function () {
                            self.handleResize(chart);
                        });
                        clearInterval(resizeRepeat)
                    }
                }, 300)
            },
	        //获取事件统计数据
	        getThingCountData () {
                this.$http.post('/api/ssa/new_global/event_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.eventCount = response.data.data.event_source;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        //获取违规类型数据
	        getOutLineTypeData () {
                this.$http.post('/api/ssa/new_global/terminal_foul_type').then(function (response) {
                    if (response.data.status == 200) {
                        this.outLineType = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
            //获取违规类型数据
	        getFoulOrgData () {
                this.$http.post('/api/ssa/new_global/terminal_foul_org').then(function (response) {
                    if (response.data.status == 200) {
                        this.terminal_foul_org.y = response.data.data.lables.reverse();
                        this.terminal_foul_org.x = response.data.data.series.reverse();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        getFoulOperationData () {
                this.$http.post('/api/ssa/new_global/terminal_foul_operate').then(function (response) {
                    if (response.data.status == 200) {
                        this.foulOperation.y = response.data.data.lables.reverse();
                        this.foulOperation.x = response.data.data.series.reverse();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        getOrgRiskCountData () {
                this.$http.post('/api/ssa/new_global/org_risk_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.orgRiskCount.y = response.data.data.lables.reverse();
                        this.orgRiskCount.x = response.data.data.series.reverse();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        getAttackScripCountData () {
                this.$http.post('/api/ssa/new_global/attack_srcip_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.attackSrcipCount.y = response.data.data.lables.reverse();
                        this.attackSrcipCount.x = response.data.data.series.reverse();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        getAttackDstipCountData () {
                this.$http.post('/api/ssa/new_global/attack_dstip_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.attackDstipCount.y = response.data.data.lables.reverse();
                        this.attackDstipCount.x = response.data.data.series.reverse();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
            handleResize(chart) {
                chart.resize();
            },
	        //事件统计
            getEventStatic() {
                this.$http.post('/api/ssa/new_global/event_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.eventStatic.wg = response.data.data.event_type.attack;
                        this.eventStatic.rq = response.data.data.event_type.norule;
                        this.eventStatic.bd = response.data.data.event_type.viruses;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
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
                        this.getSafeResultData() ;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
	        // 风险资产TOP5
            getEventRiskTop() {
                this.$http.post('/api/ssa/new_global/asset_risk_top').then(function (response) {
                    if (response.data.status == 200) {
						 let data = response.data.data.sort(function (a, b) {
						    let x = a.value ;
						    let y = b.value ;
						    if (x < y) {
						        return 1;
						    } else if (x > y) {
						        return -1;
						    } else {
						        return 0;
						    }
						 }) ;
						this.eventRiskTop.x = [];
						this.eventRiskTop.y = [];
						 for(let i in data.reverse()){
						     this.eventRiskTop.y.push(data[i].name);
						     this.eventRiskTop.x.push(data[i].value);
						 }
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
        },
        watch: {
            'show': function () {
                if (this.show) {
                    this.setRealTime();
		            this.getNetFlowData();
		            this.getRatingSystemData();
			        //this.getAssetDetailData();
			        this.getAssetStatusData();
			        this.getAssetStatus();
			        this.getThingCountData();
			        this.getOutLineTypeData();
			        this.getFoulOrgData();
			        this.getFoulOperationData();
			        this.getOrgRiskCountData();
			        this.getAttackScripCountData();
			        this.getAttackDstipCountData();
			        this.getEventStatic();
			        this.getOverallScore();
			        this.getEventRiskTop();
			        this.getNewEvent();
                }
            },
	        'newEvent': function () {
                let self = this ;
		        window.clearInterval(self.scrollTimer);
	            this.scrollTimer = setInterval(function () {
	                self.dynamicRolling(self.index, false)
	            }, 3000);
            }
        },
        destroyed: function () {
            window.clearInterval(this.scrollTimer);
        }
    }
</script>
