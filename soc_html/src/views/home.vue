<template>
  <div class="ys-con" style="display: none;">
    <!--公司用户-->
    <div v-if="userInfo.role_type==3" class="pos-r ys-clear" >
      <div class="box-left">
        <div class="ys-box">
          <div class="ys-box-title">待处理事件</div>
          <div class="ys-box-con" style="height:200px">
            <div class="home-dash-event">
              <p>
                <span class="d-i-b verticalM"><img src="../assets/images/overview-home/mon-dash.svg"/></span>
                <span class="d-i-b verticalM" style="width:120px;">
                  <span class="m-l-15 fw400 font28">{{pendingData.monitor.total}}</span>
                  <span class="m-l-5">次</span>
                </span>
                <span class="ys-info-color verticalM">新增监控告警故障&nbsp;<span>{{pendingData.monitor.new}}</span>&nbsp;次</span>
                <a class="fRight" style="line-height:33px;">立即处理</a>
              </p>
            </div>
            <div class="home-dash-event">
              <p>
                <span class="d-i-b verticalM"><img src="../assets/images/overview-home/attack-dash.svg"/></span>
                <span class="d-i-b verticalM" style="width:120px;">
                  <span class="m-l-15 fw400 font28">{{pendingData.attack.total}}</span>
                  <span class="m-l-5">次</span>
                </span>
                <span class="ys-info-color verticalM">新增攻击事件&nbsp;<span>{{pendingData.attack.new}}</span>&nbsp;次</span>
                <a class="fRight" style="line-height:33px;">立即处理</a>
              </p>
            </div>
            <div class="home-dash-event">
              <p>
                <span class="d-i-b verticalM"><img src="../assets/images/overview-home/scan-dash.svg"/></span>
                <span class="d-i-b verticalM" style="width:120px;">
                  <span class="m-l-15 fw400 font28">{{pendingData.leak.total}}</span>
                  <span class="m-l-5">个</span>
                </span>
                <span class="ys-info-color verticalM">新增漏洞&nbsp;<span>{{pendingData.leak.new}}</span>&nbsp;个</span>
                <a class="fRight" style="line-height:33px;">立即处理</a>
              </p>
            </div>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">服务情况概览</div>
          <div class="ys-box-con ys-clear service-overview" style="min-height:300px;">
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.monitor_status==0">
                  <!--<button class="ys-btn" @click="openService('monitor')">购买服务</button>-->
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/mon-service.svg"/>
                  <span class="m-l-5">监控告警</span>
                </div>
                <div class="content">
                  <p>
                    <span class="ys-info-color">监控告警故障：</span>
                    <span>{{overviewData.monitor.alarm}}</span>
                    <span>次</span>
                    <a class="fRight" v-link="{name:'server-mon-mgt'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">已部署监控项：</span>
                    <span>{{overviewData.monitor.done}}</span>
                    <span>个</span>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.hw_status==0">
                  <button class="ys-btn" @click="openService('hw')">购买服务</button>
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/defense-service.svg"/>
                  <span class="m-l-5">高防服务</span>
                </div>
                <div class="content">
                  <p>
                    <span class="ys-info-color">为您清洗攻击峰值：</span>
                    <span>{{overviewData.hw.for_you}}</span>
                    <span>Gbps</span>
                    <a class="fRight" v-link="{name:'defense-ip-mgt'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">服务即将到期IP数：</span>
                    <span>{{overviewData.hw.expiring}}</span>
                    <a class="fRight" v-link="{name:'defense-service-upgrade'}">续费</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.cloud_status==0">
                  <button class="ys-btn" @click="openService('cloud')">购买服务</button>
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/cloud-defense-service.svg"/>
                  <span class="m-l-5">云防御</span>
                </div>
                <div class="content">
                  <p>
                    <span class="ys-info-color">已开启防御域名：</span>
                    <span>{{overviewData.cloud.done}}</span>
                    <span>/</span>
                    <span>{{overviewData.cloud.all}}</span>
                    <a class="fRight" v-link="{name:'cloud-de-service-buy'}">购买防御</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">服务即将到期域名：</span>
                    <span>{{overviewData.cloud.expiring}}</span>
                    <a class="fRight" v-link="{name:'cloud-de-service-upgrade'}">续费</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.waf_status==0">
                  <button class="ys-btn" @click="openService('waf')">购买服务</button>
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/waf-service.svg"/>
                  <span class="m-l-5">WAF防御</span>
                </div>
                <div class="content">
                  <p class="m-t-10">
                    <span class="ys-info-color">已开启防御域名：</span>
                    <span>{{overviewData.waf.done}}</span>
                    <span>/</span>
                    <span>{{overviewData.waf.all}}</span>
                    <a class="fRight" v-link="{name:'waf-buy'}">购买防御</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">服务即将到期域名：</span>
                    <span>{{overviewData.waf.expiring}}</span>
                    <a class="fRight" v-link="{name:'waf-buy'}">续费</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.scan_status==0">
                  <!--<button class="ys-btn" @click="openService('scan')">购买服务</button>-->
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/scan-service.svg"/>
                  <span class="m-l-5">漏洞扫描</span>
                </div>
                <div class="content">
                  <p>
                    <span class="ys-info-color">新增漏洞：</span>
                    <span>{{overviewData.scan.new}}</span>
                    <span>次</span>
                    <a class="fRight" v-link="{name:'scan-domain-list'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">高危资产：</span>
                    <span>{{overviewData.scan.high_leak_assets}}</span>
                    <span>个</span>
                    <a class="fRight" v-link="{name:'scan-host-list'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">已扫描项：</span>
                    <span>{{overviewData.scan.done}}</span>
                    <a class="fRight" v-link="{name:'scan-domain-list'}">新建任务</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.hids_status==0">
                  <button class="ys-btn" @click="openService('hids')">购买服务</button>
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/hids-service.svg"/>
                  <span class="m-l-5">终端安全</span>
                </div>
                <div class="content">
                  <p class="m-t-10">
                    <span class="ys-info-color">已部署终端：</span>
                    <span>{{overviewData.hids.done}}</span>
                    <span>个</span>
                    <a class="fRight" v-link="{name:'hids-agent'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">服务即将到期：</span>
                    <span>{{overviewData.hids.expiring}}</span>
                    <a class="fRight" v-link="{name:'hids-buy'}">续费</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.nids_status==0">
                  <button class="ys-btn" @click="openService('nids')">购买服务</button>
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/ids-service.svg"/>
                  <span class="m-l-5">网络安全</span>
                </div>
                <div class="content">
                  <p>
                    <span class="ys-info-color">攻击事件：</span>
                    <span>{{overviewData.nids.attacks}}</span>
                    <span>次</span>
                    <a class="fRight" v-link="{name:'nids-base'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">告警：</span>
                    <span>{{overviewData.nids.alarm}}</span>
                    <span>次</span>
                    <a class="fRight" v-link="{name:'nids-base'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">已部署设备：</span>
                    <span>{{overviewData.nids.done}}</span>
                    <a class="fRight" v-link="{name:'nids-base'}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">服务即将到期：</span>
                    <span>{{overviewData.nids.expiring}}</span>
                    <a class="fRight" v-link="{name:'nids-service'}">续费</a>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="service-disabled" v-if="overviewData.dbs_status==0">
                  <button class="ys-btn" @click="openService('dbs')">购买服务</button>
                </div>
                <div class="title">
                  <img src="../assets/images/overview-home/dbs-service.svg"/>
                  <span class="m-l-5">数据库安全</span>
                </div>
                <div class="content">
                  <p>
                    <span class="ys-info-color">攻击事件：</span>
                    <span>{{overviewData.dbs.attacks}}</span>
                    <span>次</span>
                    <a class="fRight" v-link="{name:''}">查看详情</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">已开启服务项：</span>
                    <span>{{overviewData.dbs.done}}</span>
                    <span>/</span>
                    <span>{{overviewData.dbs.all}}</span>
                    <a class="fRight" v-link="{name:''}">购买防护</a>
                  </p>
                  <p class="m-t-10">
                    <span class="ys-info-color">服务即将到期：</span>
                    <span>{{overviewData.dbs.expiring}}</span>
                    <a class="fRight" v-link="{name:''}">续费</a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="box-right">
        <div class="ys-box" v-if="1<0">
          <div class="ys-box-title">
            <i class="ys-icon icon-notice m-r-5 main-color"></i>公告
            <a class="fRight">更多</a></div>
          <div class="ys-box-con" style="height:200px">
            <p v-bind:class="[$index==0 ? '' : 'm-t-15' ]" v-for="list in noticeData">
              <span class="m-r-10">{{list.date}}</span>{{list.note}}
            </p>
            <p v-if="noticeData.length==0" class="textC" style="line-height:170px;">当前没有公告</p>
          </div>
        </div>
        <div class="ys-box">
          <div class="ys-box-title">事件时间线</div>
          <div class="ys-box-con" style="height:484px;">
            <p v-if="logData.length==0" style="line-height:484px;" class="ys-info-color textC">当前没有事件</p>
            <div class="ys-timeline">
              <div class="time-item" v-for="list in logData" v-show="$index<5">
                <span class="time-icon ys-primary-color"><i class="ys-icon icon-clock"></i></span>
                <div class="item-info">
                  <p class="font12">{{list.title}}</p>
                  <div class="ys-info-color">{{list.create_time}}<span class="m-l-10"></span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--公司用户-->
    <!--代理商-->
    <div v-if="userInfo.role_type==1 || userInfo.role_type==2" class="pos-r ys-clear">
      <div class="box-left">
        <div class="ys-box">
          <div class="ys-box-title">待处理事件</div>
          <div class="ys-box-con">
            <div class="home-dash-event">
              <p>
                <span class="d-i-b verticalM"><img src="../assets/images/overview-home/mon-dash.svg"/></span>
                <span class="d-i-b verticalM" style="width:120px;">
                  <span class="m-l-15 fw400 font28">{{pendingData.monitor.total}}</span>
                  <span class="m-l-5">次</span>
                </span>
                <span class="ys-info-color verticalM">新增监控告警故障&nbsp;<span>{{pendingData.monitor.new}}</span>&nbsp;次</span>
                <a class="fRight" style="line-height:33px;">立即处理</a>
              </p>
            </div>
            <div class="home-dash-event">
              <p>
                <span class="d-i-b verticalM" style="width:32px;"><img src="../assets/images/overview-home/order-dash.svg"/></span>
                <span class="d-i-b verticalM" style="width:120px;">
                  <span class="m-l-15 fw400 font28">{{pendingData.ticket.total}}</span>
                  <span class="m-l-5">条</span>
                </span>
                <span class="ys-info-color verticalM">新增工单&nbsp;<span>{{pendingData.ticket.new}}</span>&nbsp;条</span>
                <a class="fRight" style="line-height:33px;">立即处理</a>
              </p>
            </div>
            <div class="home-dash-event">
              <p>
                <span class="d-i-b verticalM"><img src="../assets/images/overview-home/attack-dash.svg"/></span>
                <span class="d-i-b verticalM" style="width:120px;">
                  <span class="m-l-15 fw400 font28">{{pendingData.attack.total}}</span>
                  <span class="m-l-5">次</span>
                </span>
                <span class="ys-info-color verticalM">新增攻击事件&nbsp;<span>{{pendingData.attack.new}}</span>&nbsp;次</span>
                <a class="fRight" style="line-height:33px;">立即处理</a>
              </p>
            </div>
            <div class="home-dash-event">
              <p>
                <span class="d-i-b verticalM"><img src="../assets/images/overview-home/scan-dash.svg"/></span>
                <span class="d-i-b verticalM" style="width:120px;">
                  <span class="m-l-15 fw400 font28">{{pendingData.leak.total}}</span>
                  <span class="m-l-5">个</span>
                </span>
                <span class="ys-info-color verticalM">新增漏洞&nbsp;<span>{{pendingData.leak.new}}</span>&nbsp;个</span>
                <a class="fRight" style="line-height:33px;">立即处理</a>
              </p>
            </div>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">系统健康度</div>
          <div class="ys-box-con ys-clear service-overview" style="min-height:300px;">
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="status" v-if="systemData.monitor"><i class="ys-icon icon-check-outline"></i></div>
                <div class="title">
                  <i class="ys-icon font22 verticalM"
                     v-bind:class="[systemData.monitor ? 'icon-check-outline ys-success-color' : 'icon-warn-outline ys-error-color' ]"></i>
                  <span class="m-l-5">监控告警</span>
                </div>
                <div class="content">
                  <p v-if="systemData.monitor" class="ys-info-color"><span>监控服务配置正常</span></p>
                  <p v-else class="ys-error-color"><span>监控服务配置异常，功能模块将失效，请联系厂商</span></p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="status" v-if="systemData.hw"><i class="ys-icon icon-check-outline"></i></div>
                <div class="title">
                  <i class="ys-icon font22 verticalM"
                     v-bind:class="[systemData.hw ? 'icon-check-outline ys-success-color' : 'icon-warn-outline ys-error-color' ]"></i>
                  <span class="m-l-5">高防服务</span>
                </div>
                <div class="content">
                  <p v-if="systemData.hw_key" class="ys-info-color"><span>高防服务秘钥已配置</span></p>
                  <p v-else class="ys-error-color m-t-10"><span>高防服务秘钥未配置，功能模块将失效，请联系厂商</span></p>
                  <p v-if="systemData.hw_dc" class="m-t-10 ys-info-color"><span>高防服务数据中心已配置</span></p>
                  <p v-else class="ys-error-color m-t-10"><span>高防服务数据中心未配置，功能模块将失效，请联系厂商</span></p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="status" v-if="systemData.cloud"><i class="ys-icon icon-check-outline"></i></div>
                <div class="title">
                  <i class="ys-icon font22 verticalM"
                     v-bind:class="[systemData.cloud ? 'icon-check-outline ys-success-color' : 'icon-warn-outline ys-error-color' ]"></i>
                  <span class="m-l-5">云防御</span>
                </div>
                <div class="content">
                  <p v-if="systemData.cloud_qssec" class="ys-info-color"><span>云防御服务连接正常</span></p>
                  <p v-else class="ys-error-color"><span>云防御服务连接异常，功能模块将失效，请联系厂商</span></p>
                  <p v-if="systemData.cloud_qs_api" class="ys-info-color m-t-10"><span>API服务连接正常</span></p>
                  <p v-else class="ys-error-color m-t-10"><span>API服务连接异常，功能模块将失效，请联系厂商</span></p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="status" v-if="systemData.cloud_qssec"><i class="ys-icon icon-check-outline"></i></div>
                <div class="title">
                  <i class="ys-icon font22 verticalM"
                     v-bind:class="[systemData.cloud_qssec ? 'icon-check-outline ys-success-color' : 'icon-warn-outline ys-error-color' ]"></i>
                  <span class="m-l-5">WAF防御</span>
                </div>
                <div class="content">
                  <p v-if="systemData.cloud_qssec" class="ys-info-color"><span>WAF防御服务连接正常</span></p>
                  <p v-else class="ys-error-color"><span>WAF防御服务连接异常，功能模块将失效，请联系厂商</span></p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="status" v-if="systemData.scan"><i class="ys-icon icon-check-outline"></i></div>
                <div class="title">
                  <i class="ys-icon font22 verticalM"
                     v-bind:class="[systemData.scan ? 'icon-check-outline ys-success-color' : 'icon-warn-outline ys-error-color' ]"></i>
                  <span class="m-l-5">漏洞扫描</span>
                </div>
                <div class="content">
                  <p v-if="systemData.scan_conf" class="ys-info-color"><span>扫描器已配置</span></p>
                  <p v-else class="ys-error-color"><span>扫描器未配置，功能模块将失效, 请联系厂商</span></p>
                  <p v-if="systemData.scan_tools" class="ys-info-color m-t-10"><span>扫描器连接正常</span></p>
                  <p v-else class="ys-error-color m-t-10"><span>扫描器连接失败，功能模块将失效, 请联系厂商</span></p>
                  <p v-if="systemData.scan_dir" class="ys-info-color m-t-10"><span>扫描报告目录正常</span></p>
                  <p v-else class="ys-error-color m-t-10"><span>扫描报告目录不可写，扫描报告将无法存储, 请联系厂商</span></p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="status" v-if="systemData.hids"><i class="ys-icon icon-check-outline"></i></div>
                <div class="title">
                  <i class="ys-icon font22 verticalM"
                     v-bind:class="[systemData.hids ? 'icon-check-outline ys-success-color' : 'icon-warn-outline ys-error-color' ]"></i>
                  <span class="m-l-5">终端安全</span>
                </div>
                <div class="content">
                  <p v-if="systemData.hids_conf" class="ys-info-color"><span>终端安全服务已配置</span></p>
                  <p v-else class="ys-error-color"><span>终端安全服务未配置，功能模块将失效, 请联系厂商</span></p>
                  <p v-if="systemData.hids_tools" class="ys-info-color m-t-10"><span>终端安全服务连接正常</span></p>
                  <p v-else class="ys-error-color m-t-10"><span>终端安全服务连接失败，功能模块将失效, 请联系厂商</span></p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="service-overview-box">
                <div class="status" v-if="systemData.nids[0].status"><i class="ys-icon icon-check-outline"></i></div>
                <div class="title">
                  <i class="ys-icon font22 verticalM"
                     v-bind:class="[systemData.nids[0].status ? 'icon-check-outline ys-success-color' : 'icon-warn-outline ys-error-color' ]"></i>
                  <span class="m-l-5">网络安全</span>
                </div>
                <div class="content">
                  <p v-if="systemData.nids[0].status" class="ys-info-color"><span>IDPS设备连接正常</span></p>
                  <p v-else class="ys-error-color"><span>IDPS设备连接失败，功能模块将失效, 请联系厂商</span></p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="ys-clear m-t-5">
          <div class="col-md-6 p-0 p-r-5">
            <div class="ys-box">
              <div class="ys-box-title">CPU使用率(60分钟)</div>
              <div class="ys-box-con">
                <line-chart
                        :id="'home-cpu-usage-rate'"
                        :height="'200px'"
                        :name="cpuUsageRate.name"
                        :x="cpuUsageRate.x"
                        :color="cpuUsageRate.color"
                        :series="cpuUsageRate.series"
                        :unit="'percent'"></line-chart>
              </div>
            </div>
          </div>
          <div class="col-md-6 p-0">
            <div class="ys-box">
              <div class="ys-box-title">内存使用率(60分钟)</div>
              <div class="ys-box-con">
                <line-chart
                        :id="'home-storage-usage-rate'"
                        :height="'200px'"
                        :name="storageUsageRate.name"
                        :x="storageUsageRate.x"
                        :color="storageUsageRate.color"
                        :series="storageUsageRate.series"
                        :unit="'percent'"></line-chart>
              </div>
            </div>
          </div>
        </div>
        <div class="ys-clear m-t-5">
          <div class="col-md-6 p-0 p-r-5">
            <div class="ys-box">
              <div class="ys-box-title">网卡流量(60分钟)</div>
              <div class="ys-box-con">
                <line-chart
                        :id="'home-network-usage-rate'"
                        :height="'200px'"
                        :name="networkUsageRate.name"
                        :x="networkUsageRate.x"
                        :color="networkUsageRate.color"
                        :series="networkUsageRate.series"
                        :unit="'band'"></line-chart>
              </div>
            </div>
          </div>
          <div class="col-md-6 p-0">
            <div class="ys-box">
              <div class="ys-box-title">磁盘使用率(60分钟)</div>
              <div class="ys-box-con" style="height:230px;">
                <div v-for="list in diskData">
                  <div class="pos-r" style="margin-top:40px;">
                    <div style="position: absolute;left:0px;">{{list.name}}：</div>
                    <div style="margin-left:55px;margin-right:55px;">
                      <percent :data="list.percent" :width="'100%'"></percent>
                    </div>
                    <div style="position: absolute;right:0px;top:0px;" class="m-l-5">{{list.percent}}%</div>
                  </div>
                  <p class="m-t-15 textR">
                    <span class="ys-info-color">可用空间：</span>
                    <span>{{list.left | changeUnit}}</span>
                  </p>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="box-right">
        <div class="ys-box">
          <div class="ys-box-title">服务收入与支出</div>
          <div class="ys-box-con">
            <table class="ys-table">
              <thead>
              <tr>
                <th>名称</th>
                <th>收入（元）</th>
                <th>支出（元）</th>
              </tr>
              </thead>
              <tbody>
                <tr v-for="list in billData">
                  <td>{{list.name}}</td>
                  <td class="ys-error-color">{{list.income}}</td>
                  <td>{{list.expense}}</td>
                </tr>
              </tbody>
              <tbody v-if="billData.length==0">
                <tr>
                  <td colspan="3">当前没有收支数据</td>
                </tr>
                <tr v-for="x in 4"><td colspan="3"></td></tr>
              </tbody>
            </table>
            <p class="m-t-10" v-if="billData.length>0"><a>查看详情</a></p>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">用户购买服务数量TOP5</div>
          <div class="ys-box-con">
            <ling-bar-chart :id="'home-user-buy-service-top-5'"
                            :height="'240px'"
                            :name="'服务名称'"
                            :color="'#dabb61'"
                            :x="serviceCountData.x"
                            :y="serviceCountData.y"
                            :unit="'个'"></ling-bar-chart>
          </div>
        </div>
        <div class="ys-box m-t-5">
          <div class="ys-box-title">事件时间线</div>
          <div class="ys-box-con">
            <div class="ys-timeline">
              <div class="time-item" v-for="list in logData" v-show="$index<5">
                <span class="time-icon ys-primary-color"><i class="ys-icon icon-clock"></i></span>
                <div class="item-info">
                  <p class="font12">{{list.title}}</p>
                  <div class="ys-info-color">{{list.create_time}}<span class="m-l-10"></span></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--代理商-->
  </div>
</template>
<style scoped>
  .home-dash-event{
    padding: 10px 15px;
    background:rgba(0,0,0,0.2);
    margin-bottom:5px;
  }
  .service-overview .col-md-6{
    padding-left: 0px;
    padding-right: 0px;
    margin-bottom:5px;
  }

  .service-overview .col-md-6:nth-child(odd){
    padding-right: 5px;
  }
  .service-overview-box{
    background: rgba(0,0,0,0.2);
    height:174px;
    position: relative;
    overflow: hidden;
    position: relative;
  }
  .service-disabled{
    width:100%;
    height:174px;
    line-height:174px;
    background:rgba(0,0,0,0.2);
    position: absolute;
    top:0px;
    left:0px;
    text-align: center;
    z-index:1;
  }
  .service-overview-box .title{
    height:40px;
    line-height:40px;
    margin:0px 15px;
    position: relative;
  }
  .service-overview-box .status{
    height:115px;
    width:115px;
    position:absolute;
    bottom:-25px;
    right:15px;
    color:rgba(0,189,133,0.08);
  }
  .service-overview-box .status i{
    font-size:115px;
  }
  .service-overview-box .title:before{
    content:"";
    height:1px;
    width:100%;
    position:absolute;
    bottom:0px;
    margin-right:15px;
    background:rgba(255,255,255,0.08);
  }
  .service-overview-box .content{
    padding:15px;
  }
  .home-disabled {
    position: absolute;
    left: 0px;
    top: -10px;
    width: 93%;
    z-index: 2;
    background: rgba(0, 0, 0, 0.6);
  }

  .home-icon-none {
    color: #5f749b;
  }

  /* Time line 2 */
  .ys-timeline {
    position: relative;
  }

  .time-icon{
    position: absolute;
    left:0px;
    top:0px;
  }

  .time-item {
    padding-bottom: 1px;
    position: relative;
  }

  .time-item:before {
    content: " ";
    display: table;
    border-left: 1px solid rgba(74,146,255,0.15);
    height: 55px;
    position: absolute;
    left: 5px;
    top: 12px;
  }

  .item-info {
    padding-bottom: 25px;
    margin-left: 18px;
  }
  .time-item:last-child .item-info{
    padding-bottom: 0px;
  }
  .time-item:last-child:before{
    height:20px;
  }
  .item-info p {
    margin-bottom: 5px !important;
  }
</style>
<script>
  import Api from '../lib/api'
  import {getUser} from 'src/lib/getter'
  export default {
    vuex: {
      getters: {
        userInfo: getUser,
      },
    },
    data() {
      return {
        pendingData:{
          attack:{},
          leak:{},
          monitor:{},
          ticket:{},
        },
        billData:[],
        logData:[],
        cpuUsageRate:{
          name:["CPU使用率"],
          x:"",
          color:['#dabb61'],
          series:[
            {data:[]}
          ]
        },
        storageUsageRate:{
          name:["内存使用率"],
          x:"",
          color:['#4a92ff'],
          series:[
            {data:[]}
          ]
        },
        networkUsageRate:{
          name:["入口流量","出口流量"],
          x:"",
          color:['#00bd85','#4a92ff'],
          series:[
            {data:[]},
            {data:[]},
          ]
        },
        diskData:[],
        systemData:{
          nids:[
            {status:false}
          ]
        },
        serviceCountData:{x:"",y:""},
        overviewData:{
          cloud:{},
          waf:{},
          monitor:{},
          scan:{},
          hw:{},
          hids:{},
          nids:{},
          dbs:{}
        },
        noticeData:[]
      }
    },
    filters: {
      changeUnit(val){
        if (val < 1024) {
          return val + "b"
        } else if (val >= 1024 && val < 1024 * 1024) {
          val = (val / 1024).toFixed(1);
          return val + "Kb"
        } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024)).toFixed(1);
          return val + "Mb"
        } else if (val >= 1024 * 1024 * 1024) {
          val = (val / (1024 * 1024 * 1024)).toFixed(1);
          return val + "Gb"
        }
      }
    },
    computed: {
      role_type: {
        get: function () {
          return this.$store.state.user.role_type
        }
      }
    },
    ready: function () {
//      let self=this;
//      let repeat=setInterval(function(){
//        if(self.userInfo.role_type){
//          self.getData()
//          clearInterval(repeat)
//        }
//      },100)
    },
    methods: {
      getData(){
        if(this.userInfo.role_type==1 || this.userInfo.role_type==2){
          this.getAgentData()
        }else{
          this.getUserData()
        }
      },
      getUserData(){
        this.$http.get('/api/pending_tasks').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.pendingData=data
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
        this.$http.get('/api/service/summary').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.overviewData=data
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
        this.$http.get('/api/notice').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.noticeData=data
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
        this.$http.get('/api/event_timeline').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.logData=data
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      getAgentData(){
        this.$http.get('/api/pending_tasks').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.pendingData=data
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
        this.$http.get('/api/bills').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.billData=data
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
        this.$http.get('/api/service/top5').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            let xArr=[];
            let yArr=[];
            for(let x in data){
              xArr.push(data[x].name)
              yArr.push(data[x].value)
            }
            this.serviceCountData.x=yArr.reverse();
            this.serviceCountData.y=xArr.reverse();
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })

        this.$http.get('/api/system/monitor/all').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.cpuUsageRate.x=data.cpu.time;
            this.cpuUsageRate.series[0].data=data.cpu.data;
            this.storageUsageRate.x=data.mem.time;
            this.storageUsageRate.series[0].data=data.mem.data;
            this.networkUsageRate.x=data.net.time;

            let arr=[];
            let arr1=[];
            let netData=data.net.data;
            for(let x in netData){
              arr.push(netData[x].in)
              arr1.push(netData[x].out)
            }
            this.networkUsageRate.series[0].data=arr;
            this.networkUsageRate.series[1].data=arr1;

            let diskArr=[]
            let diskData=data.disk.data[data.disk.data.length-1];
            for(let x in diskData){
              diskArr.push({
                name:diskData[x].name,
                percent:(diskData[x].used / diskData[x].all * 100).toFixed(1),
                left:(diskData[x].all-diskData[x].used).toFixed(1)
              })
            }
            this.diskData=diskArr;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
        this.$http.get('/api/event_timeline').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.logData=data
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
        this.$http.get('/api/system/sys_status?re_check=soc_component').then(function (response) {
          if (response.data.status == 200) {
            let data=response.data.data
            this.systemData=data.soc_component;
          } else {
            this.$root.alertError = true;
          }
          this.$root.errorMsg = response.data.msg
        }, function (response) {
          Api.user.requestFalse(response,this);
        })
      },
      openService(type){
        switch(type)
        {
          case "hw":
            this.$router.go({name: "defense-service-buy"})
            break;
          case "cloud":
            this.$router.go({name: "cloud-de-service-buy"})
            break;
          case "waf":
            this.$router.go({name: "waf-buy"})
            break;
          case "hids":
            this.$router.go({name: "hids-buy"})
            break;
          case "nids":
            this.$router.go({name: "nids-service"})
            break;
          case "dbs":
            this.$router.go({name: "hw-devices"})
            break;
          default:;
        }
      }
    },
    watch: {

    },
    components: {},
  }
</script>
