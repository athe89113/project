<template>
    <div class="Ssource">
        <div class="ys-box-con chart-header">
            当前已有图表{{chartCount}}个
            标签检索：<span class="blue">
      <template v-for="item in tabList">
        <span v-if="$index!=0">|</span>
        <a @click="tabClick($index)" :class="{'ys-success-color':$index==tabIndex}">{{item}}</a>
      </template>
      </span>
            <div class="fRight d-i-b">
                <!-- <a class="m-r-5" href="javascript:;" @click="sort('query_time')">
                  <i class="ys-icon icon-time-sort" :class="classTime"></i>
                时间</a> -->
                <a class="m-r-5" href="javascript:;" @click="sort('name')">
                    <i class="ys-icon icon-name-sort" :class="className"></i>
                    名称</a>
                <div class="ys-search d-i-b m-l-10">
                    <input type="text" placeholder="输入关键词查询"
                           v-model="searchValue"
                           @keyup.enter="tableRe()"
                           class="ys-input" style="width:180px;"/>
                    <button class="ys-search-btn top" @click="tableRe()"><i class="ys-icon icon-search"></i></button>
                </div>
            </div>
        </div>
        <div class="grid">
            <div class="col-md-6 m-t-10 item" :data-id='index' v-for="obj in intensifyList">
                <div class="item-content display-chart-box">
                    <div class="title clearfix">
                        <span @click="list.selected=!list.selected">{{obj.name}}</span>
                        <div class="fRight d-i-b">
                            <ul class="timeList">
                                <li class="fLeft timeOption"
                                    :class="{'on':obj.query_time==1}"
                                    @click="changeSwitchTab(obj,1)">
                                    过去24小时
                                </li>
                                <li class="fLeft timeOption"
                                    :class="{'on':obj.query_time==7}"
                                    @click="changeSwitchTab(obj,7)">
                                    过去7天
                                </li>
                                <li class="fLeft timeOption"
                                    :class="{'on':obj.query_time==30}"
                                    @click="changeSwitchTab(obj,30)">
                                    过去30天
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="box-chart">
                        <chart :type="obj.chart_type"
                               :info="obj.data"
                               :datas="obj.datas"
                               :name="obj.name"
                               :box="box"
                               :show.sync="obj.show"
                               :unit="obj.unit"
                               :tablechart="obj.tablechart"
                               :mapchart.sync="mapchartText"
                               :mapbox.sync="mapbox"
                               :mapdata.sync="obj.map_data"
                        ></chart>
                    </div>
                    <div class="fRight m-r-15" v-if="true">
                        <!-- <tooltip :content="'文件下载'" class="m-r-10">
                          <a @click="download(list)"><i class="ys-icon icon-download"></i></a>
                        </tooltip> -->
                        <!-- {{obj.data.labels}} -->
                        <tooltip :content="'编辑'" class="m-r-10">
                            <a @click="EditName(obj)"><i class="ys-icon icon-edit"></i></a>
                        </tooltip>
                        <ys-poptip confirm
                                   title="您确认删除这条内容吗？"
                                   :placement="'left'"
                                   @on-ok="Vremove(obj)">
                            <a class="ys-error-color"><i class="ys-icon icon-trash"></i></a>
                        </ys-poptip>
                    </div>
                </div>
            </div>
            <div class="clear"></div>
            <table-data :url='tableUrl'
                        :data.sync="intensifyList"
                        :whole.sync="chartCount"
                        :filter.sync="tableFilter"
                        :search.sync="searchValue"
                        v-ref:table>
            </table-data>
        </div>
    </div>
</template>
<style scoped>
    .clear {
        clear: both;
    }

    .grid {
        position: relative;
        margin: 0 -8px;
    }

    .chart-header {
        /* width: calc(100% - 16px); */
        line-height: 38px;
        height: 68px;
    }

    .chart-header .blue {
        color: #5ca9e5
    }

    .item {
        /* position: absolute; */
        height: 324px;
        z-index: 1;
        color: #fff;
    }

    .item.muuri-item-dragging {
        z-index: 3;
    }

    .item.muuri-item-releasing {
        z-index: 2;
    }

    .item.muuri-item-hidden {
        z-index: 0;
    }

    .item-content {
        position: relative;
        width: 100%;
        height: 100%;
    }

    .col-md-6 {
        padding: 0 8px !important;
    }

    .ys-search button.top {
        top: 5px;
    }

    .display-chart-box {
        border: 1px solid rgba(74, 146, 255, 0.25);
        background: rgba(0, 0, 0, 0.15);
        /* position: relative; */
    }

    .display-chart-box .box-chart {
        margin-top: 20px;
    }

    .display-chart-box .title {
        height: 36px;
        line-height: 36px;
        padding-left: 15px;
    }

    .display-chart-box .title:before {
        content: '';
        width: 232px;
        height: 36px;
        background: url('../../../assets/images/ys-display-box-title-tag.png');
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
        padding-top: 40px;
    }

    .display-chart-box .con .description {
        position: absolute;
        bottom: 15px;
        left: 15px;
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

    .flipy {
        -moz-transform: scaleY(-1);
        -webkit-transform: scaleY(-1);
        -o-transform: scaleY(-1);
        transform: scaleY(-1);
    }

    .ys-search-btn {
        top: 4px;
    }
</style>
<script>
    // import "https://cdn.bootcss.com/web-animations/2.3.1/web-animations.min.js"
    // import "http://hammerjs.github.io/dist/hammer.min.js"
    // import "https://cdnjs.cloudflare.com/ajax/libs/muuri/0.5.4/muuri.min.js"
    import Vue from 'vue';
    import Api from 'src/lib/api';
    import chart from "src/components/chart/chart";
    import ysRadio from 'src/components/radio.vue'

    var _ = require('lodash');
    let echarts = require('echarts/lib/echarts');
    export default {
        name: "ssa-source",
        components: {
            chart,
            ysRadio
        },
        data() {
            return {
                tableUrl: "/api/ssa/chart/dts",
                tableFilter: {
                    "type": {id: "", name: ""},
                    //"order": {id: "change_time", name: "change_time"},
                    //"order_type": {id: "desc", name: "desc"},
                },
                tableList: [],
                listIndex: 4,
                chartCount: 0, // 图表总数
                curSwitchId: 1, // 时间切换
                timeList: [{'id': '1', name: '过去24小时'}, {'id': '2', name: '过去7天'}, {'id': '3', name: '过去30天'}],
                tabIndex: 0, // 头部索引
                tabList: [ // 头部列表
                    '默认全部',
                    '资源分析图表',
                    '安全分析图表',
                ],
                searchValue: '',
                classTime: { // 搜索图片旋转样式
                    'flipy': false
                },
                className: {
                    'flipy': false
                },
                show: false,
                levelData: [],
                curLevel: [],
                box: {
                    width: 400,
                    height: 240,
                    xName: '',
                    yName: ''
                },
                mapbox: { // 地图图大小及名称
                    height: 240,
                    width: 400,
                    xName: '',
                    yName: ''
                },
                mapchartText: {
                    id: 1,
                    name: "北京市",
                    pinyin: "beijing",
                },
                map_type: 'quangguo',
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
                    {id: 11, name: '江苏省', pinyin: 'jiangsu'},
                    {id: 12, name: '浙江省', pinyin: 'zhejiang"'},
                    {id: 13, name: '安徽省', pinyin: 'anhui'},
                    {id: 14, name: '福建省', pinyin: 'fujian'},
                    {id: 15, name: '江西省', pinyin: 'jiangxi'},
                    {id: 16, name: '山东省', pinyin: 'shandong'},
                    {id: 17, name: '河南省', pinyin: 'henan'},
                    {id: 18, name: '湖北省', pinyin: 'hubei'},
                    {id: 19, name: '湖南省', pinyin: 'hunan'},
                    {id: 20, name: '广东省', pinyin: 'guangdong'},
                    {id: 21, name: '海南省', pinyin: 'hainan'},
                    {id: 22, name: '四川省', pinyin: 'sichuan'},
                    {id: 23, name: '贵州省', pinyin: 'guizhou'},
                    {id: 24, name: '云南省', pinyin: 'yunnan'},
                    {id: 25, name: '陕西省', pinyin: 'shanxi2'},
                    {id: 26, name: '甘肃省', pinyin: 'gansu'},
                    {id: 27, name: '青海省', pinyin: 'qinghai'},
                    {id: 28, name: '台湾省', pinyin: 'taiwan'},
                    {id: 29, name: '内蒙古自治区', pinyin: 'neimenggu'},
                    {id: 30, name: '广西壮族自治区', pinyin: 'guangxi'},
                    {id: 31, name: '西藏自治区', pinyin: 'xizang'},
                    {id: 32, name: '宁夏回族自治区', pinyin: 'neimenggu'},
                    {id: 33, name: '新疆维吾尔自治区', pinyin: 'xinjiang'},
                    {id: 34, name: '香港特别行政区', pinyin: 'hongkong'},
                    {id: 35, name: '澳门特别行政区', pinyin: 'macao'}
                ], // 地图图表城市
                order_type: "asc",
                chartTypeData: [
                    {id: "bar_x", name: "柱状图"},
                    {id: "bar_y", name: "条形图"},
                    {id: "line", name: "折线图"},
                    {id: "pie", name: "饼形图"},
                    {id: "table", name: "列表"},
                    {id: "number", name: "合计数"},
                ],
                timeTypeData: [
                    {id: 1, name: "按天"},
                    {id: 7, name: "按周"},
                    {id: 30, name: "按月"},
                    {id: 90, name: "按季度"},
                    {id: 365, name: "按年"},
                ],
                TabL: [],
                showAddUnit: false,
                visitCountData: 0,
                hostWeakData: [],
                holeSeriousData: [],
                holeTypeData: [],
                riskWebsiteData: [],
                holeTop5Data: [],
                assetHoleData: {x: [], y: []},
                grid: null,
                intensifyList: [ //强化数据
                    {
                        name: 'string',
                        chart_type: {
                            id: "line",
                            name: "折线图"
                        },
                        cycle: {
                            id: "1",
                            name: "天"
                        },
                        unit: null, //单位
                        tablechart: {x: {}, y: {}}, // 表格
                        data: {
                            data: [],
                            labels: [],
                        },
                        map_data: {
                            map_text: '',
                            list: [],
                            pinyin: ''
                        },
                        sort: 1,
                        selected: false
                    }
                ],
            }
        },
        ready: function () {
            this.debouncedGetAnswer = _.debounce(function (val) {
                let len = val.length;
                for (let i = 0; i < len; i++) {
                    this.getPerview(val[i], i)
                }
                this.show = !this.show
            }, 1000)
            this.getFieldMapData()
        },
        methods: {
            debounce: function (func, wait, immediate) {
                // immediate默认为false
                var timeout, args, context, timestamp, result;
                var later = function () {
                    // 当wait指定的时间间隔期间多次调用_.debounce返回的函数，则会不断更新timestamp的值，导致last < wait && last >= 0一直为true，从而不断启动新的计时器延时执行func
                    var last = _.now() - timestamp;

                    if (last < wait && last >= 0) {
                        timeout = setTimeout(later, wait - last);
                    } else {
                        timeout = null;
                        if (!immediate) {
                            result = func.apply(context, args);
                            if (!timeout) context = args = null;
                        }
                    }
                };
                return function () {
                    context = this;
                    args = arguments;
                    timestamp = _.now();
                    // 第一次调用该方法时，且immediate为true，则调用func函数
                    var callNow = immediate && !timeout;
                    // 在wait指定的时间间隔内首次调用该方法，则启动计时器定时调用func函数
                    if (!timeout) timeout = setTimeout(later, wait);
                    if (callNow) {
                        result = func.apply(context, args);
                        context = args = null;
                    }
                    return result;
                };
            },
            saveChart() {
                let ChartArr = [];
                for (let i = 0; i < this.grid._items.length; i++) {
                    ChartArr.push(this.grid._items[i]._element.getAttribute('data-id'))
                }
            },
            tabClick(i) {
                this.tabIndex = i
                this.tableRe()
//                this.getData()
            },
            tableRe() {
                this.$set('tableFilter.type', {id: this.tabIndex, name: this.tabIndex})
                this.$refs.table.Re()
            },
            changeSwitchTab(item, index) {
                item.query_time = index
                let x = [], y = [];
                for (let i in item.x) {
                    let obj = {};
                    obj.type = item.x[i].type;
                    obj.value = item.x[i].value;
                    obj.order = '';
                    x.push(obj)
                }
                for (let i in item.y) {
                    let obj = {};
                    obj.aggregator = item.y[i].aggregator;
                    obj.value = item.y[i].value;
                    obj.order = '';
                    y.push(obj)
                }
                let _this = this;
                this.$http.post('/api/ssa/chart/perview', {
                    "name": item.name,
                    "chart_type": item.chart_type,
                    "data_tag": item.data_tag,
                    "query_time": item.query_time,
                    "styles": item.styles,
                    "x": x,
                    "y": y,
                    "data_type": item.data_type
                }).then((response) => {
                    if (response.data.status == 200) {
                        let data = response.data.data;
                        // Vue.set(item,'data',{
                        //   data:[],
                        //   labels: []
                        // })
                        item["data"]["data"] = [];
                        item["data"]["labels"] = [];
                        for (let i in data.y) {
                            let obj = {}
                            obj.name = i;
                            obj.data = data.y[i]
                            item["data"]["data"].push(obj)
                        }
                        try {
                            for (let key in data.x) {
                                for (let i = 0; i < this.curLevel.length; i++) {
                                    if (x[0].value == this.curLevel[i].name) {
                                        for (let t = 0; t < data.x[key].length; t++) {
                                            for (let j = 0; j < this.curLevel[i].list.length; j++) {
                                                if (data.x[key][t] == this.curLevel[i].list[j].id) {
                                                    data.x[key][t] = this.curLevel[i].list[j].name
                                                }
                                            }
                                        }
                                    }
                                }
                                item["data"]["labels"] = data.x[key];
                            }
                        } catch (e) {

                        }
                        item["show"] = !item["show"]
                    } else if (response.data.status == 500) {
                        item["data"]["data"] = [].concat([]);
                        item["data"]["labels"] = [].concat([]);
                        item["tablechart"]["x"] = {};
                        item["tablechart"]["y"] = {};
                        this.$root.alertError = true;
                        this.$root.errorMsg = response.data.msg;
                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })

            },
            getData() {
                this.$http.post('/api/ssa/chart/dts', {
                    type: this.tabIndex,
                    'search[value]': this.searchValue,
                }).then((response) => {
                    let data = response.data.data;
                    this.chartCount = response.data.recordsTotal
                    this.intensifyList = data
                    for (let i = 0; i < this.intensifyList.length; i++) {
                        this.getPerview(this.intensifyList[i], i)
                    }
//                    this.show = !this.show
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
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
            getPerview(item, index) {
                let x = [], y = [];
                for (let i in item.x) {
                    let obj = {};
                    obj.type = item.x[i].type;
                    obj.value = item.x[i].value;
                    obj.order = item.x[i].order;
                    x.push(obj)
                }
                for (let i in item.y) {
                    let obj = {};
                    obj.aggregator = item.y[i].aggregator;
                    obj.value = item.y[i].value;
                    obj.order = item.y[i].order;
                    y.push(obj)
                }
                var params
                if (item.chart_type == "map") {
                    params = {
                        "name": item.name,
                        "chart_type": item.chart_type,
                        "data_tag": item.data_tag,
                        "map_type": item.map_type,
                        "limit": item.limit,
                        "query_time": item.query_time,
                        "styles": item.styles,
                        "x": x,
                        "y": y,
                        "data_type": item.data_type
                    };
                } else {
                    params = {
                        "name": item.name,
                        "chart_type": item.chart_type,
                        "data_tag": item.data_tag,
                        "limit": item.limit,
                        "query_time": item.query_time,
                        "styles": item.styles,
                        "x": x,
                        "y": y,
                        "data_type": item.data_type
                    };
                }
                let _this = this;
                this.$http.post('/api/ssa/chart/perview', params).then((response) => {
                    let data = response.data.data;

                    Vue.set(_this.intensifyList[index], 'tablechart', {
                        x: {}, y: {}
                    })
                    Vue.set(_this.intensifyList[index], 'data', {
                        data: [],
                        labels: [],
                    })
                    Vue.set(_this.intensifyList[index], 'show', false)
                    Vue.set(_this.intensifyList[index], 'map_data', {
                        list: [],
                        map_text: '',
                        pinyin: item.map_type
                    })
                    item["show"] = !item["show"]
                    if (item.chart_type == 'pie' && y.length == 1) {
                        let arr = [];
                        if (data != undefined) {
                            for (let key in data.y) {
                                for (let i in data.y[key]) {
                                    arr.push(data.y[key][i])
                                }
                            }
                            for (let key in data.x) {
                                for (let i = 0; i < this.curLevel.length; i++) {
                                    if (x[0].value == this.curLevel[i].name) {
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
                                    _this.intensifyList[index]["data"]["data"].push(obj)
                                }
                            }
                        }
                    } else if (item.chart_type == "map") {
                        // _this.intensifyList[index]["map_data"]["list"] = [];
                        // let arr = [];
                        // for(let key in data.y){
                        //     for(let i in data.y[key]){
                        //         arr.push(data.y[key][i])
                        //     }
                        //     _this.intensifyList[index]["map_data"]["map_text"] = key

                        // }
                        // for(let key in data.x){
                        //     let len = data.x[key].length;
                        //     for(let i=0; i<len;i++){
                        //         let obj = {};
                        //         obj.name = data.x[key][i]+'市'
                        //         obj.value = arr[i]
                        //         _this.intensifyList[index]["map_data"]["list"].push(obj)
                        //     }
                        // }
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
                                _this.intensifyList[index]["data"]["data"].push(obj)
                            }
                        }
                        if (item.styles.unit != undefined) {
                            _this.intensifyList[index]['unit'] = item.styles.unit
                        }

                        if (data != undefined) {
                            _this.intensifyList[index]["tablechart"]["x"] = data.x;
                            _this.intensifyList[index]["tablechart"]["y"] = data.y;
                        }
                    }
                    Vue.set(_this.intensifyList[index], 'datas', data)
                    try {
                        for (let key in data.x) {
                            _this.intensifyList[index]["data"]["labels"] = data.x[key];
                        }
                        if (item.chart_type == 'bar_y') {
                            _this.intensifyList[index]["data"]["labels"].reverse();
                        }
                    } catch (e) {

                    }
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            EditName(item) { //数据编辑
                this.$router.go({name: 'ssa-new-chart', query: {chart_item_id: item.id, search_time: item.query_time}})
            },
            sort(name) {
                if (name == "name") {
                    this.className.flipy == true ? this.className.flipy = false : this.className.flipy = true
                } else if (name == "query_time") {
                    this.classTime.flipy == true ? this.classTime.flipy = false : this.classTime.flipy = true
                }
                this.order_type == 'asc' ? this.order_type = 'desc' : this.order_type = 'asc';
                this.$http.post('/api/ssa/chart/dts', {
                    "type": this.tabIndex,
                    "order_field": name,
                    "order_type": this.order_type
                }).then((response) => {
                    let data = response.data.data;
                    this.chartCount = response.data.recordsTotal
                    this.intensifyList = data
                    this.show = !this.show
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })

            },
            Vremove(obj) {
                this.$http.delete('/api/ssa/chart/' + obj.id).then((response) => {
                    this.$root.loadStatus = false;
                    if (response.data.status == 200) {
                        this.getData()
                    } else {
                        this.$root.alertError = true;
                    }
                    this.$root.errorMsg = response.data.msg;
                }, function (response) {
                    Api.user.requestFalse(response, this);
                })
            },
            Vadd() {
                var itemElem = document.createElement('div');
                let index = this.listIndex++;
                itemElem.innerHTML = `<div class="col-md-6 m-t-10 item" data-id=${index}>
            <div class="item-content display-chart-box" id="mount-point${index}"></div>
          </div>`
                var b = itemElem.firstChild
                this.grid.add([b], {index: 0});
                this.Vhtml('mount-point' + index)
            },
            Vhtml(index) {
                let dataS = this._data;
                var Profile = Vue.extend({
                    template: `<div class="title clearfix">
          <div class="title clearfix">
            <span @click="list.selected=!list.selected">${index}<checkbox :show="list.selected" :text="list.name"></checkbox></span>
            <div class="fRight d-i-b">
              <a class="m-r-5" @click="changeOrderUp(list,chart.data)"><i class="ys-icon icon-num-arrow-up"></i></a>
              <a class="m-r-10" @click="changeOrderDown(list,chart.data)"><i class="ys-icon icon-num-arrow-down"></i></a>
              <checkbox :show.sync="list.has_table" :text="'显示表格'"></checkbox>
              <ys-select :option="chartTypeData"
                          :width="64"
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
          </div>
          <div class="box-chart">
            <chart :type="list.chart_type.id" :info="list.data" :name="list.name"></chart>
          </div>
        </div>`,
                    data() {
                        return dataS
                    },
                    components: {
                        chart,
                        ysRadio
                    },
                })
                new Profile().$mount('#' + index)
            }
        },
        watch: {
            'intensifyList': function (val) {
                this.debouncedGetAnswer(val)
            },
        },
    }
</script>
