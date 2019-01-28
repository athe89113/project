<template>
    <div class="ys-con pos-r">
        <div class="ys-box-con">
            <div class="clearfix">
                <span class="ys-info-color m-r-5 verticalM">关键词搜索：</span>
                <input class="ys-input m-r-5" placeholder="输入关键词" v-model="keyword"/>
                <tooltip id="search-tip" :delay="400" :placement="'bottom'" :visible.sync="true">
                    <div slot="content">
                        <div style="width:240px;overflow:hidden;padding: 10px 0px 10px 10px">
                            <p>可根据以下关键词搜索：</p>
                            <p>阻断原因，文件名 ，终端所在组名称</p>
                            <p>病毒名称，sql语句， 事件名称</p>
                        </div>
                    </div>
                    <span>
                        <i style="margin-top: 2px;margin-right: 5px;"
                           class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                      </span>
                </tooltip>
                <span class="ys-info-color m-r-5 verticalM">IP：</span>
                <input class="ys-input m-r-5" placeholder="输入IP" v-model="src_ip"/>
                <tooltip id="tip" :delay="400" :placement="'bottom'" :visible.sync="true">
                    <div slot="content">
                        <div style="width:240px;overflow:hidden;padding: 10px 0px 10px 10px">
                            <p>所有IP类字段均可搜索</p>
                        </div>
                    </div>
                    <span>
                            <i style="margin-top: 2px;margin-right: 5px;"
                               class="ys-icon icon-help-circle ys-color-warn text-cursor"></i>
                          </span>
                </tooltip>
                <span class="ys-info-color m-r-5 verticalM">时间范围：</span>
                <calendar :type="'datetime'"
                          :value.sync="startTime"
                          :text="'选择起始时间'"></calendar>
                <span class="m-l-5 m-r-5">~</span>
                <calendar :type="'datetime'"
                          :value.sync="endTime"
                          :text="'选择终止时间'"></calendar>
                <span class="m-r-5"> </span>
                <ys-select :option="dateRangeList" :selected.sync="curDateRange"></ys-select>
                <a class="fRight" style="margin-top: 6px" @click="showEventSourceData = true"><i
                        class="ys-icon icon-setting m-r-5"></i>设置日志源标签页</a>
            </div>
        </div>
        <!--<div class="m-t-10">-->
        <!--<div class="ys-box-con box-title">-->
        <!--<div class="clearfix">-->
        <!--<span class="ys-info-color fLeft" style="padding-top:4px;">日志源标签页：</span>-->

        <!--</div>-->
        <!--</div>-->
        <!--</div>-->
        <div class="m-t-10">
            <p class="split-line">
                <button class="ys-btn" @click="goSearch_wrap()"><i class="ys-icon icon-search"></i>查询</button>
            </p>
            <div>
                <div class="eventSourceTabs">
                    <ul class="ys-nav">
                        <li v-for="list in eventSourceTabData" @click="clickType(list, $index)">
                            <a :class="{'on': list.active}" style="width: 160px;">
                                <span class="ys-nav-cor"></span>
                                <span class="text" v-text="list.name">{{list.name}}</span>
                                <span class="text">({{list.all_count}})</span>
                            </a>
                        </li>
                        <div class="clearfix"></div>
                    </ul>
                </div>
                <div class="bottom-module ys-box-con">
                    <div class="m-b-10">
                        <div class="ys-box-con box-title">
                            <div class="clearfix">
                                <span class="ys-info-color fLeft m-r-10" style="padding-top:4px;">高级查询及图表分析</span>
                                <a class="fLeft" style="padding-top:4px;" @click='lineShow = !lineShow'><i
                                        class="ys-icon m-r-3"
                                        v-bind:class="[lineShow ? 'icon-downlist-up' : 'icon-downlist' ]"></i>
                                    <span v-if="!lineShow">展开</span>
                                    <span v-if="lineShow">收起</span>
                                </a>
                                <div class="clearfix fRight">
                                    <span class="ys-info-color fLeft" style="padding-top:4px;"></span>
                                    <a class="fRight" style="padding-top:4px;" @click='fieldShow = !fieldShow'><i
                                            class="ys-icon icon-setting m-r-5"></i>列表字段设置
                                    </a>
                                </div>
                            </div>
                        </div>
                        <div class="ys-box-con" v-if="lineShow">
                            <div class="ys-box-con">
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
                                                <span class="verticalM"
                                                    v-if="single.field.id=='result'">[ {{single.value | resultNFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='proto'">[ {{single.value | protoFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='is_normal'">[ {{single.value | isNormalFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='is_success'">[ {{single.value | isSuccessFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='act_type'">[ {{single.value | actTypeFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='log_type'">[ {{single.value | logTypeFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='login_type'">[ {{single.value | loginTypeFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='login_result'">[ {{single.value | loginResultFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='request_type'">[ {{single.value | RequestTypeFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='virustype'">[ {{single.value | viruStypeFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='infectedfileinfo_cleared'">[ {{single.value | infectedFileInfoClearedFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='infectedfileinfo_custommediatype'">[ {{single.value | infectedFileInfoCustommediaTypeFil}} ]</span>
                                                <span class="verticalM"
                                                    v-if="single.field.id=='block '">[ {{single.value | blockFil}} ]</span>
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
                                    <ys-select :option="levelData" :selected.sync="curLevel"
                                               v-if="addCondition.field.id=='level'"></ys-select>
                                    <ys-select :option="resultDataN" :selected.sync="curResultN"
                                               v-if="addCondition.field.id=='result'"></ys-select>
                                    <ys-select :option="protoData" :selected.sync="curProto"
                                               v-if="addCondition.field.id=='proto'"></ys-select>
                                    <ys-select :option="isNormalData" :selected.sync="curIsNormal"
                                               v-if="addCondition.field.id=='is_normal'"></ys-select>
                                    <ys-select :option="isSuccessData" :selected.sync="curIsSuccess"
                                               v-if="addCondition.field.id=='is_success'"></ys-select>
                                    <ys-select :option="actTypeData" :selected.sync="curActType"
                                               v-if="addCondition.field.id=='act_type'"></ys-select>
                                    <ys-select :option="logTypeData" :selected.sync="curLogType"
                                               v-if="addCondition.field.id=='log_type'"></ys-select>
                                    <ys-select :option="loginTypeData" :selected.sync="curLoginType"
                                               v-if="addCondition.field.id=='login_type'"></ys-select>
                                    <ys-select :option="loginResultData" :selected.sync="curLoginResult"
                                               v-if="addCondition.field.id=='login_result'"></ys-select>
                                    <ys-select :option="RequestTypeData" :selected.sync="curRequestType"
                                               v-if="addCondition.field.id=='request_type'"></ys-select>
                                    <ys-select :option="viruStypeData" :selected.sync="curViruStype"
                                               v-if="addCondition.field.id=='virustype'"></ys-select>
                                     <ys-select :option="infectedFileInfoClearedData" :selected.sync="curInfectedFileInfoCleared"
                                               v-if="addCondition.field.id=='infectedfileinfo_cleared'"></ys-select>
                                    <ys-select :option="infectedFileInfoCustommediaTypeData" :selected.sync="curInfectedFileInfoCustommediaType"
                                               v-if="addCondition.field.id=='infectedfileinfo_custommediatype'"></ys-select>
                                    <ys-select :option="blockData" :selected.sync="curBlock"
                                               v-if="addCondition.field.id=='block'"></ys-select>
                                    <input class="ys-input" v-model="addCondition.value"
                                           v-if="addCondition.field.id!='block'&&addCondition.field.id!='infectedfileinfo_custommediatype'&&addCondition.field.id!='infectedfileinfo_cleared'&&addCondition.field.id!='virustype'&&addCondition.field.id!='request_type'&&addCondition.field.id!='login_result'&&addCondition.field.id!='login_type'&&addCondition.field.id!='log_type'&&addCondition.field.id!='act_type'&&addCondition.field.id!='is_success'&&addCondition.field.id!='is_normal'&&addCondition.field.id!='proto'&&addCondition.field.id!='result'&&addCondition.field.id!='level'">
                                    <button class="ys-btn ys-btn-s ys-btn-blue m-l-20" @click="addSetting()">添加条件
                                    </button>
                                </div>
                                <div class="m-t-10">
                                    <button class="ys-btn" @click="goSearchItem()"><i
                                            class="ys-icon icon-search"></i>查询
                                    </button>
                                </div>
                            </div>
                            <div class="ys-box-con m-t-10">
                                <div class="clearfix">
                                    <span class="ys-info-color fLeft" style="padding-top:8px;">横轴维度(X)：</span>
                                    <div class="d-i-b fLeft">
                                        <div class="tag-box" v-for="list in xData" track-by="$index">
                                            <div class="ys-tag" @mouseover="list.remove=true"
                                                 @mouseout="list.remove=false">
                                            <span v-if="list.order.id=='asc'"><i
                                                    class="ys-icon icon-sort-asc m-r-5"></i></span>
                                                <span v-if="list.order.id=='desc'"><i
                                                        class="ys-icon icon-sort-desc m-r-5"></i></span>
                                                <span>{{list.name}}</span>
                                                <span v-if="list.condition.name!=''">（{{list.condition.name}}）</span>
                                                <i class="ys-icon icon-arrow-down text-cursor"
                                                   @click="list.show=!list.show"
                                                   v-bind:class="[list.show ? 'arrow-rotate' : '' ]"></i>
                                                <span v-show="list.remove" class="remove text-cursor"
                                                      @click="removeXData(list,$index)"><i
                                                        class="ys-icon icon-remove"></i></span></div>
                                            <div class="tag-select-body" v-show="list.show" transition="slide">
                                                <div v-if="list.type=='date'">
                                                    <div class="tag-select-option"
                                                         v-for="option in timeDataList"
                                                         @click="selectOption(list,option)"
                                                         v-bind:class="[list.condition.id==option.id ? 'cur-select' : '' ]">
                                                        {{option.name}}
                                                    </div>
                                                </div>
                                                <div v-else>
                                                    <div class="tag-select-option"
                                                         v-for="option in sortDataList"
                                                         @click="selectSort(list,option)"
                                                         v-bind:class="[list.order.id==option.id ? 'cur-select' : '' ]">
                                                        {{option.name}}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <a class="fRight" style="padding-top:8px;" @click="showXConfig()"><i
                                            class="ys-icon icon-setting m-r-5"></i>设置维度</a>
                                </div>
                                <div class="clearfix m-t-10">
                                    <span class="ys-info-color fLeft" style="padding-top:8px;">纵轴维度(Y)：</span>
                                    <div class="d-i-b fLeft">
                                        <div class="tag-box" v-for="list in yData" track-by="$index">
                                            <div class="ys-tag" @mouseover="list.remove=true"
                                                 @mouseout="list.remove=false">
                                            <span v-if="list.order.id=='asc'"><i
                                                    class="ys-icon icon-sort-asc m-r-5"></i></span>
                                                <span v-if="list.order.id=='desc'"><i
                                                        class="ys-icon icon-sort-desc m-r-5"></i></span>
                                                <span>{{list.name}}</span>
                                                <span>（{{list.condition.name}}）</span>
                                                <i class="ys-icon icon-arrow-down text-cursor"
                                                   @click="list.show=!list.show"
                                                   v-bind:class="[list.show ? 'arrow-rotate' : '' ]"></i>
                                                <span v-show="list.remove" class="remove text-cursor"
                                                      @click="removeYData(list,$index)"><i
                                                        class="ys-icon icon-remove"></i></span></div>
                                            <div class="tag-select-body" v-show="list.show" transition="slide">
                                                <div>
                                                    <div class="tag-select-option"
                                                         v-for="option in sortDataList"
                                                         @click="selectSort(list,option)"
                                                         v-bind:class="[list.order.id==option.id ? 'cur-select' : '' ]">
                                                        {{option.name}}
                                                    </div>
                                                </div>
                                                <div>
                                                    <div class="tag-select-option"
                                                         v-for="option in countDataList"
                                                         @click="selectOption(list,option)"
                                                         v-bind:class="[list.condition.id==option.id ? 'cur-select' : '' ]">
                                                        {{option.name}}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <a class="fRight" style="padding-top:8px;" @click="showYConfig()"><i
                                            class="ys-icon icon-setting m-r-5"></i>设置数值</a>
                                </div>
                            </div>
                            <div class="ys-box-con m-t-10">
                                <div style="width:100%;height:150px;" id="event-search-chart"></div>
                            </div>
                        </div>
                    </div>
                    <div class="custom-table m-t-10">
                        <table class="ys-table">
                            <thead>
                            <tr>
                                <th></th>
                                <th v-for="head in resultHeader" track-by="$index">{{head.name}}</th>
                            </tr>
                            </thead>
                            <tbody v-for="list in tableList">
                            <tr>
                                <td class="detail">
                            <span @click="showDetail($index)">
                              <i class="ys-icon"
                                 v-bind:class="[curDetailId == $index ? 'icon-downlist-up' : 'icon-downlist' ]"></i>
                            </span>
                                </td>
                                <td v-for="item in resultHeader"
                                    class="text-over p-l-5 p-r-5"
                                    style="width:300px;" :title="tdFilterData(item, list)">{{tdFilterData(item, list)}}
                                </td>
                            </tr>
                            <tr class="detail" v-bind:class="[curDetailId == $index ? 'open' : '' ]">
                                <td :colspan="resultHeader.length+1">
                                    <div class="detail-info">
                                        <div class="p-15">
                                            <p v-for="(key, item) in list" class="m-b-10" v-show="key!='selected'">
                                                    <span style="width:120px;"
                                                          class="d-i-b ys-info-color">{{key | tableDetailFieldFil}}：</span>
                                                <span>{{tableDetailFieldFilValue(key,item)}}</span>
                                            </p>
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                        <table-data :url='tableUrl'
                                    :filter.sync="tableFilter"
                                    :data.sync="tableList"
                                    :search.sync="searchValue"
                                    :table-length="20"
                                    :edit-page="true"
                                    v-ref:table></table-data>
                    </div>
                </div>
            </div>
        </div>
    <aside :show.sync="showEventSourceData" :header="'日志源标签页设置'" :width="'600px'" :left="'auto'">
        <table class="ys-form-table">
            <tr>
                <td class="verticalT" style="padding-top:1px;">标签页：</td>
                <td>
                    <span v-for="list in eventSourceData" style="width:120px;" class="d-i-b m-b-10">
                        <checkbox :text="list.name" :read="$index == 0" :show.sync="list.selected"></checkbox>
                    </span>
                </td>
            </tr>
        </table>
        <div class="aside-foot m-t-20">
            <button class="ys-btn m-r-10" @click="saveEventSourceData()">保存</button>
            <button class="ys-btn ys-btn-white" @click="showEventSourceData=false">取消</button>
        </div>
    </aside>
    <aside :show.sync="showConfigStatus" :header="configHead" :width="'600px'" :left="'auto'">
        <table class="ys-form-table">
            <tr>
                <td style="padding-top:1px;">D日期型字段：</td>
                <td>
            <span v-for="list in coordFieldData" style="width:120px;" class="d-i-b text-over"
                  v-show="list.type=='date'">
              <checkbox :text="list.name" :title="list.name" :show.sync="list.selected"></checkbox>
            </span>
                </td>
            </tr>
            <tr>
                <td class="verticalT" style="padding-top:11px;">T文本字段：</td>
                <td>
            <span v-for="list in coordFieldData" style="width:120px;" class="d-i-b m-b-10 text-over"
                  v-show="list.type=='string'">
              <checkbox :text="list.name" :title="list.name" :show.sync="list.selected"></checkbox>
            </span>
                </td>
            </tr>
            <tr>
                <td class="verticalT" style="padding-top:11px;">#数值字段：</td>
                <td>
            <span v-for="list in coordFieldData" style="width:120px;" class="d-i-b m-b-10 text-over"
                  v-show="list.type=='int'">
              <checkbox :text="list.name" :title="list.name" :show.sync="list.selected"></checkbox>
            </span>
                </td>
            </tr>
        </table>
        <div class="aside-foot m-t-20">
            <button class="ys-btn m-r-10" @click="addXData()" v-if="configType=='X'">保存</button>
            <button class="ys-btn m-r-10" @click="addYData()" v-if="configType=='Y'">保存</button>
            <button class="ys-btn ys-btn-white" @click="showConfigStatus=false">取消</button>
        </div>
    </aside>
    <aside :show.sync="fieldShow" :header="'字段设置'" :width="'600px'" :left="'auto'">
        <div>
          <span class="d-i-b m-b-15" style="width:120px;" v-for="list in tableFieldData">
            <span v-bind:class="[list.precedence != 0 ? 'disabled' : '' ]" @click="refreshTable(list)">
              <checkbox :show.sync="list.selected"></checkbox>
            </span>
            <ys-poptip :placement="'bottom'">
              <div slot="title">快速统计</div>
              <div slot="content">
                <div style="width:185px;">
                  <div class="m-b-10" v-for="per in list.keys">
                    <p>{{per.name}}</p>
                    <percent :data="per.count" :width="'180px'"></percent>
                  </div>
                </div>
              </div>
              <span>
                <span style="width:90px;"
                      class="d-i-b verticalM m-l-5 text-over padding-right:10px;">{{list.name}}</span>
              </span>
            </ys-poptip>
          </span>
        </div>
        <button class="ys-btn ys-btn-white m-t-20" @click="fieldShow =!fieldShow">关闭</button>
    </aside>
    </div>
</template>
<style scoped>
    .slide-transition {
        display: inline-block; /* 否则 scale 动画不起作用 */
    }

    .slide-enter {
        animation: ysSlideUpIn .5s;
    }

    .slide-leave {
        animation: ysSlideUpOut .5s;
    }

    .arrow-rotate {
        transform: rotate(180deg);
    }

    .box-title {
        box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.4)
    }

    .tag-box {
        position: relative;
        display: inline-block;
        margin-right: 10px;
    }

    .tag-select-body {
        width: 100%;
        position: absolute;
        z-index: 9999;
        top: 28px;
        right: 0px;
        background: #161a2f;
        background: linear-gradient(to right, #1c1c2d 0%, #2d2831 100%);
        padding-top: 5px;
        border-top: none;
        border-radius: 3px;
        box-shadow: 2px 2px 5px 1px rgba(0, 0, 0, 0.3);
    }

    .tag-select-option {
        color: #6591d2;
        padding-left: 10px;
        height: 26px;
        line-height: 26px;
        cursor: pointer;
        overflow: hidden;
        text-align: left;
    }

    .tag-select-option:hover {
        color: #6591d2;
        background: rgba(74, 146, 255, 0.2);
    }

    .cur-select {
        color: #ffffff;
        background: #4a92ff;
    }

    .cur-select:hover {
        color: #ffffff;
        background: #4a92ff;
    }

    .ys-tag {
        position: relative;
        background: rgba(74, 146, 255, 0.4);
        background: linear-gradient(-135deg, transparent 5px, rgba(74, 146, 255, 0.4) 0);
        border-top-left-radius: 3px;
        border-bottom-right-radius: 3px;
        border-bottom-left-radius: 3px;
        height: 28px;
        padding: 0px 22px 0px 10px;
        display: inline-block;
        line-height: 28px;
        font-size: 12px;
    }

    .ys-tag:before {
        content: '';
        position: absolute;
        top: -1px;
        right: -1px;
        background: linear-gradient(to left bottom, transparent 50%, #4a92ff 0, #4a92ff) 100% 0 no-repeat;
        width: 9px;
        height: 9px;
        transform: translateY(0px) rotate(0deg);
        transform-origin: bottom right;
        border-bottom-left-radius: inherit;
        box-shadow: -.2em .2em .3em -.1em rgba(0, 0, 0, .15);
    }

    .ys-tag .remove {
        position: absolute;
        right: 0px;
        top: 0px;
        width: 12px;
        height: 12px;
        background: #e96157;
        border-top-right-radius: 3px;
        border-bottom-left-radius: 3px;
    }

    .ys-tag .remove i {
        position: absolute
    }

    .split-line {
        padding-bottom: 15px;
        padding-top: 5px;
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

    .bottom-module {
        background-color: rgba(30, 36, 53, 0.25);
    }

    .everyPage {
        position: absolute;
        left: 0px;
        bottom: 23px;
    }

    .ys-nav li a.on:after {
        width: 140px;
    }

    .ys-table {
        table-layout: fixed;
    }

    .ys-table td {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
<script>
    import Api from '../../lib/api'

    let moment = require('moment')
    let echarts = require('echarts/lib/echarts');
    export default {
        name: "event-search",
        data() {
            return {
                tableUrl: "/api/ssa/event/search/dts",
                tableList: "",
                tableTotal: 0,
                tableFilter: {
                    data_tag: {id: ""},
                    start_time: {id: ""},
                    end_time: {id: ""},
                    query_string: {id: ""},
                    query: {id: ""},
                    src_ip: {id: ""},
                    param_name: {id: ""},
                    param_value: {id: ""},
                },
                param_name: '',
                param_value: '',
                tablePostData: {},
                searchValue: "",
                eventDetectData: {
                    name: [""],
                    x: [],
                    color: ["#00bd85", "#dabb61", "#e77d4e", "#e96157"],
                    series: [
                        {data: []}
                    ]
                },
                filterStatus: false,
                eventSourceData: [],
                curEventSource: {},
                fieldList: [],
                logicList: [
                    {id: 1, text: "且"},
                    {id: 2, text: "或"},
                ],
                curLogic: 1,
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
                keyword: "",
                src_ip: '',

                _ip: '',
                _data_tag: '',
                _startTime: '',
                _endTime: '',
                _keyword: '',

                resultData: [],
                resultHeader: [],
                startTime: "",
                endTime: "",
                levelData: [],
                curLevel: {},
                resultDataN: [],
                curResultN: {},
                protoData: [],
                curProto: {},
                isNormalData: [],
                curIsNormal: {},
                isSuccessData: [],
                curIsSuccess: {},
                actTypeData: [],
                curActType: {},
                logTypeData: [],
                curLogType: {},
                loginTypeData: [],
                curLoginType: {},
                loginResultData: [],
                curLoginResult: {},
                RequestTypeData: [],
                curRequestType: {},
                viruStypeData: [],
                curViruStype: {},
                infectedFileInfoClearedData: [],
                curInfectedFileInfoCleared: {},
                infectedFileInfoCustommediaTypeData: [],
                curInfectedFileInfoCustommediaType: {},
                blockData: [],
                curBlock: {},
                fieldMapData: {},
                curDetailId: "-1",
                tableFieldData: [{keys: []}],
                lineShow: false,
                fieldShow: false,
                timeDataList: [
                    {id: "month", name: "按月"},
                    {id: "week", name: "按周"},
                    {id: "day", name: "按日"},
                    {id: "hour", name: "按时"},
                    {id: "minute", name: "按分"},
                    {id: "second", name: "按秒"}
                ],
                sortDataList: [
                    {id: "default", name: "默认排序"},
                    {id: "asc", name: "升序"},
                    {id: "desc", name: "降序"}
                ],
                countDataList: [
                    {id: "SUM", name: "求和"},
                    {id: "AVG", name: "平均值"},
                    {id: "MAX", name: "最大值"},
                    {id: "MIN", name: "最小值"},
                    {id: "COUNT", name: "计数"},
                    {id: "DISTINCT", name: "去重计数"}
                ],
                showConfigStatus: false,
                configHead: "",
                configType: "X",
                coordFieldData: [{selected: false}],
                xData: [],
                yData: [],
                tempCoordFieldData: [],

                dateRangeList: [
                    {id: 0, name: "最近一小时"},
                    {id: 1, name: "最近一天"},
                    {id: 3, name: "最近三天"},
                    {id: 7, name: "最近一周"},
                    {id: 30, name: "最近一个月"}
                ],
                curDateRange: {id: 0, name: "最近一小时"},
                barData1: {x: [], y: []},
                showEventSourceData: false,
                eventSourceTabData: []
            }
        },
        ready() {
            this.barData1 = {
                x: [270000, 302, 20003, 130, 2700],
                y: ["aa.com", "bb.com", "cc", "dd", "ee"]
            }
            if (this.$route.query.start_time || this.$route.query.end_time) {
                this.endTime = this.$route.query.end_time;
                this.startTime = this.$route.query.start_time;
            } else {
                this.endTime = moment().format('YYYY-MM-DD HH:mm:ss');
                this.startTime = moment().add(-60, 'minutes').format('YYYY-MM-DD HH:mm:ss')
            }
            this.getEventSourceData();
        },
        filters: {
            levelFil: function (id) {
                for (let x in this.levelData) {
                    if (id == this.levelData[x].id) {
                        return this.levelData[x].name
                    }
                }
            },
            resultNFil: function (id) {
                for (let x in this.resultDataN) {
                    if (id == this.resultDataN[x].id) {
                        return this.resultDataN[x].name
                    }
                }
            },
            protoFil: function (id) {
                for (let x in this.protoData) {
                    if (id == this.protoData[x].id) {
                        return this.protoData[x].name
                    }
                }
            },
            isNormalFil: function (id) {
                for (let x in this.isNormalData) {
                    if (id == this.isNormalData[x].id) {
                        return this.isNormalData[x].name
                    }
                }
            },
            isSuccessFil: function (id) {
                for (let x in this.isSuccessData) {
                    if (id == this.isSuccessData[x].id) {
                        return this.isSuccessData[x].name
                    }
                }
            },
            actTypeFil: function (id) {
                for (let x in this.actTypeData) {
                    if (id == this.actTypeData[x].id) {
                        return this.actTypeData[x].name
                    }
                }
            },
            logTypeFil: function (id) {
                for (let x in this.logTypeData) {
                    if (id == this.logTypeData[x].id) {
                        return this.logTypeData[x].name
                    }
                }
            },
            loginTypeFil: function (id) {
                for (let x in this.loginTypeData) {
                    if (id == this.loginTypeData[x].id) {
                        return this.loginTypeData[x].name
                    }
                }
            },
            loginResultFil: function (id) {
                for (let x in this.loginResultData) {
                    if (id == this.loginResultData[x].id) {
                        return this.loginResultData[x].name
                    }
                }
            },
            RequestTypeFil: function (id) {
                for (let x in this.RequestTypeData) {
                    if (id == this.RequestTypeData[x].id) {
                        return this.RequestTypeData[x].name
                    }
                }
            },
             viruStypeFil: function (id) {
                for (let x in this.viruStypeData) {
                    if (id == this.viruStypeData[x].id) {
                        return this.viruStypeData[x].name
                    }
                }
            },
             infectedFileInfoClearedFil: function (id) {
                for (let x in this.infectedFileInfoClearedData) {
                    if (id == this.infectedFileInfoClearedData[x].id) {
                        return this.infectedFileInfoClearedData[x].name
                    }
                }
            },
             infectedFileInfoCustommediaTypeFil: function (id) {
                for (let x in this.infectedFileInfoCustommediaTypeData) {
                    if (id == this.infectedFileInfoCustommediaTypeData[x].id) {
                        return this.infectedFileInfoCustommediaTypeData[x].name
                    }
                }
            },
             blockFil: function (id) {
                for (let x in this.blockData) {
                    if (id == this.blockData[x].id) {
                        return this.blockData[x].name
                    }
                }
            },
            tableDetailFieldFil: function (field) {
                for (let x in this.tableFieldData) {
                    if (this.tableFieldData[x].id == field) {
                        return this.tableFieldData[x].name;
                    }
                }
            },
        },
        methods: {
            tableDetailFieldFilValue: function (field,item) {
                for (let x in this.tableFieldData) {
                    if (this.tableFieldData[x].id == field) {
                        if(this.tableFieldData[x].name && this.tableFieldData[x].name.indexOf('流量') != -1||this.tableFieldData[x].name && this.tableFieldData[x].name.indexOf('文件大小') != -1){
                            return this.changeUnit(item)
                        }else{
                            return item;
                        }
                    }
                }
            },
            removeXData(list, index) {
                this.xData.splice(index, 1);
            },
            removeYData(list, index) {
                this.yData.splice(index, 1);
            },
            selectOption(list, option) {
                list.condition = option;
                list.show = false;
                this.getChartData()
            },
            selectSort(list, option) {
                list.order = option;
                list.show = false;
                this.getChartData()
            },
            showXConfig() {
                this.$http.post('/api/ssa/event/select/list', {tag: this.curEventSource.id}).then(function (response) {
                    let coordFieldData = Object.assign({}, response.data.items);
                    for (let x in coordFieldData) {
                        coordFieldData[x].selected = false;
                    }
                    this.$set("coordFieldData", coordFieldData);
                    this.showConfigStatus = true;
                    this.configHead = "选择横轴维度";
                    this.configType = "X";
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            showYConfig() {
                this.$http.post('/api/ssa/event/select/list', {tag: this.curEventSource.id}).then(function (response) {
                    let coordFieldData = Object.assign({}, response.data.items);
                    for (let x in coordFieldData) {
                        coordFieldData[x].selected = false;
                    }
                    this.$set("coordFieldData", coordFieldData);
                    this.showConfigStatus = true;
                    this.configHead = "选择纵轴维度";
                    this.configType = "Y";
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            saveEventSourceData() {
                this.eventSourceTabData = [];
                for (let key in this.eventSourceData) {
                    if (this.eventSourceData[key].selected) {
                        let obj = Object.assign({}, this.eventSourceData[key]);
                        Vue.set(obj, 'active', false);
                        this.eventSourceTabData.push(obj);
                    }
                }
                this.showEventSourceData = false;
                this.eventSourceTabData[0].active = true;
                this.curEventSource = this.eventSourceTabData[0];
            },
            addXData() {
                for (let key in this.coordFieldData) {
                    if (this.coordFieldData[key].selected) {
                        if (this.coordFieldData[key].type == 'date') {
                            this.xData.push(this.coordFieldData[key]);
                            Vue.set(this.xData[this.xData.length - 1], 'order', {id: "default", name: "默认排序"})
                            Vue.set(this.xData[this.xData.length - 1], 'condition', {id: "day", name: "按日"})
                            Vue.set(this.xData[this.xData.length - 1], 'show', false);
                            Vue.set(this.xData[this.xData.length - 1], 'remove', false);
                        } else {
                            this.xData.push(this.coordFieldData[key]);
                            Vue.set(this.xData[this.xData.length - 1], 'condition', {id: "", name: ""})
                            Vue.set(this.xData[this.xData.length - 1], 'order', {id: "default", name: "默认排序"})
                            Vue.set(this.xData[this.xData.length - 1], 'show', false)
                            Vue.set(this.xData[this.xData.length - 1], 'remove', false)
                        }
                    }
                }
                this.showConfigStatus = false;
            },
            addYData() {
                for (let key in this.coordFieldData) {
                    if (this.coordFieldData[key].selected) {
                        this.yData.push(this.coordFieldData[key]);
                        Vue.set(this.yData[this.yData.length - 1], 'condition', {id: "SUM", name: "求和"})
                        Vue.set(this.yData[this.yData.length - 1], 'order', {id: "default", name: "默认排序"})
                        Vue.set(this.yData[this.yData.length - 1], 'show', false)
                        Vue.set(this.yData[this.yData.length - 1], 'remove', false)
                    }
                }
                this.showConfigStatus = false;
            },
            //初始化获取标签页、并展示第一个标签页
            getEventSourceData() {
                let data = {
                    start_time: this.startTime,
                    end_time: this.endTime,
                    query_string: this.keyword,
                    src_ip: this.src_ip,
                };
                this.$http.post('/api/ssa/event/tags/list', data).then(function (response) {
                    this.eventSourceData = response.data.items;
                    for (let i in response.data.items) {
                        Vue.set(this.eventSourceData[i], 'selected', true);
                        this.eventSourceTabData.push(this.eventSourceData[i]);
                    }
                    Vue.set(this.eventSourceTabData[0], 'active', true);
                    this.curEventSource = this.eventSourceData[0];
                    this.getFieldMapData();
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            //查询标签页最新数据
            getTabData() {
                this.conditionList = [].concat([]);
                let data = {
                    start_time: this.startTime,
                    end_time: this.endTime,
                    query_string: this.keyword,
                    src_ip: this.src_ip,
                };
                this.$http.post('/api/ssa/event/tags/list', data).then(function (response) {
                    for (let i = 0; i < response.data.items.length; i++) {
                        for (let x = 0; x < this.eventSourceData.length; x++) {
                            if (response.data.items[i].id == this.eventSourceData[x].id) {
                                Vue.set(this.eventSourceData[x], 'all_count', response.data.items[i].all_count);
                            }
                        }
                        ;
                        for (let x = 0; x < this.eventSourceTabData.length; x++) {
                            if (response.data.items[i].id == this.eventSourceTabData[x].id) {
                                Vue.set(this.eventSourceTabData[x], 'all_count', response.data.items[i].all_count);
                            }
                        }
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getFieldData() {
                this.$http.post('/api/ssa/event/select/list', {tag: this.curEventSource.id}).then(function (response) {
                    try {
                        this.tableFieldData = JSON.parse(JSON.stringify(response.data.items))
                        this.tempCoordFieldData = JSON.parse(JSON.stringify(response.data.items))
                        let coordFieldData = JSON.parse(JSON.stringify(response.data.items))
                        for (let x in this.tableFieldData) {
                            if (this.tableFieldData[x].precedence != 0) {
                                this.tableFieldData[x].selected = true;
                            }
                        }
                        for (let x in coordFieldData) {
                            coordFieldData[x].selected = false;
                        }
                        this.$set("coordFieldData", coordFieldData);
                        this.refreshTable();
                        this.getFieldPercentData();
                    } catch (e) {

                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getComData() {
                this.$http.post('/api/ssa/event/select/list', {tag: this.curEventSource.id}).then(function (response) {
                    try {
                        this.fieldList = [];
                        for (let key in response.data.items) {
                            let item = response.data.items[key].name;
                            if (item.indexOf('时间') > -1) {
                                continue;
                            } else {
                                this.fieldList.push(response.data.items[key]);
                            }
                        }
                        //this.fieldList = response.data.items;
                        this.addCondition.field = this.fieldList[0];
                    } catch (e) {

                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getFieldMapData() {
                let data = {
                    data_tag_id: this.curEventSource.id
                }
                this.$http.get('/api/ssa/field_map', data).then(function (response) {
                    this.fieldMapData = response.data.data;
                    if (this.fieldMapData.level) {
                        this.levelData = this.fieldMapData.level.items;
                        this.curLevel = this.levelData[0];
                    }
                    if (this.fieldMapData.result) {
                        this.resultDataN = this.fieldMapData.result.items;
                        this.curResultN = this.resultDataN[0];
                    }
                    if (this.fieldMapData.proto) {
                        this.protoData = this.fieldMapData.proto.items;
                        this.curProto = this.protoData[0];
                    }
                    if (this.fieldMapData.is_normal) {
                        this.isNormalData = this.fieldMapData.is_normal.items;
                        this.curIsNormal = this.isNormalData[0];
                    }
                    if (this.fieldMapData.is_success) {
                        this.isSuccessData = this.fieldMapData.is_success.items;
                        this.curIsSuccess = this.isSuccessData[0];
                    }
                    if (this.fieldMapData.act_type) {
                        this.actTypeData = this.fieldMapData.act_type.items;
                        this.curActType = this.actTypeData[0];
                    }
                    if (this.fieldMapData.log_type) {
                        this.logTypeData = this.fieldMapData.log_type.items;
                        this.curLogType = this.logTypeData[0];
                    }
                    if (this.fieldMapData.login_type) {
                        this.loginTypeData = this.fieldMapData.login_type.items;
                        this.curLoginType = this.loginTypeData[0];
                    }
                    if (this.fieldMapData.login_result) {
                        this.loginResultData = this.fieldMapData.login_result.items;
                        this.curLoginResult = this.loginResultData[0];
                    }
                    if (this.fieldMapData.request_type) {
                        this.RequestTypeData = this.fieldMapData.request_type.items;
                        this.curRequestType = this.RequestTypeData[0];
                    }
                     if (this.fieldMapData.virustype) {
                        this.viruStypeData = this.fieldMapData.virustype.items;
                        this.curViruStype = this.viruStypeData[0];
                    }
                     if (this.fieldMapData.infectedfileinfo_cleared) {
                        this.infectedFileInfoClearedData = this.fieldMapData.infectedfileinfo_cleared.items;
                        this.curInfectedFileInfoCleared = this.infectedFileInfoClearedData[0];
                    }
                     if (this.fieldMapData.infectedfileinfo_custommediatype) {
                        this.infectedFileInfoCustommediaTypeData = this.fieldMapData.infectedfileinfo_custommediatype.items;
                        this.curInfectedFileInfoCustommediaType = this.infectedFileInfoCustommediaTypeData[0];
                    }
                     if (this.fieldMapData.block) {
                        this.blockData = this.fieldMapData.block.items;
                        this.curBlock = this.blockData[0];
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getFieldPercentData() {
                let data = {
                    data_tag: this.curEventSource.id,
                    start_time: this.startTime,
                    end_time: this.endTime,
                    src_ip: this.src_ip,
                    query_string: this.keyword,
                    query: []
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
                this.$http.post('/api/ssa/event/search/value_percent', data).then(function (response) {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        let fieldData = response.data.data;
                        for (let x in this.tableFieldData) {
                            for (let y in fieldData) {
                                if (this.tableFieldData[x].id == y) {
                                    Vue.set(this.tableFieldData[x], 'keys', fieldData[y].keys)
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
            tableRe() {
                this.tableFilter.data_tag.id = this.tablePostData.data_tag;
                this.tableFilter.start_time.id = this.tablePostData.start_time;
                this.tableFilter.end_time.id = this.tablePostData.end_time;
                this.tableFilter.query_string.id = this.tablePostData.query_string;
                this.tableFilter.query.id = this.tablePostData.query;
                this.tableFilter.src_ip.id = this.tablePostData.src_ip;
                this.tableFilter.param_value.id = this.tablePostData.param_value;
                this.tableFilter.param_name.id = this.tablePostData.param_name;
                this.$refs.table.Re();
            },
            addSetting() {
                if (!this.addCondition.value && this.addCondition.field.id != "level" && this.addCondition.field.id != "block" && this.addCondition.field.id != "infectedfileinfo_custommediatype" && this.addCondition.field.id != "infectedfileinfo_cleared" && this.addCondition.field.id != "virustype" && this.addCondition.field.id != "request_type" && this.addCondition.field.id != "login_result" && this.addCondition.field.id != "login_type" && this.addCondition.field.id != "log_type" && this.addCondition.field.id != "act_type" && this.addCondition.field.id != "is_success" && this.addCondition.field.id != "is_normal" && this.addCondition.field.id != "proto" && this.addCondition.field.id != "result") {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '筛选值不能为空';
                    return false;
                }
                if (this.addCondition.field.id == "level" && !this.curLevel.id) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '筛选值不能为空';
                    return false;
                }
                if (this.addCondition.field.id == "level") {
                    this.addCondition.value = this.curLevel.id;
                }
                if (this.addCondition.field.id == "result") {
                    this.addCondition.value = this.curResultN.id;
                }

                if (this.addCondition.field.id == "proto") {
                    this.addCondition.value = this.curProto.id;
                }

                if (this.addCondition.field.id == "is_normal") {
                    this.addCondition.value = this.curIsNormal.id;
                }

                if (this.addCondition.field.id == "is_success") {
                    this.addCondition.value = this.curIsSuccess.id;
                }

                if (this.addCondition.field.id == "act_type") {
                    this.addCondition.value = this.curActType.id;
                }

                if (this.addCondition.field.id == "log_type") {
                    this.addCondition.value = this.curLogType.id;
                }

                if (this.addCondition.field.id == "login_type") {
                    this.addCondition.value = this.curLoginType.id;
                }

                if (this.addCondition.field.id == "login_result") {
                    this.addCondition.value = this.curLoginResult.id;
                }

                if (this.addCondition.field.id == "request_type") {
                    this.addCondition.value = this.curRequestType.id;
                }

                if (this.addCondition.field.id == "virustype") {
                    this.addCondition.value = this.curViruStype.id;
                }

                if (this.addCondition.field.id == "infectedfileinfo_cleared") {
                    this.addCondition.value = this.curInfectedFileInfoCleared.id;
                }

                if (this.addCondition.field.id == "infectedfileinfo_custommediatype") {
                    this.addCondition.value = this.curInfectedFileInfoCustommediaType.id;
                }
                if (this.addCondition.field.id == "block") {
                    this.addCondition.value = this.curBlock.id;
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
            goSearch_wrap() {
                this.goSearch(false);
                this.getTabData();
            },
            goSearch(status) {
                if (!status) {
                    this.param_name = '';
                    this.param_value = '';
                }
                this._ip = this.src_ip;
                this._data_tag = this.curEventSource.id;
                this._startTime = this.startTime;
                this._endTime = this.endTime;
                this._keyword = this.keyword;
                let data = {
                    src_ip: this.src_ip,
                    data_tag: this.curEventSource.id,
                    start_time: this.startTime,
                    end_time: this.endTime,
                    query_string: this.keyword,
                    query: [],
                    param_value: this.param_value,
                    param_name: this.param_name
                };
                this.tablePostData = data;
                this.tableRe();
                this.getFieldPercentData();
                this.getChartData();
            },
            goSearchCondition() {
                let data = {
                    src_ip: this._ip,
                    data_tag: this._data_tag,
                    start_time: this._startTime,
                    end_time: this._endTime,
                    query_string: this._keyword,
                    query: []
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
                this.tablePostData = data;
                this.tableRe();
                this.getFieldPercentData();
                this.getChartData();
            },
            goSearchItem() {
                this.goSearchCondition();
            },
            getChartData() {
                let data = {
                    data_tag: this.curEventSource.id,
                    start_time: this.startTime,
                    end_time: this.endTime,
                    src_ip: this.src_ip,
                    query_string: this.keyword,
                    query: [],
                    param_value: this.param_value,
                    param_name: this.param_name
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
                let xList = [];
                for (let x in this.xData) {
                    if (this.xData[x].type == 'date') {
                        xList.push({
                            type: "date",
                            value: this.xData[x].condition.id
                        })
                    } else {
                        xList.push({
                            type: "key",
                            value: this.xData[x].id,
                            order: this.xData[x].order.id == 'default' ? '' : this.xData[x].order.id,
                        })
                    }
                }
                let yList = [];
                for (let x in this.yData) {
                    yList.push({
                        aggregator: this.yData[x].condition.id,
                        value: this.yData[x].id,
                        order: this.yData[x].order.id == 'default' ? '' : this.yData[x].order.id
                    })
                }
                data.x = xList;
                data.y = yList;
                this.$http.post('/api/ssa/event/search/line', data).then(function (response) {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        if (response.data.data.counts) {
                            this.eventDetectData.x = response.data.data.times;
                            this.eventDetectData.name = ['数量'];
                            this.eventDetectData.xLabel = '日期（日）';
                            this.eventDetectData.series[0].data = response.data.data.counts;
                        } else {
                            let x = response.data.data.x;
                            let y = response.data.data.y;
                            let xList = [];
                            let yList = [];
                            for (let key in x) {
                                this.eventDetectData.x = x[key];
                                this.eventDetectData.xLabel = Object.keys(x)[0];
                            }
                            this.eventDetectData.series = [];
                            this.eventDetectData.name = [];
                            for (let key in y) {
                                this.eventDetectData.name.push(key)
                                this.eventDetectData.series.push({
                                    data: y[key]
                                });
                            }
                        }
                        this.setChart();
                    } else {
                        this.eventDetectData = {
                            name: [""],
                            x: [],
                            xLabel:'',
                            color: ["#00bd85", "#dabb61", "#e77d4e", "#e96157"],
                            series: [
                                {data: []}
                            ]
                        };
                        this.setChart();
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
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
            showDetail(id) {
                if (this.curDetailId == id) {
                    this.curDetailId = "-1"
                } else {
                    this.curDetailId = id;
                }
            },
            refreshTable(list) {
                let resultHeader = [];
                for (let x in this.tableFieldData) {
                    if (this.tableFieldData[x].selected) {
                        resultHeader.push({
                            id: this.tableFieldData[x].id,
                            name: this.tableFieldData[x].name
                        })
                    }
                }
                this.resultHeader = resultHeader;
            },
            tdFilter(field) {
                let status = false;
                for (let x in this.tableFieldData) {
                    if (this.tableFieldData[x].id == field && this.tableFieldData[x].selected) {
                        status = true;
                    }
                }
                return status;
            },
            tdFilterData(head, list) {
                if (head.name.indexOf('流量') != -1 || head.name.indexOf('文件大小') != -1) {
                    return this.changeUnit(list[head.id])
                } else {
                    return list[head.id];
                }
            },
            changeUnit(val) {
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
            },
            changeWanUnit(val) {
                if (val < 10000) {
                    return val
                } else if (val >= 10000 && val < 10000 * 10000) {
                    val = (val / 10000).toFixed(2);
                    return val + "万"
                } else {
                    val = (val / (10000 * 10000)).toFixed(2);
                    return val + "亿"
                }
            },
            setChart() {
                if (!document.getElementById("event-search-chart")) return false;
                let self = this;
                let eventSearchChart = echarts.init(document.getElementById("event-search-chart"));
                for (let y in this.eventDetectData.series) {
                    this.eventDetectData.series[y].name = this.eventDetectData.name[y] || '数量'
                    this.eventDetectData.series[y].type = "line"
                    this.eventDetectData.series[y].symbol = "circle"
                    this.eventDetectData.series[y].symbolSize = 5
                    this.eventDetectData.series[y].lineStyle = {
                        normal: {
                            width: 0.6
                        }
                    }
                    this.eventDetectData.series[y].itemStyle = {
                        normal: {
                            color: this.hexToRgba(this.eventDetectData.color[y], 100).rgba,
                        },
                        emphasis: {
                            color: this.hexToRgba(this.eventDetectData.color[y], 100).rgba,
                        }
                    }
                    this.eventDetectData.series[y].areaStyle = {
                        normal: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0, color: this.hexToRgba(this.eventDetectData.color[y], 20).rgba // 0% 处的颜色
                                }, {
                                    offset: 1, color: this.hexToRgba(this.eventDetectData.color[y], 0).rgba // 100% 处的颜色
                                }],
                                globalCoord: false // 缺省为 false
                            },
                        }
                    }
                }
                let lineOption = {
                    toolbox: {
                        show: true,
                        iconStyle: {
                            color: "#4a92ff"
                        },
                        emphasis: {
                            iconStyle: {
                                color: "#00bd85"
                            }
                        },
                        feature: {
                            magicType: {
                                type: ['line', 'bar', 'stack', 'tiled'],
                                icon: {
                                    bar: "path://M1,10V1H0v10h12v-1H1z M4,3H2v6h2V3z M7,1H5v8h2V1z M10,6H8v3h2V6z",
                                    line: "path://M1,10V1H0v10h12v-1H1z M8,6l3-1V4L8,5L5,3L2,5v1l3-2L8,6z",
                                }
                            },
                        }
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            lineStyle: {
                                color: "#dfdfe7",
                                opacity: 0.2
                            },
                        },
                        formatter: function (params) {
                            let str = "<div class='font12 p-10'>";
                            str += "<p class='m-b-5'>" + params[0].name + "</p>";
                            for (let x in params) {
                                if (params[x].seriesName.indexOf("流量") != -1 || params[x].seriesName.indexOf("文件大小") != -1) {
                                    str += "<p><span style='display:inline-block;min-width:100px;' class='ys-info-color'>" + params[x].seriesName + "：</span>" + self.changeUnit(params[x].value) + "</p>"
                                } else {
                                    str += "<p><span style='display:inline-block;min-width:100px;' class='ys-info-color'>" + params[x].seriesName + "：</span>" + params[x].value + "</p>"
                                }

                            }
                            str += "</div>"
                            return str;
                        }
                    },
                    grid: {
                        top: '30',
                        bottom: 0,
                        left: 20,
                        right: 60,
                        containLabel: true
                    },
                    legend: {
                        textStyle: {color: "#dfdfe7"},
                        data: self.eventDetectData.name,
                        top: "0",
                        itemWidth: 25,
                        itemHeight: 6
                    },
                    calculable: true,
                    xAxis: [{
                        type: 'category',
                        name: self.eventDetectData.xLabel,
                        data: self.eventDetectData.x,
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
                    }],
                    yAxis: [{
                        type: 'value',
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
                            formatter(params) {
                                if (JSON.stringify(self.eventDetectData.name).indexOf('流量') != -1 || JSON.stringify(self.eventDetectData.name).indexOf('文件大小') != -1) {
                                    return self.changeUnit(params)
                                } else {
                                    return self.changeWanUnit(params)
                                }
                            },
                        },//y轴坐标的字颜色
                        splitLine: {
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        }
                    }],
                    series: self.eventDetectData.series
                };
                eventSearchChart.setOption(lineOption);
                eventSearchChart.on('click', function (params) {
                    let reg = /^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/;
                    if (reg.test(params.name) && self.xData.length == 0) {
                        self.startTime = params.name + ' 00:00:00';
                        self.endTime = params.name + ' 23:59:59';
                        self.goSearch(false);
                    }
                    for (let x in self.xData) {
                        if (self.xData[x].type == 'date') {
                            if (reg.test(params.name)) {
                                self.startTime = params.name + ' 00:00:00';
                                self.endTime = params.name + ' 23:59:59';
                                self.goSearch(false);
                            }
                        } else {
                            self.param_name = self.xData[x].id;
                            self.param_value = params.name;
                        }
                    }
                })
            },
            hexToRgba(hex, al) {
                var hexColor = /^#/.test(hex) ? hex.slice(1) : hex, alp = hex === 'transparent' ? 0 : Math.ceil(al), r,
                    g, b;
                hexColor = /^[0-9a-f]{3}|[0-9a-f]{6}$/i.test(hexColor) ? hexColor : 'fffff';
                if (hexColor.length === 3) {
                    hexColor = hexColor.replace(/(\w)(\w)(\w)/gi, '$1$1$2$2$3$3');
                }
                r = hexColor.slice(0, 2);
                g = hexColor.slice(2, 4);
                b = hexColor.slice(4, 6);
                r = parseInt(r, 16);
                g = parseInt(g, 16);
                b = parseInt(b, 16);
                return {
                    hex: '#' + hexColor,
                    alpha: alp,
                    rgba: 'rgba(' + r + ', ' + g + ', ' + b + ', ' + (alp / 100).toFixed(2) + ')'
                };
            },
            clickType(list, index) {
                for (let key in this.eventSourceTabData) {
                    if (key == index) {
                        Vue.set(this.eventSourceTabData[key], 'active', true);
                    } else {
                        Vue.set(this.eventSourceTabData[key], 'active', false);
                    }
                }
                this.curEventSource = list;
            }
        },
        watch: {
            'curEventSource': function () {
                this.getComData();
                this.getFieldData();
                this.getFieldMapData();
                this.tableList = [].concat([]);
                this.xData = [].concat([]);
                this.yData = [].concat([]);
                this.filterStatus = false;
                this.lineShow = false;
                this.fieldShow = false;
                this.$set('conditionList', []);
                this.eventDetectData = {
                    name: [""],
                    x: [],
                    color: ["#00bd85", "#dabb61", "#e77d4e", "#e96157"],
                    series: [
                        {data: []}
                    ]
                },
                    this.goSearch(false);
                this.getTabData();
                this.setChart();
            },
            'tableList': function () {
                this.refreshTable();
            },
            'curDateRange': function () {
                if (this.curDateRange.id == 1) {
                    this.endTime = moment().format('YYYY-MM-DD HH:mm:ss')
                    this.startTime = moment().add(-1, 'days').format('YYYY-MM-DD HH:mm:ss')
                } else if (this.curDateRange.id == 3) {
                    this.endTime = moment().format('YYYY-MM-DD HH:mm:ss')
                    this.startTime = moment().add(-3, 'days').format('YYYY-MM-DD HH:mm:ss')
                } else if (this.curDateRange.id == 7) {
                    this.endTime = moment().format('YYYY-MM-DD HH:mm:ss')
                    this.startTime = moment().add(-7, 'days').format('YYYY-MM-DD HH:mm:ss')
                } else if (this.curDateRange.id == 30) {
                    this.endTime = moment().format('YYYY-MM-DD HH:mm:ss')
                    this.startTime = moment().add(-30, 'days').format('YYYY-MM-DD HH:mm:ss')
                } else if (this.curDateRange.id == 0) {
                    this.endTime = moment().format('YYYY-MM-DD HH:mm:ss')
                    this.startTime = moment().add(-60, 'minutes').format('YYYY-MM-DD HH:mm:ss')
                }
            },
            'endTime': function () {
                if (new Date(this.startTime).getTime() > new Date(this.endTime).getTime()) {
                    let time = this.endTime;
                    this.endTime = this.startTime;
                    this.startTime = time;
                }
            },
            'startTime': function () {
                if (new Date(this.startTime).getTime() > new Date(this.endTime).getTime()) {
                    let time = this.endTime;
                    this.endTime = this.startTime;
                    this.startTime = time;
                }
            },
            'lineShow': function () {
                this.setChart();
            },
            'param_name': function () {
                this.goSearch(true);
            }
        },
    }
</script>