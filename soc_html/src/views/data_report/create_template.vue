<template>
    <div class="ys-con pos-r">
        <div class="ys-box-con pos-r">
            <input class="ys-input" placeholder="输入模版名称" style="width:160px;" v-model="templateName"/>
            <a class="m-l-10" @click="showEditList()"><i class="ys-icon icon-edit m-r-5"></i>编辑已有模板</a>
            <div class="edit-template-box" transition="slide" v-show="editTable">
                <div class="edit-template-tool clearfix">
                  <span class="search-box m-l-20 pos-r">
                    <input v-model="searchValue"
                           class="ys-input m-l-20"
                           placeholder="输入关键字搜索"
                           @blur="tableRe()"
                           @keyup.enter="tableRe()"/>
                    <i class="ys-icon icon-search ys-primary-color" @click="tableRe()"></i>
                  </span>
                </div>
                <div class="m-t-10 clearfix" style="height:350px;">
                    <div class="col-md-4 edit-template-box-list" v-for="list in tableList"
                         v-bind:class="[editId==list.id ? 'ys-white-color' : 'ys-info-color' ]"
                         @click="selectEditTemp(list)">
                        <tooltip :content="list.name" :delay="0">
                            <p style="height: 34px;line-height: 34px;overflow:hidden;"><i
                                    class="ys-icon icon-template m-r-5 ys-primary-color"></i>{{list.name}}</p>
                        </tooltip>
                    </div>
                </div>
                <table-data :url='tableUrl'
                            :data.sync="tableList"
                            :search.sync="searchValue"
                            :table-length="30"
                            :jump="false"
                            :page-place="'center'"
                            :load-set="false"
                            v-ref:table></table-data>
            </div>
            <div class="fRight d-i-b">
                <button class="ys-btn" @click=changeTempConfig()>保存</button>
                <button class="ys-btn ys-btn-blue m-l-10" @click='showViewStatus = !showViewStatus'>预览</button>
                <button class="ys-btn ys-btn-white m-l-10" @click="quitSave()">重置</button>
            </div>
        </div>
        <div id="tem-right" class="template-right m-t-10">
            <div class="ys-box-con">
                <div class="textC tem-tip m-b-10 ys-info-color ys-display-box-title ys-display-box-item">
                    <i class="ys-icon icon-add-circle m-r-10"></i><span>拖动组件到此添加</span>
                </div>
                <div id="tem-right-box" style="min-height: 1000px">
                    <div v-for="list in virtTree">
                        <div class="tem-wrap m-b-10">
                            <ul class="tem-inner">
                                <li class="d-i-b tem-btn verticalM" v-if="list.type != 'echart'">
                                    <a @click="list.status = !list.status">
                                        <tooltip v-if="!list.status" :content="'编辑'" :delay="0">
                                            <i class="ys-icon icon-edit"></i>
                                        </tooltip>
                                        <tooltip v-if="list.status" :content="'确认'" :delay="0">
                                            <i class="ys-icon icon-check"></i>
                                        </tooltip>
                                    </a>
                                </li>
                                <li class="d-i-b tem-btn verticalM">
                                    <tooltip :content="'删除'" :delay="0">
                                        <a @click="deleteStm(list.id)"><i class="ys-icon icon-trash ys-error-color"></i></a>
                                    </tooltip>
                                </li>
                            </ul>
                            <div class="ys-box" v-if="list.type == 'module'">
                                <div v-if="!list.status">
                                    <h2 class="textC">{{list.params.title}}</h2><h4 class="textC">
                                    {{list.params.time}}</h4>
                                </div>
                                <div v-if="list.status">
                                    <h2 class="textC">
                                        <input type="text" v-model="list.params.title"
                                               @keyup.13='list.status = !list.status'
                                               class="ys-input ys-input-h2 textC">
                                    </h2>
                                    <h4 class="textC">
                                        <input type="text" v-model="list.params.time"
                                               @keyup.13='list.status = !list.status'
                                               class="ys-input ys-input-h4 textC">
                                    </h4>
                                </div>
                            </div>
                            <div class="ys-box" v-if="list.type == 'title1'">
                                <div v-if="!list.status">
                                    <h2>{{list.params.title}}</h2>
                                </div>
                                <div class=" m-t-20 m-b-10" v-if="list.status">
                                    <input type="text" v-model="list.params.title"
                                           @keyup.13='list.status = !list.status' class="ys-input ys-input-h2">
                                </div>
                            </div>
                            <div class="ys-box" v-if="list.type == 'title2'">
                                <div v-if="!list.status">
                                    <h3>{{list.params.title}}</h3>
                                </div>
                                <div class=" m-t-20 m-b-10" v-if="list.status">
                                    <input type="text" v-model="list.params.title"
                                           @keyup.13='list.status = !list.status' class="ys-input ys-input-h3">
                                </div>
                            </div>
                            <div class="ys-box" v-if="list.type == 'title3'">
                                <div v-if="!list.status">
                                    <h4 class="m-t-20">{{list.params.title}}</h4>
                                </div>
                                <div class=" m-t-20 m-b-10" v-if="list.status">
                                    <input type="text" v-model="list.params.title"
                                           @keyup.13='list.status = !list.status' class="ys-input ys-input-h4">
                                </div>
                            </div>
                            <div class="ys-box m-t-20 m-b-10" v-if="list.type == 'text'">
                                <div v-if="!list.status">
                                    <p style="text-indent:2em ;line-height: 1.5">
                                        {{list.params.title}}</p>
                                </div>
                                <div class="textC" v-if="list.status">
                                    <textarea v-model="list.params.title" @keyup.13='list.status = !list.status'
                                              class="ys-textarea"></textarea>
                                </div>
                            </div>
                            <div v-if="list.type == 'echart'" class="m-t-20 m-b-10">
                                <div v-if="list.params.selected"
                                     :key="list.params.id" class="ys-box">
                                    <div class="display-chart-box m-b-10" style="overflow: hidden">
                                        <div class="box">
                                            <div class="title clearfix">
                                                <span>{{list.params.name}}</span>
                                            </div>
                                            <div>
                                                <div class="fRight" style="position: relative">
                                                    <checkbox v-if="list.params.chart_type.id != 'table'"
                                                              :show.sync="list.params.has_table"
                                                              :text="'显示表格'"></checkbox>
                                                    <div style="position: absolute;left: -145px;top: 0px;z-index: 3">
                                                        <ys-select v-if="list.data_type == terminal_type"
                                                                   :option="sectionTypeData"
                                                                   :width="140"
                                                                   :selected.sync="list.params.section"
                                                                   :searchable="false"
                                                                   :multiple="true"
                                                                   :filter="true"></ys-select>
                                                    </div>
                                                    <ys-select v-if="list.params.chart_type.id != 'table'"
                                                               :option="chartTypeData"
                                                               :width="88"
                                                               :selected.sync="list.params.chart_type"
                                                               :searchable="false"
                                                               :filter="true"></ys-select>
                                                    <span class="verticalM ys-info-color">统计周期:</span>
                                                    <ys-select :option="timeTypeData"
                                                               :width="64"
                                                               :selected.sync="list.params.cycle"
                                                               :searchable="false"
                                                               :filter="true"></ys-select>
                                                </div>
                                                <div class="clearfix"></div>
                                            </div>
                                            <div class="con text-cursor"
                                                 v-bind:class="[list.params.has_table ? '' : 'has-table']">
                                                <chart :type="list.params.chart_type.id" :info="list.params.data"
                                                       :unit="list.params.unit"
                                                       :name="list.params.name"></chart>
                                                <div v-if="list.params.has_table" style="width:80%;margin:10px auto;">
                                                    <table class="ys-table"
                                                           style="word-break: keep-all;white-space: nowrap">
                                                        <thead>
                                                        <tr>
                                                            <th></th>
                                                            <th v-for="row in splice_tool(list.params.data.labels)">{{row}}</th>
                                                        </tr>
                                                        </thead>
                                                        <tbody>
                                                        <tr>
                                                            <td>{{list.params.data.data[0].name}}</td>
                                                            <td v-for="colCon in splice_tool(list.params.data.data[0].data)"
                                                                track-by="$index">
                                                                {{colCon}}
                                                            </td>
                                                        </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                                <p class="description">
                                                    <span class="ys-info-color verticalM">说明文字：</span>
                                                    <input class="ys-input" placeholder="添加说明文字" style="width:160px;"
                                                           v-model="list.params.remark"/>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="template-left" :class="{'template-left-fixed':SCROLL_OVER}">
            <div class="m-t-10" id="tem-left">
                <div class="ys-box m-b-10">
                    <div class="ys-display-box-title">
                        <span>文档结构类组件</span>
                    </div>
                </div>
                <div class="ys-box m-b-10 ys-info-color">
                    <div class="ys-display-box-title ys-display-box-item">
                        <span>报告名称</span>
                        <a class="fRight" @click="changeTxtStatus(tempModule)"><i class="ys-icon icon-downlist-up"
                                                                                  v-bind:class="[tempModule.show ? '' : 'arrow-rotate' ]"></i></a>
                    </div>
                    <div class="clearfix ys-box-con template-chart-box"
                         v-bind:class="[tempModule.show ? 'on' : 'off' ]" id="ys-display-box-title-name">
                        <div v-for="item in tempModule.list" class="ys-display-box-title-item ys-box-con"
                             v-html="item.template"></div>
                    </div>
                </div>
                <div class="ys-box m-b-10 ys-info-color">
                    <div class="ys-display-box-title ys-display-box-item ">
                        <span>标题</span>
                        <a class="fRight" @click="changeTxtStatus(tempTitle)"><i class="ys-icon icon-downlist-up"
                                                                                 v-bind:class="[tempTitle.show ? '' : 'arrow-rotate' ]"></i></a>
                    </div>
                    <div class="clearfix ys-box-con template-chart-box" id="ys-display-box-title-title"
                         v-bind:class="[tempTitle.show ? 'on' : 'off' ]">
                        <div v-for="item in tempTitle.list" :data-type="item.type"
                             class="ys-display-box-title-item ys-box-con" :class="item.type != 'title3'?'m-b-10':''"
                             v-html="item.template"></div>
                    </div>
                </div>
                <div class="ys-box m-b-10 ys-info-color">
                    <div class="ys-display-box-title ys-display-box-item">
                        <span>正文说明</span>
                        <a class="fRight" @click="changeTxtStatus(tempText)"><i class="ys-icon icon-downlist-up"
                                                                                v-bind:class="[tempText.show ? '' : 'arrow-rotate' ]"></i></a>
                    </div>
                    <div class="clearfix ys-box-con template-chart-box" id="ys-display-box-title-text"
                         v-bind:class="[tempText.show ? 'on' : 'off' ]">
                        <div v-for="item in tempText.list" class="ys-display-box-title-item ys-box-con"
                             v-html="item.template"></div>
                    </div>
                </div>
                <div class="ys-box m-t-20 m-b-10">
                    <div class="ys-display-box-title">
                        <span>数据图表类组件</span>
                    </div>
                </div>
                <div class="ys-box tem-left-box m-b-10 ys-info-color" :id="'tem-left-'+item"
                     v-for="(item,chart) in chartData"
                     :key="chart.data_type">
                    <div class="ys-display-box-title ys-display-box-item">
                        <span>{{chart.data_type_name}}</span>
                        <a class="fRight" @click="changeChartStatus(chart,index)"><i class="ys-icon icon-downlist-up"
                                                                                     v-bind:class="[chart.show ? '' : 'arrow-rotate' ]"></i></a>
                    </div>
                    <div class="clearfix ys-box-con template-chart-box" v-bind:class="[chart.show ? 'on' : 'off' ]">
                        <div v-for="(index,list) in chart.data">
                            <div v-if="!list.selected" :id="'display-chart-box-'+item+'-'+index" :data-a="item"
                                 :data-b="index"
                                 :key="list.id">
                                <div class="display-chart-box m-b-10" style="overflow: hidden">
                                    <div class="box">
                                        <div class="title clearfix">
                                            <span>{{list.name}}</span>
                                        </div>
                                        <div class="tool-box">
                                            <div class="fRight" style="position: relative">
                                                <checkbox v-if="list.chart_type.id != 'table'"
                                                          :show.sync="list.has_table" :text="'显示表格'"></checkbox>
                                                <div style="position: absolute;left: -145px;top: 0px;z-index: 3">
                                                    <ys-select v-if="chart.data_type == terminal_type"
                                                               :option="sectionTypeData"
                                                               :width="140"
                                                               :selected.sync="list.section"
                                                               :searchable="false"
                                                               :multiple="true"
                                                               :filter="true"></ys-select>
                                                </div>
                                                <ys-select v-if="list.chart_type.id != 'table'" :option="chartTypeData"
                                                           :width="88"
                                                           :selected.sync="list.chart_type"
                                                           :searchable="false"
                                                           :filter="true"></ys-select>
                                                <span class="verticalM ys-info-color">统计周期:</span>
                                                <ys-select :option="timeTypeData"
                                                           :width="64"
                                                           :selected.sync="list.cycle"
                                                           :searchable="false"
                                                           :filter="true"></ys-select>
                                            </div>
                                            <div class="clearfix"></div>
                                        </div>
                                        <div class="con text-cursor" v-bind:class="[list.has_table ? '' : 'has-table']">
                                            <chart :type="list.chart_type.id" :info="list.data" :unit="list.unit"
                                                   :name="list.name"></chart>
                                            <div v-if=" (list.chart_type.id != 'table') && (list.has_table)"
                                                 style="width:100%;margin:10px auto;">
                                                <table class="ys-table"
                                                       style="word-break: keep-all;white-space: nowrap">
                                                    <thead>
                                                    <tr>
                                                        <th></th>
                                                        <th v-for="row in splice_tool(list.data.labels)"
                                                            track-by="$index">{{row}}
                                                        </th>
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                    <tr>
                                                        <td>{{list.data.data[0].name}}</td>
                                                        <td v-for="colCon in splice_tool(list.data.data[0].data)"
                                                            track-by="$index">
                                                            {{colCon}}
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                            <p class="description">
                                                <span class="ys-info-color verticalM">说明文字：</span>
                                                <input class="ys-input" placeholder="添加说明文字" style="width:160px;"
                                                       v-model="list.remark"/>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <aside :show.sync="showViewStatus" :header="'模版预览'" :width="'980px'" :left="'auto'">
            <div v-if="showViewStatus">
                <div v-for="list in virtTree">
                    <div class="m-b-10">
                        <div class="ys-box" v-if="list.type == 'module'">
                            <div>
                                <h2 class="textC">{{list.params.title}}</h2><h4 class="textC">{{list.params.time}}</h4>
                            </div>
                        </div>
                        <div class="ys-box" v-if="list.type == 'title1'">
                            <div>
                                <h2>{{list.params.title}}</h2>
                            </div>
                        </div>
                        <div class="ys-box" v-if="list.type == 'title2'">
                            <div>
                                <h3>{{list.params.title}}</h3>
                            </div>
                        </div>
                        <div class="ys-box" v-if="list.type == 'title3'">
                            <div>
                                <h4>{{list.params.title}}</h4>
                            </div>
                        </div>
                        <div class="ys-box m-t-20 m-b-10" v-if="list.type == 'text'">
                            <div>
                                <p style="text-indent:2em ;line-height: 1.5">
                                    {{list.params.title}}</p>
                            </div>
                        </div>
                        <div v-if="list.type == 'echart'" class="m-t-20 m-b-10">
                            <div v-if="list.params.selected"
                                 :key="list.params.id" class="ys-box">
                                <div class="display-chart-box m-b-10">
                                    <div class="box">
                                        <div class="title clearfix">
                                            <span>{{list.params.name}}</span>
                                        </div>
                                        <div class="con text-cursor"
                                             v-bind:class="[list.params.has_table ? '' : 'has-table']">
                                            <chart :type="list.params.chart_type.id" :info="list.params.data"
                                                   :unit="list.params.unit"
                                                   :width="'600px'"
                                                   :name="list.params.name"></chart>
                                            <div v-if="(list.params.chart_type.id != 'table') && (list.params.has_table)"
                                                 style="width:600px;margin:10px auto;">
                                                <table class="ys-table">
                                                    <thead>
                                                    <tr>
                                                        <th></th>
                                                        <th v-for="row in splice_tool(list.params.data.labels)"
                                                            track-by="$index">{{row}}
                                                        </th>
                                                    </tr>
                                                    </thead>
                                                    <tbody>
                                                    <tr>
                                                        <td>{{list.params.data.data[0].name}}</td>
                                                        <td v-for="colCon in splice_tool(list.params.data.data[0].data)"
                                                            track-by="$index">
                                                            {{colCon}}
                                                        </td>
                                                    </tr>
                                                    </tbody>
                                                </table>
                                            </div>
                                            <p class="description textC m-t-10 verticalM">{{list.params.remark}}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    </div>
</template>
<style scoped>
    h2 {
        font-size: 22px;
        font-weight: 100;
    }

    h3 {
        font-size: 18px;
        font-weight: 100;
    }

    h4 {
        font-size: 14px;
        font-weight: 100;
    }

    .ys-input-h2 {
        height: 36px;
        width: 100%;
        font-size: 22px;
    }

    .ys-input-h3 {
        height: 30px;
        width: 100%;
        font-size: 18px;
    }

    .ys-input-h4 {
        width: 100%;
        font-size: 14px;
    }

    .ys-display-box-title {
        height: 42px;
        line-height: 42px;
    }

    .tem-tip {
    }

    .ys-display-box-item {
        box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.2);
        background: rgba(0, 0, 0, 0.15);
    }

    .template-left {
        width: 495px;
        float: right;
    }

    .template-left-fixed {
        width: 495px;
        position: fixed !important;
        right: 15px !important;
        top: 50px !important;
        bottom: 15px !important;
    }

    .template-right {
        width: calc(100% - 505px);
        float: left;
    }

    .edit-template-box {
        width: 360px;
        height: 470px;
        background: linear-gradient(to right, #1c1c2d, #2d2831);
        padding-bottom: 10px;
        border-top: none;
        border-radius: 3px;
        box-shadow: 2px 2px 5px 1px rgba(0, 0, 0, 0.3);
        position: absolute;
        top: 42px;
        left: 15px;
        z-index: 1;
        padding: 15px;
    }

    .edit-template-box-list {
        padding-left: 10px;
        height: 34px;
        line-height: 34px;
        border: 1px solid rgba(0, 0, 0, 0);
        cursor: pointer;
    }

    .edit-template-box-list:hover, .edit-template-box-list.on {
        border: 1px solid rgba(74, 146, 255, 1);
        position: relative;
    }

    .slide-transition {
        display: inline-block; /* 否则 scale 动画不起作用 */
    }

    .slide-enter {
        animation: antSlideUpIn .5s;
    }

    .slide-leave {
        animation: antSlideUpOut .5s;
    }

    @-webkit-keyframes antSlideUpIn {
        0% {
            opacity: 0;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(0.8);
            transform: scaleY(0.8);
        }
        100% {
            opacity: 1;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(1);
            transform: scaleY(1);
        }
    }

    @keyframes antSlideUpIn {
        0% {
            opacity: 0;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(0.8);
            transform: scaleY(0.8);
        }
        100% {
            opacity: 1;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(1);
            transform: scaleY(1);
        }
    }

    @-webkit-keyframes antSlideUpOut {
        0% {
            opacity: 1;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(1);
            transform: scaleY(1);
        }
        100% {
            opacity: 0;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(0.8);
            transform: scaleY(0.8);
        }
    }

    @keyframes antSlideUpOut {
        0% {
            opacity: 1;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(1);
            transform: scaleY(1);
        }
        100% {
            opacity: 0;
            -webkit-transform-origin: 0% 0%;
            transform-origin: 0% 0%;
            -webkit-transform: scaleY(0.8);
            transform: scaleY(0.8);
        }
    }

    .edit-template-tool {
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(74, 146, 255, 0.4);
    }

    .search-box {
        position: relative;
        float: right;
    }

    .search-box i {
        position: absolute;
        top: 7px;
        right: 5px;
    }

    .arrow-rotate {
        transform: rotate(180deg);
    }

    .col-md-6 {
        padding: 0px;
    }

    .template-chart-box {
        overflow-y: hidden;
        /*max-height: 5000px; !* approximate max height *!*/
        /*transition-property: all;*/
        /*transition-duration: 0.5s;*/
        /*transition-timing-function: cubic-bezier(0, 1, 0.5, 1);*/
    }

    .template-chart-box.off {
        max-height: 0;
        padding: 0px;
    }

    .template-chart-box .col-md-6:nth-child(even) {
        padding-left: 10px !important;
    }

    .display-chart-box {
        border-top: 1px solid rgba(74, 146, 255, 0.25);
        background: rgba(0, 0, 0, 0.15);
        position: relative;
        cursor: move;
    }

    .display-chart-box .title:before {
        content: '';
        width: 232px;
        height: 36px;
        background: url('../../assets/images/ys-display-box-title-tag.png');
        background-size: 232px;
        position: absolute;
        left: 0px;
        top: 0px;
        z-index: -1;
    }

    .display-chart-box .title {
        height: 36px;
        line-height: 36px;
        padding-left: 15px;
    }

    .display-chart-box .con {
        height: 300px;
        padding-top: 10px;
    }

    .display-chart-box .con.has-table {
        padding-top: 20px;
    }

    .display-chart-box .con .description {
        position: absolute;
        bottom: 15px;
        left: 15px;
    }

    #tem-right-box .ys-box {
        cursor: move;
    }

    .tem-wrap {
        position: relative;
        border: 1px dashed #9ABCEE;
        padding: 0px 20px;
        cursor: move;
    }

    .tem-inner {
        position: absolute;
        right: 7px;
        top: 7px;
        text-align: right;
    }

    .tem-btn {
        width: 18px;
        height: 18px;
    }

    .ys-display-box-title-item {
        cursor: move;
    }
</style>
<script>
    import Api from 'src/lib/api'
    import chart from "./chart";

    let Sortable = require('sortable');
    let moment = require('moment')
    export default {
        name: "create-template",
        data() {
            return {
                editTable: false,
                tableUrl: "/api/ssa/report/template/dts",
                searchValue: "",
                tableList: "",
                chartTypeData: [
                    {id: "bar_x", name: "柱状图"},
                    {id: "bar_y", name: "条形图"},
                    {id: "bar_pile_x", name: "堆叠柱状图"},
                    {id: "bar_pile_y", name: "堆叠条形图"},
                    {id: "line", name: "折线图"},
                    {id: "pie", name: "饼形图"},
                    {id: "number", name: "合计数"},
                    {id: "scatter", name: "散点图"},
                ],
                chartTypeDataHidden: [
                    {id: "bar_x", name: "柱状图"},
                    {id: "bar_y", name: "条形图"},
                    {id: "bar_pile_x", name: "堆叠条形图"},
                    {id: "bar_pile_y", name: "堆叠条形图"},
                    {id: "line", name: "折线图"},
                    {id: "pie", name: "饼形图"},
                    {id: "number", name: "合计数"},
                    {id: "scatter", name: "散点图"},
                    {id: "table", name: "表格"},
                ], //添加表格
                timeTypeData: [
                    {id: 1, name: "按天"},
                    {id: 7, name: "按周"},
                    {id: 30, name: "按月"},
                    {id: 90, name: "按季度"},
                    {id: 365, name: "按年"},
                ],
                sectionTypeData: [
                    {id: '', name: '全部部门'},
                ],
                topTypeData: [
                    {id: 5, name: 'TOP5'},
                    {id: 10, name: 'TOP10'},
                    {id: 99, name: '全量'},
                ],
                chartData: [],
                templateName: "",
                editStatus: false,
                editId: this.$route.params.id,
                virtTree: [],
                virtTree_edit: [],
                virtTree_tag: [],
                tempModule: {
                    show: false,
                    list: [{
                        type: 'module',
                        template: '<h2 class="textC m-t-0 m-b-0" style="font-size: 22px;font-weight: 100;">报告名称</h2><h4 class="textC m-b-0" style="font-size: 14px;font-weight: 100;"">' + moment().format('YYYY-MM-DD') + '</h4>'
                    }]
                },
                tempTitle: {
                    show: false,
                    list: [{
                        name: '一级标题',
                        type: 'title1',
                        template: '<h2 class="m-t-0 m-b-0" style="font-size: 22px;font-weight: 100;">一级标题</h2>'
                    }, {
                        name: '二级标题',
                        type: 'title2',
                        template: '<h3 class="m-t-0 m-b-0" style="font-size: 18px;font-weight: 100;">二级标题</h3>'
                    }, {
                        name: '三级标题',
                        type: 'title3',
                        template: '<h4 class="m-t-0 m-b-0" style="font-size: 14px;font-weight: 100;">三级标题</h4>'
                    }]
                },
                tempText: {
                    show: false,
                    list: [{
                        type: 'text',
                        template: '<p class="textC">正文</h4>'
                    }]
                },
                showViewStatus: false,
                terminal_type: 3,
                SCROLL_OVER: false
            }
        },
        ready() {
            let self = this;
            if (this.editId == ":id") {
                this.initSortable();
                this.getTeam();
                this.getCellType();
            } else {
                this.editStatus = true;
                this.getEditTask();
            }
            $('#tem-left').slimScroll({
                height: $(window).height() - 65,
                position: 'right',
                size: "5px",
            });
            window.addEventListener('scroll', (e) => {
                if ($(document).scrollTop() > 60) {
                    self.SCROLL_OVER = true;
                } else {
                    self.SCROLL_OVER = false;
                }
            })
        },
        methods: {
            //部门列表
            getTeam() {
                return new Promise((resolve) => {
                    this.$http.get('/api/assets/team/list').then(function (response) {
                        if (response.data.status == 200) {
                            this.sectionTypeData = [{id: '-1', name: '全部部门'}].concat(response.data.data);
                            resolve();
                        }
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                });
            },
            //删除echart
            deleteStm(id) {
                this.virtTree.forEach((obj, index) => {
                    if (obj.id == id) {
                        this.virtTree.splice(index, 1);
                        if (obj.type == 'echart') {
                            obj.params.selected = false;
                            this.$nextTick(() => {
                                this.echartTem()
                            })
                        }
                        return true
                    }
                })
            },
            //排序标题
            initSortable() {
                let self = this;
                [
                    {
                        id: 'ys-display-box-title-name',
                        handle: ".ys-display-box-title-item",
                        fun: function (evt) {
                            $(evt.item).remove()
                            self.virtTree.splice(evt.newIndex, 0, {
                                type: 'module',
                                id: new Date().getTime(),
                                status: false,
                                params: {title: '报告名称', time: moment().format('YYYY-MM-DD')}
                            })
                        },
                        pull: 'clone'
                    }, {
                    id: 'ys-display-box-title-title',
                    handle: ".ys-display-box-title-item",
                    fun: function (evt) {
                        let type = '', title = '';
                        if (evt.clone.dataset.type == 'title1') {
                            type = 'title1', title = '一级标题'
                        }
                        if (evt.clone.dataset.type == 'title2') {
                            type = 'title2', title = '二级标题'
                        }
                        if (evt.clone.dataset.type == 'title3') {
                            type = 'title3', title = '三级标题'
                        }
                        $(evt.item).remove()
                        self.virtTree.splice(evt.newIndex, 0, {
                            type: type,
                            id: new Date().getTime(),
                            status: false,
                            params: {title: title}
                        })
                    },
                    pull: 'clone'
                }, {
                    id: 'ys-display-box-title-text',
                    handle: ".ys-display-box-title-item",
                    fun: function (evt) {
                        $(evt.item).remove()
                        self.virtTree.splice(evt.newIndex, 0, {
                            type: 'text',
                            id: new Date().getTime(),
                            status: false,
                            params: {title: '文本'}
                        })
                    },
                    pull: 'clone'
                }].forEach((obj) => {
                    new Sortable(document.getElementById(obj.id), Object.assign({
                        group: {
                            name: 'tem',
                            pull: obj.pull,
                            put: false
                        },
                        animation: 150,
                        handle: obj.handle,
                        sort: false,
                        onRemove: obj.fun
                    }, obj))
                });
                new Sortable(document.getElementById('tem-right-box'), {
                    group: {
                        name: 'tem',
                        pull: true,
                        put: true
                    },
                    handle: ".ys-box",
                    animation: 150,
                    sort: true,
                    onEnd: function (evt) {
                        let over = self.virtTree[evt.oldIndex];
                        self.virtTree.splice(evt.oldIndex, 1);
                        self.virtTree.splice(evt.newIndex, 0, over);
                    },
                })
            },
            //显示编辑弹窗
            showEditList: function () {
                this.editTable = !this.editTable;
            },
            //选中可编辑模版
            selectEditTemp: function (list) {
                this.editId = list.id;
                this.editTable = !this.editTable;
                this.getEditTask();
            },
            tableRe() {
                this.$refs.table.Re()
            },
            //正文 标题 显示
            changeTxtStatus(chart) {
                chart.show = !chart.show
            },
            //切换报表类型 获取数据
            changeChartStatus(chart) {
                this.chartData.forEach((obj) => {
                    if (obj.data_type == chart.data_type) {
                        if (!chart.show && !chart.data.length) {
                            this.getCellData(chart.data_type);
                        }
                        this.$nextTick(() => {
                            chart.show = !chart.show;
                        });
                    } else {
                        obj.show = false;
                    }
                })
            },
            //获取报表类型列表
            getCellType() {
                return new Promise((resolve) => {
                    this.$root.loadStatus = true;
                    this.$http.post('/api/ssa/report/cell/type').then(function (response) {
                        this.$root.loadStatus = false;
                        for (let i in response.data.data) {
                            response.data.data[i]['show'] = false;
                        }
                        this.$set('chartData', response.data.data);
                        resolve();
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                })
            },
            //获取cell数据
            getCellData(type) {
                this.$root.loadStatus = true;
                return new Promise((resolve) => {
                    let data = {
                        data_type: type
                    };
                    this.$http.post('/api/ssa/report/cell', data).then(function (response) {
                        if (response.data.status == 200) {
                            let data = response.data.data;
                            for (let module in data) {
                                data[module].remark = "";
                                data[module].selected = false;
                                data[module].has_table = false;
                                data[module].cycle = {id: 1, name: "天"};
                                if (type == this.terminal_type) {
                                    data[module].section = [{id: '-1', name: '全部部门'}];
                                } else {
                                    data[module].section = [];
                                }
                                data[module].top = {id: 5, name: "TOP5"};
                                for (let x in this.chartTypeDataHidden) {
                                    if (data[module].chart_type == this.chartTypeDataHidden[x].id) {
                                        data[module].chart_type = this.chartTypeDataHidden[x];
                                    }
                                }
                                data[module]['unit'] = 'number';
                                if (data[module]['data']['data'] && data[module]['data']['data'].length) {
                                    for (let x in data[module]['data']['data']) {
                                        if (data[module]['data']['data'][0]['name'].toString().indexOf('流量') != -1) {
                                            data[module]['unit'] = 'band';
                                        }
                                    }
                                }
                            }
                            for (let i in this.chartData) {
                                if (this.chartData[i].data_type == type) {
                                    this.chartData[i]['data'] = [].concat(data);
                                }
                            }
                            this.$nextTick(() => {
                                this.echartTem();
                            })
                        }
                        this.$root.loadStatus = false;
                        resolve()
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                })
            },
            //编辑任务
            getEditTask() {
                Promise.all([this.getTeam(), this.getTemplate(), this.getCellType()]).then((result) => {
                    this.getCellData_foreach().then(() => {
                        this.getEditData();
                    });
                })
            },
            //循环获取类型数据
            getCellData_foreach() {
                let result = Promise.resolve();
                this.virtTree_tag.forEach((type) => {
                    result = result.then(() => {
                        return this.getCellData(type);
                    });
                });
                return result;
            },
            //根据模版数据 获取类型id
            getTemplate() {
                return new Promise((resolve) => {
                    this.$http.get('/api/ssa/report/template/' + this.editId).then(function (response) {
                        this.virtTree_edit = JSON.parse(response.data.data.content);
                        this.templateName = response.data.data.name;
                        for (let i in this.virtTree_edit) {
                            if (this.virtTree_edit[i]['type'] == 'echart') {
                                this.virtTree_edit[i]['data_type'] && this.virtTree_tag.indexOf(this.virtTree_edit[i]['data_type']) == -1 ? this.virtTree_tag.push(this.virtTree_edit[i]['data_type']) : '';
                            }
                        }
                        resolve();
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                })
            },
            //编辑返回 对比显示
            getEditData() {
                let data = this.chartData;
                for (let module in data) {
                    data[module].show = false;
                    for (let list in data[module].data) {
                        data[module].data[list].remark = "";
                        data[module].data[list].selected = false;
                        data[module].data[list].has_table = false;
                        data[module].data[list].cycle = {id: 1, name: "天"};
                        for (let x in this.chartTypeDataHidden) {
                            if (data[module].data[list].chart_type == this.chartTypeDataHidden[x].id) {
                                data[module].data[list].chart_type = this.chartTypeDataHidden[x];
                            }
                        }
                        data[module].data[list]['unit'] = 'number';
                        if (data[module].data[list]['data']['data'] && data[module].data[list]['data']['data'].length) {
                            for (let x in data[module].data[list]['data']['data']) {
                                if (data[module].data[list]['data']['data'][0]['name'].toString().indexOf('流量') != -1) {
                                    data[module].data[list]['unit'] = 'band';
                                }
                            }
                        }
                        if (data[module].data_type == this.terminal_type) {
                            data[module].data[list].section = [{id: '-1', name: '全部部门'}];
                        } else {
                            data[module].data[list].section = [];
                        }
                        data[module].data[list].top = {id: 5, name: "TOP5"};
                    }
                }
                let mid = this.virtTree_edit, arr = [];
                for (let i in mid) {
                    let obj = mid[i];
                    let o = {};
                    if (obj.type != 'echart') {
                        o.id = new Date().getTime() + i;
                        o.status = false;
                        o.type = obj.type;
                        o.params = obj.params;
                        arr.push(o);
                    } else {
                        for (let module in data) {
                            for (let list in data[module].data) {
                                if (obj.id == data[module].data[list].id) {
                                    data[module].data[list].remark = obj.remark;
                                    data[module].data[list].selected = true;
                                    data[module].data[list].data_type = obj.data_type;
                                    data[module].data[list].has_table = obj.has_table;
                                    for (let x in this.chartTypeDataHidden) {
                                        if (obj.chart_type == this.chartTypeDataHidden[x].id) {
                                            data[module].data[list].chart_type = this.chartTypeDataHidden[x];
                                        }
                                    }
                                    for (let x in this.timeTypeData) {
                                        if (obj.cycle == this.timeTypeData[x].id) {
                                            data[module].data[list].cycle = this.timeTypeData[x];
                                        }
                                    }
                                    data[module].data[list].section = [].concat(obj.section);
                                    for (let x in this.topTypeData) {
                                        if (obj.top == this.topTypeData[x].id) {
                                            data[module].data[list].top = this.topTypeData[x];
                                        }
                                    }
                                    o.id = new Date().getTime() + i;
                                    o.type = obj.type;
                                    o.data_type = obj.data_type;
                                    o.params = data[module].data[list];
                                    if (!arr.includes(o)) {
                                        arr.push(o);
                                    }
                                    break;
                                }
                            }
                        }
                    }
                }
                this.virtTree = [].concat(arr);
                this.chartData = [].concat(data);
                this.$nextTick(() => {
                    this.initSortable();
                    this.echartTem();
                })
            },
            changeTempConfig() {
                var time = new Date();//获取系统当前时间
                var year = time.getFullYear();
                var month = time.getMonth() + 1;
                var date = time.getDate();//系统时间月份中的日
                var day = time.getDay();//系统时间中的星期值

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
                let schedule_start_date = year + "-" + month + "-" + date;
                let schedule_time = hour + ":" + minutes + ":" + seconds;
                if (this.templateName == "") {
                    this.$root.alertError = true;
                    this.$root.errorMsg = "模板名称必须输入";
                    return false;
                }
                if (this.virtTree.length == 0) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = "至少添加一个模块";
                    return false;
                }
                let arr = [];
                this.virtTree.forEach((obj) => {
                    let o = {};
                    o.type = obj.type;
                    if (obj.type != 'echart') {
                        o.params = obj.params;
                    } else {
                        o.id = obj.params.id;
                        o.name = obj.params.name;
                        o.remark = obj.params.remark;
                        o.cycle = obj.params.cycle.id;
                        o.has_table = obj.params.has_table ? 1 : 0;
                        o.chart_type = obj.params.chart_type.id;
                        if (obj.data_type == this.terminal_type) {
                            if (obj.params.section.length == 0) {
                                o.section = [{id: '-1', name: '全部部门'}]
                            } else {
                                o.section = obj.params.section;
                            }
                        }
                        o.unit = obj.params.unit;
                        o.top = obj.params.top.id;
                        o.data_type = obj.data_type;
                        o.report_type = obj.params.report_type;
                    }
                    arr.push(o);
                })
                let data = {
                    name: this.templateName,
                    content: arr,
                    schedule_start_date: schedule_start_date,
                    schedule_time: schedule_time,
                    schedule_type: 2
                }
                if (this.editStatus) {
                    this.$root.loadStatus = true;
                    this.$http.put('/api/ssa/report/template/' + this.editId, data).then(function (response) {
                        this.$root.loadStatus = false;
                        if (response.data.status == 200) {
                            this.$root.alertSuccess = true;
                            setTimeout(() => {
                                this.$router.go({'name': 'data-report-template-mgt','query':{tag:3}})
                            }, 1000)
                        } else {
                            this.$root.alertError = true;
                        }
                        this.$root.errorMsg = response.data.msg;
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                } else {
                    this.$root.loadStatus = true;
                    this.$http.post('/api/ssa/report/template', data).then(function (response) {
                        this.$root.loadStatus = false;
                        if (response.data.status == 200) {
                            this.$root.alertSuccess = true;
                            setTimeout(() => {
                                this.$router.go({'name': 'data-report-template-mgt','query':{tag:3}})
                            }, 1000)
                        } else {
                            this.$root.alertError = true;
                        }
                        this.$root.errorMsg = response.data.msg;
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                }
            },
            //取消事件
            quitSave() {
                if (this.editId == ":id") {
                    this.virtTree.forEach((obj) => {
                        if (obj.type == 'echart') {
                            obj.params.selected = false;
                        }
                    })
                    this.virtTree = [].concat([]);
                    this.$nextTick(() => {
                        this.echartTem();
                    })
                } else {
                    this.editStatus = true;
                    this.getEditData();
                }
            },
            //绑定拖拽事件
            echartTem() {
                let self = this
                for (let index = 0; index < this.chartData.length; index++) {
                    for (let ix = 0; ix < this.chartData[index].data.length; ix++) {
                        if (!document.getElementById('display-chart-box-' + index + '-' + ix)) continue;
                        new Sortable(document.getElementById('display-chart-box-' + index + '-' + ix), Object.assign({
                            group: {
                                name: 'tem',
                                pull: true,
                                put: false
                            },
                            animation: 150,
                            handle: '.display-chart-box',
                            onRemove: function (evt) {
                                let a = parseInt(evt.target.dataset.a);
                                let b = parseInt(evt.target.dataset.b);
                                $(evt.item).remove();
                                self.chartData[a].data[b].selected = true;
                                self.virtTree.splice(evt.newIndex, 0, {
                                    data_type: self.chartData[a].data_type,
                                    type: 'echart',
                                    id: new Date().getTime(),
                                    params: self.chartData[a].data[b]
                                });
                            }
                        }))
                    }
                }
            },
//            截取数组前五
            splice_tool(arr) {
                if (!arr.length) return arr;
                if (arr.length <= 5) {
                    return arr;
                } else {
                    return arr.slice(0, 5)
                }
            }
        },
        components: {
            chart
        }
    }
</script>