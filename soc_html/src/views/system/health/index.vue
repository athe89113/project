<template>
  <div>
    <div class="ys-box">
      <div class="ys-box-con" v-if="curStep==false">
        <div class="ys-box-con textC  m-t-20" :class="[system_status ? 'bor-green-bg-solid' : 'bor-red-bg-solid']">
          <div class="m-t-10 ys-success-color" v-show="system_status">
            <i class="ys-icon icon-check-circle ys-success-color font16"></i>
            <span class="font14">系统正常</span>
          </div>
          <div class="m-t-10 ys-error-color" v-else="">
             <i class="ys-icon icon-warn-circle ys-error-color font16"></i>
            <span class="font14">系统不可用</span>
          </div>
          <div class="m-t-10">最后检查时间 {{lastTime}}<a class="m-l-5" @click="fetchStatus(1)">重新检查</a></div>
          <button class="ys-btn m-r-10 m-t-10" @click="step=2" v-show="step==1">查看详情</button>
        </div>
      </div>
      <div class="ys-box-con" v-else="">
        <div class="ys-box-con textC bor-blue-dashed">
          <div class="m-t-10">
            <span>
              <loading-mini :show.sync="loadMini"></loading-mini>
            </span>正在检查
          </div>
          <div class="ys-load-step-con m-t-5">
            <p class="progress-box progress-box-active"
               v-bind:style="{width: curStep + '%'}"></p>
          </div>
          <p class="textC m-t-10">
            <span>{{curStep}}%</span>
          </p>
        </div>
      </div>
    </div>
    <div class="ys-box m-t-10 animated" transition="ysFade" v-show="step==2 || curStep">
      <div class="ys-box-con ys-wrap">
        <div class="col-md-6">

          <div class="ys-box-title ys-box-title-s">中心配置<span class="ys-info-color m-l-5">(必要)</span></div>
          <div class="ys-box-con bor-blue-dashed">
            <info-line :id="'sys_secret_key'" :name="'系统密钥'"
                       :status.sync="sys.secret_key"
                       :emsg="'密钥未配置，请联系厂商'"
                       :smsg="'已配置密钥'">

            </info-line>
            <info-line :id="'sys_run_user'" :name="'运行权限'"
                       :status.sync="sys.run_user"
                       :emsg="'系统需要使用特定用户权限运行，请联系厂商'"
                       :smsg="'运行权限正确'">

            </info-line>
            <info-line :id="'sys_path_conf'" :name="'目录配置'"
                       :status.sync="sys.path_conf"
                       :emsg="'系统目录未配置，请联系厂商'"
                       :smsg="'目录已配置'">

            </info-line>
            <info-line :id="'sys_path_access'" :name="'目录权限'"
                       :status.sync="sys.path_access"
                       :emsg="'系统目录或日志目录无写权限，请联系厂商'"
                       :smsg="'可写权限正常'">

            </info-line>
            <info-line :id="'sys_db'" :name="'数据连接'"
                       :status.sync="sys.db"
                       :emsg="'{系统MySql/数据中心MySql/数据中心ZMQ/Redis}数据服务连接失败，请联系厂商'"
                       :smsg="'数据连接正确'">

            </info-line>
            <info-line :id="'sys_services'" :name="'关联服务'"
                       :status.sync="sys.services"
                       :body="false">
            </info-line>
            <info-line :id="'sys_crm'"
                       :status.sync="sys.crm"
                       :smsg="'CRM服务连接正常, 延迟'+sys.crm_ms+'ms'"
                       :emsg="'CRM服务连接异常，请联系厂商'"
                        :mt="-10"
                       :head="false">
            </info-line>
            <info-line :id="'sys_qssec'"
                       :status.sync="sys.qssec"
                       :smsg="'青松服务连接正常, 延迟'+sys.qssec_ms+'ms'"
                       :emsg="'青松服务连接异常，请联系厂商'"
                       :head="false">
            </info-line>
            <info-line :id="'sys_qs_api'"
                       :status.sync="sys.qs_api"
                       :smsg="'API服务连接正常, 延迟'+sys.qs_api_ms+'ms'"
                       :emsg="'API服务连接异常，请联系厂商'"
                       :head="false">
            </info-line>
            <info-line :id="'sys_icp'"
                       :status.sync="sys.icp"
                       :smsg="'备案查询服务连接正常, 延迟'+sys.icp_ms+'ms'"
                       :emsg="'备案查询服务连接异常，请联系厂商'"
                       :head="false">
            </info-line>

            <info-line :id="'sys_soc_agent'"
                       :status.sync="sys.soc_agent"
                       :name="'Agent配置'"
                       :smsg="'Agent配置正常'"
                       :emsg="'Agent配置异常，请联系厂商'"
            >
            </info-line>
            <info-line :id="'sys_date'"
                       :status.sync="sys.date"
                       :smsg="'系统时间正常, 时差'+sys.date_ms+'ms'"
                       :emsg="'系统时间正常异常，请联系厂商'"
                       :name="'系统时间'">
            </info-line>
            <info-line :id="'sys_message'"
                       :status.sync="sys.message"
                       :name="'通知发送'"
                       :smsg="'通知发送配置正常'"
                       :emsg="'邮件服务/短信未配置，将无法发送通知'"
                       :router="'message-setting'"
                       :retry="false"
                       >
            </info-line>
            <info-line :id="'sys_pay'"
                       :status.sync="sys.pay"
                       :name="'支付配置'"
                       :smsg="'支付信息已配置'"
                       :emsg="'支付信息未配置，将无法完成线上支付'"
                       :router="'finance'"
                       :retry="false"
                       >
            </info-line>
            <info-line :id="'sys_env'"
                       :status.sync="sys.env"
                       :name="'环境配置'"
                       :smsg="'环境标识已配置'"
                       :emsg="'环境标识配置不正确, 请联系厂商'"
                       :retry="true"
                       >
            </info-line>
            <info-line :id="'sys_crontabs'"
                       :status.sync="sys.crontabs"
                       :name="'定时任务'"
                       :body="false"
                       :retry="false"
                       >
            </info-line>
            <info-line :id="'sys_cron_soc_agent'"
                       :status.sync="sys.cron_soc_agent"
                       :smsg="'Agent心跳配置正确'"
                       :emsg="'Agent心跳配置错误，请联系厂商'"
                       :mt="-10"
                       :head="false">
            </info-line>
            <info-line :id="'sys_cron_monitor'"
                       :status.sync="sys.cron_monitor"
                       :smsg="'监控服务配置正确'"
                       :emsg="'监控服务配置错误，请联系厂商'"
                       :head="false">
            </info-line>
            <info-line :id="'sys_cron_asset'"
                       :status.sync="sys.cron_asset"
                       :smsg="'资产检查配置正确'"
                       :emsg="'资产配置错误，请联系厂商'"
                       :head="false">
            </info-line>
            <info-line :id="'sys_cron_hw'"
                       :status.sync="sys.cron_hw"
                       :smsg="'高防服务配置正确'"
                       :emsg="'高防服务配置错误，请联系厂商'"
                       :head="false">
            </info-line>
            <info-line :id="'sys_cron_hids'"
                       :status.sync="sys.cron_hids"
                       :smsg="'终端安全配置正确'"
                       :emsg="'终端安全配置错误，请联系厂商'"
                       :head="false">
            </info-line>
            <info-line :id="'sys_cron_purchase'"
                       :status.sync="sys.cron_purchase"
                       :smsg="'订单同步配置正确'"
                       :emsg="'订单同步配置错误，请联系厂商'"
                       :head="false">
            </info-line>

          </div>
        </div>
        <div class="col-md-6">
          <div class="ys-box-title ys-box-title-s">中心配置<span class="ys-info-color m-l-5">(可选)</span></div>
          <div class="ys-box-con bor-blue-dashed">
            <info-line :id="'sys_b_env'"
                       :status.sync="sys_b.env"
                       :required="false"
                       :name="'运行环境'"
                       :smsg="'运行环境配置正确'"
                       :emsg="'调试信息已打开/二次验证标题未配置，请联系厂商'"
                       >
            </info-line>
            <info-line :id="'sys_b_sso'"
                       :status.sync="sys_b.sso"
                       :required="false"
                       :name="'单点登录(SSO)'"
                       :smsg="'单点登录配置正确'"
                       :emsg="'单点登录未配置，请联系厂商'"
                       >
            </info-line>
            <info-line :id="'sys_b_menu'"
                       :status.sync="sys_b.menu"
                       :required="false"
                       :name="'自定义菜单'"
                       :smsg="'自定义菜单配置正确'"
                       :emsg="'自定义菜单未配置'"
                       :router="'menu-mgt'"
                       :retry="false"
                       >
            </info-line>
            <info-line :id="'sys_b_agent_info'"
                       :status.sync="sys_b.agent_info"
                       :required="false"
                       :name="'代理商信息'"
                       :smsg="'代理商信息已补全'"
                       :emsg="'代理商信息未补全'"
                       :router="'base-info'"
                       :retry="false"
                       >
            </info-line>
          </div>
          <div class="ys-box">
            <div class="ys-box-title ys-box-title-s">功能组件</div>
            <div class="ys-box-con bor-blue-dashed">
              <info-line :id="'soc_component_monitor'"
                       :status.sync="soc_component.monitor"
                       :name="'监控设置'"
                       :smsg="'监控服务配置正常'"
                       :emsg="'监控服务配置异常，功能模块将失效，请联系厂商'"
                       >
              </info-line>
              <info-line :id="'soc_component_hw'"
                         :status.sync="soc_component.hw"
                         :name="'高防服务'"
                         :body="false"
                         :smsg="''"
                         :emsg="''">
              </info-line>
              <info-line :id="'soc_component_hw_key'"
                         :status.sync="soc_component.hw_key"
                         :name="'高防服务'"
                         :head="false"
                         :mt="-10"
                         :smsg="'高防服务秘钥已配置'"
                         :emsg="'高防服务秘钥未配置，功能模块将失效，请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_hw_dc'"
                         :status.sync="soc_component.hw_dc"
                         :name="'高防服务'"
                         :head="false"
                         :smsg="'高防服务数据中心已配置'"
                         :emsg="'高防服务数据中心未配置，功能模块将失效，请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_cloud'"
                         :status.sync="soc_component.cloud"
                         :name="'云防御'"
                         :body="false"
                         :smsg="''"
                         :emsg="''">
              </info-line>
              <info-line :id="'soc_component_cloud_qssec'"
                         :status.sync="soc_component.cloud_qssec"
                         :head="false"
                         :mt="-10"
                         :smsg="'青松服务连接正常'"
                         :emsg="'青松服务连接异常，功能模块将失效，请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_cloud_qs_api'"
                         :status.sync="soc_component.cloud_qs_api"
                         :head="false"
                         :smsg="'API服务连接正常'"
                         :emsg="'API服务连接异常，功能模块将失效，请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_cloud_qssec'"
                         :status.sync="soc_component.cloud_qssec"
                         :name="'WAF防御'"
                         :smsg="'WAF防御服务连接正常'"
                         :emsg="'WAF防御服务连接异常，功能模块将失效，请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_scan'"
                         :status.sync="soc_component.scan"
                         :name="'漏洞扫描'"
                         :body="false"
                         :smsg="''"
                         :emsg="''">
              </info-line>
              <info-line :id="'soc_component_scan_conf'"
                         :status.sync="soc_component.scan_conf"
                         :head="false"
                         :mt="-10"
                         :smsg="'扫描器已配置'"
                         :emsg="'扫描器未配置，功能模块将失效, 请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_scan_tools'"
                         :status.sync="soc_component.scan_tools"
                         :head="false"
                         :smsg="'扫描器连接正常'"
                         :emsg="'扫描器连接失败，功能模块将失效, 请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_scan_dir'"
                         :status.sync="soc_component.scan_dir"
                         :head="false"
                         :smsg="'扫描报告目录正常'"
                         :emsg="'扫描报告目录不可写，扫描报告将无法存储, 请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_hids'"
                         :status.sync="soc_component.hids"
                         :name="'终端安全'"
                         :body="false"
                         :smsg="''"
                         :emsg="''">
              </info-line>
              <info-line :id="'soc_component_hids_conf'"
                         :status.sync="soc_component.hids_conf"
                         :head="false"
                         :mt="-10"
                         :smsg="'终端安全服务已配置'"
                         :emsg="'终端安全服务未配置，功能模块将失效, 请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_hids_tools'"
                         :status.sync="soc_component.hids_tools"
                         :head="false"
                         :smsg="'终端安全服务连接正常'"
                         :emsg="'终端安全服务连接失败，功能模块将失效, 请联系厂商'">
              </info-line>
              <info-line :id="'soc_component_hids_tools'"
                         :status.sync="soc_component.hids_tools"
                         :name="'网络安全'"
                         :smsg="'IDPS设备连接正常'"
                         :emsg="'IDPS设备连接失败，功能模块将失效, 请联系厂商'">
              </info-line>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


</template>
<style scoped>

  .ys-load-step-con {
    height: 4px;
    background: #45536e;
    width: 100%;
    position: relative;
    border-radius: 3px;
  }

  .progress-box {
    width: 50%;
    height: 4px;
    position: absolute;
    top: 0px;
    left: 0px;
    border-radius: 3px;
    background: linear-gradient(to right, #4a92ff 0%, #35d778 100%);
    transition: 1.5s width ease-in;
  }

  .progress-box-active:before {
    content: "";
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: #fff;
    border-radius: 3px;
    animation: ys-progress-active 1.5s ease-in-out infinite;
  }

  @keyframes ys-progress-active {
    0% {
      opacity: .5;
      width: 0;
    }
    100% {
      opacity: .2;
      width: 100%;
    }
  }
</style>

<script>
  import Api from 'src/lib/api'
  import infoLine from './info-line.vue'
  export default {
    name: 'system-health',
    data () {
      return {
        step: 1,
        curStep: false,
        system_status: true,
        loadMini: true,
        lastTime: '2017-08-01 10:10:10',
        sys: {
          secret_key: 'loading',
          run_user: 'loading',
          path_conf: 'loading',
          path_access: 'loading',
          db: 'loading',
          services: 'loading',
          crm: 'loading',
          crm_ms: 100,
          qs_api: 'loading',
          qs_api_ms: 100,
          qssec: 'loading',
          qssec_ms: 100,
          icp: 'loading',
          icp_ms: 100,
          date: 'loading',
          date_ms: '100',
          soc_agent:'loading',
          message: 'loading',
          pay: 'loading',
          env: 'loading',
          crontabs: 'loading',
          cron_soc_agent: 'loading',
          cron_monitor: 'loading',
          cron_asset: 'loading',
          cron_hw:'loading',
          cron_hids:'loading',
          cron_purchase: 'loading',
        },
        sys_b: {
          env: 'loading',
          sso: 'loading',
          menu: 'loading',
          agent_info: 'loading'
        },
        soc_component: {
          monitor: 'loading',
          hw: 'loading',
          hw_key: 'loading',
          hw_dc: 'loading',
          cloud: 'loading',
          cloud_crm: 'loading',
          cloud_qssec: 'loading',
          cloud_qs_api: 'loading',
          waf: 'loading',
          scan: 'loading',
          scan_conf: 'loading',
          scan_tools: 'loading',
          scan_dir: 'loading',
          hids: 'loading',
          hids_conf: 'loading',
          hids_tools: 'loading',
          nids: 'loading',
        }

      }
    },
    transitions: {
      "ysFade": {
        enterClass: 'fadeInUp',
        leaveClass: 'hide'
      }
    },
    ready: function () {
      this.fetchStatus()
    },
    events: {
      'Callretry': function (key) {
        if(key.indexOf('sys_b') > -1){
          this.fetchOne('sys_b')
        }else if(key.indexOf('sys') >-1){
          this.fetchOne('sys')
        }else {
          this.fetchOne('soc_component')
        }
      }
    },
    methods: {
      fetchOne(key){
        this.$http.get('/api/system/sys_status', {re_check: key}).then((response) => {
          this.$root.loadStatus = false
          if (response.data.status == 200) {
            if (key == 'sys') {
              this.sys = {}
              this.sys = response.data.data.sys
              this.system_status = response.data.data.system_status
            }
            if (key == 'sys_b') {
              this.sys_b = response.data.data.sys_b
            }
            if (key == 'soc_component') {
              this.sys_b = response.data.data.sys_b
              this.soc_component = response.data.data.soc_component
            }
            this.lastTime = response.data.data.last_time

           } else {
             this.$root.alertError = true;
             this.$root.errorMsg = "获取信息失败"
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      },
      fetchStatus(re_check){
        let data = {}
        if(re_check){
          data = {re_check: 'all'}
          this.step = 2
          this.curStep = 5
          this.sys = {
          secret_key: 'loading',
          run_user: 'loading',
          path_conf: 'loading',
          path_access: 'loading',
          db: 'loading',
          services: 'loading',
          crm: 'loading',
          crm_ms: 100,
          qs_api: 'loading',
          qs_api_ms: 100,
          qssec: 'loading',
          qssec_ms: 100,
          icp: 'loading',
          icp_ms: 100,
          date: 'loading',
          date_ms: '100',
          soc_agent: 'loading',
          message: 'loading',
          pay: 'loading',
          env: 'loading',
          crontabs: 'loading',
          cron_soc_agent: 'loading',
          cron_monitor: 'loading',
          cron_asset: 'loading',
          cron_hw:'loading',
          cron_hids:'loading',
          cron_purchase: 'loading',
        }
          this.sys_b = {
          env: 'loading',
          sso: 'loading',
          menu: 'loading',
          agent_info: 'loading'
        }
          this.soc_component = {
          monitor: 'loading',
          hw: 'loading',
          hw_key: 'loading',
          hw_dc: 'loading',
          cloud: 'loading',
          cloud_crm: 'loading',
          cloud_qssec: 'loading',
          cloud_qs_api: 'loading',
          waf: 'loading',
          scan: 'loading',
          scan_conf: 'loading',
          scan_tools: 'loading',
          scan_dir: 'loading',
          hids: 'loading',
          hids_conf: 'loading',
          hids_tools: 'loading',
          nids: 'loading',
        }
        }
         this.$http.get('/api/system/sys_status', data).then((response) => {
          this.$root.loadStatus = false
           if (response.data.status == 200) {
             if (response.data.data.system_status != 'loading') {
               this.sys = response.data.data.sys
               this.sys_b = response.data.data.sys_b
               this.soc_component = response.data.data.soc_component
               this.lastTime = response.data.data.last_time
               this.system_status = response.data.data.system_status
               if(re_check){
                 this.step = 2
               }
             }
             else {
               if(response.data.data.system_status==50){
                 this.sys = response.data.data.sys
               }
               if(response.data.data.system_status==70){
                 this.sys_b = response.data.data.sys_b
               }
               setTimeout(this.fetchStatus, 1000)
             }
             this.curStep = response.data.data.system_check_progress
             if (this.curStep == 100) {
               this.curStep = false
             }
           } else {
             this.$root.alertError = true;
             this.$root.errorMsg = "获取信息失败"
          }
        }, function (response) {
          Api.user.requestFalse(response, this);
        })
      }
    },
    components: {
      infoLine
    }

  }
</script>