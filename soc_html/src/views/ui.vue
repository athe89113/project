<template>
  <div>
    <div class="ys-box" v-bind:class="[showInfo ? 'ys-blur' : '']">
      <div class="ys-box-con">
        <section class="component">
          <h4>字体大小</h4>
          <p class="ys-info-color">.font36  .font30 .font26 .font24  .font22  .font20  .font18  .font16  .font14  .font12</p>
        </section>
        <section class="component m-t-20">
          <h4>间距样式</h4>
          <p class="ys-info-color">整体内边距 p-0{padding:0px;} p-10 p-15 p-20 p-30</p>
          <p class="ys-info-color m-t-10">内边距 .p-l-0 .p-l-3 .p-l-5 p-l-10 .p-l-15 .p-l-20 .p-l-25 .p-l-30</p>
          <p class="ys-info-color m-t-10">内边距 .p-r-0 .p-r-5 p-r-10 .p-r-40</p>
          <p class="ys-info-color m-t-10">内边距 .p-t-0 .p-t-5 p-t-10 .p-t-15 .p-t-20 .p-t-30 .p-t-40</p>
          <p class="ys-info-color m-t-10">内边距 .p-b-0 .p-b-10</p>

          <p class="ys-info-color m-t-20">外边距 .m-0 .m-5 .m-10 .m-20</p>
          <p class="ys-info-color m-t-10">外边距 .m-r-0 .m-r-2 .m-r-3 .m-r-5 .m-r-6 .m-r-10 .m-r-12 .m-r-15 .m-r-20 .m-r-30 .m-r-40</p>
          <p class="ys-info-color m-t-10">外边距 .m-l-3 .m-l-5 .m-l-6 .m-l-8 .m-l-10 .m-l-15 .m-l-20 .m-l-40</p>
          <p class="ys-info-color m-t-10">外边距 .m-t-0 .m-t-2 .m-t-5 .m-t-8 .m-t-10 .m-t-15 .m-t-16 .m-t-20 .m-t-30 .m-t-40 .m-t-45 .m-t-50 .m-t-60</p>
          <p class="ys-info-color m-t-10">外边距 .m-b-0 .m-b-5 .m-b-10 .m-b-15 .m-b-20 .m-b-30</p>

        </section>
        <section class="component m-t-20">
          <h4>百分比进度</h4>
          <div>
            <percent :data="90"></percent>
          </div>
          <div>
            <percent :data="90" :width="'100%'"></percent>
          </div>
          <div v-highlight class="m-t-10">
            <pre>
              <code class="html xml">
                &lt;percent
                :data="10"
                :width="180px"&gt;&lt;/percent&gt;
                默认宽度是150px,传入不同width(使用默认就不用传)
                width接受的参数 100px 120px 或者 100%
              </code>
            </pre>
          </div>
        </section>
        <section class="component">
          <h4>复选框</h4>
          <div>
            <ys-checkbox :text="'露娜'" class="m-r-10" :show.sync="checkboxStatus"></ys-checkbox>
            <ys-checkbox :text="'李白'" class="m-r-10"></ys-checkbox>
            <ys-checkbox :text="'鬼谷子'" class="m-r-10"></ys-checkbox>
            <ys-checkbox :text="'干将莫邪'"></ys-checkbox>
          </div>
          <div v-highlight class="m-t-10">
            <pre>
              <code class="html xml">
                &lt;checkbox :text="'选我选我'"
                          :show="selected"
                          :auto-set="false"
                          @ys-click="doSomething()"&gt;&lt;/checkbox&gt;

                text 复选框名称
                show 显示状态，勾选还是不勾选 true或false
                auto-set 默认是自动勾选，设置此参数需要手动配合@ys-click修改显示状态
              </code>
            </pre>
          </div>
        </section>
        <section class="component">
          <h4>单选框</h4>
          <div>
            <ys-radio :list="radioData" :value.sync="curRadio"></ys-radio>
          </div>
          <div v-highlight class="m-t-10">
            <pre>
              <code class="html xml">
                &lt;radio :list="radioData"
                       :value.sync="curRadio"&gt;&lt;/radio&gt;
                list 当前单选框列表[{id:1,name:"子小猴"},{id:2,name:"小猴子"},{id:3,name:"猴小子"}]
                value 当前选中的ID 1

              </code>
            </pre>
          </div>
        </section>
        <section class="component m-t-20">
          <h4>输入框</h4>
          <div>
            <input class="ys-input" placeholder="提示内容"/>
            <span class="ys-input-unit">
              <input class="ys-input" placeholder="请输入一定金额"/>
              <span class="unit ys-info-color">元</span>
            </span>
          </div>
          <div v-highlight class="m-t-10">
            <pre>
              <code class="html xml">
                &lt;input class="ys-input"/&gt;
                
                &lt;div class="ys-input-unit d-i-b"&gt;
                  &lt;input class="ys-input" placeholder="请输入一定金额"/&gt;
                  &lt;span class="unit ys-info-color">元&lt;/span&gt;
                &lt;/div&gt;
              </code>
            </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>一级窗口</h4>
          <div class="ys-box">
            <div class="ys-box-con">
              如果用在每个页面最顶级的话,需要给 ys-box-con增加样式 ys-wrap
            </div>
          </div>
          <h4>二级窗口</h4>
          <div class="ys-box">
            <div class="ys-box-title">标题</div>
            <div class="ys-box-con">内容区域</div>
          </div>
          <h4>三级窗口</h4>
          <div class="ys-box">
            <div class="ys-box-title ys-box-title-s"><i class="ys-icon icon-title ys-primary-color m-r-5"></i>标题</div>
            <div class="ys-box-con">内容区域</div>
          </div>
          <div class="ys-box-con bor-green-bg-solid m-t-20 arrow-left">内容区域</div>
          <div class="ys-box-con bor-blue-bg-solid m-t-20">内容区域</div>
          <div class="ys-box-con bor-red-bg-solid m-t-20">内容区域</div>
          <div class="ys-box-con bor-green-dashed m-t-20">内容区域</div>
          <div class="ys-box-con bor-blue-dashed m-t-20">内容区域</div>
          <div class="ys-box-con bor-red-dashed m-t-20">内容区域</div>
        </section>
        <section class="component m-t-30">
          <h4>图标</h4>
          <p class="icon-display">
            <span><i class="ys-icon icon-download"></i></span>
            <span><i class="ys-icon icon-upload"></i></span>
            <span><i class="ys-icon icon-play"></i></span>
            <span><i class="ys-icon icon-pause"></i></span>
            <span><i class="ys-icon icon-update"></i></span>
          </p>
          <p class="icon-display m-t-10">
            <span><i class="ys-icon icon-home-attack"></i></span>
            <span><i class="ys-icon icon-menu"></i></span>
            <span><i class="ys-icon icon-category"></i></span>
            <span><i class="ys-icon icon-home-mon"></i></span>
            <span><i class="ys-icon icon-home-order"></i></span>
            <span><i class="ys-icon icon-home-scan"></i></span>
            <span><i class="ys-icon icon-notice"></i></span>
            <span><i class="ys-icon icon-look"></i></span>
            <span><i class="ys-icon icon-menu"></i></span>
            <span><i class="ys-icon icon-edit"></i></span>
            <span><i class="ys-icon icon-trash"></i></span>
            <span><i class="ys-icon icon-check"></i></span>
            <span><i class="ys-icon icon-add-circle"></i></span>
            <span><i class="ys-icon icon-downlist"></i></span>
            <span><i class="ys-icon icon-downlist-up"></i></span>
            <span><i class="ys-icon icon-arrow-up"></i></span>
            <span><i class="ys-icon icon-arrow-down"></i></span>
            <span><i class="ys-icon icon-arrow-filter"></i></span>
            <span><i class="ys-icon icon-arrow-left"></i></span>
            <span><i class="ys-icon icon-arrow-right"></i></span>
            <span><i class="ys-icon icon-prev"></i></span>
            <span><i class="ys-icon icon-next"></i></span>
            <span><i class="ys-icon icon-map"></i></span>
            <span><i class="ys-icon icon-clear"></i></span>
            <span><i class="ys-icon icon-search"></i></span>
            <span><i class="ys-icon icon-cart"></i></span>
            <span><i class="ys-icon icon-check-circle"></i></span>
            <span><i class="ys-icon icon-clear-circle"></i></span>
            <span><i class="ys-icon icon-dollar-circle"></i></span>
            <span><i class="ys-icon icon-info"></i></span>
            <span><i class="ys-icon icon-warn-circle"></i></span>
            <span><i class="ys-icon icon-file"></i></span>
            <span><i class="ys-icon icon-lock-shield"></i></span>
            <span><i class="ys-icon icon-user"></i></span>
            <span><i class="ys-icon icon-plus-box"></i></span>
            <span><i class="ys-icon icon-minus-box"></i></span>
            <span><i class="ys-icon icon-lock"></i></span>
            <span><i class="ys-icon icon-unlock"></i></span>
            <span><i class="ys-icon icon-title"></i></span>
            <span><i class="ys-icon icon-minus-circle"></i></span>
            <span><i class="ys-icon icon-ellipsis"></i></span>
            <span><i class="ys-icon icon-warn-outline"></i></span>
          </p>
          <p class="m-t-10 icon-display">
            <span><i class="ys-icon icon-info-circle"></i></span>
            <span><i class="ys-icon icon-device-two"></i></span>
            <span><i class="ys-icon icon-help-circle"></i></span>
            <span><i class="ys-icon icon-cloud"></i></span>
            <span><i class="ys-icon icon-computer"></i></span>
            <span><i class="ys-icon icon-core"></i></span>
            <span><i class="ys-icon icon-defense"></i></span>
            <span><i class="ys-icon icon-internet"></i></span>
            <span><i class="ys-icon icon-monitor"></i></span>
            <span><i class="ys-icon icon-scan"></i></span>
            <span><i class="ys-icon icon-refresh"></i></span>
            <span><i class="ys-icon icon-transfer"></i></span>
            <span><i class="ys-icon icon-arrow-right-circle"></i></span>
            <span><i class="ys-icon icon-assets"></i></span>
            <span><i class="ys-icon icon-idc"></i></span>
            <span><i class="ys-icon icon-ip"></i></span>
            <span><i class="ys-icon icon-rack"></i></span>
            <span><i class="ys-icon icon-server"></i></span>
            <span><i class="ys-icon icon-company"></i></span>
            <span><i class="ys-icon icon-child-user"></i></span>
            <span><i class="ys-icon icon-domain"></i></span>
            <span><i class="ys-icon icon-cpu"></i></span>
            <span><i class="ys-icon icon-storage"></i></span>
            <span><i class="ys-icon icon-clock"></i></span>
            <span><i class="ys-icon icon-warning-three"></i></span>
            <span><i class="ys-icon icon-check-circle-line"></i></span>
            <span><i class="ys-icon icon-tag-new font28"></i></span>
          </p>
          <p class="m-t-10 icon-display">
            <span class="font16">图表模块图标</span>
            <span><i class="ys-icon icon-chart-bar-horizontal-sort font26"></i></span>
            <span><i class="ys-icon icon-chart-bar-horizontal font26"></i></span>
            <span><i class="ys-icon icon-chart-bar-sort font26"></i></span>
            <span><i class="ys-icon icon-chart-bar font26"></i></span>
            <span><i class="ys-icon icon-chart-line font26"></i></span>
            <span><i class="ys-icon icon-chart-num font26"></i></span>
            <span><i class="ys-icon icon-chart-pie font26"></i></span>
            <span><i class="ys-icon icon-chart-map font26"></i></span>
            <span><i class="ys-icon icon-chart-table font26"></i></span>
          </p>
          <p class="m-t-10 icon-display">
            <span class="font16">资产总览图标</span>
            <span><i class="ys-icon icon-asset-dash-idc font26"></i></span>
            <span><i class="ys-icon icon-asset-dash-rack font26"></i></span>
            <span><i class="ys-icon icon-asset-dash-unum font26"></i></span>
            <span><i class="ys-icon icon-asset-dash-ip font26"></i></span>
            <span><i class="ys-icon icon-asset-dash-device font26"></i></span>
            <span><i class="ys-icon icon-asset-dash-bw font26"></i></span>
            <span><i class="ys-icon icon-export"></i></span>
            <span><i class="ys-icon icon-import"></i></span>
          </p>
          <p class="m-t-15 m-b-10 icon-display">
            <span><i class="ys-icon icon-menu-asset"></i></span>
            <span><i class="ys-icon icon-menu-bell"></i></span>
            <span><i class="ys-icon icon-menu-cart"></i></span>
            <span><i class="ys-icon icon-menu-computer"></i></span>
            <span><i class="ys-icon icon-menu-dashboard"></i></span>
            <span><i class="ys-icon icon-menu-defense"></i></span>
            <span><i class="ys-icon icon-menu-device"></i></span>
            <span><i class="ys-icon icon-menu-domain"></i></span>
            <span><i class="ys-icon icon-menu-eye-ract"></i></span>
            <span><i class="ys-icon icon-menu-eye"></i></span>
            <span><i class="ys-icon icon-menu-file"></i></span>
            <span><i class="ys-icon icon-menu-home"></i></span>
            <span><i class="ys-icon icon-menu-info-overview"></i></span>
            <span><i class="ys-icon icon-menu-internet"></i></span>
            <span><i class="ys-icon icon-menu-jizhong"></i></span>
            <span><i class="ys-icon icon-menu-lock"></i></span>
            <span><i class="ys-icon icon-menu-log"></i></span>
            <span><i class="ys-icon icon-menu-rookit"></i></span>
            <span><i class="ys-icon icon-menu-search"></i></span>
            <span><i class="ys-icon icon-menu-service"></i></span>
            <span><i class="ys-icon icon-menu-setting"></i></span>
            <span><i class="ys-icon icon-menu-support"></i></span>
            <span><i class="ys-icon icon-menu-system"></i></span>
            <span><i class="ys-icon icon-menu-topo"></i></span>
            <span><i class="ys-icon icon-menu-upgrade"></i></span>
            <span><i class="ys-icon icon-menu-user"></i></span>
            <span><i class="ys-icon icon-menu-user-tree"></i></span>
          </p>
        </section>
        <section class="component m-t-30">
          <h4>按钮</h4>
          <p class="">
            <button class="ys-btn m-r-10">默认按钮</button>
            <button class="ys-btn ys-btn-white m-r-10">白色按钮</button>
            <button class="ys-btn ys-btn-op m-r-10">透明按钮</button>
            <button class="ys-btn ys-btn-op-white m-r-10">白色按钮</button>
            <button class="ys-btn ys-btn-blue m-r-10">蓝色按钮</button>
          </p>
          <p class="m-t-20">
            <button class="ys-btn ys-btn-m m-r-10">中号按钮</button>
            <button class="ys-btn ys-btn-m ys-btn-white m-r-10">中号按钮</button>
            <button class="ys-btn ys-btn-m ys-btn-op m-r-10">中号按钮</button>
            <button class="ys-btn ys-btn-m ys-btn-op-white m-r-10">中号按钮</button>
            <button class="ys-btn ys-btn-m ys-btn-blue m-r-10">中号按钮</button>
          </p>
          <p class="m-t-20">
            <button class="ys-btn ys-btn-s m-r-10">小号按钮</button>
            <button class="ys-btn ys-btn-s ys-btn-white m-r-10">小号按钮</button>
            <button class="ys-btn ys-btn-s ys-btn-op m-r-10">小号按钮</button>
            <button class="ys-btn ys-btn-s ys-btn-op-white m-r-10">小号按钮</button>
            <button class="ys-btn ys-btn-s ys-btn-blue m-r-10">小号按钮</button>
          </p>
        </section>
        <section class="component m-t-30">
          <h4>机柜视图</h4>
          <rack-dash :devices.sync="devices"></rack-dash>
        </section>
        <section class="component m-t-30">
          <h4>颜色(参照设计图对应颜色)</h4>
          <p class="ys-primary-color">我们挥霍的一切在最高处必将汇合 ----- ys-primary-color</p>
          <p class="ys-info-color m-t-5">我们挥霍的一切在最高处必将汇合 ----- ys-info-color</p>
          <p class="ys-success-color m-t-5">我们挥霍的一切在最高处必将汇合 ----- ys-success-color</p>
          <p class="ys-error-color m-t-5">我们挥霍的一切在最高处必将汇合 ----- ys-error-color</p>
          <p class="ys-warn-color m-t-5">我们挥霍的一切在最高处必将汇合 ----- ys-warn-color</p>

          <p class="ys-medium-color m-t-5">我们挥霍的一切在最高处必将汇合 ----- ys-medium-color</p>
          <p class="ys-serious-color m-t-5">我们挥霍的一切在最高处必将汇合 ----- ys-serious-color</p>
        </section>
        <section class="component m-t-30">
          <h4>1. select组件</h4>
          <div>
            <ys-select :option="selectData"
                       :width="150"
                       :selected.sync="curSelect"
                       :searchable="false"></ys-select>
            <ys-select :option="selectData"
                       :width="150"
                       :selected.sync="curSelect"></ys-select>
            <ys-select :option="selectData"
                       :width="150"
                       :selected.sync="curSelect"
                       :searchable="false"
                       :filter="true"></ys-select>
            <ys-select :option="ispLines"
                       :width="150"
                       :selected.sync="curIsp"
                       :searchable="false"
                       :filter="true"
                       :multiple="true"></ys-select>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-select
          :option="selectData" 列表集合[{},{}]
          :width="150"              下拉列表宽度
          :selected.sync="tableFilter.location_id" 当前选中的{id:1,name:"aaaa"}
          @change="tableRe()"  change事件&gt;&lt;/ys-select&gt;
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>标签</h4>
          <p>大号标签  <tag :text="'aaaaaa'" :size="'L'"></tag></p>
          <p class="m-t-10">小号标签  <tag :text="'aaaaaa'"></tag></p>
          <div v-highlight class="m-t-10">
            <pre>
              <code class="html xml">

                &lt;tag :text="'aaaaaa'" :size="'L'"&gt;&lt;/tag&gt;

                &lt;tag :text="'aaaaaa'"&gt;&lt;/tag&gt;
              </code>
            </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>选择组件</h4>
          <div class="pos-r">
            <ys-switch-tab class="m-r-10"
                           :checked="curSwitch"
                           :list="[{'id':'IDS',name:'IDS模式'},{'id':'IPS',name:'IPS模式'}]"
                           @click="changeSwitchTab()">
            </ys-switch-tab>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-switch-tab class="m-r-10"
          :checked="curSwitch"
          :list="[{'id':'IDS',name:'IDS模式'},{'id':'IPS',name:'IPS模式'}]"
          @click="changeSwitchTab()"&gt;
          &lt;/ys-switch-tab&gt;

          组件内不控制,全都在使用时控制显示样式,通过点击事件改变当前的值
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>开关组件</h4>
          <div class="pos-r">
            <ys-switch>
              <span slot="open">开启</span>
              <span slot="close">关闭</span>
            </ys-switch>
            <ys-switch :disabled="true">
              <span slot="open">on</span>
              <span slot="close">off</span>
            </ys-switch>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-switch :size="'large'"&gt;
          &lt;span slot="open">开启&lt;/span&gt;
          &lt;span slot="close">关闭&lt;/span&gt;
          &lt;/ys-switch&gt;

          disabled 控制可用不可用 true或false
          size     控制大小 large small 默认什么也不传,正常大小
          slot     部分控制显示提示
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>loading组件</h4>
          <div class="pos-r">
            <button class="ys-btn m-r-10" @click="showMiniLoad()">局部loading</button>
            <loading-mini :show.sync="loadMini"></loading-mini>
            <button class="ys-btn m-r-10 m-l-20" @click="showNormalLoad()">表格loading</button>
            <loading-normal :show.sync="loadNormal"></loading-normal>
            <button class="ys-btn m-r-10 m-l-20" @click="showGloabalLoad()">全局loading</button>
            <loading-global :show.sync="loadGlobal"></loading-global>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;loading-mini :show.sync="loadMini"&gt;&lt;/loading-mini&gt;

          &lt;loading-normal :show.sync="loadNormal"&gt;&lt;/loading-normal&gt;

          &lt;loading-global :show.sync="loadGlobal"&gt;&lt;/loading-global&gt;

          只有一个参数,控制显示隐藏
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>时间日期组件</h4>
          <div class="pos-r">
            <calendar :type="'datetime'"
                      :text="'日期时间组件'"></calendar>
            <calendar :type="'time'"
                      :text="'时间组件'"></calendar>
            <calendar :type="'date'"
                      :text="'日期组件'"></calendar>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;calendar :type="'datetime'"
          :text="'日期时间组件'"&gt;&lt;/calendar&gt;

          type   (类型) "datetime" "time" "date"

          text   (输入框显示字) 例:"选择开始时间","选择时间"

          width  (宽度) 定义输入框宽度

          value  (值) 当前选择的日期时间值

          range  (范围) true或false 是否选择时间段

          sep    (分隔符) "-" "/"

          一般情况只用一个value和type足以创建一个组件,其他的参数有默认值,不用传
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>aside组件(右侧滑出)</h4>
          <div>
            <button class="ys-btn m-r-20" @click="showAside=true">滑出</button>
            <button class="ys-btn ys-btn-white" @click="showAside=false">关闭</button>
            <ys-aside :show.sync="showAside"
                      :header="'标题'"
                      :width="'600px'"
                      :left="'auto'">
              <p>在这里写入你的展示内容</p>
              <p>在这里写入你的展示内容</p>
              <p>在这里写入你的展示内容</p>
              <div class="aside-foot m-t-20">
                <button class="ys-btn m-r-10" @click="showAside=false">完成</button>
                <button class="ys-btn ys-btn-white" @click="showAside=false">取消</button>
              </div>
            </ys-aside>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-aside :show.sync="showAside" showAside控制显示隐藏
          :header="'标题'"  标题
          :width="'600px'" 宽度
          :left="'auto'"&gt; 距离左边距离
          &lt;p&gt;在这里写入你的展示内容&lt;/p&gt;
          &lt;p&gt;在这里写入你的展示内容&lt;/p&gt;
          &lt;p&gt;在这里写入你的展示内容&lt;/p&gt;
          &lt;div class="aside-foot m-t-20"&gt;
          &lt;button class="ys-btn m-r-10" @click="showAside=false"&gt;完成&lt;/button&gt;
          &lt;button class="ys-btn ys-btn-white" @click="showAside=false"&gt;取消&lt;/button&gt;
          &lt;/div&gt;底部完成或者取消按钮
          &lt;/ys-aside&gt;
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>info 信息弹出组件(不是弹出)</h4>
          <p>由于这个界面是白色的过多,看起来不是特别明显</p>
          <p>注意:这个组件使用特殊,联系shaoxuu</p>
          <div>
            <button class="ys-btn m-r-20" @click="showInfo=true">滑出</button>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-info :show.sync="showInfo" showInfo控制显示隐藏
          :title="'标题'"  标题&gt;
          &lt;p&gt;在这里写入你的展示内容&lt;/p&gt;
          &lt;p&gt;在这里写入你的展示内容&lt;/p&gt;
          &lt;p&gt;在这里写入你的展示内容&lt;/p&gt;
          &lt;div class="aside-foot m-t-20"&gt;
          &lt;button class="ys-btn ys-btn-white" @click="showInfo=false"&gt;取消&lt;/button&gt;
          &lt;/div&gt;底部完成或者取消按钮
          &lt;/ys-info&gt;
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>2. modal组件 (弹出框)</h4>
          <div>
            <button @click="modalStatus=true" class="ys-btn">弹出</button>
            <ys-modal :show.sync="modalStatus" :title="'弹出框标题'">
              <div slot="content">
                <p>假如我是一只鸟,我也会用嘶哑的喉咙歌唱</p>
                <p>假如我是一只鸟,我也会用嘶哑的喉咙歌唱</p>
                <p>假如我是一只鸟,我也会用嘶哑的喉咙歌唱</p>
              </div>
              <div slot="footer">
                <button class="ys-btn" type="button">
                  <span>提交</span>
                </button>
              </div>
            </ys-modal>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-modal :show.sync="modalStatus" :title="'弹出框标题'"&gt;modalStatus默认为false,改变modalStatus 控制显示隐藏
          &lt;div slot="content"&gt;   内容部分
          &lt;p&gt;假如我是一只鸟,我也会用嘶哑的喉咙歌唱&lt;/p&gt;
          &lt;p&gt;假如我是一只鸟,我也会用嘶哑的喉咙歌唱&lt;/p&gt;
          &lt;p&gt;假如我是一只鸟,我也会用嘶哑的喉咙歌唱&lt;/p&gt;
          &lt;/div&gt;
          &lt;div slot="footer"&gt;  底部按钮
          &lt;button class="ys-btn" type="button"&gt;
          &lt;span&gt;提交&lt;/span&gt;
          &lt;/button&gt;
          &lt;/div&gt;
          &lt;/ys-modal&gt;
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>3. tooltip组件 (提示信息)</h4>
          <div>
            <ys-tooltip :placement="'left'" :content="'要显示的内容'">
              <button class="ys-btn" type="button">鼠标滑过</button>
            </ys-tooltip>
            <ys-tooltip :placement="'right'" :content="'要显示的内容'">
              <button class="ys-btn" type="button">鼠标滑过</button>
            </ys-tooltip>
            <ys-tooltip :placement="'top'" :content="'要显示的内容'">
              <button class="ys-btn" type="button">鼠标滑过</button>
            </ys-tooltip>
            <ys-tooltip :placement="'bottom'" :content="'要显示的内容'">
              <button class="ys-btn" type="button">鼠标滑过</button>
            </ys-tooltip>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-tooltip :placement="'left'" :content="'要显示的内容'"&gt;
          &lt;button class="ys-btn" type="button">鼠标滑过&lt;/button&gt;
          &lt;/ys-tooltip&gt;
          placement: left,top,right,bottom
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>4. poptip组件 (一般用于删除确认操作)</h4>
          <div>
            <ys-poptip :placement="'right'"
                       :confirm="true"
                       :title="'您确认删除这条内容吗？'">
              <button class="ys-btn" type="button">删除</button>
            </ys-poptip>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-poptip :placement="'right'" left top bottom
          :confirm="true"         是否是confirm状态
          :title="'您确认删除这条内容吗？'" 标题
          @on-ok="ok"             点击确定执行的方法
          @on-cancel="cancel"&gt; 点击取消执行的方法
          &lt;button class="ys-btn" type="button"&gt;删除&lt;/button&gt;
          &lt;/ys-poptip&gt;
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>5. transfer组件 (穿梭框)</h4>
          <div>
            <ys-transfer :data-list.sync="leftData"
                         :left="'选择防御设备'"
                         :target-list.sync="rightData"></ys-transfer>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;ys-transfer :data-list.sync="leftData"  左边的数据
          :left="'选择防御设备'" 左边的标题(右边一般为"已选")
          :target-list.sync="rightData"&gt;&lt;/ys-transfer&gt;右边的数据
          当前左右数据默认没有selected字段,取回数据后应该给每一条加上一个selected:false
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>6. 饼图</h4>
          <div>
            <pie-chart
                    :id="'oooos-percent1'"
                    :height="'240px'"
                    :name="'操作系统'"
                    :y.sync="pieData"
                    :color="1"></pie-chart>
            <pie-chart
                    :id="'oooos-percent11'"
                    :height="'240px'"
                    :name="'操作系统'"
                    :y.sync="pieData"
                    :color="2"></pie-chart>
            <pie-chart
                    :id="'oooos-percent111'"
                    :height="'240px'"
                    :name="'操作系统'"
                    :y.sync="pieData1"
                    :color="3"></pie-chart>
          </div>
          <div v-highlight class="m-t-10">
            <pre>
              <code class="html xml">
                &lt;pie-chart
                :id="'oooos-percent'" id必须写,不能重复
                :height="'240px'"  高度
                :name="'操作系统'" 名称
                :y="pieData"    数据
                :color="pieColor"&gt;&lt;/pie-chart&gt; 颜色(数组)
                数据格式必须为{name:"",value:""},如果不是,转换成正确的,前后端转都可以
              </code>
            </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>7. 折线图</h4>
          <div>
            <line-chart
                    :id="'aaaa-bbbb'"
                    :height="'240px'"
                    :name="lineData.name"
                    :x="lineData.x"
                    :color="lineData.color"
                    :series="lineData.series"
                    :unit="'percent'"
            ></line-chart>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;line-chart
          :id="'aaaa-bbbb'"
          :height="'240px'"
          :name="lineData.name"  数组,多个
          :x="lineData.x" x轴数据
          :color="lineData.color" 颜色数组,每条线的颜色
          :series="lineData.series" y轴数据,数组
          :unit="'percent'"&gt;单位换算,可能是百分比,或者流量kb,mb,gb &lt;/line-chart&gt;
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>8. 柱状图</h4>
          <div>
            <bar-chart :id="'website-response'"
                       :height="'240px'"
                       :name="'服务器'"
                       :x="barData.x"
                       :y="barData.y"
                       :color="barYellow"></bar-chart>
            <div style="width:600px;">
              <ling-bar-chart :id="'website-response-server'"
                              :height="'240px'"
                              :name="'服务器'"
                              :x="barData1.x"
                              :y="barData1.y"
                              :unit="'次'"></ling-bar-chart>
            </div>
          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;bar-chart :id="'website-response'"
          :height="'240px'"
          :name="'服务器'"
          :x="barData.x" x轴数据
          :y="barData.y" y轴数据
          :color="barYellow"&gt;颜色配比,数组&lt;/bar-chart&gt;
        </code>
      </pre>
          </div>
        </section>
        <section class="component m-t-30">
          <h4>9. icon组件</h4>
          <div>
            <icon :name="'computer'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'rack'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'defense'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'asset-mgt'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'use-capacity'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'band-width'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'ip-all'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'server-mon'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'website-mon'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'cover-mon'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>
            <icon :name="'web-error-mon'" :width="'41px'" :height="'32px'" :color="'#60bfa5'"></icon>

          </div>
          <div v-highlight class="m-t-10">
      <pre>
        <code class="html xml">
          &lt;icon :name="'web-error-mon'" 指定icon名字
          :width="'41px'" 宽
          :height="'32px'" 高
          :color="'#60bfa5'"&gt;填充颜色&lt;/icon&gt;
        </code>
      </pre>
          </div>
        </section>
      </div>
    </div>
    <ys-info :show.sync="showInfo" :title="'这里是标题'">
      <div slot="content">
        <p>在这里写入你的展示内容</p>
        <p>在这里写入你的展示内容</p>
        <p>在这里写入你的展示内容</p>
      </div>
      <div slot="footer">
        <button class="ys-btn" @click="showInfo=false">关闭</button>
      </div>
    </ys-info>
  </div>
</template>
<style scoped>
  .icon-display span{
    margin-right:6px;
  }
</style>
<script>
  import Api from 'src/lib/api'
  import ysSelect from 'src/components/select.vue'
  import ysModal from 'src/components/modal.vue'
  import ysTooltip from 'src/components/tooltip.vue'
  import ysPoptip from 'src/components/poptip.vue'
  import ysTransfer from 'src/components/transfer.vue'
  import pieChart from 'src/components/pie-chart.vue'
  import lineChart from 'src/components/line-chart.vue'
  import barChart from 'src/components/bar-chart.vue'
  import icon from 'src/components/icon.vue'
  import rackDash from 'src/components/rack-dash.vue'
  import ysAside from 'src/components/Aside.vue'
  import ysInfo from 'src/components/info.vue'
  import ysSwitch from 'src/components/switch.vue'
  import ysSwitchTab from 'src/components/switch-tab.vue'
  import calendar from 'src/components/calendar.vue'
  import loadingNormal from 'src/components/loading-normal.vue'
  import loadingGlobal from 'src/components/loading-global.vue'
  import ysCheckbox from 'src/components/checkbox.vue'
  import ysRadio from 'src/components/radio.vue'
  export default {
    name: "UI",
    data() {
      return {
        checkboxStatus:true,
        selectData:[{id:1,name:"选择的内容"},{id:2,name:"选择的内容选择的内容选择的内容"},{id:3,name:"选择的内容选择的内容"}],
        curSelect:{id:1,name:"选择的内容"},
        modalStatus:false,
        leftData:[{id:0,name:"1111",selected:false},{id:1,name:"1111",selected:false}],
        rightData:[{id:3,name:"1111",selected:false},],
        pieColor:['#f1eb37','#f2607f','#3ab4cb','#f87461','#e7e4f1'],
        pieData:[],
        pieData1:[],
        lineData:{
          name:["故障率1","故障率2"],
          x:[],
          color:['#00bd85',"#ff0000"],
          series:[
            {data:[]},
            {data:[]}
          ]
        },
        barData:{x:[],y:[]},
        barData1:{x:[],y:[]},
        lineBarChartData:[],
        barYellow:['#f1eb37','#cee052','#aad56d','#79c692','#60bfa5'],

        showAside:false,
        showInfo:false,

        startCalendar: {
          type: "datetime",
          value: "",
          begin: "",
          end: "",
          sep: "/",
          range: true
        },
        loadMini:false,
        loadNormal:false,
        loadGlobal:false,
        curSwitch:"IDS",
        showSwitchTab:false,

        devices:[],
        ispLines: [
          {id: 1, name: "中国电信"},
          {id: 2, name: "中国联通"},
          {id: 3, name: "中国移动"},
          {id: 4, name: "中国移动"},
          {id: 5, name: "中国移动"},
          {id: 6, name: "中国移动"},
        ],
        curIsp:[],
        radioData:[
          {id:1,text:"猴子"},
          {id:2,text:"猿猴"},
          {id:3,text:"大猩猩"},
          {id:4,text:"milo"},
        ],
        curRadio:1
      }
    },
    ready: function() {
      this.lineData.x=["11:22","22:11","22:12","22:13","22:14"];
      this.lineData.series[0].data=["11","22","33","8","15"];
      this.lineData.series[1].data=["5","16","33","8","15"];
      this.barData={
        y:[270,302,23,130,67],
        x:["aa.com","bb.com","cc","dd","ee"]
      }
      this.barData1={
        x:[270000,302,20003,130,2700],
        y:["aa.com","bb.com","cc","dd","ee"]
      }
      this.pieData1=[
        {name:"严重",value:"111"},{name:"高",value:"60"},{name:"中",value:"80"}
      ]
      this.getRackView()
    },
    methods:{
      showMiniLoad(){
        this.loadMini=true;
      },
      showNormalLoad(){
        this.loadNormal=true;
      },
      showGloabalLoad(){
        this.loadGlobal=true;
        let self=this;
        setTimeout(function(){
          self.loadGlobal=false;
        },2000)
      },
      changeSwitchTab(){
        if(this.curSwitch=="IDS"){
          this.curSwitch="IPS"
        }else{
          this.curSwitch="IDS"
        }
      },
      getRackView(){
        this.$http.get('/api/rack_view/2223').then(function (response) {
          if(response.data.status == 200){
            this.devices = response.data.data.devices
          }
        },function(response){
          Api.user.requestFalse(response,this);
        })
      },//获取具体机柜信息
    },
    components: {
      rackDash,
      ysSelect,
      ysModal,
      ysTooltip,
      ysPoptip,
      ysTransfer,
      pieChart,
      lineChart,
      barChart,
      icon,
      ysAside,
      ysInfo,
      calendar,
      loadingNormal,
      loadingGlobal,
      ysSwitch,
      ysSwitchTab,
      ysCheckbox,
      ysRadio
    }
  }
</script>
