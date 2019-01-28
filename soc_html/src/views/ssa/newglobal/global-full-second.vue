<style scoped>
	@font-face {
		font-family: AliHYAiHei-Beta;
		src: url('../../../assets/fonts/AliHYAiHei-Beta.ttf');
		font-weight: 200;
		font-style: normal;
	}
	.global{
		width: 100%;
		height: 100%;
		padding: 0.1rem 0.15rem;
		font-family: AliHYAiHei-Beta;
		font-size: 0.12rem;
		background-image: url('../../../assets/images/ssa/global-full-second-bg.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		position: relative;
	}
	.m-t-r-5{
		margin-top: 0.05rem;
	}
	.m-t-r-8{
		margin-top: 0.08rem;
	}
	.m-t-r-10{
		margin-top: 0.1rem;
	}
	.m-t-r-20{
		margin-top: 0.2rem;
	}
	.font-normal{
		font-family: PingFangSC-Medium;
	}
	.global-color-error{
		color:rgba(199,0,10,1) !important;
	}
	.global-color-org{
		color:rgba(255,159,31,1) !important;
	}
	.global-color-green{
		color:rgba(132,196,66,1) !important;
	}
	.global-color-cyan{
		color:rgba(45,215,160,1) !important;
	}
	.global-color-error-bg{
		background-color:rgba(199,0,10,1) !important;
	}
	.global-color-org-bg{
		background-color:rgba(255,159,31,1) !important;
	}
	.global-color-green-bg{
		background-color:rgba(132,196,66,1) !important;
	}
	.global-color-cyan-bg{
		background-color:rgba(45,215,160,1) !important;
	}
	.global-color-error-bg1{
		background-color:rgba(199,0,10,0.3) !important;
	}
	.global-color-org-bg1{
		background-color:rgba(255,159,31,0.3) !important;
	}
	.global-color-green-bg1{
		background-color:rgba(132,196,66,0.3) !important;
	}
	.global-color-cyan-bg1{
		background-color:rgba(45,215,160,0.3) !important;
	}
	.global-color-green1{
		color:rgba(29,255,158,1) !important;
	}
	.global-color-green-green{
		background:rgba(29,255,158,0.2) !important;
	}

	.global-color-green-green1{
		background:rgba(29,255,158,1) !important;
	}
	.global-left, .global-right{
		width: 19.5%;
		height: 100%;
	}
	.global-center{
		width: 60%;
		height: 100%;
		margin-left: 0.5%;
		position: relative;
		background-image: url('../../../assets/images/ssa/global-full-second-center-bg.png');
		background-repeat: no-repeat;
	}
	.global-box{
		width: 100%;
		background: rgba(0,0,0,0.5);
		padding: 0.1rem 0.15rem;
	}
	.global-title{
		height: 0.46rem;
	}
	.global-title-img{
		width: 0.11rem;
		height: 0.31rem;
		border:2px solid rgba(29,255,158,1);
		border-right: none ;
		margin-top: 0.07rem;
	}
	.global-title-title{
		font-size: 0.12rem;
		color:rgba(255,255,255,0.5);
		padding-left: 0.06rem;
		margin-top: 0.03rem;
		 white-space: nowrap;
        text-overflow:ellipsis;
        overflow:hidden;
	}
	.global-title-htitle{
		font-size: 0.2rem;
		color: #fff;
		padding-left: 0.06rem;
		margin-top: 0.1rem;
		 white-space: nowrap;
        text-overflow:ellipsis;
        overflow:hidden;
	}
	.safe-score{
		height: 1.75rem;
		border: 1px solid rgba(255,255,255,0.2);
		margin-top: 0.1rem;
		position: relative;
	}
	.safe-score-score{
		position: absolute;
	}
	.safe-score-word{
		text-align: center;
		padding-top: 0.55rem;
		position: absolute;
		right: 15px;
	}
	.safe-score-word div:nth-child(1){
		font-size: 0.48rem;
	}
	.safe-score-word div:nth-child(2){
		font-size: 0.12rem;
		color:rgba(255,255,255,0.7);
		margin-top: 0.05rem;
	}
	.change-label-color{
		width: 0.1rem;
		height: 1.14rem;
		background: linear-gradient(180deg,rgba(255,0,13,1),rgba(255,230,4,1),rgba(45,215,160,1));
	}
	.global-title-top{
		font-size: 0.2rem;
		color:rgba(255,255,255,1);
		margin-top: 0.2rem;
	}
	.risk-ip-top{
		width: 100%;
		height: 2.13rem;
		padding: 0.08rem 0;
	}
	.risk-ip-logo{
		width: 40%;
		height: 1.93rem;
		background:linear-gradient(180deg,rgba(49,100,255,0.1),rgba(0,255,220,0.5));
		text-align: center;
	}
	.risk-ip-logo img{
		height: 0.81rem;
		margin-top: 0.2rem;
	}
	.risk-ip-logo div{
		width: 100%;
		text-align: center;
		color: #fff;
	}
	.risk-ip-logo div:nth-child(2){
		font-size: 0.24rem;
		margin-top: 0.2rem;
	}
	.risk-ip-content{
		width: 55%;
	}
	.risk-ip-item{
		width: 100%;
		height: 0.32rem;
		line-height: 0.32rem;
		color: #fff;
		background:rgba(255,255,255,0.15)
	}
	.risk-ip-item div:nth-child(1){
		width: 0.32rem;
		height: 0.32rem;
		line-height: 0.32rem;
		text-align: center;
		background:rgba(255,255,255,0.2)
	}
	.global-center-header{
		width: 100%;
		height: 0.72rem;
		background: rgba(0,0,0,0.5);
		box-shadow: 0px 1px 0px 0px rgba(255,255,255,0.3),0px -1px 0px 0px rgba(255,255,255,0.25);
		padding: 0.07rem 0.15rem;
	}
	.split-line{
		width:1px;
		height: 0.5rem;
		background:rgba(216,216,216,0.3);
	}
	.global-center-header .global-center-header-item{
		float: left;
		text-align: center;
	}
	.global-center-header .global-center-header-time{
		width: 19%;
		float: left;
	}
	.global-center-header-time span{
		font-size: 0.16rem;
	}
	.global-center-header-item img{
		width: 0.5rem;
	}
	.global-center-header-item-count{
		margin-left: 0.15rem;
		line-height: 1.2;
		margin-top: 0.05rem;
	}
	.global-center-header-item-count div:nth-child(1){
		font-size: 0.14rem;
	}
	.global-center-header-item-count div:nth-child(2){
		font-size: 0.24rem;
		color:rgba(29,255,158,1);
	}
	.global-bottom-line{
		height: 0.1rem;
		border: 1px solid rgba(255,255,255,0.2);
		margin-top: 0.15rem;
	}
	.safe-search{
		margin-top: 0.2rem;
	}
	.safe-search-item{
		width: 25%;
	}
	.safe-search-item div:nth-child(1){
		font-size: 0.14rem;
	}
	.safe-search-item div:nth-child(2){
		font-size: 0.24rem;
		margin-top: 0.05rem;
	}
	.safe-search-item-percent{
		width: 90%;
		height:4px;
		background: rgba(255,255,255,0.2);
		margin-top: 0.05rem;
	}
	.safe-search-item-percent-active{
		width: 90%;
		height:4px;
		background: rgba(255,0,13,1);
	}
	.outOfLine-type{
		width: 100%;
		height: 2.43rem;
		border: 1px solid rgba(255,255,255,0.2);
		margin-top: 0.2rem;
		position: relative;
	}
	.outOfLine-type .global-title{
		position: absolute;
		top: 0;
		left: 0;
	}
	.outOfLine-org{
		margin-top: 0.15rem;
		width: 95%;
	}
	.outOfLine-org-item{
		width: 100%;
		height: 0.35rem;
		line-height: 0.35rem;
		background:rgba(255,255,255,0.3);
	}
	.global-center-cell{
		height: 2.61rem;
		/*background: rgba(199,0,10,0.15);*/
		border-radius: 0.06rem;
		/*border: 1px solid rgba(199,0,10,1);*/
		margin-left: 0.01rem;
		text-align: center;
	}
	.global-center-cell img{
		width: 100%;
		/*margin-top: 0.1rem;*/
	}
	.global-center-cell-child{
		width:0.2rem;
		height: 0.18rem;
		background:rgba(255,255,255,0.2);
	}
	.global-center-footer .global-box{
		width: 49%;
	}
	.table-item-header div {
        font-size: 0.12rem;
        color: rgba(29,255,158,1);
        text-align: center;
        height: 0.34rem;
        line-height: 0.34rem;
    }
    .table-item-body {
        width: 100%;
        height: 0.3rem;
	    background:rgba(255,255,255,0.15);
        border: 1px solid rgba(29,255,158, 0.3);
    }
    .table-body-border {
        width: 100%;
        height: 1.75rem;
        overflow: hidden;
        position: relative;
    }
    .table-item-body:hover{
        background: rgba(29,255,158, 0.2);
        border: 1px solid rgba(29,255,158, 0.3);
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
	.global-center-footer{
		position: absolute;
		bottom: 0;
		left: 0;
		width: 100%;
	}
	.ys-table>tbody>tr{
		background-color: rgba(255,255,255,0.15) !important;
	}
	.position-center-border{
		position: relative;
	}
	.global-center-content-left{
		position: absolute;
		top: 0.3rem;
		left: 5%;
		z-index: 1;
	}
	.position-center-right{
		height: 6.72rem;
		position: absolute;
		right: 0;
		top: 0;
		z-index: 2;
		display: inline-block;
		width: 100%;
		padding-right: 3%;
		overflow: hidden;
	}
	.global-center-content-left img{
		height: 2.09rem;
	}
	.global-center-content-left div:nth-child(2){
		font-size: 0.24rem;
		color: #fff;
		margin-top: 0.16rem;
		padding-left: 0.2rem;
	}
	.global-center-content-left div:nth-child(3){
		font-size: 0.36rem;
		color: rgba(29,255,158,1);
		margin-top: 0.15rem;
		padding-left: 0.25rem;
	}
	.content-left-item{
		margin-top: 0.3rem;
	}
	.content-left-item i{
		color: rgba(29,255,158,0.5);
		font-size: 0.14rem;
	}
	.content-left-item span:nth-child(2){
		font-size: 0.24rem;
		color: #fff;
	}
	.content-left-item span:nth-child(3){
		font-size: 0.24rem;
		color: #1DFF9E;
	}
	.center-scroll-border{
		width: 13%;
	}
	.center-scroll-name, .event-scroll-page{
		width: 42px;
		height: 26px;
		background: rgba(0,0,0,0.3);
		border-radius: 4px;
		border: 1px solid rgba(29,255,158,1);
		font-size: 12px;
		color: #fff;
		text-align: center;
		line-height: 26px;
		margin: 5px auto;
	}
	.event-scroll-border{
		width: 100%;
		margin-top: 0.1rem;
		height: 5.8rem;
		overflow: hidden;
		position: relative;
	}
	.event-scroll-content{
		width: 100%;
		height: auto;
		position: absolute;
		top: 0;
		left: 0;
	}
	.event-scroll-item{
		width: 100%;
		height: 1rem;
		background:rgba(0,0,0,0.3);
		border-radius:4px;
		border:1px solid rgba(29,255,158,1);
		padding: 0.17rem 0 0.2rem 0.2rem;
	}
	.event-scroll-item-active {
		background:rgba(29,255,158,0.2);
	}
	.event-scroll-item div:nth-child(1){
		font-size: 0.14rem;
		color: #fff;
	}
	.event-scroll-item div:nth-child(2){
		font-size: 0.24rem;
		color:rgba(29,255,158,1);
		margin-top: 0.16rem;
	}
	.event-scroll-detail{
		width: 59%;
		height: 100%;
		background-image: url('../../../assets/images/ssa/gloabal-full-second-detail-border.png');
		background-repeat: no-repeat;
		background-size: 100% 100%;
		margin-top: 0.4rem;
		margin-left: 0.16rem;
		position: relative;
	}
	.attack-ip-border{
		position: absolute;
		z-index: 2;
		top: 16%;
		width: 100%;
		height: 0.26rem;
	}
	.be-attacked-ip-border{
		position: absolute;
		z-index: 2;
		top: 58%;
		width: 100%;
		height: 0.26rem;
	}
	.be-attacked-org-border{
		position: absolute;
		z-index: 2;
		top: 82%;
		width: 100%;
		height: 0.26rem;
	}
	.attack-ip, .be-attacked-ip{
		width: 13%;
		height: 0.26rem;
		text-align: center;
		line-height: 0.26rem;
		position: absolute;
	}
	.be-attacked-org{
		width: 15%;
		height: 0.46rem;
		text-align: center;
		line-height: 0.46rem;
		position: absolute;
	}
	.be-attacked-org:nth-child(1){
		left: 10%;
	}
	.be-attacked-org:nth-child(2){
		left: 27%;
	}
	.be-attacked-org:nth-child(3){
		left: 44%;
	}
	.be-attacked-org:nth-child(4){
		left: 61%;
	}
	.be-attacked-org:nth-child(5){
		left: 77%;
	}
	.attack-ip:nth-child(1), .be-attacked-ip:nth-child(1){
		left: 9%;
	}
	.attack-ip:nth-child(2), .be-attacked-ip:nth-child(2){
		left: 27%;
	}
	.attack-ip:nth-child(3), .be-attacked-ip:nth-child(3){
		left: 45%;
	}
	.attack-ip:nth-child(4), .be-attacked-ip:nth-child(4){
		left: 63%;
	}
	.attack-ip:nth-child(5), .be-attacked-ip:nth-child(5){
		left: 81%;
	}
	.global-button{
		position: absolute;
		right: 0;
		top: 0
	}
	.current_bg_color {
		background: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(46, 255, 183, 0.4), rgba(0, 0, 0, 0));;
	}
	.refresh-button{
		width: 98px;
		height: 26px;
		background: url('../../../assets/images/ssa/global-full-second-refresh.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		cursor: pointer;
	}
	.close-button{
		width: 72px;
		height: 26px;
		background: url('../../../assets/images/ssa/global-full-second-close.png');
		background-size: 100% 100%;
		background-repeat: no-repeat;
		margin-left: 5px;
		cursor: pointer;
	}
	.global-rating-border{
		position: relative;
	}
	.global-rating-border .global-title{
		position: absolute;
		top: 0;
		left: 0;
	}
	.event-scroll-detail-content{
		width: 94%;
		height: 100%;
		margin: 0 2% 0 4%;
		padding-top: 0.33rem;
	}
	.event-scroll-detail-content-header{
		width: 100%;
		height: 1.46rem;
		text-align: center;
		line-height: 1.46rem;
		border:  1px solid #69de95;
	}
	.event-scroll-detail-content-header img{
		height: 0.88rem;
		width: 0.78rem;
	}
	.detail-content-ip-item{
		width: 17%;
		text-align: center;
		padding-top: 0.26rem;
	}
	.detail-content-ip-item div{
		width: 100%;
		height: 0.9rem;
		border: 1px solid #a4251f;
		line-height: 0.9rem;
		background: rgba(255, 0, 13, 0.2);
		margin-top: 0.94rem;
	}
	.m-l-bai-3{
		margin-left: 3.5%;
	}
	.detail-content-ip-item div p:nth-child(1){
		margin-top: 0.2rem;
	}
	.event-scroll-detail-content-org{
		border: 1px solid #a4251f;
		text-align: center;
		padding-top: 0.12rem;
		padding-bottom: 0.14rem;
		margin-top: 0.2rem;
		position: relative;
	}
	.detail-content-org-item{
		width: 17%;
		height: 0.9rem;
		border: 1px solid #a4251f;
		background: rgba(255, 0, 13, 0.2);
		text-align: center;
	}
	.detail-content-org-item p:nth-child(1){
		margin-top: 0.2rem;
	}
	.m-r-r-16{
		margin-right: 2.5%;
	}
	.m-l-r-16{
		margin-left: 2.5%;
	}
	.event-scroll-detail-content-arrow-group{
		width: 84%;
		height: 0.69rem;
		background-image: url('../../../assets/images/ssa/global-full-second-arrow-group.png');
		background-repeat: no-repeat;
		background-size: 100% 100%;
		position: absolute;
		z-index: 2;
		top: 2.4rem;
		left: 8.5%;
	}
	.event-scroll-detail .detail-img{
		/*height: 5.92rem;*/
		width: 86%;
		height: 5.92rem;
		position: absolute;
		top: 0.2rem;
		left: 0.7rem;
		z-index: 1;
	}
</style>
<template>
	<div class="global">
		<div class="global-left fLeft">
			<div class="global-box">
				<div class="global-title">
					<div class="fLeft global-title-img"></div>
					<div class="fLeft">
						<div class="global-title-title">Security rating</div>
						<div class="global-title-htitle">内网安全评分</div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="col-md-12 safe-score">
					<div class="col-md-6">
						<div style="padding-top: 0.14rem;">
							<span class="global-color-error-bg displayIB" style="width: 0.1rem; height: 0.1rem"></span>
							<span class="font-normal">最低分数:0</span>
						</div>
						<div class="change-label-color m-t-r-5"></div>
						<div class="m-t-r-5">
							<span class="global-color-cyan-bg displayIB" style="width: 0.1rem; height: 0.1rem"></span>
							<span class="font-normal">最高分数:100</span>
						</div>
					</div>
					<div id="safe-score-score" class="safe-score-score" style="width: 50%;height: 1.8rem">

					</div>
					<div class="safe-score-word" style="width: 50%">
						<div class="global-color-cyan" v-if="securityGrade.score >= 75">低危</div>
						<div class="global-color-green" v-if="securityGrade.score >= 50 && securityGrade.score < 75">中危</div>
						<div class="global-color-org" v-if="securityGrade.score >= 25 && securityGrade.score < 50">高危</div>
						<div class="global-color-error" v-if="securityGrade.score >= 0 && securityGrade.score < 25">危急</div>
						<div>危险级别</div>
					</div>
					<div class="col-md-6 textRight">
						<div style="padding-top: 0.14rem;">
							<span class="font-normal">危急</span>
							<span class="global-color-error-bg displayIB" style="width: 0.1rem; height: 0.1rem"></span>
						</div>
						<div class="change-label-color m-t-r-5 fRight"></div>
						<div class="clearfix"></div>
						<div class="m-t-r-5">
							<span class="font-normal">低危</span>
							<span class="global-color-cyan-bg displayIB" style="width: 0.1rem; height: 0.1rem"></span>
						</div>
					</div>
				</div>
				<div class="clearfix"></div>
				<div class="global-rating-border">
					<div class="global-title m-t-r-10">
						<div class="fLeft global-title-img"></div>
						<div class="fLeft">
							<div class="global-title-title">Security rating</div>
							<div class="global-title-htitle">评分体系</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div id="global-rating-system" style="width: 100%; height: 2.69rem; padding-top: 0.30rem"></div>
				</div>
			</div>
			<div class="global-box m-t-r-5">
				<div class="global-title">
					<div class="fLeft global-title-img"></div>
					<div class="fLeft">
						<div class="global-title-title">Risk categories</div>
						<div class="global-title-htitle">风险IP</div>
					</div>
					<div class="fRight global-title-top">
						TOP5
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="risk-ip-top">
					<div class="fLeft risk-ip-logo">
						<img src="../../../assets/images/ssa/global-full-second-ip.png" alt="">
						<div>{{riskIpTotal || 0}}个</div>
						<div class="m-t-r-5">风险IP总数</div>
					</div>
					<div class="fRight risk-ip-content">
						<div v-for="item in eventRiskTop.y" :class="['risk-ip-item', $index == 0?'':'m-t-r-8', $index > 2?'': 'global-color-green-green']">
							<div :class="['fLeft', 'center']">{{$index+1}}</div>
							<div class="fRight p-r-5">{{item}}</div>
							<div class="clearfix"></div>
						</div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="global-title">
					<div class="fLeft global-title-img"></div>
					<div class="fLeft">
						<div class="global-title-title">Risk categories</div>
						<div class="global-title-htitle">风险部门</div>
					</div>
					<div class="fRight global-title-top">
						TOP5
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="risk-ip-top">
					<div class="fLeft risk-ip-logo">
						<img src="../../../assets/images/ssa/global-full-second-home.png" style="height: 0.6rem;margin-top: 0.32rem" alt="">
						<div>{{riskOrgTotal || 0}}个</div>
						<div class="m-t-r-5">风险部门总数</div>
					</div>
					<div class="fRight risk-ip-content">
						<div v-for="item in orgRiskCount.y" :class="['risk-ip-item', $index == 0?'':'m-t-r-8', $index > 2?'': 'global-color-green-green']">
							<div :class="['fLeft', 'center']">{{$index+1}}</div>
							<div class="fRight p-r-5">{{item}}</div>
							<div class="clearfix"></div>
						</div>
					</div>
					<div class="clearfix"></div>
				</div>
			</div>
		</div>
		<div class="global-center fLeft">
			<div class="global-center-header" @mouseout="mainChangeStart" @mouseover="mainChangeClear">
				<div :class="['global-center-header-item', 'text-cursor', totalType=='all'?'current_bg_color': '']" :style="{width: width+'%'}" @click="changeContent('all')">
					<div class="displayIB">
						<img class="fLeft" src="../../../assets/images/ssa/global-full-second-product.png" alt="">
						<div class="fLeft global-center-header-item-count">
							<div>事件总数</div>
							<div>{{securityGrade.total | formatterBigCoiunt}}</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div v-show="this.eventStatic.wg && this.eventStatic.wg != 0" :class="['global-center-header-item', 'text-cursor', totalType=='outline'?'current_bg_color': '']" :style="{width: width+'%'}" @click="changeContent('outline')">
					<div class="fLeft split-line"></div>
					<div class="displayIB">
						<img class="fLeft" src="../../../assets/images/ssa/global-full-second-alarm.png" alt="">
						<div class="fLeft global-center-header-item-count">
							<div>违规类事件数</div>
							<div>{{eventStatic.wg | formatterBigCoiunt}}</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div v-show="this.eventStatic.bd && this.eventStatic.bd != 0" :class="['global-center-header-item', 'text-cursor', totalType=='du'?'current_bg_color': '']" :style="{width: width+'%'}" @click="changeContent('du')">
					<div class="fLeft split-line"></div>
					<div class="displayIB">
						<img class="fLeft" src="../../../assets/images/ssa/global-full-second-du.png" alt="">
						<div class="fLeft global-center-header-item-count">
							<div>病毒类事件数</div>
							<div>{{eventStatic.bd | formatterBigCoiunt}}</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div v-show="this.eventStatic.rq && this.eventStatic.rq != 0" :class="['global-center-header-item', 'text-cursor', totalType=='attack'?'current_bg_color': '']" :style="{width: width+'%'}" @click="changeContent('attack')">
					<div class="fLeft split-line"></div>
					<div :class="['displayIB']">
						<img class="fLeft" src="../../../assets/images/ssa/global-full-second-center.png" alt="">
						<div class="fLeft global-center-header-item-count">
							<div>攻击类事件数</div>
							<div>{{eventStatic.rq | formatterBigCoiunt}}</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="clearfix"></div>
			</div>
			<div class="global-center-content" @mouseout="mainChangeStart" @mouseover="mainChangeClear">
				<div class="m-t-r-10 font14">
					<span class="displayIB">
						<span class="d-i-b p-r-5">{{curDate}}</span><span class="d-i-b p-r-5">{{curWeek}}</span>
						<span class="d-i-b p-r-5">{{curTime}}</span>
					</span>
				</div>
				<div class="position-center-border">
					<div class="fLeft global-center-content-left displayIB">
						<img v-if="currentEventKind.name == '攻击类事件数'" src="../../../assets/images/ssa/global-full-second-center.png" alt="">
						<img v-if="currentEventKind.name == '病毒类事件数'" src="../../../assets/images/ssa/global-full-second-du.png" alt="">
						<img v-if="currentEventKind.name == '违规类事件数'" src="../../../assets/images/ssa/global-full-second-alarm.png" alt="">
						<img v-if="currentEventKind.name == '事件总数'" src="../../../assets/images/ssa/global-full-second-product.png" alt="">
						<div>{{currentEventKind.name}}</div>
						<div>{{currentEventKind.total | formatterBigCoiunt}}</div>
						<div v-if="totalType == 'all' || totalType == 'attack'" class="content-left-item" style="margin-top: 0.84rem">
							<i class="ys-icon icon-arrow-right"></i>
							<span>攻击量: </span><span>{{currentEventKind.num | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'attack'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>攻击类型: </span><span>{{currentEventKind.type | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'du'" class="content-left-item" style="margin-top: 0.84rem">
							<i class="ys-icon icon-arrow-right"></i>
							<span>中毒量: </span><span>{{currentEventKind.num | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'du'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>病毒事件类型: </span><span>{{currentEventKind.type | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'outline'" class="content-left-item" style="margin-top: 0.84rem">
							<i class="ys-icon icon-arrow-right"></i>
							<span>违规量: </span><span>{{currentEventKind.num | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'outline'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>违规事件类型: </span><span>{{currentEventKind.type | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'attack'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>攻击源IP数: </span><span>{{currentEventKind.src_ip | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'attack'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>被攻击IP数: </span><span>{{currentEventKind.dst_ip | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'du'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>中毒终端IP数: </span><span>{{currentEventKind.src_ip | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'outline'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>违规终端IP数: </span><span>{{currentEventKind.src_ip | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'all'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>被攻击IP数: </span><span>{{currentEventKind.type | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'all'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>中毒终端IP数: </span><span>{{currentEventKind.src_ip | formatterBigCoiunt}}</span>
						</div>
						<div v-if="totalType == 'all'" class="content-left-item">
							<i class="ys-icon icon-arrow-right"></i>
							<span>违规终端IP数: </span><span>{{currentEventKind.dst_ip | formatterBigCoiunt}}</span>
						</div>
					</div>
					<div v-if="totalType == 'all'" class="fRight position-center-right">
						<div id="global-full-risk-status" class="fRight" style="width: 72%; height: 100%;"></div>
						<div class="clearfix"></div>
					</div>
					<div class="fRight position-center-right" v-else>
						<div v-if="totalType == 'du' || totalType == 'outline'" class="fRight event-scroll-detail">
							<div class="event-scroll-detail-content">
								<div class="event-scroll-detail-content-arrow-group">
									<div style="text-align: center;height: 0.26rem; line-height: 0.26rem;">风险IP</div>
								</div>
								<div  v-if="totalType == 'du' || totalType == 'outline'" class="event-scroll-detail-content-header global-color-cyan" style="font-size: 0.36rem">
									<!--<img style="margin-right: 15%" src="../../../assets/images/ssa/global-full-second-du.png" alt="">
									<img src="../../../assets/images/ssa/global-full-second-du.png" alt="">
									<img style="margin-left: 15%" src="../../../assets/images/ssa/global-full-second-du.png" alt="">-->
									{{ currentEventKind.event[eventIndex-1].name }}
								</div>
								<!--<div  v-if="currentEventKind.name == '违规类事件数'" class="event-scroll-detail-content-header">
									<img style="margin-right: 15%" src="../../../assets/images/ssa/global-full-second-alarm.png" alt="">
									<img src="../../../assets/images/ssa/global-full-second-alarm.png" alt="">
									<img style="margin-left: 15%" src="../../../assets/images/ssa/global-full-second-alarm.png" alt="">
								</div>-->
								<div class="event-scroll-detail-content-ip" v-if="currentEventKind.attackIp">
									<div v-for="item in currentEventKind.attackIp[eventIndex-1]" track-by="$index" :class="['detail-content-ip-item', 'fLeft', $index == 0? '': 'm-l-bai-3']">
										<img src="../../../assets/images/ssa/global-full-second-arrow.png" alt="">
										<div>
											<p>TOP{{ $index+1 }}</p>
											<p>{{item}}</p>
										</div>
										<img style="margin-top: 0.26rem" src="../../../assets/images/ssa/global-full-second-arrow.png" alt="">
									</div>
									<div class="clearfix"></div>
								</div>
								<div class="event-scroll-detail-content-org">
									<div>风险IP所属单位</div>
									<div v-if="currentEventKind.attackedOrg">
										<div v-for="item in currentEventKind.attackedOrg[eventIndex-1]" style="margin-top: 0.2rem;" track-by="$index" :class="['fLeft', 'detail-content-org-item', $index == 0?'m-l-r-16 m-r-r-16': 'm-r-r-16']">
											<p>TOP{{ $index+1 }}</p>
											<p>{{item}}</p>
										</div>
										<div class="clearfix"></div>
									</div>
								</div>
							</div>
						</div>
						<div v-if="totalType == 'attack'" class="fRight event-scroll-detail">
							<img class="detail-img" src="../../../assets/images/ssa/global-full-second-detail.png" alt="">
							<div class="attack-ip-border" v-if="currentEventKind.attackIp">
								<div v-for="item in currentEventKind.attackIp[eventIndex-1]" track-by="$index" class="attack-ip">
									{{item}}
								</div>
							</div>
							<div class="be-attacked-ip-border" v-if="currentEventKind.attackedIp">
								<div v-for="item in currentEventKind.attackedIp[eventIndex-1]" track-by="$index" class="be-attacked-ip">
									{{item}}
								</div>
							</div>
							<div class="be-attacked-org-border" v-if="currentEventKind.attackedOrg">
								<div v-for="item in currentEventKind.attackedOrg[eventIndex-1]" track-by="$index" class="be-attacked-org">
									{{item}}
								</div>
							</div>
						</div>
						<div class="fRight center-scroll-border displayIB">
							<div class="center-scroll-name" style="width: 80px">事件类型</div>
							<div class="event-scroll-border">
								<div v-if="currentEventKind.event" class="event-scroll-content" @mouseover="eventRolling('', true)" @mouseout="eventScroll">
									<div v-for="item in currentEventKind.event" track-by="$index" :class="['event-scroll-item', $index == 0?'':'m-t-r-20', $index == eventIndex-1?'event-scroll-item-active': '']">
										<div>{{item.name}}</div>
										<div>{{item.value | formatterBigCoiunt}}</div>
									</div>
								</div>
							</div>
							<div class="event-scroll-page" style="margin-top: 0.13rem">{{ showEventIndex }}/{{ currentEventKind.event? (currentEventKind.event.length > 4?currentEventKind.event.length - 5: currentEventKind.event.length): 0 }}</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="clearfix"></div>
				</div>
			</div>
			<div class="global-center-footer">
				<div class="global-box fLeft">
					<div class="global-title">
						<div class="fLeft global-title-img"></div>
						<div class="fLeft">
							<div class="global-title-title">Data visualization</div>
							<div class="global-title-htitle">事件趋势</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="m-t-r-10" style="height: 2.1rem;width: 100%" id="global-net-flow"></div>
				</div>
				<div class="global-box fRight">
					<div class="global-title">
						<div class="fLeft global-title-img"></div>
						<div class="fLeft">
							<div class="global-title-title">The real-time event</div>
							<div class="global-title-htitle">实时事件</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="table-item-header m-t-r-10 font-normal">
						<div class="col-md-12">
							<div class="col-md-2">事件来源</div>
							<div class="col-md-3">事件类型</div>
							<div class="col-md-3">事件相关IP</div>
							<div class="col-md-4">时间</div>
							<div class="clearfix"></div>
						</div>
					</div>
					<div class="table-body-border font-normal">
						<div class="table-body" @mouseover="dynamicRolling('', true)" @mouseout="startScroll">
							<div class="table-item-body" v-for="list in newEvent" :class="$index?'m-t-r-5':''" track-by="$index">
								<div class="col-md-2 overHidden tdItem" :title="list.type">{{list.name}}</div>
								<div class="col-md-3 overHidden tdItem" :title="list.event">{{list.app}}</div>
								<div class="col-md-3 overHidden tdItem" :title="list.addr">{{list.ip}}</div>
								<div class="col-md-4 overHidden tdItem" :title="list.time">{{list.time}}</div>
								<div class="clear"></div>
							</div>
						</div>
					</div>
				</div>
				<div class="clearfix"></div>
			</div>
		</div>
		<div class="global-right fRight">
			<div class="global-box">
				<div class="global-title pos-r">
					<div class="fLeft global-title-img"></div>
					<div class="fLeft">
						<div class="global-title-title">Terminal security ch</div>
						<div class="global-title-htitle">终端安全检查</div>
					</div>
					<div class="global-button">
						<div class="refresh-button fLeft" @click="refreshGlobal()"></div>
						<div class="fLeft m-l-5 text-cursor" @click="modalStatus = true">
							<img style="width: 30px;height:26px;" src="../../../assets/images/ssa/global-full-second-time-setting.png" alt="">
						</div>
						<div class="close-button fLeft" @click="closeFullPage()"></div>
						<div class="clearfix"></div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="global-bottom-line"></div>
				<div class="safe-search">
					<div class="fLeft safe-search-item">
						<div class="global-color-green1">危急</div>
						<div class="global-color-green1">{{safeResultData.super || 0}}台</div>
						<div class="safe-search-item-percent">
							<div class="safe-search-item-percent-active global-color-green-green1"></div>
						</div>
					</div>
					<div class="fLeft safe-search-item">
						<div class="global-color-green1">高危</div>
						<div class="global-color-green1">{{safeResultData.high || 0}}台</div>
						<div class="safe-search-item-percent">
							<div class="safe-search-item-percent-active global-color-green-green1"></div>
						</div>
					</div>
					<div class="fRight safe-search-item">
						<div class="global-color-green1">低危</div>
						<div class="global-color-green1">{{safeResultData.mid || 0}}台</div>
						<div class="safe-search-item-percent">
							<div class="safe-search-item-percent-active global-color-green-green1"></div>
						</div>
					</div>
					<div class="fRight safe-search-item">
						<div class="global-color-green1">中危</div>
						<div class="global-color-green1">{{safeResultData.low || 0}}台</div>
						<div class="safe-search-item-percent">
							<div class="safe-search-item-percent-active global-color-green-green1"></div>
						</div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div class="outOfLine-type">
					<div class="global-title">
						<div class="fLeft global-title-img"></div>
						<div class="fLeft">
							<div class="global-title-title" title="Statistics of illegal units">Statistics of illegal units</div>
							<div class="global-title-htitle" style="width: 1rem">安全检查类型</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<global-full-pie :id="'ssa-global-full-misdeeds-type'"
								                :height="'220px'"
									            :x="'right'"
									            :y="'center'"
									            :position="['100', '50%']"
									            :name="''"
								                :data="outLineType">

					</global-full-pie>
				</div>
			</div>
			<div class="global-box m-t-r-10">
				<div class="fLeft displayIB" style="width: 39%">
					<div class="global-title">
						<div class="fLeft global-title-img"></div>
						<div class="fLeft">
							<div class="global-title-title" style="width: 1rem" title="Statistics of illegal units">Statistics of illegal units</div>
							<div class="global-title-htitle" style="width: 1rem">问题单位</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="outOfLine-org">
						<div v-for="item in terminal_foul_org.y" :class="['risk-ip-item', $index == 0?'':'m-t-r-8', $index > 2?'': 'global-color-green-green global-color-green1']">
							<span class="m-l-10 fLeft displayIB tdItem" :title="item" style="width: 70%">{{item}}</span>
							<div class="fRight m-r-10" style="width: 3px; height: 100%;background:#000"></div>
							<div class="clearfix"></div>
						</div>
					</div>
				</div>
				<div class="fLeft global-center-cell" style="width: 20%;">
					<img src="../../../assets/images/ssa/global-full-second-battery.png" style="height: 100%" alt="">
				</div>
				<div class="fRight displayIB" style="width: 39%;margin-left: 1%">
					<div class="global-title">
						<div class="fLeft global-title-img"></div>
						<div class="fLeft">
							<div class="global-title-title" style="width: 1rem" title="Violation of the terminal">Violation of the terminal</div>
							<div class="global-title-htitle" style="width: 1rem">问题终端</div>
						</div>
						<div class="clearfix"></div>
					</div>
					<div class="outOfLine-org">
						<div v-for="item in foulOperation.y" :class="['risk-ip-item', $index == 0?'':'m-t-r-8', $index > 2?'': 'global-color-green-green global-color-green1']">
							<div class="fLeft m-l-10" style="width: 3px; height: 100%;background:#000"></div>
							<span class="m-l-10 fLeft displayIB tdItem" :title="item" style="width: 70%">{{item}}</span>
							<div class="clearfix"></div>
						</div>
					</div>
				</div>
				<div class="clearfix"></div>
			</div>
			<div class="global-box m-t-r-10">
				<div class="global-title">
					<div class="fLeft global-title-img"></div>
					<div class="fLeft">
						<div class="global-title-title">Equipment state</div>
						<div class="global-title-htitle">设备状态</div>
					</div>
					<div class="clearfix"></div>
				</div>
				<div style="width:100%;margin:0.15rem auto 0;" class="clearfix">
					<div id="device-status-full" class="font-normal" style="height: 250px;overflow: hidden;width: 100%">
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
								<!--<td class="detail">
									<span @click="showDetail(list.type)"><i class="ys-icon"
									                                        v-bind:class="[curDetailId == list.type ? 'icon-downlist-up' : 'icon-downlist' ]"></i></span>
								</td>-->
								<td style="text-align: left;">{{list.type}}</td>
								<td>{{list.num}}</td>
								<td class="ys-success-color">{{list.normal}}</td>
								<td class="ys-wasrc_iprn-color">{{list.off}}</td>
								<td class="ys-error-color">{{list.abnormal}}</td>
							</tr>
							<tr class="detail" v-bind:class="[curDetailId == list.type ? 'open' : '' ]"
							    v-for="(index,obj) in list.detail">
								<td class="ys-success-color"></td>
								<td style="text-align: left"><span
										class="displayIB verticalM m-r-5 ys-success-color font26">·</span>
									<span>{{obj.ip}}</span>
								</td>
								<td>{{obj.num}}</td>
								<td class="ys-success-color">{{obj.normal}}</td>
								<td class="ys-warn-color">{{obj.off}}</td>
								<td class="ys-error-color">{{obj.abnormal}}</td>
							</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
		<div class="clearfix"></div>
		<ys-modal :show.sync="modalStatus" :title="'轮播间隔时间设置'">
        <div slot="content">
	        <table class="ys-form-table">
		        <tbody>
			        <tr>
		                <td class="p-b-0">轮播间隔：</td>
		                <td class="p-b-0">
		                  <input class="ys-input"
		                         v-model="playTime"
		                         style="width: 218px"
		                         placeholder="请输入整数，单位(s)">
		                </td>
			        </tr>
		            <tr>
			            <td></td>
			            <td><span>请输入整数,单位(s)</span></td>
		            </tr>
		        </tbody>
	        </table>
        </div>
        <div slot="footer">
        <button class="ys-btn" type="button" @click="changeTimeSetting">
        <span>提交</span>
        </button>
        </div>
        </ys-modal>
	</div>
</template>
<script>
    import Api from 'src/lib/api';
    let echarts = require('echarts/lib/echarts');
    import globalFullBar from './global-full-bar.vue';
    import globalFullPie from './global-full-pie.vue';
    import bubble from './bubble.vue'
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
	            },
	            safeScorePieChart: '',
	            eventIndex: 0,
	            showEventIndex: 0,
	            scrollEventTimer: '',
	            currentEventKind: {},
	            totalType: 'all',
	            riskIpTotal: '',
	            riskOrgTotal: '',
	            width: 25,
	            newEventTimer: '',
	            mainChangeCount: '',
	            mainChangeTimer: '',
	            arr: ['all'],
	            modalStatus: false,
	            playTime: 90
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
		        height: '250',
		        width: '100%',
		        position: 'right',
		        size: "5px",
		        color: '#000',
		        wheelStep: 5
	        });
        },
        components: {
            globalFullBar,
	        globalFullPie,
	        bubble
        },
        methods: {
            changeTimeSetting () {
                this.modalStatus = false;
                let self = this;
                window.clearInterval(self.mainChangeTimer);
                self.mainChangeStart();
            },
            mainChange () {
                console.log(this.mainChangeCount);
                this.mainChangeCount = this.mainChangeCount + 1;
                this.changeContent(this.arr[this.mainChangeCount % this.arr.length]);
            },
	        mainChangeStart () {
		        if(this.eventStatic.wg && this.eventStatic.wg != 0){
			        this.arr.push('outline');
		        }
		        if(this.eventStatic.bd && this.eventStatic.bd != 0){
			        this.arr.push('du');
		        }
		        if(this.eventStatic.rq && this.eventStatic.rq != 0){
			        this.arr.push('attack');
		        }
                let self = this ;
                self.mainChangeTimer = setInterval(self.mainChange, self.playTime*1000);
	        },
	        mainChangeClear () {
                let self = this;
                window.clearInterval(self.mainChangeTimer);
	        },
            changeContent (type) {
                this.totalType = type ;
                if(type == 'attack'){
		            this.getKindOfEventData('攻击');
                }else if(type == 'du'){
		            this.getKindOfEventData('病毒');
                }else if(type == 'outline'){
		            this.getKindOfEventData('违规');
                }else if(type == 'all'){
		            this.getKindOfEventData('全部');
			        this.getAssetStatusData();
                }
	            this.mainChangeCount = this.arr.indexOf(type);
                let self = this ;
                self.eventIndex = 1;
	            self.showEventIndex = 1;
                $('.event-scroll-content').css({'top': 0});
	            window.clearInterval(self.scrollEventTimer);
            },
            //rem配置
	        remConfig () {
		        (function (doc, win) {
			        var docEl = doc.documentElement,
			        //console.log(window);
			        //var docEl = document.getElementById('rem-border'),
			        resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
				        recalc = function () {
			                var clientHeight = docEl.clientHeight;
			                if (!clientHeight) return;
			                if(clientHeight>=1080){
			                    docEl.style.fontSize = '100px';
			                }else{
			                    docEl.style.fontSize = 100 * (clientHeight / 1080) + 'px';
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
                }
                if(this.index == this.newEvent.length-4){
					$('.table-body').animate({
	                    top: 0
	                }, 1);
	                this.index = 0;
                    this.getNewEvent();
                    return false;
                }
	            this.index = index + 1 ;
                $('.table-body').animate({
                    top: -(0.35 * index)+'rem'
                }, 500);
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
	        //事件滚动
	        eventRolling (index, stop) {
                let curIndex = index ;
                if(this.currentEventKind.event.length < 2){
                    return false;
                }
                if(this.currentEventKind.event.length > 4 && this.currentEventKind.event.length-4 === curIndex){
                    this.eventIndex = 1 ;
                    this.showEventIndex = 1;
                    $('.event-scroll-content').css({'top': 0});
                    return false;
                }else if(this.currentEventKind.event.length > 4 && this.currentEventKind.event.length-5 === curIndex){
                    curIndex = index + 1 ;
                    $('.event-scroll-content').animate({
	                    top: -(1.2 * (curIndex-1))+'rem'
	                }, 500);
                    this.eventIndex = curIndex ;
                    this.showEventIndex = 1;
                    return false;
                }
                if(stop){
                    window.clearInterval(this.scrollEventTimer);
                    return false;
                }else{
                    curIndex = index + 1 ;
                }
                if(index === this.currentEventKind.event.length){
                    curIndex = 1 ;
                }
                $('.event-scroll-content').animate({
                    top: -(1.2 * (curIndex-1))+'rem'
                }, 500);
                this.eventIndex = curIndex;
		        this.showEventIndex = curIndex;
            },
	        eventScroll () {
	            if(this.currentEventKind.event.length < 2){
                    return false;
                }
                let self = this ;
                this.scrollEventTimer = setInterval(function () {
                    self.eventRolling(self.eventIndex, false)
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
		        this.getRiskIpOrg();
		        this.getNetFlowData();
		        this.getRatingSystemData();
		        this.changeContent('all');
		        //this.getAssetDetailData();
		        this.getAssetStatus();
		        //this.getThingCountData();
		        this.getOutLineTypeData();
		        this.getFoulOrgData();
		        this.getFoulOperationData();
		        this.getOrgRiskCountData();
		        //this.getAttackScripCountData();
		        //this.getAttackDstipCountData();
		        this.getEventStatic();
		        this.getOverallScore();
		        this.getEventRiskTop();
		        this.getNewEvent();
		        this.mainChangeClear();
		        this.mainChangeStart();
                this.eventIndex = 1;
	            this.showEventIndex = 1;
                $('.event-scroll-content').css({'top': 0});
		        this.totalType = 'outline';
	        },
	        closeFullPage () {
                this.eventIndex = 1;
	            this.showEventIndex = 1;
                $('.event-scroll-content').css({'top': 0});
		        this.totalType = 'outline';
		        window.clearInterval(this.scrollEventTimer);
                this.show = false;
	        },
	        //安全结果统计
	        getSafeResultData () {
		        this.$http.post('/api/ssa/new_global/terminal_level').then(function (response) {
                    if (response.data.status == 200) {
                        this.safeResultData = response.data.data ;
				        this.safeStaticChart = echarts.init(document.getElementById('global-safe-result'));
				        //this.initChart('global-safe-result', this.safeResult, this.safeStaticChart);
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
	         //事件趋势
	        getNetFlowData () {
                this.$http.post('/api/ssa/new_global/assets_event_trend').then(function (response) {
                    if (response.data.status == 200) {
                        this.netFlowData.name = response.data.data.labes;
                        this.netFlowData.data = response.data.data.data;
                        this.netFlowData.x = response.data.data.days;
				        this.trendChart = echarts.init(document.getElementById('global-net-flow'));
				        this.initChart('global-net-flow', this.netFlow, this.trendChart);
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                });
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
					            str += params[key].seriesName +': '+ self.formatteBigCoiunt(params[key].data)+ '<br />' ;
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
					            color: "#fff",
						        opacity: "0.3"
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
					        show: true,
					        formatter: function (value, index) {
					            return self.formatteBigCoiunt1(value);
					        }
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
					        show: true,
					        lineStyle: {
					            color: '#fff',
						        opacity: '0.3'
					        }
				        }
			        },
			        series: series
		        };
		        self.trendChart.setOption(trendOption);
	        },
	        //获取风险iP,部门总数
	        getRiskIpOrg () {
		        this.$http.post('/api/ssa/new_global/risk_ip_org').then(function (response) {
                    if (response.data.status == 200) {
                        this.riskIpTotal = response.data.data.ip_size;
                        this.riskOrgTotal = response.data.data.org_size;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
	        },
	        //格式化事件对应的值
	        formatterEventKindData (arr) {
                if(arr.length < 5){
                    let num = 5 - Number(arr.length);
                    for(let i=0 ; i< num ; i++){
                        arr.push(' ');
                    }
                    return arr ;
                }else{
                    return arr ;
                }
	        },
	        //获取各种事件对应的值
	        getKindOfEventData (type) {
                let data = {
                    type: type
                };
                this.$http.post('/api/ssa/new_global/all_event_count', data).then(function (response) {
                    if (response.data.status == 200) {
						this.currentEventKind = response.data.data;
						for(let k in this.currentEventKind.attackedIp){
						    this.formatterEventKindData(this.currentEventKind.attackedIp[k]);
						}
						for(let n in this.currentEventKind.attackIp){
						    this.formatterEventKindData(this.currentEventKind.attackIp[n]);
						}
						for(let m in this.currentEventKind.attackedOrg){
						    this.formatterEventKindData(this.currentEventKind.attackedOrg[m]);
						}
						for(let i = 0 ; i< this.currentEventKind.event.length ; i++){
						    if(i < 5){
						        if(this.currentEventKind.attackIp.length > 4){
						            this.currentEventKind.attackIp.push(this.currentEventKind.attackIp[i]);
						        }
						        if(this.currentEventKind.event.length > 4){
						            this.currentEventKind.event.push(this.currentEventKind.event[i]);
						        }
						        if(this.currentEventKind.attackedIp.length > 4){
						            this.currentEventKind.attackedIp.push(this.currentEventKind.attackedIp[i]);
						        }
						        if(this.currentEventKind.attackedOrg.length > 4){
						            this.currentEventKind.attackedOrg.push(this.currentEventKind.attackedOrg[i]);
						        }
						    }
						}
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
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
                            value.push(chartData[i].value);
                            series.push({
                                name: chartData[i].name,
                                max: 100
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
                                        str += series[key].name + ': ' + params.value[key] + '分<br/>';
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
                                radius: '77%',
                                nameGap: 10,
	                            splitNumber: 4,
	                            center: ['60%', '50%'],
                                indicator: series,
                                splitArea: {
                                    show: true,
                                    areaStyle: {
                                        color: "rgba(74, 146, 255, 0.05)",
                                    },
                                },
                                splitLine: {
                                    lineStyle: {
                                        color: "rgba(255,255,255,0.3)"
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
                                    color: "rgba(199,0,10,0.3)"
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
                let count = 100 - Number(index)*2;
                if(count > 10){
                    return count ;
                }else{
                    return 10 ;
                }
	        },
	        //去随机数
	        randomArr(maxcount){
		        var arr = [];
		        for(var i=0;i<maxcount;i++){
		            arr.push(i)
		        }
		        return arr;
		    },
		    //取出随机数, maxNum为 取出随机数的个数
            RandomNumBoth(arr,maxNum){
		        var numArr = [];
		        //最大的循环次数
		        var arrLength = arr.length;
		        for(var i = 0;i<arrLength;i++){
		            //获取arr的长度
		            var Rand = arr.length
		            //取出随机数
		            var number = Math.floor(Math.random()*arr.length); //生成随机数num
		            //往新建的数组里面传入数值
		            numArr.push(arr[number]);
		            //传入一个删除一个，避免重复
		            arr.splice(number,1);
		            if(arr.length <= arrLength-maxNum){
		                return numArr;
		            }
		        }
		    },
            //获取风险状态chart
            assetStatusChart() {
                let self = this, colors = ['#F05D5F', '#4A92FF', '#53ADF8'];
                let arr = self.randomArr(100);
                let randomArr = self.RandomNumBoth(arr, 100);
                let datalist = [];
                for(let k=0 ; k<randomArr.length ; k++){
                    datalist.push([randomArr[k], randomArr[randomArr.length-k-1]]);
                }
                /*let datalist = [[56, 48], [35, 80], [20, 43], [83, 30], [36, 20], [64, 10], [75, 75], [93, 72], [0, 12], [50, 6], [100, 20], [10, 20], [20, 0], [0, 60], [20, 80], [50, 100]];*/
                let datas = [];
                for (var i = 0; i < self.plantCap.length; i++) {
                    let count = self.formatterAssetsValue(i);
                    var item = self.plantCap[i];
                    var itemToStyle = datalist[i];
                    datas.push({
                        name: item.name + '\n\n' + item.value,
                        value: itemToStyle,
                        symbolSize: count,
                        label: {
                            normal: {
                                show: count > 50?true:false,
                                textStyle: {
                                    fontSize: 11
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: colors[i<5?0:i>10?2:1],
                                opacity: (Math.random() * 5 + 5) / 10
                            },
	                        z: 100-count
                        },
                    })
                }
                let statusOption = {
                    tooltip: {
				        backgroundColor: 'rgba(74, 146, 255, 0.2)',
				        border: '1px solid rgba(74, 146, 255, 0.3)',
				        formatter: function (params) {
				            return params.name ;
				        }
			        },
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
                this.$http.post('/api/ssa/new_global/foul_type_count').then(function (response) {
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
                this.$http.post('/api/ssa/new_global/foul_org_count').then(function (response) {
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
                        this.eventStatic.wg = response.data.data.event_type.norule;
                        this.eventStatic.rq = response.data.data.event_type.attack;
                        this.eventStatic.bd = response.data.data.event_type.viruses;
                        let count = 0;
                        if(!this.eventStatic.wg || this.eventStatic.wg == 0){
                            count = count + 1;
                        }
                        if(!this.eventStatic.rq || this.eventStatic.rq == 0){
                            count = count + 1;
                        }
                        if(!this.eventStatic.bd || this.eventStatic.bd == 0){
                            count = count + 1;
                        }
                        this.width = 100 / (4-count);
				        this.mainChangeClear();
				        this.mainChangeStart();
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
	                    this.safeScorePieChart = echarts.init(document.getElementById('safe-score-score')) ;
				        this.initChart('safe-score-score', this.safeScorePie, this.safeScorePieChart);
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
	        safeScorePie () {
	            let self = this ;
				let option = {
				    title: {
				        x: '52%',
				        y: '40%',
				        textStyle: {
				            fontWeight: 400,
				            fontSize: 20,
				            color: '#fff'
				        },
				        text: self.securityGrade.score+'分' || '0分'
				    },
				    tooltip: {
				        trigger: 'item',
				        //   formatter: '{c}%'
				    },
				    series: [{
				        type: 'pie',
				        radius: ['40', '45'],
					    center: ['60%', '49%'],
				        startAngle: 235,
				        color: [new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
						    offset: 0,
						    color: '#77faa7'
					    }, {
						    offset: 0.3,
						    color: '#adfb56'
					    }, {
						    offset: 0.7,
						    color: '#f2a342'
					    }, {
						    offset: 1,
						    color: '#eb3328'
					    }]), "transparent"],
				        hoverAnimation: false,
				        label: {
				            normal: {
				                position: 'center'
				            }
				        },
				        data: [{
				                value: 80,
				                //name: data.text,
				                label: {
				                    normal: {
				                        // formatter: '{d} %',
				                        textStyle: {
				                            fontSize: 30,
				                            fontWeight: 600,
				                            //color: data.color,
				                        }
				                    }
				                }
				            },
				            {
				                value: 20,
				                name: '',
				                tooltip: {
				                    show: false
				                },
				                itemStyle: {
				                    normal: {
				                        color: '#293738',
				                    }
				                },
				                label: {
				                    normal: {
				                        //formatter: value + '',
				                        textStyle: {
				                            fontSize: 20,
				                            //color: data.color
				                        }
				                    },

				                }
				            }
				        ]
				    }]
				};
		        self.safeScorePieChart.setOption(option);
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
                        if(response.data.data && response.data.data.length > 0){
                            window.clearInterval(this.scrollTimer);
	                        this.newEvent = response.data.data;
                            if(response.data.data.length > 5){
                                for(let i = 0 ; i< 5 ; i++){
                                    this.newEvent.push(response.data.data[i]);
                                }
                            }
                        }
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
	        formatteBigCoiunt (val) {
                if(val > 99999999){
                    return (val/100000000).toFixed(1) + ' 亿' ;
                }else if(val > 9999){
                    return (val/10000).toFixed(1) + ' 万' ;
                }else{
                    return val ;
                }
	        },
	        formatteBigCoiunt1 (val) {
                if(val > 99999999){
                    return (val/100000000) + ' 亿' ;
                }else if(val > 9999){
                    return (val/10000) + ' 万' ;
                }else{
                    return val ;
                }
	        }
        },
        watch: {
            'show': function () {
                if (this.show) {
                    this.setRealTime();
		            this.getNetFlowData();
		            this.getRatingSystemData();
		            this.getRiskIpOrg();
			        //this.getAssetDetailData();
			        this.getAssetStatus();
			        //this.getThingCountData();
			        this.getOutLineTypeData();
			        this.getFoulOrgData();
			        this.getFoulOperationData();
			        this.getOrgRiskCountData();
		            this.changeContent('all');
			        //this.getAttackScripCountData();
			        //this.getAttackDstipCountData();
			        this.getEventStatic();
			        this.getOverallScore();
			        this.getEventRiskTop();
			        this.getNewEvent();
			        this.remConfig();
			        /*if(this.totalType == 'all'){
				        this.getAssetStatusData();
	                }*/
                }
            },
	        'newEvent': function () {
		        window.clearInterval(this.newEventTimer);
		        if(this.newEvent.length < 6){
			        this.newEventTimer = setInterval(this.getNewEvent, 30000);
		        }
                let self = this ;
	            this.scrollTimer = setInterval(function () {
	                self.dynamicRolling(self.index, false)
	            }, 3000);
            },
	        'currentEventKind.event': {
                handler: function (val, oldVal) {
					let self = this ;
			        window.clearInterval(self.scrollEventTimer);
		            this.scrollEventTimer = setInterval(function () {
		                self.eventRolling(self.eventIndex, false)
		            }, 3000);
                },
		        deep: true
	        }
        },
        destroyed: function () {
            window.clearInterval(this.scrollTimer);
        }
    }
</script>
