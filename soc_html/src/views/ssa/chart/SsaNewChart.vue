<template>
    <div class="ys-con pos-r">
        <div class="">
            <p class="ys-info-color m-b-10">创建报表模板</p>
            <div class="m-b-10">
                <ys-select :option="eventSourceType"
                           :select-id.sync="curEventType"
                           @change="fetchDatabase(curEventType)"
                ></ys-select>

                <ys-select :option="defenceNodes"
                           :select-id.sync="defenceNodeId"
                           @change="fetchDatabase(defenceNodeId)"
                ></ys-select>
                <ys-select :option="eventSourceData" :selected.sync="curEventSource"></ys-select>
            </div>
        </div>
        <div class="">
            <div class="box-left">
                <div class="ys-box-con m-b-10">
                    <div class="m-b-5 clear Dimensions">
                        <div class="fLeft">
                            <span class="m-r-5 m-t-12 ys-info-color fLeft">横轴维度(x):</span>
                            <div class="d-i-b fLeft">
                                <div class="tag-box" v-for="list in xData" track-by="$index">
                                    <div class="ys-tag" @mouseover="list.remove=true" @mouseout="list.remove=false">
                                        <span v-if="list.order.id=='asc'"><i
                                                class="ys-icon icon-sort-asc m-r-5"></i></span>
                                        <span v-if="list.order.id=='desc'"><i class="ys-icon icon-sort-desc m-r-5"></i></span>
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
                        </div>
                        <div class="fRight disbut">
                            <a @click="showXConfig()"><i class="ys-icon icon-setting"></i> 设置维度</a>
                        </div>
                    </div>
                    <div class="clear Dimensions">
                        <div class="fLeft">
                            <span class="m-r-5 m-t-12 ys-info-color fLeft">纵轴维度(y):</span>
                            <div class="d-i-b fLeft">
                                <div class="tag-box" v-for="list in yData" track-by="$index">
                                    <div class="ys-tag" @mouseover="list.remove=true" @mouseout="list.remove=false">
                                        <span v-if="list.order.id=='asc'"><i
                                                class="ys-icon icon-sort-asc m-r-5"></i></span>
                                        <span v-if="list.order.id=='desc'"><i class="ys-icon icon-sort-desc m-r-5"></i></span>
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
                        </div>
                        <div class="fRight disbut">
                            <a @click="showYConfig()"><i class="ys-icon icon-setting"></i> 设置数值</a>
                        </div>
                    </div>
                    <div class="clear"></div>
                </div>
                <div class="ys-box-con chartMain">
                    <div class="pageHead">
                        <div class="pageTitle fLeft">
                            <span class="ys-info-color">设置显示数组：</span>
                            <span class="por">
                    <i class="ys-icon icon-arrow-left pal" @click="updateValue(-1)"></i>
                    <input type="text" placeholder=""
                           v-model="limit" @change="getChartData()"
                           class="ys-input special" style="width:68px;"/>
                    <i class="ys-icon icon-arrow-right par" @click="updateValue(1)"></i>
                </span>
                            <!-- <span class="ys-info-color">(图表全部数据28组)</span> -->
                        </div>
                        <div class="box-chart" v-if="xyChange">
                            <chart
                                    :id="'myChart'"
                                    :type="TchartType"
                                    :datas="datas"
                                    :info.sync="list.data"
                                    :name="list.name"
                                    :show.sync="show"
                                    :box="box"
                                    :unit="unit"
                                    :tablechart="tableChart"
                                    :mapchart.sync="mapchartText"
                                    :mapbox.sync="mapbox"
                                    :mapdata.sync="map_data">
                            </chart>
                        </div>
                    </div>
                </div>
                <div class="box-right chartSilde">
                    <div class="box-scroll">
                        <div class="ys-box-title">图表编辑面板</div>
                        <div class="ys-box-con m-b-2">
                            <div class="pageHead">
                                <span class="verticalM ys-info-color">图表标题 </span>
                                <input type="text" placeholder="未命名图表名称" class="ys-input" v-model="chartTitle">
                            </div>
                        </div>
                        <div class="ys-box-con m-b-2">
                            <div class="pageHead">
                                <span class="verticalM ys-info-color">更换图表类型:</span>
                                <a class="fRight" @click="chartTypeShow=!chartTypeShow">
                                    <i v-if="!chartTypeShow" class="ys-icon icon-downlist"></i>
                                    <i v-else class="ys-icon icon-downlist-up"></i>
                                </a>
                            </div>
                            <div class="d-i-b clear m-t-30" v-show="chartTypeShow">
                                <span v-for="item in ChartTypeList" class="m-r-15 d-i-b">
                                    <tooltip :content="item.title" :delay="0">
                                        <a><i class="ys-icon"
                                              :class="[item.icon,{'ys-success-color':$index==TchartTypeId}]"
                                              @click="TchartTypes(item,$index)"></i></a>
                                    </tooltip>
                                </span>
                                <div class="m-t-15" v-if="mapShow">
                                    <ys-select :option="mapchart" :select-id.sync="mapchartId"
                                               @change="upCity(mapchartId)"></ys-select>
                                </div>

                            </div>
                        </div>
                        <!-- <div class="ys-box-con m-b-2">
                            <div class="pageHead">
                                <span class="verticalM ys-info-color">图表选项</span>
                                <a class="fRight" @click="chartOptionShow=!chartOptionShow">
                                    <i v-if="!chartOptionShow" class="ys-icon icon-downlist"></i>
                                    <i v-else class="ys-icon icon-downlist-up"></i>
                                </a>
                                <div class="ys-box-con m-t-15" v-if="chartOptionShow">
                                    <p class="m-b-20"><checkbox :show.sync="false" :text="'显示数据标签'"></checkbox></p>
                                    <p><checkbox :show.sync="boxNameShow" :text="'显示坐标轴名称'" @click="boxNameXY"></checkbox></p>
                                    <div v-if="boxNameShow">
                                        <p><input class="ys-input m-t-10" style="width:272px" placeholder="横轴名称" v-model="box.xName"/></p>
                                        <p><input class="ys-input m-t-10" style="width:272px" placeholder="纵轴名称" v-model="box.yName"/></p>
                                    </div>
                                    <div class="pageHead m-t-30">
                                        <span class="verticalM ys-info-color">添加数据标注</span>
                                        <a class="fRight" @click="addFile">
                                            <i class="ys-icon icon-setting"></i> 添加
                                        </a>
                                        <ul class="datalist m-t-10">
                                            <li v-for="list in screen">
                                                <div class="box-min-l">
                                                    <div v-if="screenIndex != list.id" class="ys-info-color p-l-10">{{list.name}}</div>
                                                    <div v-else>
                                                        <input type="text"
                                                        style="width:170px"
                                                        class="ys-input"
                                                        placeholder="添加标签"
                                                        v-model="screenText">
                                                    </div>
                                                </div>
                                                <div class="box-min-r">
                                                    <template v-if="screenIndex != list.id">
                                                        <tooltip :content="'编辑配置'">
                                                            <a @click="EditName(list)" class="m-5"><i class="ys-icon icon-edit"></i></a>
                                                        </tooltip>

                                                        <ys-poptip confirm
                                                                title="您确认删除这条内容吗？"
                                                                :placement="$index%difference==0?'right':'left'"
                                                                @on-ok="deleteFile(list,$index)">
                                                            <a class="ys-error-color m-5"><i class="ys-icon icon-trash"></i></a>
                                                        </ys-poptip>
                                                    </template>
                                                    <div class="textC operate" v-else>
                                                        <tooltip :content="'取消'">
                                                            <a @click="removeFile(list,true)"><i class="glyphicon glyphicon-remove text-cursorr"></i></a>
                                                        </tooltip>
                                                        <tooltip :content="'确定'">
                                                            <a @click="removeFile(list,false)"><i class="glyphicon glyphicon-ok text-cursor"></i></a>
                                                        </tooltip>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div> -->
                        <div class="ys-box-con m-b-2">
                            <span class="verticalM ys-info-color">数据筛选</span>
                            <a class="fRight" @click="dataOptionShow=!dataOptionShow">
                                <i v-if="!dataOptionShow" class="ys-icon icon-downlist"></i>
                                <i v-else class="ys-icon icon-downlist-up"></i>
                            </a>
                            <!-- <span class="verticalM ys-info-color">添加数据标注</span>
                            <a class="fRight"><i class="ys-icon icon-setting"></i> 添加筛选条件</a> -->
                            <div v-if="dataOptionShow">
                                <ul class="timeList clear m-t-15">
                                    <li class="fLeft timeOption"
                                        v-for="item in timeList"
                                        :class="{'on':$index==curSwitchId}"
                                        @click="changeSwitchTab($index,'time')">
                                        {{item.name}}
                                    </li>
                                </ul>
                                <!--<ul class="unitList clear m-t-15" >-->
                                <!--<li class="fLeft unitOption"-->
                                <!--v-for="item in unitList"-->
                                <!--:class="{'on':$index==unitSwitchId}"-->
                                <!--@click="changeSwitchTab($index,'unit')">-->
                                <!--{{item.name}}-->
                                <!--</li>-->
                                <!--</ul>-->
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="ys-box-con clear save m-t-10">
            <div class="fRight d-i-b">
                <button class="ys-btn ys-btn-s ys-btn-blue m-r-6" @click="chartEmpty">清空</button>
                <button class="ys-btn ys-btn-s ys-btn-green" @click="chartSave">保存</button>
            </div>
        </div>
        <aside :show.sync="showConfigStatus" :header="'设置筛选条件'" :width="'600px'" :left="'auto'">
            <!--<div class="broadside ys-info-color">-->
            <!--<i class="ys-icon icon-warn-outline"></i> 默认识别第一个日期型字段-->
            <!--</div>-->
            <table class="ys-form-table">
                <tr>
                    <td style="padding-top:1px;">D日期型字段：</td>
                    <td>
            <span v-for="list in coordFieldData" style="width:210px;" class="d-i-b" v-show="list.type=='date'">
              <checkbox :text="list.name" :show.sync="list.selected"></checkbox>
            </span>
                    </td>
                </tr>
                <tr>
                    <td class="verticalT" style="padding-top:11px;">T文本字段：</td>
                    <td>
            <span v-for="list in coordFieldData" style="width:210px;" class="d-i-b m-b-10" v-show="list.type=='string'">
              <checkbox :text="list.name" :show.sync="list.selected"></checkbox>
            </span>
                    </td>
                </tr>
                <tr>
                    <td class="verticalT" style="padding-top:11px;">#数值字段：</td>
                    <td>
            <span v-for="list in coordFieldData" style="width:210px;" class="d-i-b m-b-10" v-show="list.type=='int'">
              <checkbox :text="list.name" :show.sync="list.selected"></checkbox>
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
    </div>
</template>
<script>
    import chart from "src/components/chart/chart";
    import ysRadio from 'src/components/radio.vue'
    import Api from 'src/lib/api'

    export default {
        name: 'newChart',
        components: {
            chart,
            ysRadio
        },
        data() {
            return {
                chartTitle: '未定义', //图表标题
                arr: [], // 纵坐标数组
                show: false, // 刷新视图
                box: { // 视图大小及名称
                    height: 450,
                    width: 640,
                    xName: '',
                    yName: ''
                },
                mapbox: { // 地图图大小及名称
                    height: 450,
                    width: 640,
                    xName: '',
                    yName: ''
                },
                datas: {},
                unit: 'number',
                chart_id: null, //编辑id
                chartTypeShow: true, // 数据图表类型
                chartOptionShow: true, // 图表选项
                dataOptionShow: true, // 数据筛选
                ChartTypeList: [  // 图表种类
                    {id: 'bar_y', icon: 'icon-chart-bar-horizontal', title: '条形图'},
                    {id: 'line', icon: 'icon-chart-line', title: '折线图'},
                    {id: 'pie', icon: 'icon-chart-pie', title: '饼形图'},
                    {id: 'bar_x', icon: 'icon-chart-bar', title: "柱状图"},
                    {id: 'table', icon: 'icon-chart-table', title: '表格'},
                    {id: 'scatter', icon: 'icon-chart-punch', title: '散点图'},
                    {id: 'bar_pile_x', icon: 'icon-chart-bar', title: '堆叠柱状图'},
                    {id: 'bar_pile_y', icon: 'icon-chart-bar-horizontal', title: '堆叠条形图'},
                ],
                tableChart: null, // table数据
                limit: 0, // 显示条数
                mapchartId: 0, // 地图编辑
                mapShow: false,
                mapchartText: {
                    id: 1,
                    name: "北京市",
                    pinyin: "beijing",
                },
                map_type: 'beijing',
                map_data: {
                    map_text: '',
                    list: []
                },
                mapchart: [
                    {id: 1, name: '北京市', pinyin: 'beijing'},
                    {id: 2, name: '天津市', pinyin: 'tianjin'},
                    {id: 3, name: '上海市', pinyin: 'shanghai'},
                    {id: 4, name: '重庆市', pinyin: 'chongqing'},
                    {id: 5, name: '河北省', pinyin: 'hebei'},
                    {id: 6, name: '山西省', pinyin: 'shanxi'},
                    {id: 7, name: '辽宁省', pinyin: 'liaoning'},
                    {id: 8, name: '吉林省', pinyin: 'jilin'},
                    {id: 9, name: '黑龙江省', pinyin: 'heilongjiang'},
                    {id: 10, name: '江苏省', pinyin: 'jiangsu'},
                    {id: 11, name: '浙江省', pinyin: 'zhejiang'},
                    {id: 12, name: '安徽省', pinyin: 'anhui'},
                    {id: 13, name: '福建省', pinyin: 'fujian'},
                    {id: 14, name: '江西省', pinyin: 'jiangxi'},
                    {id: 15, name: '山东省', pinyin: 'shandong'},
                    {id: 16, name: '河南省', pinyin: 'henan'},
                    {id: 17, name: '湖北省', pinyin: 'hubei'},
                    {id: 18, name: '湖南省', pinyin: 'hunan'},
                    {id: 19, name: '广东省', pinyin: 'guangdong'},
                    {id: 20, name: '海南省', pinyin: 'hainan'},
                    {id: 21, name: '四川省', pinyin: 'sichuan'},
                    {id: 22, name: '贵州省', pinyin: 'guizhou'},
                    {id: 23, name: '云南省', pinyin: 'yunnan'},
                    {id: 24, name: '陕西省', pinyin: 'shanxi2'},
                    {id: 25, name: '甘肃省', pinyin: 'gansu'},
                    {id: 26, name: '青海省', pinyin: 'qinghai'},
                    {id: 27, name: '台湾省', pinyin: 'taiwan'},
                    {id: 28, name: '内蒙古自治区', pinyin: 'neimenggu'},
                    {id: 29, name: '广西壮族自治区', pinyin: 'guangxi'},
                    {id: 30, name: '西藏自治区', pinyin: 'xizang'},
                    {id: 31, name: '宁夏回族自治区', pinyin: 'neimenggu'},
                    {id: 32, name: '新疆维吾尔自治区', pinyin: 'xinjiang'},
                    {id: 33, name: '香港特别行政区', pinyin: 'hongkong'},
                    {id: 34, name: '澳门特别行政区', pinyin: 'macao'}
                ], // 地图图表城市
                xyChange: true, // xy轴数据变更
                TchartType: 'line', // 确认图表类型
                TchartTypeId: 1, // 默认选中图
                curSwitchId: 1,
                timeList: [{'id': 1, name: '过去24小时', disable: false}, {
                    'id': 7,
                    name: '过去7天',
                    disable: false
                }, {'id': 30, name: '过去30天', disable: false}],
                unitSwitchId: 0,
                unitList: [{'id': 0, name: '数值', text: 'number'}, {'id': 1, name: '流量', text: 'band'}],
                boxNameShow: true, // 是否显示坐标轴名称
                valueListX: [ // 筛选数值
                    {id: 1, name: '平均值'},
                    {id: 2, name: '最大值'},
                    {id: 3, name: '最小值'}
                ],
                valueIdX: {id: 1, name: '平均值'},
                screen: [ // 数据标注
                    {
                        id: '2',
                        name: '备注说明特别数据1'
                    },
                    {
                        id: '3',
                        name: '备注说明特别数据2'
                    },
                ],
                screenText: '',
                screenIndex: null, // 数据标注索引
                defenceNodes: [
                    // {id:0,name:"默认"},
                    {id: 1, name: "资源分析", type: 1},
//                {id:2,name:"业务分析",type:2},
                    {id: 2, name: "安全分析", type: 2},
                ], // 头部标签
                defenceNodeId: 1,
                eventSourceType: [{id: 1, name: "日志"}, {id: 2, name: "事件"}],
                curEventType: 1,
                chartX: [],
                chartY: [],
                configType: "X",
                coordFieldData: [{selected: false}],
                showConfigStatus: false,
                addData: {
                    name: ''
                },
                location: '',
                locations: '',
                eventSourceData: [], // 维度设置
                order: '',
                curEventSource: {},
                fieldMapData: {},
                levelData: [],
                curLevel: [],
                xData: [],
                yData: [],
                conditionIndex: 1,
                chartTypeData: [
                    {id: "bar_x", name: "柱状图"},
                    {id: "bar_y", name: "条形图"},
                    {id: "line", name: "折线图"},
                    {id: "pie", name: "饼形图"},
                    {id: "number", name: "合计数"},
                ],
                timeDataList: [
                    {id: "month", name: "按月"},
                    {id: "week", name: "按周"},
                    {id: "day", name: "按日"},
                    // {id:"hour",name:"按时"},
                    // {id:"minute",name:"按分"},
                    // {id:"second",name:"按秒"}
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
                list: {
                    name: '',
                    chart_type: {
                        id: "line",
                        name: "折线图"
                    },
                    cycle: {
                        id: "1",
                        name: "天"
                    },
                    data: {
                        data: [],
                        labels: []
                    },
                    sort: 1,
                },
                setNumber: 0,
                editStatusx: false,
                editStatusy: false,
            }
        },
        watch: {
            'box.xName': function () {
                this.show = !this.show
            },
            'box.yName': function () {
                this.show = !this.show
            },
            'curEventSource': function () {
                this.getFieldData();
                // this.$set('conditionList', []);
            },
            'tableList': function () {
                this.refreshTable();
            },
            'xData': function (val) {
                if (val.length >= 1 && this.yData.length >= 1) {
                    if (this.editStatusx) {
                        this.editStatusx = false;
                    } else {
                        this.getChartData();
                    }
                } else {
//                    this.datas = {};
                    this.xyChange = false
//                    this.show = !this.show;
                }
            },
            'yData': function (val) {
                if (val.length >= 1 && this.xData.length >= 1) {
                    if (this.editStatusy) {
                        this.editStatusy = false;
                    } else {
                        this.getChartData();
                    }
                } else {
//                    this.datas = {};
                    this.xyChange = false;
//                    this.show = !this.show;
                }
            },
            'datas': function () {
                if (this.datas.y) {
                    try {
                        if (JSON.stringify(Object.keys(this.datas.y)).indexOf('流量') != -1) {
                            this.unit = 'band'
                        } else if (JSON.stringify(Object.keys(this.datas.y)).indexOf('文件大小') != -1) {
                            this.unit = 'band'
                        } else if (JSON.stringify(Object.keys(this.datas.y)).indexOf('时间') != -1) {
                            this.unit = 'time'
                        } else {
                            this.unit = 'number'
                        }
                    } catch (e) {
                        this.unit = 'number'
                    }
                } else {
                    this.unit = 'number'
                }
            },
            'curEventType': function (val) {
                this.chart_id = this.$route.query.chart_item_id
                if (this.chart_id != null && this.chart_id.length > 0) {
                    this.setNumber++;
                    if (this.setNumber > 1) {
                        this.resetFull();
                    }
                } else {
                    this.resetFull();
                    this.getEventSourceData(0);
                }
                this.getFieldMapData();
            }
        },
        ready() {
            $('.box-scroll').slimScroll({
                height: '677',
                position: 'right',
                size: "5px",
                color: '#000',
                wheelStep: 5
            });
            this.chart_id = this.$route.query.chart_item_id;
            for (let key in this.timeList) {
                if (this.timeList[key].id == this.$route.query.search_time) {
                    this.curSwitchId = key;
                }
            }
            if (this.chart_id != null && this.chart_id.length > 0) {
                this.editStatusx = true;
                this.editStatusy = true;
                this.EditChart();
            } else {
                this.getEventSourceData(0);
            }
            this.getFieldMapData();
        },
        methods: {
            resetFull() {
                this.chartX = [].concat([]);
                this.chartY = [].concat([]);
                this.yData = [].concat([]);
                this.xData = [].concat([]);
                this.datas = Object.assign({});
                this.info = Object.assign({});
                this.show = !this.show
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
                let url = '';
                if (this.curEventType == 1) url = '/api/ssa/event/select/list';
                if (this.curEventType == 2) url = '/api/ssa/event/analysis_select_search/list';
                this.$http.post(url, {tag: this.curEventSource.id}).then(function (response) {
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
                let url = '';
                if (this.curEventType == 1) url = '/api/ssa/event/select/list';
                if (this.curEventType == 2) url = '/api/ssa/event/analysis_select_search/list';
                this.$http.post(url, {tag: this.curEventSource.id}).then(function (response) {
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
            addXData() {
                for (let key in this.coordFieldData) {
                    if (this.coordFieldData[key].selected) {
                        if (this.coordFieldData[key].type == 'date') {
                            this.xData.push(this.coordFieldData[key]);
                            Vue.set(this.xData[this.xData.length - 1], 'order', {id: "default", name: "默认排序"})
                            Vue.set(this.xData[this.xData.length - 1], 'condition', {id: "day", name: "按日"})
                            Vue.set(this.xData[this.xData.length - 1], 'show', false)
                            Vue.set(this.xData[this.xData.length - 1], 'remove', false)
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
            editXData(coordFieldData) {
                for (let tab in this.chartX) {
                    var name, number, BerName, id, order, orderName;
                    if (this.chartX[tab].type == "date") {
                        id = this.chartX[tab].value;
                        number = '@timestamp';
                        name = "时间"
                        if (this.chartX[tab].value == 'month') {
                            BerName = "按月"
                        } else if (this.chartX[tab].value == "howeekur") {
                            BerName = "按周"
                        } else if (this.chartX[tab].value == 'day') {
                            BerName = "按日"
                        } else if (this.chartX[tab].value == "hour") {
                            BerName = "按时"
                        } else if (this.chartX[tab].value == 'minute') {
                            BerName = "按分"
                        } else if (this.chartX[tab].value == "second") {
                            BerName = "按秒"
                        }
                        var obj = {
                            id: number,
                            name: name,
                            type: 'date',
                            condition: {
                                id: id, name: BerName
                            },
                            order: {
                                id: "", name: ""
                            },
                            show: false,
                            remove: false,
                        };
                        this.xData.push(obj);
                    } else {
                        for (let x in coordFieldData) {
                            if (this.chartX[tab].value == coordFieldData[x].id || this.chartX[tab].type == coordFieldData[x].type) {
                                name = coordFieldData[x].name;
                                number = coordFieldData[x].id;
                            }
                        }
                        order = this.chartX[tab].order;
                        if (this.chartX[tab].order == "asc") {
                            orderName = "升序"
                        } else if (this.chartX[tab].order == "desc") {
                            orderName = "降序"
                        } else {
                            orderName = "默认排序"
                        }
                        var obj = {
                            id: number,
                            name: name,
                            type: this.chartX[tab].type,
                            condition: {
                                id: '', name: ''
                            },
                            order: {
                                id: order, name: orderName
                            },
                            show: false,
                            remove: false,
                        };
                        this.xData.push(obj);
                    }
                }
            },
            editYData(coordFieldData) {
                for (let tab in this.chartY) {
                    var name, number, BerName, id, order, orderName;
                    for (let x in coordFieldData) {
                        if (this.chartY[tab].value == coordFieldData[x].id || this.chartY[tab].type == coordFieldData[x].type) {
                            name = coordFieldData[x].name;
                            number = coordFieldData[x].id;
                            id = this.chartY[tab].aggregator;
                            if (this.chartY[tab].value == coordFieldData[x].id) {
                                order = this.chartY[tab].order;
                                if (this.chartY[tab].order == "asc") {
                                    orderName = "升序"
                                } else if (this.chartY[tab].order == "desc") {
                                    orderName = "降序"
                                } else {
                                    orderName = "默认排序"
                                }

                                if (this.chartY[tab].aggregator == 'SUM') {
                                    BerName = '求和';
                                } else if (this.chartY[tab].aggregator == 'AVG') {
                                    BerName = "平均值"
                                }
                                else if (this.chartY[tab].aggregator == 'MAX') {
                                    BerName = "最大值"
                                }
                                else if (this.chartY[tab].aggregator == 'MIN') {
                                    BerName = "最小值"
                                }
                                else if (this.chartY[tab].aggregator == 'COUNT') {
                                    BerName = "计数"
                                }
                                else if (this.chartY[tab].aggregator == 'DISTINCT') {
                                    BerName = "去重计数"
                                }
                            }
                        }
                    }
                    var obj = {
                        id: number,
                        name: name,
                        condition: {
                            id: id, name: BerName
                        },
                        order: {
                            id: order, name: orderName
                        },
                        show: false,
                        remove: false,
                    }
                    this.yData.push(obj);
                }
            },
            upCity(options) {
                let op = this.mapchart[options - 1];
                this.mapchartText = op
                this.map_type = op.pinyin
                this.getChartData()
            },
            EditChart() {
                this.$http.get('/api/ssa/chart/' + this.chart_id).then(function (response) {
                    let res = response.data;
                    if (res.status == 200) {
                        if (this.curEventType == res.data.data_type) {
                            this.setNumber++;
                        }
                        this.curEventType = Number(res.data.data_type);
                        this.getEventSourceData(res.data.data_tag).then(() => {
                            this.chartX = [], this.chartY = [];
                            this.chartTitle = res.data.name;
                            this.TchartType = res.data.chart_type;
                            this.defenceNodeId = Number(res.data.type);
                            this.timeList[this.curSwitchId].id = res.data.query_time;
                            this.limit = res.data.limit;
                            this.chartX = res.data.x;
                            this.chartY = res.data.y;
                            this.unit = res.data.styles.unit;
                            if (this.unit == 'band') {
                                this.unitSwitchId = 1;
                            }
                            ;
                            let chart_ids = res.data.chart_type;

                            let params = {
                                "name": this.chartTitle,
                                "chart_type": this.TchartType,
                                "data_tag": res.data.data_tag,
                                "query_time": this.timeList[this.curSwitchId].id,
                                "limit": this.limit,
                                "styles": {
                                    unit: this.unit
                                },
                                "x": this.chartX,
                                "y": this.chartY,
                                "data_type": this.curEventType
                            }
                            delete params.map_type;
                            if (chart_ids == 'bar_y') {
                                this.TchartTypeId = 0
                            } else if (chart_ids == 'line') {
                                this.TchartTypeId = 1
                            } else if (chart_ids == 'pie') {
                                this.TchartTypeId = 2
                                this.limit = 10;
                            } else if (chart_ids == 'bar_x') {
                                this.TchartTypeId = 3
                            } else if (chart_ids == 'table') {
                                this.TchartTypeId = 4
                                this.limit = 5
                            } else if (chart_ids == 'scatter') {
                                this.TchartTypeId = 5
                                this.timeList = [{'id': 1, name: '过去24小时', disable: true}, {
                                    'id': 7,
                                    name: '过去7天',
                                    disable: false
                                }, {'id': 30, name: '过去30天', disable: true}];
                            } else if (chart_ids == 'bar_pile_x') {
                                this.TchartTypeId = 6
                            } else if (chart_ids == 'bar_pile_y') {
                                this.TchartTypeId = 7
                            }
                            let url = '';
                            if (this.curEventType == 1) url = '/api/ssa/event/select/list';
                            if (this.curEventType == 2) url = '/api/ssa/event/analysis_select_search/list';
                            this.$http.post(url, {tag: res.data.data_tag}).then(function (response) {
                                let coordFieldData = Object.assign({}, response.data.items);
                                for (let i in this.chartX) {
                                    for (let x in coordFieldData) {
                                        if (this.chartX[i].value == coordFieldData[x].id || this.chartX[i].type == coordFieldData[x].type) {
                                            coordFieldData[x].selected = true;
                                        }
                                    }
                                }
                                this.$set("coordFieldData", coordFieldData);
                                for (let x in coordFieldData) {
                                    coordFieldData[x].selected = false;
                                }
                                this.editYData(coordFieldData);
                                this.editXData(coordFieldData);
                                this.$nextTick(() => {
                                    this.xyChange = false;
                                    this.$http.post('/api/ssa/chart/perview', params).then((response) => {
                                        if (response.data.status == 200) {
                                            let data = response.data.data;
                                            this.tableChart = data;
                                            this.list.data.data = [];
                                            this.chartCount = response.data.recordsTotal
                                            if (data == undefined || data.y == undefined) {
                                                return false
                                            }
                                            if (this.TchartTypeId == 2 && this.chartY.length == 1) {

                                                let arr = [];
                                                for (let key in data.y) {
                                                    for (let i in data.y[key]) {
                                                        arr.push(data.y[key][i])
                                                    }
                                                }
                                                for (let key in data.x) {
                                                    let len = data.x[key].length;
                                                    for (let i = 0; i < len; i++) {
                                                        let obj = {};
                                                        obj.name = data.x[key][i]
                                                        obj.data = [arr[i]]
                                                        this.list.data.data.push(obj)
                                                    }
                                                }
                                                this.list.data.data.slice(0, 20)

                                            } else {
                                                for (let item in data.y) {
                                                    let obj = {}
                                                    obj.name = item;
                                                    obj.data = data.y[item]
                                                    this.list.data.data.push(obj)
                                                }
                                            }
                                            for (let key in data.x) {
                                                this.list.data.labels = data.x[key];
                                            }
                                            this.limit = this.list.data.labels.length;
                                            this.$nextTick(() => {
                                                this.xyChange = true;
                                                this.datas = Object.assign({}, data);
                                            })
                                        } else {
                                            this.datas = {};
                                            this.xyChange = true;
                                        }
                                    }, function (response) {
                                        this.datas = {};
                                        this.xyChange = true;
                                        Api.user.requestFalse(response, this);
                                    })
                                })
                            }, function (response) {
                                Api.user.requestFalse(response, this);
                            })
                        });
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getFieldMapData() {
                let url = ''
                if (this.curEventType == 1) url = '/api/ssa/field_map';
                if (this.curEventType == 2) url = '/api/ssa/event/analysis_field_map';
                this.$http.get(url).then(function (response) {
                    this.fieldMapData = response.data.data;
                    for (let key in this.fieldMapData) {
                        if (this.fieldMapData[key].items.length > 0) {
                            this.levelData = {name: key, list: this.fieldMapData[key].items};
                            this.curLevel.push(this.levelData);
                        }
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getChartData() {
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
                let yList = [], zeroType = null;
                for (let x in this.yData) {
                    zeroType = this.yData[x].order.id
                    yList.push({
                        aggregator: this.yData[x].condition.id,
                        value: this.yData[x].id,
                        order: this.yData[x].order.id == 'default' ? '' : zeroType
                    })
                }
                this.chartX = xList
                this.chartY = yList
                this.box.height = 450;
                let params = {
                    "name": this.chartTitle,
                    "chart_type": this.TchartType,
                    // "map_type": this.map_type,
                    "limit": this.limit,
                    "data_tag": this.curEventSource.id,
                    "query_time": this.timeList[this.curSwitchId].id,
                    "styles": {
                        unit: this.unit
                    },
                    "x": this.chartX,
                    "y": this.chartY,
                    "data_type": this.curEventType
                };
                if (this.TchartTypeId == 4) {
                    if (this.limit == 0) {
                        this.limit = 10
                    }
                    if (this.yData.length + this.xData.length > 5) {
                        this.$root.alertError = true;
                        this.$root.errorMsg = '表格最多显示前5列数据';
                        return false
                    }

                }
                this.chartX = xList;
                this.chartY = yList;
                this.$http.post('/api/ssa/chart/perview', params).then((response) => {
                    if (response.data.status == 200) {
                        let data = response.data.data;
                        this.datas = Object.assign({}, response.data.data);
                        this.tableChart = data;
                        this.list.data.data = [];
                        this.chartCount = response.data.recordsTotal
                        if (data == undefined || data.y == undefined) {
                            return false
                        }
                        for (let key in data.x) {

                            for (let i = 0; i < this.curLevel.length; i++) {
                                if (xList[0].value == this.curLevel[i].name) {
                                    for (let t = 0; t < data.x[key].length; t++) {
                                        for (let j = 0; j < this.curLevel[i].list.length; j++) {
                                            if (data.x[key][t] == this.curLevel[i].list[j].id) {
                                                data.x[key][t] = this.curLevel[i].list[j].name
                                            }
                                        }
                                    }
                                }
                            }

                            this.list.data.labels = data.x[key];
                        }
                        if (this.TchartTypeId == 2 && this.chartY.length == 1) {
                            let arr = [];
                            for (let key in data.y) {
                                for (let i in data.y[key]) {
                                    arr.push(data.y[key][i])
                                }
                            }
                            for (let key in data.x) {
                                let len = data.x[key].length;
                                for (let i = 0; i < len; i++) {
                                    let obj = {};
                                    obj.name = data.x[key][i]
                                    obj.data = [arr[i]]
                                    this.list.data.data.push(obj)
                                }
                            }
                        } else {
                            for (let item in data.y) {
                                let obj = {}
                                obj.name = item;
                                if (this.TchartTypeId == 0) {
                                    data.y[item].reverse()
                                    this.list.data.labels.reverse()
                                }
                                obj.data = data.y[item]
                                this.list.data.data.push(obj)
                            }
                        }
                        this.limit = this.list.data.labels.length;
                        this.show = !this.show
                        this.xyChange = true;
                    } else {
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg;
                        this.datas = {};
                        this.xyChange = true;
                    }
                }, function (response) {
                    this.datas = {};
                    this.xyChange = true;
                    Api.user.requestFalse(response, this);
                })
            },
            getFieldData() {
                let url = '';
                if (this.curEventType == 1) url = '/api/ssa/event/select/list';
                if (this.curEventType == 2) url = '/api/ssa/event/analysis_select_search/list';
                this.$http.post(url, {tag: this.curEventSource.id}).then(function (response) {
                    if (response.data.status == 200) {
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
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getEventSourceData(index) {
                return new Promise((resolve) => {
                    let url = '';
                    if (this.curEventType == 1) url = '/api/ssa/event/tags/list';
                    if (this.curEventType == 2) url = '/api/ssa/event/analysis_tags/list';
                    this.$http.post(url).then(function (response) {
                        this.eventSourceData = response.data.items;
                        if (index == 0) this.curEventSource = this.eventSourceData[index];
                        if (index != 0) {
                            for (let i = 0; i < response.data.items.length; i++) {
                                if (response.data.items[i].id == index) {
                                    this.curEventSource = response.data.items[i];
                                }
                            }
                        }
                        resolve();
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                })
            },
            TchartTypes(obj, index) {
                this.xyChange = false;
                this.TchartTypeId = index
                this.TchartType = obj.id
                this.limit = 10;
                if (this.TchartType == 'scatter') {
                    this.mapShow = false;
                    if (this.xData.length == 0) return false;
                    this.timeList = [{'id': 1, name: '过去24小时', disable: true}, {
                        'id': 7,
                        name: '过去7天',
                        disable: false
                    }, {'id': 30, name: '过去30天', disable: true}]
                } else {
                    this.timeList = [{'id': 1, name: '过去24小时', disable: false}, {
                        'id': 7,
                        name: '过去7天',
                        disable: false
                    }, {'id': 30, name: '过去30天', disable: false}],
                        this.mapShow = false;
                }
                this.getChartData()
            },
            updateValue(index) {
                this.limit = index + parseInt(this.limit);
                if (this.limit < 0) {
                    this.limit = 0
                }
                this.getChartData()
            },
            addUnit() {
                this.showConfigStatus = false;
                this.addData.location = this.location.id
                let data = this.addData;
                this.$http.post('/api/assets/unit', data).then(function (response) {
                    if (response.data.status == 200) {
                        this.$root.alertSuccess = true;
                        this.showConfigStatus = false;
                        this.tableRe();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            changeSwitchTab(index, tab) {
                if (tab == "time") {
                    this.curSwitchId = index
                    if (index == 0) {
                        this.timeDataList = [
                            {id: "hour", name: "按时"},
                            {id: "minute", name: "按分"},
                            //{id:"second",name:"按秒"}
                        ]
                    } else {
                        this.timeDataList = [
                            {id: "month", name: "按月"},
                            {id: "week", name: "按周"},
                            {id: "day", name: "按日"},
                        ]
                    }
                } else if (tab == "unit") {
                    this.unitSwitchId = index
                    this.unit = this.unitList[this.unitSwitchId].text
                }
                this.getChartData()
            },
            EditName(obj) {  // 编辑标注
                this.screenText = obj.name;
                this.screenIndex = obj.id;
            },
            addFile() {  // 添加数据标注
                let obj = {
                    id: 1,
                    name: '新增'
                }
                if (this.screenIndex === 1) {
                    return false
                }
                this.screenIndex = 1;
                this.screen.unshift(obj)
            },
            deleteFile(item, i) {
                if (this.screenIndex === 1) return false
                this.loadGlobal = true
                this.screen.splice(i, 1)
                this.loadGlobal = false
            },
            removeFile(item, bl) {  // 确认标注
                let oldName = item.name;
                if (bl) {
                    if (item.name != '') {
                        if (item.newFile == true) {
                            this.screen.shift()
                        }
                        item.name = oldName
                    } else {
                        this.screen.shift()
                    }
                    this.screenIndex = 0
                } else {
                    item.name = this.screenText
                    if (this.screenText == "") {
                        this.$root.errorMsg = '文件夹名称不能为空'
                        this.$root.alertError = true;
                        return false;
                    }
                    if (this.screenText == oldName) {
                        this.screenIndex = 0
                        return false;
                    }
                    if (this.screenText != item.name && this.screenText != "") {//修改
                        this.loadGlobal = true
                        this.screenIndex = 0
                    }
                }
            },
            chartSave() { // 图表保存
                if (this.TchartTypeId == 4 && this.limit > 5) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '表格只保留前5条数据'
                    this.limit = 5;
                    return false
                }

                if (this.TchartTypeId == 2 && this.limit > 10) {
                    this.$root.alertError = true;
                    this.$root.errorMsg = '饼图最多前10条数据';
                    this.limit = 10;
                    return false
                }
                var params = { // 修改
                    "name": this.chartTitle,
                    "chart_type": this.TchartType,
                    "type": Number(this.defenceNodeId),
                    'limit': this.limit,
                    "data_tag": this.curEventSource.id,
                    "query_time": this.timeList[this.curSwitchId].id,
                    "styles": {
                        unit: this.unit
                    },
                    "x": this.chartX,
                    "y": this.chartY,
                    'data_type': this.curEventType
                };
                // echarts.init(document.getElementById(this.id))
                // chart.getDataURL({ pixelRatio: 2})

                if (this.chart_id != null && this.chart_id.length > 0) {
                    this.$http.put('/api/ssa/chart/' + this.chart_id, params).then(function (response) {
                        let res = response.data;
                        if (res.status == 200) {
                            this.$root.alertSuccess = true;
                            this.$root.errorMsg = response.data.msg
                        } else {
                            this.$root.alertError = true;
                            this.$root.errorMsg = response.data.msg
                        }
                    })
                } else {
                    this.$http.post('/api/ssa/chart', params).then(function (response) {
                        let res = response.data;
                        if (res.status == 200) {
                            this.$root.alertSuccess = true;
                            this.$root.errorMsg = response.data.msg
                        } else {
                            this.$root.alertError = true;
                            this.$root.errorMsg = response.data.msg
                        }
                    })
                }

            },
            chartEmpty() { // 图表清空
                this.defenceNodeId = 1
                this.chartTitle = '';
                //this.box.xName = '';
                //this.box.yName = '';
                this.list.data.data = [];
                this.list.data.labels = [];
                this.$root.alertSuccess = true;
                this.$root.errorMsg = '清除成功'
                this.show = !this.show
            },
            fetchDatabase(nodeId) {
                this.showConfigStatus = false
            },
        }
    }
</script>
<style scoped>
    .m-b-2 {
        margin-bottom: 2px;
    }

    .m-t-12 {
        margin-top: 12px;
    }

    .box-left {
        margin-right: 340px;
    }

    .box-right {
        top: 64px;
        width: 334px;
    }

    .box-min-l, .box-min-r {
        height: 36px;
        line-height: 36px;
        background: rgba(0, 0, 0, 0.15)
    }

    .box-min-l {
        float: left;
        width: 180px;
    }

    .box-min-r {
        float: right;
        width: 92px;
        text-align: center;
    }

    .box-chart {
        min-height: 200px;
        clear: both;
    }

    .pageHead {
        clear: both;
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

    .Dimensions {
        height: 30px;
    }

    .disbut {
        margin-top: 6px;
    }

    .clear {
        clear: both;
    }

    .clear.save {
        height: 50px;
    }

    .chartMain {
        min-height: 572px;
    }

    .chartSilde {
        height: 677px;
    }

    .broadside {
        margin-bottom: 27px;
    }

    .icon-downlist, .icon-downlist-up {
        color: #00bd85;
    }

    .datalist li {
        height: 36px;
        line-height: 36px;
        margin-bottom: 5px;
        clear: both;
    }

    .timeList {
        margin: 10px 12px 0 0;
        height: 26px;
        line-height: 26px;
        width: 224px;
        background: rgba(0, 0, 0, 0.15);
        border-radius: 5px;
        cursor: pointer;
    }

    .unitList {
        margin: 10px 12px 0 0;
        height: 26px;
        line-height: 26px;
        width: 156px;
        background: rgba(0, 0, 0, 0.15);
        border-radius: 5px;
        cursor: pointer;
    }

    .unitOption {
        border-radius: 5px;
        width: 50%;
        text-align: center;
        color: #93a6d8;
    }

    .timeOption {
        border-radius: 5px;
        width: 33.33%;
        text-align: center;
        color: #93a6d8;
    }

    .timeOption.on {
        background: #437dd9;
        color: #fff;
        border-radius: 5px;
    }

    .unitOption.on {
        background: #437dd9;
        color: #fff;
        border-radius: 5px;
    }

    .por {
        position: relative;
    }

    .por i {
        position: absolute;
        color: #437dd9;
        cursor: pointer;
    }

    .pal {
        top: 4px;
        left: 4px;
    }

    .par {
        top: 4px;
        right: 4px;
    }

    .special {
        padding: 0 20px;
        text-align: center
    }
</style>
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

    .tag-box {
        position: relative;
        display: inline-block;
        margin-right: 10px;
        margin-top: 5px;
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
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 15px;
        padding-top: 10px;
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
