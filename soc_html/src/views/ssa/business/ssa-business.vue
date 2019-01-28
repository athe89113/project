<template>
    <div>
        <div class="global-wrap">
            <div class="global-head ys-box-con">
                <div class="global-title">
                    <p class="font14 textC">态势感知平台</p>
                </div>
                <div class="global-title m-t-5">
                    <p class="ys-info-color textC">业务态势</p>
                </div>
            </div>
            <div class="m-t-5 clearfix">
                <div class="col-md-8">
                    <!--<div class="location-map m-t-5" style="height:586px;">
                      <div v-if="charts.chart1.show" style="height:586px;" >
                        <div class="ys-box-title m-b-30">
                          更换地图
                          <a @click="settingChart(charts.chart1)" class="fRight pset"><i class="ys-icon icon-setting"></i></a>
                        </div>

                        <chart :type.sync="charts.chart1.type"
                          :unit.sync="charts.chart1.unit"
                          :show.sync="show"
                          :mapbox.sync="mapbox"
                          :mapchart.sync="mapchartText"
                          :mapdata.sync="charts.chart1.map_data">
                        </chart>
                      </div>
                      <div v-else>
                        <div class="ys-box-title">添加地图</div>
                        <div class="ys-box-con">
                          <div class="chartAdd" style="height:550px" @click="addChart(1)">
                          <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                          <p class="ys-info-color m-t-20">添加新图表</p>
                        </div>
                        </div>
                      </div>

                    </div>-->
                    <div class="ys-box m-t-5">
                        <div v-if="charts.chart1.show">
                            <div class="ys-box-title">
                                {{charts.chart1.name}}
                                <a @click="settingChart(charts.chart1)" class="fRight pset"><i
                                        class="ys-icon icon-setting"></i></a>
                            </div>
                            <div class="ys-box-con">
                                <chart :type.sync="charts.chart1.chart_type"
                                       :info.sync="charts.chart1.info"
                                       :name.sync="charts.chart1.name"
                                       :unit.sync="charts.chart1.unit"
                                       :tablechart="charts.chart1.tablechart"
                                       :box="box1"
                                       :show.sync="show"
                                       :mapchart.sync="mapchartText">
                                </chart>
                            </div>
                        </div>
                        <div v-else>
                            <div class="ys-box-title">未设置标题</div>
                            <div class="ys-box-con">
                                <div class="chartAdd" style="height:220px" @click="addChart(1)">
                                    <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                    <p class="ys-info-color m-t-20">添加新图表</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="ys-box m-t-5">
                        <div v-if="charts.chart2.show">
                            <div class="ys-box-title">
                                {{charts.chart2.name}}
                                <a @click="settingChart(charts.chart2)" class="fRight pset"><i
                                        class="ys-icon icon-setting"></i></a>
                            </div>
                            <div class="ys-box-con">
                                <chart :type.sync="charts.chart2.chart_type"
                                       :info.sync="charts.chart2.info"
                                       :name.sync="charts.chart2.name"
                                       :unit.sync="charts.chart2.unit"
                                       :tablechart="charts.chart2.tablechart"
                                       :box="box"
                                       :show.sync="show"
                                       :mapchart.sync="mapchartText">
                                </chart>
                            </div>
                        </div>
                        <div v-else>
                            <div class="ys-box-title">未设置标题</div>
                            <div class="ys-box-con">
                                <div class="chartAdd" style="height:220px" @click="addChart(2)">
                                    <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                    <p class="ys-info-color m-t-20">添加新图表</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!--<div class="ys-box m-t-5">
                      <div v-if="charts.chart3.show">
                        <div class="ys-box-title">{{charts.chart3.name}}<a @click="settingChart(charts.chart3)" class="fRight pset"><i class="ys-icon icon-setting"></i></a></div>
                        <div class="ys-box-con">
                            <chart :type.sync="charts.chart3.chart_type"
                          :info.sync="charts.chart3.info"
                          :name="charts.chart3.name"
                          :unit="charts.chart3.unit"
                          :tablechart="charts.chart3.tablechart"
                          :box="box"
                          :show.sync="show"
                          :mapchart.sync="mapchartText">
                          </chart>
                        </div>
                      </div>
                      <div v-else>
                        <div class="ys-box-title">未设置标题</div>
                        <div class="ys-box-con">
                          <div class="chartAdd" style="height:220px" @click="addChart(3)">
                          <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                          <p class="ys-info-color m-t-20">添加新图表</p>
                        </div>
                        </div>
                      </div>
                    </div>-->
                </div>
            </div>
            <div class="m-t-5 clearfix">
                <div class="col-md-4">
                    <div v-if="charts.chart4.show">
                        <div class="ys-box-title">{{charts.chart4.name}}<a @click="settingChart(charts.chart4)"
                                                                           class="fRight pset"><i
                                class="ys-icon icon-setting"></i></a></div>
                        <div class="ys-box-con">
                            <chart :type.sync="charts.chart4.chart_type"
                                   :info.sync="charts.chart4.info"
                                   :name="charts.chart4.name"
                                   :unit="charts.chart4.unit"
                                   :tablechart="charts.chart4.tablechart"
                                   :box="box"
                                   :show.sync="show"
                                   :mapchart.sync="mapchartText">
                            </chart>
                        </div>
                    </div>
                    <div v-else>
                        <div class="ys-box-title">未设置标题</div>
                        <div class="ys-box-con">
                            <div class="chartAdd" style="height:220px" @click="addChart(4)">
                                <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                <p class="ys-info-color m-t-20">添加新图表</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div v-if="charts.chart5.show">
                        <div class="ys-box-title">{{charts.chart5.name}}<a @click="settingChart(charts.chart5)"
                                                                           class="fRight pset"><i
                                class="ys-icon icon-setting"></i></a></div>
                        <div class="ys-box-con">
                            <chart :type.sync="charts.chart5.chart_type"
                                   :info.sync="charts.chart5.info"
                                   :name="charts.chart5.name"
                                   :unit="charts.chart5.unit"
                                   :tablechart="charts.chart5.tablechart"
                                   :box="box"
                                   :show.sync="show"
                                   :mapchart.sync="mapchartText">
                            </chart>
                        </div>
                    </div>
                    <div v-else>
                        <div class="ys-box-title">未设置标题</div>
                        <div class="ys-box-con">
                            <div class="chartAdd" style="height:220px" @click="addChart(5)">
                                <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                <p class="ys-info-color m-t-20">添加新图表</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div v-if="charts.chart6.show">
                        <div class="ys-box-title">{{charts.chart6.name}}<a @click="settingChart(charts.chart6)"
                                                                           class="fRight pset"><i
                                class="ys-icon icon-setting"></i></a></div>
                        <div class="ys-box-con">
                            <chart :type.sync="charts.chart6.chart_type"
                                   :info.sync="charts.chart6.info"
                                   :name="charts.chart6.name"
                                   :unit="charts.chart6.unit"
                                   :tablechart="charts.chart6.tablechart"
                                   :box="box"
                                   :show.sync="show"
                                   :mapchart.sync="mapchartText">
                            </chart>
                        </div>
                    </div>
                    <div v-else>
                        <div class="ys-box-title">未设置标题</div>
                        <div class="ys-box-con">
                            <div class="chartAdd" style="height:220px" @click="addChart(6)">
                                <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                <p class="ys-info-color m-t-20">添加新图表</p>
                            </div>
                        </div>
                    </div>
                </div>


            </div>
            <div class="m-t-5 clearfix">

                <div class="col-md-4">
                    <div v-if="charts.chart7.show">
                        <div class="ys-box-title">{{charts.chart7.name}}<a @click="settingChart(charts.chart7)"
                                                                           class="fRight pset"><i
                                class="ys-icon icon-setting"></i></a></div>
                        <div class="ys-box-con">
                            <chart :type.sync="charts.chart7.chart_type"
                                   :info.sync="charts.chart7.info"
                                   :name="charts.chart7.name"
                                   :unit="charts.chart7.unit"
                                   :tablechart="charts.chart7.tablechart"
                                   :box="box"
                                   :show.sync="show"
                                   :mapchart.sync="mapchartText">
                            </chart>
                        </div>
                    </div>
                    <div v-else>
                        <div class="ys-box-title">未设置标题</div>
                        <div class="ys-box-con">
                            <div class="chartAdd" style="height:220px" @click="addChart(7)">
                                <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                <p class="ys-info-color m-t-20">添加新图表</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div v-if="charts.chart8.show">
                        <div class="ys-box-title">{{charts.chart8.name}}<a @click="settingChart(charts.chart8)"
                                                                           class="fRight pset"><i
                                class="ys-icon icon-setting"></i></a></div>
                        <div class="ys-box-con">
                            <chart :type.sync="charts.chart8.chart_type"
                                   :info.sync="charts.chart8.info"
                                   :name="charts.chart8.name"
                                   :unit="charts.chart8.unit"
                                   :tablechart="charts.chart8.tablechart"
                                   :box="box"
                                   :show.sync="show"
                                   :mapchart.sync="mapchartText">
                            </chart>
                        </div>
                    </div>
                    <div v-else>
                        <div class="ys-box-title">未设置标题</div>
                        <div class="ys-box-con">
                            <div class="chartAdd" style="height:220px" @click="addChart(8)">
                                <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                <p class="ys-info-color m-t-20">添加新图表</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div v-if="charts.chart9.show">
                        <div class="ys-box-title">{{charts.chart9.name}}<a @click="settingChart(charts.chart9)"
                                                                           class="fRight pset"><i
                                class="ys-icon icon-setting"></i></a></div>
                        <div class="ys-box-con">
                            <chart :type.sync="charts.chart9.chart_type"
                                   :info.sync="charts.chart9.info"
                                   :name="charts.chart9.name"
                                   :unit="charts.chart9.unit"
                                   :tablechart="charts.chart9.tablechart"
                                   :box="box"
                                   :show.sync="show"
                                   :mapchart.sync="mapchartText">
                            </chart>
                        </div>
                    </div>
                    <div v-else>
                        <div class="ys-box-title">未设置标题</div>
                        <div class="ys-box-con">
                            <div class="chartAdd" style="height:220px" @click="addChart(9)">
                                <img class="m-t-40" src="../../../assets/images/ssac/add.png" alt="">
                                <p class="ys-info-color m-t-20">添加新图表</p>
                            </div>
                        </div>
                    </div>
                </div>


            </div>
        </div>
        <aside :show.sync="showAddUnit" :header="'选择图表'" :left="'auto'" :width="'622px'">
            <div class="m-b-15">
                <div class="ys-info-color ">
                    当前已有图表
                    <span style="color:#fff"> {{chartCount}} </span>个

                    <div class="ys-search d-i-b m-l-10">
                        <input type="text" placeholder="输入关键词查询" v-model="searchValue" @keyup.enter="tableRe()"
                               class="ys-input" style="width:180px;"
                        />
                        <button class="ys-search-btn top" @click="tableRe()">
                            <i class="ys-icon icon-search"></i>
                        </button>
                    </div>
                </div>
                <p class="ys-info-color m-t-20">
                    标签检索：
                    <span class="blue">
            <template v-for="item in tabList">
              <span v-if="$index!=0">|</span>
              <a @click="tabClick($index)" :class="{'ys-success-color':$index==tabIndex}">{{item}}</a>
            </template>
          </span>
                </p>
            </div>
            <div class="box-chart" v-for="item in forTable">
                <div class="ys-box-con Block" @click="selectChart(item,$index)" :class="{on:$index==selectId}">
                    <div class="chart-box-title">{{item.name}}</div>
                    <img v-if="item.chart_type=='pie'" src="../../../assets/images/ssac/pie.png" alt="">
                    <img v-if="item.chart_type=='bar'" src="../../../assets/images/ssac/bar_x.png" alt="">
                    <img v-if="item.chart_type=='bar_x'" src="../../../assets/images/ssac/bar_x.png" alt="">
                    <img v-if="item.chart_type=='bar_y'" src="../../../assets/images/ssac/bar_y.png" alt="">
                    <img v-if="item.chart_type=='line'" src="../../../assets/images/ssac/line.png" alt="">
                    <img v-if="item.chart_type=='table'" src="../../../assets/images/ssac/table.png" alt="">
                    <img v-if="item.chart_type=='map'" src="../../../assets/images/ssac/map.png" alt="">
                </div>
            </div>
            <div class="clear"></div>
            <table-data :url='tableUrl' :data.sync="forTable" :whole.sync="chartCount" :filter.sync="tableFilter"
                        :search.sync="searchValue"
                        v-ref:table>
            </table-data>

            <div class="clear">
                <button class="ys-btn m-r-10" @click="addData()">保存</button>
                <button class="ys-btn ys-btn-white" @click="showAddUnit=false">取消</button>
            </div>
        </aside>
    </div>
</template>
<style scoped>
    /* 侧边框 */

    .box-chart {
        float: left;
        width: 170px;
        height: 170px;
        margin-bottom: 10px;
        margin-right: 8px;
        overflow: hidden;
    }

    .box-chart .visit-total-box {
        width: 106px;
        height: 82px;
        margin: 0px auto;
        background: url("../../../assets/images/ssa/visit-total-bg.png") no-repeat;
        background-size: 100px;
    }

    .chart-box-title {
        margin-bottom: 14px;
        color: #fff
    }

    .Block {
        height: 170px;
        width: 170px;
    }

    .Block.on {
        border: solid 1px #00bd85;
    }

    .chartAdd {
        text-align: center;
        height: 220px;
    }

    .clear {
        height: 30px;
        clear: both;
    }

    .ys-search button.top {
        top: -1px;
    }

    /* 侧边框 end*/

    .global-title {
        width: 100%;
    }

    .location-map {
        background: -webkit-linear-gradient(top, transparent 9px, rgba(74, 146, 255, 0.12) 10px), -webkit-linear-gradient(left, transparent 9px, rgba(74, 146, 255, 0.12) 10px);
        background-size: 10px 10px;
        position: relative !important;
    }

    .visit-total-box {
        width: 166px;
        height: 153px;
        margin: 0px auto;
        background: url("../../../assets/images/ssa/visit-total-bg.png") no-repeat;
        background-size: 166px;
    }

    .visit-total-box .title {
        text-align: center;
        padding-top: 50px;
    }

    .visit-total-box .grade {
        text-align: center;
        margin-top: 10px;
    }
</style>
<script>
    import Api from 'src/lib/api'
    import chart from "../chart/chart";

    let echarts = require('echarts/lib/echarts');
    export default {
        name: "ssa-business",
        components: {
            chart
        },
        data() {
            return {
                charts: {
                    chart1: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "map",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart2: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart3: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart4: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart5: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart6: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart7: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart8: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart9: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                    chart10: {
                        show: false,
                        cell_id: null,
                        chart_type: '',
                        type: "bar",
                        name: "",
                        info: {
                            data: [],
                            labels: [],
                        },
                        unit: "",
                        tablechart: "",
                    },
                },
                mapbox: { // 地图图大小及名称
                    height: 450,
                    width: 640,
                    xName: '',
                    yName: ''
                },
                mapType: '',
                saveChart: false,
                dashborad_type: 2,
                cell_id: null,
                tableUrl: "/api/ssa/chart/dts",
                tableFilter: {
                    "type": {
                        id: "",
                        name: ""
                    },
                    //"order": {id: "change_time", name: "change_time"},
                    //"order_type": {id: "desc", name: "desc"},
                },
                searchValue: '',
                tableList: [],
                show: false,
                mapchartText: {
                    id: 1,
                    name: "北京市",
                    pinyin: "beijing",
                },
                box: {
                    width: 340,
                    height: 220,
                    xName: '',
                    yName: ''
                },
                box1: {
                    width: 640,
                    height: 220,
                    xName: '',
                    yName: ''
                },
                chartCount: 0, // 图表总数
                tabIndex: 0, // 头部索引
                tabList: [ // 头部列表
                    '默认全部',
                    '资源分析图表',
                    '业务分析图表',
                    '安全分析图表',
                ],
                selectCharts: {},
                selectId: null,
                BlockIndex: 0,
                intensifyList: [ //强化数据
                    // {  //1
                    //   name: '',
                    //   chart_type:{ id: "", name: "折线图" },
                    //   cycle:{ id: "1", name: "天" },
                    //   data:{ data:[], labels:[] },
                    //   unit: null,
                    //   tableChart: []
                    //   sort:1,
                    //   selected: false
                    // },
                ],
                levelData: [],
                curLevel: [],
                lineData: {
                    color: ['rgba(0,189,133,0.8)', 'rgba(233,97,87,0.8)', 'rgba(218,187,97,0.8)', 'rgba(74,146,255,0.8)']
                },
                // 添加
                forTable: [],
                showAddUnit: false,
                visitTrendIpData: {
                    name: ["IP"],
                    x: [],
                    color: ['#00bd85'],
                    series: [{
                        data: []
                    },]
                },
                visitTrendPvData: {
                    name: ["PV"],
                    x: [],
                    color: ['#4a92ff'],
                    series: [{
                        data: []
                    },]
                },
                visitCountData: {
                    count_now: 0,
                    count_today: 0
                },
                visitTop10Data: {
                    x: [],
                    y: []
                },
                visitBrowserData: [],
                visitLocationData: {
                    x: [],
                    y: []
                },
                visitOsData: [],
                floodTrendData: {
                    name: ["入口流量", "出口流量"],
                    x: [],
                    color: ['#e96157', "#4a92ff"],
                    series: [{
                        data: []
                    },
                        {
                            data: []
                        }
                    ]
                },
                visitTypeList: [{
                    id: 1,
                    name: "IP"
                },
                    {
                        id: 2,
                        name: "PV"
                    },
                ],
                curVisitType: {
                    id: 1,
                    name: "IP"
                },
            }
        },
        ready: function () {

            // this.getVisitCount()
            // this.getVisitTop10()
            // this.getVisitBrowser()
            // this.getVisitLocation()
            // this.getVisitOs()
            // this.getServerStatus()
            // this.getFloodTrend()
            // this.getVisitTrend()

            this.getData()
            this.getChartData()
            this.getFieldMapData()
        },
        methods: {
            getData() {
                this.$http.post('/api/ssa/chart/dts', {
                    type: this.tabIndex,
                    'search[value]': this.searchValue,
                    "start": 0,
                    "length": 10
                }).then((response) => {
                    let data = response.data.data;
                    this.chartCount = response.data.recordsTotal
                    this.listData = data
                    this.show = !this.show
                    this.getPerview(this.listData)
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getChartData(obj) {
                this.$http.get('/api/ssa/dashborad', {
                    dashborad_type: this.dashborad_type,
                    query_time: 7
                }).then((response) => {
                    this.$root.loadStatus = false;

                    if (response.data.status == 200) {
                        let data = response.data.data;
                        this.intensifyList = data.data;
                        data.data.forEach(e => {
                            this.getSortChart(e, 1)
                        })
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            tableRe() {
                this.$set('tableFilter.type', {
                    id: this.tabIndex,
                    name: this.tabIndex
                })
                this.$refs.table.Re()
            },
            getPerview(obj) {
                this.forTable = obj
            },
            getFieldMapData() {
                this.$http.get('/api/ssa/field_map').then(function (response) {
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
            getSortChart(item, index) {
                var _this = this;
                this.$http.post('/api/ssa/chart/perview', {
                    "name": item.name,
                    "chart_type": item.chart_type,
                    "data_tag": item.data_tag,
                    "limit": item.limit,
                    "query_time": item.query_time,
                    "styles": item.styles,
                    "x": item.x,
                    "y": item.y, "data_type": item.data_type
                }).then((response) => {
                    let data = response.data.data;

                    _this.charts['chart' + item.cell_order].name = item.name
                    _this.charts['chart' + item.cell_order].cell_id = item.cell_id,
                        _this.charts['chart' + item.cell_order].chart_type = item.chart_type
                    _this.charts['chart' + item.cell_order].show = true

                    Vue.set(_this.charts['chart' + item.cell_order], 'tablechart', {
                        x: {},
                        y: {}
                    })
                    Vue.set(_this.charts['chart' + item.cell_order], 'info', {
                        data: [],
                        labels: [],
                    })
                    Vue.set(_this.charts['chart' + item.cell_order], 'map_data', {
                        list: [],
                        map_text: '',
                        pinyin: item.map_type
                    })
                    if (item.chart_type == 'pie' && item.y.length == 1) {
                        let arr = [];
                        for (let key in data.y) {
                            for (let i in data.y[key]) {
                                arr.push(data.y[key][i])
                            }
                        }
                        for (let key in data.x) {

                            for (let i = 0; i < this.curLevel.length; i++) {
                                if (item.x[0].value == this.curLevel[i].name) {
                                    for (let t = 0; t < data.x[key].length; t++) {
                                        for (let j = 0; j < this.curLevel[i].list.length; j++) {
                                            if (data.x[key][t] == this.curLevel[i].list[j].id) {
                                                data.x[key][t] = this.curLevel[i].list[j].name
                                            }
                                        }
                                    }
                                }
                            }

                            let len = data.x[key].length;
                            for (let i = 0; i < len; i++) {
                                let obj = {};
                                obj.name = data.x[key][i]
                                obj.data = [arr[i]]
                                _this.charts['chart' + item.cell_order]["info"]["data"].push(obj)
                            }
                        }
                    } else if (item.chart_type == "map") {
                        _this.charts['chart' + item.cell_order]["map_data"]["list"] = [];
                        let arr = [];
                        for (let key in data.y) {
                            for (let i in data.y[key]) {
                                arr.push(data.y[key][i])
                            }
                            _this.charts['chart' + item.cell_order]["map_data"]["map_text"] = key
                        }
                        for (let key in data.x) {
                            let len = data.x[key].length;
                            for (let i = 0; i < len; i++) {
                                let obj = {};
                                obj.name = data.x[key][i] + '市'
                                obj.value = arr[i]
                                _this.charts['chart' + item.cell_order]["map_data"]["list"].push(obj)
                            }
                        }
                    } else {
                        let _item = item;
                        if (data != undefined) {
                            for (let item in data.y) {
                                let obj = {};
                                obj.name = item;
                                if (_item.chart_type == 'bar_y') {
                                    data.y[item].reverse();
                                }
                                obj.data = data.y[item]
                                _this.charts['chart' + _item.cell_order].info.data.push(obj)
                            }
                        }
                        if (item.styles.unit != undefined) {
                            _this.charts['chart' + _item.cell_order]['unit'] = item.styles.unit
                        }

                        _this.charts['chart' + _item.cell_order]["tablechart"]["x"] = data.x;
                        _this.charts['chart' + _item.cell_order]["tablechart"]["y"] = data.y;
                    }
                    try {
                        for (let key in data.x) {
                            _this.charts['chart' + item.cell_order]["info"]["labels"] = data.x[key];
                        }
                        if (item.chart_type == 'bar_y') {
                            _this.charts['chart' + item.cell_order]["info"]["labels"].reverse();
                        }
                    } catch (e) {

                    }
                    this.show = !this.show
                }, function () {

                })
            },
            tabClick(i) {
                this.tabIndex = i
                this.tableRe()
                this.getData()
            },
            addDate() {

            },
            addData() {
                /*if(this.BlockIndex==1&&this.selectCharts.chart_type!='map'){
                  this.$root.alertError = true;
                  this.$root.errorMsg = '请添加地图类型'
                  return false;
                } else if(this.mapType=="map"&&this.selectCharts.chart_type!='map'){
                  this.$root.alertError = true;
                  this.$root.errorMsg = '请添加地图类型'
                  return false;
                }*/
                if (!this.saveChart) {
                    this.$http.post('/api/ssa/dashborad/chart', {
                        dashborad_type: this.dashborad_type,
                        chart_id: this.selectCharts.id,
                        order: this.BlockIndex
                    }).then((response) => {
                        if (response.status == 200) {
                            this.$root.alertSuccess = true;
                            this.showAddUnit = false
                            this.getChartData();
                        } else {
                            this.$root.alertError = true;
                        }
                        this.$root.errorMsg = response.msg
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                } else {
                    this.$http.put('/api/ssa/dashborad/chart', {
                        dashborad_type: this.dashborad_type,
                        chart_id: this.selectCharts.id,
                        cell_id: this.cell_id
                    }).then((response) => {
                        if (response.status == 200) {
                            this.$root.alertSuccess = true;
                            this.showAddUnit = false
                            this.getChartData();
                        } else {
                            this.$root.alertError = true;
                        }
                        this.$root.errorMsg = response.msg
                    }, function (response) {
                        Api.user.requestFalse(response, this);
                    })
                }
            },
            addChart(index) {
                this.saveChart = false;
                this.BlockIndex = index
                this.showAddUnit = !this.showAddUnit
            },
            settingChart(obj) {
                this.mapType = obj.type
                this.saveChart = true;
                this.cell_id = obj.cell_id
                this.showAddUnit = !this.showAddUnit
            },
            selectChart(obj, i) {
                this.selectId = i
                this.selectCharts = obj
            },
            getVisitCount() {
                this.$http.get('/api/ssa/business/visit_count').then(function (response) {
                    if (response.data.status == 200) {
                        this.visitCountData = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getVisitTop10() {
                this.$http.get('/api/ssa/business/visit_top10').then(function (response) {
                    if (response.data.status == 200) {
                        let data = response.data.data;
                        this.visitTop10Data.x = data.y.splice(0, 5).reverse();
                        this.visitTop10Data.y = data.x.splice(0, 5).reverse();
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getVisitBrowser() {
                this.$http.get('/api/ssa/business/visit_browser').then(function (response) {
                    if (response.data.status == 200) {
                        this.visitBrowserData = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getVisitLocation() {
                this.$http.get('/api/ssa/business/visit_location').then(function (response) {
                    if (response.data.status == 200) {
                        this.visitLocationData = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getVisitOs() {
                this.$http.get('/api/ssa/business/visit_os').then(function (response) {
                    if (response.data.status == 200) {
                        this.visitOsData = response.data.data;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getFloodTrend() {
                this.$http.get('/api/ssa/business/flow_trend').then(function (response) {
                    if (response.data.status == 200) {
                        let data = response.data.data;
                        this.floodTrendData.x = data.x;
                        this.floodTrendData.series[0].data = data.in;
                        this.floodTrendData.series[1].data = data.out;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getServerStatus() {
                this.$http.get('/api/ssa/business/server_status').then(function (response) {
                    if (response.data.status == 200) {
                        let statusData = response.data.data;
                        let yData = statusData.domain;
                        let serverStatusChart = echarts.init(document.getElementById('ssa-business-server-status-chart'));
                        let serverStatusOption = {
                            tooltip: {
                                trigger: 'axis',
                                axisPointer: { // 坐标轴指示器，坐标轴触发有效
                                    type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
                                }
                            },
                            grid: {
                                top: '10',
                                bottom: '20',
                                left: 10,
                                right: 10,
                                containLabel: true
                            },
                            color: ["#4b8aed", "#d45d55", "#cdaf5f", "#00bd85", "#1464ed"],
                            xAxis: {
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
                                splitLine: {
                                    lineStyle: {
                                        color: "#46578e",
                                        opacity: "0.75"
                                    }
                                },
                                axisLabel: {
                                    textStyle: {
                                        color: "#93a6d8"
                                    }
                                }, //x轴坐标的字颜色
                            },
                            yAxis: {
                                type: 'category',
                                data: yData,
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
                                axisLabel: {
                                    textStyle: {
                                        color: "#93a6d8"
                                    }
                                }, //x轴坐标的字颜色
                            },
                            series: [{
                                name: '2xx',
                                type: 'bar',
                                stack: '总量',
                                barWidth: '20',
                                barGap: 20,
                                data: statusData['2xx']
                            },
                                {
                                    name: '3xx',
                                    type: 'bar',
                                    stack: '总量',
                                    data: statusData['3xx']
                                },
                                {
                                    name: '4xx',
                                    type: 'bar',
                                    stack: '总量',
                                    data: statusData['4xx']
                                },
                                {
                                    name: '5xx',
                                    type: 'bar',
                                    stack: '总量',
                                    data: statusData['5xx']
                                },
                            ]
                        };
                        serverStatusChart.setOption(serverStatusOption);
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            getVisitTrend() {
                this.$http.get('/api/ssa/business/visit_trend').then(function (response) {
                    if (response.data.status == 200) {
                        let data = response.data.data;
                        this.visitTrendIpData.x = data.x;
                        this.visitTrendPvData.x = data.x;
                        this.visitTrendIpData.series[0].data = data.pv;
                        this.visitTrendPvData.series[0].data = data.uv;
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
        }
    }
</script>
